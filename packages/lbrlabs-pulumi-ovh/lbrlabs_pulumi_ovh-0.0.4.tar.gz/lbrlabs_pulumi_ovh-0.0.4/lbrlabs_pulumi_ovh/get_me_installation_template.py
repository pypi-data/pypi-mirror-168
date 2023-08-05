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

__all__ = [
    'GetMeInstallationTemplateResult',
    'AwaitableGetMeInstallationTemplateResult',
    'get_me_installation_template',
    'get_me_installation_template_output',
]

@pulumi.output_type
class GetMeInstallationTemplateResult:
    """
    A collection of values returned by getMeInstallationTemplate.
    """
    def __init__(__self__, available_languages=None, beta=None, bit_format=None, category=None, customizations=None, default_language=None, deprecated=None, description=None, distribution=None, family=None, filesystems=None, hard_raid_configuration=None, id=None, last_modification=None, lvm_ready=None, partition_schemes=None, supports_distribution_kernel=None, supports_gpt_label=None, supports_rtm=None, supports_sql_server=None, supports_uefi=None, template_name=None):
        if available_languages and not isinstance(available_languages, list):
            raise TypeError("Expected argument 'available_languages' to be a list")
        pulumi.set(__self__, "available_languages", available_languages)
        if beta and not isinstance(beta, bool):
            raise TypeError("Expected argument 'beta' to be a bool")
        pulumi.set(__self__, "beta", beta)
        if bit_format and not isinstance(bit_format, int):
            raise TypeError("Expected argument 'bit_format' to be a int")
        pulumi.set(__self__, "bit_format", bit_format)
        if category and not isinstance(category, str):
            raise TypeError("Expected argument 'category' to be a str")
        pulumi.set(__self__, "category", category)
        if customizations and not isinstance(customizations, list):
            raise TypeError("Expected argument 'customizations' to be a list")
        pulumi.set(__self__, "customizations", customizations)
        if default_language and not isinstance(default_language, str):
            raise TypeError("Expected argument 'default_language' to be a str")
        pulumi.set(__self__, "default_language", default_language)
        if deprecated and not isinstance(deprecated, bool):
            raise TypeError("Expected argument 'deprecated' to be a bool")
        pulumi.set(__self__, "deprecated", deprecated)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if distribution and not isinstance(distribution, str):
            raise TypeError("Expected argument 'distribution' to be a str")
        pulumi.set(__self__, "distribution", distribution)
        if family and not isinstance(family, str):
            raise TypeError("Expected argument 'family' to be a str")
        pulumi.set(__self__, "family", family)
        if filesystems and not isinstance(filesystems, list):
            raise TypeError("Expected argument 'filesystems' to be a list")
        pulumi.set(__self__, "filesystems", filesystems)
        if hard_raid_configuration and not isinstance(hard_raid_configuration, bool):
            raise TypeError("Expected argument 'hard_raid_configuration' to be a bool")
        pulumi.set(__self__, "hard_raid_configuration", hard_raid_configuration)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_modification and not isinstance(last_modification, str):
            raise TypeError("Expected argument 'last_modification' to be a str")
        pulumi.set(__self__, "last_modification", last_modification)
        if lvm_ready and not isinstance(lvm_ready, bool):
            raise TypeError("Expected argument 'lvm_ready' to be a bool")
        pulumi.set(__self__, "lvm_ready", lvm_ready)
        if partition_schemes and not isinstance(partition_schemes, list):
            raise TypeError("Expected argument 'partition_schemes' to be a list")
        pulumi.set(__self__, "partition_schemes", partition_schemes)
        if supports_distribution_kernel and not isinstance(supports_distribution_kernel, bool):
            raise TypeError("Expected argument 'supports_distribution_kernel' to be a bool")
        pulumi.set(__self__, "supports_distribution_kernel", supports_distribution_kernel)
        if supports_gpt_label and not isinstance(supports_gpt_label, bool):
            raise TypeError("Expected argument 'supports_gpt_label' to be a bool")
        pulumi.set(__self__, "supports_gpt_label", supports_gpt_label)
        if supports_rtm and not isinstance(supports_rtm, bool):
            raise TypeError("Expected argument 'supports_rtm' to be a bool")
        pulumi.set(__self__, "supports_rtm", supports_rtm)
        if supports_sql_server and not isinstance(supports_sql_server, bool):
            raise TypeError("Expected argument 'supports_sql_server' to be a bool")
        pulumi.set(__self__, "supports_sql_server", supports_sql_server)
        if supports_uefi and not isinstance(supports_uefi, str):
            raise TypeError("Expected argument 'supports_uefi' to be a str")
        pulumi.set(__self__, "supports_uefi", supports_uefi)
        if template_name and not isinstance(template_name, str):
            raise TypeError("Expected argument 'template_name' to be a str")
        pulumi.set(__self__, "template_name", template_name)

    @property
    @pulumi.getter(name="availableLanguages")
    def available_languages(self) -> Sequence[str]:
        return pulumi.get(self, "available_languages")

    @property
    @pulumi.getter
    def beta(self) -> bool:
        return pulumi.get(self, "beta")

    @property
    @pulumi.getter(name="bitFormat")
    def bit_format(self) -> int:
        return pulumi.get(self, "bit_format")

    @property
    @pulumi.getter
    def category(self) -> str:
        return pulumi.get(self, "category")

    @property
    @pulumi.getter
    def customizations(self) -> Sequence['outputs.GetMeInstallationTemplateCustomizationResult']:
        return pulumi.get(self, "customizations")

    @property
    @pulumi.getter(name="defaultLanguage")
    def default_language(self) -> str:
        return pulumi.get(self, "default_language")

    @property
    @pulumi.getter
    def deprecated(self) -> bool:
        return pulumi.get(self, "deprecated")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def distribution(self) -> str:
        return pulumi.get(self, "distribution")

    @property
    @pulumi.getter
    def family(self) -> str:
        return pulumi.get(self, "family")

    @property
    @pulumi.getter
    def filesystems(self) -> Sequence[str]:
        return pulumi.get(self, "filesystems")

    @property
    @pulumi.getter(name="hardRaidConfiguration")
    def hard_raid_configuration(self) -> bool:
        return pulumi.get(self, "hard_raid_configuration")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModification")
    def last_modification(self) -> str:
        return pulumi.get(self, "last_modification")

    @property
    @pulumi.getter(name="lvmReady")
    def lvm_ready(self) -> bool:
        return pulumi.get(self, "lvm_ready")

    @property
    @pulumi.getter(name="partitionSchemes")
    def partition_schemes(self) -> Sequence['outputs.GetMeInstallationTemplatePartitionSchemeResult']:
        return pulumi.get(self, "partition_schemes")

    @property
    @pulumi.getter(name="supportsDistributionKernel")
    def supports_distribution_kernel(self) -> bool:
        return pulumi.get(self, "supports_distribution_kernel")

    @property
    @pulumi.getter(name="supportsGptLabel")
    def supports_gpt_label(self) -> bool:
        return pulumi.get(self, "supports_gpt_label")

    @property
    @pulumi.getter(name="supportsRtm")
    def supports_rtm(self) -> bool:
        return pulumi.get(self, "supports_rtm")

    @property
    @pulumi.getter(name="supportsSqlServer")
    def supports_sql_server(self) -> bool:
        return pulumi.get(self, "supports_sql_server")

    @property
    @pulumi.getter(name="supportsUefi")
    def supports_uefi(self) -> str:
        return pulumi.get(self, "supports_uefi")

    @property
    @pulumi.getter(name="templateName")
    def template_name(self) -> str:
        return pulumi.get(self, "template_name")


class AwaitableGetMeInstallationTemplateResult(GetMeInstallationTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMeInstallationTemplateResult(
            available_languages=self.available_languages,
            beta=self.beta,
            bit_format=self.bit_format,
            category=self.category,
            customizations=self.customizations,
            default_language=self.default_language,
            deprecated=self.deprecated,
            description=self.description,
            distribution=self.distribution,
            family=self.family,
            filesystems=self.filesystems,
            hard_raid_configuration=self.hard_raid_configuration,
            id=self.id,
            last_modification=self.last_modification,
            lvm_ready=self.lvm_ready,
            partition_schemes=self.partition_schemes,
            supports_distribution_kernel=self.supports_distribution_kernel,
            supports_gpt_label=self.supports_gpt_label,
            supports_rtm=self.supports_rtm,
            supports_sql_server=self.supports_sql_server,
            supports_uefi=self.supports_uefi,
            template_name=self.template_name)


def get_me_installation_template(template_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMeInstallationTemplateResult:
    """
    Use this data source to get a custom installation template available for dedicated servers.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_ovh as ovh

    mytemplate = ovh.get_me_installation_template(template_name="mytemplate")
    ```
    """
    __args__ = dict()
    __args__['templateName'] = template_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('ovh:index/getMeInstallationTemplate:getMeInstallationTemplate', __args__, opts=opts, typ=GetMeInstallationTemplateResult).value

    return AwaitableGetMeInstallationTemplateResult(
        available_languages=__ret__.available_languages,
        beta=__ret__.beta,
        bit_format=__ret__.bit_format,
        category=__ret__.category,
        customizations=__ret__.customizations,
        default_language=__ret__.default_language,
        deprecated=__ret__.deprecated,
        description=__ret__.description,
        distribution=__ret__.distribution,
        family=__ret__.family,
        filesystems=__ret__.filesystems,
        hard_raid_configuration=__ret__.hard_raid_configuration,
        id=__ret__.id,
        last_modification=__ret__.last_modification,
        lvm_ready=__ret__.lvm_ready,
        partition_schemes=__ret__.partition_schemes,
        supports_distribution_kernel=__ret__.supports_distribution_kernel,
        supports_gpt_label=__ret__.supports_gpt_label,
        supports_rtm=__ret__.supports_rtm,
        supports_sql_server=__ret__.supports_sql_server,
        supports_uefi=__ret__.supports_uefi,
        template_name=__ret__.template_name)


@_utilities.lift_output_func(get_me_installation_template)
def get_me_installation_template_output(template_name: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMeInstallationTemplateResult]:
    """
    Use this data source to get a custom installation template available for dedicated servers.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_ovh as ovh

    mytemplate = ovh.get_me_installation_template(template_name="mytemplate")
    ```
    """
    ...
