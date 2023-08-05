"""DO NOT EDIT THIS FILE!

This file is auto generated by github rest api discription.
See https://github.com/github/rest-api-description for more information.
"""


from typing import TYPE_CHECKING, List, Union, Literal, overload

from pydantic import BaseModel, parse_obj_as

from githubkit.utils import UNSET, Unset, exclude_unset

from .models import Package, BasicError, PackageVersion

if TYPE_CHECKING:
    from githubkit import GitHubCore
    from githubkit.response import Response


class PackagesClient:
    def __init__(self, github: "GitHubCore"):
        self._github = github

    def list_packages_for_organization(
        self,
        org: str,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        visibility: Union[Unset, Literal["public", "private", "internal"]] = UNSET,
    ) -> "Response[List[Package]]":
        url = f"/orgs/{org}/packages"

        params = {
            "package_type": package_type,
            "visibility": visibility,
        }

        return self._github.request(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[Package],
            error_models={
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_list_packages_for_organization(
        self,
        org: str,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        visibility: Union[Unset, Literal["public", "private", "internal"]] = UNSET,
    ) -> "Response[List[Package]]":
        url = f"/orgs/{org}/packages"

        params = {
            "package_type": package_type,
            "visibility": visibility,
        }

        return await self._github.arequest(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[Package],
            error_models={
                "403": BasicError,
                "401": BasicError,
            },
        )

    def get_package_for_organization(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
    ) -> "Response[Package]":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}"

        return self._github.request(
            "GET",
            url,
            response_model=Package,
        )

    async def async_get_package_for_organization(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
    ) -> "Response[Package]":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}"

        return await self._github.arequest(
            "GET",
            url,
            response_model=Package,
        )

    def delete_package_for_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
    ) -> "Response":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}"

        return self._github.request(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_delete_package_for_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
    ) -> "Response":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}"

        return await self._github.arequest(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def restore_package_for_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        token: Union[Unset, str] = UNSET,
    ) -> "Response":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/restore"

        params = {
            "token": token,
        }

        return self._github.request(
            "POST",
            url,
            params=exclude_unset(params),
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_restore_package_for_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        token: Union[Unset, str] = UNSET,
    ) -> "Response":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/restore"

        params = {
            "token": token,
        }

        return await self._github.arequest(
            "POST",
            url,
            params=exclude_unset(params),
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def get_all_package_versions_for_package_owned_by_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        page: Union[Unset, int] = 1,
        per_page: Union[Unset, int] = 30,
        state: Union[Unset, Literal["active", "deleted"]] = "active",
    ) -> "Response[List[PackageVersion]]":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/versions"

        params = {
            "page": page,
            "per_page": per_page,
            "state": state,
        }

        return self._github.request(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[PackageVersion],
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_get_all_package_versions_for_package_owned_by_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        page: Union[Unset, int] = 1,
        per_page: Union[Unset, int] = 30,
        state: Union[Unset, Literal["active", "deleted"]] = "active",
    ) -> "Response[List[PackageVersion]]":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/versions"

        params = {
            "page": page,
            "per_page": per_page,
            "state": state,
        }

        return await self._github.arequest(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[PackageVersion],
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def get_package_version_for_organization(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        package_version_id: int,
    ) -> "Response[PackageVersion]":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return self._github.request(
            "GET",
            url,
            response_model=PackageVersion,
        )

    async def async_get_package_version_for_organization(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        package_version_id: int,
    ) -> "Response[PackageVersion]":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return await self._github.arequest(
            "GET",
            url,
            response_model=PackageVersion,
        )

    def delete_package_version_for_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return self._github.request(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_delete_package_version_for_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return await self._github.arequest(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def restore_package_version_for_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}/restore"

        return self._github.request(
            "POST",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_restore_package_version_for_org(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        org: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}/restore"

        return await self._github.arequest(
            "POST",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def list_packages_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        visibility: Union[Unset, Literal["public", "private", "internal"]] = UNSET,
    ) -> "Response[List[Package]]":
        url = "/user/packages"

        params = {
            "package_type": package_type,
            "visibility": visibility,
        }

        return self._github.request(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[Package],
        )

    async def async_list_packages_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        visibility: Union[Unset, Literal["public", "private", "internal"]] = UNSET,
    ) -> "Response[List[Package]]":
        url = "/user/packages"

        params = {
            "package_type": package_type,
            "visibility": visibility,
        }

        return await self._github.arequest(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[Package],
        )

    def get_package_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
    ) -> "Response[Package]":
        url = f"/user/packages/{package_type}/{package_name}"

        return self._github.request(
            "GET",
            url,
            response_model=Package,
        )

    async def async_get_package_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
    ) -> "Response[Package]":
        url = f"/user/packages/{package_type}/{package_name}"

        return await self._github.arequest(
            "GET",
            url,
            response_model=Package,
        )

    def delete_package_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
    ) -> "Response":
        url = f"/user/packages/{package_type}/{package_name}"

        return self._github.request(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_delete_package_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
    ) -> "Response":
        url = f"/user/packages/{package_type}/{package_name}"

        return await self._github.arequest(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def restore_package_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        token: Union[Unset, str] = UNSET,
    ) -> "Response":
        url = f"/user/packages/{package_type}/{package_name}/restore"

        params = {
            "token": token,
        }

        return self._github.request(
            "POST",
            url,
            params=exclude_unset(params),
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_restore_package_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        token: Union[Unset, str] = UNSET,
    ) -> "Response":
        url = f"/user/packages/{package_type}/{package_name}/restore"

        params = {
            "token": token,
        }

        return await self._github.arequest(
            "POST",
            url,
            params=exclude_unset(params),
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def get_all_package_versions_for_package_owned_by_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        page: Union[Unset, int] = 1,
        per_page: Union[Unset, int] = 30,
        state: Union[Unset, Literal["active", "deleted"]] = "active",
    ) -> "Response[List[PackageVersion]]":
        url = f"/user/packages/{package_type}/{package_name}/versions"

        params = {
            "page": page,
            "per_page": per_page,
            "state": state,
        }

        return self._github.request(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[PackageVersion],
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_get_all_package_versions_for_package_owned_by_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        page: Union[Unset, int] = 1,
        per_page: Union[Unset, int] = 30,
        state: Union[Unset, Literal["active", "deleted"]] = "active",
    ) -> "Response[List[PackageVersion]]":
        url = f"/user/packages/{package_type}/{package_name}/versions"

        params = {
            "page": page,
            "per_page": per_page,
            "state": state,
        }

        return await self._github.arequest(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[PackageVersion],
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def get_package_version_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        package_version_id: int,
    ) -> "Response[PackageVersion]":
        url = f"/user/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return self._github.request(
            "GET",
            url,
            response_model=PackageVersion,
        )

    async def async_get_package_version_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        package_version_id: int,
    ) -> "Response[PackageVersion]":
        url = f"/user/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return await self._github.arequest(
            "GET",
            url,
            response_model=PackageVersion,
        )

    def delete_package_version_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/user/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return self._github.request(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_delete_package_version_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/user/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return await self._github.arequest(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def restore_package_version_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/user/packages/{package_type}/{package_name}/versions/{package_version_id}/restore"

        return self._github.request(
            "POST",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_restore_package_version_for_authenticated_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/user/packages/{package_type}/{package_name}/versions/{package_version_id}/restore"

        return await self._github.arequest(
            "POST",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def list_packages_for_user(
        self,
        username: str,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        visibility: Union[Unset, Literal["public", "private", "internal"]] = UNSET,
    ) -> "Response[List[Package]]":
        url = f"/users/{username}/packages"

        params = {
            "package_type": package_type,
            "visibility": visibility,
        }

        return self._github.request(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[Package],
            error_models={
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_list_packages_for_user(
        self,
        username: str,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        visibility: Union[Unset, Literal["public", "private", "internal"]] = UNSET,
    ) -> "Response[List[Package]]":
        url = f"/users/{username}/packages"

        params = {
            "package_type": package_type,
            "visibility": visibility,
        }

        return await self._github.arequest(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[Package],
            error_models={
                "403": BasicError,
                "401": BasicError,
            },
        )

    def get_package_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
    ) -> "Response[Package]":
        url = f"/users/{username}/packages/{package_type}/{package_name}"

        return self._github.request(
            "GET",
            url,
            response_model=Package,
        )

    async def async_get_package_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
    ) -> "Response[Package]":
        url = f"/users/{username}/packages/{package_type}/{package_name}"

        return await self._github.arequest(
            "GET",
            url,
            response_model=Package,
        )

    def delete_package_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
    ) -> "Response":
        url = f"/users/{username}/packages/{package_type}/{package_name}"

        return self._github.request(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_delete_package_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
    ) -> "Response":
        url = f"/users/{username}/packages/{package_type}/{package_name}"

        return await self._github.arequest(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def restore_package_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
        token: Union[Unset, str] = UNSET,
    ) -> "Response":
        url = f"/users/{username}/packages/{package_type}/{package_name}/restore"

        params = {
            "token": token,
        }

        return self._github.request(
            "POST",
            url,
            params=exclude_unset(params),
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_restore_package_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
        token: Union[Unset, str] = UNSET,
    ) -> "Response":
        url = f"/users/{username}/packages/{package_type}/{package_name}/restore"

        params = {
            "token": token,
        }

        return await self._github.arequest(
            "POST",
            url,
            params=exclude_unset(params),
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def get_all_package_versions_for_package_owned_by_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
    ) -> "Response[List[PackageVersion]]":
        url = f"/users/{username}/packages/{package_type}/{package_name}/versions"

        return self._github.request(
            "GET",
            url,
            response_model=List[PackageVersion],
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_get_all_package_versions_for_package_owned_by_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
    ) -> "Response[List[PackageVersion]]":
        url = f"/users/{username}/packages/{package_type}/{package_name}/versions"

        return await self._github.arequest(
            "GET",
            url,
            response_model=List[PackageVersion],
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def get_package_version_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        package_version_id: int,
        username: str,
    ) -> "Response[PackageVersion]":
        url = f"/users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return self._github.request(
            "GET",
            url,
            response_model=PackageVersion,
        )

    async def async_get_package_version_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        package_version_id: int,
        username: str,
    ) -> "Response[PackageVersion]":
        url = f"/users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return await self._github.arequest(
            "GET",
            url,
            response_model=PackageVersion,
        )

    def delete_package_version_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return self._github.request(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_delete_package_version_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}"

        return await self._github.arequest(
            "DELETE",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    def restore_package_version_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}/restore"

        return self._github.request(
            "POST",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )

    async def async_restore_package_version_for_user(
        self,
        package_type: Literal[
            "npm", "maven", "rubygems", "docker", "nuget", "container"
        ],
        package_name: str,
        username: str,
        package_version_id: int,
    ) -> "Response":
        url = f"/users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}/restore"

        return await self._github.arequest(
            "POST",
            url,
            error_models={
                "404": BasicError,
                "403": BasicError,
                "401": BasicError,
            },
        )
