from gym_minigrid.minigrid import *
from gym_minigrid.wrappers import *
from gym_minigrid.register import register

class SidewaysDualHallwayEnv(MiniGridEnv):
    def __init__(self, max_steps=10_000, width=6, hallway_mult=5, see_through_walls=False):
        self.max_steps = max_steps
        self.room_width = width + 1
        self.hallway_mult = hallway_mult

        super().__init__(width=self.room_width * (self.hallway_mult + 2)+1, height=self.room_width, max_steps=max_steps, see_through_walls=see_through_walls)


    def _gen_grid(self, width:int, height:int):
        self.grid = Grid(width, height)

        # starting room
        self.grid.wall_rect(0, 0, width, height)
        # hallways
        self.grid.wall_rect(self.room_width,0,self.room_width*self.hallway_mult+1,height//2+1)
        self.grid.wall_rect(self.room_width,height//2,self.room_width*self.hallway_mult+1,height - height//2)
        # # last room
        self.grid.wall_rect(self.room_width*(self.hallway_mult+1),0,self.room_width+1,height)

        *door_colors, final_door = self._rand_subset(COLOR_NAMES, 5)

        # place doors for hallways
        for j,i in enumerate(range(0,self.hallway_mult+1,self.hallway_mult)):
            color = door_colors[j]
            self.grid.set( self.room_width * (i + 1), self._rand_int(1,height//2 - 1), Door(color))
            color = door_colors[j+1]
            self.grid.set(self.room_width * (i + 1), self._rand_int(height//2 + 1, height-1), Door(color))

        # place final door
        self.target_pos = width-1, self._rand_int(1,height-1)
        self.grid.set(*self.target_pos, Door(final_door))

        self.place_agent(top=(1,1), size=(self.room_width-2, height-2), rand_dir=True)

        self.mission = f"Go to the {final_door} door"

    def step(self, action):
        obs, reward, done, info = super().step(action)

        ax, ay = self.agent_pos
        tx, ty = self.target_pos

        if action == self.actions.done or (self.agent_pos == self.target_pos).all():
            if (ax == tx and abs(ay - ty) == 1) or (ay == ty and abs(ax - tx) == 1):
                reward = self._reward()
            done = True

        return obs, reward, done, info


class SidewaysDualHallway_6Env(SidewaysDualHallwayEnv):
    def __init__(self, *args, hallway_mult=6, **kwargs):
        super().__init__(*args, hallway_mult=hallway_mult, **kwargs)

class SidewaysDualHallway_7Env(SidewaysDualHallwayEnv):
    def __init__(self, *args, hallway_mult=7, **kwargs):
        super().__init__(*args, hallway_mult=hallway_mult, **kwargs)

class SidewaysDualHallway_8Env(SidewaysDualHallwayEnv):
    def __init__(self, *args, hallway_mult=8, **kwargs):
        super().__init__(*args, hallway_mult=hallway_mult, **kwargs)

register(
    id='MiniGrid-SidewaysDualHallway-v0',
    entry_point="gym_minigrid.envs:SidewaysDualHallwayEnv"
)

register(
    id='MiniGrid-SidewaysDualHallway-6-v0',
    entry_point="gym_minigrid.envs:SidewaysDualHallwayEnv"
)

register(
    id='MiniGrid-SidewaysDualHallway-7-v0',
    entry_point="gym_minigrid.envs:DualHallwayEnv"
)

register(
    id='MiniGrid-SidewaysDualHallway-8-v0',
    entry_point="gym_minigrid.envs:SidewaysDualHallwayEnv"
)