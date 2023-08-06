# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

"""
Entities generator for JSONAPI style responses in our Pyramid framework

This module generates a openapi 3.0 compatible entity file containing a list
of components generated from the given zsnl_domains entity module.

In short: it uses pydantic.schema() for every entity this module can find in
the given domain, and turns it into a JSONAPI compatible output for your
openapi specification

Example:

    $ generate-entities --entitymod=zsnl_domains.case_management.entities

"""

import json
import jsonpath_ng as jp
from copy import deepcopy
from importlib import import_module
from minty.entity import Entity
from pydantic.schema import schema
from typing import Any, Dict, Type


def _preprocess_entity_schema(
    schema_definition: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process all properties in a schema (recursively), and translate parts that
    are not valid OpenAPI 3.0.x to valid OpenAPI 3.0.x.
    """
    properties = jp.parse("$..properties").find(schema_definition)

    for property in properties:
        for prop in property.value.values():
            if "const" in prop and "enum" not in prop:
                # OpenAPI 3.0.x doesn't understand "const" in schemas, because
                # it is part of a "too new" version of the JSON Schema spec.
                prop["enum"] = [prop["const"]]
                del prop["const"]

    return schema_definition


class EntityGenerator:
    """The actual generator logic to transform pydantic entities to jsonapi

    An instance of this object turns the given entities in the given entities
    module into a JSONAPI and OpenAPI compatible "components" output.
    """

    entitymod: Any
    entities: list[Type[Entity]]

    def __init__(self, entity_module_name):
        """Initializes an instance of this entity generator

        Args:
            entity_module_name (module): name of the module containing all the
                entities in the __all__ attribute.
        """

        entities_module = import_module(entity_module_name)
        self.entitymod = entities_module

        self.entities = []
        self._load_entities()

    def _load_entities(self):
        """Adds all class instances of the loaded entity module

        Appends every entity class instance in attribute self.entities
        """
        for entity in self.entitymod.__all__:
            self.entities.append(getattr(self.entitymod, entity))

    def generate(self):
        """Generates a JSONAPI openapi compatible schema output

        For every entity in self.entities it generates a JSONAPI compatible
        entry in an openapi compatible json format
        """

        entity_types = [e for e in self.entities if issubclass(e, Entity)]

        definitions = self._build_schema_for_entity_types(entity_types)

        jsonapischema = definitions["definitions"]

        # Make sure every ref link gets updated to the proper location
        matches = jp.parse("$..'$ref'").find(definitions)

        for match in matches:
            link = match.value
            definitions_prefix = "#/definitions/"
            link_destination = link[
                link.startswith(definitions_prefix)
                and len(definitions_prefix) :
            ]

            if f"Entity{link_destination}" in jsonapischema:
                refvalue = match.value.replace(
                    "#/definitions/", "#/components/schemas/Entity"
                )
            else:
                refvalue = match.value.replace(
                    "#/definitions/", "#/components/schemas/"
                )

            match.context.value["$ref"] = refvalue

        return {"components": {"schemas": jsonapischema}}

    def generate_json(self):
        """Generates a string json response

        Same as generate, but instead of returning a python dict, it will
        return a json formatted string of it.
        """
        return json.dumps(self.generate(), sort_keys=True, indent=2)

    def generate_json_api_object(
        self,
        meta_schema,
        attribute_schema,
        entity_type,
        relationships=None,
        schema_required=None,
    ):
        """Generate a jsonapi formatted python object

        Will generate a json_api_object from the given arguments. Including
        links, attributes, relationships.

        Args:
            meta_schema (dict): A schema dictionary containing meta fields
            attribute_schema (dict): A schema dictionary containing fields for
                the attribute part of jsonapi
            entity_type (str): The name of this object (type), e.g.: "case"
            relationships (dict): An instruction of a relationship (key) and
                information about the relationship (is_list) and it's
                (entity_type)
            schema_required (list): A list of required parameters from original
                schema
        """
        if relationships is None:
            relationships = {}

        if schema_required is None:
            schema_required = []

        relationship_schema = {
            key: self._generate_json_api_relationship(key, value)
            for key, value in relationships.items()
        }

        required_field = {}

        if len(attribute_schema) > 0 and len(schema_required):
            schema_required_fields = [
                key for key in schema_required if key in attribute_schema
            ]
            if schema_required_fields:
                required_field["required"] = schema_required_fields

        return {
            "properties": {
                "type": {
                    "type": "string",
                    "example": entity_type,
                    "enum": [entity_type],
                },
                "id": {"type": "string", "format": "uuid"},
                "meta": {"type": "object", "properties": meta_schema},
                "attributes": {
                    "type": "object",
                    "properties": attribute_schema,
                    **required_field,
                },
                "relationships": {
                    "type": "object",
                    "properties": relationship_schema,
                },
                "links": {
                    "type": "object",
                    "properties": {
                        "self": {
                            "type": "string",
                            "pattern": "^/api/v2/.*$",
                            "example": "/api/v2/get_something?uuid=1a2b3c4d-1a2b-1a2b-1a2b-1a2b3c4d5e6f",
                        }
                    },
                },
            },
            "required": ["type", "id", "attributes"],
        }

    def _generate_json_api_relationship(self, name, relationship_info):
        """Generate the jsonapi formatted part for the relationships

        Args:
            name (str): Name of the relationship, e.g: "brand"
            relationship_info (dict): An instruction of the relationship with
                information about the relationship (is_list) and it's
                (entity_type)
        """
        relationship_type = {"type": "string"}

        if relationship_info["entity_type"]:
            relationship_type["example"] = relationship_info["entity_type"]

        relationship_schema_output = {
            "type": "object",
            "required": ["data"],
            "properties": {
                "links": {
                    "type": "object",
                    "properties": {
                        "self": {
                            "type": "string",
                            "pattern": "^/api/v2/.*$",
                            "example": "/api/v2/get_something?uuid=1a2b3c4d-1a2b-1a2b-1a2b-1a2b3c4d5e6f",
                        }
                    },
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "type": relationship_type,
                        "id": {"type": "string", "format": "uuid"},
                    },
                },
            },
        }

        if relationship_info["is_list"]:
            relationship_schema_output = {
                "type": "array",
                "items": relationship_schema_output,
            }

        return relationship_schema_output

    def _transform_entity_type_definition(
        self, entity: Type[Entity], schema: Dict[str, Any]
    ):
        """
        Transform JSON Schema for an entity to a JSON:API compatible version
        """
        jsonschema = self.generate_json_api_object(
            meta_schema=self._get_meta_from_entity(
                entity, schema["properties"]
            ),
            attribute_schema=self._get_attributes_from_entity(
                entity, schema["properties"]
            ),
            relationships=self._get_relationships_from_entity(
                entity, schema["properties"]
            ),
            entity_type=entity.__fields__["entity_type"].get_default(),
            schema_required=schema.get("required", []),
        )

        schema["properties"] = jsonschema["properties"]
        schema["required"] = jsonschema["required"]

        # del schema["title"]

        return schema

    def _get_meta_from_entity(self, entity, properties):
        """Generate the jsonapi formatted part for the meta part

        Args:
            entity (:obj:`Entity`): The pydantic based entity to convert
            properties (dict): The properties part of the entity
        """
        meta_properties = {}

        for prop in properties.keys():
            if (
                prop.startswith("entity_meta_")
                and prop != "entity_meta__fields"
            ):
                meta_properties[prop.replace("entity_meta_", "")] = properties[
                    prop
                ]

        return meta_properties

    def _get_attributes_from_entity(self, entity, properties):
        """Generate the jsonapi formatted part for the attributes part

        Args:
            entity (:obj:`Entity`): The pydantic based entity to convert
            properties (dict): The properties part of the entity
        """
        attribute_properties = deepcopy(properties)
        for prop in properties.keys():
            if "default" in attribute_properties[prop]:
                del attribute_properties[prop]["default"]

            if (
                prop.startswith("entity_")
                or prop in entity.__fields__.get("entity_id__fields").default
                or prop
                in entity.__fields__.get("entity_relationships").default
            ):
                del attribute_properties[prop]

        return attribute_properties

    def _get_relationships_from_entity(self, entity, properties):
        """Generate the jsonapi formatted part for the relationships part

        Args:
            entity (:obj:`Entity`): The pydantic based entity to convert
            properties (dict): The properties part of the entity
        """
        relationships = {}
        for relationship in entity.__fields__.get(
            "entity_relationships"
        ).default:
            is_list = False
            if (
                "type" in properties[relationship]
                and properties[relationship]["type"] == "array"
            ):
                is_list = True

            relationship_type = None
            try:
                relationship_type = (
                    entity.__fields__.get(relationship)
                    .type_.__fields__.get("entity_type")
                    .default
                )
            except Exception:
                pass

            relationships[relationship] = {
                "is_list": is_list,
                "entity_type": None,
            }

            if relationship_type:
                relationships[relationship]["entity_type"] = relationship_type

        return relationships

    def generate_jsonapi_envelope_for(self, schema_definition, multiple=False):
        """Generate an envelope for the jsonapi formatted object

        The envelope contains, depending of the context (list or a single
        result) the data and links attributes

        Args:
            schema (dict): The schema to include in the envelope
            multiple (bool): Indicates whether we want the response in a single
                jsonapi formatted response, or in a list format
        """
        envelope = {
            "type": "object",
            "required": ["data", "links"],
            "properties": {
                "data": None,
                "links": {
                    "type": "object",
                    "properties": {
                        "self": {
                            "type": "string",
                            "pattern": "^/api/v2/.*$",
                            "example": "/api/v2/get_something?uuid=1a2b3c4d-1a2b-1a2b-1a2b-1a2b3c4d5e6f",
                        }
                    },
                },
            },
        }

        if multiple:
            envelope["properties"]["data"] = {
                "type": "array",
                "items": schema_definition,
            }
            envelope["properties"]["meta"] = {
                "type": "object",
                "properties": {"total_results": {"type": "integer"}},
            }
        else:
            envelope["properties"]["data"] = schema_definition

        return envelope

    def _build_schema_for_entity_types(
        self, entity_types: list[Type[Entity]]
    ) -> Dict[str, Any]:
        """Transforms the the given entity in a jsonapi formatted object"""

        schema_definition = schema(entity_types)
        schema_definition = _preprocess_entity_schema(schema_definition)

        for entity_type in entity_types:
            entity_type_name = entity_type.__name__

            try:
                entity_definition = schema_definition["definitions"][
                    entity_type_name
                ]
            except KeyError as e:
                raise AssertionError(
                    f"Entity not found in JSON: {entity_type_name}. "
                    "Most likely cause: duplicate name."
                ) from e

            del schema_definition["definitions"][entity_type_name]

            jsonapi_definition = self._transform_entity_type_definition(
                entity_type, entity_definition
            )

            schema_definition["definitions"][
                f"Entity{entity_type_name}"
            ] = self.generate_jsonapi_envelope_for(jsonapi_definition)
            schema_definition["definitions"][
                f"Entity{entity_type_name}List"
            ] = self.generate_jsonapi_envelope_for(
                jsonapi_definition,
                multiple=True,
            )

        return schema_definition
