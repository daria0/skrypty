# if you move the player during the build the agent's position will change and he won't be able to close the BIRCH_DOOR
# this basically means that all your chickens will escape :(
# and the whole build won't look the way it's supposed to

# global variables
OFFSET = 5
X = 7
Y = 4
Z = 9

def on_on_chat():
    blocks.fill(GRASS,
        pos(-20, -1, -20),
        pos(20, -1, 20),
        FillOperation.REPLACE)
    blocks.fill(AIR,
        pos(-20, 0, -20),
        pos(20, 15, 20),
        FillOperation.REPLACE)
player.on_chat("remove", on_on_chat)


def on_on_chat2(number_of_chickens):
    build_walls()
    build_roof()
    place_details()
    put_lights()
    decorate_henhouse()
    move_in(number_of_chickens)
player.on_chat("build", on_on_chat2)


def build_walls():
    # floor
    blocks.fill(PLANKS_BIRCH,
        pos(OFFSET, -1, OFFSET),
        pos(OFFSET + X, -1, OFFSET + Z),
        FillOperation.REPLACE)

    agent.teleport(pos(OFFSET, 0, OFFSET), EAST)
    agent.set_slot(2)
    agent.set_assist(DESTROY_OBSTACLES, True)
    agent.set_assist(PLACE_ON_MOVE, True)
    # foundations
    for i in (X, Z, X, Z):
        agent.set_item(BRICKS, 64, 2)
        agent.move(FORWARD, i)
        agent.turn(RIGHT_TURN)
    agent.move(UP, 1)
    # walls
    for j in range(Y):
        for n in (X, Z, X, Z):
            agent.set_item(PLANKS_BIRCH, 64, 2)
            agent.move(FORWARD, n)
            agent.turn(RIGHT_TURN)
        agent.move(UP, 1)
        

def build_roof():
    # roof
    for k in range(4):
        blocks.fill(STONE_BRICKS,
            pos(OFFSET + k, Y + 1 + k, OFFSET + k),
            pos(OFFSET + X - k, Y + 1 + k, OFFSET + Z - k),
            FillOperation.REPLACE)


def place_details():
    # windows
    blocks.fill(BIRCH_FENCE,
        pos(OFFSET+2, Y - 1, OFFSET),
        pos(OFFSET+X - 2, Y - 1, OFFSET),
        FillOperation.REPLACE)
    blocks.fill(BIRCH_FENCE,
        pos(OFFSET+2, Y - 1, OFFSET+Z),
        pos(OFFSET+X - 2, Y - 1, OFFSET+Z),
        FillOperation.REPLACE)
    blocks.place(BIRCH_FENCE, pos(OFFSET, Y - 1, OFFSET+2))
    blocks.place(BIRCH_FENCE, pos(OFFSET+X, Y - 1, OFFSET+2))
    blocks.place(BIRCH_FENCE, pos(OFFSET, Y - 1, OFFSET+Z - 2))
    blocks.place(BIRCH_FENCE, pos(OFFSET+X, Y - 1, OFFSET+Z - 2))
    # doors
    blocks.place(BIRCH_DOOR, pos(OFFSET+X / 2, 0, OFFSET+Z))
    agent.teleport(pos(OFFSET+X / 2, 0,OFFSET+ Z + 1), NORTH)
    agent.interact(FORWARD)
    blocks.fill(AIR,
        pos(OFFSET, 0, OFFSET+Z / 2),
        pos(OFFSET, 0, OFFSET+Z / 2 + 1),
        FillOperation.REPLACE)


def put_lights():
    # lighting
    agent.set_item(TORCH, 4, 1)
    agent.set_slot(1)
    agent.teleport(pos(OFFSET-1, 2, OFFSET+1), EAST)
    agent.place(FORWARD)
    agent.teleport(pos(OFFSET-1, 2, OFFSET+Z - 1), EAST)
    agent.place(FORWARD)
    agent.teleport(pos(OFFSET+X / 2 - 1, 2, OFFSET+1), NORTH)
    agent.place(FORWARD)
    agent.teleport(pos(OFFSET+X / 2 - 1, 2, OFFSET+Z-1), SOUTH)
    agent.place(FORWARD)
    
    
def decorate_henhouse():
    # fence
    agent.teleport(pos(OFFSET-1, 0, OFFSET+1), WEST)
    agent.set_assist(DESTROY_OBSTACLES, False)
    agent.set_item(BIRCH_FENCE, 64, 3)
    agent.set_slot(3)
    agent.move(FORWARD, X)
    agent.move(LEFT, Z-2)
    agent.teleport(pos(OFFSET-1, 0, OFFSET+Z-1), WEST)
    agent.move(FORWARD, X+1)
    # hay
    blocks.place(HAY_BLOCK, pos(OFFSET+1, 0, OFFSET+Z - 2))
    blocks.place(HAY_BLOCK, pos(OFFSET+1, 0, OFFSET+Z - 1))
    blocks.place(HAY_BLOCK, pos(OFFSET+1, 1, OFFSET+Z - 1))
    blocks.place(HAY_BLOCK, pos(OFFSET+2, 0, OFFSET+Z - 1))
    # pool
    blocks.fill(WATER, pos(OFFSET+1, -1, OFFSET+1), pos(OFFSET+1, -1, OFFSET+3), FillOperation.REPLACE)
    # perches
    blocks.fill(PLANKS_BIRCH,
        pos(OFFSET+X - 1, 0, OFFSET+1),
        pos(OFFSET+X - 1, 1, OFFSET+Z - 1),
        FillOperation.REPLACE)
    blocks.fill(PLANKS_BIRCH,
        pos(OFFSET+X - 2, 0, OFFSET+1),
        pos(OFFSET+X - 2, 0, OFFSET+Z - 1),
        FillOperation.REPLACE)
    blocks.place(BIRCH_FENCE, pos(OFFSET+X - 2, 1, OFFSET+3))
    blocks.place(BIRCH_FENCE, pos(OFFSET+X - 2, 2, OFFSET+3))
    blocks.place(BIRCH_FENCE, pos(OFFSET+X - 1, 2, OFFSET+3))
    blocks.place(BIRCH_FENCE, pos(OFFSET+X - 2, 1, OFFSET+Z - 3))
    blocks.place(BIRCH_FENCE, pos(OFFSET+X - 2, 2, OFFSET+Z - 3))
    blocks.place(BIRCH_FENCE, pos(OFFSET+X - 1, 2, OFFSET+Z - 3))


def move_in(number_of_chickens: any):
    # chickens
    for i in range(number_of_chickens):
        mobs.spawn(CHICKEN, pos(OFFSET+X / 2, 0, OFFSET+Z / 2))
