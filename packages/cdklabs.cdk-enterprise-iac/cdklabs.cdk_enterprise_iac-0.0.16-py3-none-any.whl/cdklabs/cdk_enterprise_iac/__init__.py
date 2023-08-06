'''
<!--
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
-->

# CDK Enterprise IaC

Utilites for using CDK within enterprise constraints

## Install

Typescript

```zsh
npm install @cdklabs/cdk-enterprise-iac
```

Python

```zsh
pip install cdklabs.cdk-enterprise-iac
```

## Usage

Example for `AddPermissionBoundary` in Typescript project.

```python
import * as cdk from 'aws-cdk-lib';
import { MyStack } from '../lib/my-project-stack';
import { Aspects } from 'aws-cdk-lib';
import { AddPermissionBoundary } from '@cdklabs/cdk-enterprise-iac';

const app = new cdk.App();
new MyStack(app, 'MyStack');

Aspects.of(app).add(
  new AddPermissionBoundary({
    permissionsBoundaryPolicyName: 'MyPermissionBoundaryName',
    instanceProfilePrefix: 'MY_PREFIX_', // optional, Defaults to ''
    policyPrefix: 'MY_POLICY_PREFIX_', // optional, Defaults to ''
    rolePrefix: 'MY_ROLE_PREFIX_', // optional, Defaults to ''
  })
);
```

Example for `AddPermissionBoundary` in Python project.

```python
import aws_cdk as cdk
from cdklabs.cdk_enterprise_iac import AddPermissionBoundary
from test_py.test_py_stack import TestPyStack


app = cdk.App()
TestPyStack(app, "TestPyStack")

cdk.Aspects.of(app).add(AddPermissionBoundary(
    permissions_boundary_policy_name="MyPermissionBoundaryName",
    instance_profile_prefix="MY_PREFIX_",  # optional, Defaults to ""
    policy_prefix="MY_POLICY_PREFIX_",  # optional, Defaults to ""
    role_prefix="MY_ROLE_PREFIX_"  # optional, Defaults to ""
))

app.synth()
```

Details in [API.md](API.md)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk
import aws_cdk.aws_apigateway
import constructs


@jsii.implements(aws_cdk.IAspect)
class AddLambdaEnvironmentVariables(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.AddLambdaEnvironmentVariables",
):
    '''Add one or more environment variables to *all* lambda functions within a scope.

    :extends: IAspect
    '''

    def __init__(self, props: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''
        :param props: : string} props - Key Value pair(s) for environment variables to add to all lambda functions.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AddLambdaEnvironmentVariables.__init__)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AddLambdaEnvironmentVariables.visit)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.implements(aws_cdk.IAspect)
class AddPermissionBoundary(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary",
):
    '''A patch for Adding Permissions Boundaries to all IAM roles.

    Additional options for adding prefixes to IAM role, policy and instance profile names

    Can account for non commercial partitions (e.g. aws-gov, aws-cn)
    '''

    def __init__(
        self,
        *,
        permissions_boundary_policy_name: builtins.str,
        instance_profile_prefix: typing.Optional[builtins.str] = None,
        policy_prefix: typing.Optional[builtins.str] = None,
        role_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param permissions_boundary_policy_name: Name of Permissions Boundary Policy to add to all IAM roles.
        :param instance_profile_prefix: A prefix to prepend to the name of the IAM InstanceProfiles (Default: '').
        :param policy_prefix: A prefix to prepend to the name of the IAM Policies and ManagedPolicies (Default: '').
        :param role_prefix: A prefix to prepend to the name of IAM Roles (Default: '').
        '''
        props = AddPermissionBoundaryProps(
            permissions_boundary_policy_name=permissions_boundary_policy_name,
            instance_profile_prefix=instance_profile_prefix,
            policy_prefix=policy_prefix,
            role_prefix=role_prefix,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="checkAndOverride")
    def check_and_override(
        self,
        node: aws_cdk.CfnResource,
        prefix: builtins.str,
        length: jsii.Number,
        cfn_prop: builtins.str,
        cdk_prop: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param node: -
        :param prefix: -
        :param length: -
        :param cfn_prop: -
        :param cdk_prop: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AddPermissionBoundary.check_and_override)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument length", value=length, expected_type=type_hints["length"])
            check_type(argname="argument cfn_prop", value=cfn_prop, expected_type=type_hints["cfn_prop"])
            check_type(argname="argument cdk_prop", value=cdk_prop, expected_type=type_hints["cdk_prop"])
        return typing.cast(None, jsii.invoke(self, "checkAndOverride", [node, prefix, length, cfn_prop, cdk_prop]))

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AddPermissionBoundary.visit)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "permissions_boundary_policy_name": "permissionsBoundaryPolicyName",
        "instance_profile_prefix": "instanceProfilePrefix",
        "policy_prefix": "policyPrefix",
        "role_prefix": "rolePrefix",
    },
)
class AddPermissionBoundaryProps:
    def __init__(
        self,
        *,
        permissions_boundary_policy_name: builtins.str,
        instance_profile_prefix: typing.Optional[builtins.str] = None,
        policy_prefix: typing.Optional[builtins.str] = None,
        role_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties to pass to the AddPermissionBoundary.

        :param permissions_boundary_policy_name: Name of Permissions Boundary Policy to add to all IAM roles.
        :param instance_profile_prefix: A prefix to prepend to the name of the IAM InstanceProfiles (Default: '').
        :param policy_prefix: A prefix to prepend to the name of the IAM Policies and ManagedPolicies (Default: '').
        :param role_prefix: A prefix to prepend to the name of IAM Roles (Default: '').

        :interface: AddPermissionBoundaryProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AddPermissionBoundaryProps.__init__)
            check_type(argname="argument permissions_boundary_policy_name", value=permissions_boundary_policy_name, expected_type=type_hints["permissions_boundary_policy_name"])
            check_type(argname="argument instance_profile_prefix", value=instance_profile_prefix, expected_type=type_hints["instance_profile_prefix"])
            check_type(argname="argument policy_prefix", value=policy_prefix, expected_type=type_hints["policy_prefix"])
            check_type(argname="argument role_prefix", value=role_prefix, expected_type=type_hints["role_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "permissions_boundary_policy_name": permissions_boundary_policy_name,
        }
        if instance_profile_prefix is not None:
            self._values["instance_profile_prefix"] = instance_profile_prefix
        if policy_prefix is not None:
            self._values["policy_prefix"] = policy_prefix
        if role_prefix is not None:
            self._values["role_prefix"] = role_prefix

    @builtins.property
    def permissions_boundary_policy_name(self) -> builtins.str:
        '''Name of Permissions Boundary Policy to add to all IAM roles.'''
        result = self._values.get("permissions_boundary_policy_name")
        assert result is not None, "Required property 'permissions_boundary_policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_profile_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix to prepend to the name of the IAM InstanceProfiles (Default: '').'''
        result = self._values.get("instance_profile_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix to prepend to the name of the IAM Policies and ManagedPolicies (Default: '').'''
        result = self._values.get("policy_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix to prepend to the name of IAM Roles (Default: '').'''
        result = self._values.get("role_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddPermissionBoundaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.IAspect)
class RemovePublicAccessBlockConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.RemovePublicAccessBlockConfiguration",
):
    '''Looks for S3 Buckets, and removes the ``PublicAccessBlockConfiguration`` property.

    For use in regions where Cloudformation doesn't support this property
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemovePublicAccessBlockConfiguration.visit)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.implements(aws_cdk.IAspect)
class RemoveTags(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.RemoveTags",
):
    '''Patch for removing tags from a specific Cloudformation Resource.

    In some regions, the 'Tags' property isn't supported in Cloudformation. This patch makes it easy to remove

    Example::

        // Remove tags on a resource
        Aspects.of(stack).add(new RemoveTags({
          cloudformationResource: 'AWS::ECS::Cluster',
        }));
        // Remove tags without the standard 'Tags' name
        Aspects.of(stack).add(new RemoveTags({
          cloudformationResource: 'AWS::Backup::BackupPlan',
           tagPropertyName: 'BackupPlanTags',
        }));
    '''

    def __init__(
        self,
        *,
        cloudformation_resource: builtins.str,
        tag_property_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloudformation_resource: Name of Cloudformation resource Type (e.g. 'AWS::Lambda::Function').
        :param tag_property_name: Name of the tag property to remove from the resource. Default: Tags
        '''
        props = RemoveTagsProps(
            cloudformation_resource=cloudformation_resource,
            tag_property_name=tag_property_name,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoveTags.visit)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.RemoveTagsProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloudformation_resource": "cloudformationResource",
        "tag_property_name": "tagPropertyName",
    },
)
class RemoveTagsProps:
    def __init__(
        self,
        *,
        cloudformation_resource: builtins.str,
        tag_property_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloudformation_resource: Name of Cloudformation resource Type (e.g. 'AWS::Lambda::Function').
        :param tag_property_name: Name of the tag property to remove from the resource. Default: Tags
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoveTagsProps.__init__)
            check_type(argname="argument cloudformation_resource", value=cloudformation_resource, expected_type=type_hints["cloudformation_resource"])
            check_type(argname="argument tag_property_name", value=tag_property_name, expected_type=type_hints["tag_property_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "cloudformation_resource": cloudformation_resource,
        }
        if tag_property_name is not None:
            self._values["tag_property_name"] = tag_property_name

    @builtins.property
    def cloudformation_resource(self) -> builtins.str:
        '''Name of Cloudformation resource Type (e.g. 'AWS::Lambda::Function').'''
        result = self._values.get("cloudformation_resource")
        assert result is not None, "Required property 'cloudformation_resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_property_name(self) -> typing.Optional[builtins.str]:
        '''Name of the tag property to remove from the resource.

        :default: Tags
        '''
        result = self._values.get("tag_property_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoveTagsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.IAspect)
class SetApiGatewayEndpointConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfiguration",
):
    '''Override RestApis to use a set endpoint configuration.

    Some regions don't support EDGE endpoints, and some enterprises require
    specific endpoint types for RestApis
    '''

    def __init__(
        self,
        *,
        endpoint_type: typing.Optional[aws_cdk.aws_apigateway.EndpointType] = None,
    ) -> None:
        '''
        :param endpoint_type: API Gateway endpoint type to override to. Defaults to EndpointType.REGIONAL Default: EndpointType.REGIONAL
        '''
        props = SetApiGatewayEndpointConfigurationProps(endpoint_type=endpoint_type)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SetApiGatewayEndpointConfiguration.visit)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"endpoint_type": "endpointType"},
)
class SetApiGatewayEndpointConfigurationProps:
    def __init__(
        self,
        *,
        endpoint_type: typing.Optional[aws_cdk.aws_apigateway.EndpointType] = None,
    ) -> None:
        '''
        :param endpoint_type: API Gateway endpoint type to override to. Defaults to EndpointType.REGIONAL Default: EndpointType.REGIONAL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SetApiGatewayEndpointConfigurationProps.__init__)
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
        self._values: typing.Dict[str, typing.Any] = {}
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type

    @builtins.property
    def endpoint_type(self) -> typing.Optional[aws_cdk.aws_apigateway.EndpointType]:
        '''API Gateway endpoint type to override to.

        Defaults to EndpointType.REGIONAL

        :default: EndpointType.REGIONAL
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[aws_cdk.aws_apigateway.EndpointType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetApiGatewayEndpointConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddLambdaEnvironmentVariables",
    "AddPermissionBoundary",
    "AddPermissionBoundaryProps",
    "RemovePublicAccessBlockConfiguration",
    "RemoveTags",
    "RemoveTagsProps",
    "SetApiGatewayEndpointConfiguration",
    "SetApiGatewayEndpointConfigurationProps",
]

publication.publish()
