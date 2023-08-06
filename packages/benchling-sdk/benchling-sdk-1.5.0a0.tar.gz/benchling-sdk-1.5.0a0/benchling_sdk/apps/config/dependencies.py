from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generic, List, Optional, Type, TypeVar, Union

from benchling_api_client.v2.alpha.types import UNSET
from benchling_api_client.v2.beta.models.benchling_app_configuration import BenchlingAppConfiguration
from benchling_api_client.v2.beta.models.dropdown_dependency_link import DropdownDependencyLink
from benchling_api_client.v2.beta.models.entity_schema_dependency_link import EntitySchemaDependencyLink
from benchling_api_client.v2.beta.models.resource_dependency_link import ResourceDependencyLink
from benchling_api_client.v2.beta.models.scalar_config import ScalarConfig
from benchling_api_client.v2.beta.models.scalar_config_types import ScalarConfigTypes
from benchling_api_client.v2.beta.models.schema_base_dependency_link_field_definitions_item import (
    SchemaBaseDependencyLinkFieldDefinitionsItem,
)
from benchling_api_client.v2.beta.models.schema_dependency_link import SchemaDependencyLink
from benchling_api_client.v2.beta.models.secure_text_config import SecureTextConfig
from benchling_api_client.v2.beta.models.subdependency_link import SubdependencyLink
from benchling_api_client.v2.beta.models.workflow_task_schema_dependency_link import (
    WorkflowTaskSchemaDependencyLink,
)
from benchling_api_client.v2.extensions import UnknownType
from typing_extensions import Protocol

from benchling_sdk.apps.config.decryption_provider import BaseDecryptionProvider
from benchling_sdk.apps.config.scalars import DEFAULT_SCALAR_DEFINITIONS, ScalarDefinition, ScalarType
from benchling_sdk.benchling import Benchling


class MissingDependencyError(Exception):
    """
    Missing dependency error.

    Indicates a dependency was missing from app config.
    For instance, no dependency with that name was in the list.
    """

    pass


class MissingAppConfigError(Exception):
    """
    Missing app config error.

    The app did not return any configuration.
    It may not have a manifest installed, or may not have been configured.
    """

    pass


class UnsupportedDependencyError(Exception):
    """
    Unsupported dependency error.

    The manifest and configuration specified a dependency which the SDK is incapable of handling yet.
    """

    pass


class MissingScalarDefinitionError(Exception):
    """
    Missing scalar definition error.

    The manifest and configuration specified a scalar type which the SDK does not know how to translate
    to Python values yet.
    """

    pass


ApiConfigurationReference = Union[
    DropdownDependencyLink,
    EntitySchemaDependencyLink,
    ResourceDependencyLink,
    SchemaDependencyLink,
    SubdependencyLink,
    WorkflowTaskSchemaDependencyLink,
]
ConfigurationReference = Union[ApiConfigurationReference, ScalarConfig, SecureTextConfig]

AnyConfigType = TypeVar(
    "AnyConfigType",
    DropdownDependencyLink,
    EntitySchemaDependencyLink,
    ResourceDependencyLink,
    ScalarConfig,
    SecureTextConfig,
    SchemaDependencyLink,
    SubdependencyLink,
    WorkflowTaskSchemaDependencyLink,
)
ApiConfigType = TypeVar(
    "ApiConfigType",
    DropdownDependencyLink,
    EntitySchemaDependencyLink,
    ResourceDependencyLink,
    SchemaDependencyLink,
    SubdependencyLink,
    WorkflowTaskSchemaDependencyLink,
)

D = TypeVar("D", bound="BaseDependencies")


class ConfigProvider(Protocol):
    """
    Config provider.

    Provides a BenchlingAppConfiguration.
    """

    def config(self) -> BenchlingAppConfiguration:
        """Implement to provide a Benchling app configuration."""
        ...


class BenchlingConfigProvider(ConfigProvider):
    """
    Benchling Config provider.

    Provides a BenchlingAppConfiguration retrieved from Benchling's API.
    """

    _client: Benchling
    _app_id: str

    def __init__(self, client: Benchling, app_id: str):
        """
        Initialize Benchling Config Provider.

        :param client: A configured Benchling instance for making API calls.
        :param app_id: The app_id from which to retrieve configuration.
        """
        self._client = client
        self._app_id = app_id

    def config(self) -> BenchlingAppConfiguration:
        """Provide a Benchling app configuration from Benchling's APIs."""
        app_config = self._client.v2.beta.apps.get_configuration_by_app_id(app_id=self._app_id)
        if not (app_config and app_config.configuration):
            raise MissingAppConfigError(
                f"The configuration for app {self._app_id} was empty or "
                f"the app may not have the necessary permissions."
            )
        return app_config


class StaticConfigProvider(ConfigProvider):
    """
    Static Config provider.

    Provides a BenchlingAppConfiguration from a static declaration. Useful for mocking or testing.
    """

    _configuration: BenchlingAppConfiguration

    def __init__(self, configuration: BenchlingAppConfiguration):
        """
        Initialize Static Config Provider.

        :param configuration: The configuration object to return.
        """
        self._configuration = configuration

    def config(self) -> BenchlingAppConfiguration:
        """Provide a Benchling app configuration from a static object."""
        return self._configuration


class DependencyLinkStore(object):
    """
    Dependency Link Store.

    Marshalls an app configuration from the configuration provider into an indexable structure.
    Only retrieves app configuration once unless its cache is invalidated.
    """

    _configuration_provider: ConfigProvider
    _configuration: Optional[BenchlingAppConfiguration] = None
    _configuration_map: Optional[Dict[str, ConfigurationReference]] = None

    def __init__(self, configuration_provider: ConfigProvider):
        """
        Initialize Dependency Link Store.

        :param configuration_provider: A ConfigProvider that will be invoked to provide the
        underlying config from which to organize dependency links.
        """
        self._configuration_provider = configuration_provider

    @classmethod
    def from_app(cls, client: Benchling, app_id: str) -> DependencyLinkStore:
        """
        From App.

        Instantiate a DependencyLinkStore from an app_id and a configured Benchling instance. Preferred to
        using the class's constructor.
        """
        config_provider = BenchlingConfigProvider(client, app_id)
        return DependencyLinkStore(config_provider)

    @property
    def configuration(self) -> BenchlingAppConfiguration:
        """
        Get the underlying configuration.

        Return the raw, stored configuration. Can be used if the provided accessors are inadequate
        to find particular configuration items.
        """
        if not self._configuration:
            self._configuration = self._configuration_provider.config()
        return self._configuration

    @property
    def config_links(self) -> Dict[str, ConfigurationReference]:
        """
        Config links.

        Return a map of configuration item names to their corresponding API link or dependency value.
        """
        if not self._configuration_map:
            self._configuration_map = self.map_from_configuration(self.configuration)
        return self._configuration_map

    def config_by_name(self, name: str, config_type: Type[AnyConfigType]) -> AnyConfigType:
        """
        Config by name.

        Look up a configuration reference by its name. Only applies to named configuration at the top level,
        not subdependencies.
        """
        if name not in self.config_links:
            raise MissingDependencyError(
                f"The configuration did not have an option named '{name}'. "
                f"Valid configuration names are: {sorted(self.config_links.keys())}"
            )
        config = self.config_links[name]
        assert isinstance(config, config_type), (
            f"Expected configuration for `{name}` to be of type " f"{config_type} but found {type(config)}"
        )
        return config

    def map_from_configuration(self, config: BenchlingAppConfiguration) -> Dict[str, ConfigurationReference]:
        """
        Map from configuration.

        Produce a map of Benchling configuration references where the `name` is the key for easy lookup.
        """
        return {
            item.name: item
            # Use map to avoid MyPy thinking item can be UnknownType
            for item in map(self.to_map_value, config.configuration)
        }

    # noinspection PyMethodMayBeStatic
    def to_map_value(
        self,
        configuration_item: Union[ConfigurationReference, UnknownType],
    ) -> ConfigurationReference:
        """
        Transform configuration item to a map.

        This method can be overridden to change handling of UnknownType and type safety for ConfigurationReference.
        """
        # We don't have a productive way of handling UnknownType
        if type(configuration_item) == UnknownType:
            raise UnsupportedDependencyError(
                f"Unable to read configuration with unsupported dependency {configuration_item}"
            )
        assert isinstance(
            configuration_item,
            (
                DropdownDependencyLink,
                EntitySchemaDependencyLink,
                ResourceDependencyLink,
                SchemaDependencyLink,
                ScalarConfig,
                SecureTextConfig,
                SubdependencyLink,
                WorkflowTaskSchemaDependencyLink,
            ),
        ), f"Type of configuration was invalid {type(configuration_item)}"
        return configuration_item

    def invalidate_cache(self) -> None:
        """
        Invalidate Cache.

        Will force retrieval of configuration from the ConfigProvider the next time the link store is accessed.
        """
        self._configuration = None
        self._configuration_map = None


@dataclass
class ApiDependency(ABC, Generic[ApiConfigType]):
    """
    Api Dependency.

    A dependency that is API identifiable in Benchling, such as a schema.
    """

    link: ApiConfigType


class HasLink(Protocol):
    """
    Has Link.

    A mixin for typing to assert that a particular class has any link.
    """

    @property
    def link(self) -> ApiConfigurationReference:
        """Return the underlying dependency link."""
        ...


class HasEntityLink(Protocol):
    """
    Has Entity Link.

    A mixin for typing to assert that a particular class has a link to an entity schema.
    """

    @property
    def link(self) -> Union[EntitySchemaDependencyLink, SchemaDependencyLink]:
        """Return the underlying schema dependency link."""
        ...


class HasWorkflowTaskSchemaParentLink(Protocol):
    """
    Has Workflow Task Schema Parent Link.

    A mixin for typing to assert that a particular class has a link to a parent workflow task schema.
    """

    @property
    def parent(self) -> HasWorkflowTaskSchemaLink:
        """Return the parent workflow task schema dependency link."""
        ...


class HasWorkflowTaskSchemaLink(Protocol):
    """
    Has Workflow Task Schema Link.

    A mixin for typing to assert that a particular class has a link to a workflow task schema.
    """

    @property
    def link(self) -> WorkflowTaskSchemaDependencyLink:
        """Return the underlying workflow task schema dependency link."""
        ...


class HasScalarDefinition(Protocol):
    """
    Has Scalar Definition.

    A mixin for typing to assert that a particular class has scalar attributes.
    """

    @property
    def config(self) -> ScalarConfig:
        """Return the underlying scalar config."""
        ...

    @property
    def definition(self) -> Optional[ScalarDefinition]:
        """Return the scalar definition, allowing for conversion to Python types."""
        ...


class HasConfigWithDecryptionProvider(Protocol):
    """
    Has Config With Decryption Provider.

    A mixin for typing to assert that a particular class has a decryption provider and config.
    """

    # We can't extend HasScalarDefinition for type erasure, or mix these in so duplicate for typing
    @property
    def config(self) -> ScalarConfig:
        """Return the underlying scalar config."""
        ...

    @property
    def decryption_provider(self) -> Optional[BaseDecryptionProvider]:
        """Return the decryption provider."""
        ...


class RequiredApiDependencyMixin:
    """
    Require Api Link.

    A mixin for accessing an API link which is required and should always be present. Should
    only be mixed in with ApiDependency or another class that provides the `self.link` attribute.
    """

    @property
    def id(self: HasLink) -> str:
        """Return the API ID of the linked configuration."""
        # Currently, the API does not have a concept of required dependencies
        # Treat all dependencies as required for now so we don't have to null check in code
        assert self.link.resource_id is not None, f"The dependency {self.link} is not linked in Benchling"
        return self.link.resource_id

    @property
    def name(self: HasLink) -> str:
        """Return the name of the linked configuration."""
        # Currently, the API does not have a concept of required dependencies
        # Treat all dependencies as required for now so we don't have to null check in code
        assert self.link.resource_name is not None, f"The dependency {self.link} is not linked in Benchling"
        return self.link.resource_name


class RequiredScalarDependencyMixin(Generic[ScalarType]):
    """
    Require Scalar Config.

    A mixin for accessing a scalar config which is required and should always be present.
    Should only be mixed in with ScalarConfig.
    """

    @property
    def value(self: HasScalarDefinition) -> ScalarType:
        """Return the value of the scalar."""
        if self.definition:
            assert self.config.value is not None, f"The dependency {self.config} is not set in Benchling"
            optional_typed_value = self.definition.from_str(value=self.config.value)
            assert optional_typed_value is not None
            return optional_typed_value
        raise MissingScalarDefinitionError(f"No definition registered for scalar config {self.config}")

    @property
    def value_str(self: HasScalarDefinition) -> str:
        """Return the value of the scalar as a string."""
        assert self.config.value is not None, f"The dependency {self.config} is not set in Benchling"
        # Booleans are currently specified as str in the spec but are bool at runtime in JSON
        return str(self.config.value)


class RequiredSecureTextDependencyMixin(RequiredScalarDependencyMixin[str]):
    """
    Require Secure Text.

    A mixin for accessing a secure text config which is required and should always be present.
    Should only be mixed in with SecureTextConfig.
    """

    def decrypted_value(self: HasConfigWithDecryptionProvider) -> str:
        """
        Decrypted value.

        Decrypts a secure_text dependency's encrypted value into plain text.
        """
        # Currently, the API does not have a concept of required dependencies
        # Treat all dependencies as required for now so we don't have to null check in code
        assert (
            self.decryption_provider is not None
        ), f"The dependency {self.config} cannot be decrypted because no DecryptionProvider was set"
        assert self.config.value is not None, f"The dependency {self.config} is not set in Benchling"
        return self.decryption_provider.decrypt(self.config.value)


class Subdependencies(ABC):
    """
    Subdependencies.

    Assigns behavior to a class that can have a list of dependencies, such as schema fields
    or dropdown options.
    """

    _subdependency_map: Optional[Dict[str, SubdependencyLink]] = None

    @abstractmethod
    def subdependency_links(self) -> List[SubdependencyLink]:
        """Implement to fetch the list of subdependency links."""
        pass

    @abstractmethod
    def subdependency_type_display_name(self) -> str:
        """Implement for user messaging, for example when surfacing errors."""
        pass

    @property
    def subdependency_mapping(self) -> Dict[str, SubdependencyLink]:
        """Access subdependencies as a map with names as the key and subdependency links as the values."""
        if not self._subdependency_map:
            # TODO BNCH-50127 Stop compensating for bad spec models once new app config lands
            links = [_fix_subdependency(item) for item in self.subdependency_links()]
            self._subdependency_map = {item.name: item for item in links}
        return self._subdependency_map

    def subdependency_by_name(self, name: str) -> SubdependencyLink:
        """Get a subdependency link by its name."""
        if name not in self.subdependency_mapping:
            raise MissingDependencyError(
                f"The configuration did not have a "
                f"{self.subdependency_type_display_name()} named '{name}'. "
                f"Valid {self.subdependency_type_display_name()} names are: "
                f"{sorted(self.subdependency_mapping.keys())}"
            )
        return self.subdependency_mapping[name]


# TODO BNCH-50127 - Remove this once the new app config APIs and models land. For now this fixes tests
# and unblocks code generation
def _fix_subdependency(link):
    # The SchemaBaseDependencyLinkFieldDefinitionsItem model has no properties,
    # so pull them out of additional_properties
    if isinstance(link, SchemaBaseDependencyLinkFieldDefinitionsItem):
        id = link.additional_properties.get("id", UNSET)
        name = link.additional_properties["name"]
        resource_id = link.additional_properties.get("resourceId", None)
        resource_name = link.additional_properties.get("resourceName", None)
        return SubdependencyLink(id=id, name=name, resource_id=resource_id, resource_name=resource_name)
    return link


class SchemaFieldsMixin(Subdependencies):
    """Implements Subdependencies for schema fields."""

    def subdependency_links(self: HasEntityLink) -> List[SubdependencyLink]:
        """Get field definition dependency links from a dependency with schema fields."""
        # TODO: BNCH-50127
        return self.link.field_definitions  # type: ignore

    def subdependency_type_display_name(self) -> str:
        """Get the user-friendly name for this subdependency type."""
        return "field"


class WorkflowTaskSchemaOutputFieldsMixin(Subdependencies):
    """Implements Subdependencies for workflow task schema output schema fields."""

    def subdependency_links(self: HasWorkflowTaskSchemaParentLink) -> List[SubdependencyLink]:
        """Get field definition dependency links from a workflow task schema output with schema fields."""
        # TODO: BNCH-50127
        return self.parent.link.output.field_definitions  # type: ignore

    def subdependency_type_display_name(self) -> str:
        """Get the user-friendly name for this subdependency type."""
        return "workflow task schema output field"


@dataclass
class SchemaDependency(ApiDependency[SchemaDependencyLink], SchemaFieldsMixin):
    """
    Schema Dependency.

    Links a Benchling schema for types other than bio entities.
    """

    link: SchemaDependencyLink


@dataclass
class EntitySchemaDependency(ApiDependency[EntitySchemaDependencyLink], SchemaFieldsMixin):
    """
    Entity Schema Dependency.

    Links a Benchling entity schema.
    """

    link: EntitySchemaDependencyLink


@dataclass
class DropdownDependency(ApiDependency[DropdownDependencyLink], Subdependencies):
    """
    Dropdown Dependency.

    Links a Benchling dropdown.
    """

    link: DropdownDependencyLink

    def subdependency_links(self) -> List[SubdependencyLink]:
        """Get options dependency links from a dropdown dependency."""
        return self.link.options

    def subdependency_type_display_name(self) -> str:
        """Get the user-friendly name for this subdependency type."""
        return "option"


@dataclass
class DropdownOptionsDependency:
    """
    Dropdown Options Dependency.

    Links a Benchling dropdown with options to the parent that owns those options.
    """

    parent: DropdownDependency


@dataclass
class SchemaFieldsDependency:
    """
    Schema Fields Dependency.

    Links a Benchling object with schema fields to the parent that owns those fields.
    """

    parent: Union[
        EntitySchemaDependency,
        SchemaDependency,
        WorkflowTaskSchemaDependency,
        WorkflowTaskSchemaOutputDependency,
    ]


@dataclass
class Subdependency(ApiDependency[SubdependencyLink]):
    """
    Subdependency.

    Holds a reference to an API identified Benchling subdependency that belongs to a parent.
    Examples are fields on a schema or options on a dropdown.
    """

    link: SubdependencyLink


@dataclass
class ResourceDependency(ApiDependency[ResourceDependencyLink]):
    """
    Resource Dependency.

    Holds a reference to an API identified Benchling resource.
    Typically a singleton, such as a registry, or particular entity.
    """

    link: ResourceDependencyLink


@dataclass
class ScalarDependency:
    """
    Scalar Dependency.

    Scalars are values that can be represented outside the Benchling domain.
    """

    config: Union[ScalarConfig, SecureTextConfig]
    definition: Optional[ScalarDefinition]


@dataclass
class SecureTextDependency(ScalarDependency):
    """
    SecureText Config.

    A dependency for accessing a secure_text config.
    """

    # This is declared Optional because a decryption provider is not required until attempting
    # to decrypt a value.
    decryption_provider: Optional[BaseDecryptionProvider]


@dataclass
class WorkflowTaskSchemaDependency(ApiDependency[WorkflowTaskSchemaDependencyLink], SchemaFieldsMixin):
    """
    Workflow Task Schema Dependency.

    Links a Benchling workflow task schema.
    """

    link: WorkflowTaskSchemaDependencyLink


@dataclass
class WorkflowTaskSchemaOutputDependency(WorkflowTaskSchemaOutputFieldsMixin):
    """
    Workflow Task Schema Output Dependency.

    Links a Benchling workflow task schema output to its parent workflow task schema.
    """

    parent: WorkflowTaskSchemaDependency


class BaseDependencies:
    """
    A base class for implementing dependencies.

    Used as a facade for the underlying link store, which holds dependency links configured in Benchling.
    """

    _store: DependencyLinkStore
    _scalar_definitions: Dict[ScalarConfigTypes, ScalarDefinition]
    _unknown_scalar_definition: Optional[ScalarDefinition]
    # Will be required at runtime if an app attempts to decrypt a secure_text config
    _decryption_provider: Optional[BaseDecryptionProvider]

    def __init__(
        self,
        store: DependencyLinkStore,
        scalar_definitions: Dict[ScalarConfigTypes, ScalarDefinition] = DEFAULT_SCALAR_DEFINITIONS,
        unknown_scalar_definition: Optional[ScalarDefinition] = None,
        decryption_provider: Optional[BaseDecryptionProvider] = None,
    ):
        """
        Initialize Base Dependencies.

        :param store: The dependency link store to source dependency links from.
        :param scalar_definitions: A map of scalar types from the API definitions to ScalarDefinitions which
        determines how we want map them to concrete Python types and values. Can be overridden to customize
        deserialization behavior or formatting.
        :param unknown_scalar_definition: A scalar definition for handling unknown scalar types from the API. Can be
        used to control behavior for forwards compatibility with new types the SDK does not yet support (e.g.,
        by treating them as strings).
        :param decryption_provider: A decryption provider that can decrypt secrets from app config. If
        dependencies attempt to use a secure_text's decrypted value, a decryption_provider must be specified.
        """
        self._store = store
        self._scalar_definitions = scalar_definitions
        self._unknown_scalar_definition = unknown_scalar_definition
        self._decryption_provider = decryption_provider

    @classmethod
    def from_app(
        cls: Type[D],
        client: Benchling,
        app_id: str,
        decryption_provider: Optional[BaseDecryptionProvider] = None,
    ) -> D:
        """Initialize dependencies from an app_id."""
        link_store = DependencyLinkStore.from_app(client=client, app_id=app_id)
        return cls(link_store, decryption_provider=decryption_provider)

    def invalidate_cache(self) -> None:
        """Invalidate the cache of dependency links and force an update."""
        self._store.invalidate_cache()
