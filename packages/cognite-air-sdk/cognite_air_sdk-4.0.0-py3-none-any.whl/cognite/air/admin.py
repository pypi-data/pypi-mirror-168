from cognite.air._spaces_api import SpacesAPI
from cognite.air._tasks_api import TasksAPI
from cognite.client import CogniteClient


class AIRAdmin:
    """AIRAdmin client to create, edit, and delete spaces and groups.

    Args:
        client (CogniteClient): Cognite client
        staging (bool): If operations should be made to staging or production (False is default)
    """

    def __init__(self, client: CogniteClient, staging: bool = False):
        self.spaces = SpacesAPI(client, staging)
        self.tasks = TasksAPI(client, staging)
