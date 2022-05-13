from data_lake.storage.base import Client


class MStorageClient(Client):

    def pipe_json_api(self, prepared_request, file_prefix, file_name=None):
        return True


def get_mock_storage_client():
    client = MStorageClient("test_bucket", "prefix", "temp_folder")
    try:
        yield client
    finally:
        pass
