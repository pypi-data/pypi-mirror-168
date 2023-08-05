"""DO NOT EDIT THIS FILE!

This file is auto generated by github rest api discription.
See https://github.com/github/rest-api-description for more information.
"""


from typing import TYPE_CHECKING, Union, overload

from pydantic import BaseModel, parse_obj_as

from githubkit.utils import UNSET, Unset, exclude_unset

from .models import (
    BasicError,
    ActionsBillingUsage,
    CombinedBillingUsage,
    PackagesBillingUsage,
    AdvancedSecurityActiveCommitters,
)

if TYPE_CHECKING:
    from githubkit import GitHubCore
    from githubkit.response import Response


class BillingClient:
    def __init__(self, github: "GitHubCore"):
        self._github = github

    def get_github_advanced_security_billing_ghe(
        self,
        enterprise: str,
        per_page: Union[Unset, int] = 30,
        page: Union[Unset, int] = 1,
    ) -> "Response[AdvancedSecurityActiveCommitters]":
        url = f"/enterprises/{enterprise}/settings/billing/advanced-security"

        params = {
            "per_page": per_page,
            "page": page,
        }

        return self._github.request(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=AdvancedSecurityActiveCommitters,
            error_models={
                "403": BasicError,
            },
        )

    async def async_get_github_advanced_security_billing_ghe(
        self,
        enterprise: str,
        per_page: Union[Unset, int] = 30,
        page: Union[Unset, int] = 1,
    ) -> "Response[AdvancedSecurityActiveCommitters]":
        url = f"/enterprises/{enterprise}/settings/billing/advanced-security"

        params = {
            "per_page": per_page,
            "page": page,
        }

        return await self._github.arequest(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=AdvancedSecurityActiveCommitters,
            error_models={
                "403": BasicError,
            },
        )

    def get_github_actions_billing_org(
        self,
        org: str,
    ) -> "Response[ActionsBillingUsage]":
        url = f"/orgs/{org}/settings/billing/actions"

        return self._github.request(
            "GET",
            url,
            response_model=ActionsBillingUsage,
        )

    async def async_get_github_actions_billing_org(
        self,
        org: str,
    ) -> "Response[ActionsBillingUsage]":
        url = f"/orgs/{org}/settings/billing/actions"

        return await self._github.arequest(
            "GET",
            url,
            response_model=ActionsBillingUsage,
        )

    def get_github_advanced_security_billing_org(
        self,
        org: str,
        per_page: Union[Unset, int] = 30,
        page: Union[Unset, int] = 1,
    ) -> "Response[AdvancedSecurityActiveCommitters]":
        url = f"/orgs/{org}/settings/billing/advanced-security"

        params = {
            "per_page": per_page,
            "page": page,
        }

        return self._github.request(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=AdvancedSecurityActiveCommitters,
            error_models={
                "403": BasicError,
            },
        )

    async def async_get_github_advanced_security_billing_org(
        self,
        org: str,
        per_page: Union[Unset, int] = 30,
        page: Union[Unset, int] = 1,
    ) -> "Response[AdvancedSecurityActiveCommitters]":
        url = f"/orgs/{org}/settings/billing/advanced-security"

        params = {
            "per_page": per_page,
            "page": page,
        }

        return await self._github.arequest(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=AdvancedSecurityActiveCommitters,
            error_models={
                "403": BasicError,
            },
        )

    def get_github_packages_billing_org(
        self,
        org: str,
    ) -> "Response[PackagesBillingUsage]":
        url = f"/orgs/{org}/settings/billing/packages"

        return self._github.request(
            "GET",
            url,
            response_model=PackagesBillingUsage,
        )

    async def async_get_github_packages_billing_org(
        self,
        org: str,
    ) -> "Response[PackagesBillingUsage]":
        url = f"/orgs/{org}/settings/billing/packages"

        return await self._github.arequest(
            "GET",
            url,
            response_model=PackagesBillingUsage,
        )

    def get_shared_storage_billing_org(
        self,
        org: str,
    ) -> "Response[CombinedBillingUsage]":
        url = f"/orgs/{org}/settings/billing/shared-storage"

        return self._github.request(
            "GET",
            url,
            response_model=CombinedBillingUsage,
        )

    async def async_get_shared_storage_billing_org(
        self,
        org: str,
    ) -> "Response[CombinedBillingUsage]":
        url = f"/orgs/{org}/settings/billing/shared-storage"

        return await self._github.arequest(
            "GET",
            url,
            response_model=CombinedBillingUsage,
        )

    def get_github_actions_billing_user(
        self,
        username: str,
    ) -> "Response[ActionsBillingUsage]":
        url = f"/users/{username}/settings/billing/actions"

        return self._github.request(
            "GET",
            url,
            response_model=ActionsBillingUsage,
        )

    async def async_get_github_actions_billing_user(
        self,
        username: str,
    ) -> "Response[ActionsBillingUsage]":
        url = f"/users/{username}/settings/billing/actions"

        return await self._github.arequest(
            "GET",
            url,
            response_model=ActionsBillingUsage,
        )

    def get_github_packages_billing_user(
        self,
        username: str,
    ) -> "Response[PackagesBillingUsage]":
        url = f"/users/{username}/settings/billing/packages"

        return self._github.request(
            "GET",
            url,
            response_model=PackagesBillingUsage,
        )

    async def async_get_github_packages_billing_user(
        self,
        username: str,
    ) -> "Response[PackagesBillingUsage]":
        url = f"/users/{username}/settings/billing/packages"

        return await self._github.arequest(
            "GET",
            url,
            response_model=PackagesBillingUsage,
        )

    def get_shared_storage_billing_user(
        self,
        username: str,
    ) -> "Response[CombinedBillingUsage]":
        url = f"/users/{username}/settings/billing/shared-storage"

        return self._github.request(
            "GET",
            url,
            response_model=CombinedBillingUsage,
        )

    async def async_get_shared_storage_billing_user(
        self,
        username: str,
    ) -> "Response[CombinedBillingUsage]":
        url = f"/users/{username}/settings/billing/shared-storage"

        return await self._github.arequest(
            "GET",
            url,
            response_model=CombinedBillingUsage,
        )
