import copy

from cognite.air._air_api_url import retrieve_air_api_url
from cognite.client import CogniteClient


class AdminAPI:
    def __init__(self, client: CogniteClient, staging: bool = False):
        self.client = client
        self.air_client = copy.deepcopy(client)
        self.air_client.config.base_url = retrieve_air_api_url(client, staging, add_project=False)
