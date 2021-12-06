from gym_minigrid.minigrid import *
from gym_minigrid.wrappers import *
from gym_minigrid.register import register

class DualHallwayEnv(MiniGridEnv):
    def __init__(self, max_steps=10_000, height=6, see_through_walls=False):
        self.max_steps = max_steps
        self.room_height = height + 1

        super().__init__(width=height + 2, height=self.room_height * 4+1, max_steps=max_steps, see_through_walls=see_through_walls)


    def _gen_grid(self, width:int, height:int):
        self.grid = Grid(width, height)

        # starting room
        self.grid.wall_rect(0, 0, width, height)
        # hallways
        self.grid.wall_rect(0,self.room_height,width//2,self.room_height*2+1)
        self.grid.wall_rect(width//2,self.room_height,width - width//2,self.room_height*2+1)
        # last room
        self.grid.wall_rect(0,self.room_height*3,width,self.room_height)

        *door_colors, final_door = self._rand_subset(COLOR_NAMES, 5)

        # place doors for hallways
        for i in range(0,4,2):
            color = door_colors[i]
            self.grid.set(self._rand_int(1,width//2 - 1), self.room_height * (i + 1), Door(color))
            color = door_colors[i+1]
            self.grid.set(self._rand_int(width//2 + 1, width-1), self.room_height * (i + 1), Door(color))

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


register(
    id='MiniGrid-DualHallway-v0',
    entry_point="gym_minigrid.envs:DualHallwayEnv"
)