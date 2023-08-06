import json
import logging

from botocore.exceptions import NoCredentialsError
from time import time
from typing import Dict, Optional

from cache import Cache
from no_secrets_found_error import NoSecretsFoundError
from secrets_manager import SecretsManager


class CachedSecretsManager:
    """
    This class is used for creating a json cache file for secrets so that they do not need to be invoked from AWS
    each time. Cache modification and insertion is done using the Cache class.
    """

    _VALID_UNTIL_KEY = "valid_until"

    _LOGGER = logging.getLogger()
    _LOGGER.setLevel(logging.INFO)

    def __init__(self, cache_name: str, secret_name: str, region_name: str, cache_base_path: Optional[str] = None):
        self._secrets_cache: Cache = Cache(cache_name, cache_base_path)
        self._secrets_manager: SecretsManager = SecretsManager(secret_name, region_name)

    def get(self, minutes_to_live: int = 60) -> Dict:
        """
        This method tries to retrieve a secret from cache first and falls back to secret manager otherwise.
        :return: secret of throws exception
        """
        try:
            self._LOGGER.info("Trying to get cache")
            secrets: Dict = self._get_secrets_from_cache()
            current_time = int(round(time()))
            valid_until = int(secrets.get(self._VALID_UNTIL_KEY, 0))
            self._LOGGER.info(f"Extracted validity timestamp: {valid_until}")
            if current_time > valid_until:
                self._LOGGER.info(
                    f"Cache needs to be invalidated (Current time: {current_time}, valid until: {valid_until})."
                )
                self.reset_cache()
                raise NoSecretsFoundError
            self._LOGGER.info(
                f"Collected secrets from cache (Current time: {current_time}, valid until: {valid_until})."
            )
        except NoSecretsFoundError:
            self._LOGGER.info(
                f"No secrets found in cache {self._secrets_cache.cache_path}. Trying through secrets manager."
            )
            secrets = self._get_secrets_from_secrets_manager()
            valid_until = int(round(time())) + minutes_to_live * 60
            secrets[self._VALID_UNTIL_KEY] = valid_until
            self._set_secrets_in_cache(secrets)
        secrets.pop(self._VALID_UNTIL_KEY, None)
        return secrets

    def set(self, secrets: Dict):
        self._secrets_manager.update(json.dumps(secrets))
        self.reset_cache()

    def reset_cache(self):
        self._secrets_cache.delete_all()

    def _get_secrets_from_cache(self):
        secrets = self._secrets_cache.get_all()
        if not secrets:
            raise NoSecretsFoundError("No secrets found in cache.")
        for secret_value in secrets.values():
            if not secret_value:
                raise NoSecretsFoundError("No secrets found in cache.")
        self._LOGGER.info("Found secrets in cache.")
        return secrets

    def _set_secrets_in_cache(self, secrets):
        self._secrets_cache.set_all(secrets)
        self._LOGGER.info("Set secrets in cache.")

    def _get_secrets_from_secrets_manager(self):
        self._LOGGER.info("Retrieving secrets from secrets manager.")
        try:
            secrets = json.loads(self._secrets_manager.get())
        except NoCredentialsError as error:
            raise NoSecretsFoundError("Secret missing in secrets manager.") from error
        if not secrets:
            raise NoSecretsFoundError("No secrets found in secret.")
        for secret_value in secrets.values():
            if not secret_value:
                raise NoSecretsFoundError("Incomplete secrets found through secrets manager.")
        return secrets
