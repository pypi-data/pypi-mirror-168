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
    'GetKubernetesConnectorResult',
    'AwaitableGetKubernetesConnectorResult',
    'get_kubernetes_connector',
    'get_kubernetes_connector_output',
]

@pulumi.output_type
class GetKubernetesConnectorResult:
    """
    A collection of values returned by getKubernetesConnector.
    """
    def __init__(__self__, client_key_certs=None, delegate_selectors=None, description=None, id=None, identifier=None, inherit_from_delegates=None, name=None, openid_connects=None, org_id=None, project_id=None, service_accounts=None, tags=None, username_passwords=None):
        if client_key_certs and not isinstance(client_key_certs, list):
            raise TypeError("Expected argument 'client_key_certs' to be a list")
        pulumi.set(__self__, "client_key_certs", client_key_certs)
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
        if inherit_from_delegates and not isinstance(inherit_from_delegates, list):
            raise TypeError("Expected argument 'inherit_from_delegates' to be a list")
        pulumi.set(__self__, "inherit_from_delegates", inherit_from_delegates)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if openid_connects and not isinstance(openid_connects, list):
            raise TypeError("Expected argument 'openid_connects' to be a list")
        pulumi.set(__self__, "openid_connects", openid_connects)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if service_accounts and not isinstance(service_accounts, list):
            raise TypeError("Expected argument 'service_accounts' to be a list")
        pulumi.set(__self__, "service_accounts", service_accounts)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if username_passwords and not isinstance(username_passwords, list):
            raise TypeError("Expected argument 'username_passwords' to be a list")
        pulumi.set(__self__, "username_passwords", username_passwords)

    @property
    @pulumi.getter(name="clientKeyCerts")
    def client_key_certs(self) -> Sequence['outputs.GetKubernetesConnectorClientKeyCertResult']:
        """
        Client key and certificate config for the connector.
        """
        return pulumi.get(self, "client_key_certs")

    @property
    @pulumi.getter(name="delegateSelectors")
    def delegate_selectors(self) -> Sequence[str]:
        """
        Selectors to use for the delegate.
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
    @pulumi.getter(name="inheritFromDelegates")
    def inherit_from_delegates(self) -> Sequence['outputs.GetKubernetesConnectorInheritFromDelegateResult']:
        """
        Credentials are inherited from the delegate.
        """
        return pulumi.get(self, "inherit_from_delegates")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="openidConnects")
    def openid_connects(self) -> Sequence['outputs.GetKubernetesConnectorOpenidConnectResult']:
        """
        OpenID configuration for the connector.
        """
        return pulumi.get(self, "openid_connects")

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
    @pulumi.getter(name="serviceAccounts")
    def service_accounts(self) -> Sequence['outputs.GetKubernetesConnectorServiceAccountResult']:
        """
        Service account for the connector.
        """
        return pulumi.get(self, "service_accounts")

    @property
    @pulumi.getter
    def tags(self) -> Sequence[str]:
        """
        Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="usernamePasswords")
    def username_passwords(self) -> Sequence['outputs.GetKubernetesConnectorUsernamePasswordResult']:
        """
        Username and password for the connector.
        """
        return pulumi.get(self, "username_passwords")


class AwaitableGetKubernetesConnectorResult(GetKubernetesConnectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKubernetesConnectorResult(
            client_key_certs=self.client_key_certs,
            delegate_selectors=self.delegate_selectors,
            description=self.description,
            id=self.id,
            identifier=self.identifier,
            inherit_from_delegates=self.inherit_from_delegates,
            name=self.name,
            openid_connects=self.openid_connects,
            org_id=self.org_id,
            project_id=self.project_id,
            service_accounts=self.service_accounts,
            tags=self.tags,
            username_passwords=self.username_passwords)


def get_kubernetes_connector(identifier: Optional[str] = None,
                             name: Optional[str] = None,
                             org_id: Optional[str] = None,
                             project_id: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetKubernetesConnectorResult:
    """
    Datasource for looking up a Kubernetes connector.


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
    __ret__ = pulumi.runtime.invoke('harness:platform/getKubernetesConnector:getKubernetesConnector', __args__, opts=opts, typ=GetKubernetesConnectorResult).value

    return AwaitableGetKubernetesConnectorResult(
        client_key_certs=__ret__.client_key_certs,
        delegate_selectors=__ret__.delegate_selectors,
        description=__ret__.description,
        id=__ret__.id,
        identifier=__ret__.identifier,
        inherit_from_delegates=__ret__.inherit_from_delegates,
        name=__ret__.name,
        openid_connects=__ret__.openid_connects,
        org_id=__ret__.org_id,
        project_id=__ret__.project_id,
        service_accounts=__ret__.service_accounts,
        tags=__ret__.tags,
        username_passwords=__ret__.username_passwords)


@_utilities.lift_output_func(get_kubernetes_connector)
def get_kubernetes_connector_output(identifier: Optional[pulumi.Input[Optional[str]]] = None,
                                    name: Optional[pulumi.Input[Optional[str]]] = None,
                                    org_id: Optional[pulumi.Input[Optional[str]]] = None,
                                    project_id: Optional[pulumi.Input[Optional[str]]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetKubernetesConnectorResult]:
    """
    Datasource for looking up a Kubernetes connector.


    :param str identifier: Unique identifier of the resource.
    :param str name: Name of the resource.
    :param str org_id: Unique identifier of the organization.
    :param str project_id: Unique identifier of the project.
    """
    ...
