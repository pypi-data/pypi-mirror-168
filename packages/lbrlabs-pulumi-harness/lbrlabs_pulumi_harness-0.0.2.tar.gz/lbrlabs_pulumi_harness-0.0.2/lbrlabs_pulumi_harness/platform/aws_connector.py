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
from ._inputs import *

__all__ = ['AwsConnectorArgs', 'AwsConnector']

@pulumi.input_type
class AwsConnectorArgs:
    def __init__(__self__, *,
                 identifier: pulumi.Input[str],
                 cross_account_access: Optional[pulumi.Input['AwsConnectorCrossAccountAccessArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 inherit_from_delegate: Optional[pulumi.Input['AwsConnectorInheritFromDelegateArgs']] = None,
                 irsa: Optional[pulumi.Input['AwsConnectorIrsaArgs']] = None,
                 manual: Optional[pulumi.Input['AwsConnectorManualArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a AwsConnector resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input['AwsConnectorCrossAccountAccessArgs'] cross_account_access: Select this option if you want to use one AWS account for the connection, but you want to deploy or build in a different AWS account. In this scenario, the AWS account used for AWS access in Credentials will assume the IAM role you specify in Cross-account role ARN setting. This option uses the AWS Security Token Service (STS) feature.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input['AwsConnectorInheritFromDelegateArgs'] inherit_from_delegate: Inherit credentials from the delegate.
        :param pulumi.Input['AwsConnectorIrsaArgs'] irsa: Use IAM role for service accounts.
        :param pulumi.Input['AwsConnectorManualArgs'] manual: Use IAM role for service accounts.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        pulumi.set(__self__, "identifier", identifier)
        if cross_account_access is not None:
            pulumi.set(__self__, "cross_account_access", cross_account_access)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if inherit_from_delegate is not None:
            pulumi.set(__self__, "inherit_from_delegate", inherit_from_delegate)
        if irsa is not None:
            pulumi.set(__self__, "irsa", irsa)
        if manual is not None:
            pulumi.set(__self__, "manual", manual)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Input[str]:
        """
        Unique identifier of the resource.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter(name="crossAccountAccess")
    def cross_account_access(self) -> Optional[pulumi.Input['AwsConnectorCrossAccountAccessArgs']]:
        """
        Select this option if you want to use one AWS account for the connection, but you want to deploy or build in a different AWS account. In this scenario, the AWS account used for AWS access in Credentials will assume the IAM role you specify in Cross-account role ARN setting. This option uses the AWS Security Token Service (STS) feature.
        """
        return pulumi.get(self, "cross_account_access")

    @cross_account_access.setter
    def cross_account_access(self, value: Optional[pulumi.Input['AwsConnectorCrossAccountAccessArgs']]):
        pulumi.set(self, "cross_account_access", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="inheritFromDelegate")
    def inherit_from_delegate(self) -> Optional[pulumi.Input['AwsConnectorInheritFromDelegateArgs']]:
        """
        Inherit credentials from the delegate.
        """
        return pulumi.get(self, "inherit_from_delegate")

    @inherit_from_delegate.setter
    def inherit_from_delegate(self, value: Optional[pulumi.Input['AwsConnectorInheritFromDelegateArgs']]):
        pulumi.set(self, "inherit_from_delegate", value)

    @property
    @pulumi.getter
    def irsa(self) -> Optional[pulumi.Input['AwsConnectorIrsaArgs']]:
        """
        Use IAM role for service accounts.
        """
        return pulumi.get(self, "irsa")

    @irsa.setter
    def irsa(self, value: Optional[pulumi.Input['AwsConnectorIrsaArgs']]):
        pulumi.set(self, "irsa", value)

    @property
    @pulumi.getter
    def manual(self) -> Optional[pulumi.Input['AwsConnectorManualArgs']]:
        """
        Use IAM role for service accounts.
        """
        return pulumi.get(self, "manual")

    @manual.setter
    def manual(self, value: Optional[pulumi.Input['AwsConnectorManualArgs']]):
        pulumi.set(self, "manual", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _AwsConnectorState:
    def __init__(__self__, *,
                 cross_account_access: Optional[pulumi.Input['AwsConnectorCrossAccountAccessArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 inherit_from_delegate: Optional[pulumi.Input['AwsConnectorInheritFromDelegateArgs']] = None,
                 irsa: Optional[pulumi.Input['AwsConnectorIrsaArgs']] = None,
                 manual: Optional[pulumi.Input['AwsConnectorManualArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering AwsConnector resources.
        :param pulumi.Input['AwsConnectorCrossAccountAccessArgs'] cross_account_access: Select this option if you want to use one AWS account for the connection, but you want to deploy or build in a different AWS account. In this scenario, the AWS account used for AWS access in Credentials will assume the IAM role you specify in Cross-account role ARN setting. This option uses the AWS Security Token Service (STS) feature.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input['AwsConnectorInheritFromDelegateArgs'] inherit_from_delegate: Inherit credentials from the delegate.
        :param pulumi.Input['AwsConnectorIrsaArgs'] irsa: Use IAM role for service accounts.
        :param pulumi.Input['AwsConnectorManualArgs'] manual: Use IAM role for service accounts.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        if cross_account_access is not None:
            pulumi.set(__self__, "cross_account_access", cross_account_access)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if inherit_from_delegate is not None:
            pulumi.set(__self__, "inherit_from_delegate", inherit_from_delegate)
        if irsa is not None:
            pulumi.set(__self__, "irsa", irsa)
        if manual is not None:
            pulumi.set(__self__, "manual", manual)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="crossAccountAccess")
    def cross_account_access(self) -> Optional[pulumi.Input['AwsConnectorCrossAccountAccessArgs']]:
        """
        Select this option if you want to use one AWS account for the connection, but you want to deploy or build in a different AWS account. In this scenario, the AWS account used for AWS access in Credentials will assume the IAM role you specify in Cross-account role ARN setting. This option uses the AWS Security Token Service (STS) feature.
        """
        return pulumi.get(self, "cross_account_access")

    @cross_account_access.setter
    def cross_account_access(self, value: Optional[pulumi.Input['AwsConnectorCrossAccountAccessArgs']]):
        pulumi.set(self, "cross_account_access", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def identifier(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the resource.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter(name="inheritFromDelegate")
    def inherit_from_delegate(self) -> Optional[pulumi.Input['AwsConnectorInheritFromDelegateArgs']]:
        """
        Inherit credentials from the delegate.
        """
        return pulumi.get(self, "inherit_from_delegate")

    @inherit_from_delegate.setter
    def inherit_from_delegate(self, value: Optional[pulumi.Input['AwsConnectorInheritFromDelegateArgs']]):
        pulumi.set(self, "inherit_from_delegate", value)

    @property
    @pulumi.getter
    def irsa(self) -> Optional[pulumi.Input['AwsConnectorIrsaArgs']]:
        """
        Use IAM role for service accounts.
        """
        return pulumi.get(self, "irsa")

    @irsa.setter
    def irsa(self, value: Optional[pulumi.Input['AwsConnectorIrsaArgs']]):
        pulumi.set(self, "irsa", value)

    @property
    @pulumi.getter
    def manual(self) -> Optional[pulumi.Input['AwsConnectorManualArgs']]:
        """
        Use IAM role for service accounts.
        """
        return pulumi.get(self, "manual")

    @manual.setter
    def manual(self, value: Optional[pulumi.Input['AwsConnectorManualArgs']]):
        pulumi.set(self, "manual", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class AwsConnector(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cross_account_access: Optional[pulumi.Input[pulumi.InputType['AwsConnectorCrossAccountAccessArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 inherit_from_delegate: Optional[pulumi.Input[pulumi.InputType['AwsConnectorInheritFromDelegateArgs']]] = None,
                 irsa: Optional[pulumi.Input[pulumi.InputType['AwsConnectorIrsaArgs']]] = None,
                 manual: Optional[pulumi.Input[pulumi.InputType['AwsConnectorManualArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource for creating an AWS connector.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AwsConnectorCrossAccountAccessArgs']] cross_account_access: Select this option if you want to use one AWS account for the connection, but you want to deploy or build in a different AWS account. In this scenario, the AWS account used for AWS access in Credentials will assume the IAM role you specify in Cross-account role ARN setting. This option uses the AWS Security Token Service (STS) feature.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[pulumi.InputType['AwsConnectorInheritFromDelegateArgs']] inherit_from_delegate: Inherit credentials from the delegate.
        :param pulumi.Input[pulumi.InputType['AwsConnectorIrsaArgs']] irsa: Use IAM role for service accounts.
        :param pulumi.Input[pulumi.InputType['AwsConnectorManualArgs']] manual: Use IAM role for service accounts.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AwsConnectorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for creating an AWS connector.

        :param str resource_name: The name of the resource.
        :param AwsConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AwsConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cross_account_access: Optional[pulumi.Input[pulumi.InputType['AwsConnectorCrossAccountAccessArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 inherit_from_delegate: Optional[pulumi.Input[pulumi.InputType['AwsConnectorInheritFromDelegateArgs']]] = None,
                 irsa: Optional[pulumi.Input[pulumi.InputType['AwsConnectorIrsaArgs']]] = None,
                 manual: Optional[pulumi.Input[pulumi.InputType['AwsConnectorManualArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AwsConnectorArgs.__new__(AwsConnectorArgs)

            __props__.__dict__["cross_account_access"] = cross_account_access
            __props__.__dict__["description"] = description
            if identifier is None and not opts.urn:
                raise TypeError("Missing required property 'identifier'")
            __props__.__dict__["identifier"] = identifier
            __props__.__dict__["inherit_from_delegate"] = inherit_from_delegate
            __props__.__dict__["irsa"] = irsa
            __props__.__dict__["manual"] = manual
            __props__.__dict__["name"] = name
            __props__.__dict__["org_id"] = org_id
            __props__.__dict__["project_id"] = project_id
            __props__.__dict__["tags"] = tags
        super(AwsConnector, __self__).__init__(
            'harness:platform/awsConnector:AwsConnector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cross_account_access: Optional[pulumi.Input[pulumi.InputType['AwsConnectorCrossAccountAccessArgs']]] = None,
            description: Optional[pulumi.Input[str]] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            inherit_from_delegate: Optional[pulumi.Input[pulumi.InputType['AwsConnectorInheritFromDelegateArgs']]] = None,
            irsa: Optional[pulumi.Input[pulumi.InputType['AwsConnectorIrsaArgs']]] = None,
            manual: Optional[pulumi.Input[pulumi.InputType['AwsConnectorManualArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'AwsConnector':
        """
        Get an existing AwsConnector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AwsConnectorCrossAccountAccessArgs']] cross_account_access: Select this option if you want to use one AWS account for the connection, but you want to deploy or build in a different AWS account. In this scenario, the AWS account used for AWS access in Credentials will assume the IAM role you specify in Cross-account role ARN setting. This option uses the AWS Security Token Service (STS) feature.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[pulumi.InputType['AwsConnectorInheritFromDelegateArgs']] inherit_from_delegate: Inherit credentials from the delegate.
        :param pulumi.Input[pulumi.InputType['AwsConnectorIrsaArgs']] irsa: Use IAM role for service accounts.
        :param pulumi.Input[pulumi.InputType['AwsConnectorManualArgs']] manual: Use IAM role for service accounts.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AwsConnectorState.__new__(_AwsConnectorState)

        __props__.__dict__["cross_account_access"] = cross_account_access
        __props__.__dict__["description"] = description
        __props__.__dict__["identifier"] = identifier
        __props__.__dict__["inherit_from_delegate"] = inherit_from_delegate
        __props__.__dict__["irsa"] = irsa
        __props__.__dict__["manual"] = manual
        __props__.__dict__["name"] = name
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["tags"] = tags
        return AwsConnector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="crossAccountAccess")
    def cross_account_access(self) -> pulumi.Output[Optional['outputs.AwsConnectorCrossAccountAccess']]:
        """
        Select this option if you want to use one AWS account for the connection, but you want to deploy or build in a different AWS account. In this scenario, the AWS account used for AWS access in Credentials will assume the IAM role you specify in Cross-account role ARN setting. This option uses the AWS Security Token Service (STS) feature.
        """
        return pulumi.get(self, "cross_account_access")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output[str]:
        """
        Unique identifier of the resource.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter(name="inheritFromDelegate")
    def inherit_from_delegate(self) -> pulumi.Output[Optional['outputs.AwsConnectorInheritFromDelegate']]:
        """
        Inherit credentials from the delegate.
        """
        return pulumi.get(self, "inherit_from_delegate")

    @property
    @pulumi.getter
    def irsa(self) -> pulumi.Output[Optional['outputs.AwsConnectorIrsa']]:
        """
        Use IAM role for service accounts.
        """
        return pulumi.get(self, "irsa")

    @property
    @pulumi.getter
    def manual(self) -> pulumi.Output[Optional['outputs.AwsConnectorManual']]:
        """
        Use IAM role for service accounts.
        """
        return pulumi.get(self, "manual")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[Optional[str]]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[Optional[str]]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Tags to associate with the resource. Tags should be in the form `name:value`.
        """
        return pulumi.get(self, "tags")

