from typing import Awaitable, Callable

from ploupy.core.exceptions import PloupyException

from .models.game import Techs

from .order import Order
from .game import Tile, Player
from .actions import Actions


class PloupyOrder(Order):
    """
    Internal class
    """

    def __init__(
        self,
        on: Callable[[], bool] | None = None,
        action: Callable[[], Awaitable[None]] | None = None,
        name: str | None = None,
        with_timeout: float | None = None,
        with_retry: bool = True,
    ) -> None:
        super().__init__(
            self._on,
            self._action,
            name=name,
            with_timeout=with_timeout,
            with_retry=with_retry,
        )
        self._player: Player | None = None
        self._custom_on = on if on is not None else lambda: True
        self._custom_action = action

    def _on(self) -> bool:
        if self._player is None:
            raise PloupyException(
                (
                    "Player instance missing. "
                    "Maybe you called Game.place_order instead of Behaviour.place_order ?"
                )
            )
        return True

    async def _action(self) -> None:
        pass


class BuildFactoryOrder(PloupyOrder):
    """
    Order for the build factory action
    """

    def __init__(
        self,
        tile: Tile,
        on: Callable[[], bool] | None = None,
        action: Callable[[], Awaitable[None]] | None = None,
        name: str | None = None,
        with_timeout: float | None = None,
        with_retry: bool = True,
    ) -> None:
        super().__init__(
            on=on,
            action=action,
            name=name,
            with_timeout=with_timeout,
            with_retry=with_retry,
        )
        self._tile = tile

    def _on(self) -> bool:
        return (
            super()._on()
            and self._player.can_build_factory()
            and self._tile.can_build(self._player)
            and self._custom_on()
        )

    async def _action(self) -> None:
        await Actions.build_factory(self._player._game._gid, self._tile.coord)

        if self._custom_action is not None:
            await self._custom_action()


class BuildTurretOrder(PloupyOrder):
    """
    Order for the build turret action
    """

    def __init__(
        self,
        tile: Tile,
        on: Callable[[], bool] | None = None,
        action: Callable[[], Awaitable[None]] | None = None,
        name: str | None = None,
        with_timeout: float | None = None,
        with_retry: bool = True,
    ) -> None:
        super().__init__(
            on=on,
            action=action,
            name=name,
            with_timeout=with_timeout,
            with_retry=with_retry,
        )
        self._tile = tile

    def _on(self) -> bool:
        return (
            super()._on()
            and self._player.can_build_turret()
            and self._tile.can_build(self._player)
            and self._custom_on()
        )

    async def _action(self) -> None:
        await Actions.build_turret(self._player._game._gid, self._tile.coord)

        if self._custom_action is not None:
            await self._custom_action()


class AcquireTechOrder(PloupyOrder):
    """
    Order for the acquire tech action
    """

    def __init__(
        self,
        tech: Techs,
        on: Callable[[], bool] | None = None,
        action: Callable[[], Awaitable[None]] | None = None,
        name: str | None = None,
        with_timeout: float | None = None,
        with_retry: bool = True,
    ) -> None:
        super().__init__(
            on=on,
            action=action,
            name=name,
            with_timeout=with_timeout,
            with_retry=with_retry,
        )
        self._tech = tech

    def _on(self) -> bool:
        if not super()._on():
            return False
        if not self._player.is_tech_acquirable(self._tech):
            self.abort()
            return False
        return self._player.can_acquire_tech(self._tech) and self._custom_on()

    async def _action(self) -> None:
        await Actions.acquire_tech(self._player._game._gid, self._tech)

        if self._custom_action is not None:
            await self._custom_action()
