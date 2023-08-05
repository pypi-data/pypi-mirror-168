# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ObjectBucketWebsiteConfigurationArgs', 'ObjectBucketWebsiteConfiguration']

@pulumi.input_type
class ObjectBucketWebsiteConfigurationArgs:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 error_document: Optional[pulumi.Input['ObjectBucketWebsiteConfigurationErrorDocumentArgs']] = None,
                 index_document: Optional[pulumi.Input['ObjectBucketWebsiteConfigurationIndexDocumentArgs']] = None):
        """
        The set of arguments for constructing a ObjectBucketWebsiteConfiguration resource.
        :param pulumi.Input[str] bucket: (Required, Forces new resource) The name of the bucket.
        :param pulumi.Input['ObjectBucketWebsiteConfigurationErrorDocumentArgs'] error_document: (Optional) The name of the error document for the website detailed below.
        :param pulumi.Input['ObjectBucketWebsiteConfigurationIndexDocumentArgs'] index_document: (Optional) The name of the index document for the website detailed below.
        """
        pulumi.set(__self__, "bucket", bucket)
        if error_document is not None:
            pulumi.set(__self__, "error_document", error_document)
        if index_document is not None:
            pulumi.set(__self__, "index_document", index_document)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        (Required, Forces new resource) The name of the bucket.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="errorDocument")
    def error_document(self) -> Optional[pulumi.Input['ObjectBucketWebsiteConfigurationErrorDocumentArgs']]:
        """
        (Optional) The name of the error document for the website detailed below.
        """
        return pulumi.get(self, "error_document")

    @error_document.setter
    def error_document(self, value: Optional[pulumi.Input['ObjectBucketWebsiteConfigurationErrorDocumentArgs']]):
        pulumi.set(self, "error_document", value)

    @property
    @pulumi.getter(name="indexDocument")
    def index_document(self) -> Optional[pulumi.Input['ObjectBucketWebsiteConfigurationIndexDocumentArgs']]:
        """
        (Optional) The name of the index document for the website detailed below.
        """
        return pulumi.get(self, "index_document")

    @index_document.setter
    def index_document(self, value: Optional[pulumi.Input['ObjectBucketWebsiteConfigurationIndexDocumentArgs']]):
        pulumi.set(self, "index_document", value)


@pulumi.input_type
class _ObjectBucketWebsiteConfigurationState:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 error_document: Optional[pulumi.Input['ObjectBucketWebsiteConfigurationErrorDocumentArgs']] = None,
                 index_document: Optional[pulumi.Input['ObjectBucketWebsiteConfigurationIndexDocumentArgs']] = None,
                 website_domain: Optional[pulumi.Input[str]] = None,
                 website_endpoint: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ObjectBucketWebsiteConfiguration resources.
        :param pulumi.Input[str] bucket: (Required, Forces new resource) The name of the bucket.
        :param pulumi.Input['ObjectBucketWebsiteConfigurationErrorDocumentArgs'] error_document: (Optional) The name of the error document for the website detailed below.
        :param pulumi.Input['ObjectBucketWebsiteConfigurationIndexDocumentArgs'] index_document: (Optional) The name of the index document for the website detailed below.
        :param pulumi.Input[str] website_domain: The website endpoint.
        :param pulumi.Input[str] website_endpoint: The domain of the website endpoint.
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if error_document is not None:
            pulumi.set(__self__, "error_document", error_document)
        if index_document is not None:
            pulumi.set(__self__, "index_document", index_document)
        if website_domain is not None:
            pulumi.set(__self__, "website_domain", website_domain)
        if website_endpoint is not None:
            pulumi.set(__self__, "website_endpoint", website_endpoint)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        (Required, Forces new resource) The name of the bucket.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="errorDocument")
    def error_document(self) -> Optional[pulumi.Input['ObjectBucketWebsiteConfigurationErrorDocumentArgs']]:
        """
        (Optional) The name of the error document for the website detailed below.
        """
        return pulumi.get(self, "error_document")

    @error_document.setter
    def error_document(self, value: Optional[pulumi.Input['ObjectBucketWebsiteConfigurationErrorDocumentArgs']]):
        pulumi.set(self, "error_document", value)

    @property
    @pulumi.getter(name="indexDocument")
    def index_document(self) -> Optional[pulumi.Input['ObjectBucketWebsiteConfigurationIndexDocumentArgs']]:
        """
        (Optional) The name of the index document for the website detailed below.
        """
        return pulumi.get(self, "index_document")

    @index_document.setter
    def index_document(self, value: Optional[pulumi.Input['ObjectBucketWebsiteConfigurationIndexDocumentArgs']]):
        pulumi.set(self, "index_document", value)

    @property
    @pulumi.getter(name="websiteDomain")
    def website_domain(self) -> Optional[pulumi.Input[str]]:
        """
        The website endpoint.
        """
        return pulumi.get(self, "website_domain")

    @website_domain.setter
    def website_domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "website_domain", value)

    @property
    @pulumi.getter(name="websiteEndpoint")
    def website_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The domain of the website endpoint.
        """
        return pulumi.get(self, "website_endpoint")

    @website_endpoint.setter
    def website_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "website_endpoint", value)


class ObjectBucketWebsiteConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 error_document: Optional[pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationErrorDocumentArgs']]] = None,
                 index_document: Optional[pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationIndexDocumentArgs']]] = None,
                 __props__=None):
        """
        Provides an Object bucket website configuration resource.
        For more information, see [Hosting Websites on Object bucket](https://www.scaleway.com/en/docs/storage/object/how-to/use-bucket-website/).

        ## Example Usage

        ```python
        import pulumi
        import lbrlabs_pulumi_scaleway as scaleway

        main_object_bucket = scaleway.ObjectBucket("mainObjectBucket", acl="public-read")
        main_object_bucket_website_configuration = scaleway.ObjectBucketWebsiteConfiguration("mainObjectBucketWebsiteConfiguration",
            bucket=main_object_bucket.name,
            index_document=scaleway.ObjectBucketWebsiteConfigurationIndexDocumentArgs(
                suffix="index.html",
            ))
        ```
        ## Example with `policy`

        ```python
        import pulumi
        import json
        import lbrlabs_pulumi_scaleway as scaleway

        main_object_bucket = scaleway.ObjectBucket("mainObjectBucket", acl="public-read")
        main_object_bucket_policy = scaleway.ObjectBucketPolicy("mainObjectBucketPolicy",
            bucket=main_object_bucket.name,
            policy=json.dumps({
                "Version": "2012-10-17",
                "Id": "MyPolicy",
                "Statement": [{
                    "Sid": "GrantToEveryone",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": ["<bucket-name>/*"],
                }],
            }))
        main_object_bucket_website_configuration = scaleway.ObjectBucketWebsiteConfiguration("mainObjectBucketWebsiteConfiguration",
            bucket=main_object_bucket.name,
            index_document=scaleway.ObjectBucketWebsiteConfigurationIndexDocumentArgs(
                suffix="index.html",
            ))
        ```

        ## error_document

        The error_document configuration block supports the following arguments:

        * `key` - (Required) The object key name to use when a 4XX class error occurs.

        ## index_document

        The `index_document` configuration block supports the following arguments:

        * `suffix` - (Required) A suffix that is appended to a request that is for a directory on the website endpoint.

        > **Important:** The suffix must not be empty and must not include a slash character. The routing is not supported.

        In addition to all above arguments, the following attribute is exported:

        * `id` - The bucket and region separated by a slash (/)
        * `website_domain` - The domain of the website endpoint. This is used to create DNS alias [records](https://www.scaleway.com/en/docs/network/dns-cloud/how-to/manage-dns-records).
        * `website_endpoint` - The website endpoint.

        > **Important:** Please check our concepts section to know more about the [endpoint](https://www.scaleway.com/en/docs/storage/object/concepts/#endpoint).

        ## Import

        Website configuration Bucket can be imported using the `{region}/{bucketName}` identifier, e.g. bash

        ```sh
         $ pulumi import scaleway:index/objectBucketWebsiteConfiguration:ObjectBucketWebsiteConfiguration some_bucket fr-par/some-bucket
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: (Required, Forces new resource) The name of the bucket.
        :param pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationErrorDocumentArgs']] error_document: (Optional) The name of the error document for the website detailed below.
        :param pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationIndexDocumentArgs']] index_document: (Optional) The name of the index document for the website detailed below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ObjectBucketWebsiteConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Object bucket website configuration resource.
        For more information, see [Hosting Websites on Object bucket](https://www.scaleway.com/en/docs/storage/object/how-to/use-bucket-website/).

        ## Example Usage

        ```python
        import pulumi
        import lbrlabs_pulumi_scaleway as scaleway

        main_object_bucket = scaleway.ObjectBucket("mainObjectBucket", acl="public-read")
        main_object_bucket_website_configuration = scaleway.ObjectBucketWebsiteConfiguration("mainObjectBucketWebsiteConfiguration",
            bucket=main_object_bucket.name,
            index_document=scaleway.ObjectBucketWebsiteConfigurationIndexDocumentArgs(
                suffix="index.html",
            ))
        ```
        ## Example with `policy`

        ```python
        import pulumi
        import json
        import lbrlabs_pulumi_scaleway as scaleway

        main_object_bucket = scaleway.ObjectBucket("mainObjectBucket", acl="public-read")
        main_object_bucket_policy = scaleway.ObjectBucketPolicy("mainObjectBucketPolicy",
            bucket=main_object_bucket.name,
            policy=json.dumps({
                "Version": "2012-10-17",
                "Id": "MyPolicy",
                "Statement": [{
                    "Sid": "GrantToEveryone",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": ["<bucket-name>/*"],
                }],
            }))
        main_object_bucket_website_configuration = scaleway.ObjectBucketWebsiteConfiguration("mainObjectBucketWebsiteConfiguration",
            bucket=main_object_bucket.name,
            index_document=scaleway.ObjectBucketWebsiteConfigurationIndexDocumentArgs(
                suffix="index.html",
            ))
        ```

        ## error_document

        The error_document configuration block supports the following arguments:

        * `key` - (Required) The object key name to use when a 4XX class error occurs.

        ## index_document

        The `index_document` configuration block supports the following arguments:

        * `suffix` - (Required) A suffix that is appended to a request that is for a directory on the website endpoint.

        > **Important:** The suffix must not be empty and must not include a slash character. The routing is not supported.

        In addition to all above arguments, the following attribute is exported:

        * `id` - The bucket and region separated by a slash (/)
        * `website_domain` - The domain of the website endpoint. This is used to create DNS alias [records](https://www.scaleway.com/en/docs/network/dns-cloud/how-to/manage-dns-records).
        * `website_endpoint` - The website endpoint.

        > **Important:** Please check our concepts section to know more about the [endpoint](https://www.scaleway.com/en/docs/storage/object/concepts/#endpoint).

        ## Import

        Website configuration Bucket can be imported using the `{region}/{bucketName}` identifier, e.g. bash

        ```sh
         $ pulumi import scaleway:index/objectBucketWebsiteConfiguration:ObjectBucketWebsiteConfiguration some_bucket fr-par/some-bucket
        ```

        :param str resource_name: The name of the resource.
        :param ObjectBucketWebsiteConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ObjectBucketWebsiteConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 error_document: Optional[pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationErrorDocumentArgs']]] = None,
                 index_document: Optional[pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationIndexDocumentArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ObjectBucketWebsiteConfigurationArgs.__new__(ObjectBucketWebsiteConfigurationArgs)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            __props__.__dict__["error_document"] = error_document
            __props__.__dict__["index_document"] = index_document
            __props__.__dict__["website_domain"] = None
            __props__.__dict__["website_endpoint"] = None
        super(ObjectBucketWebsiteConfiguration, __self__).__init__(
            'scaleway:index/objectBucketWebsiteConfiguration:ObjectBucketWebsiteConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            error_document: Optional[pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationErrorDocumentArgs']]] = None,
            index_document: Optional[pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationIndexDocumentArgs']]] = None,
            website_domain: Optional[pulumi.Input[str]] = None,
            website_endpoint: Optional[pulumi.Input[str]] = None) -> 'ObjectBucketWebsiteConfiguration':
        """
        Get an existing ObjectBucketWebsiteConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: (Required, Forces new resource) The name of the bucket.
        :param pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationErrorDocumentArgs']] error_document: (Optional) The name of the error document for the website detailed below.
        :param pulumi.Input[pulumi.InputType['ObjectBucketWebsiteConfigurationIndexDocumentArgs']] index_document: (Optional) The name of the index document for the website detailed below.
        :param pulumi.Input[str] website_domain: The website endpoint.
        :param pulumi.Input[str] website_endpoint: The domain of the website endpoint.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ObjectBucketWebsiteConfigurationState.__new__(_ObjectBucketWebsiteConfigurationState)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["error_document"] = error_document
        __props__.__dict__["index_document"] = index_document
        __props__.__dict__["website_domain"] = website_domain
        __props__.__dict__["website_endpoint"] = website_endpoint
        return ObjectBucketWebsiteConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        (Required, Forces new resource) The name of the bucket.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="errorDocument")
    def error_document(self) -> pulumi.Output[Optional['outputs.ObjectBucketWebsiteConfigurationErrorDocument']]:
        """
        (Optional) The name of the error document for the website detailed below.
        """
        return pulumi.get(self, "error_document")

    @property
    @pulumi.getter(name="indexDocument")
    def index_document(self) -> pulumi.Output[Optional['outputs.ObjectBucketWebsiteConfigurationIndexDocument']]:
        """
        (Optional) The name of the index document for the website detailed below.
        """
        return pulumi.get(self, "index_document")

    @property
    @pulumi.getter(name="websiteDomain")
    def website_domain(self) -> pulumi.Output[str]:
        """
        The website endpoint.
        """
        return pulumi.get(self, "website_domain")

    @property
    @pulumi.getter(name="websiteEndpoint")
    def website_endpoint(self) -> pulumi.Output[str]:
        """
        The domain of the website endpoint.
        """
        return pulumi.get(self, "website_endpoint")

