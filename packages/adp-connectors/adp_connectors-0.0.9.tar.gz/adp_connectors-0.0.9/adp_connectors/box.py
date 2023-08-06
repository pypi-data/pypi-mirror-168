from boxsdk import JWTAuth, Client
from .base import Connector


class BoxConnector(Connector):

    def __init__(self, config_from_local=False, mount_path='/box-credentials', secret_file='box.secrets'):
        super().__init__(config_from_local, mount_path, secret_file)

    def _get_client_from_oc(self, mount_path):
        config_file = {
            "boxAppSettings": {
                "clientID": "",
                "clientSecret": "",
                "appAuth": {
                    "publicKeyID": "",
                    "privateKey": "",
                    "passphrase": ""
                }
            },
            "enterpriseID": ""
        }
        with open(f'{mount_path}/clientID', 'r') as secret_file:
            config_file['boxAppSettings']['clientID'] = secret_file.read()
        with open(f'{mount_path}/clientSecret', 'r') as secret_file:
            config_file['boxAppSettings']['clientSecret'] = secret_file.read()
        with open(f'{mount_path}/publicKeyID', 'r') as secret_file:
            config_file['boxAppSettings']['appAuth']['publicKeyID'] = secret_file.read()
        with open(f'{mount_path}/privateKey', 'r') as secret_file:
            config_file['boxAppSettings']['appAuth']['privateKey'] = secret_file.read()
        with open(f'{mount_path}/passphrase', 'r') as secret_file:
            config_file['boxAppSettings']['appAuth']['passphrase'] = secret_file.read()
        with open(f'{mount_path}/enterpriseID', 'r') as secret_file:
            config_file['enterpriseID'] = secret_file.read()
        sdk = JWTAuth.from_settings_dictionary(config_file)
        return Client(sdk)

    def _get_client_from_local(self, secret_file):
        sdk = JWTAuth.from_settings_file(secret_file)
        return Client(sdk)

    def get_object(self, obj):
        """
        Get a file object by its ID
        :param obj: object ID
        :return: Box File object
        """
        return self.client.file(obj)

    def list_objects(self, target):
        # target: folder id
        items = self.client.folder(folder_id=target).get_items()
        return [(f.id, f.name) for f in items]

    def rename_object(self, obj, name):
        # obj: file id
        _ = self.client.file(obj).update_info(data={'name': name})
        return

    def save_object(self, data, file_name, suffix, target):
        # data: pandas DataFrame
        # target: folder id
        data.to_csv(f'{suffix}_temp.csv', index=False)
        remote_folder = self.client.folder(target)
        try:
            _ = remote_folder.upload(
                f'{suffix}_temp.csv',
                f"{file_name}_{suffix}.csv")
        except Exception as e:
            conflict_id = self.handle_file_conflict_error(e)
            if conflict_id:
                _ = self.client.file(conflict_id).update_contents(f'{suffix}_temp.csv')
            else:
                self.logger.error("Other errors")
                raise e

    @staticmethod
    def handle_file_conflict_error(e):
        if e.status == 409 and e.context_info['conflicts']:
            return e.context_info['conflicts']['id']
