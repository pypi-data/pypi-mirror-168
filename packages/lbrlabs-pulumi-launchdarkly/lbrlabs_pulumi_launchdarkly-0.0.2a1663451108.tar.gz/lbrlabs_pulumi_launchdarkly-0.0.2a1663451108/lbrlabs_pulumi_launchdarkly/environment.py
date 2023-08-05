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

__all__ = ['EnvironmentArgs', 'Environment']

@pulumi.input_type
class EnvironmentArgs:
    def __init__(__self__, *,
                 color: pulumi.Input[str],
                 key: pulumi.Input[str],
                 project_key: pulumi.Input[str],
                 approval_settings: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentApprovalSettingArgs']]]] = None,
                 confirm_changes: Optional[pulumi.Input[bool]] = None,
                 default_track_events: Optional[pulumi.Input[bool]] = None,
                 default_ttl: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 require_comments: Optional[pulumi.Input[bool]] = None,
                 secure_mode: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Environment resource.
        :param pulumi.Input[str] color: The color swatch as an RGB hex value with no leading `#`. For example: `000000`.
        :param pulumi.Input[str] key: The project-unique key for the environment.
        :param pulumi.Input[str] project_key: - The environment's project key.
        :param pulumi.Input[bool] confirm_changes: Set to `true` if this environment requires confirmation for flag and segment changes. This field will default to `false` when not set.
        :param pulumi.Input[bool] default_track_events: Set to `true` to enable data export for every flag created in this environment after you configure this argument. This field will default to `false` when not set. To learn more, read [Data Export](https://docs.launchdarkly.com/docs/data-export).
        :param pulumi.Input[int] default_ttl: The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to `0` when not set. To learn more, read [TTL settings](https://docs.launchdarkly.com/docs/environments#section-ttl-settings).
        :param pulumi.Input[str] name: The name of the environment.
        :param pulumi.Input[bool] require_comments: Set to `true` if this environment requires comments for flag and segment changes. This field will default to `false` when not set.
        :param pulumi.Input[bool] secure_mode: Set to `true` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to `false` when not set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Set of tags associated with the environment.
        """
        pulumi.set(__self__, "color", color)
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "project_key", project_key)
        if approval_settings is not None:
            pulumi.set(__self__, "approval_settings", approval_settings)
        if confirm_changes is not None:
            pulumi.set(__self__, "confirm_changes", confirm_changes)
        if default_track_events is not None:
            pulumi.set(__self__, "default_track_events", default_track_events)
        if default_ttl is not None:
            pulumi.set(__self__, "default_ttl", default_ttl)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if require_comments is not None:
            pulumi.set(__self__, "require_comments", require_comments)
        if secure_mode is not None:
            pulumi.set(__self__, "secure_mode", secure_mode)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def color(self) -> pulumi.Input[str]:
        """
        The color swatch as an RGB hex value with no leading `#`. For example: `000000`.
        """
        return pulumi.get(self, "color")

    @color.setter
    def color(self, value: pulumi.Input[str]):
        pulumi.set(self, "color", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The project-unique key for the environment.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter(name="projectKey")
    def project_key(self) -> pulumi.Input[str]:
        """
        - The environment's project key.
        """
        return pulumi.get(self, "project_key")

    @project_key.setter
    def project_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "project_key", value)

    @property
    @pulumi.getter(name="approvalSettings")
    def approval_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentApprovalSettingArgs']]]]:
        return pulumi.get(self, "approval_settings")

    @approval_settings.setter
    def approval_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentApprovalSettingArgs']]]]):
        pulumi.set(self, "approval_settings", value)

    @property
    @pulumi.getter(name="confirmChanges")
    def confirm_changes(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to `true` if this environment requires confirmation for flag and segment changes. This field will default to `false` when not set.
        """
        return pulumi.get(self, "confirm_changes")

    @confirm_changes.setter
    def confirm_changes(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "confirm_changes", value)

    @property
    @pulumi.getter(name="defaultTrackEvents")
    def default_track_events(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to `true` to enable data export for every flag created in this environment after you configure this argument. This field will default to `false` when not set. To learn more, read [Data Export](https://docs.launchdarkly.com/docs/data-export).
        """
        return pulumi.get(self, "default_track_events")

    @default_track_events.setter
    def default_track_events(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "default_track_events", value)

    @property
    @pulumi.getter(name="defaultTtl")
    def default_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to `0` when not set. To learn more, read [TTL settings](https://docs.launchdarkly.com/docs/environments#section-ttl-settings).
        """
        return pulumi.get(self, "default_ttl")

    @default_ttl.setter
    def default_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "default_ttl", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the environment.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="requireComments")
    def require_comments(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to `true` if this environment requires comments for flag and segment changes. This field will default to `false` when not set.
        """
        return pulumi.get(self, "require_comments")

    @require_comments.setter
    def require_comments(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "require_comments", value)

    @property
    @pulumi.getter(name="secureMode")
    def secure_mode(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to `true` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to `false` when not set.
        """
        return pulumi.get(self, "secure_mode")

    @secure_mode.setter
    def secure_mode(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "secure_mode", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of tags associated with the environment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _EnvironmentState:
    def __init__(__self__, *,
                 api_key: Optional[pulumi.Input[str]] = None,
                 approval_settings: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentApprovalSettingArgs']]]] = None,
                 client_side_id: Optional[pulumi.Input[str]] = None,
                 color: Optional[pulumi.Input[str]] = None,
                 confirm_changes: Optional[pulumi.Input[bool]] = None,
                 default_track_events: Optional[pulumi.Input[bool]] = None,
                 default_ttl: Optional[pulumi.Input[int]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 mobile_key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project_key: Optional[pulumi.Input[str]] = None,
                 require_comments: Optional[pulumi.Input[bool]] = None,
                 secure_mode: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Environment resources.
        :param pulumi.Input[str] api_key: The environment's SDK key.
        :param pulumi.Input[str] client_side_id: The environment's client-side ID.
        :param pulumi.Input[str] color: The color swatch as an RGB hex value with no leading `#`. For example: `000000`.
        :param pulumi.Input[bool] confirm_changes: Set to `true` if this environment requires confirmation for flag and segment changes. This field will default to `false` when not set.
        :param pulumi.Input[bool] default_track_events: Set to `true` to enable data export for every flag created in this environment after you configure this argument. This field will default to `false` when not set. To learn more, read [Data Export](https://docs.launchdarkly.com/docs/data-export).
        :param pulumi.Input[int] default_ttl: The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to `0` when not set. To learn more, read [TTL settings](https://docs.launchdarkly.com/docs/environments#section-ttl-settings).
        :param pulumi.Input[str] key: The project-unique key for the environment.
        :param pulumi.Input[str] mobile_key: The environment's mobile key.
        :param pulumi.Input[str] name: The name of the environment.
        :param pulumi.Input[str] project_key: - The environment's project key.
        :param pulumi.Input[bool] require_comments: Set to `true` if this environment requires comments for flag and segment changes. This field will default to `false` when not set.
        :param pulumi.Input[bool] secure_mode: Set to `true` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to `false` when not set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Set of tags associated with the environment.
        """
        if api_key is not None:
            pulumi.set(__self__, "api_key", api_key)
        if approval_settings is not None:
            pulumi.set(__self__, "approval_settings", approval_settings)
        if client_side_id is not None:
            pulumi.set(__self__, "client_side_id", client_side_id)
        if color is not None:
            pulumi.set(__self__, "color", color)
        if confirm_changes is not None:
            pulumi.set(__self__, "confirm_changes", confirm_changes)
        if default_track_events is not None:
            pulumi.set(__self__, "default_track_events", default_track_events)
        if default_ttl is not None:
            pulumi.set(__self__, "default_ttl", default_ttl)
        if key is not None:
            pulumi.set(__self__, "key", key)
        if mobile_key is not None:
            pulumi.set(__self__, "mobile_key", mobile_key)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project_key is not None:
            pulumi.set(__self__, "project_key", project_key)
        if require_comments is not None:
            pulumi.set(__self__, "require_comments", require_comments)
        if secure_mode is not None:
            pulumi.set(__self__, "secure_mode", secure_mode)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> Optional[pulumi.Input[str]]:
        """
        The environment's SDK key.
        """
        return pulumi.get(self, "api_key")

    @api_key.setter
    def api_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_key", value)

    @property
    @pulumi.getter(name="approvalSettings")
    def approval_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentApprovalSettingArgs']]]]:
        return pulumi.get(self, "approval_settings")

    @approval_settings.setter
    def approval_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentApprovalSettingArgs']]]]):
        pulumi.set(self, "approval_settings", value)

    @property
    @pulumi.getter(name="clientSideId")
    def client_side_id(self) -> Optional[pulumi.Input[str]]:
        """
        The environment's client-side ID.
        """
        return pulumi.get(self, "client_side_id")

    @client_side_id.setter
    def client_side_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_side_id", value)

    @property
    @pulumi.getter
    def color(self) -> Optional[pulumi.Input[str]]:
        """
        The color swatch as an RGB hex value with no leading `#`. For example: `000000`.
        """
        return pulumi.get(self, "color")

    @color.setter
    def color(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "color", value)

    @property
    @pulumi.getter(name="confirmChanges")
    def confirm_changes(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to `true` if this environment requires confirmation for flag and segment changes. This field will default to `false` when not set.
        """
        return pulumi.get(self, "confirm_changes")

    @confirm_changes.setter
    def confirm_changes(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "confirm_changes", value)

    @property
    @pulumi.getter(name="defaultTrackEvents")
    def default_track_events(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to `true` to enable data export for every flag created in this environment after you configure this argument. This field will default to `false` when not set. To learn more, read [Data Export](https://docs.launchdarkly.com/docs/data-export).
        """
        return pulumi.get(self, "default_track_events")

    @default_track_events.setter
    def default_track_events(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "default_track_events", value)

    @property
    @pulumi.getter(name="defaultTtl")
    def default_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to `0` when not set. To learn more, read [TTL settings](https://docs.launchdarkly.com/docs/environments#section-ttl-settings).
        """
        return pulumi.get(self, "default_ttl")

    @default_ttl.setter
    def default_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "default_ttl", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        The project-unique key for the environment.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter(name="mobileKey")
    def mobile_key(self) -> Optional[pulumi.Input[str]]:
        """
        The environment's mobile key.
        """
        return pulumi.get(self, "mobile_key")

    @mobile_key.setter
    def mobile_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mobile_key", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the environment.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="projectKey")
    def project_key(self) -> Optional[pulumi.Input[str]]:
        """
        - The environment's project key.
        """
        return pulumi.get(self, "project_key")

    @project_key.setter
    def project_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_key", value)

    @property
    @pulumi.getter(name="requireComments")
    def require_comments(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to `true` if this environment requires comments for flag and segment changes. This field will default to `false` when not set.
        """
        return pulumi.get(self, "require_comments")

    @require_comments.setter
    def require_comments(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "require_comments", value)

    @property
    @pulumi.getter(name="secureMode")
    def secure_mode(self) -> Optional[pulumi.Input[bool]]:
        """
        Set to `true` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to `false` when not set.
        """
        return pulumi.get(self, "secure_mode")

    @secure_mode.setter
    def secure_mode(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "secure_mode", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of tags associated with the environment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Environment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 approval_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentApprovalSettingArgs']]]]] = None,
                 color: Optional[pulumi.Input[str]] = None,
                 confirm_changes: Optional[pulumi.Input[bool]] = None,
                 default_track_events: Optional[pulumi.Input[bool]] = None,
                 default_ttl: Optional[pulumi.Input[int]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project_key: Optional[pulumi.Input[str]] = None,
                 require_comments: Optional[pulumi.Input[bool]] = None,
                 secure_mode: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import lbrlabs_pulumi_launchdarkly as launchdarkly

        staging = launchdarkly.Environment("staging",
            key="staging",
            color="ff00ff",
            tags=[
                "terraform",
                "staging",
            ],
            project_key=launchdarkly_project["example"]["key"])
        ```

        ```python
        import pulumi
        import lbrlabs_pulumi_launchdarkly as launchdarkly

        approvals_example = launchdarkly.Environment("approvalsExample",
            key="approvals-example",
            color="ff00ff",
            tags=[
                "terraform",
                "staging",
            ],
            approval_settings=[launchdarkly.EnvironmentApprovalSettingArgs(
                required=True,
                can_review_own_request=True,
                min_num_approvals=2,
                can_apply_declined_changes=True,
            )],
            project_key=launchdarkly_project["example"]["key"])
        ```

        ## Import

        You can import a LaunchDarkly environment using this format`project_key/environment_key`. For example

        ```sh
         $ pulumi import launchdarkly:index/environment:Environment staging example-project/staging
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] color: The color swatch as an RGB hex value with no leading `#`. For example: `000000`.
        :param pulumi.Input[bool] confirm_changes: Set to `true` if this environment requires confirmation for flag and segment changes. This field will default to `false` when not set.
        :param pulumi.Input[bool] default_track_events: Set to `true` to enable data export for every flag created in this environment after you configure this argument. This field will default to `false` when not set. To learn more, read [Data Export](https://docs.launchdarkly.com/docs/data-export).
        :param pulumi.Input[int] default_ttl: The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to `0` when not set. To learn more, read [TTL settings](https://docs.launchdarkly.com/docs/environments#section-ttl-settings).
        :param pulumi.Input[str] key: The project-unique key for the environment.
        :param pulumi.Input[str] name: The name of the environment.
        :param pulumi.Input[str] project_key: - The environment's project key.
        :param pulumi.Input[bool] require_comments: Set to `true` if this environment requires comments for flag and segment changes. This field will default to `false` when not set.
        :param pulumi.Input[bool] secure_mode: Set to `true` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to `false` when not set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Set of tags associated with the environment.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnvironmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import lbrlabs_pulumi_launchdarkly as launchdarkly

        staging = launchdarkly.Environment("staging",
            key="staging",
            color="ff00ff",
            tags=[
                "terraform",
                "staging",
            ],
            project_key=launchdarkly_project["example"]["key"])
        ```

        ```python
        import pulumi
        import lbrlabs_pulumi_launchdarkly as launchdarkly

        approvals_example = launchdarkly.Environment("approvalsExample",
            key="approvals-example",
            color="ff00ff",
            tags=[
                "terraform",
                "staging",
            ],
            approval_settings=[launchdarkly.EnvironmentApprovalSettingArgs(
                required=True,
                can_review_own_request=True,
                min_num_approvals=2,
                can_apply_declined_changes=True,
            )],
            project_key=launchdarkly_project["example"]["key"])
        ```

        ## Import

        You can import a LaunchDarkly environment using this format`project_key/environment_key`. For example

        ```sh
         $ pulumi import launchdarkly:index/environment:Environment staging example-project/staging
        ```

        :param str resource_name: The name of the resource.
        :param EnvironmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnvironmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 approval_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentApprovalSettingArgs']]]]] = None,
                 color: Optional[pulumi.Input[str]] = None,
                 confirm_changes: Optional[pulumi.Input[bool]] = None,
                 default_track_events: Optional[pulumi.Input[bool]] = None,
                 default_ttl: Optional[pulumi.Input[int]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project_key: Optional[pulumi.Input[str]] = None,
                 require_comments: Optional[pulumi.Input[bool]] = None,
                 secure_mode: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnvironmentArgs.__new__(EnvironmentArgs)

            __props__.__dict__["approval_settings"] = approval_settings
            if color is None and not opts.urn:
                raise TypeError("Missing required property 'color'")
            __props__.__dict__["color"] = color
            __props__.__dict__["confirm_changes"] = confirm_changes
            __props__.__dict__["default_track_events"] = default_track_events
            __props__.__dict__["default_ttl"] = default_ttl
            if key is None and not opts.urn:
                raise TypeError("Missing required property 'key'")
            __props__.__dict__["key"] = key
            __props__.__dict__["name"] = name
            if project_key is None and not opts.urn:
                raise TypeError("Missing required property 'project_key'")
            __props__.__dict__["project_key"] = project_key
            __props__.__dict__["require_comments"] = require_comments
            __props__.__dict__["secure_mode"] = secure_mode
            __props__.__dict__["tags"] = tags
            __props__.__dict__["api_key"] = None
            __props__.__dict__["client_side_id"] = None
            __props__.__dict__["mobile_key"] = None
        super(Environment, __self__).__init__(
            'launchdarkly:index/environment:Environment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_key: Optional[pulumi.Input[str]] = None,
            approval_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EnvironmentApprovalSettingArgs']]]]] = None,
            client_side_id: Optional[pulumi.Input[str]] = None,
            color: Optional[pulumi.Input[str]] = None,
            confirm_changes: Optional[pulumi.Input[bool]] = None,
            default_track_events: Optional[pulumi.Input[bool]] = None,
            default_ttl: Optional[pulumi.Input[int]] = None,
            key: Optional[pulumi.Input[str]] = None,
            mobile_key: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project_key: Optional[pulumi.Input[str]] = None,
            require_comments: Optional[pulumi.Input[bool]] = None,
            secure_mode: Optional[pulumi.Input[bool]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'Environment':
        """
        Get an existing Environment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_key: The environment's SDK key.
        :param pulumi.Input[str] client_side_id: The environment's client-side ID.
        :param pulumi.Input[str] color: The color swatch as an RGB hex value with no leading `#`. For example: `000000`.
        :param pulumi.Input[bool] confirm_changes: Set to `true` if this environment requires confirmation for flag and segment changes. This field will default to `false` when not set.
        :param pulumi.Input[bool] default_track_events: Set to `true` to enable data export for every flag created in this environment after you configure this argument. This field will default to `false` when not set. To learn more, read [Data Export](https://docs.launchdarkly.com/docs/data-export).
        :param pulumi.Input[int] default_ttl: The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to `0` when not set. To learn more, read [TTL settings](https://docs.launchdarkly.com/docs/environments#section-ttl-settings).
        :param pulumi.Input[str] key: The project-unique key for the environment.
        :param pulumi.Input[str] mobile_key: The environment's mobile key.
        :param pulumi.Input[str] name: The name of the environment.
        :param pulumi.Input[str] project_key: - The environment's project key.
        :param pulumi.Input[bool] require_comments: Set to `true` if this environment requires comments for flag and segment changes. This field will default to `false` when not set.
        :param pulumi.Input[bool] secure_mode: Set to `true` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to `false` when not set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Set of tags associated with the environment.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EnvironmentState.__new__(_EnvironmentState)

        __props__.__dict__["api_key"] = api_key
        __props__.__dict__["approval_settings"] = approval_settings
        __props__.__dict__["client_side_id"] = client_side_id
        __props__.__dict__["color"] = color
        __props__.__dict__["confirm_changes"] = confirm_changes
        __props__.__dict__["default_track_events"] = default_track_events
        __props__.__dict__["default_ttl"] = default_ttl
        __props__.__dict__["key"] = key
        __props__.__dict__["mobile_key"] = mobile_key
        __props__.__dict__["name"] = name
        __props__.__dict__["project_key"] = project_key
        __props__.__dict__["require_comments"] = require_comments
        __props__.__dict__["secure_mode"] = secure_mode
        __props__.__dict__["tags"] = tags
        return Environment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> pulumi.Output[str]:
        """
        The environment's SDK key.
        """
        return pulumi.get(self, "api_key")

    @property
    @pulumi.getter(name="approvalSettings")
    def approval_settings(self) -> pulumi.Output[Sequence['outputs.EnvironmentApprovalSetting']]:
        return pulumi.get(self, "approval_settings")

    @property
    @pulumi.getter(name="clientSideId")
    def client_side_id(self) -> pulumi.Output[str]:
        """
        The environment's client-side ID.
        """
        return pulumi.get(self, "client_side_id")

    @property
    @pulumi.getter
    def color(self) -> pulumi.Output[str]:
        """
        The color swatch as an RGB hex value with no leading `#`. For example: `000000`.
        """
        return pulumi.get(self, "color")

    @property
    @pulumi.getter(name="confirmChanges")
    def confirm_changes(self) -> pulumi.Output[Optional[bool]]:
        """
        Set to `true` if this environment requires confirmation for flag and segment changes. This field will default to `false` when not set.
        """
        return pulumi.get(self, "confirm_changes")

    @property
    @pulumi.getter(name="defaultTrackEvents")
    def default_track_events(self) -> pulumi.Output[Optional[bool]]:
        """
        Set to `true` to enable data export for every flag created in this environment after you configure this argument. This field will default to `false` when not set. To learn more, read [Data Export](https://docs.launchdarkly.com/docs/data-export).
        """
        return pulumi.get(self, "default_track_events")

    @property
    @pulumi.getter(name="defaultTtl")
    def default_ttl(self) -> pulumi.Output[Optional[int]]:
        """
        The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to `0` when not set. To learn more, read [TTL settings](https://docs.launchdarkly.com/docs/environments#section-ttl-settings).
        """
        return pulumi.get(self, "default_ttl")

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[str]:
        """
        The project-unique key for the environment.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter(name="mobileKey")
    def mobile_key(self) -> pulumi.Output[str]:
        """
        The environment's mobile key.
        """
        return pulumi.get(self, "mobile_key")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the environment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="projectKey")
    def project_key(self) -> pulumi.Output[str]:
        """
        - The environment's project key.
        """
        return pulumi.get(self, "project_key")

    @property
    @pulumi.getter(name="requireComments")
    def require_comments(self) -> pulumi.Output[Optional[bool]]:
        """
        Set to `true` if this environment requires comments for flag and segment changes. This field will default to `false` when not set.
        """
        return pulumi.get(self, "require_comments")

    @property
    @pulumi.getter(name="secureMode")
    def secure_mode(self) -> pulumi.Output[Optional[bool]]:
        """
        Set to `true` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to `false` when not set.
        """
        return pulumi.get(self, "secure_mode")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Set of tags associated with the environment.
        """
        return pulumi.get(self, "tags")

