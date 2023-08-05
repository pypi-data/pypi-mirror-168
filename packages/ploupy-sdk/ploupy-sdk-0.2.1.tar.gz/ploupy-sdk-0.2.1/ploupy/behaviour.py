from functools import partial

from .order import Order
from .orders import PloupyOrder
from .models.core import Pos
from .models.game import Techs
from .core.exceptions import PloupyException
from .game import Game, Probe, Turret, Player, Factory
from .actions import Actions


class Behaviour:
    """
    Behaviour class

    Inherits from this class to define the behaviour of the bot.

    Each instance of the class exposes some useful attributes:
    * config : The game config
    * metadata: The game metadata
    * game : The game instance
    * map : The map instance
    * player : The bot's player instance

    ---

    Define callbacks by overriding the following methods:
    * `on_start`
    * `on_income`
    * `on_factory_build`
    * `on_turret_build`
    * `on_probe_build`
    * `on_move_probes`
    * `on_probes_attack`
    * `on_acquire_tech`

    ---

    To send actions to the server, call one of these methods:
    * `build_factory`
    * `build_turret`
    * `move_probes`
    * `explode_probes`
    * `probes_attack`

    Note: the `Order` concept can also be used to perform actions
    (see `place_order`)
    """

    def __init__(self, uid: str, game: Game, _bind_callbacks: bool = True) -> None:
        self._uid = uid
        self.config = game.config
        self.metadata = game.metadata
        self.game = game
        self.map = game.map
        self.player = self.game.get_player(self._uid)
        if self.player is None:
            raise PloupyException("Can't find own player.")

        if _bind_callbacks:
            self._bind_callbacks()

    def _bind_callbacks(self):
        """
        Bind Behaviour callbacks to corresponding Player callbacks
        """
        self.game.on_order_fail = self._wrap_callback(self.on_order_fail)
        self.player.on_income = self._wrap_callback(self.on_income)

        for player in self.game.players:
            player.on_factory_build = partial(
                self._wrap_callback(self.on_factory_build),
                player=player,
            )
            player.on_turret_build = partial(
                self._wrap_callback(self.on_turret_build),
                player=player,
            )
            player.on_probe_build = partial(
                self._wrap_callback(self.on_probe_build),
                player=player,
            )
            player.on_move_probes = partial(
                self._wrap_callback(self.on_move_probes),
                player=player,
            )
            player.on_probes_attack = partial(
                self._wrap_callback(self.on_probes_attack),
                attacking_player=player,
            )
            player.on_acquire_tech = partial(
                self._wrap_callback(self.on_acquire_tech),
                player=player,
            )

    def _wrap_callback(self, cb):
        async def wrapper(*args, **kwargs):
            await cb(*args, **kwargs)

        return wrapper

    async def place_order(self, order: Order) -> None:
        """
        Place an order

        Try to resolve it directly, if not
        possible, add it to the orders pool
        and tries to resolve it on game state update
        """
        # set player instance for ploupy order
        # -> always bot's player
        if isinstance(order, PloupyOrder):
            order._player = self.player

        await self.game.place_order(order)

    async def build_factory(self, coord: Pos):
        """
        Send an action to the server

        Build a factory on the given coordinates
        (see `BuildFactoryOrder` for related `Order`)

        Raises:
            ActionFailedException: When the action can't be performed
        """
        await Actions.build_factory(self.game._gid, coord)

    async def build_turret(self, coord: Pos):
        """
        Send an action to the server

        Build a turret on the given coordinates
        (see `BuildTurretOrder` for related `Order`)

        Raises:
            ActionFailedException: When the action can't be performed
        """
        await Actions.build_turret(self.game._gid, coord)

    async def move_probes(self, probes: list[Probe], target: Pos):
        """
        Send an action to the server

        Set the target of the given probes (Farm policy),
        the target can not be a tile owned by an opponent player.

        Raises:
            ActionFailedException: When the action can't be performed
        """
        await Actions.move_probes(self.game._gid, probes, target)

    async def explode_probes(self, probes: list[Probe]):
        """
        Send an action to the server

        Explode the given probes immediately

        Raises:
            ActionFailedException: When the action can't be performed
        """
        await Actions.explode_probes(self.game._gid, probes)

    async def probes_attack(self, probes: list[Probe]):
        """
        Send an action to the server

        Orders the given probes to attack,
        they will select an attack target, set it as move target (policy Attack)
        and explode when the target is reached.

        Raises:
            ActionFailedException: When the action can't be performed
        """
        await Actions.probes_attack(self.game._gid, probes)

    async def acquire_tech(self, tech: Techs):
        """
        Send an action to the server

        Acquire the given tech.

        Raises:
            ActionFailedException: When the action can't be performed
        """
        await Actions.acquire_tech(self.game._gid, tech)

    async def on_start(self) -> None:
        """
        Called on start of the game
        """

    async def on_order_fail(self, order: Order) -> None:
        """
        Called when an order fails
        """

    async def on_income(self, money: int) -> None:
        """
        Called when the bot's money is updated

        Note: See `Player.on_income` for callback on opponent players
        """

    async def on_factory_build(self, factory: Factory, player: Player) -> None:
        """
        Called when a factory is built by `player`
        """

    async def on_turret_build(self, turret: Turret, player: Player) -> None:
        """
        Called when a turret is built by `player`
        """

    async def on_probe_build(self, probe: Probe, player: Player) -> None:
        """
        Called when a probe is built by `player`
        """

    async def on_move_probes(
        self, probes: list[Probe], target: Pos, player: Player
    ) -> None:
        """
        Called when some probes of `Player` are given a new target
        """

    async def on_probes_attack(
        self, probes: list[Probe], attacked_player: Player, attacking_player: Player
    ) -> None:
        """
        Called when some `probes` of `attacking_player` are attacking `attacked_player`.

        Note: Only called once by attack, the callback won't be triggered again in
        case one of the probe change its target during the attack
        """

    async def on_acquire_tech(self, tech: Techs, player: Player) -> None:
        """
        Called when `player` acquires a new tech
        """


class BehaviourDispatcher(Behaviour):
    """
    Behaviour dispatcher

    Works with `BehaviourStage` class

    Use this class to encapsulate different stages of the game
    as separate `BehaviourStage` classes.

    Warning:
        Do NOT override from `Behaviour` methods in this class.
        It will be ignored. Instead override these methods in
        `BehaviourStage` classes.
    """

    def __init__(self, uid: str, game: Game) -> None:

        self._current_stage: str | None = None
        self._stages: dict[str, BehaviourStage] = {}

        self._build_dispatchers()

        # must be called after building dispatchers
        # -> callbacks are binded in parent __init__
        super().__init__(uid, game, _bind_callbacks=True)

    def _build_dispatchers(self):
        """
        Build dispatcher in each callback,
        to call the callback of the current stage.
        """
        for attr in dir(self):
            if attr.startswith("on_"):
                setattr(self, attr, self._dispatch_callback(attr))

    def _dispatch_callback(self, cb_name: str):
        async def wrapper(*args, **kwargs):
            stage = self._stages[self._current_stage]
            cb = getattr(stage, cb_name)
            await cb(*args, **kwargs)

        return wrapper

    def add_stage(self, stage: "BehaviourStage") -> None:
        """
        Add a stage to the dispatcher
        """
        self._stages[stage.name] = stage
        if self._current_stage is None:
            self._current_stage = stage.name

    async def set_current_stage(self, stage_name: str) -> None:
        """
        Set the current stage
        """
        if stage_name not in self._stages.keys():
            raise PloupyException(f"Invalid stage name: '{stage_name}'")
        self._current_stage = stage_name

        await self._stages[self._current_stage].on_stage()


class BehaviourStage(Behaviour):
    """
    Behaviour stage

    Use as a standard `Behaviour` class.

    Use `set_current_stage` to change stage.

    A callback is specific to this class:
    * `on_stage`
    """

    def __init__(self, dispatcher: BehaviourDispatcher, name: str) -> None:
        super().__init__(
            uid=dispatcher._uid,
            game=dispatcher.game,
            _bind_callbacks=False,
        )
        self._dispatcher: BehaviourDispatcher = dispatcher
        self.name = name

    async def set_current_stage(self, stage_name: str) -> None:
        """
        Set the current stage
        """
        await self._dispatcher.set_current_stage(stage_name)

    async def on_stage(self) -> None:
        """
        Called when this stage is selected as current.
        """
