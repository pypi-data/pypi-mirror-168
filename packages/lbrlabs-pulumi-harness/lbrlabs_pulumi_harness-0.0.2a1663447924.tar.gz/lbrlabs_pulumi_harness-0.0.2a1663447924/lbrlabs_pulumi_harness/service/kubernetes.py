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

__all__ = ['KubernetesArgs', 'Kubernetes']

@pulumi.input_type
class KubernetesArgs:
    def __init__(__self__, *,
                 app_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 helm_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 variables: Optional[pulumi.Input[Sequence[pulumi.Input['KubernetesVariableArgs']]]] = None):
        """
        The set of arguments for constructing a Kubernetes resource.
        :param pulumi.Input[str] app_id: The id of the application the service belongs to
        :param pulumi.Input[str] description: Description of th service
        :param pulumi.Input[str] helm_version: The version of Helm to use. Options are `V2` and `V3`. Defaults to 'V2'. Only used when `type` is `KUBERNETES` or `HELM`.
        :param pulumi.Input[str] name: Name of the service
        :param pulumi.Input[Sequence[pulumi.Input['KubernetesVariableArgs']]] variables: Variables to be used in the service
        """
        pulumi.set(__self__, "app_id", app_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if helm_version is not None:
            pulumi.set(__self__, "helm_version", helm_version)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if variables is not None:
            pulumi.set(__self__, "variables", variables)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Input[str]:
        """
        The id of the application the service belongs to
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of th service
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="helmVersion")
    def helm_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of Helm to use. Options are `V2` and `V3`. Defaults to 'V2'. Only used when `type` is `KUBERNETES` or `HELM`.
        """
        return pulumi.get(self, "helm_version")

    @helm_version.setter
    def helm_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "helm_version", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the service
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def variables(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['KubernetesVariableArgs']]]]:
        """
        Variables to be used in the service
        """
        return pulumi.get(self, "variables")

    @variables.setter
    def variables(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['KubernetesVariableArgs']]]]):
        pulumi.set(self, "variables", value)


@pulumi.input_type
class _KubernetesState:
    def __init__(__self__, *,
                 app_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 helm_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 variables: Optional[pulumi.Input[Sequence[pulumi.Input['KubernetesVariableArgs']]]] = None):
        """
        Input properties used for looking up and filtering Kubernetes resources.
        :param pulumi.Input[str] app_id: The id of the application the service belongs to
        :param pulumi.Input[str] description: Description of th service
        :param pulumi.Input[str] helm_version: The version of Helm to use. Options are `V2` and `V3`. Defaults to 'V2'. Only used when `type` is `KUBERNETES` or `HELM`.
        :param pulumi.Input[str] name: Name of the service
        :param pulumi.Input[Sequence[pulumi.Input['KubernetesVariableArgs']]] variables: Variables to be used in the service
        """
        if app_id is not None:
            pulumi.set(__self__, "app_id", app_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if helm_version is not None:
            pulumi.set(__self__, "helm_version", helm_version)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if variables is not None:
            pulumi.set(__self__, "variables", variables)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the application the service belongs to
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of th service
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="helmVersion")
    def helm_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of Helm to use. Options are `V2` and `V3`. Defaults to 'V2'. Only used when `type` is `KUBERNETES` or `HELM`.
        """
        return pulumi.get(self, "helm_version")

    @helm_version.setter
    def helm_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "helm_version", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the service
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def variables(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['KubernetesVariableArgs']]]]:
        """
        Variables to be used in the service
        """
        return pulumi.get(self, "variables")

    @variables.setter
    def variables(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['KubernetesVariableArgs']]]]):
        pulumi.set(self, "variables", value)


class Kubernetes(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 helm_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 variables: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KubernetesVariableArgs']]]]] = None,
                 __props__=None):
        """
        Resource for creating a Kubernetes service. This resource uses the config-as-code API's. When updating the `name` or `path` of this resource you should typically also set the `create_before_destroy = true` lifecycle setting.

        ## Example Usage

        ```python
        import pulumi
        import lbrlabs_pulumi_harness as harness

        example_application = harness.Application("exampleApplication")
        example_kubernetes = harness.service.Kubernetes("exampleKubernetes",
            app_id=example_application.id,
            helm_version="V3",
            description="Service for deploying Kubernetes manifests",
            variables=[
                harness.service.KubernetesVariableArgs(
                    name="test",
                    value="test_value",
                    type="TEXT",
                ),
                harness.service.KubernetesVariableArgs(
                    name="test2",
                    value="test_value2",
                    type="TEXT",
                ),
            ])
        ```

        ## Import

        # Import using the Harness application id and service id

        ```sh
         $ pulumi import harness:service/kubernetes:Kubernetes example <app_id>/<svc_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_id: The id of the application the service belongs to
        :param pulumi.Input[str] description: Description of th service
        :param pulumi.Input[str] helm_version: The version of Helm to use. Options are `V2` and `V3`. Defaults to 'V2'. Only used when `type` is `KUBERNETES` or `HELM`.
        :param pulumi.Input[str] name: Name of the service
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KubernetesVariableArgs']]]] variables: Variables to be used in the service
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KubernetesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for creating a Kubernetes service. This resource uses the config-as-code API's. When updating the `name` or `path` of this resource you should typically also set the `create_before_destroy = true` lifecycle setting.

        ## Example Usage

        ```python
        import pulumi
        import lbrlabs_pulumi_harness as harness

        example_application = harness.Application("exampleApplication")
        example_kubernetes = harness.service.Kubernetes("exampleKubernetes",
            app_id=example_application.id,
            helm_version="V3",
            description="Service for deploying Kubernetes manifests",
            variables=[
                harness.service.KubernetesVariableArgs(
                    name="test",
                    value="test_value",
                    type="TEXT",
                ),
                harness.service.KubernetesVariableArgs(
                    name="test2",
                    value="test_value2",
                    type="TEXT",
                ),
            ])
        ```

        ## Import

        # Import using the Harness application id and service id

        ```sh
         $ pulumi import harness:service/kubernetes:Kubernetes example <app_id>/<svc_id>
        ```

        :param str resource_name: The name of the resource.
        :param KubernetesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KubernetesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 helm_version: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 variables: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KubernetesVariableArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KubernetesArgs.__new__(KubernetesArgs)

            if app_id is None and not opts.urn:
                raise TypeError("Missing required property 'app_id'")
            __props__.__dict__["app_id"] = app_id
            __props__.__dict__["description"] = description
            __props__.__dict__["helm_version"] = helm_version
            __props__.__dict__["name"] = name
            __props__.__dict__["variables"] = variables
        super(Kubernetes, __self__).__init__(
            'harness:service/kubernetes:Kubernetes',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            app_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            helm_version: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            variables: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KubernetesVariableArgs']]]]] = None) -> 'Kubernetes':
        """
        Get an existing Kubernetes resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_id: The id of the application the service belongs to
        :param pulumi.Input[str] description: Description of th service
        :param pulumi.Input[str] helm_version: The version of Helm to use. Options are `V2` and `V3`. Defaults to 'V2'. Only used when `type` is `KUBERNETES` or `HELM`.
        :param pulumi.Input[str] name: Name of the service
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['KubernetesVariableArgs']]]] variables: Variables to be used in the service
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _KubernetesState.__new__(_KubernetesState)

        __props__.__dict__["app_id"] = app_id
        __props__.__dict__["description"] = description
        __props__.__dict__["helm_version"] = helm_version
        __props__.__dict__["name"] = name
        __props__.__dict__["variables"] = variables
        return Kubernetes(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Output[str]:
        """
        The id of the application the service belongs to
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of th service
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="helmVersion")
    def helm_version(self) -> pulumi.Output[Optional[str]]:
        """
        The version of Helm to use. Options are `V2` and `V3`. Defaults to 'V2'. Only used when `type` is `KUBERNETES` or `HELM`.
        """
        return pulumi.get(self, "helm_version")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the service
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def variables(self) -> pulumi.Output[Optional[Sequence['outputs.KubernetesVariable']]]:
        """
        Variables to be used in the service
        """
        return pulumi.get(self, "variables")

