import random
import collections
import logging

from BaseClasses import RegionType, DoorType, Direction, Sector, pol_idx
from Dungeons import hyrule_castle_regions, eastern_regions, desert_regions, hera_regions

def link_doors(world, player):

    # Drop-down connections & push blocks
    for exitName, regionName in logical_connections:
        connect_simple_door(world, exitName, regionName, player)
    # These should all be connected for now as normal connections
    for edge_a, edge_b in interior_doors:
        connect_two_way(world, edge_a, edge_b, player)

    # These connection are here because they are currently unable to be shuffled
    for entrance, ext in straight_staircases:
        connect_two_way(world, entrance, ext, player)
    for entrance, ext in open_edges:
        connect_two_way(world, entrance, ext, player)
    for exitName, regionName in falldown_pits:
        connect_simple_door(world, exitName, regionName, player)
    for exitName, regionName in dungeon_warps:
        connect_simple_door(world, exitName, regionName, player)

    if world.doorShuffle == 'vanilla':
        for entrance, ext in spiral_staircases:
            connect_two_way(world, entrance, ext, player)
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
                logger.debug('spoiler: %s connected to %s', door_a.name, door_b.name)
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
                    logger.debug('Door not found in queue: %s connected to %s', door_b.name, door_a.name)
            else:
                logger.warning('Door not connected: %s', door_a.name)


# some useful functions
oppositemap = {
    Direction.South: Direction.North,
    Direction.North: Direction.South,
    Direction.West: Direction.East,
    Direction.East: Direction.West,
    Direction.Up: Direction.Down,
    Direction.Down: Direction.Up,
}


def switch_dir(direction):
    return oppositemap[direction]


def connect_simple_door(world, exit_name, region_name, player):
    region = world.get_region(region_name, player)
    world.get_entrance(exit_name, player).connect(region)
    d = world.check_for_door(exit_name, player)
    if d is not None:
        d.dest = region


def connect_two_way(world, entrancename, exitname, player):
    entrance = world.get_entrance(entrancename, player)
    ext = world.get_entrance(exitname, player)

    # if these were already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)
    if ext.connected_region is not None:
        ext.connected_region.entrances.remove(ext)

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
        entrance.connected_region.entrances.remove(entrance)
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
    # TODO: The "starts" regions need access logic
    # Aerinon's note: I think this is handled already by ER Rules - may need to check correct requirements
    dungeon_region_starts_es = ['Hyrule Castle Lobby', 'Hyrule Castle West Lobby', 'Hyrule Castle East Lobby', 'Sewers Secret Room']
    dungeon_region_starts_ep = ['Eastern Lobby']
    dungeon_region_starts_dp = ['Desert Back Lobby', 'Desert Main Lobby', 'Desert West Lobby', 'Desert East Lobby']
    dungeon_region_starts_th = ['Hera Lobby']
    dungeon_region_lists = [
        (dungeon_region_starts_es, hyrule_castle_regions),
        (dungeon_region_starts_ep, eastern_regions),
        (dungeon_region_starts_dp, desert_regions),
        (dungeon_region_starts_th, hera_regions)
    ]
    for start_list, region_list in dungeon_region_lists:
        shuffle_dungeon(world, player, start_list, region_list)

def shuffle_dungeon(world, player, start_region_names, dungeon_region_names):
    logger = logging.getLogger('')
    # Part one - generate a random layout
    available_regions = []
    for name in [r for r in dungeon_region_names if r not in start_region_names]:
        available_regions.append(world.get_region(name, player))
    random.shuffle(available_regions)

    # "Ugly" doors are doors that we don't want to see from the front, because of some
    # sort of unsupported key door. To handle them, make a map of "ugly regions" and
    # never link across them.
    ugly_regions = {}
    next_ugly_region = 1

    # Add all start regions to the open set.
    available_doors = []
    for name in start_region_names:
        logger.info("Starting in %s", name)
        for door in get_doors(world, world.get_region(name, player), player):
            ugly_regions[door.name] = 0
            available_doors.append(door)
    
    # Loop until all available doors are used
    while len(available_doors) > 0:
        # Pick a random available door to connect, prioritizing ones that aren't blocked.
        # This makes them either get picked up through another door (so they head deeper
        # into the dungeon), or puts them late in the dungeon (so they probably are part
        # of a loop). Panic if neither of these happens.
        random.shuffle(available_doors)
        available_doors.sort(key=lambda door: 1 if door.blocked else 2 if door.ugly else 0)
        door = available_doors.pop()
        logger.info('Linking %s', door.name)
        # Find an available region that has a compatible door
        connect_region, connect_door = find_compatible_door_in_regions(world, door, available_regions, player)
        # Also ignore compatible doors if they're blocked; these should only be used to
        # create loops.
        if connect_region is not None and not door.blocked:
            logger.info('  Found new region %s via %s', connect_region.name, connect_door.name)
            # Apply connection and add the new region's doors to the available list
            maybe_connect_two_way(world, door, connect_door, player)
            # Figure out the new room's ugliness region
            new_room_ugly_region = ugly_regions[door.name]
            if connect_door.ugly:
                next_ugly_region += 1
                new_room_ugly_region = next_ugly_region
            is_new_region = connect_region in available_regions
            # Add the doors
            for door in get_doors(world, connect_region, player):
                ugly_regions[door.name] = new_room_ugly_region
                if is_new_region:
                    available_doors.append(door)
                # If an ugly door is anything but the connect door, panic and die
                if door != connect_door and door.ugly:
                    logger.info('Failed because of ugly door, trying again.')
                    shuffle_dungeon(world, player, start_region_names, dungeon_region_names)
                    return

            # We've used this region and door, so don't use them again
            if is_new_region:
                available_regions.remove(connect_region)
            if connect_door in available_doors:
                available_doors.remove(connect_door)
        else:
            # If there's no available region with a door, use an internal connection
            connect_door = find_compatible_door_in_list(ugly_regions, world, door, available_doors, player)
            if connect_door is not None:
                logger.info('  Adding loop via %s', connect_door.name)
                maybe_connect_two_way(world, door, connect_door, player)
                if connect_door in available_doors:
                    available_doors.remove(connect_door)
    # Check that we used everything, and retry if we failed
    if len(available_regions) > 0 or len(available_doors) > 0:
        logger.info('Failed to add all regions to dungeon, trying again.')
        shuffle_dungeon(world, player, start_region_names, dungeon_region_names)
        return


# Connects a and b. Or don't if they're an unsupported connection type.
# TODO: This is gross, don't do it this way
def maybe_connect_two_way(world, a, b, player):
    # Return on unsupported types.
    if a.type in [DoorType.Open, DoorType.StraightStairs, DoorType.Hole, DoorType.Warp, DoorType.Interior, DoorType.Logical]:
        return
    # Connect supported types
    if a.type == DoorType.Normal or a.type == DoorType.SpiralStairs:
        if a.blocked:
            connect_one_way(world, b.name, a.name, player)
        elif b.blocked:
            connect_one_way(world, a.name, b.name, player)
        else:
            connect_two_way(world, a.name, b.name, player)
        return
    # If we failed to account for a type, panic
    raise RuntimeError('Unknown door type ' + a.type.name)


# Finds a compatible door in regions, returns the region and door
def find_compatible_door_in_regions(world, door, regions, player):
    if door.type in [DoorType.Hole, DoorType.Warp, DoorType.Logical]:
        return door.dest, door
    for region in regions:
        for proposed_door in get_doors(world, region, player):
            if doors_compatible(door, proposed_door):
                return region, proposed_door
    return None, None

def find_compatible_door_in_list(ugly_regions, world, door, doors, player):
    if door.type in [DoorType.Hole, DoorType.Warp, DoorType.Logical]:
        return door
    for proposed_door in doors:
        if ugly_regions[door.name] != ugly_regions[proposed_door.name]:
            continue
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
    if a.type == DoorType.Interior:
        return doors_fit_mandatory_pair(interior_doors, a, b)
    if a.type == DoorType.Normal and (a.smallKey or b.smallKey or a.bigKey or b.bigKey):
        return doors_fit_mandatory_pair(key_doors, a, b)
    if a.type in [DoorType.Hole, DoorType.Warp, DoorType.Logical]:
        return False  # these aren't compatible with anything
    return a.direction == switch_dir(b.direction)


def doors_fit_mandatory_pair(pair_list, a, b):
  for pair_a, pair_b in pair_list:
      if (a.name == pair_a and b.name == pair_b) or (a.name == pair_b and b.name == pair_a):
          return True
  return False

# goals:
# 1. have enough chests to be interesting (2 more than dungeon items)
# 2. have a balanced amount of regions added (check)
# 3. prevent soft locks due to key usage
# 4. rules in place to affect item placement (lamp, keys, etc.)
# 5. to be complete -- all doors linked (check, somewhat)
# 6. avoid deadlocks/dead end dungeon (check)
# 7. certain paths through dungeon must be possible - be able to reach goals (check)


def cross_dungeon(world, player):
    hc = convert_to_sectors(hyrule_castle_regions, world, player)
    ep = convert_to_sectors(eastern_regions, world, player)
    dp = convert_to_sectors(desert_regions, world, player)
    th = convert_to_sectors(hera_regions, world, player)
    world_split = split_up_sectors(hc + ep + dp + th, default_dungeon_sets)
    dp_split = split_up_sectors(world_split.pop(2), desert_default_entrance_sets)
    world_split.extend(dp_split)
    # todo - adjust dungeon item pools
    for sector_list in world_split:
        shuffle_dungeon_no_repeats(world, player, sector_list)


def experiment(world, player):
    hc = convert_to_sectors(hyrule_castle_regions, world, player)
    ep = convert_to_sectors(eastern_regions, world, player)
    dp = convert_to_sectors(desert_regions, world, player)
    th = convert_to_sectors(hera_regions, world, player)
    dungeon_sectors = [hc, ep, th]
    dp_split = split_up_sectors(dp, desert_default_entrance_sets)
    dungeon_sectors.extend(dp_split)
    for sector_list in dungeon_sectors:
        shuffle_dungeon_no_repeats(world, player, sector_list)


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
                if door is not None and not door.landing:
                    outstanding_doors.append(door)
        sector = Sector()
        sector.regions.extend(region_chunk)
        sector.outstanding_doors.extend(outstanding_doors)
        sectors.append(sector)
    return sectors


def split_up_sectors(sector_list, entrance_sets):
    new_sector_grid = []
    leftover_sectors = []
    leftover_sectors.extend(sector_list)
    for entrance_set in entrance_sets:
        new_sector_list = []
        for sector in sector_list:
            s_regions = list(map(lambda r: r.name, sector.regions))
            for entrance in entrance_set:
                if entrance in s_regions:
                    new_sector_list.append(sector)
                    leftover_sectors.remove(sector)
                    break
        new_sector_grid.append(new_sector_list)
    shuffle_sectors(new_sector_grid, leftover_sectors)
    return new_sector_grid


def sum_vector(sector_list, func):
    result = [0, 0, 0]
    for sector in sector_list:
        vector = func(sector)
        for i in range(len(result)):
            result[i] = result[i] + vector[i]
    return result


def add_vectors(vector_one, vector_two):
    result = [0]*len(vector_one)
    for i in range(len(result)):
        result[i] = vector_one[i] + vector_two[i]
    return result


def is_polarity_neutral(polarity):
    for value in polarity:
        if value != 0:
            return False
    return True


search_iterations = 0


def is_proposal_valid(proposal, buckets, candidates):
    logger = logging.getLogger('')
    global search_iterations
    search_iterations = search_iterations + 1
    if search_iterations % 100 == 0:
        logger.info('Iteration %s', search_iterations)
    # check that proposal is complete
    for i in range(len(proposal)):
        if proposal[i] is -1:
            return False  # indicates an incomplete proposal
    test_bucket = []
    for bucket_idx in range(len(buckets)):
        test_bucket.append(list(buckets[bucket_idx]))
    for i in range(len(proposal)):
        test_bucket[proposal[i]].append(candidates[i])
    for test in test_bucket:
        valid = is_polarity_neutral(sum_vector(test, lambda s: s.polarity()))
        if not valid:
            return False
    return True


def shuffle_sectors(buckets, candidates):
    # for a faster search - instead of random - put the most likely culprits to cause problems at the end, least likely at the front
    # unless we start checking for failures earlier in the algo
    random.shuffle(candidates)
    proposal = [-1]*len(candidates)

    solution = find_proposal_monte_carlo(proposal, buckets, candidates)
    if solution is None:
        raise Exception('Unable to find a proposal')
    for i in range(len(solution)):
        buckets[solution[i]].append(candidates[i])


# monte carlo proposal generation
def find_proposal_monte_carlo(proposal, buckets, candidates):
    n = len(candidates)
    k = len(buckets)
    hashes = set()
    collisions = 0

    while collisions < 10000:
        hash = ''
        for i in range(n):
            proposal[i] = random.randrange(k)
            hash = hash + str(proposal[i])
        if hash not in hashes:
            collisions = 0
            if is_proposal_valid(proposal, buckets, candidates):
                return proposal
            hashes.add(hash)
        else:
            collisions = collisions + 1
    raise Exception('Too many collisions in a row, solutions space is sparse')


# this is a DFS search - fairly slow
def find_proposal(proposal, buckets, candidates):
    size = len(candidates)
    combination_grid = []
    for i in range(size):
        combination_grid.append(list(range(len(buckets))))
    # randomize which bucket
    for possible_buckets in combination_grid:
        random.shuffle(possible_buckets)

    idx = 0
    while idx != size or not is_proposal_valid(proposal, buckets, candidates):
        if idx == size:
            idx = idx - 1
            while len(combination_grid[idx]) == 0:
                if idx == -1:  # this is the failure case - we shouldn't hit it
                    return None
                combination_grid[idx] = list(range(len(buckets)))
                idx = idx - 1
        proposal[idx] = combination_grid[idx].pop()
        # can we detect a bad choice at this stage
        idx = idx + 1
    return proposal


# code below is for an algorithm without restarts

# "simple" thing that would probably reduce the number of restarts:
# When you pick a region check for all existing connections to other regions
# first via region.exits (which is a list of non-door exits from the current region)
# then for each Entrance in that list it may have a connected_region (or not)
# but make sure the connected_region is a Dungeon type so the search doesn't venture out into the overworld.
# Then, once you have this region chunk, add all the doors and do the normal loop.
# Nuts, normal loop


def shuffle_dungeon_no_repeats(world, player, available_sectors):
    logger = logging.getLogger('')

    random.shuffle(available_sectors)
    for sector in available_sectors:
        random.shuffle(sector.outstanding_doors)

    while len(available_sectors) > 0:
        # Pick a random region and make its doors the open set
        sector = available_sectors.pop()
        current_sector = sector

        # Loop until all available doors are used
        while len(current_sector.outstanding_doors) > 0:
            # Pick a random available door to connect
            random.shuffle(current_sector.outstanding_doors)
            door = current_sector.outstanding_doors.pop()
            logger.info('Linking %s', door.name)
            # Find an available region that has a compatible door
            compatibles = find_all_compatible_door_in_sectors_ex(door, available_sectors)
            while len(compatibles) > 0:
                connect_sector, connect_door = compatibles.pop()
                logger.info('  Found possible new sector via %s', connect_door.name)
                # Check if valid
                if is_valid(door, connect_door, current_sector, connect_sector, available_sectors):
                    # Apply connection and add the new region's doors to the available list
                    maybe_connect_two_way(world, door, connect_door, player)
                    connect_sector.outstanding_doors.remove(connect_door)
                    available_sectors.remove(connect_sector)
                    current_sector.outstanding_doors.extend(connect_sector.outstanding_doors)
                    current_sector.regions.extend(connect_sector.regions)
                    break
                logger.info(' Not Linking %s to %s', door.name, connect_door.name)
                if len(compatibles) == 0:  # time to try again
                    current_sector.outstanding_doors.insert(0, door)
                    if len(current_sector.outstanding_doors) <= 1:
                        raise Exception('Rejected last option due to dead end... infinite loop ensues')
            else:
                # If there's no available region with a door, use an internal connection
                # todo: find all possibles for this door first
                connect_door = find_compatible_door_in_list_old(world, door, current_sector.outstanding_doors, player)
                if connect_door is not None:
                    logger.info('  Adding loop via %s', connect_door.name)
                    # Check if valid
                    if is_loop_valid(door, connect_door, current_sector, len(available_sectors) == 0):
                        maybe_connect_two_way(world, door, connect_door, player)
                        current_sector.outstanding_doors.remove(connect_door)
                    else:
                        logger.info(' Not Linking %s to %s', door.name, connect_door.name)
                        current_sector.outstanding_doors.insert(0, door)
                        if len(current_sector.outstanding_doors) <= 2:
                            raise Exception('Rejected last option due to likely improper loops...')
                else:
                    raise Exception('Something has gone terribly wrong')
    # Check that we used everything, we failed otherwise
    if len(available_sectors) > 0 or len(current_sector.outstanding_doors) > 0:
        logger.warning('Failed to add all regions/doors to dungeon, generation will likely fail.')


def find_all_compatible_door_in_sectors_ex(door, sectors):
    result = []
    for sector in sectors:
        for proposed_door in sector.outstanding_doors:
            if doors_compatible_ignore_keys(door, proposed_door):
                result.append((sector, proposed_door))
    return result


def find_compatible_door_in_list_old(world, door, doors, player):
    for proposed_door in doors:
        if doors_compatible_ignore_keys(door, proposed_door):
            return proposed_door


# this method also assumes that sectors have been build appropriately
def doors_compatible_ignore_keys(a, b):
    if a.type != b.type:
        return False
    # todo: test spirals linking to each other
    # if a.type == DoorType.SpiralStairs:
    #     return True
    return a.direction == switch_dir(b.direction)


# todo: path checking needed?
def is_valid(door_a, door_b, sector_a, sector_b, available_sectors):
    if len(available_sectors) == 1:
        return True
    elif not are_there_outstanding_doors_of_type(door_a, door_b, sector_a, sector_b, available_sectors):
        return False
    elif door_a.blocked and door_b.blocked:  # I can't see this going well unless we are in loop generation...
        return False
    elif not door_a.blocked and not door_b.blocked:
        return sector_a.outflow() + sector_b.outflow() - 1 > 0  # door_a has been removed already, so a.outflow is reduced by one
    elif door_a.blocked or door_b.blocked:
        return sector_a.outflow() + sector_b.outflow() > 0
    return False  # not sure how we got here, but it's a bad idea


def is_loop_valid(door_a, door_b, sector, no_more_sectors):
    if no_more_sectors:
        return True
    elif not door_a.blocked and not door_b.blocked:
        return sector.outflow() - 1 > 0
    elif door_a.blocked or door_b.blocked:
        return sector.outflow() > 0
    return True  #  I think this is always true. Both blocked but we're connecting loops now, so dead end?


def are_there_outstanding_doors_of_type(door_a, door_b, sector_a, sector_b, available_sectors):
    idx = pol_idx[door_a.direction][0]
    diff = sum_vector(available_sectors, lambda x: x.magnitude())[idx]-sector_b.magnitude()[idx]
    if diff == 0:
        return True  # this case will cover all the doors of that DirectionPair
    only_neutral_left = True
    for sector in available_sectors:
        if sector != sector_b and sector.polarity()[idx] != 0:
            only_neutral_left = False
            break

    if only_neutral_left:
        hooks_left = False
        for door in sector_a.outstanding_doors:
            if door != door_a and pol_idx[door.direction][0] == idx:
                hooks_left = True
                break
        if not hooks_left:
            for door in sector_b.outstanding_doors:
                if door != door_b and pol_idx[door.direction][0] == idx:
                    hooks_left = True
                    break
        return hooks_left
    return True



# DATA GOES DOWN HERE

logical_connections = [
    ('Hyrule Dungeon North Abyss Catwalk Dropdown', 'Hyrule Dungeon North Abyss'),
    ('Sewers Secret Room Push Block', 'Sewers Secret Room Blocked Path'),
    ('Eastern Hint Tile Push Block', 'Eastern Compass Area'),
    ('Hera Big Chest Landing Exit', 'Hera 4F')
]

spiral_staircases = [
    ('Hyrule Castle Back Hall Down Stairs', 'Hyrule Dungeon Map Room Up Stairs'),
    ('Hyrule Dungeon Armory Down Stairs', 'Hyrule Dungeon Staircase Up Stairs'),
    ('Hyrule Dungeon Staircase Down Stairs', 'Hyrule Dungeon Cellblock Up Stairs'),
    ('Sewers Behind Tapestry Down Stairs', 'Sewers Rope Room Up Stairs'),
    ('Sewers Secret Room Up Stairs', 'Sewers Pull Switch Down Stairs'),
    ('Eastern Darkness Up Stairs', 'Eastern Attic Start Down Stairs'),
    ('Desert Tiles 1 Up Stairs', 'Desert Bridge Down Stairs'),
    ('Hera Lobby Down Stairs', 'Hera Basement Cage Up Stairs'),
    ('Hera Lobby Key Stairs', 'Hera Tile Room Up Stairs'),
    ('Hera Lobby Up Stairs', 'Hera Beetles Down Stairs'),
    ('Hera Startile Wide Up Stairs', 'Hera 4F Down Stairs'),
    ('Hera 4F Up Stairs', 'Hera 5F Down Stairs'),
    ('Hera 5F Up Stairs', 'Hera Boss Down Stairs'),
]

straight_staircases = [
    ('Hyrule Castle Lobby North Stairs', 'Hyrule Castle Throne Room South Stairs'),
    ('Sewers Rope Room North Stairs', 'Sewers Dark Cross South Stairs')
]

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

falldown_pits = [
    ('Eastern Courtyard Potholes', 'Eastern Fairies'),
    ('Hera Beetles Holes', 'Hera Lobby'),
    ('Hera Startile Corner Holes', 'Hera Lobby'),
    ('Hera Startile Wide Holes', 'Hera Lobby'),
    ('Hera 4F Holes', 'Hera Lobby'),  # failed bomb jump
    ('Hera Big Chest Landing Holes', 'Hera Startile Wide'),  # the other holes near big chest
    ('Hera 5F Star Hole', 'Hera Big Chest Landing'),
    ('Hera 5F Pothole Chain', 'Hera Fairies'),
    ('Hera 5F Normal Holes', 'Hera 4F'),
    ('Hera Boss Outer Hole', 'Hera 5F'),
    ('Hera Boss Inner Hole', 'Hera 4F'),
]

dungeon_warps = [
    ('Eastern Fairies\' Warp', 'Eastern Courtyard'),
    ('Hera Fairies\' Warp', 'Hera 5F')
]

interior_doors = [
    ('Hyrule Dungeon Armory Interior Key Door S', 'Hyrule Dungeon Armory Interior Key Door N'),
    ('Hyrule Dungeon Map Room Key Door S', 'Hyrule Dungeon North Abyss Key Door N'),
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
    ('Hera Tile Room EN', 'Hera Tridorm WN'),
    ('Hera Tridorm SE', 'Hera Torches NE'),
    ('Hera Beetles WS', 'Hera Startile Corner ES'),
    ('Hera Startile Corner NW', 'Hera Startile Wide SW'),
]

key_doors = [
    ('Sewers Key Rat Key Door N', 'Sewers Secret Room Key Door S'),
    ('Sewers Dark Cross Key Door N', 'Sewers Dark Cross Key Door S'),
    ('Eastern Dark Square Key Door WN', 'Eastern Cannonball Ledge Key Door EN'),
    ('Eastern Darkness Up Stairs', 'Eastern Attic Start Down Stairs'),
    ('Eastern Big Key NE', 'Eastern Compass Area SW'),
    ('Eastern Darkness S', 'Eastern Courtyard N'),
    ('Desert East Wing Key Door EN', 'Desert Compass Key Door WN'),
    ('Desert Tiles 1 Up Stairs', 'Desert Bridge Down Stairs'),
    ('Desert Beamos Hall NE', 'Desert Tiles 2 SE'),
    ('Desert Tiles 2 NE', 'Desert Wall Slide SE'),
    ('Desert Wall Slide NW', 'Desert Boss SW'),
    ('Hera Lobby Key Stairs', 'Hera Tile Room Up Stairs'),
    ('Hera Startile Corner NW', 'Hera Startile Wide SW'),
]

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

# For crossed
default_dungeon_sets = [
    ['Hyrule Castle Lobby', 'Hyrule Castle West Lobby', 'Hyrule Castle East Lobby', 'Sewers Secret Room', 'Sanctuary',
     'Hyrule Dungeon Cellblock'],
    ['Eastern Lobby', 'Eastern Boss'],
    ['Desert Back Lobby', 'Desert Boss', 'Desert Main Lobby', 'Desert West Lobby', 'Desert East Lobby'],
    ['Hera Lobby', 'Hera Boss']
]


desert_default_entrance_sets = [
    ['Desert Back Lobby'],
    ['Desert Main Lobby', 'Desert West Lobby', 'Desert East Lobby']
]
