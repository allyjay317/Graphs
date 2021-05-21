import random

reverse = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}


def findpath(room):
    # Set up
    path_graph = {0: dict.fromkeys(room.get_exits(), "?")}
    # Create quick reference graph for unvisited exits
    path_graph[0]['unvisited'] = room.get_exits()
    random.shuffle(path_graph[0]['unvisited'])
    path = []
    # our stack of rooms with unvisited directions
    with_unvisited = [0]
    while len(with_unvisited) > 0:
        room_id = with_unvisited.pop()
        # Get the list of exits from our path_graph
        exits = path_graph.get(room_id)
        unvisited = exits.get('unvisited')
        # Select a direction from the unvisited directions
        dir = unvisited.pop()
        # Check to see if the location still has unvisited directions
        # If so, add it back to the stack
        if len(unvisited) > 0:
            with_unvisited.append(room_id)
        # Create reference to the room we are traveling to
        new_room = room.get_room_in_direction(dir)
        # Assign id to our current room
        exits[dir] = new_room.id
        # Attempt to see if this room has already had a path_graph key
        # set up
        nr_exits = path_graph.get(new_room.id, None)
        if nr_exits:
            # We've been to this room before, assign direction
            nr_exits[reverse[dir]] = room_id
            # Update unvisited array in the place we've already been
            nr_exits['unvisited'] = []
            for key, id in nr_exits.items():
                if id == "?":
                    nr_exits['unvisited'].append(key)
            if len(nr_exits):
                random.shuffle(nr_exits['unvisited'])
            # If we have exausted all directions in the new location
            # we should remove it from the stack.
            # can also be resolved with a check before we attempt
            # to pop a direction from the location we're in on line 25
            # if doing this is not "right"
            if len(nr_exits['unvisited']) == 0:
                with_unvisited.remove(new_room.id)
            # Check to see if we've already exausted
            # all paths along the loop, and if so, move forward
            # this is likely where the optimization could happen
            # with a bfs that checks to see if we're in a loop so
            # that we always exaust all paths along a loop first
            # and reduce backtracking
            if with_unvisited[-1] == new_room.id:
                room = new_room
                path.append(dir)
            # travel backwards on the path to the last node with
            # unvisited directions
            else:
                backwards, room = travelBack(
                    path_graph, with_unvisited[-1], room)
                path = path + backwards
        # We have never been to this room before
        else:
            # Create the new path_graph node, same as outside
            # the for loop above
            nr_pg = dict.fromkeys(new_room.get_exits(), "?")
            nr_pg[reverse[dir]] = room_id
            nr_pg['first_entered'] = dir
            nr_pg['unvisited'] = []
            for key, id in nr_pg.items():
                if id == "?":
                    nr_pg['unvisited'].append(key)
            if len(nr_pg['unvisited']):
                random.shuffle(nr_pg['unvisited'])
            # assign our new node to the path_graph under the correct
            # room id
            path_graph[new_room.id] = nr_pg
            # check to see if we're at a dead end
            # if not, add new room to the stack of rooms with unvisited
            # locations and move into it
            path.append(dir)
            if len(nr_pg['unvisited']) > 0:
                with_unvisited.append(new_room.id)
                room = new_room
            # we are at a dead end
            else:
                # check to see if this is the last node, if not,
                # move backwards
                if len(with_unvisited):
                    backwards, room = travelBack(
                        path_graph, with_unvisited[-1], new_room)
                    path = path + backwards
    return path

# helper function to find the path back to the last node
# with unvisited locations


def travelBack(path_graph, target, room):
    new_path = []
    while room.id != target:
        dir = reverse[path_graph[room.id]['first_entered']]
        new_path.append(dir)
        room = room.get_room_in_direction(dir)

    return (new_path, room)
