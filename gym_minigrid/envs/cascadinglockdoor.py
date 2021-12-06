from gym_minigrid.minigrid import *
from gym_minigrid.wrappers import *
from gym_minigrid.register import register

class CascadingLockDoorEnv(MiniGridEnv):
    def __init__(self, max_steps=10_000, height=6, num_rooms=2, see_through_walls=False):

        assert 0 < num_rooms <= 4

        self.max_steps = max_steps
        self.room_height = height
        self.num_rooms = num_rooms
        self.doors = [None for i in range(self.num_rooms)]

        super().__init__(width=height + 2, height=(self.room_height + 1) * self.num_rooms + 1, max_steps=max_steps, see_through_walls=see_through_walls)

    def _gen_grid(self, width:int, height:int):
        self.grid = Grid(width, height)

        self.grid.wall_rect(0, 0, width, height)

        self.place_agent(top=(1,1), size=(width-2, width-2), rand_dir=True)
        self.target_pos = (self._rand_int(1, width - 1), height - 1)

        colors = self._rand_elem(COLOR_SUBGROUP_BY_LEN[self.num_rooms])[::-1]

        for i in range(len(colors)):
            y = (i + 1) * (self.room_height + 1)
            self.grid.horz_wall(0, y, width)
            self.target_pos = (self._rand_int(1, width - 1), y)

            self.doors[i] = MultiDoor(colors[:i+1][::-1], is_locked=True)
            self.grid.set(*self.target_pos, self.doors[i])
            self.place_obj(Key(colors[i]), top=(1, (self.room_height + 1) * i + 1), size=(self.room_height, self.room_height))

            self.mission = f"Go to the {colors[i]} door"

    def step(self, action):
        obs, reward, done, info = super().step(action)

        ax, ay = self.agent_pos
        tx, ty = self.target_pos

        if action == self.actions.done or (self.agent_pos == self.target_pos).all():
            if (ax == tx and abs(ay - ty) == 1) or (ay == ty and abs(ax - tx) == 1):
                reward = self._reward()
            done = True

        return obs, reward, done, info

class CascadingLockDoor_3Env(CascadingLockDoorEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=3, **kwargs)

class CascadingLockDoor_4Env(CascadingLockDoorEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=4, **kwargs)

class CascadingLockDoor_5Env(CascadingLockDoorEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=5, **kwargs)


register(
    id='MiniGrid-CascadingLockDoor-v0',
    entry_point="gym_minigrid.envs:CascadingLockDoorEnv"
)

register(
    id='MiniGrid-CascadingLockDoor-3-v0',
    entry_point="gym_minigrid.envs:CascadingLockDoor_3Env"
)

register(
    id='MiniGrid-CascadingLockDoor-4-v0',
    entry_point="gym_minigrid.envs:CascadingLockDoor_4Env"
)