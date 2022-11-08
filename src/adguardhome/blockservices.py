"""Asynchronous Python client for the AdGuard Home API."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .exceptions import AdGuardHomeError

if TYPE_CHECKING:
    from . import AdGuardHome


class AdGuardHomeBlockServices:
    """Controls AdGuard Home parental control."""

    def __init__(self, adguard: AdGuardHome) -> None:
        """Initialize object.

        Args:
            adguard: The AdGuard Home instance.
        """
        self._adguard = adguard

    async def list_services(self) -> list:
        """Return AdGuard Home blocked service list.

        Returns:
            The the blocked service list currently loaded in the
            AdGuard Home instance.
        """
        response = await self._adguard.request("blocked_services/list")
        return response

    async def add_service(self, service: str) -> None:
        """Enable a blocked service to AdGuard Home.

        Args:
            service: The name of the service to be blocked.

        Raises:
            AdGuardHomeError: Failed adding the blocked service.
        """
        enabled_services = await self.list_services()
        if service not in enabled_services:
            enabled_services.append(service)

        try:
            await self._adguard.request(
                "blocked_services/set",
                method="POST",
                json_data=enabled_services,
            )
        except AdGuardHomeError as exception:
            raise AdGuardHomeError(
                "Failed to add the service to AdGuard Blocked services"
            ) from exception

    async def remove_service(self, service: str) -> None:
        """Remove a blocked service from AdGuard Home.

        Args:
            service: The name of the service to be removed.

        Raises:
            AdGuardHomeError: Failed removing the blocked service.
        """
        enabled_services = await self.list_services()
        if service in enabled_services:
            enabled_services.remove(service)

        try:
            await self._adguard.request(
                "blocked_services/set",
                method="POST",
                json_data=enabled_services,
            )
        except AdGuardHomeError as exception:
            raise AdGuardHomeError(
                "Failed to remove the service from AdGuard Blocked services"
            ) from exception

    async def remove_all_services(self) -> None:
        """Remove a all blocked service from AdGuard Home.

        Raises:
            AdGuardHomeError: Failed removing the all blocked services.
        """
        try:
            await self._adguard.request(
                "blocked_services/set",
                method="POST",
                json_data=[],
            )
        except AdGuardHomeError as exception:
            raise AdGuardHomeError(
                "Failed to remove all services from AdGuard Blocked services"
            ) from exception