# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['DatabaseArgs', 'Database']

@pulumi.input_type
class DatabaseArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Database resource.
        :param pulumi.Input[str] instance_id: UUID of the instance where to create the database.
        :param pulumi.Input[str] name: Name of the database (e.g. `my-new-database`).
        """
        pulumi.set(__self__, "instance_id", instance_id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        UUID of the instance where to create the database.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the database (e.g. `my-new-database`).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _DatabaseState:
    def __init__(__self__, *,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 managed: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Database resources.
        :param pulumi.Input[str] instance_id: UUID of the instance where to create the database.
        :param pulumi.Input[bool] managed: Whether or not the database is managed or not.
        :param pulumi.Input[str] name: Name of the database (e.g. `my-new-database`).
        :param pulumi.Input[str] owner: The name of the owner of the database.
        :param pulumi.Input[str] size: Size of the database (in bytes).
        """
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if managed is not None:
            pulumi.set(__self__, "managed", managed)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if owner is not None:
            pulumi.set(__self__, "owner", owner)
        if size is not None:
            pulumi.set(__self__, "size", size)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        UUID of the instance where to create the database.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def managed(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not the database is managed or not.
        """
        return pulumi.get(self, "managed")

    @managed.setter
    def managed(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "managed", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the database (e.g. `my-new-database`).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def owner(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the owner of the database.
        """
        return pulumi.get(self, "owner")

    @owner.setter
    def owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[str]]:
        """
        Size of the database (in bytes).
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "size", value)


class Database(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates and manages Scaleway RDB database.
        For more information, see [the documentation](https://developers.scaleway.com/en/products/rdb/api).

        ## Examples

        ### Basic

        ```python
        import pulumi
        import lbrlabs_scaleway as scaleway

        main = scaleway.Database("main", instance_id=scaleway_rdb_instance["main"]["id"])
        ```

        ## Import

        RDB Database can be imported using the `{region}/{id}/{DBNAME}`, e.g. bash

        ```sh
         $ pulumi import scaleway:index/database:Database rdb01_mydb fr-par/11111111-1111-1111-1111-111111111111/mydb
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: UUID of the instance where to create the database.
        :param pulumi.Input[str] name: Name of the database (e.g. `my-new-database`).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DatabaseArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates and manages Scaleway RDB database.
        For more information, see [the documentation](https://developers.scaleway.com/en/products/rdb/api).

        ## Examples

        ### Basic

        ```python
        import pulumi
        import lbrlabs_scaleway as scaleway

        main = scaleway.Database("main", instance_id=scaleway_rdb_instance["main"]["id"])
        ```

        ## Import

        RDB Database can be imported using the `{region}/{id}/{DBNAME}`, e.g. bash

        ```sh
         $ pulumi import scaleway:index/database:Database rdb01_mydb fr-par/11111111-1111-1111-1111-111111111111/mydb
        ```

        :param str resource_name: The name of the resource.
        :param DatabaseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatabaseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DatabaseArgs.__new__(DatabaseArgs)

            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            __props__.__dict__["name"] = name
            __props__.__dict__["managed"] = None
            __props__.__dict__["owner"] = None
            __props__.__dict__["size"] = None
        super(Database, __self__).__init__(
            'scaleway:index/database:Database',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            managed: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            owner: Optional[pulumi.Input[str]] = None,
            size: Optional[pulumi.Input[str]] = None) -> 'Database':
        """
        Get an existing Database resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: UUID of the instance where to create the database.
        :param pulumi.Input[bool] managed: Whether or not the database is managed or not.
        :param pulumi.Input[str] name: Name of the database (e.g. `my-new-database`).
        :param pulumi.Input[str] owner: The name of the owner of the database.
        :param pulumi.Input[str] size: Size of the database (in bytes).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DatabaseState.__new__(_DatabaseState)

        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["managed"] = managed
        __props__.__dict__["name"] = name
        __props__.__dict__["owner"] = owner
        __props__.__dict__["size"] = size
        return Database(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        UUID of the instance where to create the database.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def managed(self) -> pulumi.Output[bool]:
        """
        Whether or not the database is managed or not.
        """
        return pulumi.get(self, "managed")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the database (e.g. `my-new-database`).
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def owner(self) -> pulumi.Output[str]:
        """
        The name of the owner of the database.
        """
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter
    def size(self) -> pulumi.Output[str]:
        """
        Size of the database (in bytes).
        """
        return pulumi.get(self, "size")

