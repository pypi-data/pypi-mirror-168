'''
# AWS Analytics Reference Architecture

The AWS Analytics Reference Architecture is a set of analytics solutions put together as end-to-end examples.
It regroups AWS best practices for designing, implementing, and operating analytics platforms through different purpose-built patterns, handling common requirements, and solving customers' challenges.

This project is composed of:

* Reusable core components exposed in an AWS CDK (Cloud Development Kit) library currently available in [Typescript](https://www.npmjs.com/package/aws-analytics-reference-architecture) and [Python](https://pypi.org/project/aws-analytics-reference-architecture/). This library contains [AWS CDK constructs](https://constructs.dev/packages/aws-analytics-reference-architecture/?lang=python) that can be used to quickly provision analytics solutions in demos, prototypes, proof of concepts and end-to-end reference architectures.
* Reference architectures consumming the reusable components to demonstrate end-to-end examples in a business context. Currently, the [AWS native reference architecture](https://aws-samples.github.io/aws-analytics-reference-architecture/) is available.

This documentation explains how to get started with the core components of the AWS Analytics Reference Architecture.

## Getting started

* [AWS Analytics Reference Architecture](#aws-analytics-reference-architecture)

  * [Getting started](#getting-started)

    * [Prerequisites](#prerequisites)
    * [Initialization (in Python)](#initialization-in-python)
    * [Development](#development)
    * [Deployment](#deployment)
    * [Cleanup](#cleanup)
  * [API Reference](#api-reference)
  * [Contributing](#contributing)
* [License Summary](#license-summary)

### Prerequisites

1. [Create an AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
2. The core components can be deployed in any AWS region
3. Install the following components with the specified version on the machine from which the deployment will be executed:

   1. Python [3.8-3.9.2] or Typescript
   2. AWS CDK v2: Please refer to the [Getting started](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) guide.
4. Bootstrap AWS CDK in your region (here **eu-west-1**). It will provision resources required to deploy AWS CDK applications

```bash
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export AWS_REGION=eu-west-1
cdk bootstrap aws://$ACCOUNT_ID/eu-west-1
```

### Initialization (in Python)

1. Initialize a new AWS CDK application in Python and use a virtual environment to install dependencies

```bash
mkdir my_demo
cd my_demo
cdk init app --language python
python3 -m venv .env
source .env/bin/activate
```

1. Add the AWS Analytics Reference Architecture library in the dependencies of your project. Update **requirements.txt**

```bash
aws-cdk-lib==2.27.0
constructs>=10.0.0,<11.0.0
aws_analytics_reference_architecture>=2.0.0
```

1. Install The Packages via **pip**

```bash
python -m pip install -r requirements.txt
```

### Development

1. Import the AWS Analytics Reference Architecture in your code in **my_demo/my_demo_stack.py**

```bash
import aws_analytics_reference_architecture as ara
```

1. Now you can use all the constructs available from the core components library to quickly provision resources in your AWS CDK stack. For example:

* The DataLakeStorage to provision a full set of pre-configured Amazon S3 Bucket for a data lake

```bash
        # Create a new DataLakeStorage with Raw, Clean and Transform buckets configured with data lake best practices
        storage = ara.DataLakeStorage (self,"storage")
```

* The DataLakeCatalog to provision a full set of AWS Glue databases for registring tables in your data lake

```bash
        # Create a new DataLakeCatalog with Raw, Clean and Transform databases
        catalog = ara.DataLakeCatalog (self,"catalog")
```

* The DataGenerator to generate live data in the data lake from a pre-configured retail dataset

```bash
        # Generate the Sales Data
        sales_data = ara.BatchReplayer(
            scope=self,
            id="sale-data",
            dataset=ara.PreparedDataset.RETAIL_1_GB_STORE_SALE,
            sink_object_key="sale",
            sink_bucket=storage.raw_bucket,
         )

```

```bash
        # Generate the Customer Data
        customer_data = ara.BatchReplayer(
            scope=self,
            id="customer-data",
            dataset=ara.PreparedDataset.RETAIL_1_GB_CUSTOMER,
            sink_object_key="customer",
            sink_bucket=storage.raw_bucket,
         )

```

* Additionally, the library provides some helpers to quickly run demos:

```bash
        # Configure defaults for Athena console
        athena_defaults = ara.AthenaDemoSetup(scope=self, id="demo_setup")
```

```bash
        # Configure a default role for AWS Glue jobs
        ara.GlueDemoRole.get_or_create(self)
```

### Deployment

Deploy the AWS CDK application

```bash
cdk deploy
```

The time to deploy the application is depending on the constructs you are using

### Cleanup

Delete the AWS CDK application

```bash
cdk destroy
```

## API Reference

More contructs, helpers and datasets are available in the AWS Analytics Reference Architecture. See the full API specification [here](https://constructs.dev/packages/aws-analytics-reference-architecture)

## Contributing

Please refer to the [contributing guidelines](../CONTRIBUTING.md) and [contributing FAQ](../CONTRIB_FAQ.md) for details.

# License Summary

The documentation is made available under the Creative Commons Attribution-ShareAlike 4.0 International License. See the LICENSE file.

The sample code within this documentation is made available under the MIT-0 license. See the LICENSE-SAMPLECODE file.
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
import aws_cdk.aws_athena
import aws_cdk.aws_ec2
import aws_cdk.aws_eks
import aws_cdk.aws_emrcontainers
import aws_cdk.aws_events
import aws_cdk.aws_glue_alpha
import aws_cdk.aws_iam
import aws_cdk.aws_kinesis
import aws_cdk.aws_kinesisfirehose
import aws_cdk.aws_kms
import aws_cdk.aws_logs
import aws_cdk.aws_redshift_alpha
import aws_cdk.aws_s3
import aws_cdk.aws_stepfunctions
import constructs


class AraBucket(
    aws_cdk.aws_s3.Bucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.AraBucket",
):
    '''(experimental) An Amazon S3 Bucket following best practices for the AWS Analytics Reference Architecture.

    The bucket name is mandatory and is used as the CDK id.
    The bucket name is postfixed with the AWS account ID and the AWS region.

    The bucket has the following default properties:

    - the encryption mode is KMS managed by AWS
    - if the encryption mode is KMS customer managed, the encryption key is a default and unique KMS key for ARA
    - the KMS key is used as a bucket key
    - the SSL is enforced
    - the objects are automatically deleted when the bucket is deleted
    - the access are logged in a default and unique S3 bucket for ARA if serverAccessLogsPrefix is provided
    - the access are not logged if serverAccessLogsPrefix is  not provided
    - the public access is blocked and no bucket policy or object permission can grant public access

    All standard S3 Bucket properties can be provided to not use the defaults.
    Usage example::

       import * as cdk from 'aws-cdk-lib';
       import { AraBucket } from 'aws-analytics-reference-architecture';

       const exampleApp = new cdk.App();
       const stack = new cdk.Stack(exampleApp, 'AraBucketStack');

       new AraBucket(stack, {
         bucketName: 'test-bucket',
         serverAccessLogsPrefix: 'test-bucket',
       });

    :stability: experimental
    '''

    @jsii.member(jsii_name="getOrCreate")
    @builtins.classmethod
    def get_or_create(
        cls,
        scope: constructs.Construct,
        *,
        bucket_name: builtins.str,
        access_control: typing.Optional[aws_cdk.aws_s3.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[aws_cdk.aws_s3.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.CorsRule, typing.Dict[str, typing.Any]]]] = None,
        encryption: typing.Optional[aws_cdk.aws_s3.BucketEncryption] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.IntelligentTieringConfiguration, typing.Dict[str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.Inventory, typing.Dict[str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.LifecycleRule, typing.Dict[str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.BucketMetrics, typing.Dict[str, typing.Any]]]] = None,
        notifications_handler_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        object_ownership: typing.Optional[aws_cdk.aws_s3.ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        server_access_logs_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        transfer_acceleration: typing.Optional[builtins.bool] = None,
        versioned: typing.Optional[builtins.bool] = None,
    ) -> aws_cdk.aws_s3.Bucket:
        '''(experimental) Get the Amazon S3 Bucket from the AWS CDK Stack based on the provided name.

        If no bucket exists, it creates a new one based on the provided properties.

        :param scope: -
        :param bucket_name: (experimental) The Amazon S3 bucket name. The bucket name is postfixed with the AWS account ID and the AWS region
        :param access_control: (experimental) Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: (experimental) Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. Default: true
        :param block_public_access: (experimental) The block public access configuration of this bucket. Default: - Block all public access and no ACL or bucket policy can grant public access.
        :param bucket_key_enabled: (experimental) Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Default: true
        :param cors: (experimental) The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: (experimental) The encryption mode for the bucket. Default: - Server side encryption with AWS managed key (SSE-KMS)
        :param encryption_key: (experimental) The KMS key for the bucket encryption. Default: - if encryption is KMS, use a unique KMS key across the stack called ``AraDefaultKmsKey``
        :param enforce_ssl: (experimental) Enforces SSL for requests. Default: true
        :param intelligent_tiering_configurations: (experimental) Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: (experimental) The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: (experimental) Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: (experimental) The metrics configuration of this bucket. Default: - No metrics configuration.
        :param notifications_handler_role: (experimental) The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_ownership: (experimental) The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: (experimental) Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: (experimental) Policy to apply when the bucket is removed from this stack. Default: - destroy the bucket
        :param server_access_logs_bucket: (experimental) Destination bucket for the server access logs. Default: - if serverAccessLogsPrefix is defined, use a unique bucket across the stack called ``s3-access-logs``
        :param server_access_logs_prefix: (experimental) The log file prefix to use for the bucket's access logs. Default: - access are not logged
        :param transfer_acceleration: (experimental) Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: (experimental) Whether this bucket should have versioning turned on or not. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AraBucket.get_or_create)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = AraBucketProps(
            bucket_name=bucket_name,
            access_control=access_control,
            auto_delete_objects=auto_delete_objects,
            block_public_access=block_public_access,
            bucket_key_enabled=bucket_key_enabled,
            cors=cors,
            encryption=encryption,
            encryption_key=encryption_key,
            enforce_ssl=enforce_ssl,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventories=inventories,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
            notifications_handler_role=notifications_handler_role,
            object_ownership=object_ownership,
            public_read_access=public_read_access,
            removal_policy=removal_policy,
            server_access_logs_bucket=server_access_logs_bucket,
            server_access_logs_prefix=server_access_logs_prefix,
            transfer_acceleration=transfer_acceleration,
            versioned=versioned,
        )

        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.sinvoke(cls, "getOrCreate", [scope, props]))


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.AraBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "access_control": "accessControl",
        "auto_delete_objects": "autoDeleteObjects",
        "block_public_access": "blockPublicAccess",
        "bucket_key_enabled": "bucketKeyEnabled",
        "cors": "cors",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "enforce_ssl": "enforceSSL",
        "intelligent_tiering_configurations": "intelligentTieringConfigurations",
        "inventories": "inventories",
        "lifecycle_rules": "lifecycleRules",
        "metrics": "metrics",
        "notifications_handler_role": "notificationsHandlerRole",
        "object_ownership": "objectOwnership",
        "public_read_access": "publicReadAccess",
        "removal_policy": "removalPolicy",
        "server_access_logs_bucket": "serverAccessLogsBucket",
        "server_access_logs_prefix": "serverAccessLogsPrefix",
        "transfer_acceleration": "transferAcceleration",
        "versioned": "versioned",
    },
)
class AraBucketProps:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        access_control: typing.Optional[aws_cdk.aws_s3.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[aws_cdk.aws_s3.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.CorsRule, typing.Dict[str, typing.Any]]]] = None,
        encryption: typing.Optional[aws_cdk.aws_s3.BucketEncryption] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.IntelligentTieringConfiguration, typing.Dict[str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.Inventory, typing.Dict[str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.LifecycleRule, typing.Dict[str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_s3.BucketMetrics, typing.Dict[str, typing.Any]]]] = None,
        notifications_handler_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        object_ownership: typing.Optional[aws_cdk.aws_s3.ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        server_access_logs_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        transfer_acceleration: typing.Optional[builtins.bool] = None,
        versioned: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param bucket_name: (experimental) The Amazon S3 bucket name. The bucket name is postfixed with the AWS account ID and the AWS region
        :param access_control: (experimental) Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: (experimental) Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. Default: true
        :param block_public_access: (experimental) The block public access configuration of this bucket. Default: - Block all public access and no ACL or bucket policy can grant public access.
        :param bucket_key_enabled: (experimental) Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Default: true
        :param cors: (experimental) The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: (experimental) The encryption mode for the bucket. Default: - Server side encryption with AWS managed key (SSE-KMS)
        :param encryption_key: (experimental) The KMS key for the bucket encryption. Default: - if encryption is KMS, use a unique KMS key across the stack called ``AraDefaultKmsKey``
        :param enforce_ssl: (experimental) Enforces SSL for requests. Default: true
        :param intelligent_tiering_configurations: (experimental) Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: (experimental) The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: (experimental) Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: (experimental) The metrics configuration of this bucket. Default: - No metrics configuration.
        :param notifications_handler_role: (experimental) The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_ownership: (experimental) The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: (experimental) Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: (experimental) Policy to apply when the bucket is removed from this stack. Default: - destroy the bucket
        :param server_access_logs_bucket: (experimental) Destination bucket for the server access logs. Default: - if serverAccessLogsPrefix is defined, use a unique bucket across the stack called ``s3-access-logs``
        :param server_access_logs_prefix: (experimental) The log file prefix to use for the bucket's access logs. Default: - access are not logged
        :param transfer_acceleration: (experimental) Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: (experimental) Whether this bucket should have versioning turned on or not. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AraBucketProps.__init__)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument auto_delete_objects", value=auto_delete_objects, expected_type=type_hints["auto_delete_objects"])
            check_type(argname="argument block_public_access", value=block_public_access, expected_type=type_hints["block_public_access"])
            check_type(argname="argument bucket_key_enabled", value=bucket_key_enabled, expected_type=type_hints["bucket_key_enabled"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument enforce_ssl", value=enforce_ssl, expected_type=type_hints["enforce_ssl"])
            check_type(argname="argument intelligent_tiering_configurations", value=intelligent_tiering_configurations, expected_type=type_hints["intelligent_tiering_configurations"])
            check_type(argname="argument inventories", value=inventories, expected_type=type_hints["inventories"])
            check_type(argname="argument lifecycle_rules", value=lifecycle_rules, expected_type=type_hints["lifecycle_rules"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument notifications_handler_role", value=notifications_handler_role, expected_type=type_hints["notifications_handler_role"])
            check_type(argname="argument object_ownership", value=object_ownership, expected_type=type_hints["object_ownership"])
            check_type(argname="argument public_read_access", value=public_read_access, expected_type=type_hints["public_read_access"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument server_access_logs_bucket", value=server_access_logs_bucket, expected_type=type_hints["server_access_logs_bucket"])
            check_type(argname="argument server_access_logs_prefix", value=server_access_logs_prefix, expected_type=type_hints["server_access_logs_prefix"])
            check_type(argname="argument transfer_acceleration", value=transfer_acceleration, expected_type=type_hints["transfer_acceleration"])
            check_type(argname="argument versioned", value=versioned, expected_type=type_hints["versioned"])
        self._values: typing.Dict[str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if access_control is not None:
            self._values["access_control"] = access_control
        if auto_delete_objects is not None:
            self._values["auto_delete_objects"] = auto_delete_objects
        if block_public_access is not None:
            self._values["block_public_access"] = block_public_access
        if bucket_key_enabled is not None:
            self._values["bucket_key_enabled"] = bucket_key_enabled
        if cors is not None:
            self._values["cors"] = cors
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if enforce_ssl is not None:
            self._values["enforce_ssl"] = enforce_ssl
        if intelligent_tiering_configurations is not None:
            self._values["intelligent_tiering_configurations"] = intelligent_tiering_configurations
        if inventories is not None:
            self._values["inventories"] = inventories
        if lifecycle_rules is not None:
            self._values["lifecycle_rules"] = lifecycle_rules
        if metrics is not None:
            self._values["metrics"] = metrics
        if notifications_handler_role is not None:
            self._values["notifications_handler_role"] = notifications_handler_role
        if object_ownership is not None:
            self._values["object_ownership"] = object_ownership
        if public_read_access is not None:
            self._values["public_read_access"] = public_read_access
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if server_access_logs_bucket is not None:
            self._values["server_access_logs_bucket"] = server_access_logs_bucket
        if server_access_logs_prefix is not None:
            self._values["server_access_logs_prefix"] = server_access_logs_prefix
        if transfer_acceleration is not None:
            self._values["transfer_acceleration"] = transfer_acceleration
        if versioned is not None:
            self._values["versioned"] = versioned

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''(experimental) The Amazon S3 bucket name.

        The bucket name is postfixed with the AWS account ID and the AWS region

        :stability: experimental
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_control(self) -> typing.Optional[aws_cdk.aws_s3.BucketAccessControl]:
        '''(experimental) Specifies a canned ACL that grants predefined permissions to the bucket.

        :default: BucketAccessControl.PRIVATE

        :stability: experimental
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketAccessControl], result)

    @builtins.property
    def auto_delete_objects(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted.

        Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_delete_objects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def block_public_access(self) -> typing.Optional[aws_cdk.aws_s3.BlockPublicAccess]:
        '''(experimental) The block public access configuration of this bucket.

        :default: - Block all public access and no ACL or bucket policy can grant public access.

        :stability: experimental
        '''
        result = self._values.get("block_public_access")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BlockPublicAccess], result)

    @builtins.property
    def bucket_key_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("bucket_key_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cors(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.CorsRule]]:
        '''(experimental) The CORS configuration of this bucket.

        :default: - No CORS configuration.

        :stability: experimental
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.CorsRule]], result)

    @builtins.property
    def encryption(self) -> typing.Optional[aws_cdk.aws_s3.BucketEncryption]:
        '''(experimental) The encryption mode for the bucket.

        :default: - Server side encryption with AWS managed key (SSE-KMS)

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''(experimental) The KMS key for the bucket encryption.

        :default: - if encryption is KMS, use a unique KMS key across the stack called ``AraDefaultKmsKey``

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    @builtins.property
    def enforce_ssl(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enforces SSL for requests.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enforce_ssl")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def intelligent_tiering_configurations(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_s3.IntelligentTieringConfiguration]]:
        '''(experimental) Inteligent Tiering Configurations.

        :default: No Intelligent Tiiering Configurations.

        :stability: experimental
        '''
        result = self._values.get("intelligent_tiering_configurations")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.IntelligentTieringConfiguration]], result)

    @builtins.property
    def inventories(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.Inventory]]:
        '''(experimental) The inventory configuration of the bucket.

        :default: - No inventory configuration

        :stability: experimental
        '''
        result = self._values.get("inventories")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.Inventory]], result)

    @builtins.property
    def lifecycle_rules(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_s3.LifecycleRule]]:
        '''(experimental) Rules that define how Amazon S3 manages objects during their lifetime.

        :default: - No lifecycle rules.

        :stability: experimental
        '''
        result = self._values.get("lifecycle_rules")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.LifecycleRule]], result)

    @builtins.property
    def metrics(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.BucketMetrics]]:
        '''(experimental) The metrics configuration of this bucket.

        :default: - No metrics configuration.

        :stability: experimental
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.BucketMetrics]], result)

    @builtins.property
    def notifications_handler_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''(experimental) The role to be used by the notifications handler.

        :default: - a new role will be created.

        :stability: experimental
        '''
        result = self._values.get("notifications_handler_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def object_ownership(self) -> typing.Optional[aws_cdk.aws_s3.ObjectOwnership]:
        '''(experimental) The objectOwnership of the bucket.

        :default: - No ObjectOwnership configuration, uploading account will own the object.

        :stability: experimental
        '''
        result = self._values.get("object_ownership")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.ObjectOwnership], result)

    @builtins.property
    def public_read_access(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Grants public read access to all objects in the bucket.

        Similar to calling ``bucket.grantPublicAccess()``

        :default: false

        :stability: experimental
        '''
        result = self._values.get("public_read_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.RemovalPolicy]:
        '''(experimental) Policy to apply when the bucket is removed from this stack.

        :default: - destroy the bucket

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[aws_cdk.RemovalPolicy], result)

    @builtins.property
    def server_access_logs_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        '''(experimental) Destination bucket for the server access logs.

        :default: - if serverAccessLogsPrefix is defined, use a unique bucket across the stack called ``s3-access-logs``

        :stability: experimental
        '''
        result = self._values.get("server_access_logs_bucket")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.IBucket], result)

    @builtins.property
    def server_access_logs_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The log file prefix to use for the bucket's access logs.

        :default: - access are not logged

        :stability: experimental
        '''
        result = self._values.get("server_access_logs_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transfer_acceleration(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this bucket should have transfer acceleration turned on or not.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("transfer_acceleration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def versioned(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this bucket should have versioning turned on or not.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("versioned")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AraBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaDemoSetup(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.AthenaDemoSetup",
):
    '''(experimental) AthenaDemoSetup Construct to automatically setup a new Amazon Athena Workgroup with proper configuration for out-of-the-box demo.

    :stability: experimental
    '''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''(experimental) Constructs a new instance of the AthenaDefaultSetup class.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.

        :stability: experimental
        :access: public
        '''
        if __debug__:
            type_hints = typing.get_type_hints(AthenaDemoSetup.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="athenaWorkgroup")
    def athena_workgroup(self) -> aws_cdk.aws_athena.CfnWorkGroup:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_athena.CfnWorkGroup, jsii.get(self, "athenaWorkgroup"))

    @builtins.property
    @jsii.member(jsii_name="resultBucket")
    def result_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "resultBucket"))


class BatchReplayer(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.BatchReplayer",
):
    '''(experimental) Replay the data in the given PartitionedDataset.

    It will dump files into the ``sinkBucket`` based on the given ``frequency``.
    The computation is in a Step Function with two Lambda steps.

    1. resources/lambdas/find-file-paths
       Read the manifest file and output a list of S3 file paths within that batch time range
    2. resources/lambdas/write-in-batch
       Take a file path, filter only records within given time range, adjust the the time with offset to
       make it looks like just being generated. Then write the output to the ``sinkBucket``

    Usage example::


       const myBucket = new Bucket(stack, "MyBucket")

       new BatchReplayer(stack, "WebSalesReplayer", {
          dataset: PreparedDataset.RETAIL_1_GB_WEB_SALE,
          s3BucketSink: myBucket
          s3ObjectKeySink: 'some-prefix',
          frequency: 120,
          outputFileMaxSizeInBytes: 10000000,
       });

    :warnning: **If the Bucket is encrypted with KMS, the Key must be managed by this stack.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        dataset: "PreparedDataset",
        sink_bucket: aws_cdk.aws_s3.Bucket,
        frequency: typing.Optional[aws_cdk.Duration] = None,
        output_file_max_size_in_bytes: typing.Optional[jsii.Number] = None,
        sink_object_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the BatchReplayer construct.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param dataset: (experimental) The [PreparedDataset]{@link PreparedDataset} used to replay data.
        :param sink_bucket: (experimental) The S3 Bucket sink where the BatchReplayer writes data. :warnning: **If the Bucket is encrypted with KMS, the Key must be managed by this stack.
        :param frequency: (experimental) The frequency of the replay. Default: - The BatchReplayer is triggered every 60 seconds
        :param output_file_max_size_in_bytes: (experimental) The maximum file size in Bytes written by the BatchReplayer. Default: - The BatchReplayer writes 100MB files maximum
        :param sink_object_key: (experimental) The S3 object key sink where the BatchReplayer writes data. Default: - No object key is used and the BatchReplayer writes the dataset in s3://<BUCKET_NAME>/<TABLE_NAME>

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BatchReplayer.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BatchReplayerProps(
            dataset=dataset,
            sink_bucket=sink_bucket,
            frequency=frequency,
            output_file_max_size_in_bytes=output_file_max_size_in_bytes,
            sink_object_key=sink_object_key,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> "PreparedDataset":
        '''(experimental) Dataset used for replay.

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> jsii.Number:
        '''(experimental) Frequency (in Seconds) of the replaying.

        The batch job will start
        for every given frequency and replay the data in that period

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "frequency"))

    @builtins.property
    @jsii.member(jsii_name="sinkBucket")
    def sink_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''(experimental) Sink bucket where the batch replayer will put data in.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "sinkBucket"))

    @builtins.property
    @jsii.member(jsii_name="outputFileMaxSizeInBytes")
    def output_file_max_size_in_bytes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum file size for each output file.

        If the output batch file is,
        larger than that, it will be splitted into multiple files that fit this size.

        Default to 100MB (max value)

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "outputFileMaxSizeInBytes"))

    @builtins.property
    @jsii.member(jsii_name="sinkObjectKey")
    def sink_object_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) Sink object key where the batch replayer will put data in.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sinkObjectKey"))


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.BatchReplayerProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset": "dataset",
        "sink_bucket": "sinkBucket",
        "frequency": "frequency",
        "output_file_max_size_in_bytes": "outputFileMaxSizeInBytes",
        "sink_object_key": "sinkObjectKey",
    },
)
class BatchReplayerProps:
    def __init__(
        self,
        *,
        dataset: "PreparedDataset",
        sink_bucket: aws_cdk.aws_s3.Bucket,
        frequency: typing.Optional[aws_cdk.Duration] = None,
        output_file_max_size_in_bytes: typing.Optional[jsii.Number] = None,
        sink_object_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The properties for the BatchReplayer construct.

        :param dataset: (experimental) The [PreparedDataset]{@link PreparedDataset} used to replay data.
        :param sink_bucket: (experimental) The S3 Bucket sink where the BatchReplayer writes data. :warnning: **If the Bucket is encrypted with KMS, the Key must be managed by this stack.
        :param frequency: (experimental) The frequency of the replay. Default: - The BatchReplayer is triggered every 60 seconds
        :param output_file_max_size_in_bytes: (experimental) The maximum file size in Bytes written by the BatchReplayer. Default: - The BatchReplayer writes 100MB files maximum
        :param sink_object_key: (experimental) The S3 object key sink where the BatchReplayer writes data. Default: - No object key is used and the BatchReplayer writes the dataset in s3://<BUCKET_NAME>/<TABLE_NAME>

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BatchReplayerProps.__init__)
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument sink_bucket", value=sink_bucket, expected_type=type_hints["sink_bucket"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument output_file_max_size_in_bytes", value=output_file_max_size_in_bytes, expected_type=type_hints["output_file_max_size_in_bytes"])
            check_type(argname="argument sink_object_key", value=sink_object_key, expected_type=type_hints["sink_object_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "dataset": dataset,
            "sink_bucket": sink_bucket,
        }
        if frequency is not None:
            self._values["frequency"] = frequency
        if output_file_max_size_in_bytes is not None:
            self._values["output_file_max_size_in_bytes"] = output_file_max_size_in_bytes
        if sink_object_key is not None:
            self._values["sink_object_key"] = sink_object_key

    @builtins.property
    def dataset(self) -> "PreparedDataset":
        '''(experimental) The [PreparedDataset]{@link PreparedDataset} used to replay data.

        :stability: experimental
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast("PreparedDataset", result)

    @builtins.property
    def sink_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''(experimental) The S3 Bucket sink where the BatchReplayer writes data.

        :warnning: **If the Bucket is encrypted with KMS, the Key must be managed by this stack.

        :stability: experimental
        '''
        result = self._values.get("sink_bucket")
        assert result is not None, "Required property 'sink_bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.Bucket, result)

    @builtins.property
    def frequency(self) -> typing.Optional[aws_cdk.Duration]:
        '''(experimental) The frequency of the replay.

        :default: - The BatchReplayer is triggered every 60 seconds

        :stability: experimental
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def output_file_max_size_in_bytes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum file size in Bytes written by the BatchReplayer.

        :default: - The BatchReplayer writes 100MB files maximum

        :stability: experimental
        '''
        result = self._values.get("output_file_max_size_in_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sink_object_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The S3 object key sink where the BatchReplayer writes data.

        :default: - No object key is used and the BatchReplayer writes the dataset in s3://<BUCKET_NAME>/<TABLE_NAME>

        :stability: experimental
        '''
        result = self._values.get("sink_object_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchReplayerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CentralGovernance(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.CentralGovernance",
):
    '''(experimental) This CDK Construct creates a Data Product registration workflow and resources for the Central Governance account.

    It uses AWS Step Functions state machine to orchestrate the workflow:

    - creates tables in AWS Glue Data Catalog
    - shares tables to Data Product owner account (Producer)

    This construct also creates an Amazon EventBridge Event Bus to enable communication with Data Domain accounts (Producer/Consumer).

    This construct requires to use the default `CDK qualifier <https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html>`_ generated with the standard CDK bootstrap stack.
    It ensures the right CDK execution role is used and granted Lake Formation administrator permissions so CDK can create Glue databases when registring a DataDomain.

    To register a DataDomain, the following information are required:

    - The account Id of the DataDomain
    - The secret ARN for the domain configuration available as a CloudFormation output when creating a {@link DataDomain}

    Usage example::

       import { App, Stack } from 'aws-cdk-lib';
       import { Role } from 'aws-cdk-lib/aws-iam';
       import { CentralGovernance, LfTag } from 'aws-analytics-reference-architecture';

       const exampleApp = new App();
       const stack = new Stack(exampleApp, 'CentralGovStack');

       const tags: LfTag[] = [{key: 'tag1': values:['LfTagValue1', 'LfTagValue2']}]
       const governance = new CentralGovernance(stack, 'myCentralGov', { tags });

       governance.registerDataDomain('Domain1', 'domain1Name', <DOMAIN_CONFIG_SECRET_ARN>);

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        lf_tags: typing.Optional[typing.Sequence[typing.Union["LfTag", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Construct a new instance of CentralGovernance.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param lf_tags: (experimental) LF tags.

        :stability: experimental
        :access: public
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CentralGovernance.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CentralGovernanceProps(lf_tags=lf_tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="registerDataDomain")
    def register_data_domain(
        self,
        id: builtins.str,
        domain_id: builtins.str,
        domain_name: builtins.str,
        domain_secret_arn: builtins.str,
        lf_access_control_mode: typing.Optional["LfAccessControlMode"] = None,
    ) -> None:
        '''(experimental) Registers a new Data Domain account in Central Governance account.

        Each Data Domain account {@link DataDomain} has to be registered in Central Gov. account before it can participate in a mesh.

        It creates:

        - A cross-account policy for Amazon EventBridge Event Bus to enable Data Domain to send events to Central Gov. account
        - A Lake Formation data access role scoped down to the data domain products bucket
        - A Glue Catalog Database to hold Data Products for this Data Domain
        - A Rule to forward events to target Data Domain account.

        Object references are passed from the DataDomain account to the CentralGovernance account via a AWS Secret Manager secret and cross account access.
        It includes the following JSON object::

           {
              BucketName: 'clean-<ACCOUNT_ID>-<REGION>',
              Prefix: 'data-products',
              KmsKeyId: '<KMS_ID>,
           }

        :param id: the ID of the CDK Construct.
        :param domain_id: the account ID of the DataDomain to register.
        :param domain_name: the name of the DataDomain, i.e. Line of Business name.
        :param domain_secret_arn: the full ARN of the secret used by producers to share references with the central governance.
        :param lf_access_control_mode: Lake Formation Access Control mode for the DataDomain.

        :stability: experimental
        :access: public
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CentralGovernance.register_data_domain)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument domain_id", value=domain_id, expected_type=type_hints["domain_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_secret_arn", value=domain_secret_arn, expected_type=type_hints["domain_secret_arn"])
            check_type(argname="argument lf_access_control_mode", value=lf_access_control_mode, expected_type=type_hints["lf_access_control_mode"])
        return typing.cast(None, jsii.invoke(self, "registerDataDomain", [id, domain_id, domain_name, domain_secret_arn, lf_access_control_mode]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOMAIN_DATABASE_PREFIX")
    def DOMAIN_DATABASE_PREFIX(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DOMAIN_DATABASE_PREFIX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOMAIN_TAG_KEY")
    def DOMAIN_TAG_KEY(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DOMAIN_TAG_KEY"))

    @builtins.property
    @jsii.member(jsii_name="eventBus")
    def event_bus(self) -> aws_cdk.aws_events.IEventBus:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_events.IEventBus, jsii.get(self, "eventBus"))

    @builtins.property
    @jsii.member(jsii_name="workflowRole")
    def workflow_role(self) -> aws_cdk.aws_iam.IRole:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "workflowRole"))


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.CentralGovernanceProps",
    jsii_struct_bases=[],
    name_mapping={"lf_tags": "lfTags"},
)
class CentralGovernanceProps:
    def __init__(
        self,
        *,
        lf_tags: typing.Optional[typing.Sequence[typing.Union["LfTag", typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for the CentralGovernance Construct.

        :param lf_tags: (experimental) LF tags.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CentralGovernanceProps.__init__)
            check_type(argname="argument lf_tags", value=lf_tags, expected_type=type_hints["lf_tags"])
        self._values: typing.Dict[str, typing.Any] = {}
        if lf_tags is not None:
            self._values["lf_tags"] = lf_tags

    @builtins.property
    def lf_tags(self) -> typing.Optional[typing.List["LfTag"]]:
        '''(experimental) LF tags.

        :stability: experimental
        '''
        result = self._values.get("lf_tags")
        return typing.cast(typing.Optional[typing.List["LfTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CentralGovernanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomDataset(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.CustomDataset",
):
    '''(experimental) A CustomDataset is a dataset that you need to prepare for the [BatchReplayer](@link BatchReplayer) to generate data.

    The dataset is transformed into a [PreparedDataset](@link PreparedDataset) by a Glue Job that runs synchronously during the CDK deploy.
    The Glue job is sized based on the approximate size of the input data or uses autoscaling (max 100) if no data size is provided.

    The Glue job is applying the following transformations to the input dataset:

    1. Read the input dataset based on its format. Currently, it supports data in CSV, JSON and Parquet
    2. Group rows into tumbling windows based on the partition range parameter provided.
       The partition range should be adapted to the data volume and the total dataset time range
    3. Convert dates from MM-dd-yyyy HH:mm:ss.SSS to MM-dd-yyyyTHH:mm:ss.SSSZ format and remove null values
    4. Write data into the output bucket partitioned by the tumbling window time.
       For example, one partition for every 5 minutes.
    5. Generate a manifest file based on the previous output to be used by the BatchReplayer for generating data

    The CloudWatch log group is stored as an object parameter to help check any error with the Glue job.

    Usage example::

       import { CustomDataset, CustomDatasetInputFormat } from './data-generator/custom-dataset';

       const app = new App();
       const stack = new Stack(app, 'CustomDatasetStack');

       const custom = new CustomDataset(stack, 'CustomDataset', {
          s3Location: {
            bucketName: 'aws-analytics-reference-architecture',
            objectKey: 'datasets/custom',
          },
          inputFormat: CustomDatasetInputFormat.CSV,
          datetimeColumn: 'tpep_pickup_datetime',
          datetimeColumnsToAdjust: ['tpep_pickup_datetime'],
          partitionRange: Duration.minutes(5),
          approximateDataSize: 1,
       });

       new CfnOutput(this, 'LogGroupName', {
          exportName: 'logGroupName,
          value: custom.glueJobLogGroup,
       });

    An example of a custom dataset that can be processed by this construct is available in s3://aws-analytics-reference-architecture/datasets/custom

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        datetime_column: builtins.str,
        datetime_columns_to_adjust: typing.Sequence[builtins.str],
        input_format: "CustomDatasetInputFormat",
        partition_range: aws_cdk.Duration,
        s3_location: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        approximate_data_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of a CustomDataset construct that extends a PreparedDataset.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param datetime_column: (experimental) The datetime column to use for data generation as the time reference.
        :param datetime_columns_to_adjust: (experimental) The datetime columns to use for data generation.
        :param input_format: (experimental) The format of the input data.
        :param partition_range: (experimental) The interval to partition data and optimize the data generation in Minutes.
        :param s3_location: (experimental) The S3 location of the input data.
        :param approximate_data_size: (experimental) Approximate data size (in GB) of the custom dataset. Default: - The Glue job responsible for preparing the data uses autoscaling with a maximum of 100 workers

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(CustomDataset.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CustomDatasetProps(
            datetime_column=datetime_column,
            datetime_columns_to_adjust=datetime_columns_to_adjust,
            input_format=input_format,
            partition_range=partition_range,
            s3_location=s3_location,
            approximate_data_size=approximate_data_size,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="glueJobLogGroup")
    def glue_job_log_group(self) -> builtins.str:
        '''(experimental) The location of the logs to analyze potential errors in the Glue job.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "glueJobLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="preparedDataset")
    def prepared_dataset(self) -> "PreparedDataset":
        '''(experimental) The prepared dataset generated from the custom dataset.

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.get(self, "preparedDataset"))


@jsii.enum(jsii_type="aws-analytics-reference-architecture.CustomDatasetInputFormat")
class CustomDatasetInputFormat(enum.Enum):
    '''
    :stability: experimental
    '''

    CSV = "CSV"
    '''
    :stability: experimental
    '''
    PARQUET = "PARQUET"
    '''
    :stability: experimental
    '''
    JSON = "JSON"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.CustomDatasetProps",
    jsii_struct_bases=[],
    name_mapping={
        "datetime_column": "datetimeColumn",
        "datetime_columns_to_adjust": "datetimeColumnsToAdjust",
        "input_format": "inputFormat",
        "partition_range": "partitionRange",
        "s3_location": "s3Location",
        "approximate_data_size": "approximateDataSize",
    },
)
class CustomDatasetProps:
    def __init__(
        self,
        *,
        datetime_column: builtins.str,
        datetime_columns_to_adjust: typing.Sequence[builtins.str],
        input_format: CustomDatasetInputFormat,
        partition_range: aws_cdk.Duration,
        s3_location: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        approximate_data_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The properties for the Bring Your Own Data generator.

        :param datetime_column: (experimental) The datetime column to use for data generation as the time reference.
        :param datetime_columns_to_adjust: (experimental) The datetime columns to use for data generation.
        :param input_format: (experimental) The format of the input data.
        :param partition_range: (experimental) The interval to partition data and optimize the data generation in Minutes.
        :param s3_location: (experimental) The S3 location of the input data.
        :param approximate_data_size: (experimental) Approximate data size (in GB) of the custom dataset. Default: - The Glue job responsible for preparing the data uses autoscaling with a maximum of 100 workers

        :stability: experimental
        '''
        if isinstance(s3_location, dict):
            s3_location = Location(**s3_location)
        if __debug__:
            type_hints = typing.get_type_hints(CustomDatasetProps.__init__)
            check_type(argname="argument datetime_column", value=datetime_column, expected_type=type_hints["datetime_column"])
            check_type(argname="argument datetime_columns_to_adjust", value=datetime_columns_to_adjust, expected_type=type_hints["datetime_columns_to_adjust"])
            check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
            check_type(argname="argument partition_range", value=partition_range, expected_type=type_hints["partition_range"])
            check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            check_type(argname="argument approximate_data_size", value=approximate_data_size, expected_type=type_hints["approximate_data_size"])
        self._values: typing.Dict[str, typing.Any] = {
            "datetime_column": datetime_column,
            "datetime_columns_to_adjust": datetime_columns_to_adjust,
            "input_format": input_format,
            "partition_range": partition_range,
            "s3_location": s3_location,
        }
        if approximate_data_size is not None:
            self._values["approximate_data_size"] = approximate_data_size

    @builtins.property
    def datetime_column(self) -> builtins.str:
        '''(experimental) The datetime column to use for data generation as the time reference.

        :stability: experimental
        '''
        result = self._values.get("datetime_column")
        assert result is not None, "Required property 'datetime_column' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datetime_columns_to_adjust(self) -> typing.List[builtins.str]:
        '''(experimental) The datetime columns to use for data generation.

        :stability: experimental
        '''
        result = self._values.get("datetime_columns_to_adjust")
        assert result is not None, "Required property 'datetime_columns_to_adjust' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def input_format(self) -> CustomDatasetInputFormat:
        '''(experimental) The format of the input data.

        :stability: experimental
        '''
        result = self._values.get("input_format")
        assert result is not None, "Required property 'input_format' is missing"
        return typing.cast(CustomDatasetInputFormat, result)

    @builtins.property
    def partition_range(self) -> aws_cdk.Duration:
        '''(experimental) The interval to partition data and optimize the data generation in Minutes.

        :stability: experimental
        '''
        result = self._values.get("partition_range")
        assert result is not None, "Required property 'partition_range' is missing"
        return typing.cast(aws_cdk.Duration, result)

    @builtins.property
    def s3_location(self) -> aws_cdk.aws_s3.Location:
        '''(experimental) The S3 location of the input data.

        :stability: experimental
        '''
        result = self._values.get("s3_location")
        assert result is not None, "Required property 's3_location' is missing"
        return typing.cast(aws_cdk.aws_s3.Location, result)

    @builtins.property
    def approximate_data_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Approximate data size (in GB) of the custom dataset.

        :default: - The Glue job responsible for preparing the data uses autoscaling with a maximum of 100 workers

        :stability: experimental
        '''
        result = self._values.get("approximate_data_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomDatasetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDomain(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.DataDomain",
):
    '''(experimental) This CDK Construct creates all required resources for data mesh in Data Domain account.

    It creates the following:

    - A data lake with multiple layers (Raw, Cleaned, Transformed) using {@link DataLakeStorage} construct
    - An mazon EventBridge Event Bus and Rules to enable Central Governance account to send events to Data Domain account
    - An AWS Secret Manager secret encrypted via AWS KMS and used to share references with the central governance account
    - A Data Domain Workflow {@link DataDomainWorkflow} responsible for creating resources in the data domain via a Step Functions state machine
    - An optional Crawler workflow {@link DataDomainCrawler} responsible for updating the data product schema after registration via a Step Functions state machine

    Usage example::

       import { App, Stack } from 'aws-cdk-lib';
       import { Role } from 'aws-cdk-lib/aws-iam';
       import { DataDomain } from 'aws-analytics-reference-architecture';

       const exampleApp = new App();
       const stack = new Stack(exampleApp, 'DataProductStack');

       new DataDomain(stack, 'myDataDomain', {
         centralAccountId: '1234567891011',
         crawlerWorkflow: true,
         domainName: 'domainName'
       });

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        central_account_id: builtins.str,
        domain_name: builtins.str,
        crawler_workflow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Construct a new instance of DataDomain.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param central_account_id: (experimental) Central Governance account Id.
        :param domain_name: (experimental) Data domain name.
        :param crawler_workflow: (experimental) Flag to create a Crawler workflow in Data Domain account.

        :stability: experimental
        :access: public
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataDomain.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataDomainProps(
            central_account_id=central_account_id,
            domain_name=domain_name,
            crawler_workflow=crawler_workflow,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addBusRule")
    def add_bus_rule(
        self,
        id: builtins.str,
        mode: "LfAccessControlMode",
        workflow: aws_cdk.aws_stepfunctions.StateMachine,
    ) -> None:
        '''
        :param id: -
        :param mode: -
        :param workflow: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataDomain.add_bus_rule)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument workflow", value=workflow, expected_type=type_hints["workflow"])
        return typing.cast(None, jsii.invoke(self, "addBusRule", [id, mode, workflow]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DATA_PRODUCTS_PREFIX")
    def DATA_PRODUCTS_PREFIX(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DATA_PRODUCTS_PREFIX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOMAIN_BUS_NAME")
    def DOMAIN_BUS_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DOMAIN_BUS_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOMAIN_CONFIG_SECRET")
    def DOMAIN_CONFIG_SECRET(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DOMAIN_CONFIG_SECRET"))

    @builtins.property
    @jsii.member(jsii_name="centralAccountId")
    def central_account_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "centralAccountId"))

    @builtins.property
    @jsii.member(jsii_name="dataLake")
    def data_lake(self) -> "DataLakeStorage":
        '''
        :stability: experimental
        '''
        return typing.cast("DataLakeStorage", jsii.get(self, "dataLake"))

    @builtins.property
    @jsii.member(jsii_name="eventBus")
    def event_bus(self) -> aws_cdk.aws_events.EventBus:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_events.EventBus, jsii.get(self, "eventBus"))


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.DataDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "central_account_id": "centralAccountId",
        "domain_name": "domainName",
        "crawler_workflow": "crawlerWorkflow",
    },
)
class DataDomainProps:
    def __init__(
        self,
        *,
        central_account_id: builtins.str,
        domain_name: builtins.str,
        crawler_workflow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for the DataDomain Construct.

        :param central_account_id: (experimental) Central Governance account Id.
        :param domain_name: (experimental) Data domain name.
        :param crawler_workflow: (experimental) Flag to create a Crawler workflow in Data Domain account.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataDomainProps.__init__)
            check_type(argname="argument central_account_id", value=central_account_id, expected_type=type_hints["central_account_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument crawler_workflow", value=crawler_workflow, expected_type=type_hints["crawler_workflow"])
        self._values: typing.Dict[str, typing.Any] = {
            "central_account_id": central_account_id,
            "domain_name": domain_name,
        }
        if crawler_workflow is not None:
            self._values["crawler_workflow"] = crawler_workflow

    @builtins.property
    def central_account_id(self) -> builtins.str:
        '''(experimental) Central Governance account Id.

        :stability: experimental
        '''
        result = self._values.get("central_account_id")
        assert result is not None, "Required property 'central_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''(experimental) Data domain name.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def crawler_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Flag to create a Crawler workflow in Data Domain account.

        :stability: experimental
        '''
        result = self._values.get("crawler_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.DataLakeExporterProps",
    jsii_struct_bases=[],
    name_mapping={
        "sink_bucket": "sinkBucket",
        "source_glue_database": "sourceGlueDatabase",
        "source_glue_table": "sourceGlueTable",
        "source_kinesis_data_stream": "sourceKinesisDataStream",
        "delivery_interval": "deliveryInterval",
        "delivery_size": "deliverySize",
        "sink_object_key": "sinkObjectKey",
    },
)
class DataLakeExporterProps:
    def __init__(
        self,
        *,
        sink_bucket: aws_cdk.aws_s3.Bucket,
        source_glue_database: aws_cdk.aws_glue_alpha.Database,
        source_glue_table: aws_cdk.aws_glue_alpha.Table,
        source_kinesis_data_stream: aws_cdk.aws_kinesis.Stream,
        delivery_interval: typing.Optional[jsii.Number] = None,
        delivery_size: typing.Optional[jsii.Number] = None,
        sink_object_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The properties for DataLakeExporter Construct.

        :param sink_bucket: (experimental) Amazon S3 sink Bucket where the data lake exporter write data.
        :param source_glue_database: (experimental) Source AWS Glue Database containing the schema of the stream.
        :param source_glue_table: (experimental) Source AWS Glue Table containing the schema of the stream.
        :param source_kinesis_data_stream: (experimental) Source must be an Amazon Kinesis Data Stream.
        :param delivery_interval: (experimental) Delivery interval in seconds. The frequency of the data delivery is defined by this interval. Default: - Set to 900 seconds
        :param delivery_size: (experimental) Maximum delivery size in MB. The frequency of the data delivery is defined by this maximum delivery size. Default: - Set to 128 MB
        :param sink_object_key: (experimental) Amazon S3 sink object key where the data lake exporter write data. Default: - The data is written at the bucket root

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataLakeExporterProps.__init__)
            check_type(argname="argument sink_bucket", value=sink_bucket, expected_type=type_hints["sink_bucket"])
            check_type(argname="argument source_glue_database", value=source_glue_database, expected_type=type_hints["source_glue_database"])
            check_type(argname="argument source_glue_table", value=source_glue_table, expected_type=type_hints["source_glue_table"])
            check_type(argname="argument source_kinesis_data_stream", value=source_kinesis_data_stream, expected_type=type_hints["source_kinesis_data_stream"])
            check_type(argname="argument delivery_interval", value=delivery_interval, expected_type=type_hints["delivery_interval"])
            check_type(argname="argument delivery_size", value=delivery_size, expected_type=type_hints["delivery_size"])
            check_type(argname="argument sink_object_key", value=sink_object_key, expected_type=type_hints["sink_object_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "sink_bucket": sink_bucket,
            "source_glue_database": source_glue_database,
            "source_glue_table": source_glue_table,
            "source_kinesis_data_stream": source_kinesis_data_stream,
        }
        if delivery_interval is not None:
            self._values["delivery_interval"] = delivery_interval
        if delivery_size is not None:
            self._values["delivery_size"] = delivery_size
        if sink_object_key is not None:
            self._values["sink_object_key"] = sink_object_key

    @builtins.property
    def sink_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''(experimental) Amazon S3 sink Bucket where the data lake exporter write data.

        :stability: experimental
        '''
        result = self._values.get("sink_bucket")
        assert result is not None, "Required property 'sink_bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.Bucket, result)

    @builtins.property
    def source_glue_database(self) -> aws_cdk.aws_glue_alpha.Database:
        '''(experimental) Source AWS Glue Database containing the schema of the stream.

        :stability: experimental
        '''
        result = self._values.get("source_glue_database")
        assert result is not None, "Required property 'source_glue_database' is missing"
        return typing.cast(aws_cdk.aws_glue_alpha.Database, result)

    @builtins.property
    def source_glue_table(self) -> aws_cdk.aws_glue_alpha.Table:
        '''(experimental) Source AWS Glue Table containing the schema of the stream.

        :stability: experimental
        '''
        result = self._values.get("source_glue_table")
        assert result is not None, "Required property 'source_glue_table' is missing"
        return typing.cast(aws_cdk.aws_glue_alpha.Table, result)

    @builtins.property
    def source_kinesis_data_stream(self) -> aws_cdk.aws_kinesis.Stream:
        '''(experimental) Source must be an Amazon Kinesis Data Stream.

        :stability: experimental
        '''
        result = self._values.get("source_kinesis_data_stream")
        assert result is not None, "Required property 'source_kinesis_data_stream' is missing"
        return typing.cast(aws_cdk.aws_kinesis.Stream, result)

    @builtins.property
    def delivery_interval(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Delivery interval in seconds.

        The frequency of the data delivery is defined by this interval.

        :default: - Set to 900 seconds

        :stability: experimental
        '''
        result = self._values.get("delivery_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delivery_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum delivery size in MB.

        The frequency of the data delivery is defined by this maximum delivery size.

        :default: - Set to 128 MB

        :stability: experimental
        '''
        result = self._values.get("delivery_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sink_object_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) Amazon S3 sink object key where the data lake exporter write data.

        :default: - The data is written at the bucket root

        :stability: experimental
        '''
        result = self._values.get("sink_object_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLakeExporterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.DataLakeStorageProps",
    jsii_struct_bases=[],
    name_mapping={
        "clean_archive_delay": "cleanArchiveDelay",
        "clean_infrequent_access_delay": "cleanInfrequentAccessDelay",
        "raw_archive_delay": "rawArchiveDelay",
        "raw_infrequent_access_delay": "rawInfrequentAccessDelay",
        "transform_archive_delay": "transformArchiveDelay",
        "transform_infrequent_access_delay": "transformInfrequentAccessDelay",
    },
)
class DataLakeStorageProps:
    def __init__(
        self,
        *,
        clean_archive_delay: typing.Optional[jsii.Number] = None,
        clean_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        raw_archive_delay: typing.Optional[jsii.Number] = None,
        raw_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        transform_archive_delay: typing.Optional[jsii.Number] = None,
        transform_infrequent_access_delay: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for the DataLakeStorage Construct.

        :param clean_archive_delay: (experimental) Delay (in days) before archiving CLEAN data to frozen storage (Glacier storage class). Default: - Objects are not archived to Glacier
        :param clean_infrequent_access_delay: (experimental) Delay (in days) before moving CLEAN data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 90 days
        :param raw_archive_delay: (experimental) Delay (in days) before archiving RAW data to frozen storage (Glacier storage class). Default: - Move objects to Glacier after 90 days
        :param raw_infrequent_access_delay: (experimental) Delay (in days) before moving RAW data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 30 days
        :param transform_archive_delay: (experimental) Delay (in days) before archiving TRANSFORM data to frozen storage (Glacier storage class). Default: - Objects are not archived to Glacier
        :param transform_infrequent_access_delay: (experimental) Delay (in days) before moving TRANSFORM data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 90 days

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataLakeStorageProps.__init__)
            check_type(argname="argument clean_archive_delay", value=clean_archive_delay, expected_type=type_hints["clean_archive_delay"])
            check_type(argname="argument clean_infrequent_access_delay", value=clean_infrequent_access_delay, expected_type=type_hints["clean_infrequent_access_delay"])
            check_type(argname="argument raw_archive_delay", value=raw_archive_delay, expected_type=type_hints["raw_archive_delay"])
            check_type(argname="argument raw_infrequent_access_delay", value=raw_infrequent_access_delay, expected_type=type_hints["raw_infrequent_access_delay"])
            check_type(argname="argument transform_archive_delay", value=transform_archive_delay, expected_type=type_hints["transform_archive_delay"])
            check_type(argname="argument transform_infrequent_access_delay", value=transform_infrequent_access_delay, expected_type=type_hints["transform_infrequent_access_delay"])
        self._values: typing.Dict[str, typing.Any] = {}
        if clean_archive_delay is not None:
            self._values["clean_archive_delay"] = clean_archive_delay
        if clean_infrequent_access_delay is not None:
            self._values["clean_infrequent_access_delay"] = clean_infrequent_access_delay
        if raw_archive_delay is not None:
            self._values["raw_archive_delay"] = raw_archive_delay
        if raw_infrequent_access_delay is not None:
            self._values["raw_infrequent_access_delay"] = raw_infrequent_access_delay
        if transform_archive_delay is not None:
            self._values["transform_archive_delay"] = transform_archive_delay
        if transform_infrequent_access_delay is not None:
            self._values["transform_infrequent_access_delay"] = transform_infrequent_access_delay

    @builtins.property
    def clean_archive_delay(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Delay (in days) before archiving CLEAN data to frozen storage (Glacier storage class).

        :default: - Objects are not archived to Glacier

        :stability: experimental
        '''
        result = self._values.get("clean_archive_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def clean_infrequent_access_delay(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Delay (in days) before moving CLEAN data to cold storage (Infrequent Access storage class).

        :default: - Move objects to Infrequent Access after 90 days

        :stability: experimental
        '''
        result = self._values.get("clean_infrequent_access_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def raw_archive_delay(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Delay (in days) before archiving RAW data to frozen storage (Glacier storage class).

        :default: - Move objects to Glacier after 90 days

        :stability: experimental
        '''
        result = self._values.get("raw_archive_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def raw_infrequent_access_delay(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Delay (in days) before moving RAW data to cold storage (Infrequent Access storage class).

        :default: - Move objects to Infrequent Access after 30 days

        :stability: experimental
        '''
        result = self._values.get("raw_infrequent_access_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def transform_archive_delay(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Delay (in days) before archiving TRANSFORM data to frozen storage (Glacier storage class).

        :default: - Objects are not archived to Glacier

        :stability: experimental
        '''
        result = self._values.get("transform_archive_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def transform_infrequent_access_delay(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Delay (in days) before moving TRANSFORM data to cold storage (Infrequent Access storage class).

        :default: - Move objects to Infrequent Access after 90 days

        :stability: experimental
        '''
        result = self._values.get("transform_infrequent_access_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLakeStorageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ec2SsmRole(
    aws_cdk.aws_iam.Role,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.Ec2SsmRole",
):
    '''(experimental) Construct extending IAM Role with AmazonSSMManagedInstanceCore managed policy.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        assumed_by: aws_cdk.aws_iam.IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IManagedPolicy]] = None,
        max_session_duration: typing.Optional[aws_cdk.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[aws_cdk.aws_iam.IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the Ec2SsmRole class.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        :stability: experimental
        :access: public
        :since: 1.0.0
        '''
        if __debug__:
            type_hints = typing.get_type_hints(Ec2SsmRole.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.aws_iam.RoleProps(
            assumed_by=assumed_by,
            description=description,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.EmrEksClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "eks_admin_role_arn": "eksAdminRoleArn",
        "autoscaler_version": "autoscalerVersion",
        "default_node_groups": "defaultNodeGroups",
        "eks_cluster_name": "eksClusterName",
        "eks_vpc_attributes": "eksVpcAttributes",
        "emr_eks_nodegroups": "emrEksNodegroups",
        "kubernetes_version": "kubernetesVersion",
    },
)
class EmrEksClusterProps:
    def __init__(
        self,
        *,
        eks_admin_role_arn: builtins.str,
        autoscaler_version: typing.Optional[jsii.Number] = None,
        default_node_groups: typing.Optional[builtins.bool] = None,
        eks_cluster_name: typing.Optional[builtins.str] = None,
        eks_vpc_attributes: typing.Optional[typing.Union[aws_cdk.aws_ec2.VpcAttributes, typing.Dict[str, typing.Any]]] = None,
        emr_eks_nodegroups: typing.Optional[typing.Sequence["EmrEksNodegroup"]] = None,
        kubernetes_version: typing.Optional[aws_cdk.aws_eks.KubernetesVersion] = None,
    ) -> None:
        '''(experimental) The properties for the EmrEksCluster Construct class.

        :param eks_admin_role_arn: (experimental) Amazon IAM Role to be added to Amazon EKS master roles that will give access to kubernetes cluster from AWS console UI.
        :param autoscaler_version: (experimental) The version of autoscaler to pass to Helm. Default: - version matching the default Kubernete version
        :param default_node_groups: (experimental) If set to true construct will create default EKS nodegroups. There are three types of Nodegroup: - Nodegroup for critical jobs which use on-demand instances. - Nodegroup using spot instances for jobs that are not critical and can be preempted if a spot instance is reclaimed - Nodegroup to provide capacity for creating and running managed endpoints spark drivers and executors. Default: - true
        :param eks_cluster_name: (experimental) Name of the Amazon EKS cluster to be created. Default: - The [default cluster name]{@link EmrEksCluster.DEFAULT_CLUSTER_NAME}
        :param eks_vpc_attributes: (experimental) Attributes of the VPC where to deploy the EKS cluster VPC should have at least two private and public subnets in different Availability Zones All private subnets should have the following tags: 'for-use-with-amazon-emr-managed-policies'='true' 'kubernetes.io/role/internal-elb'='1' All public subnets should have the following tag: 'kubernetes.io/role/elb'='1'.
        :param emr_eks_nodegroups: (experimental) List of EmrEksNodegroup to create in the cluster in addition to the default [nodegroups]{@link EmrEksNodegroup}. Default: - Don't create additional nodegroups
        :param kubernetes_version: (experimental) Kubernetes version for Amazon EKS cluster that will be created. Default: - v1.21 version is used

        :stability: experimental
        '''
        if isinstance(eks_vpc_attributes, dict):
            eks_vpc_attributes = VpcAttributes(**eks_vpc_attributes)
        if __debug__:
            type_hints = typing.get_type_hints(EmrEksClusterProps.__init__)
            check_type(argname="argument eks_admin_role_arn", value=eks_admin_role_arn, expected_type=type_hints["eks_admin_role_arn"])
            check_type(argname="argument autoscaler_version", value=autoscaler_version, expected_type=type_hints["autoscaler_version"])
            check_type(argname="argument default_node_groups", value=default_node_groups, expected_type=type_hints["default_node_groups"])
            check_type(argname="argument eks_cluster_name", value=eks_cluster_name, expected_type=type_hints["eks_cluster_name"])
            check_type(argname="argument eks_vpc_attributes", value=eks_vpc_attributes, expected_type=type_hints["eks_vpc_attributes"])
            check_type(argname="argument emr_eks_nodegroups", value=emr_eks_nodegroups, expected_type=type_hints["emr_eks_nodegroups"])
            check_type(argname="argument kubernetes_version", value=kubernetes_version, expected_type=type_hints["kubernetes_version"])
        self._values: typing.Dict[str, typing.Any] = {
            "eks_admin_role_arn": eks_admin_role_arn,
        }
        if autoscaler_version is not None:
            self._values["autoscaler_version"] = autoscaler_version
        if default_node_groups is not None:
            self._values["default_node_groups"] = default_node_groups
        if eks_cluster_name is not None:
            self._values["eks_cluster_name"] = eks_cluster_name
        if eks_vpc_attributes is not None:
            self._values["eks_vpc_attributes"] = eks_vpc_attributes
        if emr_eks_nodegroups is not None:
            self._values["emr_eks_nodegroups"] = emr_eks_nodegroups
        if kubernetes_version is not None:
            self._values["kubernetes_version"] = kubernetes_version

    @builtins.property
    def eks_admin_role_arn(self) -> builtins.str:
        '''(experimental) Amazon IAM Role to be added to Amazon EKS master roles that will give access to kubernetes cluster from AWS console UI.

        :stability: experimental
        '''
        result = self._values.get("eks_admin_role_arn")
        assert result is not None, "Required property 'eks_admin_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaler_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The version of autoscaler to pass to Helm.

        :default: - version matching the default Kubernete version

        :stability: experimental
        '''
        result = self._values.get("autoscaler_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_node_groups(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If set to true construct will create default EKS nodegroups.

        There are three types of Nodegroup:

        - Nodegroup for critical jobs which use on-demand instances.
        - Nodegroup using spot instances for jobs that are not critical and can be preempted if a spot instance is reclaimed
        - Nodegroup to provide capacity for creating and running managed endpoints spark drivers and executors.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("default_node_groups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def eks_cluster_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the Amazon EKS cluster to be created.

        :default: - The [default cluster name]{@link EmrEksCluster.DEFAULT_CLUSTER_NAME}

        :stability: experimental
        '''
        result = self._values.get("eks_cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eks_vpc_attributes(self) -> typing.Optional[aws_cdk.aws_ec2.VpcAttributes]:
        '''(experimental) Attributes of the VPC where to deploy the EKS cluster VPC should have at least two private and public subnets in different Availability Zones All private subnets should have the following tags: 'for-use-with-amazon-emr-managed-policies'='true' 'kubernetes.io/role/internal-elb'='1' All public subnets should have the following tag: 'kubernetes.io/role/elb'='1'.

        :stability: experimental
        '''
        result = self._values.get("eks_vpc_attributes")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.VpcAttributes], result)

    @builtins.property
    def emr_eks_nodegroups(self) -> typing.Optional[typing.List["EmrEksNodegroup"]]:
        '''(experimental) List of EmrEksNodegroup to create in the cluster in addition to the default [nodegroups]{@link EmrEksNodegroup}.

        :default: - Don't create additional nodegroups

        :stability: experimental
        '''
        result = self._values.get("emr_eks_nodegroups")
        return typing.cast(typing.Optional[typing.List["EmrEksNodegroup"]], result)

    @builtins.property
    def kubernetes_version(self) -> typing.Optional[aws_cdk.aws_eks.KubernetesVersion]:
        '''(experimental) Kubernetes version for Amazon EKS cluster that will be created.

        :default: - v1.21 version is used

        :stability: experimental
        '''
        result = self._values.get("kubernetes_version")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.KubernetesVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrEksClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrEksNodegroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.EmrEksNodegroup",
):
    '''
    :stability: experimental
    :summary: EmrEksNodegroup containing the default Nodegroups
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CRITICAL_ALL")
    def CRITICAL_ALL(cls) -> "EmrEksNodegroupOptions":
        '''(experimental) Default nodegroup configuration for EMR on EKS critical workloads (both drivers and executors).

        :stability: experimental
        '''
        return typing.cast("EmrEksNodegroupOptions", jsii.sget(cls, "CRITICAL_ALL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NOTEBOOK_DRIVER")
    def NOTEBOOK_DRIVER(cls) -> "EmrEksNodegroupOptions":
        '''(experimental) Default nodegroup configuration for EMR Studio notebooks used with EMR on EKS (drivers only).

        :stability: experimental
        '''
        return typing.cast("EmrEksNodegroupOptions", jsii.sget(cls, "NOTEBOOK_DRIVER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NOTEBOOK_EXECUTOR")
    def NOTEBOOK_EXECUTOR(cls) -> "EmrEksNodegroupOptions":
        '''(experimental) Default nodegroup configuration for EMR Studio notebooks used with EMR on EKS (executors only).

        :stability: experimental
        '''
        return typing.cast("EmrEksNodegroupOptions", jsii.sget(cls, "NOTEBOOK_EXECUTOR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NOTEBOOK_WITHOUT_PODTEMPLATE")
    def NOTEBOOK_WITHOUT_PODTEMPLATE(cls) -> "EmrEksNodegroupOptions":
        '''(experimental) Default nodegroup configuration for EMR Studio notebooks used with EMR on EKS This nodegroup is replacing [NOTEBOOK_DRIVER]{@link EmrEksNodegroup.NOTEBOOK_DRIVER} and [NOTEBOOK_EXECUTOR]{@link EmrEksNodegroup.NOTEBOOK_EXECUTOR} because EMR on EKS Managed Endpoint currently doesn't support Pod Template customization.

        :stability: experimental
        '''
        return typing.cast("EmrEksNodegroupOptions", jsii.sget(cls, "NOTEBOOK_WITHOUT_PODTEMPLATE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SHARED_DRIVER")
    def SHARED_DRIVER(cls) -> "EmrEksNodegroupOptions":
        '''(experimental) Default nodegroup configuration for EMR on EKS shared (non-crtical) workloads (drivers only).

        :stability: experimental
        '''
        return typing.cast("EmrEksNodegroupOptions", jsii.sget(cls, "SHARED_DRIVER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SHARED_EXECUTOR")
    def SHARED_EXECUTOR(cls) -> "EmrEksNodegroupOptions":
        '''(experimental) Default nodegroup configuration for EMR on EKS shared (non-crtical) workloads (executors only).

        :stability: experimental
        '''
        return typing.cast("EmrEksNodegroupOptions", jsii.sget(cls, "SHARED_EXECUTOR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TOOLING_ALL")
    def TOOLING_ALL(cls) -> "EmrEksNodegroupOptions":
        '''
        :stability: experimental
        '''
        return typing.cast("EmrEksNodegroupOptions", jsii.sget(cls, "TOOLING_ALL"))


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.EmrEksNodegroupOptions",
    jsii_struct_bases=[aws_cdk.aws_eks.NodegroupOptions],
    name_mapping={
        "ami_type": "amiType",
        "capacity_type": "capacityType",
        "desired_size": "desiredSize",
        "disk_size": "diskSize",
        "force_update": "forceUpdate",
        "instance_types": "instanceTypes",
        "labels": "labels",
        "launch_template_spec": "launchTemplateSpec",
        "max_size": "maxSize",
        "min_size": "minSize",
        "nodegroup_name": "nodegroupName",
        "node_role": "nodeRole",
        "release_version": "releaseVersion",
        "remote_access": "remoteAccess",
        "subnets": "subnets",
        "tags": "tags",
        "taints": "taints",
        "mount_nvme": "mountNvme",
        "subnet": "subnet",
    },
)
class EmrEksNodegroupOptions(aws_cdk.aws_eks.NodegroupOptions):
    def __init__(
        self,
        *,
        ami_type: typing.Optional[aws_cdk.aws_eks.NodegroupAmiType] = None,
        capacity_type: typing.Optional[aws_cdk.aws_eks.CapacityType] = None,
        desired_size: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update: typing.Optional[builtins.bool] = None,
        instance_types: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.InstanceType]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_template_spec: typing.Optional[typing.Union[aws_cdk.aws_eks.LaunchTemplateSpec, typing.Dict[str, typing.Any]]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        nodegroup_name: typing.Optional[builtins.str] = None,
        node_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        release_version: typing.Optional[builtins.str] = None,
        remote_access: typing.Optional[typing.Union[aws_cdk.aws_eks.NodegroupRemoteAccess, typing.Dict[str, typing.Any]]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_eks.TaintSpec, typing.Dict[str, typing.Any]]]] = None,
        mount_nvme: typing.Optional[builtins.bool] = None,
        subnet: typing.Optional[aws_cdk.aws_ec2.ISubnet] = None,
    ) -> None:
        '''(experimental) The Options for adding EmrEksNodegroup to an EmrEksCluster.

        Some of the Amazon EKS Nodegroup parameters are overriden:

        - NodegroupName by the id and an index per AZ
        - LaunchTemplate spec
        - SubnetList by either the subnet parameter or one subnet per Amazon EKS Cluster AZ.
        - Labels and Taints are automatically used to tag the nodegroup for the cluster autoscaler

        :param ami_type: The AMI type for your node group. If you explicitly specify the launchTemplate with custom AMI, do not specify this property, or the node group deployment will fail. In other cases, you will need to specify correct amiType for the nodegroup. Default: - auto-determined from the instanceTypes property when launchTemplateSpec property is not specified
        :param capacity_type: The capacity type of the nodegroup. Default: - ON_DEMAND
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_types: The instance types to use for your node group. Default: t3.medium will be used according to the cloudformation document.
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param launch_template_spec: Launch template specification used for the nodegroup. Default: - no launch template
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than or equal to zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None
        :param taints: The Kubernetes taints to be applied to the nodes in the node group when they are created. Default: - None
        :param mount_nvme: (experimental) Set to true if using instance types with local NVMe drives to mount them automatically at boot time. Default: false
        :param subnet: (experimental) Configure the Amazon EKS NodeGroup in this subnet. Use this setting for resource dependencies like an Amazon RDS database. The subnet must include the availability zone information because the nodegroup is tagged with the AZ for the K8S Cluster Autoscaler. Default: - One NodeGroup is deployed per cluster AZ

        :stability: experimental
        '''
        if isinstance(launch_template_spec, dict):
            launch_template_spec = LaunchTemplateSpec(**launch_template_spec)
        if isinstance(remote_access, dict):
            remote_access = NodegroupRemoteAccess(**remote_access)
        if isinstance(subnets, dict):
            subnets = SubnetSelection(**subnets)
        if __debug__:
            type_hints = typing.get_type_hints(EmrEksNodegroupOptions.__init__)
            check_type(argname="argument ami_type", value=ami_type, expected_type=type_hints["ami_type"])
            check_type(argname="argument capacity_type", value=capacity_type, expected_type=type_hints["capacity_type"])
            check_type(argname="argument desired_size", value=desired_size, expected_type=type_hints["desired_size"])
            check_type(argname="argument disk_size", value=disk_size, expected_type=type_hints["disk_size"])
            check_type(argname="argument force_update", value=force_update, expected_type=type_hints["force_update"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument launch_template_spec", value=launch_template_spec, expected_type=type_hints["launch_template_spec"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            check_type(argname="argument nodegroup_name", value=nodegroup_name, expected_type=type_hints["nodegroup_name"])
            check_type(argname="argument node_role", value=node_role, expected_type=type_hints["node_role"])
            check_type(argname="argument release_version", value=release_version, expected_type=type_hints["release_version"])
            check_type(argname="argument remote_access", value=remote_access, expected_type=type_hints["remote_access"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
            check_type(argname="argument mount_nvme", value=mount_nvme, expected_type=type_hints["mount_nvme"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        self._values: typing.Dict[str, typing.Any] = {}
        if ami_type is not None:
            self._values["ami_type"] = ami_type
        if capacity_type is not None:
            self._values["capacity_type"] = capacity_type
        if desired_size is not None:
            self._values["desired_size"] = desired_size
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if force_update is not None:
            self._values["force_update"] = force_update
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if labels is not None:
            self._values["labels"] = labels
        if launch_template_spec is not None:
            self._values["launch_template_spec"] = launch_template_spec
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size
        if nodegroup_name is not None:
            self._values["nodegroup_name"] = nodegroup_name
        if node_role is not None:
            self._values["node_role"] = node_role
        if release_version is not None:
            self._values["release_version"] = release_version
        if remote_access is not None:
            self._values["remote_access"] = remote_access
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags
        if taints is not None:
            self._values["taints"] = taints
        if mount_nvme is not None:
            self._values["mount_nvme"] = mount_nvme
        if subnet is not None:
            self._values["subnet"] = subnet

    @builtins.property
    def ami_type(self) -> typing.Optional[aws_cdk.aws_eks.NodegroupAmiType]:
        '''The AMI type for your node group.

        If you explicitly specify the launchTemplate with custom AMI, do not specify this property, or
        the node group deployment will fail. In other cases, you will need to specify correct amiType for the nodegroup.

        :default: - auto-determined from the instanceTypes property when launchTemplateSpec property is not specified
        '''
        result = self._values.get("ami_type")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.NodegroupAmiType], result)

    @builtins.property
    def capacity_type(self) -> typing.Optional[aws_cdk.aws_eks.CapacityType]:
        '''The capacity type of the nodegroup.

        :default: - ON_DEMAND
        '''
        result = self._values.get("capacity_type")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.CapacityType], result)

    @builtins.property
    def desired_size(self) -> typing.Optional[jsii.Number]:
        '''The current number of worker nodes that the managed node group should maintain.

        If not specified,
        the nodewgroup will initially create ``minSize`` instances.

        :default: 2
        '''
        result = self._values.get("desired_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        '''The root device disk size (in GiB) for your node group instances.

        :default: 20
        '''
        result = self._values.get("disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def force_update(self) -> typing.Optional[builtins.bool]:
        '''Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue.

        If an update fails because pods could not be drained, you can force the update after it fails to terminate the old
        node whether or not any pods are
        running on the node.

        :default: true
        '''
        result = self._values.get("force_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instance_types(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.InstanceType]]:
        '''The instance types to use for your node group.

        :default: t3.medium will be used according to the cloudformation document.

        :see: - https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-instancetypes
        '''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.InstanceType]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The Kubernetes labels to be applied to the nodes in the node group when they are created.

        :default: - None
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def launch_template_spec(
        self,
    ) -> typing.Optional[aws_cdk.aws_eks.LaunchTemplateSpec]:
        '''Launch template specification used for the nodegroup.

        :default: - no launch template

        :see: - https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html
        '''
        result = self._values.get("launch_template_spec")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.LaunchTemplateSpec], result)

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of worker nodes that the managed node group can scale out to.

        Managed node groups can support up to 100 nodes by default.

        :default: - desiredSize
        '''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of worker nodes that the managed node group can scale in to.

        This number must be greater than or equal to zero.

        :default: 1
        '''
        result = self._values.get("min_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nodegroup_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Nodegroup.

        :default: - resource ID
        '''
        result = self._values.get("nodegroup_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''The IAM role to associate with your node group.

        The Amazon EKS worker node kubelet daemon
        makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through
        an IAM instance profile and associated policies. Before you can launch worker nodes and register them
        into a cluster, you must create an IAM role for those worker nodes to use when they are launched.

        :default: - None. Auto-generated if not specified.
        '''
        result = self._values.get("node_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def release_version(self) -> typing.Optional[builtins.str]:
        '''The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``).

        :default: - The latest available AMI version for the node group's current Kubernetes version is used.
        '''
        result = self._values.get("release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_access(self) -> typing.Optional[aws_cdk.aws_eks.NodegroupRemoteAccess]:
        '''The remote access (SSH) configuration to use with your node group.

        Disabled by default, however, if you
        specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group,
        then port 22 on the worker nodes is opened to the internet (0.0.0.0/0)

        :default: - disabled
        '''
        result = self._values.get("remote_access")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.NodegroupRemoteAccess], result)

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''The subnets to use for the Auto Scaling group that is created for your node group.

        By specifying the
        SubnetSelection, the selected subnets will automatically apply required tags i.e.
        ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with
        the name of your cluster.

        :default: - private subnets
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The metadata to apply to the node group to assist with categorization and organization.

        Each tag consists of
        a key and an optional value, both of which you define. Node group tags do not propagate to any other resources
        associated with the node group, such as the Amazon EC2 instances or subnets.

        :default: - None
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def taints(self) -> typing.Optional[typing.List[aws_cdk.aws_eks.TaintSpec]]:
        '''The Kubernetes taints to be applied to the nodes in the node group when they are created.

        :default: - None
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_eks.TaintSpec]], result)

    @builtins.property
    def mount_nvme(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true if using instance types with local NVMe drives to mount them automatically at boot time.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("mount_nvme")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def subnet(self) -> typing.Optional[aws_cdk.aws_ec2.ISubnet]:
        '''(experimental) Configure the Amazon EKS NodeGroup in this subnet.

        Use this setting for resource dependencies like an Amazon RDS database.
        The subnet must include the availability zone information because the nodegroup is tagged with the AZ for the K8S Cluster Autoscaler.

        :default: - One NodeGroup is deployed per cluster AZ

        :stability: experimental
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISubnet], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrEksNodegroupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.EmrManagedEndpointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role": "executionRole",
        "managed_endpoint_name": "managedEndpointName",
        "virtual_cluster_id": "virtualClusterId",
        "configuration_overrides": "configurationOverrides",
        "emr_on_eks_version": "emrOnEksVersion",
    },
)
class EmrManagedEndpointOptions:
    def __init__(
        self,
        *,
        execution_role: aws_cdk.aws_iam.IRole,
        managed_endpoint_name: builtins.str,
        virtual_cluster_id: builtins.str,
        configuration_overrides: typing.Optional[builtins.str] = None,
        emr_on_eks_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The properties for the EMR Managed Endpoint to create.

        :param execution_role: (experimental) The Amazon IAM role used as the execution role, this role must provide access to all the AWS resource a user will interact with These can be S3, DynamoDB, Glue Catalog.
        :param managed_endpoint_name: (experimental) The name of the EMR managed endpoint.
        :param virtual_cluster_id: (experimental) The Id of the Amazon EMR virtual cluster containing the managed endpoint.
        :param configuration_overrides: (experimental) The JSON configuration overrides for Amazon EMR on EKS configuration attached to the managed endpoint. Default: - Configuration related to the [default nodegroup for notebook]{@link EmrEksNodegroup.NOTEBOOK_EXECUTOR}
        :param emr_on_eks_version: (experimental) The Amazon EMR version to use. Default: - The [default Amazon EMR version]{@link EmrEksCluster.DEFAULT_EMR_VERSION}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmrManagedEndpointOptions.__init__)
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument managed_endpoint_name", value=managed_endpoint_name, expected_type=type_hints["managed_endpoint_name"])
            check_type(argname="argument virtual_cluster_id", value=virtual_cluster_id, expected_type=type_hints["virtual_cluster_id"])
            check_type(argname="argument configuration_overrides", value=configuration_overrides, expected_type=type_hints["configuration_overrides"])
            check_type(argname="argument emr_on_eks_version", value=emr_on_eks_version, expected_type=type_hints["emr_on_eks_version"])
        self._values: typing.Dict[str, typing.Any] = {
            "execution_role": execution_role,
            "managed_endpoint_name": managed_endpoint_name,
            "virtual_cluster_id": virtual_cluster_id,
        }
        if configuration_overrides is not None:
            self._values["configuration_overrides"] = configuration_overrides
        if emr_on_eks_version is not None:
            self._values["emr_on_eks_version"] = emr_on_eks_version

    @builtins.property
    def execution_role(self) -> aws_cdk.aws_iam.IRole:
        '''(experimental) The Amazon IAM role used as the execution role, this role must provide access to all the AWS resource a user will interact with These can be S3, DynamoDB, Glue Catalog.

        :stability: experimental
        '''
        result = self._values.get("execution_role")
        assert result is not None, "Required property 'execution_role' is missing"
        return typing.cast(aws_cdk.aws_iam.IRole, result)

    @builtins.property
    def managed_endpoint_name(self) -> builtins.str:
        '''(experimental) The name of the EMR managed endpoint.

        :stability: experimental
        '''
        result = self._values.get("managed_endpoint_name")
        assert result is not None, "Required property 'managed_endpoint_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_cluster_id(self) -> builtins.str:
        '''(experimental) The Id of the Amazon EMR virtual cluster containing the managed endpoint.

        :stability: experimental
        '''
        result = self._values.get("virtual_cluster_id")
        assert result is not None, "Required property 'virtual_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_overrides(self) -> typing.Optional[builtins.str]:
        '''(experimental) The JSON configuration overrides for Amazon EMR on EKS configuration attached to the managed endpoint.

        :default: - Configuration related to the [default nodegroup for notebook]{@link EmrEksNodegroup.NOTEBOOK_EXECUTOR}

        :stability: experimental
        '''
        result = self._values.get("configuration_overrides")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emr_on_eks_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Amazon EMR version to use.

        :default: - The [default Amazon EMR version]{@link EmrEksCluster.DEFAULT_EMR_VERSION}

        :stability: experimental
        '''
        result = self._values.get("emr_on_eks_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrManagedEndpointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.EmrVirtualClusterOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "create_namespace": "createNamespace",
        "eks_namespace": "eksNamespace",
    },
)
class EmrVirtualClusterOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        create_namespace: typing.Optional[builtins.bool] = None,
        eks_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The properties for the EmrVirtualCluster Construct class.

        :param name: (experimental) name of the Amazon Emr virtual cluster to be created.
        :param create_namespace: (experimental) creates Amazon EKS namespace. Default: - Do not create the namespace
        :param eks_namespace: (experimental) name of the Amazon EKS namespace to be linked to the Amazon EMR virtual cluster. Default: - Use the default namespace

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmrVirtualClusterOptions.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument create_namespace", value=create_namespace, expected_type=type_hints["create_namespace"])
            check_type(argname="argument eks_namespace", value=eks_namespace, expected_type=type_hints["eks_namespace"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if create_namespace is not None:
            self._values["create_namespace"] = create_namespace
        if eks_namespace is not None:
            self._values["eks_namespace"] = eks_namespace

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) name of the Amazon Emr virtual cluster to be created.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def create_namespace(self) -> typing.Optional[builtins.bool]:
        '''(experimental) creates Amazon EKS namespace.

        :default: - Do not create the namespace

        :stability: experimental
        '''
        result = self._values.get("create_namespace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def eks_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) name of the Amazon EKS namespace to be linked to the Amazon EMR virtual cluster.

        :default: - Use the default namespace

        :stability: experimental
        '''
        result = self._values.get("eks_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrVirtualClusterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FlywayRunner(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.FlywayRunner",
):
    '''(experimental) A CDK construct that runs flyway migration scripts against a redshift cluster.

    This construct is based on two main resource, an AWS Lambda hosting a flyway runner
    and one custom resource invoking it when content of migrationScriptsFolderAbsolutePath changes.

    Usage example:

    *This example assume that migration SQL files are located in ``resources/sql`` of the cdk project.::

       import * as path from 'path';
       import * as ec2 from 'aws-cdk-lib/aws-ec2';
       import * as redshift from '@aws-cdk/aws-redshift-alpha';
       import * as cdk from 'aws-cdk-lib';

       import { FlywayRunner } from 'aws-analytics-reference-architecture';

       const integTestApp = new cdk.App();
       const stack = new cdk.Stack(integTestApp, 'fywayRunnerTest');

       const vpc = new ec2.Vpc(stack, 'Vpc');

       const dbName = 'testdb';
       const cluster = new redshift.Cluster(stack, 'Redshift', {
          removalPolicy: cdk.RemovalPolicy.DESTROY,
          masterUser: {
            masterUsername: 'admin',
          },
          vpc,
          defaultDatabaseName: dbName,
       });

       new FlywayRunner(stack, 'testMigration', {
          migrationScriptsFolderAbsolutePath: path.join(__dirname, './resources/sql'),
          cluster: cluster,
          vpc: vpc,
          databaseName: dbName,
       });

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_redshift_alpha.Cluster,
        database_name: builtins.str,
        migration_scripts_folder_absolute_path: builtins.str,
        vpc: aws_cdk.aws_ec2.Vpc,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        replace_dictionary: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the FlywayRunner construct.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param cluster: (experimental) The cluster to run migration scripts against.
        :param database_name: (experimental) The database name to run migration scripts against.
        :param migration_scripts_folder_absolute_path: (experimental) The absolute path to the flyway migration scripts. Those scripts needs to follow expected flyway naming convention.
        :param vpc: (experimental) The vpc hosting the cluster.
        :param log_retention: (experimental) Period to keep the logs around. Default: logs.RetentionDays.ONE_WEEK
        :param replace_dictionary: (experimental) A key-value map of string (encapsulated between ``${`` and ``}``) to replace in the SQL files given. Example: - The SQL file:: SELECT * FROM ${TABLE_NAME}; - The replacement map:: replaceDictionary = { TABLE_NAME: 'my_table' } Default: - No replacement is done

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlywayRunner.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FlywayRunnerProps(
            cluster=cluster,
            database_name=database_name,
            migration_scripts_folder_absolute_path=migration_scripts_folder_absolute_path,
            vpc=vpc,
            log_retention=log_retention,
            replace_dictionary=replace_dictionary,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="runner")
    def runner(self) -> aws_cdk.CustomResource:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.CustomResource, jsii.get(self, "runner"))


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.FlywayRunnerProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "database_name": "databaseName",
        "migration_scripts_folder_absolute_path": "migrationScriptsFolderAbsolutePath",
        "vpc": "vpc",
        "log_retention": "logRetention",
        "replace_dictionary": "replaceDictionary",
    },
)
class FlywayRunnerProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_redshift_alpha.Cluster,
        database_name: builtins.str,
        migration_scripts_folder_absolute_path: builtins.str,
        vpc: aws_cdk.aws_ec2.Vpc,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        replace_dictionary: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) The properties of the FlywayRunner construct, needed to run flyway migration scripts.

        :param cluster: (experimental) The cluster to run migration scripts against.
        :param database_name: (experimental) The database name to run migration scripts against.
        :param migration_scripts_folder_absolute_path: (experimental) The absolute path to the flyway migration scripts. Those scripts needs to follow expected flyway naming convention.
        :param vpc: (experimental) The vpc hosting the cluster.
        :param log_retention: (experimental) Period to keep the logs around. Default: logs.RetentionDays.ONE_WEEK
        :param replace_dictionary: (experimental) A key-value map of string (encapsulated between ``${`` and ``}``) to replace in the SQL files given. Example: - The SQL file:: SELECT * FROM ${TABLE_NAME}; - The replacement map:: replaceDictionary = { TABLE_NAME: 'my_table' } Default: - No replacement is done

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlywayRunnerProps.__init__)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument migration_scripts_folder_absolute_path", value=migration_scripts_folder_absolute_path, expected_type=type_hints["migration_scripts_folder_absolute_path"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument replace_dictionary", value=replace_dictionary, expected_type=type_hints["replace_dictionary"])
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "database_name": database_name,
            "migration_scripts_folder_absolute_path": migration_scripts_folder_absolute_path,
            "vpc": vpc,
        }
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if replace_dictionary is not None:
            self._values["replace_dictionary"] = replace_dictionary

    @builtins.property
    def cluster(self) -> aws_cdk.aws_redshift_alpha.Cluster:
        '''(experimental) The cluster to run migration scripts against.

        :stability: experimental
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_redshift_alpha.Cluster, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        '''(experimental) The database name to run migration scripts against.

        :stability: experimental
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def migration_scripts_folder_absolute_path(self) -> builtins.str:
        '''(experimental) The absolute path to the flyway migration scripts.

        Those scripts needs to follow expected flyway naming convention.

        :see: https://flywaydb.org/documentation/concepts/migrations.html#sql-based-migrations for more details.
        :stability: experimental
        '''
        result = self._values.get("migration_scripts_folder_absolute_path")
        assert result is not None, "Required property 'migration_scripts_folder_absolute_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.Vpc:
        '''(experimental) The vpc hosting the cluster.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.Vpc, result)

    @builtins.property
    def log_retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        '''(experimental) Period to keep the logs around.

        :default: logs.RetentionDays.ONE_WEEK

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.RetentionDays], result)

    @builtins.property
    def replace_dictionary(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) A key-value map of string (encapsulated between ``${`` and ``}``) to replace in the SQL files given.

        Example:

        - The SQL file::

             SELECT * FROM ${TABLE_NAME};
        - The replacement map::

             replaceDictionary = {
               TABLE_NAME: 'my_table'
             }

        :default: - No replacement is done

        :stability: experimental
        '''
        result = self._values.get("replace_dictionary")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlywayRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueDemoRole(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.GlueDemoRole",
):
    '''(experimental) GlueDemoRole Construct to automatically setup a new Amazon IAM role to use with AWS Glue jobs.

    The role is created with AWSGlueServiceRole policy and authorize all actions on S3.
    If you would like to scope down the permission you should create a new role with a scoped down policy
    The Construct provides a getOrCreate method for SingletonInstantiation

    :stability: experimental
    '''

    @jsii.member(jsii_name="getOrCreate")
    @builtins.classmethod
    def get_or_create(cls, scope: constructs.Construct) -> "GlueDemoRole":
        '''
        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GlueDemoRole.get_or_create)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("GlueDemoRole", jsii.sinvoke(cls, "getOrCreate", [scope]))

    @builtins.property
    @jsii.member(jsii_name="iamRole")
    def iam_role(self) -> aws_cdk.aws_iam.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_iam.Role, jsii.get(self, "iamRole"))


class LakeFormationAdmin(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.LakeFormationAdmin",
):
    '''(experimental) An AWS Lake Formation administrator with privileges to do all the administration tasks in AWS Lake Formation.

    The principal is an Amazon IAM user or role and is added/removed to the list of AWS Lake Formation administrator
    via the Data Lake Settings API.
    Creation/deleting first retrieves the current list of administrators and then add/remove the principal to this list.
    These steps are done outside of any transaction. Concurrent modifications between retrieving and updating can lead to inconsistent results.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        principal: typing.Union[aws_cdk.aws_iam.IRole, aws_cdk.aws_iam.IUser],
        catalog_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construct a new instance of LakeFormationAdmin.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param principal: (experimental) The principal to declare as an AWS Lake Formation administrator.
        :param catalog_id: (experimental) The catalog ID to create the administrator in. Default: - The account ID

        :stability: experimental
        :access: public
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LakeFormationAdmin.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LakeFormationAdminProps(principal=principal, catalog_id=catalog_id)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addCdkExecRole")
    @builtins.classmethod
    def add_cdk_exec_role(
        cls,
        scope: constructs.Construct,
        name: builtins.str,
    ) -> "LakeFormationAdmin":
        '''(experimental) Adds the CDK execution role to LF admins It requires default cdk bootstrap.

        :param scope: -
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LakeFormationAdmin.add_cdk_exec_role)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("LakeFormationAdmin", jsii.sinvoke(cls, "addCdkExecRole", [scope, name]))

    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "catalogId"))

    @catalog_id.setter
    def catalog_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(LakeFormationAdmin, "catalog_id").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalogId", value)

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> typing.Union[aws_cdk.aws_iam.IRole, aws_cdk.aws_iam.IUser]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Union[aws_cdk.aws_iam.IRole, aws_cdk.aws_iam.IUser], jsii.get(self, "principal"))

    @principal.setter
    def principal(
        self,
        value: typing.Union[aws_cdk.aws_iam.IRole, aws_cdk.aws_iam.IUser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(LakeFormationAdmin, "principal").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value)


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.LakeFormationAdminProps",
    jsii_struct_bases=[],
    name_mapping={"principal": "principal", "catalog_id": "catalogId"},
)
class LakeFormationAdminProps:
    def __init__(
        self,
        *,
        principal: typing.Union[aws_cdk.aws_iam.IRole, aws_cdk.aws_iam.IUser],
        catalog_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for the lakeFormationAdmin Construct.

        :param principal: (experimental) The principal to declare as an AWS Lake Formation administrator.
        :param catalog_id: (experimental) The catalog ID to create the administrator in. Default: - The account ID

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LakeFormationAdminProps.__init__)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "principal": principal,
        }
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id

    @builtins.property
    def principal(self) -> typing.Union[aws_cdk.aws_iam.IRole, aws_cdk.aws_iam.IUser]:
        '''(experimental) The principal to declare as an AWS Lake Formation administrator.

        :stability: experimental
        '''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(typing.Union[aws_cdk.aws_iam.IRole, aws_cdk.aws_iam.IUser], result)

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The catalog ID to create the administrator in.

        :default: - The account ID

        :stability: experimental
        '''
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LakeFormationAdminProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LakeFormationS3Location(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.LakeFormationS3Location",
):
    '''(experimental) This CDK construct aims to register an S3 Location for Lakeformation with Read and Write access.

    If the location is in a different account, cross account access should be granted via the [S3CrossAccount]{@link S3CrossAccount} construct.
    If the S3 location is encrypted with KMS, the key must be explicitly passed to the construct because CDK cannot retrieve bucket encryption key from imported buckets.
    Imported buckets are generally used in cross account setup like data mesh.

    This construct instantiate 2 objects:

    - An IAM role with read/write permissions to the S3 location and encrypt/decrypt access to the KMS key used to encypt the bucket
    - A CfnResource is based on an IAM role with 2 policy statement folowing the least privilege AWS best practices:

      - Statement 1 for S3 permissions
      - Statement 2 for KMS permissions if the bucket is encrypted

    The CDK construct instantiate the CfnResource in order to register the S3 location with Lakeformation using the IAM role defined above.

    Usage example::

       import * as cdk from 'aws-cdk-lib';
       import { LakeformationS3Location } from 'aws-analytics-reference-architecture';

       const exampleApp = new cdk.App();
       const stack = new cdk.Stack(exampleApp, 'LakeformationS3LocationStack');

       const myKey = new Key(stack, 'MyKey')
       const myBucket = new Bucket(stack, 'MyBucket', {
          encryptionKey: myKey,
       })

       new LakeFormationS3Location(stack, 'MyLakeformationS3Location', {
          s3Location: {
            bucketName: myBucket.bucketName,
            objectKey: 'my-prefix',
          },
          kmsKeyId: myBucket.encryptionKey.keyId,
       });

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        kms_key_id: builtins.str,
        s3_location: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param kms_key_id: (experimental) KMS key used to encrypt the S3 Location. Default: - No encryption is used
        :param s3_location: (experimental) S3 location to be registered with Lakeformation.
        :param account_id: (experimental) Account ID owning the S3 location. Default: - Current account is used

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LakeFormationS3Location.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LakeFormationS3LocationProps(
            kms_key_id=kms_key_id, s3_location=s3_location, account_id=account_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="dataAccessRole")
    def data_access_role(self) -> aws_cdk.aws_iam.Role:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_iam.Role, jsii.get(self, "dataAccessRole"))


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.LakeFormationS3LocationProps",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_id": "kmsKeyId",
        "s3_location": "s3Location",
        "account_id": "accountId",
    },
)
class LakeFormationS3LocationProps:
    def __init__(
        self,
        *,
        kms_key_id: builtins.str,
        s3_location: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The props for LF-S3-Location Construct.

        :param kms_key_id: (experimental) KMS key used to encrypt the S3 Location. Default: - No encryption is used
        :param s3_location: (experimental) S3 location to be registered with Lakeformation.
        :param account_id: (experimental) Account ID owning the S3 location. Default: - Current account is used

        :stability: experimental
        '''
        if isinstance(s3_location, dict):
            s3_location = Location(**s3_location)
        if __debug__:
            type_hints = typing.get_type_hints(LakeFormationS3LocationProps.__init__)
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "kms_key_id": kms_key_id,
            "s3_location": s3_location,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def kms_key_id(self) -> builtins.str:
        '''(experimental) KMS key used to encrypt the S3 Location.

        :default: - No encryption is used

        :stability: experimental
        '''
        result = self._values.get("kms_key_id")
        assert result is not None, "Required property 'kms_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_location(self) -> aws_cdk.aws_s3.Location:
        '''(experimental) S3 location to be registered with Lakeformation.

        :stability: experimental
        '''
        result = self._values.get("s3_location")
        assert result is not None, "Required property 's3_location' is missing"
        return typing.cast(aws_cdk.aws_s3.Location, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account ID owning the S3 location.

        :default: - Current account is used

        :stability: experimental
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LakeFormationS3LocationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-analytics-reference-architecture.LfAccessControlMode")
class LfAccessControlMode(enum.Enum):
    '''(experimental) Enum to define access control mode in Lake Formation.

    :stability: experimental
    '''

    NRAC = "NRAC"
    '''
    :stability: experimental
    '''
    TBAC = "TBAC"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.LfTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class LfTag:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''(experimental) LF Tag interface.

        :param key: 
        :param values: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LfTag.__init__)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LfTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.NotebookManagedEndpointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "execution_policy": "executionPolicy",
        "managed_endpoint_name": "managedEndpointName",
        "configuration_overrides": "configurationOverrides",
        "emr_on_eks_version": "emrOnEksVersion",
    },
)
class NotebookManagedEndpointOptions:
    def __init__(
        self,
        *,
        execution_policy: aws_cdk.aws_iam.ManagedPolicy,
        managed_endpoint_name: builtins.str,
        configuration_overrides: typing.Any = None,
        emr_on_eks_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The properties for defining a Managed Endpoint The interface is used to create a managed Endpoint which can be leveraged by multiple users.

        :param execution_policy: (experimental) The name of the policy to be used for the execution Role to pass to ManagedEndpoint, this role should allow access to any resource needed for the job including: Amazon S3 buckets, Amazon DynamoDB, AWS Glue Data Catalog.
        :param managed_endpoint_name: (experimental) The name of the managed endpoint if no name is provided then the name of the policy associated with managed endpoint will be used as a name.
        :param configuration_overrides: (experimental) The JSON configuration overrides for Amazon EMR on EKS configuration attached to the managed endpoint an example can be found [here] (https://github.com/aws-samples/aws-analytics-reference-architecture/blob/main/core/src/emr-eks-data-platform/resources/k8s/emr-eks-config/critical.json).
        :param emr_on_eks_version: (experimental) The version of Amazon EMR to deploy.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NotebookManagedEndpointOptions.__init__)
            check_type(argname="argument execution_policy", value=execution_policy, expected_type=type_hints["execution_policy"])
            check_type(argname="argument managed_endpoint_name", value=managed_endpoint_name, expected_type=type_hints["managed_endpoint_name"])
            check_type(argname="argument configuration_overrides", value=configuration_overrides, expected_type=type_hints["configuration_overrides"])
            check_type(argname="argument emr_on_eks_version", value=emr_on_eks_version, expected_type=type_hints["emr_on_eks_version"])
        self._values: typing.Dict[str, typing.Any] = {
            "execution_policy": execution_policy,
            "managed_endpoint_name": managed_endpoint_name,
        }
        if configuration_overrides is not None:
            self._values["configuration_overrides"] = configuration_overrides
        if emr_on_eks_version is not None:
            self._values["emr_on_eks_version"] = emr_on_eks_version

    @builtins.property
    def execution_policy(self) -> aws_cdk.aws_iam.ManagedPolicy:
        '''(experimental) The name of the policy to be used for the execution Role to pass to ManagedEndpoint, this role should allow access to any resource needed for the job including: Amazon S3 buckets, Amazon DynamoDB, AWS Glue Data Catalog.

        :stability: experimental
        '''
        result = self._values.get("execution_policy")
        assert result is not None, "Required property 'execution_policy' is missing"
        return typing.cast(aws_cdk.aws_iam.ManagedPolicy, result)

    @builtins.property
    def managed_endpoint_name(self) -> builtins.str:
        '''(experimental) The name of the managed endpoint if no name is provided then the name of the policy associated with managed endpoint will be used as a name.

        :stability: experimental
        '''
        result = self._values.get("managed_endpoint_name")
        assert result is not None, "Required property 'managed_endpoint_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_overrides(self) -> typing.Any:
        '''(experimental) The JSON configuration overrides for Amazon EMR on EKS configuration attached to the managed endpoint an example can be found [here] (https://github.com/aws-samples/aws-analytics-reference-architecture/blob/main/core/src/emr-eks-data-platform/resources/k8s/emr-eks-config/critical.json).

        :stability: experimental
        '''
        result = self._values.get("configuration_overrides")
        return typing.cast(typing.Any, result)

    @builtins.property
    def emr_on_eks_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of Amazon EMR to deploy.

        :stability: experimental
        '''
        result = self._values.get("emr_on_eks_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebookManagedEndpointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.NotebookPlatformProps",
    jsii_struct_bases=[],
    name_mapping={
        "emr_eks": "emrEks",
        "studio_auth_mode": "studioAuthMode",
        "studio_name": "studioName",
        "eks_namespace": "eksNamespace",
        "idp_arn": "idpArn",
        "idp_auth_url": "idpAuthUrl",
        "idp_relay_state_parameter_name": "idpRelayStateParameterName",
    },
)
class NotebookPlatformProps:
    def __init__(
        self,
        *,
        emr_eks: "EmrEksCluster",
        studio_auth_mode: "StudioAuthMode",
        studio_name: builtins.str,
        eks_namespace: typing.Optional[builtins.str] = None,
        idp_arn: typing.Optional[builtins.str] = None,
        idp_auth_url: typing.Optional[builtins.str] = None,
        idp_relay_state_parameter_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The properties for NotebookPlatform Construct.

        :param emr_eks: (experimental) Required the EmrEks infrastructure used for the deployment.
        :param studio_auth_mode: (experimental) Required the authentication mode of Amazon EMR Studio Either 'SSO' or 'IAM' defined in the Enum {@link studioAuthMode}.
        :param studio_name: (experimental) Required the name to be given to the Amazon EMR Studio Must be unique across the AWS account.
        :param eks_namespace: (experimental) the namespace where to deploy the EMR Virtual Cluster. Default: - Use the {@link EmrVirtualClusterOptions} default namespace
        :param idp_arn: (experimental) Used when IAM Authentication is selected with IAM federation with an external identity provider (IdP) for Amazon EMR Studio Value taken from the IAM console in the Identity providers console.
        :param idp_auth_url: (experimental) Used when IAM Authentication is selected with IAM federation with an external identity provider (IdP) for Amazon EMR Studio This is the URL used to sign in the AWS console.
        :param idp_relay_state_parameter_name: (experimental) Used when IAM Authentication is selected with IAM federation with an external identity provider (IdP) for Amazon EMR Studio Value can be set with {@link IdpRelayState} Enum or through a value provided by the user.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NotebookPlatformProps.__init__)
            check_type(argname="argument emr_eks", value=emr_eks, expected_type=type_hints["emr_eks"])
            check_type(argname="argument studio_auth_mode", value=studio_auth_mode, expected_type=type_hints["studio_auth_mode"])
            check_type(argname="argument studio_name", value=studio_name, expected_type=type_hints["studio_name"])
            check_type(argname="argument eks_namespace", value=eks_namespace, expected_type=type_hints["eks_namespace"])
            check_type(argname="argument idp_arn", value=idp_arn, expected_type=type_hints["idp_arn"])
            check_type(argname="argument idp_auth_url", value=idp_auth_url, expected_type=type_hints["idp_auth_url"])
            check_type(argname="argument idp_relay_state_parameter_name", value=idp_relay_state_parameter_name, expected_type=type_hints["idp_relay_state_parameter_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "emr_eks": emr_eks,
            "studio_auth_mode": studio_auth_mode,
            "studio_name": studio_name,
        }
        if eks_namespace is not None:
            self._values["eks_namespace"] = eks_namespace
        if idp_arn is not None:
            self._values["idp_arn"] = idp_arn
        if idp_auth_url is not None:
            self._values["idp_auth_url"] = idp_auth_url
        if idp_relay_state_parameter_name is not None:
            self._values["idp_relay_state_parameter_name"] = idp_relay_state_parameter_name

    @builtins.property
    def emr_eks(self) -> "EmrEksCluster":
        '''(experimental) Required the EmrEks infrastructure used for the deployment.

        :stability: experimental
        '''
        result = self._values.get("emr_eks")
        assert result is not None, "Required property 'emr_eks' is missing"
        return typing.cast("EmrEksCluster", result)

    @builtins.property
    def studio_auth_mode(self) -> "StudioAuthMode":
        '''(experimental) Required the authentication mode of Amazon EMR Studio Either 'SSO' or 'IAM' defined in the Enum {@link studioAuthMode}.

        :stability: experimental
        '''
        result = self._values.get("studio_auth_mode")
        assert result is not None, "Required property 'studio_auth_mode' is missing"
        return typing.cast("StudioAuthMode", result)

    @builtins.property
    def studio_name(self) -> builtins.str:
        '''(experimental) Required the name to be given to the Amazon EMR Studio Must be unique across the AWS account.

        :stability: experimental
        '''
        result = self._values.get("studio_name")
        assert result is not None, "Required property 'studio_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eks_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) the namespace where to deploy the EMR Virtual Cluster.

        :default: - Use the {@link EmrVirtualClusterOptions} default namespace

        :stability: experimental
        '''
        result = self._values.get("eks_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idp_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Used when IAM Authentication is selected with IAM federation with an external identity provider (IdP) for Amazon EMR Studio Value taken from the IAM console in the Identity providers console.

        :stability: experimental
        '''
        result = self._values.get("idp_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idp_auth_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Used when IAM Authentication is selected with IAM federation with an external identity provider (IdP) for Amazon EMR Studio This is the URL used to sign in the AWS console.

        :stability: experimental
        '''
        result = self._values.get("idp_auth_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idp_relay_state_parameter_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Used when IAM Authentication is selected with IAM federation with an external identity provider (IdP) for Amazon EMR Studio Value can be set with {@link IdpRelayState} Enum or through a value provided by the user.

        :stability: experimental
        '''
        result = self._values.get("idp_relay_state_parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebookPlatformProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.NotebookUserOptions",
    jsii_struct_bases=[],
    name_mapping={
        "identity_name": "identityName",
        "notebook_managed_endpoints": "notebookManagedEndpoints",
        "identity_type": "identityType",
    },
)
class NotebookUserOptions:
    def __init__(
        self,
        *,
        identity_name: builtins.str,
        notebook_managed_endpoints: typing.Sequence[typing.Union[NotebookManagedEndpointOptions, typing.Dict[str, typing.Any]]],
        identity_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The properties for defining a user.

        The interface is used to create and assign a user or a group to an Amazon EMR Studio

        :param identity_name: (experimental) Required Name of the identity as it appears in AWS SSO console, or the name to be given to a user in IAM_AUTHENTICATED.
        :param notebook_managed_endpoints: (experimental) Required Array of {@link NotebookManagedEndpointOptions} this defines the managed endpoint the notebook/workspace user will have access to.
        :param identity_type: (experimental) Required Type of the identity either GROUP or USER, to be used when SSO is used as an authentication mode {@see SSOIdentityType}.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NotebookUserOptions.__init__)
            check_type(argname="argument identity_name", value=identity_name, expected_type=type_hints["identity_name"])
            check_type(argname="argument notebook_managed_endpoints", value=notebook_managed_endpoints, expected_type=type_hints["notebook_managed_endpoints"])
            check_type(argname="argument identity_type", value=identity_type, expected_type=type_hints["identity_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "identity_name": identity_name,
            "notebook_managed_endpoints": notebook_managed_endpoints,
        }
        if identity_type is not None:
            self._values["identity_type"] = identity_type

    @builtins.property
    def identity_name(self) -> builtins.str:
        '''(experimental) Required Name of the identity as it appears in AWS SSO console, or the name to be given to a user in IAM_AUTHENTICATED.

        :stability: experimental
        '''
        result = self._values.get("identity_name")
        assert result is not None, "Required property 'identity_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notebook_managed_endpoints(self) -> typing.List[NotebookManagedEndpointOptions]:
        '''(experimental) Required Array of {@link NotebookManagedEndpointOptions} this defines the managed endpoint the notebook/workspace user will have access to.

        :stability: experimental
        '''
        result = self._values.get("notebook_managed_endpoints")
        assert result is not None, "Required property 'notebook_managed_endpoints' is missing"
        return typing.cast(typing.List[NotebookManagedEndpointOptions], result)

    @builtins.property
    def identity_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Required Type of the identity either GROUP or USER, to be used when SSO is used as an authentication mode {@see SSOIdentityType}.

        :stability: experimental
        '''
        result = self._values.get("identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebookUserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PreparedDataset(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.PreparedDataset",
):
    '''(experimental) PreparedDataset is used by the [BatchReplayer]{@link BatchReplayer} to generate data in different targets.

    One of the startDatetime or offset parameter needs to be passed to the constructor:

    - StartDatetime is used for prepared datasets provided by the Analytics Reference Architecture because they are known during synthetize time.
    - Offset is used when a PreparedDataset is created from a CustomDataset because the startDatetime is not known during synthetize time.

    A PreparedDataset has following properties:

    1. Data is partitioned by timestamp (a range in seconds). Each folder stores data within a given range.
       There is no constraint on how long the timestamp range can be. But each file must not be larger than 100MB.
       Creating new PreparedDataset requires to find the right balance between number of partitions and the amount of data read by each BatchReplayer (micro-)batch
       The available PreparedDatasets have a timestamp range that fit the total dataset time range (see each dataset documentation below) to avoid having too many partitions.

    Here is an example:

    |- time_range_start=16000000000 Example::

       |- file1.csv 100MB

       |- file2.csv 50MB

    |- time_range_start=16000000300 // 5 minute range (300 sec::

       |- file1.csv 1MB

    |- time_range_start=16000000600 Example::

       |- file1.csv 100MB

       |- file2.csv 100MB

       |- whichever-file-name-is-fine-as-we-have-manifest-files.csv 50MB

    1. It has a manifest CSV file with two columns: start and path. Start is the timestamp

    start        , path

    16000000000  , s3://///time_range_start=16000000000/file1.csv

    16000000000  , s3://///time_range_start=16000000000/file2.csv

    16000000300  , s3://///time_range_start=16000000300/file1.csv

    16000000600  , s3://///time_range_start=16000000600/file1.csv

    16000000600  , s3://///time_range_start=16000000600/file2.csv

    16000000600  , s3://///time_range_start=16000000600/whichever-file....csv

    If the stack is deployed in another region than eu-west-1, data transfer costs will apply.
    The pre-defined PreparedDataset access is recharged to the consumer via Amazon S3 Requester Pay feature.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        date_time_column_to_filter: builtins.str,
        location: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        manifest_location: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        date_time_columns_to_adjust: typing.Optional[typing.Sequence[builtins.str]] = None,
        offset: typing.Optional[builtins.str] = None,
        start_datetime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the Dataset class.

        :param date_time_column_to_filter: (experimental) Datetime column for filtering data.
        :param location: (experimental) The Amazon S3 Location of the source dataset. It's composed of an Amazon S3 bucketName and an Amazon S3 objectKey
        :param manifest_location: (experimental) Manifest file in csv format with two columns: start, path.
        :param date_time_columns_to_adjust: (experimental) Array of column names with datetime to adjust. The source data will have date in the past 2021-01-01T00:00:00 while the data replayer will have have the current time. The difference (aka. offset) must be added to all datetime columns
        :param offset: (experimental) The offset in seconds for replaying data. It is the difference between the ``startDatetime`` and now. Default: - Calculate the offset from startDatetime parameter during CDK deployment
        :param start_datetime: (experimental) The minimum datetime value in the dataset used to calculate time offset. Default: - The offset parameter is used.

        :stability: experimental
        :access: public
        '''
        props = PreparedDatasetProps(
            date_time_column_to_filter=date_time_column_to_filter,
            location=location,
            manifest_location=manifest_location,
            date_time_columns_to_adjust=date_time_columns_to_adjust,
            offset=offset,
            start_datetime=start_datetime,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DATASETS_BUCKET")
    def DATASETS_BUCKET(cls) -> builtins.str:
        '''(experimental) The bucket name of the AWS Analytics Reference Architecture datasets.

        Data transfer costs will aply if the stack is deployed in another region than eu-west-1.
        The pre-defined PreparedDataset access is recharged to the consumer via Amazon S3 Requester Pay feature.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DATASETS_BUCKET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RETAIL_1_GB_CUSTOMER")
    def RETAIL_1_GB_CUSTOMER(cls) -> "PreparedDataset":
        '''(experimental) The customer dataset part of 1GB retail datasets. The time range is one week from min(customer_datetime) to max(customer_datetime).

        | Column name       	| Column type 	| Example                    	|
        |-------------------	|-------------	|----------------------------	|
        | customer_id       	| string      	| AAAAAAAAHCLFOHAA           	|
        | salutation        	| string      	| Miss                       	|
        | first_name        	| string      	| Tina                       	|
        | last_name         	| string      	| Frias                      	|
        | birth_country     	| string      	| GEORGIA                    	|
        | email_address     	| string      	| Tina.Frias@jdK4TZ1qJXB.org 	|
        | birth_date        	| string      	| 1924-06-14                 	|
        | gender            	| string      	| F                          	|
        | marital_status    	| string      	| D                          	|
        | education_status  	| string      	| 2 yr Degree                	|
        | purchase_estimate 	| bigint      	| 2500                       	|
        | credit_rating     	| string      	| Low Risk                   	|
        | buy_potential     	| string      	| 1001-5000                  	|
        | vehicle_count     	| bigint      	| 1                          	|
        | lower_bound       	| bigint      	| 170001                     	|
        | upper_bound       	| bigint      	| 180000                     	|
        | address_id        	| string      	| AAAAAAAALAFINEAA           	|
        | customer_datetime 	| string      	| 2021-01-19T08:07:47.140Z   	|

        The BatchReplayer adds two columns ingestion_start and ingestion_end

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.sget(cls, "RETAIL_1_GB_CUSTOMER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RETAIL_1_GB_CUSTOMER_ADDRESS")
    def RETAIL_1_GB_CUSTOMER_ADDRESS(cls) -> "PreparedDataset":
        '''(experimental) The customer address dataset part of 1GB retail datasets.

        It can be joined with customer dataset on address_id column.
        The time range is one week from min(address_datetime) to max(address_datetime)

        | Column name      | Column type | Example                  |
        |------------------|-------------|--------------------------|
        | address_id       | string      | AAAAAAAAINDKAAAA         |
        | city             | string      | Farmington               |
        | county           | string      | Greeley County           |
        | state            | string      | KS                       |
        | zip              | bigint      | 69145                    |
        | country          | string      | United States            |
        | gmt_offset       | double      | -6.0                     |
        | location_type    | string      | apartment                |
        | street           | string      | 390 Pine South Boulevard |
        | address_datetime | string      | 2021-01-03T02:25:52.826Z |

        The BatchReplayer adds two columns ingestion_start and ingestion_end

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.sget(cls, "RETAIL_1_GB_CUSTOMER_ADDRESS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RETAIL_1_GB_ITEM")
    def RETAIL_1_GB_ITEM(cls) -> "PreparedDataset":
        '''(experimental) The item dataset part of 1GB retail datasets The time range is one week from min(item_datetime) to max(item_datetime).

        | Column name   | Column type | Example                                        |
        |---------------|-------------|------------------------------------------------|
        |       item_id |      bigint |                                          15018 |
        |     item_desc |      string | Even ready materials tell with a ministers; un |
        |         brand |      string |                                 scholarmaxi #9 |
        |         class |      string |                                        fishing |
        |      category |      string |                                         Sports |
        |      manufact |      string |                                    eseoughtpri |
        |          size |      string |                                            N/A |
        |         color |      string |                                        thistle |
        |         units |      string |                                         Bundle |
        |     container |      string |                                        Unknown |
        |  product_name |      string |                          eingoughtbarantiought |
        | item_datetime |      string |                       2021-01-01T18:17:56.718Z |

        The BatchReplayer adds two columns ingestion_start and ingestion_end

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.sget(cls, "RETAIL_1_GB_ITEM"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RETAIL_1_GB_PROMO")
    def RETAIL_1_GB_PROMO(cls) -> "PreparedDataset":
        '''(experimental) The promo dataset part of 1GB retail datasets The time range is one week from min(promo_datetime) to max(promo_datetime).

        | Column name     | Column type | Example                  |
        |-----------------|-------------|--------------------------|
        |        promo_id |      string |         AAAAAAAAHIAAAAAA |
        |            cost |      double |                   1000.0 |
        | response_target |      bigint |                        1 |
        |      promo_name |      string |                     anti |
        |         purpose |      string |                  Unknown |
        |  start_datetime |      string | 2021-01-01 00:00:35.890Z |
        |    end_datetime |      string | 2021-01-02 13:16:09.785Z |
        |  promo_datetime |      string | 2021-01-01 00:00:16.104Z |

        The BatchReplayer adds two columns ingestion_start and ingestion_end

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.sget(cls, "RETAIL_1_GB_PROMO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RETAIL_1_GB_STORE")
    def RETAIL_1_GB_STORE(cls) -> "PreparedDataset":
        '''(experimental) The store dataset part of 1GB retail datasets The time range is one week from min(store_datetime) to max(store_datetime).

        | Column name      | Column type | Example                  |
        |------------------|-------------|--------------------------|
        |         store_id |      string |         AAAAAAAAKAAAAAAA |
        |       store_name |      string |                      bar |
        | number_employees |      bigint |                      219 |
        |      floor_space |      bigint |                  6505323 |
        |            hours |      string |                 8AM-12AM |
        |          manager |      string |             David Trahan |
        |        market_id |      bigint |                       10 |
        |   market_manager |      string |      Christopher Maxwell |
        |             city |      string |                   Midway |
        |           county |      string |        Williamson County |
        |            state |      string |                       TN |
        |              zip |      bigint |                    31904 |
        |          country |      string |            United States |
        |       gmt_offset |      double |                     -5.0 |
        |   tax_percentage |      double |                      0.0 |
        |           street |      string |            71 Cedar Blvd |
        |   store_datetime |      string | 2021-01-01T00:00:00.017Z |

        The BatchReplayer adds two columns ingestion_start and ingestion_end

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.sget(cls, "RETAIL_1_GB_STORE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RETAIL_1_GB_STORE_SALE")
    def RETAIL_1_GB_STORE_SALE(cls) -> "PreparedDataset":
        '''(experimental) The store sale dataset part of 1GB retail datasets. The time range is one week from min(sale_datetime) to max(sale_datetime).

        | Column name        | Column type | Example                  |
        |--------------------|-------------|--------------------------|
        | item_id            | bigint      | 3935                     |
        | ticket_id          | bigint      | 81837                    |
        | quantity           | bigint      | 96                       |
        | wholesale_cost     | double      | 21.15                    |
        | list_price         | double      | 21.78                    |
        | sales_price        | double      | 21.18                    |
        | ext_discount_amt   | double      | 0.0                      |
        | ext_sales_price    | double      | 2033.28                  |
        | ext_wholesale_cost | double      | 2030.4                   |
        | ext_list_price     | double      | 2090.88                  |
        | ext_tax            | double      | 81.1                     |
        | coupon_amt         | double      | 0.0                      |
        | net_paid           | double      | 2033.28                  |
        | net_paid_inc_tax   | double      | 2114.38                  |
        | net_profit         | double      | 2.88                     |
        | customer_id        | string      | AAAAAAAAEOIDAAAA         |
        | store_id           | string      | AAAAAAAABAAAAAAA         |
        | promo_id           | string      | AAAAAAAAEEAAAAAA         |
        | sale_datetime      | string      | 2021-01-04T22:20:04.144Z |

        The BatchReplayer adds two columns ingestion_start and ingestion_end

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.sget(cls, "RETAIL_1_GB_STORE_SALE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RETAIL_1_GB_WAREHOUSE")
    def RETAIL_1_GB_WAREHOUSE(cls) -> "PreparedDataset":
        '''(experimental) The store dataset part of 1GB retail datasets The time range is one week from min(warehouse_datetime) to max(warehouse_datetime).

        | Column name        | Column type | Example                  |
        |--------------------|-------------|--------------------------|
        |       warehouse_id |      string |         AAAAAAAAEAAAAAAA |
        |     warehouse_name |      string |               Operations |
        |             street |      string |    461 Second Johnson Wy |
        |               city |      string |                 Fairview |
        |                zip |      bigint |                    35709 |
        |             county |      string |        Williamson County |
        |              state |      string |                       TN |
        |            country |      string |            United States |
        |         gmt_offset |      double |                     -5.0 |
        | warehouse_datetime |      string | 2021-01-01T00:00:00.123Z |

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.sget(cls, "RETAIL_1_GB_WAREHOUSE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RETAIL_1_GB_WEB_SALE")
    def RETAIL_1_GB_WEB_SALE(cls) -> "PreparedDataset":
        '''(experimental) The web sale dataset part of 1GB retail datasets. The time range is one week from min(sale_datetime) to max(sale_datetime).

        | Column name           | Column type | Example                  |
        |-----------------------|-------------|--------------------------|
        | item_id               | bigint      | 3935                     |
        | order_id              | bigint      | 81837                    |
        | quantity              | bigint      | 65                       |
        | wholesale_cost        | double      | 32.98                    |
        | list_price            | double      | 47.82                    |
        | sales_price           | double      | 36.34                    |
        | ext_discount_amt      | double      | 2828.8                   |
        | ext_sales_price       | double      | 2362.1                   |
        | ext_wholesale_cost    | double      | 2143.7                   |
        | ext_list_price        | double      | 3108.3                   |
        | ext_tax               | double      | 0.0                      |
        | coupon_amt            | double      | 209.62                   |
        | ext_ship_cost         | double      | 372.45                   |
        | net_paid              | double      | 2152.48                  |
        | net_paid_inc_tax      | double      | 2152.48                  |
        | net_paid_inc_ship     | double      | 442.33                   |
        | net_paid_inc_ship_tax | double      | 442.33                   |
        | net_profit            | double      | 8.78                     |
        | bill_customer_id      | string      | AAAAAAAALNLFAAAA         |
        | ship_customer_id      | string      | AAAAAAAALPPJAAAA         |
        | warehouse_id          | string      | AAAAAAAABAAAAAAA         |
        | promo_id              | string      | AAAAAAAAPCAAAAAA         |
        | ship_delay            | string      | OVERNIGHT                |
        | ship_mode             | string      | SEA                      |
        | ship_carrier          | string      | GREAT EASTERN            |
        | sale_datetime         | string      | 2021-01-06T15:00:19.373Z |

        The BatchReplayer adds two columns ingestion_start and ingestion_end

        :stability: experimental
        '''
        return typing.cast("PreparedDataset", jsii.sget(cls, "RETAIL_1_GB_WEB_SALE"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeColumnToFilter")
    def date_time_column_to_filter(self) -> builtins.str:
        '''(experimental) Datetime column for filtering data.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dateTimeColumnToFilter"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> aws_cdk.aws_s3.Location:
        '''(experimental) The Amazon S3 Location of the source dataset.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Location, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="manifestLocation")
    def manifest_location(self) -> aws_cdk.aws_s3.Location:
        '''(experimental) Manifest file in csv format with two columns: start, path.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Location, jsii.get(self, "manifestLocation"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) The name of the SQL table extracted from path.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeColumnsToAdjust")
    def date_time_columns_to_adjust(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Array of column names with datetime to adjust.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dateTimeColumnsToAdjust"))

    @builtins.property
    @jsii.member(jsii_name="offset")
    def offset(self) -> typing.Optional[builtins.str]:
        '''(experimental) The offset of the Dataset (difference between min datetime and now) in Seconds.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offset"))

    @builtins.property
    @jsii.member(jsii_name="startDateTime")
    def start_date_time(self) -> typing.Optional[builtins.str]:
        '''(experimental) Start datetime replaying this dataset.

        Your data set may start from 1 Jan 2020
        But you can specify this to 1 Feb 2020 to omit the first month data.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDateTime"))


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.PreparedDatasetProps",
    jsii_struct_bases=[],
    name_mapping={
        "date_time_column_to_filter": "dateTimeColumnToFilter",
        "location": "location",
        "manifest_location": "manifestLocation",
        "date_time_columns_to_adjust": "dateTimeColumnsToAdjust",
        "offset": "offset",
        "start_datetime": "startDatetime",
    },
)
class PreparedDatasetProps:
    def __init__(
        self,
        *,
        date_time_column_to_filter: builtins.str,
        location: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        manifest_location: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        date_time_columns_to_adjust: typing.Optional[typing.Sequence[builtins.str]] = None,
        offset: typing.Optional[builtins.str] = None,
        start_datetime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The properties for the PreparedDataset class used by the BatchReplayer construct.

        :param date_time_column_to_filter: (experimental) Datetime column for filtering data.
        :param location: (experimental) The Amazon S3 Location of the source dataset. It's composed of an Amazon S3 bucketName and an Amazon S3 objectKey
        :param manifest_location: (experimental) Manifest file in csv format with two columns: start, path.
        :param date_time_columns_to_adjust: (experimental) Array of column names with datetime to adjust. The source data will have date in the past 2021-01-01T00:00:00 while the data replayer will have have the current time. The difference (aka. offset) must be added to all datetime columns
        :param offset: (experimental) The offset in seconds for replaying data. It is the difference between the ``startDatetime`` and now. Default: - Calculate the offset from startDatetime parameter during CDK deployment
        :param start_datetime: (experimental) The minimum datetime value in the dataset used to calculate time offset. Default: - The offset parameter is used.

        :stability: experimental
        '''
        if isinstance(location, dict):
            location = Location(**location)
        if isinstance(manifest_location, dict):
            manifest_location = Location(**manifest_location)
        if __debug__:
            type_hints = typing.get_type_hints(PreparedDatasetProps.__init__)
            check_type(argname="argument date_time_column_to_filter", value=date_time_column_to_filter, expected_type=type_hints["date_time_column_to_filter"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument manifest_location", value=manifest_location, expected_type=type_hints["manifest_location"])
            check_type(argname="argument date_time_columns_to_adjust", value=date_time_columns_to_adjust, expected_type=type_hints["date_time_columns_to_adjust"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument start_datetime", value=start_datetime, expected_type=type_hints["start_datetime"])
        self._values: typing.Dict[str, typing.Any] = {
            "date_time_column_to_filter": date_time_column_to_filter,
            "location": location,
            "manifest_location": manifest_location,
        }
        if date_time_columns_to_adjust is not None:
            self._values["date_time_columns_to_adjust"] = date_time_columns_to_adjust
        if offset is not None:
            self._values["offset"] = offset
        if start_datetime is not None:
            self._values["start_datetime"] = start_datetime

    @builtins.property
    def date_time_column_to_filter(self) -> builtins.str:
        '''(experimental) Datetime column for filtering data.

        :stability: experimental
        '''
        result = self._values.get("date_time_column_to_filter")
        assert result is not None, "Required property 'date_time_column_to_filter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> aws_cdk.aws_s3.Location:
        '''(experimental) The Amazon S3 Location of the source dataset.

        It's composed of an Amazon S3 bucketName and an Amazon S3 objectKey

        :stability: experimental
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(aws_cdk.aws_s3.Location, result)

    @builtins.property
    def manifest_location(self) -> aws_cdk.aws_s3.Location:
        '''(experimental) Manifest file in csv format with two columns: start, path.

        :stability: experimental
        '''
        result = self._values.get("manifest_location")
        assert result is not None, "Required property 'manifest_location' is missing"
        return typing.cast(aws_cdk.aws_s3.Location, result)

    @builtins.property
    def date_time_columns_to_adjust(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Array of column names with datetime to adjust.

        The source data will have date in the past 2021-01-01T00:00:00 while
        the data replayer will have have the current time. The difference (aka. offset)
        must be added to all datetime columns

        :stability: experimental
        '''
        result = self._values.get("date_time_columns_to_adjust")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def offset(self) -> typing.Optional[builtins.str]:
        '''(experimental) The offset in seconds for replaying data.

        It is the difference between the ``startDatetime`` and now.

        :default: - Calculate the offset from startDatetime parameter during CDK deployment

        :stability: experimental
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_datetime(self) -> typing.Optional[builtins.str]:
        '''(experimental) The minimum datetime value in the dataset used to calculate time offset.

        :default: - The offset parameter is used.

        :stability: experimental
        '''
        result = self._values.get("start_datetime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PreparedDatasetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3CrossAccount(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.S3CrossAccount",
):
    '''(experimental) This CDK construct grants cross account permissions on an Amazon S3 location.

    It uses a bucket policy and an Amazon KMS Key policy if the bucket is encrypted with KMS.
    The cross account permission is granted to the entire account and not to a specific principal in this account.
    It's the responsibility of the target account to grant permissions to the relevant principals.

    Note that it uses a Bucket object and not an IBucket because CDK can only add policies to objects managed in the CDK stack.

    Usage example::

       import * as cdk from 'aws-cdk-lib';
       import { S3CrossAccount } from 'aws-analytics-reference-architecture';

       const exampleApp = new cdk.App();
       const stack = new cdk.Stack(exampleApp, 'S3CrossAccountStack');

       const myBucket = new Bucket(stack, 'MyBucket')

       new S3CrossAccount(stack, 'S3CrossAccountGrant', {
          bucket: myBucket,
          s3ObjectKey: 'my-data',
          accountId: '1234567891011',
       });

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        account_id: builtins.str,
        s3_bucket: aws_cdk.aws_s3.Bucket,
        s3_object_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account_id: (experimental) The account ID to grant on the S3 location.
        :param s3_bucket: (experimental) The S3 Bucket object to grant cross account access. This needs to be a Bucket object and not an IBucket because the construct modifies the Bucket policy
        :param s3_object_key: (experimental) The S3 object key to grant cross account access (S3 prefix without the bucket name). Default: - Grant cross account for the entire bucket

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3CrossAccount.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3CrossAccountProps(
            account_id=account_id, s3_bucket=s3_bucket, s3_object_key=s3_object_key
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.S3CrossAccountProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "s3_bucket": "s3Bucket",
        "s3_object_key": "s3ObjectKey",
    },
)
class S3CrossAccountProps:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        s3_bucket: aws_cdk.aws_s3.Bucket,
        s3_object_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The props for S3CrossAccount construct.

        :param account_id: (experimental) The account ID to grant on the S3 location.
        :param s3_bucket: (experimental) The S3 Bucket object to grant cross account access. This needs to be a Bucket object and not an IBucket because the construct modifies the Bucket policy
        :param s3_object_key: (experimental) The S3 object key to grant cross account access (S3 prefix without the bucket name). Default: - Grant cross account for the entire bucket

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(S3CrossAccountProps.__init__)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "account_id": account_id,
            "s3_bucket": s3_bucket,
        }
        if s3_object_key is not None:
            self._values["s3_object_key"] = s3_object_key

    @builtins.property
    def account_id(self) -> builtins.str:
        '''(experimental) The account ID to grant on the S3 location.

        :stability: experimental
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''(experimental) The S3 Bucket object to grant cross account access.

        This needs to be a Bucket object and not an IBucket because the construct modifies the Bucket policy

        :stability: experimental
        '''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.Bucket, result)

    @builtins.property
    def s3_object_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The S3 object key to grant cross account access (S3 prefix without the bucket name).

        :default: - Grant cross account for the entire bucket

        :stability: experimental
        '''
        result = self._values.get("s3_object_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3CrossAccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-analytics-reference-architecture.SSOIdentityType")
class SSOIdentityType(enum.Enum):
    '''(experimental) Enum to define the type of identity Type in EMR studio.

    :stability: experimental
    '''

    USER = "USER"
    '''
    :stability: experimental
    '''
    GROUP = "GROUP"
    '''
    :stability: experimental
    '''


class SingletonCfnLaunchTemplate(
    aws_cdk.aws_ec2.CfnLaunchTemplate,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.SingletonCfnLaunchTemplate",
):
    '''(experimental) An Amazon S3 Bucket implementing the singleton pattern.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        launch_template_data: typing.Union[typing.Union[aws_cdk.aws_ec2.CfnLaunchTemplate.LaunchTemplateDataProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable],
        launch_template_name: typing.Optional[builtins.str] = None,
        tag_specifications: typing.Optional[typing.Union[aws_cdk.IResolvable, typing.Sequence[typing.Union[typing.Union[aws_cdk.aws_ec2.CfnLaunchTemplate.LaunchTemplateTagSpecificationProperty, typing.Dict[str, typing.Any]], aws_cdk.IResolvable]]]] = None,
    ) -> None:
        '''Create a new ``AWS::EC2::LaunchTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param launch_template_data: The information for the launch template.
        :param launch_template_name: A name for the launch template.
        :param tag_specifications: The tags to apply to the launch template during creation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SingletonCfnLaunchTemplate.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.aws_ec2.CfnLaunchTemplateProps(
            launch_template_data=launch_template_data,
            launch_template_name=launch_template_name,
            tag_specifications=tag_specifications,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getOrCreate")
    @builtins.classmethod
    def get_or_create(
        cls,
        scope: constructs.Construct,
        name: builtins.str,
        data: builtins.str,
    ) -> aws_cdk.aws_ec2.CfnLaunchTemplate:
        '''
        :param scope: -
        :param name: -
        :param data: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SingletonCfnLaunchTemplate.get_or_create)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(aws_cdk.aws_ec2.CfnLaunchTemplate, jsii.sinvoke(cls, "getOrCreate", [scope, name, data]))


class SingletonGlueDatabase(
    aws_cdk.aws_glue_alpha.Database,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.SingletonGlueDatabase",
):
    '''(experimental) AWS Glue Database implementing the singleton pattern.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        database_name: builtins.str,
        location_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param database_name: (experimental) The name of the database.
        :param location_uri: (experimental) The location of the database (for example, an HDFS path). Default: undefined. This field is optional in AWS::Glue::Database DatabaseInput

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SingletonGlueDatabase.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.aws_glue_alpha.DatabaseProps(
            database_name=database_name, location_uri=location_uri
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getOrCreate")
    @builtins.classmethod
    def get_or_create(
        cls,
        scope: constructs.Construct,
        name: builtins.str,
    ) -> aws_cdk.aws_glue_alpha.Database:
        '''
        :param scope: -
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SingletonGlueDatabase.get_or_create)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(aws_cdk.aws_glue_alpha.Database, jsii.sinvoke(cls, "getOrCreate", [scope, name]))


class SingletonKey(
    aws_cdk.aws_kms.Key,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.SingletonKey",
):
    '''(experimental) An Amazon S3 Bucket implementing the singleton pattern.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        admins: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IPrincipal]] = None,
        alias: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        key_spec: typing.Optional[aws_cdk.aws_kms.KeySpec] = None,
        key_usage: typing.Optional[aws_cdk.aws_kms.KeyUsage] = None,
        pending_window: typing.Optional[aws_cdk.Duration] = None,
        policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param admins: A list of principals to add as key administrators to the key policy. Key administrators have permissions to manage the key (e.g., change permissions, revoke), but do not have permissions to use the key in cryptographic operations (e.g., encrypt, decrypt). These principals will be added to the default key policy (if none specified), or to the specified policy (if provided). Default: []
        :param alias: Initial alias to add to the key. More aliases can be added later by calling ``addAlias``. Default: - No alias is added for the key.
        :param description: A description of the key. Use a description that helps your users decide whether the key is appropriate for a particular task. Default: - No description.
        :param enabled: Indicates whether the key is available for use. Default: - Key is enabled.
        :param enable_key_rotation: Indicates whether AWS KMS rotates the key. Default: false
        :param key_spec: The cryptographic configuration of the key. The valid value depends on usage of the key. IMPORTANT: If you change this property of an existing key, the existing key is scheduled for deletion and a new key is created with the specified value. Default: KeySpec.SYMMETRIC_DEFAULT
        :param key_usage: The cryptographic operations for which the key can be used. IMPORTANT: If you change this property of an existing key, the existing key is scheduled for deletion and a new key is created with the specified value. Default: KeyUsage.ENCRYPT_DECRYPT
        :param pending_window: Specifies the number of days in the waiting period before AWS KMS deletes a CMK that has been removed from a CloudFormation stack. When you remove a customer master key (CMK) from a CloudFormation stack, AWS KMS schedules the CMK for deletion and starts the mandatory waiting period. The PendingWindowInDays property determines the length of waiting period. During the waiting period, the key state of CMK is Pending Deletion, which prevents the CMK from being used in cryptographic operations. When the waiting period expires, AWS KMS permanently deletes the CMK. Enter a value between 7 and 30 days. Default: - 30 days
        :param policy: Custom policy document to attach to the KMS key. NOTE - If the ``@aws-cdk/aws-kms:defaultKeyPolicies`` feature flag is set (the default for new projects), this policy will *override* the default key policy and become the only key policy for the key. If the feature flag is not set, this policy will be appended to the default key policy. Default: - A policy document with permissions for the account root to administer the key will be created.
        :param removal_policy: Whether the encryption key should be retained when it is removed from the Stack. This is useful when one wants to retain access to data that was encrypted with a key that is being retired. Default: RemovalPolicy.Retain
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SingletonKey.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.aws_kms.KeyProps(
            admins=admins,
            alias=alias,
            description=description,
            enabled=enabled,
            enable_key_rotation=enable_key_rotation,
            key_spec=key_spec,
            key_usage=key_usage,
            pending_window=pending_window,
            policy=policy,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getOrCreate")
    @builtins.classmethod
    def get_or_create(
        cls,
        scope: constructs.Construct,
        key_name: builtins.str,
    ) -> aws_cdk.aws_kms.Key:
        '''(experimental) Get the Amazon KMS Key the AWS CDK Stack based on the provided name.

        If no key exists, it creates a new one.

        :param scope: -
        :param key_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SingletonKey.get_or_create)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
        return typing.cast(aws_cdk.aws_kms.Key, jsii.sinvoke(cls, "getOrCreate", [scope, key_name]))


@jsii.enum(jsii_type="aws-analytics-reference-architecture.StudioAuthMode")
class StudioAuthMode(enum.Enum):
    '''(experimental) Enum to define authentication mode for Amazon EMR Studio.

    :stability: experimental
    '''

    IAM = "IAM"
    '''
    :stability: experimental
    '''
    SSO = "SSO"
    '''
    :stability: experimental
    '''


class SynchronousAthenaQuery(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.SynchronousAthenaQuery",
):
    '''(experimental) Execute an Amazon Athena query synchronously during CDK deployment.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        result_path: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        statement: builtins.str,
        execution_role_statements: typing.Optional[typing.Sequence[aws_cdk.aws_iam.PolicyStatement]] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the SynchronousAthenaQuery class.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param result_path: (experimental) The Amazon S3 Location for the query results (without trailing slash).
        :param statement: (experimental) The name of the Athena query to execute.
        :param execution_role_statements: (experimental) The Amazon IAM Policy Statements used to run the query. Default: - No Policy Statements are added to the execution role
        :param timeout: (experimental) The timeout in seconds to wait for query success. Default: - 60 seconds

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SynchronousAthenaQuery.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SynchronousAthenaQueryProps(
            result_path=result_path,
            statement=statement,
            execution_role_statements=execution_role_statements,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.SynchronousAthenaQueryProps",
    jsii_struct_bases=[],
    name_mapping={
        "result_path": "resultPath",
        "statement": "statement",
        "execution_role_statements": "executionRoleStatements",
        "timeout": "timeout",
    },
)
class SynchronousAthenaQueryProps:
    def __init__(
        self,
        *,
        result_path: typing.Union[aws_cdk.aws_s3.Location, typing.Dict[str, typing.Any]],
        statement: builtins.str,
        execution_role_statements: typing.Optional[typing.Sequence[aws_cdk.aws_iam.PolicyStatement]] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The properties for the SynchronousAthenaQuery construct.

        :param result_path: (experimental) The Amazon S3 Location for the query results (without trailing slash).
        :param statement: (experimental) The name of the Athena query to execute.
        :param execution_role_statements: (experimental) The Amazon IAM Policy Statements used to run the query. Default: - No Policy Statements are added to the execution role
        :param timeout: (experimental) The timeout in seconds to wait for query success. Default: - 60 seconds

        :stability: experimental
        '''
        if isinstance(result_path, dict):
            result_path = Location(**result_path)
        if __debug__:
            type_hints = typing.get_type_hints(SynchronousAthenaQueryProps.__init__)
            check_type(argname="argument result_path", value=result_path, expected_type=type_hints["result_path"])
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            check_type(argname="argument execution_role_statements", value=execution_role_statements, expected_type=type_hints["execution_role_statements"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[str, typing.Any] = {
            "result_path": result_path,
            "statement": statement,
        }
        if execution_role_statements is not None:
            self._values["execution_role_statements"] = execution_role_statements
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def result_path(self) -> aws_cdk.aws_s3.Location:
        '''(experimental) The Amazon S3 Location for the query results (without trailing slash).

        :stability: experimental
        '''
        result = self._values.get("result_path")
        assert result is not None, "Required property 'result_path' is missing"
        return typing.cast(aws_cdk.aws_s3.Location, result)

    @builtins.property
    def statement(self) -> builtins.str:
        '''(experimental) The name of the Athena query to execute.

        :stability: experimental
        '''
        result = self._values.get("statement")
        assert result is not None, "Required property 'statement' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_role_statements(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        '''(experimental) The Amazon IAM Policy Statements used to run the query.

        :default: - No Policy Statements are added to the execution role

        :stability: experimental
        '''
        result = self._values.get("execution_role_statements")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The timeout in seconds to wait for query success.

        :default: - 60 seconds

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynchronousAthenaQueryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynchronousCrawler(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.SynchronousCrawler",
):
    '''(experimental) CrawlerStartWait Construct to start an AWS Glue Crawler execution and asynchronously wait for completion.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        crawler_name: builtins.str,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the DataGenerator class.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param crawler_name: (experimental) The name of the Crawler to use.
        :param timeout: (experimental) The timeout in seconds to wait for the Crawler success. Default: - 300 seconds

        :stability: experimental
        :access: public
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SynchronousCrawler.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SynchronousCrawlerProps(crawler_name=crawler_name, timeout=timeout)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.SynchronousCrawlerProps",
    jsii_struct_bases=[],
    name_mapping={"crawler_name": "crawlerName", "timeout": "timeout"},
)
class SynchronousCrawlerProps:
    def __init__(
        self,
        *,
        crawler_name: builtins.str,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The properties for SynchronousCrawler Construct.

        :param crawler_name: (experimental) The name of the Crawler to use.
        :param timeout: (experimental) The timeout in seconds to wait for the Crawler success. Default: - 300 seconds

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SynchronousCrawlerProps.__init__)
            check_type(argname="argument crawler_name", value=crawler_name, expected_type=type_hints["crawler_name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[str, typing.Any] = {
            "crawler_name": crawler_name,
        }
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def crawler_name(self) -> builtins.str:
        '''(experimental) The name of the Crawler to use.

        :stability: experimental
        '''
        result = self._values.get("crawler_name")
        assert result is not None, "Required property 'crawler_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The timeout in seconds to wait for the Crawler success.

        :default: - 300 seconds

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynchronousCrawlerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynchronousGlueJob(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.SynchronousGlueJob",
):
    '''(experimental) SynchronousGlueJob Construct to start an AWS Glue Job execution and wait for completion during CDK deploy.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        executable: aws_cdk.aws_glue_alpha.JobExecutable,
        connections: typing.Optional[typing.Sequence[aws_cdk.aws_glue_alpha.IConnection]] = None,
        continuous_logging: typing.Optional[typing.Union[aws_cdk.aws_glue_alpha.ContinuousLoggingProps, typing.Dict[str, typing.Any]]] = None,
        default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_profiling_metrics: typing.Optional[builtins.bool] = None,
        job_name: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        notify_delay_after: typing.Optional[aws_cdk.Duration] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_configuration: typing.Optional[aws_cdk.aws_glue_alpha.ISecurityConfiguration] = None,
        spark_ui: typing.Optional[typing.Union[aws_cdk.aws_glue_alpha.SparkUIProps, typing.Dict[str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        worker_count: typing.Optional[jsii.Number] = None,
        worker_type: typing.Optional[aws_cdk.aws_glue_alpha.WorkerType] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the DataGenerator class.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param executable: (experimental) The job's executable properties.
        :param connections: (experimental) The {@link Connection}s used for this job. Connections are used to connect to other AWS Service or resources within a VPC. Default: [] - no connections are added to the job
        :param continuous_logging: (experimental) Enables continuous logging with the specified props. Default: - continuous logging is disabled.
        :param default_arguments: (experimental) The default arguments for this job, specified as name-value pairs. Default: - no arguments
        :param description: (experimental) The description of the job. Default: - no value
        :param enable_profiling_metrics: (experimental) Enables the collection of metrics for job profiling. Default: - no profiling metrics emitted.
        :param job_name: (experimental) The name of the job. Default: - a name is automatically generated
        :param max_capacity: (experimental) The number of AWS Glue data processing units (DPUs) that can be allocated when this job runs. Cannot be used for Glue version 2.0 and later - workerType and workerCount should be used instead. Default: - 10 when job type is Apache Spark ETL or streaming, 0.0625 when job type is Python shell
        :param max_concurrent_runs: (experimental) The maximum number of concurrent runs allowed for the job. An error is returned when this threshold is reached. The maximum value you can specify is controlled by a service limit. Default: 1
        :param max_retries: (experimental) The maximum number of times to retry this job after a job run fails. Default: 0
        :param notify_delay_after: (experimental) The number of minutes to wait after a job run starts, before sending a job run delay notification. Default: - no delay notifications
        :param role: (experimental) The IAM role assumed by Glue to run this job. If providing a custom role, it needs to trust the Glue service principal (glue.amazonaws.com) and be granted sufficient permissions. Default: - a role is automatically generated
        :param security_configuration: (experimental) The {@link SecurityConfiguration} to use for this job. Default: - no security configuration.
        :param spark_ui: (experimental) Enables the Spark UI debugging and monitoring with the specified props. Default: - Spark UI debugging and monitoring is disabled.
        :param tags: (experimental) The tags to add to the resources on which the job runs. Default: {} - no tags
        :param timeout: (experimental) The maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. Default: cdk.Duration.hours(48)
        :param worker_count: (experimental) The number of workers of a defined {@link WorkerType} that are allocated when a job runs. Default: - differs based on specific Glue version/worker type
        :param worker_type: (experimental) The type of predefined worker that is allocated when a job runs. Default: - differs based on specific Glue version

        :stability: experimental
        :access: public
        '''
        if __debug__:
            type_hints = typing.get_type_hints(SynchronousGlueJob.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = aws_cdk.aws_glue_alpha.JobProps(
            executable=executable,
            connections=connections,
            continuous_logging=continuous_logging,
            default_arguments=default_arguments,
            description=description,
            enable_profiling_metrics=enable_profiling_metrics,
            job_name=job_name,
            max_capacity=max_capacity,
            max_concurrent_runs=max_concurrent_runs,
            max_retries=max_retries,
            notify_delay_after=notify_delay_after,
            role=role,
            security_configuration=security_configuration,
            spark_ui=spark_ui,
            tags=tags,
            timeout=timeout,
            worker_count=worker_count,
            worker_type=worker_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="glueJobLogStream")
    def glue_job_log_stream(self) -> builtins.str:
        '''(experimental) The Glue job logstream to check potential errors.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "glueJobLogStream"))


class TrackedConstruct(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.TrackedConstruct",
):
    '''(experimental) A type of CDK Construct that is tracked via a unique code in Stack labels.

    It is  used to measure the number of deployments and so the impact of the Analytics Reference Architecture.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        tracking_code: builtins.str,
    ) -> None:
        '''(experimental) Constructs a new instance of the TrackedConstruct.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param tracking_code: (experimental) Unique code used to measure the number of the CloudFormation deployments.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TrackedConstruct.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TrackedConstructProps(tracking_code=tracking_code)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-analytics-reference-architecture.TrackedConstructProps",
    jsii_struct_bases=[],
    name_mapping={"tracking_code": "trackingCode"},
)
class TrackedConstructProps:
    def __init__(self, *, tracking_code: builtins.str) -> None:
        '''(experimental) The properties for the TrackedConstructProps construct.

        :param tracking_code: (experimental) Unique code used to measure the number of the CloudFormation deployments.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TrackedConstructProps.__init__)
            check_type(argname="argument tracking_code", value=tracking_code, expected_type=type_hints["tracking_code"])
        self._values: typing.Dict[str, typing.Any] = {
            "tracking_code": tracking_code,
        }

    @builtins.property
    def tracking_code(self) -> builtins.str:
        '''(experimental) Unique code used to measure the number of the CloudFormation deployments.

        :stability: experimental
        '''
        result = self._values.get("tracking_code")
        assert result is not None, "Required property 'tracking_code' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrackedConstructProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLakeCatalog(
    TrackedConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.DataLakeCatalog",
):
    '''(experimental) A Data Lake Catalog composed of 3 AWS Glue Database configured with AWS best practices:   Databases for Raw/Cleaned/Transformed data,.

    :stability: experimental
    '''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''(experimental) Construct a new instance of DataLakeCatalog based on S3 buckets with best practices configuration.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.

        :stability: experimental
        :access: public
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataLakeCatalog.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="cleanDatabase")
    def clean_database(self) -> aws_cdk.aws_glue_alpha.Database:
        '''(experimental) AWS Glue Database for Clean data.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_glue_alpha.Database, jsii.get(self, "cleanDatabase"))

    @builtins.property
    @jsii.member(jsii_name="rawDatabase")
    def raw_database(self) -> aws_cdk.aws_glue_alpha.Database:
        '''(experimental) AWS Glue Database for Raw data.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_glue_alpha.Database, jsii.get(self, "rawDatabase"))

    @builtins.property
    @jsii.member(jsii_name="transformDatabase")
    def transform_database(self) -> aws_cdk.aws_glue_alpha.Database:
        '''(experimental) AWS Glue Database for Transform data.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_glue_alpha.Database, jsii.get(self, "transformDatabase"))


class DataLakeExporter(
    TrackedConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.DataLakeExporter",
):
    '''(experimental) DataLakeExporter Construct to export data from a stream to the data lake.

    Source can be an Amazon Kinesis Data Stream.
    Target can be an Amazon S3 bucket.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        sink_bucket: aws_cdk.aws_s3.Bucket,
        source_glue_database: aws_cdk.aws_glue_alpha.Database,
        source_glue_table: aws_cdk.aws_glue_alpha.Table,
        source_kinesis_data_stream: aws_cdk.aws_kinesis.Stream,
        delivery_interval: typing.Optional[jsii.Number] = None,
        delivery_size: typing.Optional[jsii.Number] = None,
        sink_object_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param sink_bucket: (experimental) Amazon S3 sink Bucket where the data lake exporter write data.
        :param source_glue_database: (experimental) Source AWS Glue Database containing the schema of the stream.
        :param source_glue_table: (experimental) Source AWS Glue Table containing the schema of the stream.
        :param source_kinesis_data_stream: (experimental) Source must be an Amazon Kinesis Data Stream.
        :param delivery_interval: (experimental) Delivery interval in seconds. The frequency of the data delivery is defined by this interval. Default: - Set to 900 seconds
        :param delivery_size: (experimental) Maximum delivery size in MB. The frequency of the data delivery is defined by this maximum delivery size. Default: - Set to 128 MB
        :param sink_object_key: (experimental) Amazon S3 sink object key where the data lake exporter write data. Default: - The data is written at the bucket root

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataLakeExporter.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLakeExporterProps(
            sink_bucket=sink_bucket,
            source_glue_database=source_glue_database,
            source_glue_table=source_glue_table,
            source_kinesis_data_stream=source_kinesis_data_stream,
            delivery_interval=delivery_interval,
            delivery_size=delivery_size,
            sink_object_key=sink_object_key,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cfnIngestionStream")
    def cfn_ingestion_stream(self) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream:
        '''(experimental) Constructs a new instance of the DataLakeExporter class.

        :stability: experimental
        :access: public
        '''
        return typing.cast(aws_cdk.aws_kinesisfirehose.CfnDeliveryStream, jsii.get(self, "cfnIngestionStream"))


class DataLakeStorage(
    TrackedConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.DataLakeStorage",
):
    '''(experimental) A CDK Construct that creates the storage layers of a data lake composed of Amazon S3 Buckets.

    This construct is based on 3 Amazon S3 buckets configured with AWS best practices:

    - S3 buckets for Raw/Cleaned/Transformed data,
    - data lifecycle optimization/transitioning to different Amazon S3 storage classes
    - server side buckets encryption managed by KMS customer key
    - Default single KMS key
    - SSL communication enforcement
    - access logged to an S3 bucket
    - All public access blocked

    By default the transitioning rules to Amazon S3 storage classes are configured as following:

    - Raw data is moved to Infrequent Access after 30 days and archived to Glacier after 90 days
    - Clean and Transformed data is moved to Infrequent Access after 90 days and is not archived

    Objects and buckets are automatically deleted when the CDK application is detroyed.

    For custom requirements, consider using {@link AraBucket}.

    Usage example::

       import * as cdk from 'aws-cdk-lib';
       import { DataLakeStorage } from 'aws-analytics-reference-architecture';

       const exampleApp = new cdk.App();
       const stack = new cdk.Stack(exampleApp, 'DataLakeStorageStack');

       new DataLakeStorage(stack, 'MyDataLakeStorage', {
         rawInfrequentAccessDelay: 90,
         rawArchiveDelay: 180,
         cleanInfrequentAccessDelay: 180,
         cleanArchiveDelay: 360,
         transformInfrequentAccessDelay: 180,
         transformArchiveDelay: 360,
       });

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        clean_archive_delay: typing.Optional[jsii.Number] = None,
        clean_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        raw_archive_delay: typing.Optional[jsii.Number] = None,
        raw_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        transform_archive_delay: typing.Optional[jsii.Number] = None,
        transform_infrequent_access_delay: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Construct a new instance of DataLakeStorage based on Amazon S3 buckets with best practices configuration.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param clean_archive_delay: (experimental) Delay (in days) before archiving CLEAN data to frozen storage (Glacier storage class). Default: - Objects are not archived to Glacier
        :param clean_infrequent_access_delay: (experimental) Delay (in days) before moving CLEAN data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 90 days
        :param raw_archive_delay: (experimental) Delay (in days) before archiving RAW data to frozen storage (Glacier storage class). Default: - Move objects to Glacier after 90 days
        :param raw_infrequent_access_delay: (experimental) Delay (in days) before moving RAW data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 30 days
        :param transform_archive_delay: (experimental) Delay (in days) before archiving TRANSFORM data to frozen storage (Glacier storage class). Default: - Objects are not archived to Glacier
        :param transform_infrequent_access_delay: (experimental) Delay (in days) before moving TRANSFORM data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 90 days

        :stability: experimental
        :access: public
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DataLakeStorage.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLakeStorageProps(
            clean_archive_delay=clean_archive_delay,
            clean_infrequent_access_delay=clean_infrequent_access_delay,
            raw_archive_delay=raw_archive_delay,
            raw_infrequent_access_delay=raw_infrequent_access_delay,
            transform_archive_delay=transform_archive_delay,
            transform_infrequent_access_delay=transform_infrequent_access_delay,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cleanBucket")
    def clean_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "cleanBucket"))

    @builtins.property
    @jsii.member(jsii_name="rawBucket")
    def raw_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "rawBucket"))

    @builtins.property
    @jsii.member(jsii_name="transformBucket")
    def transform_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "transformBucket"))


class EmrEksCluster(
    TrackedConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.EmrEksCluster",
):
    '''(experimental) EmrEksCluster Construct packaging all the resources and configuration required to run Amazon EMR on EKS.

    It deploys:

    - An EKS cluster (VPC configuration can be customized)
    - A tooling nodegroup to run tools including the Kubedashboard and the Cluster Autoscaler
    - Optionally multiple nodegroups (one per AZ) for critical/shared/notebook EMR workloads
    - Additional nodegroups can be configured

    The construct will upload on S3 the Pod templates required to run EMR jobs on the default nodegroups.
    It will also parse and store the configuration of EMR on EKS jobs for each default nodegroup in object parameters

    Methods are available to add EMR Virtual Clusters to the EKS cluster and to create execution roles for the virtual clusters.

    Usage example::

       const emrEks: EmrEksCluster = EmrEksCluster.getOrCreate(stack, {
          eksAdminRoleArn: <ROLE_ARN>,
          eksClusterName: <CLUSTER_NAME>,
       });

       const virtualCluster = emrEks.addEmrVirtualCluster(stack, {
          name: <Virtual_Cluster_Name>,
          createNamespace: <TRUE OR FALSE>,
          eksNamespace: <K8S_namespace>,
       });

       const role = emrEks.createExecutionRole(stack, 'ExecRole',{
          policy: <POLICY>,
       })

       // EMR on EKS virtual cluster ID
       cdk.CfnOutput(self, 'VirtualClusterId',value = virtualCluster.attr_id)
       // Job config for each nodegroup
       cdk.CfnOutput(self, "CriticalConfig", value = emrEks.criticalDefaultConfig)
       cdk.CfnOutput(self, "SharedConfig", value = emrEks.sharedDefaultConfig)
       // Execution role arn
       cdk.CfnOutput(self,'ExecRoleArn', value = role.roleArn)

    :stability: experimental
    '''

    @jsii.member(jsii_name="getOrCreate")
    @builtins.classmethod
    def get_or_create(
        cls,
        scope: constructs.Construct,
        *,
        eks_admin_role_arn: builtins.str,
        autoscaler_version: typing.Optional[jsii.Number] = None,
        default_node_groups: typing.Optional[builtins.bool] = None,
        eks_cluster_name: typing.Optional[builtins.str] = None,
        eks_vpc_attributes: typing.Optional[typing.Union[aws_cdk.aws_ec2.VpcAttributes, typing.Dict[str, typing.Any]]] = None,
        emr_eks_nodegroups: typing.Optional[typing.Sequence[EmrEksNodegroup]] = None,
        kubernetes_version: typing.Optional[aws_cdk.aws_eks.KubernetesVersion] = None,
    ) -> "EmrEksCluster":
        '''(experimental) Get an existing EmrEksCluster based on the cluster name property or create a new one only one EKS cluster can exist per stack.

        :param scope: the CDK scope used to search or create the cluster.
        :param eks_admin_role_arn: (experimental) Amazon IAM Role to be added to Amazon EKS master roles that will give access to kubernetes cluster from AWS console UI.
        :param autoscaler_version: (experimental) The version of autoscaler to pass to Helm. Default: - version matching the default Kubernete version
        :param default_node_groups: (experimental) If set to true construct will create default EKS nodegroups. There are three types of Nodegroup: - Nodegroup for critical jobs which use on-demand instances. - Nodegroup using spot instances for jobs that are not critical and can be preempted if a spot instance is reclaimed - Nodegroup to provide capacity for creating and running managed endpoints spark drivers and executors. Default: - true
        :param eks_cluster_name: (experimental) Name of the Amazon EKS cluster to be created. Default: - The [default cluster name]{@link EmrEksCluster.DEFAULT_CLUSTER_NAME}
        :param eks_vpc_attributes: (experimental) Attributes of the VPC where to deploy the EKS cluster VPC should have at least two private and public subnets in different Availability Zones All private subnets should have the following tags: 'for-use-with-amazon-emr-managed-policies'='true' 'kubernetes.io/role/internal-elb'='1' All public subnets should have the following tag: 'kubernetes.io/role/elb'='1'.
        :param emr_eks_nodegroups: (experimental) List of EmrEksNodegroup to create in the cluster in addition to the default [nodegroups]{@link EmrEksNodegroup}. Default: - Don't create additional nodegroups
        :param kubernetes_version: (experimental) Kubernetes version for Amazon EKS cluster that will be created. Default: - v1.21 version is used

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmrEksCluster.get_or_create)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = EmrEksClusterProps(
            eks_admin_role_arn=eks_admin_role_arn,
            autoscaler_version=autoscaler_version,
            default_node_groups=default_node_groups,
            eks_cluster_name=eks_cluster_name,
            eks_vpc_attributes=eks_vpc_attributes,
            emr_eks_nodegroups=emr_eks_nodegroups,
            kubernetes_version=kubernetes_version,
        )

        return typing.cast("EmrEksCluster", jsii.sinvoke(cls, "getOrCreate", [scope, props]))

    @jsii.member(jsii_name="addEmrEksNodegroup")
    def add_emr_eks_nodegroup(
        self,
        id: builtins.str,
        *,
        mount_nvme: typing.Optional[builtins.bool] = None,
        subnet: typing.Optional[aws_cdk.aws_ec2.ISubnet] = None,
        ami_type: typing.Optional[aws_cdk.aws_eks.NodegroupAmiType] = None,
        capacity_type: typing.Optional[aws_cdk.aws_eks.CapacityType] = None,
        desired_size: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update: typing.Optional[builtins.bool] = None,
        instance_types: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.InstanceType]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_template_spec: typing.Optional[typing.Union[aws_cdk.aws_eks.LaunchTemplateSpec, typing.Dict[str, typing.Any]]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        nodegroup_name: typing.Optional[builtins.str] = None,
        node_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        release_version: typing.Optional[builtins.str] = None,
        remote_access: typing.Optional[typing.Union[aws_cdk.aws_eks.NodegroupRemoteAccess, typing.Dict[str, typing.Any]]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_eks.TaintSpec, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Add new nodegroups to the cluster for Amazon EMR on EKS.

        This method overrides Amazon EKS nodegroup options then create the nodegroup.
        If no subnet is provided, it creates one nodegroup per private subnet in the Amazon EKS Cluster.
        If NVME local storage is used, the user_data is modified.

        :param id: the CDK ID of the resource.
        :param mount_nvme: (experimental) Set to true if using instance types with local NVMe drives to mount them automatically at boot time. Default: false
        :param subnet: (experimental) Configure the Amazon EKS NodeGroup in this subnet. Use this setting for resource dependencies like an Amazon RDS database. The subnet must include the availability zone information because the nodegroup is tagged with the AZ for the K8S Cluster Autoscaler. Default: - One NodeGroup is deployed per cluster AZ
        :param ami_type: The AMI type for your node group. If you explicitly specify the launchTemplate with custom AMI, do not specify this property, or the node group deployment will fail. In other cases, you will need to specify correct amiType for the nodegroup. Default: - auto-determined from the instanceTypes property when launchTemplateSpec property is not specified
        :param capacity_type: The capacity type of the nodegroup. Default: - ON_DEMAND
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_types: The instance types to use for your node group. Default: t3.medium will be used according to the cloudformation document.
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param launch_template_spec: Launch template specification used for the nodegroup. Default: - no launch template
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than or equal to zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None
        :param taints: The Kubernetes taints to be applied to the nodes in the node group when they are created. Default: - None

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmrEksCluster.add_emr_eks_nodegroup)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EmrEksNodegroupOptions(
            mount_nvme=mount_nvme,
            subnet=subnet,
            ami_type=ami_type,
            capacity_type=capacity_type,
            desired_size=desired_size,
            disk_size=disk_size,
            force_update=force_update,
            instance_types=instance_types,
            labels=labels,
            launch_template_spec=launch_template_spec,
            max_size=max_size,
            min_size=min_size,
            nodegroup_name=nodegroup_name,
            node_role=node_role,
            release_version=release_version,
            remote_access=remote_access,
            subnets=subnets,
            tags=tags,
            taints=taints,
        )

        return typing.cast(None, jsii.invoke(self, "addEmrEksNodegroup", [id, props]))

    @jsii.member(jsii_name="addEmrVirtualCluster")
    def add_emr_virtual_cluster(
        self,
        scope: constructs.Construct,
        *,
        name: builtins.str,
        create_namespace: typing.Optional[builtins.bool] = None,
        eks_namespace: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_emrcontainers.CfnVirtualCluster:
        '''(experimental) Add a new Amazon EMR Virtual Cluster linked to Amazon EKS Cluster.

        :param scope: of the stack where virtual cluster is deployed.
        :param name: (experimental) name of the Amazon Emr virtual cluster to be created.
        :param create_namespace: (experimental) creates Amazon EKS namespace. Default: - Do not create the namespace
        :param eks_namespace: (experimental) name of the Amazon EKS namespace to be linked to the Amazon EMR virtual cluster. Default: - Use the default namespace

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmrEksCluster.add_emr_virtual_cluster)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = EmrVirtualClusterOptions(
            name=name, create_namespace=create_namespace, eks_namespace=eks_namespace
        )

        return typing.cast(aws_cdk.aws_emrcontainers.CfnVirtualCluster, jsii.invoke(self, "addEmrVirtualCluster", [scope, options]))

    @jsii.member(jsii_name="addManagedEndpoint")
    def add_managed_endpoint(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        execution_role: aws_cdk.aws_iam.IRole,
        managed_endpoint_name: builtins.str,
        virtual_cluster_id: builtins.str,
        configuration_overrides: typing.Optional[builtins.str] = None,
        emr_on_eks_version: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.CustomResource:
        '''(experimental) Creates a new Amazon EMR managed endpoint to be used with Amazon EMR Virtual Cluster .

        CfnOutput can be customized.

        :param scope: the scope of the stack where managed endpoint is deployed.
        :param id: the CDK id for endpoint.
        :param execution_role: (experimental) The Amazon IAM role used as the execution role, this role must provide access to all the AWS resource a user will interact with These can be S3, DynamoDB, Glue Catalog.
        :param managed_endpoint_name: (experimental) The name of the EMR managed endpoint.
        :param virtual_cluster_id: (experimental) The Id of the Amazon EMR virtual cluster containing the managed endpoint.
        :param configuration_overrides: (experimental) The JSON configuration overrides for Amazon EMR on EKS configuration attached to the managed endpoint. Default: - Configuration related to the [default nodegroup for notebook]{@link EmrEksNodegroup.NOTEBOOK_EXECUTOR}
        :param emr_on_eks_version: (experimental) The Amazon EMR version to use. Default: - The [default Amazon EMR version]{@link EmrEksCluster.DEFAULT_EMR_VERSION}

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmrEksCluster.add_managed_endpoint)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = EmrManagedEndpointOptions(
            execution_role=execution_role,
            managed_endpoint_name=managed_endpoint_name,
            virtual_cluster_id=virtual_cluster_id,
            configuration_overrides=configuration_overrides,
            emr_on_eks_version=emr_on_eks_version,
        )

        return typing.cast(aws_cdk.CustomResource, jsii.invoke(self, "addManagedEndpoint", [scope, id, options]))

    @jsii.member(jsii_name="addNodegroupCapacity")
    def add_nodegroup_capacity(
        self,
        nodegroup_id: builtins.str,
        *,
        mount_nvme: typing.Optional[builtins.bool] = None,
        subnet: typing.Optional[aws_cdk.aws_ec2.ISubnet] = None,
        ami_type: typing.Optional[aws_cdk.aws_eks.NodegroupAmiType] = None,
        capacity_type: typing.Optional[aws_cdk.aws_eks.CapacityType] = None,
        desired_size: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update: typing.Optional[builtins.bool] = None,
        instance_types: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.InstanceType]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_template_spec: typing.Optional[typing.Union[aws_cdk.aws_eks.LaunchTemplateSpec, typing.Dict[str, typing.Any]]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        nodegroup_name: typing.Optional[builtins.str] = None,
        node_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        release_version: typing.Optional[builtins.str] = None,
        remote_access: typing.Optional[typing.Union[aws_cdk.aws_eks.NodegroupRemoteAccess, typing.Dict[str, typing.Any]]] = None,
        subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Sequence[typing.Union[aws_cdk.aws_eks.TaintSpec, typing.Dict[str, typing.Any]]]] = None,
    ) -> aws_cdk.aws_eks.Nodegroup:
        '''(experimental) Add a new Amazon EKS Nodegroup to the cluster.

        This method is be used to add a nodegroup to the Amazon EKS cluster and automatically set tags based on labels and taints
        so it can be used for the cluster autoscaler.

        :param nodegroup_id: the ID of the nodegroup.
        :param mount_nvme: (experimental) Set to true if using instance types with local NVMe drives to mount them automatically at boot time. Default: false
        :param subnet: (experimental) Configure the Amazon EKS NodeGroup in this subnet. Use this setting for resource dependencies like an Amazon RDS database. The subnet must include the availability zone information because the nodegroup is tagged with the AZ for the K8S Cluster Autoscaler. Default: - One NodeGroup is deployed per cluster AZ
        :param ami_type: The AMI type for your node group. If you explicitly specify the launchTemplate with custom AMI, do not specify this property, or the node group deployment will fail. In other cases, you will need to specify correct amiType for the nodegroup. Default: - auto-determined from the instanceTypes property when launchTemplateSpec property is not specified
        :param capacity_type: The capacity type of the nodegroup. Default: - ON_DEMAND
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_types: The instance types to use for your node group. Default: t3.medium will be used according to the cloudformation document.
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param launch_template_spec: Launch template specification used for the nodegroup. Default: - no launch template
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than or equal to zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None
        :param taints: The Kubernetes taints to be applied to the nodes in the node group when they are created. Default: - None

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmrEksCluster.add_nodegroup_capacity)
            check_type(argname="argument nodegroup_id", value=nodegroup_id, expected_type=type_hints["nodegroup_id"])
        options = EmrEksNodegroupOptions(
            mount_nvme=mount_nvme,
            subnet=subnet,
            ami_type=ami_type,
            capacity_type=capacity_type,
            desired_size=desired_size,
            disk_size=disk_size,
            force_update=force_update,
            instance_types=instance_types,
            labels=labels,
            launch_template_spec=launch_template_spec,
            max_size=max_size,
            min_size=min_size,
            nodegroup_name=nodegroup_name,
            node_role=node_role,
            release_version=release_version,
            remote_access=remote_access,
            subnets=subnets,
            tags=tags,
            taints=taints,
        )

        return typing.cast(aws_cdk.aws_eks.Nodegroup, jsii.invoke(self, "addNodegroupCapacity", [nodegroup_id, options]))

    @jsii.member(jsii_name="createExecutionRole")
    def create_execution_role(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        policy: aws_cdk.aws_iam.IManagedPolicy,
        namespace: builtins.str,
        name: builtins.str,
    ) -> aws_cdk.aws_iam.Role:
        '''(experimental) Create and configure a new Amazon IAM Role usable as an execution role.

        This method makes the created role assumed by the Amazon EKS cluster Open ID Connect provider.

        :param scope: of the IAM role.
        :param id: of the CDK resource to be created, it should be unique across the stack.
        :param policy: the execution policy to attach to the role.
        :param namespace: The namespace from which the role is going to be used. MUST be the same as the namespace of the Virtual Cluster from which the job is submitted
        :param name: Name to use for the role, required and is used to scope the iam role.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmrEksCluster.create_execution_role)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(aws_cdk.aws_iam.Role, jsii.invoke(self, "createExecutionRole", [scope, id, policy, namespace, name]))

    @jsii.member(jsii_name="uploadPodTemplate")
    def upload_pod_template(self, id: builtins.str, file_path: builtins.str) -> None:
        '''(experimental) Upload podTemplates to the Amazon S3 location used by the cluster.

        :param id: the unique ID of the CDK resource.
        :param file_path: The local path of the yaml podTemplate files to upload.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(EmrEksCluster.upload_pod_template)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(None, jsii.invoke(self, "uploadPodTemplate", [id, file_path]))

    @builtins.property
    @jsii.member(jsii_name="assetBucket")
    def asset_bucket(self) -> aws_cdk.aws_s3.Bucket:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "assetBucket"))

    @builtins.property
    @jsii.member(jsii_name="criticalDefaultConfig")
    def critical_default_config(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "criticalDefaultConfig"))

    @builtins.property
    @jsii.member(jsii_name="eksCluster")
    def eks_cluster(self) -> aws_cdk.aws_eks.Cluster:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_eks.Cluster, jsii.get(self, "eksCluster"))

    @builtins.property
    @jsii.member(jsii_name="notebookDefaultConfig")
    def notebook_default_config(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "notebookDefaultConfig"))

    @builtins.property
    @jsii.member(jsii_name="podTemplateLocation")
    def pod_template_location(self) -> aws_cdk.aws_s3.Location:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_s3.Location, jsii.get(self, "podTemplateLocation"))

    @builtins.property
    @jsii.member(jsii_name="sharedDefaultConfig")
    def shared_default_config(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "sharedDefaultConfig"))


class NotebookPlatform(
    TrackedConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-analytics-reference-architecture.NotebookPlatform",
):
    '''(experimental) A CDK construct to create a notebook infrastructure based on Amazon EMR Studio and assign users to it.

    This construct is initialized through a constructor that takes as argument an interface defined in {@link NotebookPlatformProps}
    The construct has a method to add users {@link addUser} the method take as argument {@link NotebookUserOptions}

    Resources deployed:

    - An S3 Bucket used by EMR Studio to store the Jupyter notebooks
    - A KMS encryption Key used to encrypt an S3 bucket used by EMR Studio to store jupyter notebooks
    - An EMR Studio service Role as defined here, and allowed to access the S3 bucket and KMS key created above
    - An EMR Studio User Role as defined here - The policy template which is leveraged is the Basic one from the Amazon EMR Studio documentation
    - Multiple EMR on EKS Managed Endpoints, each for a user or a group of users
    - An execution role to be passed to the Managed endpoint from a policy provided by the user
    - Multiple Session Policies that are used to map an EMR Studio user or group to a set of resources they are allowed to access. These resources are:

      - EMR Virtual Cluster - created above
      - ManagedEndpoint

    Usage example::

       const emrEks = EmrEksCluster.getOrCreate(stack, {
          eksAdminRoleArn: 'arn:aws:iam::012345678912:role/Admin-Admin',
          eksClusterName: 'cluster',
       });

       const notebookPlatform = new NotebookPlatform(stack, 'platform-notebook', {
          emrEks: emrEks,
          eksNamespace: 'platformns',
          studioName: 'platform',
          studioAuthMode: StudioAuthMode.SSO,
       });

       // If the S3 bucket is encrypted, add policy to the key for the role
       const policy1 = new ManagedPolicy(stack, 'MyPolicy1', {
          statements: [
            new PolicyStatement({
              resources: <BUCKET ARN(s)>,
              actions: ['s3:*'],
            }),
            new PolicyStatement({
              resources: [
                stack.formatArn({
                  account: Aws.ACCOUNT_ID,
                  region: Aws.REGION,
                  service: 'logs',
                  resource: '*',
                  arnFormat: ArnFormat.NO_RESOURCE_NAME,
                }),
              ],
              actions: [
                'logs:*',
              ],
            }),
          ],
       });

       notebookPlatform.addUser([{
          identityName: 'user1',
          identityType: SSOIdentityType.USER,
          notebookManagedEndpoints: [{
            emrOnEksVersion: 'emr-6.4.0-latest',
            executionPolicy: policy1,
          }],
       }]);

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        emr_eks: EmrEksCluster,
        studio_auth_mode: StudioAuthMode,
        studio_name: builtins.str,
        eks_namespace: typing.Optional[builtins.str] = None,
        idp_arn: typing.Optional[builtins.str] = None,
        idp_auth_url: typing.Optional[builtins.str] = None,
        idp_relay_state_parameter_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: the Scope of the AWS CDK Construct.
        :param id: the ID of the AWS CDK Construct.
        :param emr_eks: (experimental) Required the EmrEks infrastructure used for the deployment.
        :param studio_auth_mode: (experimental) Required the authentication mode of Amazon EMR Studio Either 'SSO' or 'IAM' defined in the Enum {@link studioAuthMode}.
        :param studio_name: (experimental) Required the name to be given to the Amazon EMR Studio Must be unique across the AWS account.
        :param eks_namespace: (experimental) the namespace where to deploy the EMR Virtual Cluster. Default: - Use the {@link EmrVirtualClusterOptions} default namespace
        :param idp_arn: (experimental) Used when IAM Authentication is selected with IAM federation with an external identity provider (IdP) for Amazon EMR Studio Value taken from the IAM console in the Identity providers console.
        :param idp_auth_url: (experimental) Used when IAM Authentication is selected with IAM federation with an external identity provider (IdP) for Amazon EMR Studio This is the URL used to sign in the AWS console.
        :param idp_relay_state_parameter_name: (experimental) Used when IAM Authentication is selected with IAM federation with an external identity provider (IdP) for Amazon EMR Studio Value can be set with {@link IdpRelayState} Enum or through a value provided by the user.

        :stability: experimental
        :public: Constructs a new instance of the DataPlatform class
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NotebookPlatform.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NotebookPlatformProps(
            emr_eks=emr_eks,
            studio_auth_mode=studio_auth_mode,
            studio_name=studio_name,
            eks_namespace=eks_namespace,
            idp_arn=idp_arn,
            idp_auth_url=idp_auth_url,
            idp_relay_state_parameter_name=idp_relay_state_parameter_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addUser")
    def add_user(
        self,
        user_list: typing.Sequence[typing.Union[NotebookUserOptions, typing.Dict[str, typing.Any]]],
    ) -> typing.List[builtins.str]:
        '''
        :param user_list: list of users.

        :stability: experimental
        :public:

        Method to add users, take a list of userDefinition and will create a managed endpoints for each user
        and create an IAM Policy scoped to the list managed endpoints
        '''
        if __debug__:
            type_hints = typing.get_type_hints(NotebookPlatform.add_user)
            check_type(argname="argument user_list", value=user_list, expected_type=type_hints["user_list"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "addUser", [user_list]))


__all__ = [
    "AraBucket",
    "AraBucketProps",
    "AthenaDemoSetup",
    "BatchReplayer",
    "BatchReplayerProps",
    "CentralGovernance",
    "CentralGovernanceProps",
    "CustomDataset",
    "CustomDatasetInputFormat",
    "CustomDatasetProps",
    "DataDomain",
    "DataDomainProps",
    "DataLakeCatalog",
    "DataLakeExporter",
    "DataLakeExporterProps",
    "DataLakeStorage",
    "DataLakeStorageProps",
    "Ec2SsmRole",
    "EmrEksCluster",
    "EmrEksClusterProps",
    "EmrEksNodegroup",
    "EmrEksNodegroupOptions",
    "EmrManagedEndpointOptions",
    "EmrVirtualClusterOptions",
    "FlywayRunner",
    "FlywayRunnerProps",
    "GlueDemoRole",
    "LakeFormationAdmin",
    "LakeFormationAdminProps",
    "LakeFormationS3Location",
    "LakeFormationS3LocationProps",
    "LfAccessControlMode",
    "LfTag",
    "NotebookManagedEndpointOptions",
    "NotebookPlatform",
    "NotebookPlatformProps",
    "NotebookUserOptions",
    "PreparedDataset",
    "PreparedDatasetProps",
    "S3CrossAccount",
    "S3CrossAccountProps",
    "SSOIdentityType",
    "SingletonCfnLaunchTemplate",
    "SingletonGlueDatabase",
    "SingletonKey",
    "StudioAuthMode",
    "SynchronousAthenaQuery",
    "SynchronousAthenaQueryProps",
    "SynchronousCrawler",
    "SynchronousCrawlerProps",
    "SynchronousGlueJob",
    "TrackedConstruct",
    "TrackedConstructProps",
]

publication.publish()
