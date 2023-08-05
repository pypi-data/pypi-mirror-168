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
    'GetAwsSecretManagerConnectorResult',
    'AwaitableGetAwsSecretManagerConnectorResult',
    'get_aws_secret_manager_connector',
    'get_aws_secret_manager_connector_output',
]

@pulumi.output_type
class GetAwsSecretManagerConnectorResult:
    """
    A collection of values returned by getAwsSecretManagerConnector.
    """
    def __init__(__self__, credentials=None, delegate_selectors=None, description=None, id=None, identifier=None, name=None, org_id=None, project_id=None, region=None, secret_name_prefix=None, tags=None):
        if credentials and not isinstance(credentials, list):
            raise TypeError("Expected argument 'credentials' to be a list")
        pulumi.set(__self__, "credentials", credentials)
        if delegate_selectors and not isinstance(delegate_selectors, list):
            raise TypeError("Expected argument 'delegate_selectors' to be a list")
        pulumi.set(__self__, "delegate_selectors", delegate_selectors)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identifier and not isinstance(identifier, str):
            raise TypeError("Expected argument 'identifier' to be a str")
        pulumi.set(__self__, "identifier", identifier)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if secret_name_prefix and not isinstance(secret_name_prefix, str):
            raise TypeError("Expected argument 'secret_name_prefix' to be a str")
        pulumi.set(__self__, "secret_name_prefix", secret_name_prefix)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def credentials(self) -> Sequence['outputs.GetAwsSecretManagerConnectorCredentialResult']:
        """
        The credentials to use for connecting to aws.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter(name="delegateSelectors")
    def delegate_selectors(self) -> Sequence[str]:
        """
        Connect using only the delegates which have these tags.
        """
        return pulumi.get(self, "delegate_selectors")

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
    def region(self) -> str:
        """
        The AWS region where the AWS Secret Manager is.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="secretNamePrefix")
    def secret_name_prefix(self) -> str:
        """
        A prefix to be added to all secrets.
        """
        return pulumi.get(self, "secret_name_prefix")

    @property
    @pulumi.getter
    def tags(self) -> Sequence[str]:
        """
        Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        return pulumi.get(self, "tags")


class AwaitableGetAwsSecretManagerConnectorResult(GetAwsSecretManagerConnectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAwsSecretManagerConnectorResult(
            credentials=self.credentials,
            delegate_selectors=self.delegate_selectors,
            description=self.description,
            id=self.id,
            identifier=self.identifier,
            name=self.name,
            org_id=self.org_id,
            project_id=self.project_id,
            region=self.region,
            secret_name_prefix=self.secret_name_prefix,
            tags=self.tags)


def get_aws_secret_manager_connector(identifier: Optional[str] = None,
                                     name: Optional[str] = None,
                                     org_id: Optional[str] = None,
                                     project_id: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAwsSecretManagerConnectorResult:
    """
    Datasource for looking up an AWS Secret Manager connector.


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
    __ret__ = pulumi.runtime.invoke('harness:platform/getAwsSecretManagerConnector:getAwsSecretManagerConnector', __args__, opts=opts, typ=GetAwsSecretManagerConnectorResult).value

    return AwaitableGetAwsSecretManagerConnectorResult(
        credentials=__ret__.credentials,
        delegate_selectors=__ret__.delegate_selectors,
        description=__ret__.description,
        id=__ret__.id,
        identifier=__ret__.identifier,
        name=__ret__.name,
        org_id=__ret__.org_id,
        project_id=__ret__.project_id,
        region=__ret__.region,
        secret_name_prefix=__ret__.secret_name_prefix,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_aws_secret_manager_connector)
def get_aws_secret_manager_connector_output(identifier: Optional[pulumi.Input[Optional[str]]] = None,
                                            name: Optional[pulumi.Input[Optional[str]]] = None,
                                            org_id: Optional[pulumi.Input[Optional[str]]] = None,
                                            project_id: Optional[pulumi.Input[Optional[str]]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAwsSecretManagerConnectorResult]:
    """
    Datasource for looking up an AWS Secret Manager connector.


    :param str identifier: Unique identifier of the resource.
    :param str name: Name of the resource.
    :param str org_id: Unique identifier of the organization.
    :param str project_id: Unique identifier of the project.
    """
    ...
