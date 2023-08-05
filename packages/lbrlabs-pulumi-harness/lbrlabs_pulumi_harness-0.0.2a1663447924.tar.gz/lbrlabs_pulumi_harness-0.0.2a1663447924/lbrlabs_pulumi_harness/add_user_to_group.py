# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AddUserToGroupArgs', 'AddUserToGroup']

@pulumi.input_type
class AddUserToGroupArgs:
    def __init__(__self__, *,
                 group_id: pulumi.Input[str],
                 user_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a AddUserToGroup resource.
        :param pulumi.Input[str] group_id: The name of the user.
        :param pulumi.Input[str] user_id: Unique identifier of the user.
        """
        pulumi.set(__self__, "group_id", group_id)
        pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Input[str]:
        """
        The name of the user.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Input[str]:
        """
        Unique identifier of the user.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_id", value)


@pulumi.input_type
class _AddUserToGroupState:
    def __init__(__self__, *,
                 group_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AddUserToGroup resources.
        :param pulumi.Input[str] group_id: The name of the user.
        :param pulumi.Input[str] user_id: Unique identifier of the user.
        """
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the user.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)


class AddUserToGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for adding a user to a group.

        ## Example Usage

        ```python
        import pulumi
        import lbrlabs_pulumi_harness as harness
        import pulumi_harness as harness

        example_user = harness.get_user(email="testuser@example.com")
        admin = harness.UserGroup("admin")
        example_add_user_to_groups = harness.AddUserToGroup("exampleAddUserToGroups",
            group_id=admin.id,
            user_id=data["harness_user"]["test"]["id"])
        ```

        ## Import

        # Import using the Harness user and user group id

        ```sh
         $ pulumi import harness:index/addUserToGroup:AddUserToGroup example_admin <user_id>/<group_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_id: The name of the user.
        :param pulumi.Input[str] user_id: Unique identifier of the user.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AddUserToGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for adding a user to a group.

        ## Example Usage

        ```python
        import pulumi
        import lbrlabs_pulumi_harness as harness
        import pulumi_harness as harness

        example_user = harness.get_user(email="testuser@example.com")
        admin = harness.UserGroup("admin")
        example_add_user_to_groups = harness.AddUserToGroup("exampleAddUserToGroups",
            group_id=admin.id,
            user_id=data["harness_user"]["test"]["id"])
        ```

        ## Import

        # Import using the Harness user and user group id

        ```sh
         $ pulumi import harness:index/addUserToGroup:AddUserToGroup example_admin <user_id>/<group_id>
        ```

        :param str resource_name: The name of the resource.
        :param AddUserToGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AddUserToGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AddUserToGroupArgs.__new__(AddUserToGroupArgs)

            if group_id is None and not opts.urn:
                raise TypeError("Missing required property 'group_id'")
            __props__.__dict__["group_id"] = group_id
            if user_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_id'")
            __props__.__dict__["user_id"] = user_id
        super(AddUserToGroup, __self__).__init__(
            'harness:index/addUserToGroup:AddUserToGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            group_id: Optional[pulumi.Input[str]] = None,
            user_id: Optional[pulumi.Input[str]] = None) -> 'AddUserToGroup':
        """
        Get an existing AddUserToGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_id: The name of the user.
        :param pulumi.Input[str] user_id: Unique identifier of the user.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AddUserToGroupState.__new__(_AddUserToGroupState)

        __props__.__dict__["group_id"] = group_id
        __props__.__dict__["user_id"] = user_id
        return AddUserToGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[str]:
        """
        The name of the user.
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        Unique identifier of the user.
        """
        return pulumi.get(self, "user_id")

