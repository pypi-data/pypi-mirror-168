import logging


def get_logger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False
    return logger


class Connector:

    def __init__(self, config_from_local, mount_path, secret_file):
        """
        :param config_from_local: True if read secrets from local files, False if from OC mounted secrets.
        """
        self.logger = get_logger('connectors')
        try:
            if config_from_local:
                self.client = self._get_client_from_local(secret_file)
            else:
                self.client = self._get_client_from_oc(mount_path)
        except Exception as e:
            self.logger.error(f"Failed to initialize client, {e}")
            self.client = None

    def _get_client_from_oc(self, mount_path):
        pass

    def _get_client_from_local(self, secret_file):
        pass
