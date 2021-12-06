from itertools import product

from gym_minigrid.minigrid import *
from gym_minigrid.wrappers import *
from gym_minigrid.register import register

class LockedHallwayEnv(MiniGridEnv):
    def __init__(self, max_steps=100_000, height=10, num_rooms=8, see_through_walls=False):

        self.max_steps = max_steps
        self.room_height = height
        self.num_rooms = num_rooms

        super().__init__(width=height, height=(self.room_height + 1) * num_rooms + 1, max_steps=max_steps, see_through_walls=see_through_walls)


    def _gen_grid(self, width:int, height:int):
        self.grid = Grid(width, height)

        self.grid.wall_rect(0, 0, width, height)
        self.place_agent(size=(5, 5), rand_dir=True)

        for i,color in enumerate(self._rand_subset(COLOR_NAMES, self.num_rooms)):
            y = (i + 1) * (self.room_height + 1)
            self.grid.horz_wall(0, y, width)
            self.target_pos = (self._rand_int(1, width - 1), y)

            self.grid.set(*self.target_pos, Door(color, is_locked=True))
            self.place_obj(Key(color), top=(0, (self.room_height + 1) * i), size=(self.room_height, self.room_height))

            self.mission = f"Go to the {color} door"

    def step(self, action):
        obs, reward, done, info = super().step(action)

        ax, ay = self.agent_pos
        tx, ty = self.target_pos

        if action == self.actions.done or (self.agent_pos == self.target_pos).all():
            if (ax == tx and abs(ay - ty) == 1) or (ay == ty and abs(ax - tx) == 1):
                reward = self._reward()
            done = True

        return obs, reward, done, info

class LockedHallwayEnv_6rooms(LockedHallwayEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=6, **kwargs)

class LockedHallwayEnv_7rooms(LockedHallwayEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=7, **kwargs)

class LockedHallwayEnv_8rooms(LockedHallwayEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=8, **kwargs)


class LockedHallway2Env(MiniGridEnv):
    def __init__(self, max_steps=10_000, height=10, num_rooms=5):

        # All keys are in the first room

        self.max_steps = max_steps
        self.room_height = height
        self.num_rooms = num_rooms

        super().__init__(width=height, height=(self.room_height + 1) * num_rooms + 1, max_steps=max_steps, see_through_walls=True)


    def _gen_grid(self, width:int, height:int):
        self.grid = Grid(width, height)

        self.grid.wall_rect(0, 0, width, height)
        self.place_agent(size=(5, 5), rand_dir=True)

        for i,color in enumerate(self._rand_subset(COLOR_NAMES, self.num_rooms)):
            y = (i + 1) * (self.room_height + 1)
            self.grid.horz_wall(0, y, width)
            self.target_pos = (self._rand_int(1, width - 1), y)

            self.grid.set(*self.target_pos, Door(color, is_locked=True))
            self.place_obj(Key(color), top=(0, 0), size=(self.room_height, self.room_height + 1))

            self.mission = f"Go to the {color} door"

    def step(self, action):
        obs, reward, done, info = super().step(action)

        ax, ay = self.agent_pos
        tx, ty = self.target_pos

        if action == self.actions.done or (self.agent_pos == self.target_pos).all():
            if (ax == tx and abs(ay - ty) == 1) or (ay == ty and abs(ax - tx) == 1):
                reward = self._reward()
            done = True

        return obs, reward, done, info

class LockedHallway2Env_6rooms(LockedHallway2Env):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=6, **kwargs)

class LockedHallway2Env_7rooms(LockedHallway2Env):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=7, **kwargs)

class LockedHallway2Env_8rooms(LockedHallway2Env):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=8, **kwargs)

class LockedHallway3Env(MiniGridEnv):
    def __init__(self, max_steps=10_000, height=10, num_rooms=5):

        # All keys are in the first room

        self.max_steps = max_steps
        self.room_height = height
        self.num_rooms = num_rooms

        super().__init__(width=height, height=(self.room_height + 1) * num_rooms + 1, max_steps=max_steps, see_through_walls=True)


    def _gen_grid(self, width:int, height:int):
        self.grid = Grid(width, height)

        self.grid.wall_rect(0, 0, width, height)
        self.place_agent(size=(5, 5), rand_dir=True)

        for i,color in enumerate(self._rand_subset(COLOR_NAMES, self.num_rooms)):
            y = (i + 1) * (self.room_height + 1)
            self.grid.horz_wall(0, y, width)
            self.target_pos = (self._rand_int(1, width - 1), y)

            self.grid.set(*self.target_pos, Door(color, is_locked=True))
            self.place_obj(Key(color), top=(0, 0), size=(self.room_height, (self.room_height + 1) * (i + 1)))

            self.mission = f"Go to the {color} door"

    def step(self, action):
        obs, reward, done, info = super().step(action)

        ax, ay = self.agent_pos
        tx, ty = self.target_pos

        if action == self.actions.done or (self.agent_pos == self.target_pos).all():
            if (ax == tx and abs(ay - ty) == 1) or (ay == ty and abs(ax - tx) == 1):
                reward = self._reward()
            done = True

        return obs, reward, done, info



class LockedHallway3Env_6rooms(LockedHallway3Env):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=6, **kwargs)

class LockedHallway3Env_7rooms(LockedHallway3Env):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=7, **kwargs)

class LockedHallway3Env_8rooms(LockedHallway3Env):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, num_rooms=8, **kwargs)

register(
    id='MiniGrid-LockedHallway-v0',
    entry_point=LockedHallwayEnv
)

register(
    id='MiniGrid-LockedHallway-6-v0',
    entry_point=LockedHallwayEnv_6rooms
)
register(
    id='MiniGrid-LockedHallway-7-v0',
    entry_point=LockedHallwayEnv_7rooms
)
register(
    id='MiniGrid-LockedHallway-8-v0',
    entry_point=LockedHallwayEnv_8rooms
)

register(
    id='MiniGrid-LockedHallway-v1',
    entry_point=LockedHallway2Env
)

register(
    id='MiniGrid-LockedHallway-6-v1',
    entry_point=LockedHallway2Env_6rooms
)

register(
    id='MiniGrid-LockedHallway-7-v1',
    entry_point=LockedHallway2Env_7rooms
)

register(
    id='MiniGrid-LockedHallway-8-v1',
    entry_point=LockedHallway2Env_8rooms
)


register(
    id='MiniGrid-LockedHallway-v2',
    entry_point=LockedHallway3Env
)

register(
    id='MiniGrid-LockedHallway-6-v2',
    entry_point=LockedHallway3Env_6rooms
)

register(
    id='MiniGrid-LockedHallway-7-v2',
    entry_point=LockedHallway3Env_7rooms
)

register(
    id='MiniGrid-LockedHallway-8-v2',
    entry_point=LockedHallway3Env_8rooms
)