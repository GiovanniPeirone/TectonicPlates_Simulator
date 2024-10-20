import pygame

class map:
    
    def __init__(self, widhgt, height) -> None:
        self.widhgt = widhgt
        self.height = height


    def Maping(self):
        tall_default = 1

        world_Arr = []

        for i in world_Arr:
            for o in world_Arr:
                world_Arr[i][o].append(1)

        print(world_Arr)

        return world_Arr
            