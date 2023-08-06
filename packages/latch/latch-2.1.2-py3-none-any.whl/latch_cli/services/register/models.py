"""Models used in the register service."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import docker
import paramiko

import latch_cli.tinyrequests as tinyrequests
from latch_cli.config.latch import LatchConfig
from latch_cli.utils import (
    account_id_from_token,
    current_workspace,
    hash_directory,
    retrieve_or_login,
)

config = LatchConfig()
endpoints = config.sdk_endpoints


@dataclass
class RegisterOutput:
    """A typed structure to consolidate relevant values from the registration
    process.
    """

    build_logs: List[str] = None
    """Stdout/stderr from the container construction process."""
    serialize_logs: List[str] = None
    """Stdout/stderr from in-container serialization of workflow code."""
    registration_response: dict = None
    """JSON returned from the Latch API from a request to register serialized
    workflow code.
    """


class RegisterCtx:
    """This context object manages state for the lifetime of registration flow.

    The context holds values that are relevant throughout the "lifetime" of a
    registration, such as the location of local code and package name, as well
    as managing clients to interact with local docker servers and make remote HTTP
    requests.

    It also holds values extracted from early steps to be used later, eg. workflow
    version is parsed and stored so that it can be used in the API request for
    registration.

    Example: ::

        ctx = RegisterCtx(pkg_root)
        build_logs = _build_image(ctx, ...)
        serialize_logs = _serialize_pkg(ctx, ...)

    Args:
        pkg_root: Vaid path to root of workflow package,
        token: An optional JWT, only used for testing purposes.
    """

    dkr_repo: Optional[str] = None
    dkr_client: docker.APIClient = None
    ssh_client: paramiko.client.SSHClient = None
    key_material: Optional[str] = None
    pkg_root: Path = None  # root
    disable_auto_version: bool = False
    image_full = None
    token = None
    version = None
    serialize_dir = None
    latch_register_api_url = endpoints["register-workflow"]
    latch_image_api_url = endpoints["initiate-image-upload"]
    latch_provision_url = endpoints["provision-centromere"]

    def __init__(
        self,
        pkg_root: Path,
        token: Optional[str] = None,
        disable_auto_version: bool = False,
        remote: bool = False,
    ):

        if token is None:
            self.token = retrieve_or_login()
        else:
            self.token = token

        ws = current_workspace()
        if ws == "" or ws is None:
            self.account_id = account_id_from_token(self.token)
        else:
            self.account_id = ws

        self.pkg_root = Path(pkg_root).resolve()
        self.disable_auto_version = disable_auto_version
        try:
            version_file = self.pkg_root.joinpath("version")
            with open(version_file, "r") as vf:
                self.version = vf.read().strip()
            if not self.disable_auto_version:
                hash = hash_directory(self.pkg_root)
                self.version = self.version + "-" + hash[:6]
        except Exception as e:
            raise ValueError(
                f"Unable to extract pkg version from {str(self.pkg_root)}"
            ) from e

        self.dkr_repo = LatchConfig.dkr_repo
        self.remote = remote

        if remote is True:
            headers = {"Authorization": f"Bearer {self.token}"}

            try:
                user_agent = paramiko.Agent()
            except paramiko.SSHException as e:
                raise ValueError(
                    "An error occurred during SSH protocol negotiation. "
                    "This is due to a problem with your system. "
                    "Please use `latch register` without the `--remote` flag."
                ) from e
            keys = user_agent.get_keys()
            if len(keys) == 0:
                raise ValueError(
                    "It seems you don't have any (valid) SSH keys set up. "
                    "Check that any keys that you have are valid, or use "
                    "a utility like `ssh-keygen` to set one up and try again."
                )

            pub_key = keys[0]
            alg = pub_key.get_name()
            material = pub_key.get_base64()

            response = tinyrequests.post(
                self.latch_provision_url,
                headers=headers,
                json={
                    "public_key": f"{alg} {material}",
                },
            )

            resp = response.json()
            try:
                public_ip = resp["ip"]
                username = resp["username"]
            except KeyError as e:
                raise ValueError(
                    f"Malformed response from request for access token {resp}"
                ) from e

            self.dkr_client = self._construct_dkr_client(
                ssh_host=f"ssh://{username}@{public_ip}"
            )
            self.ssh_client = self._construct_ssh_client(
                host_ip=public_ip,
                username=username,
            )

        else:
            self.dkr_client = self._construct_dkr_client()

    @property
    def image(self):
        """The image to be registered."""
        if self.account_id is None:
            raise ValueError("You need to log in before you can register a workflow.")

        # CAUTION ~ this weird formatting is maintained indepedently in the
        # nucleus endpoint and here.
        # Name for federated token request has minimum of 2 characters.
        if int(self.account_id) < 10:
            account_id = f"x{self.account_id}"
        else:
            account_id = self.account_id

        return f"{account_id}_{self.pkg_root.name}"

    @property
    def image_tagged(self):
        """The tagged image to be registered.

        eg. dkr.ecr.us-west-2.amazonaws.com/pkg_name:version
        """

        # TODO (kenny): check version is valid for docker
        if self.version is None:
            raise ValueError(
                "Attempting to create a tagged image name without first"
                "extracting the package version."
            )
        if self.image is None or self.version is None:
            raise ValueError(
                "Attempting to create a tagged image name without first"
                " logging in or extracting the package version."
            )
        return f"{self.image}:{self.version}"

    @property
    def full_image(self):
        """The full image to be registered (without a tag).

            <repo/image>


        An example: ::

            dkr.ecr.us-west-2.amazonaws.com/pkg_name

        """
        return f"{self.dkr_repo}/{self.image}"

    @property
    def full_image_tagged(self):
        """The full image to be registered.

            - Registry name
            - Repository name
            - Version/tag name

        An example: ::

            dkr.ecr.us-west-2.amazonaws.com/pkg_name:version

        """
        return f"{self.dkr_repo}/{self.image_tagged}"

    @property
    def version_archive_path(self):
        version_archive_path = (
            Path.home() / ".latch" / self.image / "registered_versions"
        )
        version_archive_path.parent.mkdir(parents=True, exist_ok=True)
        version_archive_path.touch(exist_ok=True)
        return version_archive_path

    @staticmethod
    def _construct_dkr_client(ssh_host: Optional[str] = None):
        """Try many methods of establishing valid connection with client.

        This was helpful -
        https://github.com/docker/docker-py/blob/a48a5a9647761406d66e8271f19fab7fa0c5f582/docker/utils/utils.py#L321

        If `ssh_host` is passed, we attempt to make a connection with a remote
        machine.
        """

        def _from_env():

            host = environment.get("DOCKER_HOST")

            # empty string for cert path is the same as unset.
            cert_path = environment.get("DOCKER_CERT_PATH") or None

            # empty string for tls verify counts as "false".
            # Any value or 'unset' counts as true.
            tls_verify = environment.get("DOCKER_TLS_VERIFY")
            if tls_verify == "":
                tls_verify = False
            else:
                tls_verify = tls_verify is not None

            enable_tls = cert_path or tls_verify

            dkr_client = None
            try:
                if not enable_tls:
                    dkr_client = docker.APIClient(host)
                else:
                    if not cert_path:
                        cert_path = os.path.join(os.path.expanduser("~"), ".docker")

                    tls_config = docker.tls.TLSConfig(
                        client_cert=(
                            os.path.join(cert_path, "cert.pem"),
                            os.path.join(cert_path, "key.pem"),
                        ),
                        ca_cert=os.path.join(cert_path, "ca.pem"),
                        verify=tls_verify,
                    )
                    dkr_client = docker.APIClient(host, tls=tls_config)

            except docker.errors.DockerException as de:
                raise OSError(
                    "Unable to establish a connection to Docker. Make sure that"
                    " Docker is running and properly configured before attempting"
                    " to register a workflow."
                ) from de

            return dkr_client

        if ssh_host is not None:
            try:
                return docker.APIClient(ssh_host, use_ssh_client=True)
            except docker.errors.DockerException as de:
                raise OSError(
                    f"Unable to establish a connection to remote docker host {ssh_host}."
                ) from de

        environment = os.environ
        host = environment.get("DOCKER_HOST")
        if host is not None and host != "":
            return _from_env()
        else:
            try:
                # TODO: platform specific socket defaults
                return docker.APIClient(base_url="unix://var/run/docker.sock")
            except docker.errors.DockerException as de:
                raise OSError(
                    "Docker is not running. Make sure that"
                    " Docker is running before attempting to register a workflow."
                ) from de

    @staticmethod
    def _construct_ssh_client(host_ip: str, username: str):

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(host_ip, username=username)
        return ssh
