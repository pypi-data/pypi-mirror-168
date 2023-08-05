# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetUserGroupResult',
    'AwaitableGetUserGroupResult',
    'get_user_group',
    'get_user_group_output',
]

@pulumi.output_type
class GetUserGroupResult:
    """
    A collection of values returned by getUserGroup.
    """
    def __init__(__self__, id=None, name=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Unique identifier of the user group
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the user group.
        """
        return pulumi.get(self, "name")


class AwaitableGetUserGroupResult(GetUserGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserGroupResult(
            id=self.id,
            name=self.name)


def get_user_group(id: Optional[str] = None,
                   name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserGroupResult:
    """
    Data source for retrieving a Harness user group


    :param str id: Unique identifier of the user group
    :param str name: The name of the user group.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('harness:index/getUserGroup:getUserGroup', __args__, opts=opts, typ=GetUserGroupResult).value

    return AwaitableGetUserGroupResult(
        id=__ret__.id,
        name=__ret__.name)


@_utilities.lift_output_func(get_user_group)
def get_user_group_output(id: Optional[pulumi.Input[Optional[str]]] = None,
                          name: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserGroupResult]:
    """
    Data source for retrieving a Harness user group


    :param str id: Unique identifier of the user group
    :param str name: The name of the user group.
    """
    ...
