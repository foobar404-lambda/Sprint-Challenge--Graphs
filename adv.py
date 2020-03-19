from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


def getPath(start, room_count):
    stack = [start]
    visited = {}
    prev = None
    path = []

    while len(stack) > 0:
        room = stack[-1]
        visited[room.name] = True

        if prev:
            path.append(prev.relationship(room))

        exits = []
        for dir_ in room.get_exits():
            exits.append(room.get_room_in_direction(dir_))

        new_rooms = []
        for exit_ in exits:
            if exit_.name not in visited:
                new_rooms.append(exit_)

        if len(new_rooms) == 0:
            stack = stack[:-1]
        else:
            stack.append(new_rooms[0])

        prev = room

        if len(visited) == room_count:
            break

    return path


traversal_path = getPath(player.current_room, len(world.rooms))


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
