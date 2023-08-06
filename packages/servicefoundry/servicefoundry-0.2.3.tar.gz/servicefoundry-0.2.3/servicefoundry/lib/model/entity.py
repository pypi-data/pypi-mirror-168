import datetime
from typing import Any, ClassVar, Dict, List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Extra, Field

from servicefoundry.lib import const

# TODO: switch to Enums for str literals
# TODO: Need a better approach to keep fields in sync with server
#       most fields should have a default in case server adds/removes a field
# TODO: Implement NotImplementedError sections


class Base(BaseModel):
    class Config:
        validate_assignment = True
        use_enum_values = True
        extra = Extra.allow

    def __repr_args__(self):
        return [
            (key, value)
            for key, value in self.__dict__.items()
            if self.__fields__[key].field_info.extra.get("repr", True)
        ]

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]):
        return cls.parse_obj(dct)

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()


class Entity(Base):
    createdAt: datetime.datetime = Field(repr=False)
    updatedAt: datetime.datetime = Field(repr=False)
    list_display_columns: ClassVar[List[str]] = []
    get_display_columns: ClassVar[List[str]] = []


class Cluster(Entity):
    id: str = Field(repr=False)
    name: str
    fqn: str
    region: str = Field(repr=False)
    isTenantDefault: bool = False
    list_display_columns: ClassVar[List[str]] = [
        "name",
        "fqn",
        "region",
        "createdAt",
    ]
    get_display_columns: ClassVar[List[str]] = [
        "name",
        "fqn",
        "region",
        "createdAt",
        "updatedAt",
    ]

    def to_dict_for_session(self) -> Dict[str, Any]:
        return self.dict()

    @property
    def workspaces(self) -> List["Workspace"]:
        raise NotImplementedError


class Workspace(Entity):
    id: str = Field(repr=False)
    fqn: str
    name: str
    clusterId: str = Field(repr=False)
    createdBy: str = Field(repr=False)
    grafanaEndpoint: Optional[str] = Field(default=None, repr=False)
    list_display_columns: ClassVar[List[str]] = [
        "name",
        "fqn",
        "createdAt",
    ]
    get_display_columns: ClassVar[List[str]] = [
        "name",
        "fqn",
        "createdBy",
        "grafanaEndpoint",
        "createdAt",
        "updatedAt",
    ]

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]):
        dct.setdefault(
            "grafanaEndpoint", dct.get("metadata", {}).get("grafanaEndpoint")
        )
        return super().from_dict(dct)

    def to_dict_for_session(self) -> Dict[str, Any]:
        return self.dict()

    @property
    def cluster(self) -> Cluster:
        raise NotImplementedError


class NewDeployment(Entity):
    def __init__(self, **data: Any):
        super().__init__(**data)
        self.workspaceName = self.workspace["name"]
        self.clusterName = self.workspace["cluster"]["name"]
        self.workspaceDetails = (
            f'{self.workspace["name"]} ({self.workspace["cluster"]["name"]})'
        )
        self.type = self.manifest["components"][0]["type"]

    id: str = Field(repr=False)
    version: str = Field(repr=False)
    fqn: str
    applicationId: str = Field(repr=False)
    workspaceId: str = Field(repr=False)

    metadata: Optional[Dict[str, Any]] = Field(repr=False)
    manifest: Dict[str, Any] = Field(repr=False)

    failureReason: Optional[str] = Field(repr=False)
    active: int = Field(repr=False)
    application: Optional[Dict[str, Any]] = Field(repr=False)
    workspace: Dict[str, Any] = Field(repr=False)
    baseDomainURL: str = Field(repr=False)
    createdBy: str = Field(repr=False)
    workspaceName: Optional[str] = Field(repr=False)
    clusterName: Optional[str] = Field(repr=False)
    workspaceDetails: Optional[str] = Field(repr=False)
    type: Optional[str] = Field(repr=False)

    list_display_columns: ClassVar[List[str]] = [
        "fqn",
        "workspaceDetails",
        "type",
        "createdAt",
    ]


# TODO: Should treat displaying and handling these with more respect as it is sensitive data


class Secret(Entity):
    id: str = Field(repr=False)
    name: str
    fqn: str
    value: str = Field(repr=False)
    secretGroupId: str = Field(repr=False)
    createdBy: str = Field(repr=False)
    list_display_columns: ClassVar[List[str]] = [
        "name",
        "fqn",
        "createdAt",
    ]
    get_display_columns: ClassVar[List[str]] = [
        "name",
        "value",
        "createdAt",
        "updatedAt",
    ]

    @property
    def secret_group(self) -> "SecretGroup":
        raise NotImplementedError


class SecretGroup(Entity):
    id: str = Field(repr=False)
    name: str
    fqn: str
    createdBy: str = Field(repr=False)
    associatedSecrets: List[Secret] = Field(repr=False)
    list_display_columns: ClassVar[List[str]] = [
        "name",
        "fqn",
        "createdAt",
    ]
    get_display_columns: ClassVar[List[str]] = [
        "name",
        "fqn",
        "associatedSecrets",
        "createdAt",
        "updatedAt",
    ]

    @classmethod
    def from_dict(cls, dct):
        dct.setdefault(
            "associatedSecrets",
            [Secret.from_dict(s) for s in dct.get("associatedSecrets", [])],
        )
        return super().from_dict(dct)


class ServerConfig(Base):
    api_server: str = const.DEFAULT_API_SERVER
    auth_server: str = const.DEFAULT_AUTH_SERVER
    auth_ui: str = const.DEFAULT_AUTH_UI
    tenant_name: str = const.DEFAULT_TENANT_NAME

    @property
    def base_url(self):
        parsed_url = urlparse(self.api_server)

        return f"{parsed_url.scheme}://{parsed_url.netloc}".rstrip("/")

    @classmethod
    def from_base_url(cls, base_url: str):
        from servicefoundry.lib.clients.service_foundry_client import (
            ServiceFoundryServiceClient,
        )

        base_url = base_url.rstrip("/")
        api_server = f"{base_url}/{const.API_SERVER_RELATIVE_PATH}"
        auth_ui = base_url
        tenant_info = ServiceFoundryServiceClient.get_tenant_info(
            api_server_host=api_server, tenant_hostname=urlparse(base_url).netloc
        )
        return cls(
            api_server=api_server,
            auth_server=tenant_info["auth_server_url"],
            auth_ui=auth_ui,
            tenant_name=tenant_info["tenant_name"],
        )


class Profile(Base):
    name: str = const.DEFAULT_PROFILE_NAME
    server_config: ServerConfig = Field(default_factory=ServerConfig)
