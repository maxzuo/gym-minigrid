from gym_minigrid.minigrid import *
from gym_minigrid.wrappers import *
from gym_minigrid.register import register

class KeyDoorEnv(MiniGridEnv):
    def __init__(self, max_steps=100_000, see_through_walls=True):
        super().__init__(grid_size=50, max_steps=max_steps, see_through_walls=see_through_walls)

        self.max_steps = max_steps

    def _gen_grid(self, width:int, height:int):
        self.grid = Grid(width, height)

        width = self._rand_int(5, width+1)
        height = self._rand_int(5, height+1)

        self.grid.wall_rect(0, 0, width, height)
        self.place_agent(size=(3, 3))

        self.target_pos = doorPos = (self._rand_int(2, width-2), height - 1)
        doorColor = self._rand_elem(COLOR_NAMES)
        doorKey = Key(doorColor)

        self.grid.set(*doorPos, Door(doorColor, is_locked=True))
        self.grid.set(*(width - 2, self._rand_int(2,4)), doorKey)

        self.mission = f"Go to the {doorColor} door"

    def step(self, action):
        obs, reward, done, info = super().step(action)

        ax, ay = self.agent_pos
        tx, ty = self.target_pos

        if action == self.actions.done or (self.agent_pos == self.target_pos).all():
            if (ax == tx and abs(ay - ty) == 1) or (ay == ty and abs(ax - tx) == 1):
                reward = self._reward()
            done = True

        return obs, reward, done, info


register(
    id='MiniGrid-KeyDoor-v0',
    entry_point=KeyDoorEnv
)