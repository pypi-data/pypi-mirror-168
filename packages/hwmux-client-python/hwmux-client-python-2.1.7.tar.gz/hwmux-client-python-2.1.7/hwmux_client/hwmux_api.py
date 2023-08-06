from . import Configuration, ApiClient
from .apis import (
    GroupsApi,
    DevicesApi,
    SitesApi,
    RoomsApi,
    PartsApi,
    PartFamiliesApi,
    LabelsApi,
    LogsApi,
    SchemaApi,
    ReservationsApi,
)

__all__ = ["HwMuxApi", "DevicesApiEx"]


class ListAllMixin:
    def list_all(self, method, *args, **kwargs):
        all_items = []
        page = 0
        while True:
            page += 1
            kwargs["page"] = page
            items = method(*args, **kwargs)
            all_items.extend(items.results)
            if items.next is None:
                break
        return all_items


class GroupsApiEx(GroupsApi, ListAllMixin):
    pass


class DevicesApiEx(DevicesApi, ListAllMixin):
    pass


class SitesApiEx(SitesApi, ListAllMixin):
    pass


class RoomsApiEx(RoomsApi, ListAllMixin):
    pass


class PartsApiEx(PartsApi, ListAllMixin):
    pass


class PartFamiliesApiEx(PartFamiliesApi, ListAllMixin):
    pass


class LabelsApiEx(LabelsApi, ListAllMixin):
    pass


class LogsApiEx(LogsApi, ListAllMixin):
    pass


class SchemaApiEx(SchemaApi, ListAllMixin):
    pass


class ReservationsApiEx(ReservationsApi, ListAllMixin):
    pass


class HwMuxApi:
    def __init__(self, user_token=None, server_url=None):
        config = Configuration(host=server_url, discard_unknown_keys=True)
        if user_token is not None:
            config = Configuration(
                host=server_url,
                api_key={"tokenAuth": user_token},
                api_key_prefix={"tokenAuth": "Token"},
                discard_unknown_keys=True
            )
        self.client = ApiClient(config)
        self._groups_api = GroupsApiEx(self.client)
        self._devices_api = DevicesApiEx(self.client)
        self._sites_api = SitesApiEx(self.client)
        self._rooms_api = RoomsApiEx(self.client)
        self._parts_api = PartsApiEx(self.client)
        self._part_families_api = PartFamiliesApiEx(self.client)
        self._labels_api = LabelsApiEx(self.client)
        self._logs_api = LogsApiEx(self.client)
        self._schema_api = SchemaApiEx(self.client)
        self._reservations_api = ReservationsApiEx(self.client)

    def get_location_url(self, site, room, location_id):
        url = f"{self.client.configuration.host}/api/sites/{site}/rooms/{room}/locations/{location_id}/".replace(
            "https", "http"
        )
        return url

    @property
    def groups_api(self) -> GroupsApiEx:
        return self._groups_api

    @property
    def devices_api(self) -> DevicesApiEx:
        return self._devices_api

    @property
    def sites_api(self) -> SitesApiEx:
        return self._sites_api

    @property
    def rooms_api(self) -> RoomsApiEx:
        return self._rooms_api

    @property
    def parts_api(self) -> PartsApiEx:
        return self._parts_api

    @property
    def part_families_api(self) -> PartFamiliesApiEx:
        return self._part_families_api

    @property
    def labels_api(self) -> LabelsApiEx:
        return self._labels_api

    @property
    def logs_api(self) -> LogsApiEx:
        return self._logs_api

    @property
    def schema_api(self) -> SchemaApiEx:
        return self._schema_api

    @property
    def reservations_api(self) -> ReservationsApiEx:
        return self._reservations_api
