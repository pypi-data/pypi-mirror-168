'''
# AWS CDK Construct for Simple Email Service (SES) SMTP Credentials

[![build](https://github.com/RenovoSolutions/cdk-library-aws-ses-smtp-credentials/actions/workflows/build.yml/badge.svg)](https://github.com/RenovoSolutions/cdk-library-aws-ses-smtp-credentials/actions/workflows/build.yml)

This construct creates SES SMTP Credentials

## Overview

* Creates an IAM user with a policy to send SES emails
* Uses a custom resource to generate then convert AWS credentials to SES SMTP Credentials
* Uploads the resulting SMTP credentials to AWS Secrets Manager

## Usage examples

See [API](API.md) doc for full details

**typescript example:**

```python
new SesSmtpCredentials(stack, 'SesSmtpCredentials', {
  iamUserName: 'exampleUser',
});
```

## Testing the generated credentials in the CLI

See [this document from AWS](https://docs.aws.amazon.com/ses/latest/dg/send-email-smtp-client-command-line.html#send-email-using-openssl) for full details
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

import aws_cdk.aws_iam
import aws_cdk.aws_secretsmanager
import constructs


class SesSmtpCredentials(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-aws-ses-smtp-credentials.SesSmtpCredentials",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        iam_user_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param iam_user_name: The name of the IAM user to create.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SesSmtpCredentials.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SesSmtpCredentialsProps(iam_user_name=iam_user_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="iamUser")
    def iam_user(self) -> aws_cdk.aws_iam.User:
        '''The IAM user to which the SMTP credentials are attached.'''
        return typing.cast(aws_cdk.aws_iam.User, jsii.get(self, "iamUser"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''The AWS secrets manager secret that contains the SMTP credentials.'''
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, jsii.get(self, "secret"))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-ses-smtp-credentials.SesSmtpCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"iam_user_name": "iamUserName"},
)
class SesSmtpCredentialsProps:
    def __init__(self, *, iam_user_name: builtins.str) -> None:
        '''The properties of a new set of SMTP Credentials.

        :param iam_user_name: The name of the IAM user to create.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SesSmtpCredentialsProps.__init__)
            check_type(argname="argument iam_user_name", value=iam_user_name, expected_type=type_hints["iam_user_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "iam_user_name": iam_user_name,
        }

    @builtins.property
    def iam_user_name(self) -> builtins.str:
        '''The name of the IAM user to create.'''
        result = self._values.get("iam_user_name")
        assert result is not None, "Required property 'iam_user_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SesSmtpCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SesSmtpCredentials",
    "SesSmtpCredentialsProps",
]

publication.publish()
