# [Ploupy Python SDK](https://github.com/Plouc314/ploupy-python-sdk)

## Installation

```
pip install ploupy-sdk
```

> **Note**  
> This library requires python 3.10 or higher

## Getting started

Here is a minimal example:

```python
import ploupy as pp

class MyBehaviour(pp.Behaviour):
    pass  # the bot code goes here

BOT_KEY = "..." # the key given when creating the bot

bot = pp.Bot(bot_key=BOT_KEY, behaviour_class=MyBehaviour)

if __name__ == "__main__":
    bot.run()
```

## Behaviour

The SDK is events driven. Define the bot by inheriting from the `Behaviour` class
and overriding callback methods.

### Callbacks

All callbacks are asynchronous methods, to allow to perform orders and other IO bound
tasks. They are automatically called when receiving updates from the server.

> **Warning**  
> Time-consuming tasks (typically where there is a `sleep` call) should not be executed
> directly in a callback, as this could block another callback from being executed.
> Instead use the `start_background_task` to execute the task in parrallel.

```python
# this function is very time-consuming
# calling directly in on_turret_build would
# potentially delay other callbacks by several seconds
async def time_consuming_task(behaviour: pp.Behaviour) -> None:
    
    # wait for 5 seconds to give opponents a chance
    await pp.sleep(5)

    tile = behaviour.map.get_tile((10,10))

    # build a new factory
    await behaviour.place_order(pp.BuildFactoryOrder(tile))


class MyBehaviour(pp.Behaviour):

    async def on_turret_build(self, turret: pp.Turret, player: pp.Player) -> None:
        # check that it is the bot that builded the turret
        if player is not self.player:
            return

        # acquire a new tech, this is IO bound (thus the await)
        # but not time-consuming (a requests over a websocket)
        await self.place_order(pp.AcquireTechOrder(pp.Techs.TURRET_SCOPE))

        # start a task in parrallel to avoid delaying other callbacks
        pp.start_background_task(time_consuming_task, self)
```

### Attributes

The `Behaviour` class expose some useful instances of the game,
such as: 
- `game (Game)`: the game instance
- `map (Map)`: the game's map
- `player (Player)`: the bot's Player
- `config (GameConfig)`: The game configuration

Here is an example of a bot that build a factory as soon as he can:

```python
import ploupy as pp

class MyBehaviour(pp.Behaviour):

    async def on_income(self, money: int) -> None:
        # select the tile to build the factory on
        # using Map instance exposed by Behaviour class
        # and the bot's Player instance
        tiles = self.map.get_buildable_tiles(self.player)
        if len(tiles) == 0:
            return
        
        # get one of the possible tiles
        tile = tiles.pop() # tiles is a set

        # check if the bot has enough money
        # using GameConfig instance exposed by Behaviour class
        if money >= self.config.factory_price:
            # send an action to the server
            # this can failed if all the necessary conditions aren't
            # met to perform the action
            try:
                await self.build_factory(tile.coord)
            except pp.ActionFailedException:
                return
```

### Tiles & geometry

The `geometry` module and `Map` class provide utility functions / methods to
work with coordinates / tiles.

Here is an example of a bot that will try to build a turret when attacked:

```python
import ploupy as pp

class MyBehaviour(pp.Behaviour):

    async def on_probes_attack(
        self,
        probes: list[pp.Probe],
        attacked_player: pp.Player,
        attacking_player: pp.Player,
    ) -> None:
        # check that it is the bot that is attacked
        if attacked_player is not self.player:
            return

        # get the center of where the probes are attacking
        target = pp.geometry.center([probe.target for probe in probes])

        # get tiles where a turret could be built
        tiles = self.map.get_buildable_tiles(self.player)

        # if none are buildable then too bad...
        if len(tiles) == 0:
            return

        # get the tile that is as close as possible to the center of the attack
        tile = pp.geometry.closest_tile(tiles, target)

        # place an order on "build turret" action, the action will be performed
        # when the necessary conditions are met
        await self.place_order(
            pp.BuildTurretOrder(
                tile,
                with_timeout=2.0, # maximum time (sec) before aborting the order
            )
        )

```

### Stages

As the complexity of the bot grows, it can become very handy to encapsulate different
types of behaviour. This can be done by defining multiple `BehaviourStage` (which is essentially
the same as `Behaviour`) and grouping them in a `BehaviourDispatcher`.

Here is an example that splits the game into different stages:

```python
import ploupy as pp

class EarlyStage(pp.BehaviourStage):
    def __init__(self, dispatcher: pp.BehaviourDispatcher) -> None:
        super().__init__(dispatcher, "early")  # specify stage name

    ...  # the bot's behaviour in early game

class MidStage(pp.BehaviourStage):
    def __init__(self, dispatcher: pp.BehaviourDispatcher) -> None:
        super().__init__(dispatcher, "mid")
    
    async def on_income(self, money: int) -> None:
        
        # switch of BehaviourStage
        await self.set_current_stage("end")

class EndStage(pp.BehaviourStage):
    def __init__(self, dispatcher: pp.BehaviourDispatcher) -> None:
        super().__init__(dispatcher, "end")

    async def on_stage(self) -> None:
        ...  # this callback is called when the stage is selected as current stage

# regroup all stages into one behaviour
class BotBehaviour(pp.BehaviourDispatcher):
    def __init__(self, uid: str, game: pp.Game) -> None:
        super().__init__(uid, game)

        self.add_stage(EarlyStage(self))
        self.add_stage(MidStage(self))
        self.add_stage(EndStage(self))

```
