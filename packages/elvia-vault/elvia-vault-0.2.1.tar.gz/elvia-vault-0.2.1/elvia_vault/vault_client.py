"""
Vault Client class.
"""

import hvac
import kubernetes
import jwt
import os
from typing import Callable, Tuple


class EnvVarNames:
    """Reduce hardcoding by collecting env var names in this class."""

    VAULT_ADDR = 'VAULT_ADDR'
    GITHUB_TOKEN = 'GITHUB_TOKEN'
    ROLE_ID = 'ROLE_ID'
    KUBERNETES_SERVICE_HOST = 'KUBERNETES_SERVICE_HOST'


class VaultClient():
    """Connect to the vault and get secrets using different authentication methods."""
    def __init__(self,
                 vault_addr: str = None,
                 github_token: str = None) -> None:
        if self.is_in_cluster():
            self._client, self._authenticate_func = self._use_kubernetes_auth()
        elif EnvVarNames.ROLE_ID in os.environ:
            self._client, self._authenticate_func = self._use_approle_auth()
        else:
            self._client, self._authenticate_func = self._use_github_auth(
                vault_addr, github_token)

        self._authenticate_func(self._client)

    def get_value(self, secret_path: str) -> str:
        """Retrieve a secret value for a given secret path.        
        
        Parameters
        ----------        
        secret_path : str
        
        Returns
        -------
        str
        """
        if not self._client.is_authenticated():
            self._authenticate_func(self._client)

        secret = secret_path.split("/")[-1]
        mount_point = "/".join(secret_path.split("/")[:2])

        secret_path_array_length = len(secret_path.split("/"))
        path = "/".join(secret_path.split("/")[2:secret_path_array_length - 1])

        return self._client.secrets.kv.v2.read_secret_version(
            mount_point=mount_point, path=path)['data']['data'][secret]
    
    def encrypt_secret(self, transit_path: str, key_name: str,  plaintext: str) -> str:
        """Encrypts a secret and returns the ciphertext
        
        Parameters
        ----------        
        transit_path: str, {system}/transit (usually)
        key_name: str, name of the backend key
        plaintext: str, base64
        
        Returns
        -------
        str, format: vault:v1:{ciphertext}, where the entire string should be sent to vault for decryption
        """
        if not self._client.is_authenticated():
            self._authenticate_func(self._client)
        
        response = self._client.secrets.transit.encrypt_data(key_name, plaintext, mount_point=transit_path)
        return response['data']['ciphertext']

    def decrypt_secret(self, transit_path: str, key_name: str, ciphertext: str) -> str:
        """Encrypts a secret and returns the ciphertext
        
        Parameters
        ----------        
        transit_path: str, {system}/transit (usually)
        key_name: str, name of the backend key
        ciphertext: str, format: vault:v1:{ciphertext}
        
        Returns
        -------
        str, base64
        """
        if not self._client.is_authenticated():
            self._authenticate_func(self._client)
            
        response = self._client.secrets.transit.decrypt_data(key_name, ciphertext, mount_point=transit_path)
        return response['data']['plaintext']

    @staticmethod
    def is_in_cluster() -> bool:
        """Tell whether the code is running in the cluster or not."""
        if EnvVarNames.KUBERNETES_SERVICE_HOST in os.environ:
            return True
        return False

    def _use_kubernetes_auth(
            self) -> Tuple[hvac.Client, Callable[[hvac.Client], None]]:
        vault_addr, vault_base_mount_point = self._read_vault_addr()
        jwt_token = self._read_serviceaccount_token()

        decoded_token = jwt.decode(jwt_token,
                                   options={"verify_signature": False})

        if "kubernetes.io/serviceaccount/namespace" in decoded_token:
            namespace = decoded_token["kubernetes.io/serviceaccount/namespace"]
            serviceaccount_name = decoded_token[
                "kubernetes.io/serviceaccount/service-account.name"]
        else:
            namespace = decoded_token['kubernetes.io']['namespace']
            serviceaccount_name = decoded_token["kubernetes.io"]["serviceaccount"]["name"]

        vault_client = hvac.Client(url=vault_addr)
        mount_point = f"{vault_base_mount_point}{namespace}/{serviceaccount_name}"

        authenticate_func = lambda client, serviceaccount_name=serviceaccount_name, \
            jwt_token=jwt_token, mount_point=mount_point: client.auth_kubernetes(
            serviceaccount_name, jwt_token, mount_point=mount_point)

        return vault_client, authenticate_func

    @staticmethod
    def _use_approle_auth(
    ) -> Tuple[hvac.Client, Callable[[hvac.Client], None]]:
        role_id = os.environ[EnvVarNames.ROLE_ID]
        vault_addr = os.environ[EnvVarNames.VAULT_ADDR]

        vault_client = hvac.Client(url=vault_addr)

        authenticate_func = lambda client, role_id=role_id: client.auth_approle(
            role_id)

        return vault_client, authenticate_func

    @staticmethod
    def _read_vault_addr() -> Tuple[str, str]:
        kubernetes.config.load_incluster_config()
        api_instance = kubernetes.client.CoreV1Api()

        response = api_instance.read_namespaced_config_map("vault", "vault")

        return response.data["vault_hostname"], response.data[
            "vault_base_mountpoint"]

    @staticmethod
    def _read_k8s_secret(path: str, err_msg: str) -> str:
        if os.path.exists(path):
            with open(path) as file_open:
                secret = file_open.read()
            if len(secret) > 0:
                return secret

        raise OSError(
            err_msg)  #OSError because involves I/O failure when reading a file

    def _read_serviceaccount_token(self):
        return self._read_k8s_secret(
            "/var/run/secrets/kubernetes.io/serviceaccount/token",
            "If running on kubernetes, the pod must be running as a separate service account with its token loaded at /var/run/secrets/kubernetes.io/serviceaccount/token"
        )

    @staticmethod
    def _use_github_auth(
        vault_addr: str = None,
        github_token: str = None
    ) -> Tuple[hvac.Client, Callable[[hvac.Client], None]]:
        if vault_addr is None:
            if EnvVarNames.VAULT_ADDR not in os.environ:
                raise AttributeError("The environment variable " +
                                     EnvVarNames.VAULT_ADDR +
                                     " must be set or vault_addr given")
            vault_addr = os.environ[EnvVarNames.VAULT_ADDR]
        if github_token is None:
            if EnvVarNames.GITHUB_TOKEN not in os.environ:
                raise AttributeError("The environment variable " +
                                     EnvVarNames.GITHUB_TOKEN +
                                     " must be set or github_token given")
            github_token = os.environ[EnvVarNames.GITHUB_TOKEN]

        vault_client = hvac.Client(vault_addr)

        authenticate_func = lambda client, github_token=github_token: client.auth.github.login(
            github_token)

        return vault_client, authenticate_func
