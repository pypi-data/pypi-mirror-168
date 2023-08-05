# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetAwsConnectorResult',
    'AwaitableGetAwsConnectorResult',
    'get_aws_connector',
    'get_aws_connector_output',
]

@pulumi.output_type
class GetAwsConnectorResult:
    """
    A collection of values returned by getAwsConnector.
    """
    def __init__(__self__, cross_account_accesses=None, description=None, id=None, identifier=None, inherit_from_delegates=None, irsas=None, manuals=None, name=None, org_id=None, project_id=None, tags=None):
        if cross_account_accesses and not isinstance(cross_account_accesses, list):
            raise TypeError("Expected argument 'cross_account_accesses' to be a list")
        pulumi.set(__self__, "cross_account_accesses", cross_account_accesses)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identifier and not isinstance(identifier, str):
            raise TypeError("Expected argument 'identifier' to be a str")
        pulumi.set(__self__, "identifier", identifier)
        if inherit_from_delegates and not isinstance(inherit_from_delegates, list):
            raise TypeError("Expected argument 'inherit_from_delegates' to be a list")
        pulumi.set(__self__, "inherit_from_delegates", inherit_from_delegates)
        if irsas and not isinstance(irsas, list):
            raise TypeError("Expected argument 'irsas' to be a list")
        pulumi.set(__self__, "irsas", irsas)
        if manuals and not isinstance(manuals, list):
            raise TypeError("Expected argument 'manuals' to be a list")
        pulumi.set(__self__, "manuals", manuals)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="crossAccountAccesses")
    def cross_account_accesses(self) -> Sequence['outputs.GetAwsConnectorCrossAccountAccessResult']:
        """
        Select this option if you want to use one AWS account for the connection, but you want to deploy or build in a different AWS account. In this scenario, the AWS account used for AWS access in Credentials will assume the IAM role you specify in Cross-account role ARN setting. This option uses the AWS Security Token Service (STS) feature.
        """
        return pulumi.get(self, "cross_account_accesses")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identifier(self) -> Optional[str]:
        """
        Unique identifier of the resource.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter(name="inheritFromDelegates")
    def inherit_from_delegates(self) -> Sequence['outputs.GetAwsConnectorInheritFromDelegateResult']:
        """
        Inherit credentials from the delegate.
        """
        return pulumi.get(self, "inherit_from_delegates")

    @property
    @pulumi.getter
    def irsas(self) -> Sequence['outputs.GetAwsConnectorIrsaResult']:
        """
        Use IAM role for service accounts.
        """
        return pulumi.get(self, "irsas")

    @property
    @pulumi.getter
    def manuals(self) -> Sequence['outputs.GetAwsConnectorManualResult']:
        """
        Use IAM role for service accounts.
        """
        return pulumi.get(self, "manuals")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[str]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[str]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def tags(self) -> Sequence[str]:
        """
        Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        return pulumi.get(self, "tags")


class AwaitableGetAwsConnectorResult(GetAwsConnectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAwsConnectorResult(
            cross_account_accesses=self.cross_account_accesses,
            description=self.description,
            id=self.id,
            identifier=self.identifier,
            inherit_from_delegates=self.inherit_from_delegates,
            irsas=self.irsas,
            manuals=self.manuals,
            name=self.name,
            org_id=self.org_id,
            project_id=self.project_id,
            tags=self.tags)


def get_aws_connector(identifier: Optional[str] = None,
                      name: Optional[str] = None,
                      org_id: Optional[str] = None,
                      project_id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAwsConnectorResult:
    """
    Datasource for looking up an AWS connector.


    :param str identifier: Unique identifier of the resource.
    :param str name: Name of the resource.
    :param str org_id: Unique identifier of the organization.
    :param str project_id: Unique identifier of the project.
    """
    __args__ = dict()
    __args__['identifier'] = identifier
    __args__['name'] = name
    __args__['orgId'] = org_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('harness:platform/getAwsConnector:getAwsConnector', __args__, opts=opts, typ=GetAwsConnectorResult).value

    return AwaitableGetAwsConnectorResult(
        cross_account_accesses=__ret__.cross_account_accesses,
        description=__ret__.description,
        id=__ret__.id,
        identifier=__ret__.identifier,
        inherit_from_delegates=__ret__.inherit_from_delegates,
        irsas=__ret__.irsas,
        manuals=__ret__.manuals,
        name=__ret__.name,
        org_id=__ret__.org_id,
        project_id=__ret__.project_id,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_aws_connector)
def get_aws_connector_output(identifier: Optional[pulumi.Input[Optional[str]]] = None,
                             name: Optional[pulumi.Input[Optional[str]]] = None,
                             org_id: Optional[pulumi.Input[Optional[str]]] = None,
                             project_id: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAwsConnectorResult]:
    """
    Datasource for looking up an AWS connector.


    :param str identifier: Unique identifier of the resource.
    :param str name: Name of the resource.
    :param str org_id: Unique identifier of the organization.
    :param str project_id: Unique identifier of the project.
    """
    ...
