import json
import pprint
from typing import Any, Dict, Optional, Union

from cognite.air._admin_config import AdminAPI
from cognite.client.exceptions import CogniteAPIError


class TasksAPI(AdminAPI):
    def _retrieve_models(self):
        r = self.air_client.get("/models")
        return json.loads(r.content.decode("utf-8"))["models"]

    def _retrieve_model(self, model_name: str):
        models = self._retrieve_models()
        model = [i for i in models if i["externalId"] == model_name]
        if len(model) == 0:
            raise ValueError(f"Model with external id {model_name} does not exist")
        return model[0]

    def _validate_creation_args(self, model_fields, arguments):
        field_ids = [i["id"] for i in model_fields]
        for i in field_ids:
            if i not in arguments.keys():
                raise ValueError(f"Field {i} needs to be defined.")
        for field in model_fields:
            argument = arguments[field["id"]]
            error = False
            if field["type"] == "TimeSeries":
                error = self._validate_time_series(argument)
            elif field["type"] == "Asset":
                error = self._validate_asset(argument)
            elif field["type"] == "bool":
                error = self._validate_bool(argument)
            elif field["type"] == "float":
                error = self._validate_float(argument)
            elif field["type"] == "str":
                error = self._validate_str(argument)

            if error:
                raise ValueError(f"{field['id']} is not of type {field['type']} or is empty.")

    def _validate_time_series(self, time_series):
        return self.client.time_series.retrieve(external_id=time_series) is None

    def _validate_asset(self, asset):
        return self.client.assets.retrieve(external_id=asset) is None

    def _validate_bool(self, boolean):
        return not isinstance(boolean, bool)

    def _validate_float(self, number):
        return not (isinstance(number, float) or isinstance(number, int))

    def _validate_str(self, string):
        return string == ""

    def _create_payload(
        self,
        data: Dict[str, Any],
        space_id: str,
        group_id: str,
        model_name: str,
        model_id: str,
        model_ext_id: str,
        name_of_monitoring_task: Optional[str] = None,
    ) -> Dict:
        schedule: Dict[str, Union[str, Dict]] = {
            "name": name_of_monitoring_task if name_of_monitoring_task else f"{model_name} schedule",
            "modelId": model_id,
            "modelExternalId": model_ext_id,
            "dashboardId": space_id,
            "systemId": group_id,
            "data": data,
        }
        payload = {"project": self.client.config.project, "schedule": schedule}
        return payload

    def create(
        self,
        space_id: str,
        group_id: str,
        model_name: str,
        name_of_monitoring_task: Optional[str] = None,
        show_fields: bool = True,
        **kwargs,
    ):
        """Create Monitoring Task in a specific Space and Group.

        The `space_id` and `group_id` can be extracted from the url:
        `https://air.cogniteapp.com/my_project/space/123/group/567`

        123 would be the `space_id` and 567 would be the `group_id`.

        Args:
            space_id (str): The id for the Space where the Monitoring Task is created in.
            group_id (str): The id for the Group where the Monitoring Task is created in.
            model_name (str): Name of the model the monitoring task should be created for.
            name_of_monitoring_task (str): Optional name for the Monitoring Task.
            show_fields (bool): Print out the fields for the model in question. Defaults to True.
            kwargs: Keyword arguments that specify the fields for the specific model.

        Examples:
            >>> from cognite.client import CogniteClient
            >>> from cognite.air.admin import AIRAdmin
            >>> c = CogniteClient()
            >>> air_admin = AIRAdmin(c)
            >>> air_admin.tasks.create(space_id="123",
            ...         group_id="567",
            ...         model_name="upperthreshold",
            ...         ts_ext_id="external_id_of_ts",
            ...         threshold=50)
        """
        model = self._retrieve_model(model_name)
        model_fields = json.loads(model["metadata"]["fields"])
        if show_fields:
            pprint.pprint(model_fields)

        self._validate_creation_args(model_fields, kwargs)
        data = {k: str(v) for k, v in kwargs.items()}
        payload = self._create_payload(
            data, space_id, group_id, model_name, str(model["id"]), str(model["externalId"]), name_of_monitoring_task
        )
        self._create_schedule_asset(payload)

    def _create_schedule_asset(self, payload: Dict):
        r = self.air_client.post("/schedule", json=payload)
        if r.status_code != 200:
            raise CogniteAPIError(r.reason)
