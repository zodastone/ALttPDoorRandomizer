import random
import collections
import logging

from BaseClasses import RegionType, DoorType, Direction, RegionChunk, Sector
from Dungeons import hyrule_castle_regions, eastern_regions, desert_regions

def link_doors(world, player):

    # Drop-down connections & push blocks
    for exitName, regionName in mandatory_connections:
        connect_simple_door(world, exitName, regionName, player)
    # These should all be connected for now as normal connections
    for edge_a, edge_b in intratile_doors:
        connect_intertile_door(world, edge_a, edge_b, player)

    # These connection are here because they are currently unable to be shuffled
    if world.doorShuffle not in ['basic', 'experimental']:  # these modes supports spirals
        for entrance, ext in spiral_staircases:
            connect_two_way(world, entrance, ext, player)
    for entrance, ext in straight_staircases:
        connect_two_way(world, entrance, ext, player)
    for entrance, ext in open_edges:
        connect_two_way(world, entrance, ext, player)
    for exitName, regionName in falldown_pits:
        connect_simple_door(world, exitName, regionName, player)
    for exitName, regionName in dungeon_warps:
        connect_simple_door(world, exitName, regionName, player)

    if world.doorShuffle == 'vanilla':
        for entrance, ext in default_door_connections:
            connect_two_way(world, entrance, ext, player)
        for ent, ext in default_one_way_connections:
            connect_one_way(world, ent, ext, player)
    elif world.doorShuffle == 'basic':
        within_dungeon(world, player)
    elif world.doorShuffle == 'crossed':
        cross_dungeon(world, player)
    elif world.doorShuffle == 'experimental':
        experiment(world, player)

    mark_regions(world, player)
    if world.doorShuffle != 'vanilla':
        create_door_spoiler(world, player)


def mark_regions(world, player):
    # traverse dungeons and make sure dungeon property is assigned
    playerDungeons = [dungeon for dungeon in world.dungeons if dungeon.player == player]
    for dungeon in playerDungeons:
        queue = collections.deque(dungeon.regions)
        while len(queue) > 0:
            region = world.get_region(queue.popleft(), player)
            if region.name not in dungeon.regions:
                dungeon.regions.append(region.name)
                region.dungeon = dungeon
            for ext in region.exits:
                d = world.check_for_door(ext.name, player)
                connected = ext.connected_region
                if d is not None and connected is not None:
                    if d.dest is not None and connected.name not in dungeon.regions and connected.type == RegionType.Dungeon and connected.name not in queue:
                        queue.append(connected)  # needs to be added
                elif connected is not None and connected.name not in dungeon.regions and connected.type == RegionType.Dungeon and connected.name not in queue:
                    queue.append(connected)  # needs to be added


def create_door_spoiler(world, player):
    logger = logging.getLogger('')
    queue = collections.deque(world.doors)
    while len(queue) > 0:
        door_a = queue.popleft()
        if door_a.type in [DoorType.Normal, DoorType.SpiralStairs]:
            door_b = door_a.dest
            if door_b is not None:
                logger.info('spoiler: %s connected to %s', door_a.name, door_b.name)
                if not door_a.blocked and not door_b.blocked:
                    world.spoiler.set_door(door_a.name, door_b.name, 'both', player)
                elif door_a.blocked:
                    world.spoiler.set_door(door_b.name, door_a.name, 'entrance', player)
                elif door_b.blocked:
                    world.spoiler.set_door(door_a.name, door_b.name, 'entrance', player)
                else:
                    logger.warning('This is a bug')
                if door_b in queue:
                    queue.remove(door_b)
                else:
                    logger.info('Door not found in queue: %s connected to %s', door_b.name, door_a.name)
            else:
                logger.info('Door not connected: %s', door_a.name)


# some useful functions
def switch_dir(direction):
    oppositemap = {
        Direction.South: Direction.North,
        Direction.North: Direction.South,
        Direction.West: Direction.East,
        Direction.East: Direction.West,
        Direction.Up: Direction.Down,
        Direction.Down: Direction.Up,
    }
    return oppositemap[direction]


def connect_simple_door(world, exit_name, region_name, player):
    region = world.get_region(region_name, player)
    world.get_entrance(exit_name, player).connect(region)
    d = world.check_for_door(exit_name, player)
    if d is not None:
        d.dest = region


def connect_intertile_door(world, edge_1, edge_2, player):
    ent_a = world.get_entrance(edge_1, player)
    ent_b = world.get_entrance(edge_2, player)

    # if these were already connected somewhere, remove the backreference
    if ent_a.connected_region is not None:
        ent_a.connected_region.entrances.remove(ent_a)
    if ent_b.connected_region is not None:
        ent_b.connected_region.entrances.remove(ent_b)

    ent_a.connect(ent_b.parent_region)
    ent_b.connect(ent_a.parent_region)


def connect_two_way(world, entrancename, exitname, player):
    entrance = world.get_entrance(entrancename, player)
    ext = world.get_entrance(exitname, player)

    # if these were already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)
    if ext.connected_region is not None:
        ext.connected_region.entrances.remove(ext)

    # todo - access rules for the doors...
    entrance.connect(ext.parent_region)
    ext.connect(entrance.parent_region)
    if entrance.parent_region.dungeon:
        ext.parent_region.dungeon = entrance.parent_region.dungeon
    x = world.check_for_door(entrancename, player)
    y = world.check_for_door(exitname, player)
    if x is not None:
        x.dest = y
    if y is not None:
        y.dest = x


def connect_one_way(world, entrancename, exitname, player):
    entrance = world.get_entrance(entrancename, player)
    ext = world.get_entrance(exitname, player)

    # if these were already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance, player)
    if ext.connected_region is not None:
        ext.connected_region.entrances.remove(ext)

    entrance.connect(ext.parent_region)
    if entrance.parent_region.dungeon:
        ext.parent_region.dungeon = entrance.parent_region.dungeon
    x = world.check_for_door(entrancename, player)
    y = world.check_for_door(exitname, player)
    if x is not None:
        x.dest = y
    if y is not None:
        y.dest = x


def within_dungeon(world, player):
    dungeon_region_lists = [hyrule_castle_regions, eastern_regions, desert_regions]
    for region_list in dungeon_region_lists:
        shuffle_dungeon(world, player, region_list)


def shuffle_dungeon(world, player, dungeon_region_names):
    logger = logging.getLogger('')
    available_regions = []
    for name in dungeon_region_names:
        available_regions.append(world.get_region(name, player))
    random.shuffle(available_regions)
    
    # Pick a random region and make its doors the open set
    # TODO: It would make sense to start with the entrance but I'm not sure it's needed.
    available_doors = []
    region = available_regions.pop()
    print("Starting in " + region.name)
    available_doors.extend(get_doors(world, region, player))
    
    # Loop until all available doors are used
    while len(available_doors) > 0:
        # Pick a random available door to connect
        # TODO: Is there an existing "remove random from list" in this codebase?
        random.shuffle(available_doors)
        door = available_doors.pop()
        logger.info('Linking %s', door.name)
        # Find an available region that has a compatible door
        connect_region, connect_door = find_compatible_door_in_regions(world, door, available_regions, player)
        if connect_region is not None:
            logger.info('  Found new region %s via %s', connect_region.name, connect_door.name)
            # Apply connection and add the new region's doors to the available list
            maybe_connect_two_way(world, door, connect_door, player)
            available_doors.extend(get_doors(world, connect_region, player))
            # We've used this region and door, so don't use them again
            available_regions.remove(connect_region)
            available_doors.remove(connect_door)
        else:
            # If there's no available region with a door, use an internal connection
            connect_door = find_compatible_door_in_list(world, door, available_doors, player)
            if connect_door is not None:
                logger.info('  Adding loop via %s', connect_door.name)
                maybe_connect_two_way(world, door, connect_door, player)
                available_doors.remove(connect_door)
    # Check that we used everything, and retry if we failed
    if len(available_regions) > 0 or len(available_doors) > 0:
      logger.info('Failed to add all regions to dungeon, trying again.')
      shuffle_dungeon(world, player, dungeon_region_names)

# Connects a and b. Or don't if they're an unsupported connection type.
# TODO: This is gross, don't do it this way
def maybe_connect_two_way(world, a, b, player):
    if a.type in [DoorType.Open, DoorType.StraightStairs, DoorType.Hole, DoorType.Warp]:
        return
    connect_two_way(world, a.name, b.name, player)

# Finds a compatible door in regions, returns the region and door
def find_compatible_door_in_regions(world, door, regions, player):
    for region in regions:
        for proposed_door in get_doors(world, region, player):
            if doors_compatible(door, proposed_door):
                return region, proposed_door
    return None, None


def find_compatible_door_in_list(world, door, doors, player):
    for proposed_door in doors:
        if doors_compatible(door, proposed_door):
            return proposed_door


def get_doors(world, region, player):
    res = []
    for exit in region.exits:
        door = world.check_for_door(exit.name, player)
        if door is not None:
            res.append(door)
    return res


def doors_compatible(a, b):
    if a.type != b.type:
        return False
    if a.type == DoorType.Open:
        return doors_fit_mandatory_pair(open_edges, a, b)
    if a.type == DoorType.StraightStairs:
        return doors_fit_mandatory_pair(straight_staircases, a, b)
    if a.type == DoorType.Hole:
        return doors_fit_mandatory_pair(falldown_pits_as_doors, a, b)
    if a.type == DoorType.Warp:
        return doors_fit_mandatory_pair(dungeon_warps_as_doors, a, b)
    return a.direction == switch_dir(b.direction)


def doors_fit_mandatory_pair(pair_list, a, b):
  for pair_a, pair_b in pair_list:
      if (a.name == pair_a and b.name == pair_b) or (a.name == pair_b and b.name == pair_a):
          return True
  return False


# code below is an early prototype for cross-dungeon mode
def cross_dungeon(world, player):
    logger = logging.getLogger('')

    # figure out which dungeons have open doors and which doors still need to be connected

    # goals:
    # 1. have enough chests to be interesting (2 more than dungeon items)
    # 2. have a balanced amount of regions added
    # 3. prevent soft locks due to key usage
    # 4. rules in place to affect item placement (lamp, keys, etc.)
    # 5. to be complete -- all doors linked
    # 6. avoid deadlocks/dead end dungeon
    # 7. certain paths through dungeon must be possible - be able to reach goals

    available_dungeon_regions = set([])
    for region in world.regions:
        if region.type == RegionType.Dungeon:
            available_dungeon_regions.add(region)

    available_doors = set(world.doors)

    unfinished_dungeons = []
    # modify avail doors and d_regions, produces a list of unlinked doors
    for dungeon in world.dungeons:
        dungeon.paths = dungeon_paths[dungeon.name]
        for path in dungeon.paths:
            dungeon.path_completion[path] = False
        for regionName in list(dungeon.regions):
            region = world.get_region(regionName, player)
            dungeon.regions.remove(regionName)
            chunk = create_chunk(world, player, region, available_dungeon_regions, available_doors)
            dungeon.chunks.append(chunk)
            # todo: indicate entrance chunks
            dungeon.regions.extend(chunk.regions)
            dungeon.unlinked_doors.update(chunk.unlinked_doors)
            dungeon.chests += chunk.chests
            for path in dungeon.paths:
                if path[0] in chunk.regions or path[1] in chunk.regions:
                    chunk.paths_needed.append(path)
        if len(dungeon.unlinked_doors) > 0:
            unfinished_dungeons.append(dungeon)

    ttl_regions = len(available_dungeon_regions)
    for dungeon in unfinished_dungeons:
        ttl_regions += len(dungeon.regions)
    target_regions = ttl_regions // len(unfinished_dungeons)

    # chunk up the rest of the avail dungeon regions
    avail_chunks = []
    while len(available_dungeon_regions) > 0:
        region = available_dungeon_regions.pop()
        chunk = create_chunk(world, player, region, available_dungeon_regions)
        if chunk.outflow > 0:
            avail_chunks.append(chunk)

    normal_door_map = {Direction.South: [], Direction.North: [], Direction.East: [], Direction.West: []}
    for d in available_doors:
        if d.type == DoorType.Normal:
            normal_door_map[d.direction].append(d)
    random.shuffle(normal_door_map[Direction.South])
    random.shuffle(normal_door_map[Direction.North])
    random.shuffle(normal_door_map[Direction.East])
    random.shuffle(normal_door_map[Direction.West])

    # unfinished dungeons should be generated
    random.shuffle(unfinished_dungeons)
    for dungeon in unfinished_dungeons:
        logger.info('Starting %s', dungeon.name)
        bailcnt = 0
        while not is_dungeon_finished(world, player, dungeon):
            # pick some unfinished criteria to help?
            trgt_pct = len(dungeon.regions) / target_regions
            for path in dungeon.paths:
                find_path(world, player, path, dungeon.path_completion)

            # process - expand to about half size
            # start closing off unlinked doors - self pick vs dead end pick
            # ensure pick does not cutoff path (Zelda Cell direct to Sanc)
            # potential problems:
            # not enough outflow from path "source" to different locations
            # one-way doors
            # number of chests
            # key spheres

            if trgt_pct < .5:  # nothing to worry about yet
                pick = expand_pick(dungeon, normal_door_map)
                if pick is None:  # very possibly, some dungeon (looking at you HC) took forever to solve and the rest will have to be small
                    pick = self_pick(dungeon)
                # other bad situations for last dungeon: unused chests in avail_chunks
            else:
                if len(dungeon.unlinked_doors) // 2 > dungeon.incomplete_paths():
                    if len(dungeon.unlinked_doors) % 2 == 1:
                        logger.info('dead end')
                        pick = dead_end_pick(dungeon, avail_chunks)
                    else:
                        logger.info('self connection')
                        pick = self_pick(dungeon)
                elif len(dungeon.unlinked_doors) // 2 >= dungeon.incomplete_paths() and trgt_pct >= .8:
                    if len(dungeon.unlinked_doors) % 2 == 1:
                        logger.info('dead end')
                        pick = dead_end_pick(dungeon, avail_chunks)
                    else:  # we should ensure paths get done at this point
                        logger.info('path connection')
                        pick = path_pick(dungeon)
                # todo - branch here for chests?
                else:
                    pick = expand_pick(dungeon, normal_door_map)
                if pick is None:
                    # todo: efficiency note: if dead was selected, outflow helps more
                    # todo: if path or self was selected then direction helps more
                    logger.info('change request')
                    pick = change_outflow_or_dir_pick(dungeon, avail_chunks)

            # other cases: finding more chests for key spheres or chest count.
            # last dungeon should use all the remaining chests / doors

            if pick is not None:
                (srcdoor, destdoor) = pick
                logger.info('connecting %s to %s', srcdoor.name, destdoor.name)
                connect_two_way(world, srcdoor.name, destdoor.name, player)
                if destdoor.parentChunk in avail_chunks:
                    avail_chunks.remove(destdoor.parentChunk)
                for d in destdoor.parentChunk.unlinked_doors:
                    if d in normal_door_map[d.direction]:
                        normal_door_map[d.direction].remove(d)  # from the available door pool

                merge_chunks(dungeon, srcdoor.parentChunk, destdoor.parentChunk, srcdoor, destdoor)
            else:
                bailcnt += 1

            if len(dungeon.unlinked_doors) == 0 and not is_dungeon_finished(world, player, dungeon):
                raise RuntimeError('Made a bad dungeon - more smarts needed')
            if bailcnt > 100:
                raise RuntimeError('Infinite loop detected - see output')


def create_chunk(world, player, newregion, available_dungeon_regions, available_doors=None):
    # if newregion.name in dungeon.regions:
    # return  # we've been here before
    chunk = RegionChunk()
    queue = collections.deque([newregion])
    while len(queue) > 0:
        region = queue.popleft()
        chunk.regions.append(region.name)
        if region in available_dungeon_regions:
            available_dungeon_regions.remove(region)
        chunk.chests += len(region.locations)
        for ext in region.exits:
            d = world.check_for_door(ext.name, player)
            connected = ext.connected_region
            # todo - check for key restrictions?
            if d is not None:
                if available_doors is not None:
                    available_doors.remove(d)
                d.parentChunk = chunk
                if d.dest is None:
                    chunk.outflow += 1
                    # direction of door catalog ?
                    chunk.unlinked_doors.add(d)
                elif connected.name not in chunk.regions and connected.type == RegionType.Dungeon and connected not in queue:
                    queue.append(connected)  # needs to be added
            elif connected is not None and connected.name not in chunk.regions and connected.type == RegionType.Dungeon and connected not in queue:
                queue.append(connected)  # needs to be added
    return chunk


def merge_chunks(dungeon, old_chunk, new_chunk, old_door, new_door):
    old_chunk.unlinked_doors.remove(old_door)
    if old_door in dungeon.unlinked_doors:
        dungeon.unlinked_doors.remove(old_door)
    new_chunk.unlinked_doors.remove(new_door)
    if new_door in dungeon.unlinked_doors:
        dungeon.unlinked_doors.remove(new_door)

    if old_chunk is new_chunk:  # i think no merging necessary
        old_chunk.outflow -= 2  # loses some outflow # todo - keysphere or pathing re-eval?
        return

    # merge new chunk with old
    old_chunk.regions.extend(new_chunk.regions)
    old_chunk.unlinked_doors.update(new_chunk.unlinked_doors)
    for d in new_chunk.unlinked_doors:
        d.parentChunk = old_chunk
    new_door.parentChunk = old_chunk
    old_chunk.outflow += new_chunk.outflow - 2  # todo - one-way doors most likely
    paths_needed = []
    for path in old_chunk.paths_needed:
        if not ((path[0] in old_chunk.regions and path[1] in new_chunk.regions)
                or (path[1] in old_chunk.regions and path[0] in new_chunk.regions)):
            paths_needed.append(path)
    for path in new_chunk.paths_needed:
        if not ((path[0] in old_chunk.regions and path[1] in new_chunk.regions)
                or (path[1] in old_chunk.regions and path[0] in new_chunk.regions)):
            paths_needed.append(path)

    old_chunk.paths_needed = paths_needed
    old_chunk.chests += new_chunk.chests
    old_chunk.entrance = old_chunk.entrance or new_chunk.entrance
    # key spheres?

    if new_chunk in dungeon.chunks:
        dungeon.chunks.remove(new_chunk)
    dungeon.regions.extend(new_chunk.regions)
    dungeon.unlinked_doors.update(new_chunk.unlinked_doors)
    dungeon.chests += new_chunk.chests


def expand_pick(dungeon, normal_door_map):
    pairs = []
    for src in dungeon.unlinked_doors:
        for dest in normal_door_map[switch_dir(src.direction)]:
            pairs.append((src, dest))

    if len(pairs) == 0:
        return None
    random.shuffle(pairs)
    valid, pick = False, None
    while not valid and len(pairs) > 0:
        pick = pairs.pop()
        valid = valid_extend_pick(pick[0], pick[1])
    if valid:
        return pick
    else:
        return None


def dead_end_pick(dungeon, avail_chunks):
    door_map = {Direction.South: [], Direction.North: [], Direction.East: [], Direction.West: []}
    for d in dungeon.unlinked_doors:
        door_map[d.direction].append(d)

    chunky_doors = []
    for chunk in avail_chunks:
        if chunk.outflow == 1:  # dead end definition
            chunky_doors.extend(chunk.unlinked_doors)  # one-way door warning? todo

    pairs = []
    for dest in chunky_doors:
        for src in door_map[switch_dir(dest.direction)]:
            pairs.append((src, dest))

    if len(pairs) == 0:
        return None
    random.shuffle(pairs)
    valid, pick = False, None
    while not valid and len(pairs) > 0:
        pick = pairs.pop()
        valid = valid_extend_pick(pick[0], pick[1])
    if valid:
        return pick
    else:
        return None

def change_outflow_or_dir_pick(dungeon, avail_chunks):
    door_map = {Direction.South: [], Direction.North: [], Direction.East: [], Direction.West: []}
    for d in dungeon.unlinked_doors:
        door_map[d.direction].append(d)

    chunky_doors = []
    for chunk in avail_chunks:
        if chunk.outflow >= 2:  # no dead ends considered
            chunky_doors.extend(chunk.unlinked_doors)

    pairs = []
    for dest in chunky_doors:
        for src in door_map[switch_dir(dest.direction)]:
            if dest.parentChunk.outflow > 2:  # increases outflow
                pairs.append((src, dest))
            else:
                dest_doors = set(dest.parentChunk.unlinked_doors)
                dest_doors.remove(dest)
                if dest_doors.pop().direction != src.direction:  # the other door is not the same direction (or type?)
                    pairs.append((src, dest))

    if len(pairs) == 0:
        return None
    random.shuffle(pairs)
    valid, pick = False, None
    while not valid and len(pairs) > 0:
        pick = pairs.pop()
        valid = valid_extend_pick(pick[0], pick[1])
    if valid:
        return pick
    else:
        return None


# there shouldn't be any path in the destination
def valid_extend_pick(src_door, dest_door):
    src_chunk = src_door.parentChunk
    dest_chunk = dest_door.parentChunk
    unfulfilled_paths = 0
    for path in src_chunk.paths_needed:
        if not ((path[0] in src_chunk.regions and path[1] in dest_chunk.regions)
                or (path[1] in src_chunk.regions and path[0] in dest_chunk.regions)):
            unfulfilled_paths += 1
    if unfulfilled_paths == 0 or dest_chunk.outflow + src_chunk.outflow - 2 > 0:
        return True
    return False


def self_pick(dungeon):
    door_map = {Direction.South: [], Direction.North: [], Direction.East: [], Direction.West: []}
    for d in dungeon.unlinked_doors:
        door_map[d.direction].append(d)

    pairs = []
    for dest in dungeon.unlinked_doors:
        for src in door_map[switch_dir(dest.direction)]:
            pairs.append((src, dest))

    if len(pairs) == 0:
        return None
    random.shuffle(pairs)
    valid, pick = False, None
    while not valid and len(pairs) > 0:
        pick = pairs.pop()
        valid = valid_self_pick(pick[0], pick[1])
    if valid:
        return pick
    else:
        return None

# this currently checks
# 1. that all paths are fulfilled by this connection or the outflow is greater than 0.
def path_pick(dungeon) -> object:
    paths = []
    for path in dungeon.paths:
        if not dungeon.path_completion[path]:
            paths.append(path)
    random.shuffle(paths)
    pick = None
    while pick is None and len(paths) > 0:
        path = paths.pop()
        src_chunk = dest_chunk = None
        for chunk in dungeon.chunks:
            if path[0] in chunk.regions:
                src_chunk = chunk
            if path[1] in chunk.regions:
                dest_chunk = chunk

        door_map = {Direction.South: [], Direction.North: [], Direction.East: [], Direction.West: []}
        for d in src_chunk.unlinked_doors:
            door_map[d.direction].append(d)

        pairs = []
        for dest in dest_chunk.unlinked_doors:
            for src in door_map[switch_dir(dest.direction)]:
                pairs.append((src, dest))

        if len(pairs) == 0:
            continue
        random.shuffle(pairs)
        valid, pair = False, None
        while not valid and len(pairs) > 0:
            pair = pairs.pop()
            valid = valid_self_pick(pair[0], pair[1])
        if valid:
            pick = pair
    return pick


def valid_self_pick(src_door, dest_door):
    src_chunk, dest_chunk = src_door.parentChunk, dest_door.parentChunk
    if src_chunk == dest_chunk:
        return src_chunk.outflow - 2 > 0 or len(src_chunk.paths_needed) == 0
    unfulfilled_paths = 0
    for path in src_chunk.paths_needed:
        if not ((path[0] in src_chunk.regions and path[1] in dest_chunk.regions)
                or (path[1] in src_chunk.regions and path[0] in dest_chunk.regions)):
            unfulfilled_paths += 1
    for path in dest_chunk.paths_needed:
        if not ((path[0] in src_chunk.regions and path[1] in dest_chunk.regions)
                or (path[1] in src_chunk.regions and path[0] in dest_chunk.regions)):
            unfulfilled_paths += 1
    if unfulfilled_paths == 0 or dest_chunk.outflow + src_chunk.outflow - 2 > 0:
        return True
    return False


def is_dungeon_finished(world, player, dungeon):
    if len(dungeon.unlinked_doors) > 0:  # no unlinked doors
        return False
    for path in dungeon.paths:  # paths through dungeon are possible
        if not find_path(world, player, path, dungeon.path_completion):
            return False
    # if dungeon.chests < dungeon.count_dungeon_item() + 2:  # 2 or more chests reachable in dungeon than number of dungeon items
    #    return False
    # size of dungeon is acceptable
    # enough chests+keys within each key sphere to open key doors
    return True


def find_path(world, player, path, path_completion):
    if path_completion[path]:   # found it earlier -- assuming no disconnects
        return True
    visited_regions = set([])
    queue = collections.deque([world.get_region(path[0], player)])
    while len(queue) > 0:
        region = queue.popleft()
        if region.name == path[1]:
            path_completion[path] = True
            # would be nice if we could mark off the path needed in the chunks here
            return True
        visited_regions.add(region)
        for ext in region.exits:
            connected = ext.connected_region
            if connected is not None and connected not in visited_regions and connected.type == RegionType.Dungeon and connected not in queue:
                queue.append(connected)
    return False


def experiment(world, player):
    hc = convert_to_sectors(hyrule_castle_regions, world, player)
    ep = convert_to_sectors(eastern_regions, world, player)
    dp = convert_to_sectors(desert_regions, world, player)
    dungeon_sectors = [hc, ep, dp]
    for sector_list in dungeon_sectors:
        for sector in sector_list:
            for region in sector.regions:
                print(region.name)
            for door in sector.oustandings_doors:
                print(door.name)
            print()
            print()

    dungeon_region_lists = [hyrule_castle_regions, eastern_regions, desert_regions]
    for region_list in dungeon_region_lists:
        shuffle_dungeon_no_repeats(world, player, region_list)
    # for ent, ext in experimental_connections:
    #     if world.get_door(ent, player).blocked:
    #         connect_one_way(world, ext, ent, player)
    #     elif  world.get_door(ext, player).blocked:
    #         connect_one_way(world, ent, ext, player)
    #     else:
    #         connect_two_way(world, ent, ext, player)

    # Create list of regions


def convert_regions(region_names, world, player):
    region_list = []
    for name in region_names:
        region_list.append(world.get_region(name, player))
    return region_list


def convert_to_sectors(region_names, world, player):
    region_list = convert_regions(region_names, world, player)
    sectors = []
    while len(region_list) > 0:
        region = region_list.pop()
        region_chunk = [region]
        exits = []
        exits.extend(region.exits)
        outstanding_doors = []
        while len(exits) > 0:
            ext = exits.pop()
            if ext.connected_region is not None:
                connect_region = ext.connected_region
                if connect_region not in region_chunk and connect_region in region_list:
                    region_list.remove(connect_region)
                    region_chunk.append(connect_region)
                    exits.extend(connect_region.exits)
            else:
                door = world.check_for_door(ext.name, player)
                if door is not None:
                    outstanding_doors.append(door)
        sector = Sector()
        sector.regions.extend(region_chunk)
        sector.oustandings_doors.extend(outstanding_doors)
        sectors.append(sector)
    return sectors


def split_up_sectors(sector_list, entrance_sets):
    new_sector_grid = []
    for entrance_set in entrance_sets:
        new_sector_list = []
        for sector in sector_list:
            s_regions = list(map(lambda r: r.name, sector.regions))
            for entrance in entrance_set:
                if entrance in s_regions:
                    new_sector_list.append(sector)
                    break
        new_sector_grid.append(new_sector_list)
    # appalling I know - how to split up other things
    return new_sector_grid



# code below is for an algorithm without restarts

# "simple" thing that would probably reduce the number of restarts:
# When you pick a region check for all existing connections to other regions
# first via region.exits (which is a list of non-door exits from the current region)
# then for each Entrance in that list it may have a connected_region (or not)
# but make sure the connected_region is a Dungeon type so the search doesn't venture out into the overworld.
# Then, once you have this region chunk, add all the doors and do the normal loop.
# Nuts, normal loop


def shuffle_dungeon_no_repeats(world, player, dungeon_region_names):
    logger = logging.getLogger('')
    available_regions = []
    for name in dungeon_region_names:
        available_regions.append(world.get_region(name, player))
    random.shuffle(available_regions)

    available_doors = []
    # this is interesting but I want to ensure connectedness
    # Except for Desert1/2 and Skull 1/2/3 - treat them as separate dungeons?
    while len(available_regions) > 0:
        # Pick a random region and make its doors the open set
        region = available_regions.pop()
        logger.info("Starting in %s", region.name)
        regions = find_connected_regions(region, available_regions, logger)
        for region in regions:
            available_doors.extend(get_doors_ex(world, region, player))

        # Loop until all available doors are used
        while len(available_doors) > 0:
            # Pick a random available door to connect
            random.shuffle(available_doors)
            door = available_doors.pop()
            logger.info('Linking %s', door.name)
            # Find an available region that has a compatible door
            connect_region, connect_door = find_compatible_door_in_regions_ex(world, door, available_regions, player)
            if connect_region is not None:
                logger.info('  Found new region %s via %s', connect_region.name, connect_door.name)
                # Apply connection and add the new region's doors to the available list
                maybe_connect_two_way(world, door, connect_door, player)
                c_regions = find_connected_regions(connect_region, available_regions, logger)
                for region in c_regions:
                    available_doors.extend(get_doors_ex(world, region, player))
                # We've used this region and door, so don't use them again
                available_doors.remove(connect_door)
                available_regions.remove(connect_region)
            else:
                # If there's no available region with a door, use an internal connection
                connect_door = find_compatible_door_in_list(world, door, available_doors, player)
                if connect_door is not None:
                    logger.info('  Adding loop via %s', connect_door.name)
                    maybe_connect_two_way(world, door, connect_door, player)
                    available_doors.remove(connect_door)
    # Check that we used everything, we failed otherwise
    if len(available_regions) > 0 or len(available_doors) > 0:
        logger.warning('Failed to add all regions/doors to dungeon, generation will likely fail.')


def find_connected_regions(region, available_regions, logger):
    region_chunk = [region]
    exits = []
    exits.extend(region.exits)
    while len(exits) > 0:
        ext = exits.pop()
        if ext.connected_region is not None:
            connect_region = ext.connected_region
            if connect_region not in region_chunk and connect_region in available_regions:
                # door = world.check_for_door(ext.name, player)
                # if door is None or door.type not in [DoorType.Normal, DoorType.SpiralStairs]:
                logger.info('  Found new region %s via %s', connect_region.name, ext.name)
                available_regions.remove(connect_region)
                region_chunk.append(connect_region)
                exits.extend(connect_region.exits)
    return region_chunk


def find_compatible_door_in_regions_ex(world, door, regions, player):
    for region in regions:
        for proposed_door in get_doors_ex(world, region, player):
            if doors_compatible(door, proposed_door):
                return region, proposed_door
    return None, None

def get_doors_ex(world, region, player):
    res = []
    for exit in region.exits:
        door = world.check_for_door(exit.name, player)
        if door is not None and door.type in [DoorType.Normal, DoorType.SpiralStairs]:
            res.append(door)
    return res



# DATA GOES DOWN HERE

mandatory_connections = [
    ('Hyrule Dungeon North Abyss Catwalk Dropdown', 'Hyrule Dungeon North Abyss'),
    # ('Hyrule Dungeon Key Door S', 'Hyrule Dungeon North Abyss'),
    # ('Hyrule Dungeon Key Door N', 'Hyrule Dungeon Map Room'),
    ('Sewers Secret Room Push Block', 'Sewers Secret Room Blocked Path'),
    ('Eastern Hint Tile Push Block', 'Eastern Compass Area')
]

intratile_doors = [
    ('Hyrule Dungeon Key Door S', 'Hyrule Dungeon Key Door N'),
    ('Desert East Lobby WS', 'Desert East Wing ES'),
    ('Desert East Wing Key Door EN', 'Desert Compass Key Door WN'),
    ('Desert North Hall NW', 'Desert Map SW'),
    ('Desert North Hall NE', 'Desert Map SE'),
    ('Desert Sandworm Corner NE', 'Desert Bonk Torch SE'),
    ('Desert Sandworm Corner WS', 'Desert Circle of Pots ES'),
    ('Desert Circle of Pots NW', 'Desert Big Chest SW'),
    ('Desert West Wing WS', 'Desert West Lobby ES',),
    ('Desert Back Lobby NW', 'Desert Tiles 1 SW'),
    ('Desert Bridge SW', 'Desert Four Statues NW'),
    ('Desert Four Statues ES', 'Desert Beamos Hall WS',),
    ('Desert Tiles 2 NE', 'Desert Wall Slide SE'),
]

# todo: these path rules are more complicated I think...
#  there may be a better way to do them if we randomize dungeon entrances
dungeon_paths = {
    'Hyrule Castle': [('Hyrule Castle Lobby', 'Hyrule Castle West Lobby'),
                      ('Hyrule Castle Lobby', 'Hyrule Castle East Lobby'),
                      ('Hyrule Castle Lobby', 'Hyrule Dungeon Cellblock'),  # just for standard mode?
                      ('Hyrule Dungeon Cellblock', 'Sanctuary')],  # again, standard mode?
    'Eastern Palace': [('Eastern Lobby', 'Eastern Boss')],
    'Desert Palace': [('Desert Main Lobby', 'Desert West Lobby'),
                      ('Desert Main Lobby', 'Desert East Lobby'),
                      ('Desert Back Lobby', 'Desert Boss')],  # or Desert Main Lobby to Desert Boss would be fine I guess
    'Tower of Hera': [],
    'Agahnims Tower': [],
    'Palace of Darkness': [],
    'Thieves Town': [],
    'Skull Woods': [],
    'Swamp Palace': [],
    'Ice Palace': [],
    'Misery Mire': [],
    'Turtle Rock': [],
    'Ganons Tower': []
}

spiral_staircases = [('Hyrule Castle Back Hall Down Stairs', 'Hyrule Dungeon Map Room Up Stairs'),
                     ('Hyrule Dungeon Armory Down Stairs', 'Hyrule Dungeon Staircase Up Stairs'),
                     ('Hyrule Dungeon Staircase Down Stairs', 'Hyrule Dungeon Cellblock Up Stairs'),
                     ('Sewers Behind Tapestry Down Stairs', 'Sewers Rope Room Up Stairs'),
                     ('Sewers Secret Room Up Stairs', 'Sewers Pull Switch Down Stairs'),
                     ('Eastern Darkness Up Stairs', 'Eastern Attic Start Down Stairs'),
                     ('Desert Tiles 1 Up Stairs', 'Desert Bridge Down Stairs')]

straight_staircases = [('Hyrule Castle Lobby North Stairs', 'Hyrule Castle Throne Room South Stairs'),
                       ('Sewers Rope Room North Stairs', 'Sewers Dark Cross South Stairs')]

open_edges = [
    ('Hyrule Dungeon North Abyss South Edge', 'Hyrule Dungeon South Abyss North Edge'),
    ('Hyrule Dungeon North Abyss Catwalk Edge', 'Hyrule Dungeon South Abyss Catwalk North Edge'),
    ('Hyrule Dungeon South Abyss West Edge', 'Hyrule Dungeon Guardroom Abyss Edge'),
    ('Hyrule Dungeon South Abyss Catwalk West Edge', 'Hyrule Dungeon Guardroom Catwalk Edge'),
    ('Desert Main Lobby NW Edge', 'Desert North Hall SW Edge'),
    ('Desert Main Lobby N Edge', 'Desert Dead End Edge'),
    ('Desert Main Lobby NE Edge', 'Desert North Hall SE Edge'),
    ('Desert Main Lobby E Edge', 'Desert East Wing W Edge'),
    ('Desert East Wing N Edge', 'Desert Arrow Pot Corner S Edge'),
    ('Desert Arrow Pot Corner W Edge', 'Desert North Hall E Edge'),
    ('Desert North Hall W Edge', 'Desert Sandworm Corner S Edge'),
    ('Desert Sandworm Corner E Edge', 'Desert West Wing N Edge')
]

falldown_pits = [('Eastern Courtyard Potholes', 'Eastern Fairies')]
falldown_pits_as_doors = [('Eastern Courtyard Potholes', 'Eastern Fairy Landing')]

dungeon_warps = [('Eastern Fairies\' Warp', 'Eastern Courtyard')]
dungeon_warps_as_doors = [('Eastern Fairies\' Warp', 'Eastern Courtyard Warp End')]

default_door_connections = [
    ('Hyrule Castle Lobby W', 'Hyrule Castle West Lobby E'),
    ('Hyrule Castle Lobby E', 'Hyrule Castle East Lobby W'),
    ('Hyrule Castle Lobby WN', 'Hyrule Castle West Lobby EN'),
    ('Hyrule Castle West Lobby N', 'Hyrule Castle West Hall S'),
    ('Hyrule Castle East Lobby N', 'Hyrule Castle East Hall S'),
    ('Hyrule Castle East Lobby NW', 'Hyrule Castle East Hall SW'),
    ('Hyrule Castle East Hall W', 'Hyrule Castle Back Hall E'),
    ('Hyrule Castle West Hall E', 'Hyrule Castle Back Hall W'),
    ('Hyrule Castle Throne Room N', 'Sewers Behind Tapestry S'),
    ('Hyrule Dungeon Guardroom N', 'Hyrule Dungeon Armory S'),
    ('Sewers Dark Cross Key Door N', 'Sewers Dark Cross Key Door S'),
    ('Sewers Water W', 'Sewers Key Rat E'),
    ('Sewers Key Rat Key Door N', 'Sewers Secret Room Key Door S'),
    ('Eastern Lobby N', 'Eastern Cannonball S'),
    ('Eastern Cannonball N', 'Eastern Courtyard Ledge S'),
    ('Eastern Cannonball Ledge WN', 'Eastern Big Key EN'),
    ('Eastern Cannonball Ledge Key Door EN', 'Eastern Dark Square Key Door WN'),
    ('Eastern Courtyard Ledge W', 'Eastern Compass Area E'),
    ('Eastern Courtyard Ledge E', 'Eastern Map Area W'),
    ('Eastern Compass Area EN', 'Eastern Courtyard WN'),
    ('Eastern Courtyard EN', 'Eastern Map Valley WN'),
    ('Eastern Courtyard N', 'Eastern Darkness S'),
    ('Eastern Map Valley SW', 'Eastern Dark Square NW'),
    ('Eastern Attic Start WS', 'Eastern Attic Switches ES'),
    ('Eastern Attic Switches WS', 'Eastern Eyegores ES'),
    ('Desert Compass NW', 'Desert Cannonball S'),
    ('Desert Beamos Hall NE', 'Desert Tiles 2 SE')
]

# ('', ''),
default_one_way_connections = [
    ('Sewers Pull Switch S', 'Sanctuary N'),
    ('Eastern Eyegores NE', 'Eastern Boss SE'),
    ('Desert Wall Slide NW', 'Desert Boss SW')
]

experimental_connections = [('Eastern Boss SE', 'Eastern Eyegores NE'),
                            ('Eastern Eyegores ES', 'Eastern Map Valley WN'),
                            ('Eastern Lobby N', 'Eastern Courtyard Ledge S'),
                            ('Eastern Big Key EN', 'Eastern Courtyard Ledge W'),
                            ('Eastern Big Key NE', 'Eastern Compass Area SW'),
                            ('Eastern Compass Area EN', 'Eastern Courtyard WN'),
                            ('Eastern Courtyard N', 'Eastern Map Valley SW'),
                            ('Eastern Courtyard EN', 'Eastern Map Area W'),


                            ('Hyrule Castle Lobby W', 'Hyrule Castle Back Hall E'),
                            ('Hyrule Castle Throne Room N', 'Sewers Behind Tapestry S'),
                            ('Hyrule Castle Lobby WN', 'Hyrule Castle West Lobby EN'),
                            ('Hyrule Castle West Lobby N', 'Eastern Cannonball S'),

                            ('Hyrule Castle Lobby E', 'Sewers Water W'),
                            ('Sewers Dark Cross Key Door S', 'Sanctuary N')]

# experimental_connections = [('Eastern Boss SE', 'Eastern Courtyard N'),
#                             ('Eastern Courtyard EN', 'Eastern Attic Switches WS'),
#                             ('Eastern Lobby N', 'Eastern Darkness S'),
#                             ('Eastern Courtyard WN', 'Eastern Compass Area E'),
#                             ('Eastern Attic Switches ES', 'Eastern Cannonball Ledge WN'),
#                             ('Eastern Compass Area EN', 'Hyrule Castle Back Hall W'),
#                             ('Hyrule Castle Back Hall E', 'Eastern Map Area W'),
#                             ('Eastern Attic Start WS', 'Eastern Cannonball Ledge Key Door EN'),
#                             ('Eastern Compass Area SW', 'Hyrule Dungeon Guardroom N'),
#                             ('Hyrule Castle East Lobby NW', 'Hyrule Castle East Hall SW'),
#                             ('Hyrule Castle East Lobby N', 'Eastern Courtyard Ledge S'),
#                             ('Hyrule Castle Lobby E', 'Eastern Courtyard Ledge W'),
#                             ('Hyrule Castle Lobby WN', 'Eastern Courtyard Ledge E'),
#                             ('Hyrule Castle West Lobby EN', 'Hyrule Castle East Lobby W'),
#                             ('Hyrule Castle Throne Room N', 'Hyrule Castle East Hall S'),
#                             ('Hyrule Castle West Lobby E', 'Hyrule Castle East Hall W'),
#                             ('Hyrule Castle West Lobby N', 'Hyrule Dungeon Armory S'),
#                             ('Hyrule Castle Lobby W', 'Hyrule Castle West Hall E'),
#                             ('Hyrule Castle West Hall S', 'Sanctuary N')]


desert_default_entrance_sets = [
    ['Desert Back Lobby'],
    ['Desert Main Lobby', 'Desert West Lobby', 'Desert East Lobby']
]
