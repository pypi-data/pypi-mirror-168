'''
[![npm version](https://badge.fury.io/js/cdk-remote-stack.svg)](https://badge.fury.io/js/cdk-remote-stack)
[![PyPI version](https://badge.fury.io/py/cdk-remote-stack.svg)](https://badge.fury.io/py/cdk-remote-stack)
[![release](https://github.com/pahud/cdk-remote-stack/actions/workflows/release.yml/badge.svg)](https://github.com/pahud/cdk-remote-stack/actions/workflows/release.yml)

# cdk-remote-stack

Get outputs and AWS SSM parameters from cross-region AWS CloudFormation stacks

# Install

Use the npm dist tag to opt in CDKv1 or CDKv2:

```sh
// for CDKv2
npm install cdk-remote-stack
or
npm install cdk-remote-stack@latest

// for CDKv1
npm install cdk-remote-stack@cdkv1
```

# Why

Setting up cross-regional cross-stack references requires using multiple constructs from the AWS CDK construct library and is not straightforward.

`cdk-remote-stack` aims to simplify the cross-regional cross-stack references to help you easily build cross-regional multi-stack AWS CDK applications.

This construct library provides two main constructs:

* **RemoteOutputs** - cross regional stack outputs reference.
* **RemoteParameters** - cross regional/account SSM parameters reference.

# RemoteOutputs

`RemoteOutputs` is ideal for one stack referencing the outputs from another across different AWS regions.

Let's say we have two cross-regional stacks in the same AWS CDK application:

1. **stackJP** - stack in Japan (`JP`) to create a SNS topic
2. **stackUS** - stack in United States (`US`) to get the outputs from `stackJP` and print out the SNS `TopicName` from `stackJP` outputs.

```python
import { RemoteOutputs } from 'cdk-remote-stack';
import * as cdk from 'aws-cdk-lib';

const app = new cdk.App();

const envJP = {
  region: 'ap-northeast-1',
  account: process.env.CDK_DEFAULT_ACCOUNT,
};

const envUS = {
  region: 'us-west-2',
  account: process.env.CDK_DEFAULT_ACCOUNT,
};

// first stack in JP
const stackJP = new cdk.Stack(app, 'demo-stack-jp', { env: envJP })

new cdk.CfnOutput(stackJP, 'TopicName', { value: 'foo' })

// second stack in US
const stackUS = new cdk.Stack(app, 'demo-stack-us', { env: envUS })

// ensure the dependency
stackUS.addDependency(stackJP)

// get the stackJP stack outputs from stackUS
const outputs = new RemoteOutputs(stackUS, 'Outputs', { stack: stackJP })

const remoteOutputValue = outputs.get('TopicName')

// the value should be exactly the same with the output value of `TopicName`
new cdk.CfnOutput(stackUS, 'RemoteTopicName', { value: remoteOutputValue })
```

At this moment, `RemoteOutputs` only supports cross-regional reference in a single AWS account.

## Always get the latest stack output

By default, the `RemoteOutputs` construct will always try to get the latest output from the source stack. You may opt out by setting `alwaysUpdate` to `false` to turn this feature off.

For example:

```python
const outputs = new RemoteOutputs(stackUS, 'Outputs', {
  stack: stackJP,
  alwaysUpdate: false,
})
```

# RemoteParameters

[AWS Systems Manager (AWS SSM) Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) is great to store and persist parameters and allow stacks from other regons/accounts to reference. Let's dive into the two major scenarios below:

## Stacks from single account and different regions

In this sample, we create two stacks from JP (`ap-northeast-1`) and US (`us-west-2`). The JP stack will produce and update parameters in its parameter store, while the US stack will consume the parameters across differnt regions with the `RemoteParameters` construct.

![](images/remote-param-1.svg)

```python
    const envJP = { region: 'ap-northeast-1', account: '111111111111' };
    const envUS = { region: 'us-west-2', account: '111111111111' };

    // first stack in JP
    const producerStackName = 'demo-stack-jp';
    const stackJP = new cdk.Stack(app, producerStackName, { env: envJP });
    const parameterPath = `/${envJP.account}/${envJP.region}/${producerStackName}`

    new ssm.StringParameter(stackJP, 'foo1', {
      parameterName: `${parameterPath}/foo1`,
      stringValue: 'bar1',
    });
    new ssm.StringParameter(stackJP, 'foo2', {
      parameterName: `${parameterPath}/foo2`,
      stringValue: 'bar2',
    });
    new ssm.StringParameter(stackJP, 'foo3', {
      parameterName: `${parameterPath}/foo3`,
      stringValue: 'bar3',
    });

    // second stack in US
    const stackUS = new cdk.Stack(app, 'demo-stack-us', { env: envUS });

    // ensure the dependency
    stackUS.addDependency(stackJP);

    // get remote parameters by path from AWS SSM parameter store
    const parameters = new RemoteParameters(stackUS, 'Parameters', {
      path: parameterPath,
      region: stackJP.region,
    })

    const foo1 = parameters.get(`${parameterPath}/foo1`);
    const foo2 = parameters.get(`${parameterPath}/foo2`);
    const foo3 = parameters.get(`${parameterPath}/foo3`);

    new cdk.CfnOutput(stackUS, 'foo1Output', { value: foo1 });
    new cdk.CfnOutput(stackUS, 'foo2Output', { value: foo2 });
    new cdk.CfnOutput(stackUS, 'foo3Output', { value: foo3 });
```

## Stacks from differnt accounts and different regions

Similar to the use case above, but now we deploy stacks in separate accounts and regions.  We will need to pass an AWS Identity and Access Management (AWS IAM) `role` to the `RemoteParameters` construct to get all the parameters from the remote environment.

![](images/remote-param-2.svg)

```python

    const envJP = { region: 'ap-northeast-1', account: '111111111111' };
    const envUS = { region: 'us-west-2', account: '222222222222' };

    // first stack in JP
    const producerStackName = 'demo-stack-jp';
    const stackJP = new cdk.Stack(app, producerStackName, { env: envJP });
    const parameterPath = `/${envJP.account}/${envJP.region}/${producerStackName}`

    new ssm.StringParameter(stackJP, 'foo1', {
      parameterName: `${parameterPath}/foo1`,
      stringValue: 'bar1',
    });
    new ssm.StringParameter(stackJP, 'foo2', {
      parameterName: `${parameterPath}/foo2`,
      stringValue: 'bar2',
    });
    new ssm.StringParameter(stackJP, 'foo3', {
      parameterName: `${parameterPath}/foo3`,
      stringValue: 'bar3',
    });

    // allow US account to assume this read only role to get parameters
    const cdkReadOnlyRole = new iam.Role(stackJP, 'readOnlyRole', {
      assumedBy: new iam.AccountPrincipal(envUS.account),
      roleName: PhysicalName.GENERATE_IF_NEEDED,
      managedPolicies: [ iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMReadOnlyAccess')],
    })

    // second stack in US
    const stackUS = new cdk.Stack(app, 'demo-stack-us', { env: envUS });

    // ensure the dependency
    stackUS.addDependency(stackJP);

    // get remote parameters by path from AWS SSM parameter store
    const parameters = new RemoteParameters(stackUS, 'Parameters', {
      path: parameterPath,
      region: stackJP.region,
      // assume this role for cross-account parameters
      role: iam.Role.fromRoleArn(stackUS, 'readOnlyRole', cdkReadOnlyRole.roleArn),
    })

    const foo1 = parameters.get(`${parameterPath}/foo1`);
    const foo2 = parameters.get(`${parameterPath}/foo2`);
    const foo3 = parameters.get(`${parameterPath}/foo3`);

    new cdk.CfnOutput(stackUS, 'foo1Output', { value: foo1 });
    new cdk.CfnOutput(stackUS, 'foo2Output', { value: foo2 });
    new cdk.CfnOutput(stackUS, 'foo3Output', { value: foo3 });
```

## Dedicated account for a centralized parameter store

The parameters are stored in a centralized account/region and previously provisioned as a source-of-truth configuration store. All other stacks from different accounts/regions are consuming the parameters from the central configuration store.

This scenario is pretty much like #2. The difference is that there's a dedicated account for centralized configuration store being shared with all other accounts.

![](images/remote-param-3.svg)

You will need create `RemoteParameters` for all the consuming stacks like:

```python
// for StackUS
new RemoteParameters(stackUS, 'Parameters', {
  path: parameterPath,
  region: 'eu-central-1'
  // assume this role for cross-account parameters
  role: iam.Role.fromRoleArn(stackUS, 'readOnlyRole', sharedReadOnlyRoleArn),
})

// for StackJP
new RemoteParameters(stackJP, 'Parameters', {
  path: parameterPath,
  region: 'eu-central-1'
  // assume this role for cross-account parameters
  role: iam.Role.fromRoleArn(stackJP, 'readOnlyRole', sharedReadOnlyRoleArn),
})
```

## Tools for multi-account deployment

You will need to install and bootstrap your target accounts with AWS CDK 1.108.0 or later, so you can deploy stacks from different accounts. It [adds support](https://github.com/aws/aws-cdk/pull/14874) for cross-account lookups. Alternatively, install [cdk-assume-role-credential-plugin](https://github.com/aws-samples/cdk-assume-role-credential-plugin). Read this [blog post](https://aws.amazon.com/tw/blogs/devops/cdk-credential-plugin/) to setup this plugin.

## Limitations

1. At this moment, the `RemoteParameters` construct only supports the `String` data type from parameter store.
2. Maximum number of parameters is `100`. Will make it configurable in the future if required.

# Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more information.

# License

This code is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file.
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
import aws_cdk.aws_iam
import constructs


class RemoteOutputs(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-remote-stack.RemoteOutputs",
):
    '''Represents the RemoteOutputs of the remote CDK stack.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        stack: aws_cdk.Stack,
        always_update: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stack: The remote CDK stack to get the outputs from.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteOutputs.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RemoteOutputsProps(stack=stack, always_update=always_update)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="get")
    def get(self, key: builtins.str) -> builtins.str:
        '''Get the attribute value from the outputs.

        :param key: output key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteOutputs.get)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(builtins.str, jsii.invoke(self, "get", [key]))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> aws_cdk.CustomResource:
        '''The outputs from the remote stack.'''
        return typing.cast(aws_cdk.CustomResource, jsii.get(self, "outputs"))


@jsii.data_type(
    jsii_type="cdk-remote-stack.RemoteOutputsProps",
    jsii_struct_bases=[],
    name_mapping={"stack": "stack", "always_update": "alwaysUpdate"},
)
class RemoteOutputsProps:
    def __init__(
        self,
        *,
        stack: aws_cdk.Stack,
        always_update: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties of the RemoteOutputs.

        :param stack: The remote CDK stack to get the outputs from.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteOutputsProps.__init__)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument always_update", value=always_update, expected_type=type_hints["always_update"])
        self._values: typing.Dict[str, typing.Any] = {
            "stack": stack,
        }
        if always_update is not None:
            self._values["always_update"] = always_update

    @builtins.property
    def stack(self) -> aws_cdk.Stack:
        '''The remote CDK stack to get the outputs from.'''
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(aws_cdk.Stack, result)

    @builtins.property
    def always_update(self) -> typing.Optional[builtins.bool]:
        '''Indicate whether always update the custom resource to get the new stack output.

        :default: true
        '''
        result = self._values.get("always_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteOutputsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RemoteParameters(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-remote-stack.RemoteParameters",
):
    '''Represents the RemoteParameters of the remote CDK stack.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        path: builtins.str,
        region: builtins.str,
        always_update: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param path: The parameter path.
        :param region: The region code of the remote stack.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        :param role: The assumed role used to get remote parameters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteParameters.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RemoteParametersProps(
            path=path, region=region, always_update=always_update, role=role
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="get")
    def get(self, key: builtins.str) -> builtins.str:
        '''Get the parameter.

        :param key: output key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteParameters.get)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(builtins.str, jsii.invoke(self, "get", [key]))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> aws_cdk.CustomResource:
        '''The parameters in the SSM parameter store for the remote stack.'''
        return typing.cast(aws_cdk.CustomResource, jsii.get(self, "parameters"))


@jsii.data_type(
    jsii_type="cdk-remote-stack.RemoteParametersProps",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "region": "region",
        "always_update": "alwaysUpdate",
        "role": "role",
    },
)
class RemoteParametersProps:
    def __init__(
        self,
        *,
        path: builtins.str,
        region: builtins.str,
        always_update: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        '''Properties of the RemoteParameters.

        :param path: The parameter path.
        :param region: The region code of the remote stack.
        :param always_update: Indicate whether always update the custom resource to get the new stack output. Default: true
        :param role: The assumed role used to get remote parameters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(RemoteParametersProps.__init__)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument always_update", value=always_update, expected_type=type_hints["always_update"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[str, typing.Any] = {
            "path": path,
            "region": region,
        }
        if always_update is not None:
            self._values["always_update"] = always_update
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def path(self) -> builtins.str:
        '''The parameter path.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''The region code of the remote stack.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_update(self) -> typing.Optional[builtins.bool]:
        '''Indicate whether always update the custom resource to get the new stack output.

        :default: true
        '''
        result = self._values.get("always_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''The assumed role used to get remote parameters.'''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteParametersProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "RemoteOutputs",
    "RemoteOutputsProps",
    "RemoteParameters",
    "RemoteParametersProps",
]

publication.publish()
