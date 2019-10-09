import random
import collections
import logging
import operator as op

from functools import reduce
from BaseClasses import RegionType, DoorType, Direction, Sector, pol_idx
from Dungeons import hyrule_castle_regions, eastern_regions, desert_regions, hera_regions, tower_regions, pod_regions
from Dungeons import dungeon_regions, region_starts, split_region_starts
from Regions import key_only_locations
from RoomData import DoorKind, PairedDoor


def link_doors(world, player):

    # Drop-down connections & push blocks
    for exitName, regionName in logical_connections:
        connect_simple_door(world, exitName, regionName, player)
    # These should all be connected for now as normal connections
    for edge_a, edge_b in interior_doors:
        connect_two_way(world, edge_a, edge_b, player)

    # These connections are here because they are currently unable to be shuffled
    for entrance, ext in straight_staircases:
        connect_two_way(world, entrance, ext, player)
    for entrance, ext in open_edges:
        connect_two_way(world, entrance, ext, player)
    for exitName, regionName in falldown_pits:
        connect_simple_door(world, exitName, regionName, player)
    for exitName, regionName in dungeon_warps:
        connect_simple_door(world, exitName, regionName, player)
    for ent, ext in ladders:
        connect_two_way(world, ent, ext, player)

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
    for dp in world.paired_doors[player]:
        if dp.pair:
            logger.debug('Paired Doors: %s with %s (p%d)', dp.door_a, dp.door_b, player)
        else:
            logger.debug('Unpaired Doors: %s not paired with %s (p%d)', dp.door_a, dp.door_b, player)


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


def fix_big_key_doors_with_ugly_smalls(world, player):
    remove_ugly_small_key_doors(world, player)
    unpair_big_key_doors(world, player)


def remove_ugly_small_key_doors(world, player):
    for d in ['Eastern Compass Area SW', 'Eastern Darkness S']:
        door = world.get_door(d, player)
        room = world.get_room(door.roomIndex, player)
        room.change(door.doorListPos, DoorKind.Normal)
        door.smallKey = False
        door.ugly = False


def unpair_big_key_doors(world, player):
    problematic_bk_doors = ['Eastern Courtyard N', 'Eastern Big Key NE']
    for paired_door in world.paired_doors[player]:
        if paired_door.door_a in problematic_bk_doors or paired_door.door_b in problematic_bk_doors:
            paired_door.pair = False


def pair_existing_key_doors(world, player, door_a, door_b):
    already_paired = False
    door_names = [door_a.name, door_b.name]
    for pd in world.paired_doors[player]:
        if pd.door_a in door_names and pd.door_b in door_names:
            already_paired = True
            break
    if already_paired:
        return
    for paired_door in world.paired_doors[player]:
        if paired_door.door_a in door_names or paired_door.door_b in door_names:
            paired_door.pair = False
    world.paired_doors[player].append(PairedDoor(door_a, door_b))


# def unpair_all_doors(world, player):
#     for paired_door in world.paired_doors[player]:
#         paired_door.pair = False


def within_dungeon(world, player):
    # TODO: The "starts" regions need access logic
    # Aerinon's note: I think this is handled already by ER Rules - may need to check correct requirements
    dungeon_region_starts_es = ['Hyrule Castle Lobby', 'Hyrule Castle West Lobby', 'Hyrule Castle East Lobby', 'Sewers Secret Room']
    dungeon_region_starts_ep = ['Eastern Lobby']
    dungeon_region_starts_dp = ['Desert Back Lobby', 'Desert Main Lobby', 'Desert West Lobby', 'Desert East Lobby']
    dungeon_region_starts_th = ['Hera Lobby']
    dungeon_region_starts_at = ['Tower Lobby']
    dungeon_region_starts_pd = ['PoD Lobby']
    dungeon_region_lists = [
        (dungeon_region_starts_es, hyrule_castle_regions),
        (dungeon_region_starts_ep, eastern_regions),
        (dungeon_region_starts_dp, desert_regions),
        (dungeon_region_starts_th, hera_regions),
        (dungeon_region_starts_at, tower_regions),
        (dungeon_region_starts_pd, pod_regions),
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
        available_doors.sort(key=lambda door: 1 if door.blocked else 0 if door.ugly else 2)
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
    if a.type in [DoorType.Open, DoorType.StraightStairs, DoorType.Hole, DoorType.Warp, DoorType.Ladder,
                  DoorType.Interior, DoorType.Logical]:
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
    if a.type == DoorType.Ladder:
        return doors_fit_mandatory_pair(ladders, a, b)
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
    all_sectors = []
    for key in dungeon_regions.keys():
        all_sectors.extend(convert_to_sectors(dungeon_regions[key], world, player))
    dungeon_split = split_up_sectors(all_sectors, default_dungeon_sets)
    dungeon_sectors = []
    for idx, sector_list in enumerate(dungeon_split):
        name = dungeon_x_idx_to_name[idx]
        if name in split_region_starts.keys():
            split = split_up_sectors(sector_list, split_region_starts[name])
            for sub_idx, sub_sector_list in enumerate(split):
                dungeon_sectors.append((name, sub_sector_list, split_region_starts[name][sub_idx]))
        else:
            dungeon_sectors.append((name, sector_list, region_starts[name]))
    # todo - adjust dungeon item pools -- ?
    dungeon_layouts = []
    for key, sector_list, entrance_list in dungeon_sectors:
        ds = shuffle_dungeon_no_repeats(world, player, sector_list, entrance_list)
        ds.name = key
        dungeon_layouts.append((ds, entrance_list))

    combine_layouts(dungeon_layouts)

    for layout in dungeon_layouts:
        shuffle_key_doors(layout[1], layout[2], world, player)


def experiment(world, player):
    fix_big_key_doors_with_ugly_smalls(world, player)
    dungeon_sectors = []
    for key in dungeon_regions.keys():
        sector_list = convert_to_sectors(dungeon_regions[key], world, player)
        if key in split_region_starts.keys():
            split_sectors = split_up_sectors(sector_list, split_region_starts[key])
            for idx, sub_sector_list in enumerate(split_sectors):
                dungeon_sectors.append((key, sub_sector_list, split_region_starts[key][idx]))
        else:
            dungeon_sectors.append((key, sector_list, region_starts[key]))

    dungeon_layouts = []
    for key, sector_list, entrance_list in dungeon_sectors:
        ds = shuffle_dungeon_no_repeats(world, player, sector_list, entrance_list)
        ds.name = key
        dungeon_layouts.append((ds, entrance_list))

    combine_layouts(dungeon_layouts)

    # shuffle_key_doors for dungeons
    for layout in dungeon_layouts:
        shuffle_key_doors(layout[0], layout[1], world, player)


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
        sector = None
        new_sector = True
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
                if connect_region not in region_chunk:
                    for existing in sectors:
                        if connect_region in existing.regions:
                            sector = existing
                            new_sector = False
            else:
                door = world.check_for_door(ext.name, player)
                if door is not None:
                    outstanding_doors.append(door)
        if new_sector:
            sector = Sector()
        sector.regions.extend(region_chunk)
        sector.outstanding_doors.extend(outstanding_doors)
        if new_sector:
            sectors.append(sector)
    return sectors


# those with split region starts like Desert/Skull combine for key layouts
def combine_layouts(dungeon_layouts):
    combined = {}
    queue = collections.deque(dungeon_layouts)
    while len(queue) > 0:
        sector, entrance_list = queue.pop()
        if sector.name in split_region_starts:
            dungeon_layouts.remove((sector, entrance_list))
            # desert_entrances.extend(entrance_list)
            if sector.name not in combined:
                combined[sector.name] = sector
            else:
                combined[sector.name].regions.extend(sector.regions)
    for key in combined.keys():
        dungeon_layouts.append((combined[key], region_starts[key]))


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

def shuffle_dungeon_no_repeats(world, player, available_sectors, entrance_region_names):
    logger = logging.getLogger('')
    random.shuffle(available_sectors)
    for sector in available_sectors:
        random.shuffle(sector.outstanding_doors)

    entrance_regions = []
    # current_sector = None
    for region_name in entrance_region_names:
        entrance_regions.append(world.get_region(region_name, player))

    reachable_doors, visited_regions = extend_reachable(entrance_regions, [], world, player)
    # Loop until all available doors are used
    while len(reachable_doors) > 0:
        # Pick a random available door to connect
        door = random.choice(reachable_doors)
        sector = find_sector_for_door(door, available_sectors)
        sector.outstanding_doors.remove(door)
        # door_connected = False
        logger.info('Linking %s', door.name)
        # Find an available region that has a compatible door
        compatibles = find_all_compatible_door_in_sectors_ex(door, available_sectors, reachable_doors)
        while len(compatibles) > 0:
            connect_sector, connect_door = compatibles.pop()
            logger.info('  Found possible new sector via %s', connect_door.name)
            # Check if valid
            if is_valid(door, connect_door, sector, connect_sector, available_sectors):
                # Apply connection and add the new region's doors to the available list
                maybe_connect_two_way(world, door, connect_door, player)
                reachable_doors.remove(door)
                connect_sector.outstanding_doors.remove(connect_door)
                if sector != connect_sector:  # combine if not the same
                    available_sectors.remove(connect_sector)
                    sector.outstanding_doors.extend(connect_sector.outstanding_doors)
                    sector.regions.extend(connect_sector.regions)
                if not door.blocked:
                    connect_region = world.get_entrance(door.dest.name, player).parent_region
                    potential_new_doors, visited_regions = extend_reachable([connect_region], visited_regions, world, player)
                    reachable_doors.extend(potential_new_doors)
                break  # skips else block below
            logger.info(' Not Linking %s to %s', door.name, connect_door.name)
            if len(compatibles) == 0:  # time to try again
                sector.outstanding_doors.insert(0, door)
                if len(reachable_doors) <= 1:
                    raise Exception('Rejected last option due to dead end... infinite loop ensues')
        else:
            # If there's no available region with a door, use an internal connection
            compatibles = find_all_compatible_door_in_list(door, reachable_doors)
            while len(compatibles) > 0:
                connect_door = compatibles.pop()
                logger.info('  Adding loop via %s', connect_door.name)
                # Check if valid
                if is_loop_valid(door, connect_door, sector, available_sectors):
                    maybe_connect_two_way(world, door, connect_door, player)
                    reachable_doors.remove(door)
                    reachable_doors.remove(connect_door)
                    connect_sector = find_sector_for_door(connect_door, available_sectors)
                    connect_sector.outstanding_doors.remove(connect_door)
                    if sector != connect_sector:  # combine if not the same
                        available_sectors.remove(connect_sector)
                        sector.outstanding_doors.extend(connect_sector.outstanding_doors)
                        sector.regions.extend(connect_sector.regions)
                    break  # skips else block with exception
                else:
                    logger.info(' Not Linking %s to %s', door.name, connect_door.name)
                    sector.outstanding_doors.insert(0, door)
                    if len(reachable_doors) <= 2:
                        raise Exception('Rejected last option due to likely improper loops...')
            else:
                raise Exception('Nothing is apparently compatible with %s', door.name)
    # Check that we used everything, we failed otherwise
    if len(available_sectors) != 1:
        logger.warning('Failed to add all regions/doors to dungeon, generation will likely fail.')
    return available_sectors[0]


def extend_reachable(search_regions, visited_regions, world, player):
    region_list = list(search_regions)
    visited_regions = visited_regions
    reachable_doors = []
    while len(region_list) > 0:
        region = region_list.pop()
        visited_regions.append(region)
        for ext in region.exits:
            if ext.connected_region is not None:
                connect_region = ext.connected_region
                if connect_region not in visited_regions and connect_region not in region_list:
                    region_list.append(connect_region)
            else:
                door = world.check_for_door(ext.name, player)
                if door is not None and door.dest is None:  # make sure it isn't a weird blocked door
                    reachable_doors.append(door)
    return reachable_doors, visited_regions


def find_sector_for_door(door, sectors):
    for sector in sectors:
        if door in sector.outstanding_doors:
            return sector
    return None


def find_all_compatible_door_in_sectors_ex(door, sectors, reachable_doors):
    result = []
    for sector in sectors:
        for proposed_door in sector.outstanding_doors:
            if doors_compatible_ignore_keys(door, proposed_door) and proposed_door not in reachable_doors:
                result.append((sector, proposed_door))
    return result


def find_all_compatible_door_in_list(door, doors):
    result = []
    for proposed_door in doors:
        if proposed_door != door and doors_compatible_ignore_keys(door, proposed_door):
            result.append(proposed_door)
    return result


# this method also assumes that sectors have been built appropriately - so only randomizable doors get here
def doors_compatible_ignore_keys(a, b):
    if a.type != b.type:
        return False
    if a.type == DoorType.SpiralStairs and a != b:
        return True
    return a.direction == switch_dir(b.direction)


# todo: path checking needed?
def is_valid(door_a, door_b, sector_a, sector_b, available_sectors):
    if len(available_sectors) == 1:
        return True
    if len(available_sectors) <= 2 and sector_a != sector_b:
        return True
    elif not are_there_outstanding_doors_of_type(door_a, door_b, sector_a, sector_b, available_sectors):
        return False
    elif door_a.blocked and door_b.blocked:  # I can't see this going well unless we are in loop generation...
        return False
    elif not door_a.blocked and not door_b.blocked and sector_a != sector_b:
        return sector_a.outflow() + sector_b.outflow() - 1 > 0  # door_a has been removed already, so a.outflow is reduced by one
    elif door_a.blocked or door_b.blocked and sector_a != sector_b:
        return sector_a.outflow() + sector_b.outflow() > 0
    elif sector_a == sector_b and not door_a.blocked and not door_b.blocked:
        return sector_a.outflow() - 1 > 0
    elif sector_a == sector_b and door_a.blocked or door_b.blocked:
        return sector_a.outflow() > 0
    return False  # not sure how we got here, but it's a bad idea


def is_loop_valid(door_a, door_b, sector, available_sectors):
    if len(available_sectors) == 1:
        return True
    if len(available_sectors) == 2 and door_b not in sector.outstanding_doors:
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
            if door != door_a and door != door_b and pol_idx[door.direction][0] == idx:
                hooks_left = True
                break
        if not hooks_left:
            for door in sector_b.outstanding_doors:
                if door != door_b and door != door_a and pol_idx[door.direction][0] == idx:
                    hooks_left = True
                    break
        return hooks_left
    return True


def shuffle_key_doors(dungeon_sector, entrances, world, player):
    start_regions = convert_regions(entrances, world, player)
    # count number of key doors - this could be a table?
    num_key_doors = 0
    current_doors = []
    skips = []
    for region in dungeon_sector.regions:
        for ext in region.exits:
            d = world.check_for_door(ext.name, player)
            if d is not None and d.smallKey:
                current_doors.append(d)
                if d not in skips:
                    if d.type == DoorType.Interior:
                        skips.append(d.dest)
                    if d.type == DoorType.Normal:
                        for dp in world.paired_doors[player]:
                            if d.name == dp.door_a:
                                skips.append(world.get_door(dp.door_b, player))
                                break
                            elif d.name == dp.door_b:
                                skips.append(world.get_door(dp.door_a, player))
                                break
                    num_key_doors += 1

    # traverse dungeon and find candidates
    candidates = []
    checked_doors = set()
    for region in start_regions:
        possible, checked = find_key_door_candidates(region, checked_doors, world, player)
        candidates.extend(possible)
        checked_doors.update(checked)
    flat_candidates = []
    for candidate in candidates:
        # not valid if: Normal and Pair in is Checked and Pair is not in Candidates
        if candidate.type != DoorType.Normal or candidate.dest not in checked_doors or candidate.dest in candidates:
            flat_candidates.append(candidate)

    # find valid combination of candidates
    paired_candidates = build_pair_list(flat_candidates)
    if len(paired_candidates) < num_key_doors:
        num_key_doors = len(paired_candidates)  # reduce number of key doors
        logging.getLogger('').debug('Lowering key door count because not enough candidates: %s', dungeon_sector.name)
    random.shuffle(paired_candidates)
    combinations = ncr(len(paired_candidates), num_key_doors)
    itr = 0
    proposal = kth_combination(itr, paired_candidates, num_key_doors)
    while not validate_key_layout(dungeon_sector, start_regions, proposal, world, player):
        itr += 1
        if itr >= combinations:
            logging.getLogger('').debug('Lowering key door count because no valid layouts: %s', dungeon_sector.name)
            num_key_doors -= 1
            combinations = ncr(len(paired_candidates), num_key_doors)
            itr = 0
        proposal = kth_combination(itr, paired_candidates, num_key_doors)
    # make changes
    reassign_key_doors(current_doors, proposal, world, player)


def build_pair_list(flat_list):
    paired_list = []
    queue = collections.deque(flat_list)
    while len(queue) > 0:
        d = queue.pop()
        if d.dest in queue:
            paired_list.append((d, d.dest))
            queue.remove(d.dest)
        else:
            paired_list.append(d)
    return paired_list


def flatten_pair_list(paired_list):
    flat_list = []
    for d in paired_list:
        if type(d) is tuple:
            flat_list.append(d[0])
            flat_list.append(d[1])
        else:
            flat_list.append(d)
    return flat_list


def find_key_door_candidates(region, checked, world, player):
    candidates = []
    checked_doors = list(checked)
    queue = collections.deque([(region, None)])
    while len(queue) > 0:
        current, last_door = queue.pop()
        for ext in current.exits:
            d = world.check_for_door(ext.name, player)
            if d is not None and not d.blocked and d.dest is not last_door and d not in checked_doors:
                valid = False
                if 0 <= d.doorListPos < 4 and d.type in [DoorType.Interior, DoorType.Normal, DoorType.SpiralStairs]:
                    room = world.get_room(d.roomIndex, player)
                    position, kind = room.doorList[d.doorListPos]

                    if d.type == DoorType.Interior:
                        valid = kind in [DoorKind.Normal, DoorKind.SmallKey, DoorKind.Bombable, DoorKind.Dashable]
                    elif d.type == DoorType.SpiralStairs:
                        valid = kind in [DoorKind.StairKey, DoorKind.StairKey2, DoorKind.StairKeyLow]
                    elif d.type == DoorType.Normal:
                        d2 = d.dest
                        if d2 not in candidates:
                            room_b = world.get_room(d2.roomIndex, player)
                            pos_b, kind_b = room_b.doorList[d2.doorListPos]
                            okay_normals = [DoorKind.Normal, DoorKind.SmallKey, DoorKind.Bombable,
                                            DoorKind.Dashable, DoorKind.DungeonChanger]
                            valid = kind in okay_normals and kind_b in okay_normals
                        else:
                            valid = True
                if valid:
                    candidates.append(d)
                queue.append((ext.connected_region, d))
                if d is not None:
                    checked_doors.append(d)
    return candidates, checked_doors


def kth_combination(k, l, r):
    if r == 0:
        return []
    elif len(l) == r:
        return l
    else:
        i = ncr(len(l)-1, r-1)
        if k < i:
            return l[0:1] + kth_combination(k, l[1:], r-1)
        else:
            return kth_combination(k-i, l[1:], r)


def ncr(n, r):
    if r == 0:
        return 1
    r = min(r, n-r)
    numerator = reduce(op.mul, range(n, n-r, -1), 1)
    denominator = reduce(op.mul, range(1, r+1), 1)
    return numerator / denominator


class KeyDoorState(object):

    def __init__(self):
        self.avail_doors = []
        self.small_doors = []
        self.big_doors = []
        self.opened_doors = []
        self.big_key_opened = False
        self.big_key_special = False

        self.visited_regions = set()
        self.ttl_locations = 0
        self.used_locations = 0
        self.key_locations = 0
        self.used_smalls = 0

    def copy(self):
        ret = KeyDoorState()
        ret.avail_doors = list(self.avail_doors)
        ret.small_doors = list(self.small_doors)
        ret.big_doors = list(self.big_doors)
        ret.opened_doors = list(self.opened_doors)
        ret.big_key_opened = self.big_key_opened
        ret.big_key_special = self.big_key_special
        ret.visited_regions = set(self.visited_regions)
        ret.ttl_locations = self.ttl_locations
        ret.key_locations = self.key_locations
        ret.used_locations = self.used_locations
        ret.used_smalls = self.used_smalls

        return ret


def validate_key_layout(sector, start_regions, key_door_proposal, world, player):
    flat_proposal = flatten_pair_list(key_door_proposal)
    state = KeyDoorState()
    state.key_locations = len(world.get_dungeon(sector.name, player).small_keys)
    state.big_key_special = world.get_region('Hyrule Dungeon Cellblock', player) in sector.regions
    # Everything in a start region is in key region 0.
    for region in start_regions:
        state.visited_regions.add(region)
        state.ttl_locations += len(region.locations)
        for location in region.locations:
            if location.name in key_only_locations:
                state.key_locations += 1
        add_doors_to_lists(region, flat_proposal, state, world, player)
    return validate_key_layout_r(state, flat_proposal, world, player)


def validate_key_layout_r(state, flat_proposal, world, player):
    # improvements: remove recursion to make this iterative
    # store a cache of various states of opened door to increase speed of checks - many are repetitive
    while len(state.avail_doors) > 0:
        door = state.avail_doors.pop()
        connect_region = world.get_entrance(door.name, player).connected_region
        if not door.blocked and connect_region not in state.visited_regions:
            state.visited_regions.add(connect_region)
            state.ttl_locations += len([x for x in connect_region.locations if '- Prize' not in x.name])
            for location in connect_region.locations:
                if location.name in key_only_locations:
                    state.key_locations += 1
            if connect_region.name == 'Hyrule Dungeon Cellblock':
                state.big_key_opened = True
                state.avail_doors.extend(state.big_doors)
                state.big_doors.clear()
            add_doors_to_lists(connect_region, flat_proposal, state, world, player)
        if len(state.avail_doors) == 0:
            num_smalls = 0
            for small in state.small_doors:
                if small.dest in state.small_doors:
                    num_smalls += 0.5  # half now, half with the dest
                else:
                    num_smalls += 1
            num_bigs = 1 if len(state.big_doors) > 0 else 0  # all or nothing
            if num_smalls == 0 and num_bigs == 0:
                return True   # I think that's the end
            available_small_locations = min(state.ttl_locations - state.used_locations, state.key_locations - state.used_smalls)
            available_big_locations = state.ttl_locations - state.used_locations if not state.big_key_special else 0
            valid = True
            if (num_smalls == 0 or available_small_locations == 0) and (state.big_key_opened or num_bigs == 0 or available_big_locations == 0):
                return False
            else:
                if num_smalls > 0 and available_small_locations > 0:
                    for d in state.small_doors:
                        state_copy = state.copy()
                        state_copy.opened_doors.append(d)
                        state_copy.avail_doors.append(d)
                        state_copy.small_doors.remove(d)
                        if d.dest in flat_proposal:
                            state_copy.opened_doors.append(d.dest)
                            if d.dest in state_copy.small_doors:
                                state_copy.small_doors.remove(d.dest)
                                state_copy.avail_doors.append(d.dest)
                        state_copy.used_locations += 1
                        state_copy.used_smalls += 1
                        valid = validate_key_layout_r(state_copy, flat_proposal, world, player)
                        if not valid:
                            return valid
                if not state.big_key_opened and available_big_locations >= num_bigs > 0:
                    state_copy = state.copy()
                    state_copy.big_key_opened = True
                    state_copy.used_locations += 1
                    state_copy.avail_doors.extend(state.big_doors)
                    state_copy.big_doors.clear()
                    valid = validate_key_layout_r(state_copy, flat_proposal, world, player)
            return valid
    return len(state.small_doors) == 0 and len(state.big_doors) == 0


def add_doors_to_lists(region, key_door_proposal, kd_state, world, player):
    for door in get_doors(world, region, player):
        if not door.blocked:
            if door in key_door_proposal and door not in kd_state.small_doors and door not in kd_state.opened_doors:
                kd_state.small_doors.append(door)
            elif door.bigKey and not kd_state.big_key_opened and door not in kd_state.big_doors:
                kd_state.big_doors.append(door)
            elif door not in kd_state.avail_doors:
                kd_state.avail_doors.append(door)


def reassign_key_doors(current_doors, proposal, world, player):
    flat_proposal = flatten_pair_list(proposal)
    queue = collections.deque(current_doors)
    while len(queue) > 0:
        d = queue.pop()
        if d.type is DoorType.SpiralStairs and d not in proposal:
            world.get_room(d.roomIndex, player).change(d.doorListPos, DoorKind.Waterfall)
            d.smallKey = False
        elif d.type is DoorType.Interior and d not in flat_proposal and d.dest not in flat_proposal:
            world.get_room(d.roomIndex, player).change(d.doorListPos, DoorKind.Normal)
            d.smallKey = False
            d.dest.smallKey = False
            queue.remove(d.dest)
        elif d.type is DoorType.Normal and d not in flat_proposal:
            world.get_room(d.roomIndex, player).change(d.doorListPos, DoorKind.Normal)
            d.smallKey = False
            for dp in world.paired_doors[player]:
                if dp.door_a == d.name or dp.door_b == d.name:
                    dp.pair = False
    for obj in proposal:
        if type(obj) is tuple:
            d1 = obj[0]
            d2 = obj[1]
            if d1.type is DoorType.Interior:
                change_door_to_small_key(d1, world, player)
            else:
                names = [d1.name, d2.name]
                found = False
                for dp in world.paired_doors[player]:
                    if dp.door_a in names and dp.door_b in names:
                        dp.pair = True
                        found = True
                    elif dp.door_a in names:
                        dp.pair = False
                    elif dp.door_b in names:
                        dp.pair = False
                if not found:
                    world.paired_doors[player].append(PairedDoor(d1.name, d2.name))
                    change_door_to_small_key(d1, world, player)
                    change_door_to_small_key(d2, world, player)
            world.spoiler.set_door_type(d1.name+' <-> '+d2.name, 'Key Door', player)
        else:
            d = obj
            if d.type is DoorType.Interior:
                change_door_to_small_key(d, world, player)
            elif d.type is DoorType.SpiralStairs:
                pass  # we don't have spiral stairs candidates yet that aren't already key doors
            elif d.type is DoorType.Normal:
                change_door_to_small_key(d, world, player)
            world.spoiler.set_door_type(d.name, 'Key Door', player)


def change_door_to_small_key(d, world, player):
    d.smallKey = True
    room = world.get_room(d.roomIndex, player)
    if room.doorList[d.doorListPos][1] != DoorKind.SmallKey:
        room.change(d.doorListPos, DoorKind.SmallKey)


# DATA GOES DOWN HERE

logical_connections = [
    ('Hyrule Dungeon North Abyss Catwalk Dropdown', 'Hyrule Dungeon North Abyss'),
    ('Sewers Secret Room Push Block', 'Sewers Secret Room Blocked Path'),
    ('Eastern Hint Tile Push Block', 'Eastern Compass Area'),
    ('Hera Big Chest Landing Exit', 'Hera 4F'),
    ('PoD Arena Main Crystal Path', 'PoD Arena Crystal'),
    ('PoD Arena Crystal Path', 'PoD Arena Main'),
    ('PoD Arena Bridge Drop Down', 'PoD Arena Main'),
    ('PoD Map Balcony Drop Down', 'PoD Sexy Statue'),
    ('PoD Basement Ledge Drop Down', 'PoD Stalfos Basement'),
    ('Swamp Lobby Moat', 'Swamp Entrance'),
    ('Swamp Entrance Moat', 'Swamp Lobby'),
    ('Swamp Trench 1 Approach Dry', 'Swamp Trench 1 Nexus'),
    ('Swamp Trench 1 Approach Key', 'Swamp Trench 1 Key Ledge'),
    ('Swamp Trench 1 Approach Swim Depart', 'Swamp Trench 1 Departure'),
    ('Swamp Trench 1 Nexus Approach', 'Swamp Trench 1 Approach'),
    ('Swamp Trench 1 Nexus Key', 'Swamp Trench 1 Key Ledge'),
    ('Swamp Trench 1 Key Ledge Dry', 'Swamp Trench 1 Nexus'),
    ('Swamp Trench 1 Key Approach', 'Swamp Trench 1 Approach'),
    ('Swamp Trench 1 Key Ledge Depart', 'Swamp Trench 1 Departure'),
    ('Swamp Trench 1 Departure Dry', 'Swamp Trench 1 Nexus'),
    ('Swamp Trench 1 Departure Approach', 'Swamp Trench 1 Approach'),
    ('Swamp Trench 1 Departure Key', 'Swamp Trench 1 Key Ledge'),
    ('Swamp Hub Hook Path', 'Swamp Hub North Ledge'),
    ('Swamp Hub North Ledge Drop Down', 'Swamp Hub'),
    ('Swamp Compass Donut Push Block', 'Swamp Donut Top'),
    ('Swamp Shortcut Blue Barrier', 'Swamp Trench 2 Pots'),
    ('Swamp Trench 2 Pots Blue Barrier', 'Swamp Shortcut'),
    ('Swamp Trench 2 Pots Dry', 'Swamp Trench 2 Blocks'),
    ('Swamp Trench 2 Pots Wet', 'Swamp Trench 2 Departure'),
    ('Swamp Trench 2 Blocks Pots', 'Swamp Trench 2 Pots'),
    ('Swamp Trench 2 Departure Wet', 'Swamp Trench 2 Pots'),
    ('Swamp West Shallows Push Blocks', 'Swamp West Block Path'),
    ('Swamp West Ledge Drop Down', 'Swamp West Shallows'),
    ('Swamp West Ledge Hook Path', 'Swamp Barrier Ledge'),
    ('Swamp Barrier Ledge Drop Down', 'Swamp West Shallows'),
    ('Swamp Barrier Ledge - Orange', 'Swamp Barrier'),
    ('Swamp Barrier - Orange', 'Swamp Barrier Ledge'),
    ('Swamp Barrier Ledge Hook Path', 'Swamp West Ledge'),
    ('Swamp Drain Left Switch', 'Swamp Drain Right'),
    ('Swamp Drain Right Switch', 'Swamp Drain Left'),
    # ('', ''),
    # ('', ''),
    # ('', ''),
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
    ('Tower Room 03 Up Stairs', 'Tower Lone Statue Down Stairs'),
    ('Tower Dark Chargers Up Stairs', 'Tower Dual Statues Down Stairs'),
    ('Tower Dark Archers Up Stairs', 'Tower Red Spears Down Stairs'),
    ('Tower Pacifist Run Up Stairs', 'Tower Push Statue Down Stairs'),
    ('PoD Left Cage Down Stairs', 'PoD Shooter Room Up Stairs'),
    ('PoD Middle Cage Down Stairs', 'PoD Warp Room Up Stairs'),
    ('PoD Basement Ledge Up Stairs', 'PoD Big Key Landing Down Stairs'),
    ('PoD Compass Room W Down Stairs', 'PoD Dark Basement W Up Stairs'),
    ('PoD Compass Room E Down Stairs', 'PoD Dark Basement E Up Stairs'),
    ('Swamp Entrance Down Stairs', 'Swamp Pot Row Up Stairs'),
    ('Swamp West Block Path Up Stairs', 'Swamp Attic Down Stairs'),
    ('Swamp Push Statue Down Stairs', 'Swamp Flooded Room Up Stairs'),
    ('Swamp Left Elbow Down Stairs', 'Swamp Drain Left Up Stairs'),
    ('Swamp Right Elbow Down Stairs', 'Swamp Drain Right Up Stairs'),
    ('Swamp Behind Waterfall Up Stairs', 'Swamp C Down Stairs'),
    # ('', ''),
    # ('', ''),
    # ('', ''),
]

straight_staircases = [
    ('Hyrule Castle Lobby North Stairs', 'Hyrule Castle Throne Room South Stairs'),
    ('Sewers Rope Room North Stairs', 'Sewers Dark Cross South Stairs'),
    ('Tower Catwalk North Stairs', 'Tower Antechamber South Stairs'),
    ('PoD Conveyor North Stairs', 'PoD Map Balcony South Stairs'),
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
    ('PoD Pit Room Freefall', 'PoD Stalfos Basement'),
    ('PoD Pit Room Bomb Hole', 'PoD Basement Ledge'),
    ('PoD Big Key Landing Hole', 'PoD Stalfos Basement'),
    ('Swamp Attic Right Pit', 'Swamp Barrier Ledge'),
    ('Swamp Attic Left Pit', 'Swamp West Ledge'),
    # ('', ''),
    # ('', ''),
]

dungeon_warps = [
    ('Eastern Fairies\' Warp', 'Eastern Courtyard'),
    ('Hera Fairies\' Warp', 'Hera 5F'),
    ('PoD Warp Hint Warp', 'PoD Warp Room'),
    ('PoD Warp Room Warp', 'PoD Warp Hint'),
    ('PoD Stalfos Basement Warp', 'PoD Warp Room'),
    ('PoD Callback Warp', 'PoD Dark Alley'),
    # ('', ''),
]

ladders = [
    ('PoD Bow Statue Down Ladder', 'PoD Dark Pegs Up Ladder')
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
    ('Tower Lobby NW', 'Tower Gold Knights SW'),
    ('Tower Gold Knights EN', 'Tower Room 03 WN'),
    ('Tower Lone Statue WN', 'Tower Dark Maze EN'),
    ('Tower Dark Maze ES', 'Tower Dark Chargers WS'),
    ('Tower Dual Statues WS', 'Tower Dark Pits ES'),
    ('Tower Dark Pits EN', 'Tower Dark Archers WN'),
    ('Tower Red Spears WN', 'Tower Red Guards EN'),
    ('Tower Red Guards SW', 'Tower Circle of Pots NW'),
    ('Tower Circle of Pots WS', 'Tower Pacifist Run ES'),
    ('Tower Push Statue WS', 'Tower Catwalk ES'),
    ('Tower Antechamber NW', 'Tower Altar SW'),
    ('PoD Lobby N', 'PoD Middle Cage S'),
    ('PoD Lobby NW', 'PoD Left Cage SW'),
    ('PoD Lobby NE', 'PoD Middle Cage SE'),
    ('PoD Warp Hint SE', 'PoD Jelly Hall NE'),
    ('PoD Jelly Hall NW', 'PoD Mimics 1 SW'),
    ('PoD Falling Bridge EN', 'PoD Compass Room WN'),
    ('PoD Compass Room SE', 'PoD Harmless Hellway NE'),
    ('PoD Mimics 2 NW', 'PoD Bow Statue SW'),
    ('PoD Dark Pegs WN', 'PoD Lonely Turtle EN'),
    ('PoD Lonely Turtle SW', 'PoD Turtle Party NW'),
    ('PoD Turtle Party ES', 'PoD Callback WS'),
    ('Swamp Trench 1 Nexus N', 'Swamp Trench 1 Alcove S'),
    ('Swamp Trench 1 Key Ledge NW', 'Swamp Hammer Switch SW'),
    ('Swamp Donut Top SE', 'Swamp Donut Bottom NE'),
    ('Swamp Donut Bottom NW', 'Swamp Compass Donut SW'),
    ('Swamp Crystal Switch SE', 'Swamp Shortcut NE'),
    ('Swamp Trench 2 Blocks N', 'Swamp Trench 2 Alcove S'),
    ('Swamp Push Statue NW', 'Swamp Shooters SW'),
    ('Swamp Push Statue NE', 'Swamp Right Elbow SE'),
    ('Swamp Shooters EN', 'Swamp Left Elbow WN'),
    ('Swamp Drain WN', 'Swamp Basement Shallows EN'),
    ('Swamp Flooded Room WS', 'Swamp Basement Shallows ES'),
    ('Swamp Waterfall Room NW', 'Swamp Refill 1 SW'),
    ('Swamp Waterfall Room NE', 'Swamp Behind Waterfall SE'),
    ('Swamp C SE', 'Swamp Waterway NE'),
    ('Swamp Waterway N', 'Swamp I S'),
    ('Swamp Waterway NW', 'Swamp T SW'),
    # ('', ''),
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
    ('PoD Middle Cage N', 'PoD Pit Room S'),
    ('PoD Arena Main NW', 'PoD Falling Bridge SW'),
    ('PoD Falling Bridge WN', 'PoD Dark Maze EN'),
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
    ('Desert Beamos Hall NE', 'Desert Tiles 2 SE'),
    ('PoD Middle Cage N', 'PoD Pit Room S'),
    ('PoD Pit Room NW', 'PoD Arena Main SW'),
    ('PoD Pit Room NE', 'PoD Arena Bridge SE'),
    ('PoD Arena Main NW', 'PoD Falling Bridge SW'),
    ('PoD Arena Crystals E', 'PoD Sexy Statue W'),
    ('PoD Mimics 1 NW', 'PoD Conveyor SW'),
    ('PoD Map Balcony WS', 'PoD Arena Ledge ES'),
    ('PoD Falling Bridge WN', 'PoD Dark Maze EN'),
    ('PoD Dark Maze E', 'PoD Big Chest Balcony W'),
    ('PoD Sexy Statue NW', 'PoD Mimics 2 SW'),
    ('Swamp Pot Row WN', 'Swamp Map Ledge EN'),
    ('Swamp Pot Row WS', 'Swamp Trench 1 Approach ES'),
    ('Swamp Trench 1 Departure WS', 'Swamp Hub ES'),
    ('Swamp Hammer Switch WN', 'Swamp Hub Dead Ledge EN'),
    ('Swamp Hub S', 'Swamp Donut Top N'),
    ('Swamp Hub WS', 'Swamp Trench 2 Pots ES'),
    ('Swamp Hub WN', 'Swamp Crystal Switch EN'),
    ('Swamp Hub North Ledge N', 'Swamp Push Statue S'),
    ('Swamp Trench 2 Departure WS', 'Swamp West Shallows ES'),
    ('Swamp Big Key Ledge WN', 'Swamp Barrier EN'),
    ('Swamp Basement Shallows NW', 'Swamp Waterfall Room SW'),
    # ('', ''),
    # ('', ''),
    # ('', ''),
    # ('', ''),
]

# ('', ''),
default_one_way_connections = [
    ('Sewers Pull Switch S', 'Sanctuary N'),
    ('Eastern Eyegores NE', 'Eastern Boss SE'),
    ('Desert Wall Slide NW', 'Desert Boss SW'),
    ('Tower Altar NW', 'Tower Agahnim 1 SW'),
    ('PoD Harmless Hellway SE', 'PoD Arena Main NE'),
    ('PoD Dark Alley NE', 'PoD Boss SE'),
    ('Swamp T NW', 'Swamp Boss SW'),
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
    ['Hera Lobby', 'Hera Boss'],
    ['Tower Lobby', 'Tower Agahnim 1'],
    ['PoD Lobby', 'PoD Boss'],
    ['Swamp Lobby', 'Swamp Boss']
]

dungeon_x_idx_to_name = {
    0: 'Hyrule Castle',
    1: 'Eastern Palace',
    2: 'Desert Palace',
    3: 'Tower of Hera',
    4: 'Agahnims Tower',
    5: 'Palace of Darkness',
    6: 'Swamp Palace',
#     etc
}
