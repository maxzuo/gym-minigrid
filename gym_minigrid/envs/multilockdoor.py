from gym_minigrid.minigrid import *
from gym_minigrid.wrappers import *
from gym_minigrid.register import register

class MultiLockDoorEnv(MiniGridEnv):
    def __init__(self, max_steps=10_000, height=6, see_through_walls=False):

        self.max_steps = max_steps
        self.room_height = height

        super().__init__(width=height + 2, height=(self.room_height + 1) * 2 + 1, max_steps=max_steps, see_through_walls=see_through_walls)
        # NOTE: possible refactor


    def _gen_grid(self, width:int, height:int):
        self.grid = Grid(width, height)

        self.grid.wall_rect(0, 0, width, height)

        self.place_agent(top=(1,1), size=(width-2, width-2), rand_dir=True)
        self.target_pos = (self._rand_int(1, width - 1), height - 1)

        wall = self.room_height + 1
        self.grid.horz_wall(0, wall, width)

        key_colors = self._rand_elem(COLOR_SUBGROUP_BY_LEN[3])

        # place keys to the multidoor
        for color in key_colors[:-1]:
            self.place_obj(Key(color), top=(1,1), size=(width-2,width-2))

        # place key to regular door
        self.place_obj(Key(key_colors[-1]), top=(1,width+1), size=(width-2,width-2))

        # place doors 1) multilock 2) regular door
        self.grid.set(self._rand_int(1, width - 1), wall, MultiDoor(key_colors[:-1], is_locked=True))
        self.grid.set(*self.target_pos, Door(key_colors[-1], is_locked=True))

        self.mission = f"Go to the {key_colors[-1]} door"

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
    id='MiniGrid-MultiLockDoor-v0',
    entry_point="gym_minigrid.envs:MultiLockDoorEnv"
)