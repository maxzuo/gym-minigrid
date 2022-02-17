from gym_minigrid.minigrid import *
from gym_minigrid.wrappers import *
from gym_minigrid.register import register

class DualHallwayEnv(MiniGridEnv):
    def __init__(self, max_steps=10_000, height=6, hallway_mult=5, see_through_walls=False,distractor_doors=0):
        self.max_steps = max_steps
        self.room_height = height + 1
        self.hallway_mult = hallway_mult
        self.distractor_doors = distractor_doors

        super().__init__(width=height + 2, height=self.room_height * (self.hallway_mult + 2)+1, max_steps=max_steps, see_through_walls=see_through_walls)


    def _gen_grid(self, width:int, height:int):
        self.grid = Grid(width, height)

        # starting room
        self.grid.wall_rect(0, 0, width, height)
        # hallways
        self.grid.wall_rect(0,self.room_height,width//2,self.room_height*self.hallway_mult+1)
        self.grid.wall_rect(width//2,self.room_height,width - width//2,self.room_height*self.hallway_mult+1)
        # last room
        self.grid.wall_rect(0,self.room_height*(self.hallway_mult+1),width,self.room_height+1)

        *door_colors, final_door = self._rand_subset(COLOR_NAMES[:len(COLOR_NAMES)-self.distractor_doors], 5)

        # place doors for hallways
        for j,i in enumerate(range(0,self.hallway_mult+1,self.hallway_mult)):
            color = door_colors[j]
            self.grid.set(self._rand_int(1,width//2 - 1), self.room_height * (i + 1), Door(color))
            color = door_colors[j+1]
            self.grid.set(self._rand_int(width//2 + 1, width-1), self.room_height * (i + 1), Door(color))

        # place distractor doors
        possible_heights = self._rand_subset(list(range(self.room_height + 1, height - self.room_height, 1)), self.distractor_doors)
        for _,dd_h in enumerate(possible_heights):
            self.grid.set(self._rand_elem((width//2,width//2 - 1)), dd_h, Door(COLOR_NAMES[-(1+_)]))
            self.place_obj(Ball())

        # place final door
        self.target_pos = self._rand_int(1,width-1), height-1
        self.grid.set(*self.target_pos, Door(final_door))

        self.place_agent(top=(1,1), size=(width-2, self.room_height-2), rand_dir=True)

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


class DualHallway_6Env(DualHallwayEnv):
    def __init__(self, *args, hallway_mult=6, **kwargs):
        super().__init__(*args, hallway_mult=hallway_mult, **kwargs)

class DualHallway_7Env(DualHallwayEnv):
    def __init__(self, *args, hallway_mult=7, **kwargs):
        super().__init__(*args, hallway_mult=hallway_mult, **kwargs)

class DualHallway_8Env(DualHallwayEnv):
    def __init__(self, *args, hallway_mult=8, **kwargs):
        super().__init__(*args, hallway_mult=hallway_mult, **kwargs)

class DualHallway_DistractorDoors(DualHallwayEnv):
    def __init__(self, *args, distractor_doors=5, **kwargs):
        super().__init__(*args, distractor_doors=distractor_doors, **kwargs)

register(
    id='MiniGrid-DualHallway-v0',
    entry_point="gym_minigrid.envs:DualHallwayEnv"
)

register(
    id='MiniGrid-DualHallway-6-v0',
    entry_point="gym_minigrid.envs:DualHallway_6Env"
)

register(
    id='MiniGrid-DualHallway-7-v0',
    entry_point="gym_minigrid.envs:DualHallway_7Env"
)

register(
    id='MiniGrid-DualHallway-8-v0',
    entry_point="gym_minigrid.envs:DualHallway_8Env"
)

register(
    id='MiniGrid-DualHallway-DD-v0',
    entry_point="gym_minigrid.envs:DualHallway_DistractorDoors"
)
