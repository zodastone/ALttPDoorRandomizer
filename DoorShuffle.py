import random
import collections
from collections import defaultdict
import logging
import operator as op
import time

from functools import reduce
from BaseClasses import RegionType, Door, DoorType, Direction, Sector, Polarity, CrystalBarrier
from Dungeons import hyrule_castle_regions, eastern_regions, desert_regions, hera_regions, tower_regions, pod_regions
from Dungeons import dungeon_regions, region_starts, split_region_starts, flexible_starts
from Dungeons import drop_entrances
from RoomData import DoorKind, PairedDoor
from DungeonGenerator import ExplorationState, convert_regions, generate_dungeon
from KeyDoorShuffle import analyze_dungeon, validate_vanilla_key_logic, build_key_layout, validate_key_layout_ex


def link_doors(world, player):

    # Drop-down connections & push blocks
    for exitName, regionName in logical_connections:
        connect_simple_door(world, exitName, regionName, player)
    # These should all be connected for now as normal connections
    for edge_a, edge_b in interior_doors:
        connect_interior_doors(edge_a, edge_b, world, player)

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
        for exitName, regionName in vanilla_logical_connections:
            connect_simple_door(world, exitName, regionName, player)
        for entrance, ext in spiral_staircases:
            connect_two_way(world, entrance, ext, player)
        for entrance, ext in default_door_connections:
            connect_two_way(world, entrance, ext, player)
        for ent, ext in default_one_way_connections:
            connect_one_way(world, ent, ext, player)
        vanilla_key_logic(world, player)
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
    # for dp in world.paired_doors[player]:
    #     if dp.pair:
    #         logger.debug('Paired Doors: %s with %s (p%d)', dp.door_a, dp.door_b, player)
    #     else:
    #         logger.debug('Unpaired Doors: %s not paired with %s (p%d)', dp.door_a, dp.door_b, player)


def vanilla_key_logic(world, player):
    sectors = []
    for dungeon in [dungeon for dungeon in world.dungeons if dungeon.player == player]:
        sector = Sector()
        sector.name = dungeon.name
        sector.regions.extend(convert_regions(dungeon.regions, world, player))
        sectors.append(sector)

    overworld_prep(world, player)
    entrances_map, potentials, connections = determine_entrance_list(world, player)
    for sector in sectors:
        start_regions = convert_regions(entrances_map[sector.name], world, player)
        doors = convert_key_doors(default_small_key_doors[sector.name], world, player)
        key_layout = build_key_layout(sector, start_regions, doors, world, player)
        valid = validate_key_layout_ex(key_layout, world, player)
        if not valid:
            raise Exception('Vanilla key layout not valid %s' % sector.name)
        if player not in world.key_logic.keys():
            world.key_logic[player] = {}
        key_layout = analyze_dungeon(key_layout, world, player)
        world.key_logic[player][sector.name] = key_layout.key_logic
    validate_vanilla_key_logic(world, player)


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


def convert_key_doors(key_doors, world, player):
    result = []
    for d in key_doors:
        if type(d) is tuple:
            result.append((world.get_door(d[0], player), world.get_door(d[1], player)))
        else:
            result.append(world.get_door(d, player))
    return result


def connect_simple_door(world, exit_name, region_name, player):
    region = world.get_region(region_name, player)
    world.get_entrance(exit_name, player).connect(region)
    d = world.check_for_door(exit_name, player)
    if d is not None:
        d.dest = region


def connect_door_only(world, exit_name, region_name, player):
    region = world.get_region(region_name, player)
    d = world.check_for_door(exit_name, player)
    if d is not None:
        d.dest = region


def connect_interior_doors(a, b, world, player):
    door_a = world.get_door(a, player)
    door_b = world.get_door(b, player)
    if door_a.blocked:
        connect_one_way(world, b, a, player)
    elif door_b.blocked:
        connect_one_way(world, a, b, player)
    else:
        connect_two_way(world, a, b, player)


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
    for d in ['Eastern Hint Tile Blocked Path SE', 'Eastern Darkness S', 'Thieves Hallway SE', 'Mire Left Bridge S',
              'TR Lava Escape SE', 'GT Hidden Spikes SE']:
        door = world.get_door(d, player)
        room = world.get_room(door.roomIndex, player)
        room.change(door.doorListPos, DoorKind.Normal)
        door.smallKey = False
        door.ugly = False


def unpair_big_key_doors(world, player):
    problematic_bk_doors = ['Eastern Courtyard N', 'Eastern Big Key NE', 'Thieves BK Corner NE', 'Mire BK Door Room N',
                            'TR Dodgers NE', 'GT Dash Hall NE']
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
    fix_big_key_doors_with_ugly_smalls(world, player)
    overworld_prep(world, player)
    dungeon_sectors = []
    entrances_map, potentials, connections = determine_entrance_list(world, player)
    for key in dungeon_regions.keys():
        sector_list = convert_to_sectors(dungeon_regions[key], world, player)
        if key in split_region_starts.keys():
            split_sectors = split_up_sectors(sector_list, split_region_starts[key])
            for idx, sub_sector_list in enumerate(split_sectors):
                entrance_list = list(split_region_starts[key][idx])
                # shuffable entrances like pinball, left pit need to be added to entrance list
                if key in flexible_starts.keys():
                    add_shuffled_entrances(sub_sector_list, flexible_starts[key], entrance_list)
                filtered_list = [x for x in entrance_list if x in entrances_map[key]]
                dungeon_sectors.append((key, sub_sector_list, filtered_list))
        else:
            dungeon_sectors.append((key, sector_list, list(entrances_map[key])))

    enabled_entrances = {}
    dungeon_layouts = []
    sector_queue = collections.deque(dungeon_sectors)
    last_key = None
    while len(sector_queue) > 0:
        key, sector_list, entrance_list = sector_queue.popleft()
        split_dungeon = key in split_region_starts.keys()
        origin_list = list(entrance_list)
        find_enabled_origins(sector_list, enabled_entrances, origin_list, entrances_map, key)
        origin_list_sans_drops = remove_drop_origins(origin_list)
        if len(origin_list_sans_drops) <= 0:
            if last_key == key:
                raise Exception('Infinte loop detected %s' % key)
            sector_queue.append((key, sector_list, entrance_list))
            last_key = key
        else:
            ds = generate_dungeon(key, sector_list, origin_list_sans_drops, split_dungeon, world, player)
            find_new_entrances(ds, connections, potentials, enabled_entrances, world, player)
            ds.name = key
            layout_starts = origin_list if len(entrance_list) <= 0 else entrance_list
            dungeon_layouts.append((ds, layout_starts))
            last_key = None

    combine_layouts(dungeon_layouts, entrances_map)
    world.dungeon_layouts[player] = {}
    for sector, entrances in dungeon_layouts:
        find_enabled_origins([sector], enabled_entrances, entrances, entrances_map, sector.name)
        world.dungeon_layouts[player][sector.name] = (sector, entrances_map[sector.name])

    paths = determine_required_paths(world)
    check_required_paths(paths, world, player)

    # shuffle_key_doors for dungeons
    start = time.process_time()
    for sector, entrances in world.dungeon_layouts[player].values():
        shuffle_key_doors(sector, entrances, world, player)
    logging.getLogger('').info('Key door shuffle time: %s', time.process_time()-start)


def determine_entrance_list(world, player):
    entrance_map = {}
    potential_entrances = {}
    connections = {}
    for key, r_names in region_starts.items():
        entrance_map[key] = []
        for region_name in r_names:
            region = world.get_region(region_name, player)
            for ent in region.entrances:
                parent = ent.parent_region
                if parent.type != RegionType.Dungeon or parent.name == 'Sewer Drop':
                    if parent.name not in world.inaccessible_regions[player]:
                        entrance_map[key].append(region_name)
                    else:
                        if ent.parent_region not in potential_entrances.keys():
                            potential_entrances[parent] = []
                        potential_entrances[parent].append(region_name)
                        connections[region_name] = parent
    return entrance_map, potential_entrances, connections


def drop_exception(name):
    return name in ['Skull Pot Circle', 'Skull Back Drop']


def add_shuffled_entrances(sectors, region_list, entrance_list):
    for sector in sectors:
        for region in sector.regions:
            if region.name in region_list:
                entrance_list.append(region.name)


def find_enabled_origins(sectors, enabled, entrance_list, entrance_map, key):
    for sector in sectors:
        for region in sector.regions:
            if region.name in enabled.keys() and region.name not in entrance_list:
                entrance_list.append(region.name)
                origin_reg, origin_dungeon = enabled[region.name]
                if origin_reg != region.name and origin_dungeon != region.dungeon:
                    entrance_map[key].append(region.name)
            if drop_exception(region.name):  # only because they have unique regions
                entrance_list.append(region.name)


def remove_drop_origins(entrance_list):
    return [x for x in entrance_list if x not in drop_entrances]


def find_new_entrances(sector, connections, potentials, enabled, world, player):
    for region in sector.regions:
        if region.name in connections.keys() and (connections[region.name] in potentials.keys() or connections[region.name].name in world.inaccessible_regions[player]):
            new_region = connections[region.name]
            if new_region in potentials.keys():
                for potential in potentials.pop(new_region):
                    enabled[potential] = (region.name, region.dungeon)
            # see if this unexplored region connects elsewhere
            queue = collections.deque(new_region.exits)
            visited = set()
            while len(queue) > 0:
                ext = queue.popleft()
                visited.add(ext)
                region_name = ext.connected_region.name
                if region_name in connections.keys() and connections[region_name] in potentials.keys():
                    for potential in potentials.pop(connections[region_name]):
                        enabled[potential] = (region.name, region.dungeon)
                if ext.connected_region.name in world.inaccessible_regions[player]:
                    for new_exit in ext.connected_region.exits:
                        if new_exit not in visited:
                            queue.append(new_exit)


def within_dungeon_legacy(world, player):
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

    world.dungeon_layouts[player] = {}
    for key in dungeon_regions.keys():
        world.dungeon_layouts[player][key] = (key, region_starts[key])


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


def get_entrance_doors(world, region, player):
    res = []
    for exit in region.entrances:
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
# 3. prevent soft locks due to key usage (algorithm written)
# 4. rules in place to affect item placement (lamp, keys, etc. -- in rules)
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
    # for key, sector_list, entrance_list in dungeon_sectors:
        # ds = shuffle_dungeon_no_repeats_new(world, player, sector_list, entrance_list)
        # ds.name = key
        # dungeon_layouts.append((ds, entrance_list))

    combine_layouts(dungeon_layouts)

    for layout in dungeon_layouts:
        shuffle_key_doors(layout[0], layout[1], world, player)


def experiment(world, player):
    within_dungeon(world, player)


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
                if door is not None and door.controller is None and door.dest is None:
                    outstanding_doors.append(door)
        if new_sector:
            sector = Sector()
        sector.regions.extend(region_chunk)
        sector.outstanding_doors.extend(outstanding_doors)
        if new_sector:
            sectors.append(sector)
    return sectors


# those with split region starts like Desert/Skull combine for key layouts
def combine_layouts(dungeon_layouts, entrances_map):
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
        dungeon_layouts.append((combined[key], list(entrances_map[key])))


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


def is_polarity_neutral(sector_list):
    pol = Polarity()
    for sector in sector_list:
        pol += sector.polarity()
    return pol.is_neutral()


search_iterations = 0


def is_proposal_valid(proposal, buckets, candidates):
    logger = logging.getLogger('')
    global search_iterations
    search_iterations = search_iterations + 1
    if search_iterations % 100 == 0:
        logger.debug('Iteration %s', search_iterations)
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
        valid = is_polarity_neutral(test)
        if not valid:
            return False
        for sector in test:
            other_sectors = list(test)
            other_sectors.remove(sector)
            sector_mag = sector.magnitude()
            other_mag = sum_vector(other_sectors, lambda x: x.magnitude())
            for i in range(len(sector_mag)):
                if sector_mag[i] > 0 and other_mag[i] == 0:
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


def valid_region_to_explore(region, world, player):
    return region.type == RegionType.Dungeon or region.name in world.inaccessible_regions[player]


def shuffle_key_doors(dungeon_sector, entrances, world, player):
    logger = logging.getLogger('')
    logger.info('Shuffling Key doors for %s', dungeon_sector.name)
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
        logger.info('Lowering key door count because not enough candidates: %s', dungeon_sector.name)
    combinations = ncr(len(paired_candidates), num_key_doors)
    itr = 0
    start = time.process_time()
    sample_list = list(range(0, int(combinations)))
    random.shuffle(sample_list)
    proposal = kth_combination(sample_list[itr], paired_candidates, num_key_doors)

    key_layout = build_key_layout(dungeon_sector, start_regions, proposal, world, player)
    while not validate_key_layout_ex(key_layout, world, player):
        itr += 1
        if itr >= combinations:
            logger.info('Lowering key door count because no valid layouts: %s', dungeon_sector.name)
            num_key_doors -= 1
            if num_key_doors < 0:
                raise Exception('Bad dungeon %s - 0 key doors not valid' % dungeon_sector.name)
            combinations = ncr(len(paired_candidates), num_key_doors)
            sample_list = list(range(0, int(combinations)))
            random.shuffle(sample_list)
            itr = 0
        proposal = kth_combination(sample_list[itr], paired_candidates, num_key_doors)
        key_layout.reset(proposal)
        if (itr+1) % 1000 == 0:
            mark = time.process_time()-start
            logger.info('%s time elapsed. %s iterations/s', mark, itr/mark)
    # make changes
    if player not in world.key_logic.keys():
        world.key_logic[player] = {}
    key_layout_new = analyze_dungeon(key_layout, world, player)
    reassign_key_doors(current_doors, proposal, world, player)
    log_key_logic(dungeon_sector.name, key_layout_new.key_logic)
    world.key_logic[player][dungeon_sector.name] = key_layout_new.key_logic


def log_key_logic(d_name, key_logic):
    logger = logging.getLogger('')
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Key Logic for %s', d_name)
        if len(key_logic.bk_restricted) > 0:
            logger.debug('-BK Restrictions')
            for restriction in key_logic.bk_restricted:
                logger.debug(restriction)
        if len(key_logic.sm_restricted) > 0:
            logger.debug('-Small Restrictions')
            for restriction in key_logic.sm_restricted:
                logger.debug(restriction)
        for key in key_logic.door_rules.keys():
            rule = key_logic.door_rules[key]
            logger.debug('--Rule for %s: Nrm:%s Allow:%s Loc:%s Alt:%s', key, rule.small_key_num, rule.allow_small, rule.small_location, rule.alternate_small_key)
            if rule.alternate_small_key is not None:
                for loc in rule.alternate_big_key_loc:
                    logger.debug('---BK Loc %s', loc.name)


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
    dungeon = region.dungeon
    candidates = []
    checked_doors = list(checked)
    queue = collections.deque([(region, None, None)])
    while len(queue) > 0:
        current, last_door, last_region = queue.pop()
        for ext in current.exits:
            d = world.check_for_door(ext.name, player)
            if d is not None and not d.blocked and d.dest is not last_door and d.dest is not last_region and d not in checked_doors:
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
                if ext.connected_region.type != RegionType.Dungeon or ext.connected_region.dungeon == dungeon:
                    queue.append((ext.connected_region, d, current))
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


def reassign_key_doors(current_doors, proposal, world, player):
    logger = logging.getLogger('')
    flat_proposal = flatten_pair_list(proposal)
    queue = collections.deque(current_doors)
    while len(queue) > 0:
        d = queue.pop()
        if d.type is DoorType.SpiralStairs and d not in proposal:
            room = world.get_room(d.roomIndex, player)
            if room.doorList[d.doorListPos][1] == DoorKind.StairKeyLow:
                room.delete(d.doorListPos)
            else:
                if len(room.doorList) > 1:
                    room.mirror(d.doorListPos)
                else:
                    room.delete(d.doorListPos)
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
                d2.smallKey = True  # ensure flag is set
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
            logger.debug('Key Door: %s', d1.name+' <-> '+d2.name)
        else:
            d = obj
            if d.type is DoorType.Interior:
                change_door_to_small_key(d, world, player)
                d.dest.smallKey = True  # ensure flag is set
            elif d.type is DoorType.SpiralStairs:
                pass  # we don't have spiral stairs candidates yet that aren't already key doors
            elif d.type is DoorType.Normal:
                change_door_to_small_key(d, world, player)
            world.spoiler.set_door_type(d.name, 'Key Door', player)
            logger.debug('Key Door: %s', d.name)


def change_door_to_small_key(d, world, player):
    d.smallKey = True
    room = world.get_room(d.roomIndex, player)
    if room.doorList[d.doorListPos][1] != DoorKind.SmallKey:
        room.change(d.doorListPos, DoorKind.SmallKey)


def determine_required_paths(world):
    paths = {
        'Hyrule Castle': [],
        'Eastern Palace': ['Eastern Boss'],
        'Desert Palace': ['Desert Boss'],
        'Tower of Hera': ['Hera Boss'],
        'Agahnims Tower': ['Tower Agahnim 1'],
        'Palace of Darkness': ['PoD Boss'],
        'Swamp Palace': ['Swamp Boss'],
        'Skull Woods': ['Skull Boss'],
        'Thieves Town': ['Thieves Boss', ('Thieves Blind\'s Cell', 'Thieves Boss')],
        'Ice Palace': ['Ice Boss'],
        'Misery Mire': ['Mire Boss'],
        'Turtle Rock': ['TR Boss'],
        'Ganons Tower': ['GT Agahnim 2']
        }
    if world.shuffle == 'vanilla':
        paths['Skull Woods'].insert(0, 'Skull 2 West Lobby')
        paths['Turtle Rock'].insert(0, 'TR Eye Bridge')
        paths['Turtle Rock'].insert(0, 'TR Big Chest Entrance')
        paths['Turtle Rock'].insert(0, 'TR Lazy Eyes')
        if world.mode == 'standard':
            paths['Hyrule Castle'].append('Hyrule Dungeon Cellblock')
            # noinspection PyTypeChecker
            paths['Hyrule Castle'].append(('Hyrule Dungeon Cellblock', 'Sanctuary'))
    if world.doorShuffle in ['basic', 'experimental']:
        paths['Thieves Town'].append('Thieves Attic Window')
    return paths


def overworld_prep(world, player):
    find_inaccessible_regions(world, player)
    add_inaccessible_doors(world, player)


def find_inaccessible_regions(world, player):
    world.inaccessible_regions[player] = []
    if world.mode != 'inverted':
        start_regions = ['Links House', 'Sanctuary']
    else:
        start_regions = ['Inverted Links House', 'Inverted Dark Sanctuary']
    regs = convert_regions(start_regions, world, player)
    all_regions = set([r for r in world.regions if r.player == player and r.type is not RegionType.Dungeon])
    visited_regions = set()
    queue = collections.deque(regs)
    while len(queue) > 0:
        next_region = queue.popleft()
        visited_regions.add(next_region)
        for ext in next_region.exits:
            connect = ext.connected_region
            if connect is not None and connect.type is not RegionType.Dungeon and connect not in queue and connect not in visited_regions:
                queue.append(connect)
    world.inaccessible_regions[player].extend([r.name for r in all_regions.difference(visited_regions) if valid_inaccessible_region(r)])
    if world.mode == 'standard':
        world.inaccessible_regions[player].append('Hyrule Castle Ledge')
        world.inaccessible_regions[player].append('Sewer Drop')
    logger = logging.getLogger('')
    logger.info('Inaccessible Regions:')
    for r in world.inaccessible_regions[player]:
        logger.info('%s', r)


def valid_inaccessible_region(r):
    return r.type is not RegionType.Cave or (len(r.exits) > 0 and r.name not in ['Links House', 'Chris Houlihan Room'])


def add_inaccessible_doors(world, player):
    if 'Skull Woods Forest (West)' in world.inaccessible_regions[player]:
        create_door(world, player, 'Skull Woods Second Section Door (West)', 'Skull Woods Forest (West)')
        create_door(world, player, 'Skull Woods Second Section Hole', 'Skull Woods Forest (West)')
        create_door(world, player, 'Skull Woods Final Section', 'Skull Woods Forest (West)')
    if 'Dark Death Mountain Ledge' in world.inaccessible_regions[player]:
        create_door(world, player, 'Dark Death Mountain Ledge (East)', 'Dark Death Mountain Ledge')
        create_door(world, player, 'Dark Death Mountain Ledge (West)', 'Dark Death Mountain Ledge')
        create_door(world, player, 'Mimic Cave Mirror Spot', 'Dark Death Mountain Ledge')
    if 'Mimic Cave Ledge' in world.inaccessible_regions[player]:
        create_door(world, player, 'Mimic Cave', 'Mimic Cave Ledge')
    if 'Dark Death Mountain Isolated Ledge' in world.inaccessible_regions[player]:
        create_door(world, player, 'Turtle Rock Isolated Ledge Entrance', 'Dark Death Mountain Isolated Ledge')
    if 'Death Mountain Floating Island (Dark World)' in world.inaccessible_regions[player]:
        create_door(world, player, 'Hookshot Cave Back Entrance', 'Death Mountain Floating Island (Dark World)')
    if 'Bumper Cave Ledge' in world.inaccessible_regions[player]:
        create_door(world, player, 'Bumper Cave (Top)', 'Bumper Cave Ledge')
        create_door(world, player, 'Bumper Cave Ledge Mirror Spot', 'Bumper Cave Ledge')
    if 'Death Mountain Return Ledge' in world.inaccessible_regions[player]:
        create_door(world, player, 'Death Mountain Return Cave (West)', 'Death Mountain Return Ledge')
    if 'Desert Palace Lone Stairs' in world.inaccessible_regions[player]:
        create_door(world, player, 'Desert Palace Entrance (East)', 'Desert Palace Lone Stairs')
    if world.mode == 'standard' and 'Hyrule Castle Ledge' in world.inaccessible_regions[player]:
        create_door(world, player, 'Hyrule Castle Entrance (East)', 'Hyrule Castle Ledge')
        create_door(world, player, 'Hyrule Castle Entrance (West)', 'Hyrule Castle Ledge')


def create_door(world, player, entName, region_name):
    connect = world.get_entrance(entName, player).connected_region
    for ext in connect.exits:
        if ext.connected_region is not None and ext.connected_region.name == region_name:
            d = Door(player, ext.name, DoorType.Logical),
            world.doors += d
            connect_door_only(world, ext.name, ext.connected_region, player)
    d = Door(player, entName, DoorType.Logical),
    world.doors += d
    connect_door_only(world, entName, connect, player)


def check_required_paths(paths, world, player):
    for dungeon_name in paths.keys():
        sector, entrances = world.dungeon_layouts[player][dungeon_name]
        if len(paths[dungeon_name]) > 0:
            states_to_explore = defaultdict(list)
            for path in paths[dungeon_name]:
                if type(path) is tuple:
                    states_to_explore[tuple([path[0]])].append(path[1])
                else:
                    states_to_explore[tuple(entrances)].append(path)
            cached_initial_state = None
            for start_regs, dest_regs in states_to_explore.items():
                check_paths = convert_regions(dest_regs, world, player)
                start_regions = convert_regions(start_regs, world, player)
                initial = start_regs == tuple(entrances)
                if not initial or cached_initial_state is None:
                    init = determine_init_crystal(initial, cached_initial_state, start_regions)
                    state = ExplorationState(init, dungeon_name)
                    for region in start_regions:
                        state.visit_region(region)
                        state.add_all_doors_check_unattached(region, world, player)
                    explore_state(state, world, player)
                    if initial and cached_initial_state is None:
                        cached_initial_state = state
                else:
                    state = cached_initial_state
                valid, bad_region = check_if_regions_visited(state, check_paths)
                if not valid:
                    if check_for_pinball_fix(state, bad_region, world, player):
                        explore_state(state, world, player)
                        valid, bad_region = check_if_regions_visited(state, check_paths)
                if not valid:
                    raise Exception('%s cannot reach %s' % (dungeon_name, bad_region.name))


def determine_init_crystal(initial, state, start_regions):
    if initial:
        return CrystalBarrier.Orange
    if state is None:
        raise Exception('Please start path checking from the entrances')
    if len(start_regions) > 1:
        raise NotImplementedError('Path checking for multiple start regions (not the entrances) not implemented, use more paths instead')
    start_region = start_regions[0]
    if start_region in state.visited_blue and start_region in state.visited_orange:
        return CrystalBarrier.Either
    elif start_region in state.visited_blue:
        return CrystalBarrier.Blue
    elif start_region in state.visited_orange:
        return CrystalBarrier.Orange
    else:
        raise Exception('Can\'t get to %s from initial state', start_region.name)


def explore_state(state, world, player):
    while len(state.avail_doors) > 0:
        door = state.next_avail_door().door
        connect_region = world.get_entrance(door.name, player).connected_region
        if state.can_traverse(door) and not state.visited(connect_region) and valid_region_to_explore(connect_region, world, player):
            state.visit_region(connect_region)
            state.add_all_doors_check_unattached(connect_region, world, player)


def check_if_regions_visited(state, check_paths):
    valid = True
    breaking_region = None
    for region_target in check_paths:
        if not state.visited_at_all(region_target):
            valid = False
            breaking_region = region_target
            break
    return valid, breaking_region


def check_for_pinball_fix(state, bad_region, world, player):
    pinball_region = world.get_region('Skull Pinball', player)
    if bad_region.name == 'Skull 2 West Lobby' and state.visited_at_all(pinball_region):
        door = world.get_door('Skull Pinball WS', player)
        room = world.get_room(door.roomIndex, player)
        if room.doorList[door.doorListPos][1] == DoorKind.Trap:
            room.change(door.doorListPos, DoorKind.Normal)
            door.trapFlag = 0x0
            door.blocked = False
            connect_two_way(world, door.name, door.dest.name, player)
            state.add_all_doors_check_unattached(pinball_region, world, player)
            return True
    return False


# DATA GOES DOWN HERE

logical_connections = [
    ('Hyrule Dungeon North Abyss Catwalk Dropdown', 'Hyrule Dungeon North Abyss'),
    ('Sewers Secret Room Push Block', 'Sewers Secret Room Blocked Path'),
    ('Eastern Hint Tile Push Block', 'Eastern Hint Tile'),
    ('Eastern Map Balcony Hook Path', 'Eastern Map Room'),
    ('Eastern Map Room Drop Down', 'Eastern Map Balcony'),
    ('Hera Big Chest Landing Exit', 'Hera 4F'),
    ('PoD Arena Bonk Path', 'PoD Arena Bridge'),
    ('PoD Arena Main Crystal Path', 'PoD Arena Crystal'),
    ('PoD Arena Crystal Path', 'PoD Arena Main'),
    ('PoD Arena Main Orange Barrier', 'PoD Arena North'),
    ('PoD Arena North Drop Down', 'PoD Arena Main'),
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
    ('Swamp West Block Path Drop Down', 'Swamp West Shallows'),
    ('Swamp West Ledge Drop Down', 'Swamp West Shallows'),
    ('Swamp West Ledge Hook Path', 'Swamp Barrier Ledge'),
    ('Swamp Barrier Ledge Drop Down', 'Swamp West Shallows'),
    ('Swamp Barrier Ledge - Orange', 'Swamp Barrier'),
    ('Swamp Barrier - Orange', 'Swamp Barrier Ledge'),
    ('Swamp Barrier Ledge Hook Path', 'Swamp West Ledge'),
    ('Swamp Drain Right Switch', 'Swamp Drain Left'),
    ('Swamp Flooded Spot Ladder', 'Swamp Flooded Room'),
    ('Swamp Flooded Room Ladder', 'Swamp Flooded Spot'),
    ('Skull Pot Circle Star Path', 'Skull Map Room'),
    ('Skull Big Chest Hookpath', 'Skull 1 Lobby'),
    ('Skull Back Drop Star Path', 'Skull Small Hall'),
    ('Thieves Rail Ledge Drop Down', 'Thieves BK Corner'),
    ('Thieves Hellway Orange Barrier', 'Thieves Hellway S Crystal'),
    ('Thieves Hellway Crystal Orange Barrier', 'Thieves Hellway'),
    ('Thieves Hellway Blue Barrier', 'Thieves Hellway N Crystal'),
    ('Thieves Hellway Crystal Blue Barrier', 'Thieves Hellway'),
    ('Thieves Basement Block Path', 'Thieves Blocked Entry'),
    ('Thieves Blocked Entry Path', 'Thieves Basement Block'),
    ('Thieves Conveyor Bridge Block Path', 'Thieves Conveyor Block'),
    ('Thieves Conveyor Block Path', 'Thieves Conveyor Bridge'),
    ('Ice Cross Bottom Push Block Left', 'Ice Floor Switch'),
    ('Ice Cross Right Push Block Top', 'Ice Bomb Drop'),
    ('Ice Cross Top Push Block Left', 'Ice Floor Switch'),
    ('Ice Big Key Push Block', 'Ice Dead End'),
    ('Ice Bomb Jump Ledge Orange Barrier', 'Ice Bomb Jump Catwalk'),
    ('Ice Bomb Jump Catwalk Orange Barrier', 'Ice Bomb Jump Ledge'),
    ('Ice Hookshot Ledge Path', 'Ice Hookshot Balcony'),
    ('Ice Hookshot Balcony Path', 'Ice Hookshot Ledge'),
    ('Ice Crystal Right Orange Barrier', 'Ice Crystal Left'),
    ('Ice Crystal Left Orange Barrier', 'Ice Crystal Right'),
    ('Ice Crystal Left Blue Barrier', 'Ice Crystal Block'),
    ('Ice Crystal Block Exit', 'Ice Crystal Left'),
    ('Ice Big Chest Landing Push Blocks', 'Ice Big Chest View'),
    ('Mire Lobby Gap', 'Mire Post-Gap'),
    ('Mire Post-Gap Gap', 'Mire Lobby'),
    ('Mire Hub Upper Blue Barrier', 'Mire Hub Top'),
    ('Mire Hub Lower Blue Barrier', 'Mire Hub Right'),
    ('Mire Hub Right Blue Barrier', 'Mire Hub'),
    ('Mire Hub Top Blue Barrier', 'Mire Hub'),
    ('Mire Map Spike Side Drop Down', 'Mire Lone Shooter'),
    ('Mire Map Spike Side Blue Barrier', 'Mire Crystal Dead End'),
    ('Mire Map Spot Blue Barrier', 'Mire Crystal Dead End'),
    ('Mire Crystal Dead End Left Barrier', 'Mire Map Spot'),
    ('Mire Crystal Dead End Right Barrier', 'Mire Map Spike Side'),
    ('Mire Left Bridge Hook Path', 'Mire Right Bridge'),
    ('Mire Crystal Right Orange Barrier', 'Mire Crystal Mid'),
    ('Mire Crystal Mid Orange Barrier', 'Mire Crystal Right'),
    ('Mire Crystal Mid Blue Barrier', 'Mire Crystal Left'),
    ('Mire Crystal Left Blue Barrier', 'Mire Crystal Mid'),
    ('Mire Firesnake Skip Orange Barrier', 'Mire Antechamber'),
    ('Mire Antechamber Orange Barrier', 'Mire Firesnake Skip'),
    ('Mire Compass Blue Barrier', 'Mire Compass Chest'),
    ('Mire Compass Chest Exit', 'Mire Compass Room'),
    ('Mire South Fish Blue Barrier', 'Mire Fishbone'),
    ('Mire Fishbone Blue Barrier', 'Mire South Fish'),
    ('TR Main Lobby Gap', 'TR Lobby Ledge'),
    ('TR Lobby Ledge Gap', 'TR Main Lobby'),
    ('TR Pipe Ledge Drop Down', 'TR Pipe Pit'),
    ('TR Big Chest Gap', 'TR Big Chest Entrance'),
    ('TR Big Chest Entrance Gap', 'TR Big Chest'),
    ('TR Crystal Maze Forwards Path', 'TR Crystal Maze End'),
    ('TR Crystal Maze Blue Path', 'TR Crystal Maze'),
    ('TR Crystal Maze Cane Path', 'TR Crystal Maze'),
    ('GT Blocked Stairs Block Path', 'GT Big Chest'),
    ('GT Hookshot East-North Path', 'GT Hookshot North Platform'),
    ('GT Hookshot East-South Path', 'GT Hookshot South Platform'),
    ('GT Hookshot North-East Path', 'GT Hookshot East Platform'),
    ('GT Hookshot North-South Path', 'GT Hookshot South Platform'),
    ('GT Hookshot South-East Path', 'GT Hookshot East Platform'),
    ('GT Hookshot South-North Path', 'GT Hookshot North Platform'),
    ('GT Hookshot Platform Blue Barrier', 'GT Hookshot South Entry'),
    ('GT Hookshot Entry Blue Barrier', 'GT Hookshot South Platform'),
    ('GT Double Switch Orange Barrier', 'GT Double Switch Switches'),
    ('GT Double Switch Orange Barrier 2', 'GT Double Switch Key Spot'),
    ('GT Double Switch Transition Blue', 'GT Double Switch Exit'),
    ('GT Double Switch Blue Path', 'GT Double Switch Transition'),
    ('GT Double Switch Orange Path', 'GT Double Switch Entry'),
    ('GT Double Switch Key Blue Path', 'GT Double Switch Exit'),
    ('GT Double Switch Key Orange Path', 'GT Double Switch Entry'),
    ('GT Double Switch Blue Barrier', 'GT Double Switch Key Spot'),
    ('GT Warp Maze - Pit Section Warp Spot', 'GT Warp Maze - Pit Exit Warp Spot'),
    ('GT Warp Maze Exit Section Warp Spot', 'GT Warp Maze - Pit Exit Warp Spot'),
    ('GT Firesnake Room Hook Path', 'GT Firesnake Room Ledge'),
    ('GT Left Moldorm Ledge Drop Down', 'GT Moldorm'),
    ('GT Right Moldorm Ledge Drop Down', 'GT Moldorm'),
    ('GT Moldorm Gap', 'GT Validation'),
    ('GT Validation Block Path', 'GT Validation Door')
]

vanilla_logical_connections = [
    ('Ice Cross Left Push Block', 'Ice Compass Room'),
    ('Ice Cross Right Push Block Bottom', 'Ice Compass Room'),
    ('Ice Cross Bottom Push Block Right', 'Ice Pengator Switch'),
    ('Ice Cross Top Push Block Right', 'Ice Pengator Switch'),
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
    ('Thieves Spike Switch Up Stairs', 'Thieves Attic Down Stairs'),
    ('Thieves Conveyor Maze Down Stairs', 'Thieves Basement Block Up Stairs'),
    ('Ice Jelly Key Down Stairs', 'Ice Floor Switch Up Stairs'),
    ('Ice Narrow Corridor Down Stairs', 'Ice Pengator Trap Up Stairs'),
    ('Ice Spike Room Up Stairs', 'Ice Hammer Block Down Stairs'),
    ('Ice Spike Room Down Stairs', 'Ice Spikeball Up Stairs'),
    ('Ice Lonely Freezor Down Stairs', 'Iced T Up Stairs'),
    ('Ice Backwards Room Down Stairs', 'Ice Anti-Fairy Up Stairs'),
    ('Mire Post-Gap Down Stairs', 'Mire 2 Up Stairs'),
    ('Mire Left Bridge Down Stairs', 'Mire Dark Shooters Up Stairs'),
    ('Mire Conveyor Barrier Up Stairs', 'Mire Torches Top Down Stairs'),
    ('Mire Falling Foes Up Stairs', 'Mire Firesnake Skip Down Stairs'),
    ('TR Chain Chomps Down Stairs', 'TR Pipe Pit Up Stairs'),
    ('TR Crystaroller Down Stairs', 'TR Dark Ride Up Stairs'),
    ('GT Lobby Left Down Stairs', 'GT Torch Up Stairs'),
    ('GT Lobby Up Stairs', 'GT Crystal Paths Down Stairs'),
    ('GT Lobby Right Down Stairs', 'GT Hope Room Up Stairs'),
    ('GT Blocked Stairs Down Stairs', 'GT Four Torches Up Stairs'),
    ('GT Cannonball Bridge Up Stairs', 'GT Gauntlet 1 Down Stairs'),
    ('GT Quad Pot Up Stairs', 'GT Wizzrobes 1 Down Stairs'),
    ('GT Moldorm Pit Up Stairs', 'GT Right Moldorm Ledge Down Stairs'),
    ('GT Frozen Over Up Stairs', 'GT Brightly Lit Hall Down Stairs')
]

straight_staircases = [
    ('Hyrule Castle Lobby North Stairs', 'Hyrule Castle Throne Room South Stairs'),
    ('Sewers Rope Room North Stairs', 'Sewers Dark Cross South Stairs'),
    ('Tower Catwalk North Stairs', 'Tower Antechamber South Stairs'),
    ('PoD Conveyor North Stairs', 'PoD Map Balcony South Stairs'),
    ('TR Crystal Maze North Stairs', 'TR Final Abyss South Stairs')
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
    ('Desert Sandworm Corner E Edge', 'Desert West Wing N Edge'),
    ('Thieves Lobby N Edge', 'Thieves Ambush S Edge'),
    ('Thieves Lobby NE Edge', 'Thieves Ambush SE Edge'),
    ('Thieves Ambush ES Edge', 'Thieves BK Corner WS Edge'),
    ('Thieves Ambush EN Edge', 'Thieves BK Corner WN Edge'),
    ('Thieves BK Corner S Edge', 'Thieves Compass Room N Edge'),
    ('Thieves BK Corner SW Edge', 'Thieves Compass Room NW Edge'),
    ('Thieves Compass Room WS Edge', 'Thieves Big Chest Nook WS Edge'),
    ('Thieves Cricket Hall Left Edge', 'Thieves Cricket Hall Right Edge')
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
    ('Skull Final Drop Hole', 'Skull Boss'),
    ('Ice Bomb Drop Hole', 'Ice Stalfos Hint'),
    ('Ice Falling Square Hole', 'Ice Tall Hint'),
    ('Ice Freezors Hole', 'Ice Big Chest View'),
    ('Ice Freezors Ledge Hole', 'Ice Big Chest View'),
    ('Ice Freezors Bomb Hole', 'Ice Big Chest Landing'),
    ('Ice Crystal Block Hole', 'Ice Switch Room'),
    ('Ice Crystal Right Blue Hole', 'Ice Switch Room'),
    ('Ice Backwards Room Hole', 'Ice Fairy'),
    ('Ice Antechamber Hole', 'Ice Boss'),
    ('Mire Attic Hint Hole', 'Mire BK Chest Ledge'),
    ('GT Bob\'s Room Hole', 'GT Ice Armos'),
    ('GT Falling Torches Hole', 'GT Staredown'),
    ('GT Moldorm Hole', 'GT Moldorm Pit')
]

dungeon_warps = [
    ('Eastern Fairies\' Warp', 'Eastern Courtyard'),
    ('Hera Fairies\' Warp', 'Hera 5F'),
    ('PoD Warp Hint Warp', 'PoD Warp Room'),
    ('PoD Warp Room Warp', 'PoD Warp Hint'),
    ('PoD Stalfos Basement Warp', 'PoD Warp Room'),
    ('PoD Callback Warp', 'PoD Dark Alley'),
    ('Ice Fairy Warp', 'Ice Anti-Fairy'),
    ('Mire Lone Warp Warp', 'Mire BK Door Room'),
    ('Mire Warping Pool Warp', 'Mire Square Rail'),
    ('GT Compass Room Warp', 'GT Conveyor Star Pits'),
    ('GT Spike Crystals Warp', 'GT Firesnake Room'),
    ('GT Warp Maze - Left Section Warp', 'GT Warp Maze - Rando Rail'),
    ('GT Warp Maze - Mid Section Left Warp', 'GT Warp Maze - Main Rails'),
    ('GT Warp Maze - Mid Section Right Warp', 'GT Warp Maze - Main Rails'),
    ('GT Warp Maze - Right Section Warp', 'GT Warp Maze - Main Rails'),
    ('GT Warp Maze - Pit Exit Warp', 'GT Warp Maze - Pot Rail'),
    ('GT Warp Maze - Rail Choice Left Warp', 'GT Warp Maze - Left Section'),
    ('GT Warp Maze - Rail Choice Right Warp', 'GT Warp Maze - Mid Section'),
    ('GT Warp Maze - Rando Rail Warp', 'GT Warp Maze - Mid Section'),
    ('GT Warp Maze - Main Rails Best Warp', 'GT Warp Maze - Pit Section'),
    ('GT Warp Maze - Main Rails Mid Left Warp', 'GT Warp Maze - Mid Section'),
    ('GT Warp Maze - Main Rails Mid Right Warp', 'GT Warp Maze - Mid Section'),
    ('GT Warp Maze - Main Rails Right Top Warp', 'GT Warp Maze - Right Section'),
    ('GT Warp Maze - Main Rails Right Mid Warp', 'GT Warp Maze - Right Section'),
    ('GT Warp Maze - Pot Rail Warp', 'GT Warp Maze Exit Section'),
    ('GT Hidden Star Warp', 'GT Invisible Bridges')
]

ladders = [
    ('PoD Bow Statue Down Ladder', 'PoD Dark Pegs Up Ladder'),
    ('Ice Big Key Down Ladder', 'Ice Tongue Pull Up Ladder'),
    ('Ice Firebar Down Ladder', 'Ice Freezors Up Ladder'),
    ('GT Staredown Up Ladder', 'GT Falling Torches Down Ladder')
]

interior_doors = [
    ('Hyrule Dungeon Armory Interior Key Door S', 'Hyrule Dungeon Armory Interior Key Door N'),
    ('Hyrule Dungeon Armory ES', 'Hyrule Dungeon Armory Boomerang WS'),
    ('Hyrule Dungeon Map Room Key Door S', 'Hyrule Dungeon North Abyss Key Door N'),
    ('Sewers Rat Path WS', 'Sewers Secret Room ES'),
    ('Sewers Rat Path WN', 'Sewers Secret Room EN'),
    ('Sewers Yet More Rats S', 'Sewers Pull Switch N'),
    ('Eastern Lobby N', 'Eastern Lobby Bridge S'),
    ('Eastern Lobby NW', 'Eastern Lobby Left Ledge SW'),
    ('Eastern Lobby NE', 'Eastern Lobby Right Ledge SE'),
    ('Eastern East Wing EN', 'Eastern Pot Switch WN'),
    ('Eastern East Wing ES', 'Eastern Map Balcony WS'),
    ('Eastern Pot Switch SE', 'Eastern Map Room NE'),
    ('Eastern West Wing WS', 'Eastern Stalfos Spawn ES'),
    ('Eastern Stalfos Spawn NW', 'Eastern Compass Room SW'),
    ('Eastern Compass Room EN', 'Eastern Hint Tile WN'),
    ('Eastern Dark Square EN', 'Eastern Dark Pots WN'),
    ('Eastern Darkness NE', 'Eastern Rupees SE'),
    ('Eastern False Switches WS', 'Eastern Cannonball Hell ES'),
    ('Eastern Single Eyegore NE', 'Eastern Duo Eyegores SE'),
    ('Desert East Lobby WS', 'Desert East Wing ES'),
    ('Desert East Wing Key Door EN', 'Desert Compass Key Door WN'),
    ('Desert North Hall NW', 'Desert Map SW'),
    ('Desert North Hall NE', 'Desert Map SE'),
    ('Desert Arrow Pot Corner NW', 'Desert Trap Room SW'),
    ('Desert Sandworm Corner NE', 'Desert Bonk Torch SE'),
    ('Desert Sandworm Corner WS', 'Desert Circle of Pots ES'),
    ('Desert Circle of Pots NW', 'Desert Big Chest SW'),
    ('Desert West Wing WS', 'Desert West Lobby ES',),
    ('Desert Fairy Fountain SW', 'Desert West Lobby NW'),
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
    ('Swamp Waterfall Room NW', 'Swamp Refill SW'),
    ('Swamp Waterfall Room NE', 'Swamp Behind Waterfall SE'),
    ('Swamp C SE', 'Swamp Waterway NE'),
    ('Swamp Waterway N', 'Swamp I S'),
    ('Swamp Waterway NW', 'Swamp T SW'),
    ('Skull 1 Lobby ES', 'Skull Map Room WS'),
    ('Skull Pot Circle WN', 'Skull Pull Switch EN'),
    ('Skull Pull Switch S', 'Skull Big Chest N'),
    ('Skull Left Drop ES', 'Skull Compass Room WS'),
    ('Skull 2 East Lobby NW', 'Skull Big Key SW'),
    ('Skull Big Key WN', 'Skull Lone Pot EN'),
    ('Skull Small Hall WS', 'Skull 2 West Lobby ES'),
    ('Skull 2 West Lobby NW', 'Skull X Room SW'),
    ('Skull 3 Lobby WN', 'Skull East Bridge EN'),
    ('Skull East Bridge ES', 'Skull West Bridge Nook WS'),
    ('Skull Star Pits WS', 'Skull Torch Room ES'),
    ('Skull Torch Room EN', 'Skull Vines WN'),
    ('Skull Spike Corner ES', 'Skull Final Drop WS'),
    ('Thieves Hallway WS', 'Thieves Pot Alcove Mid ES'),
    ('Thieves Conveyor Maze SW', 'Thieves Pot Alcove Top NW'),
    ('Thieves Conveyor Maze EN', 'Thieves Hallway WN'),
    ('Thieves Spike Track NE', 'Thieves Triple Bypass SE'),
    ('Thieves Spike Track WS', 'Thieves Hellway Crystal ES'),
    ('Thieves Hellway Crystal EN', 'Thieves Triple Bypass WN'),
    ('Thieves Attic ES', 'Thieves Cricket Hall Left WS'),
    ('Thieves Cricket Hall Right ES', 'Thieves Attic Window WS'),
    ('Thieves Blocked Entry SW', 'Thieves Lonely Zazak NW'),
    ('Thieves Lonely Zazak ES', 'Thieves Blind\'s Cell WS'),
    ('Thieves Conveyor Bridge WS', 'Thieves Big Chest Room ES'),
    ('Thieves Conveyor Block WN', 'Thieves Trap EN'),
    ('Ice Lobby WS', 'Ice Jelly Key ES'),
    ('Ice Floor Switch ES', 'Ice Cross Left WS'),
    ('Ice Cross Top NE', 'Ice Bomb Drop SE'),
    ('Ice Pengator Switch ES', 'Ice Dead End WS'),
    ('Ice Stalfos Hint SE', 'Ice Conveyor NE'),
    ('Ice Bomb Jump EN', 'Ice Narrow Corridor WN'),
    ('Ice Spike Cross WS', 'Ice Firebar ES'),
    ('Ice Spike Cross NE', 'Ice Falling Square SE'),
    ('Ice Hammer Block ES', 'Ice Tongue Pull WS'),
    ('Ice Freezors Ledge ES', 'Ice Tall Hint WS'),
    ('Ice Hookshot Balcony SW', 'Ice Spikeball NW'),
    ('Ice Crystal Right NE', 'Ice Backwards Room SE'),
    ('Ice Crystal Left WS', 'Ice Big Chest View ES'),
    ('Ice Anti-Fairy SE', 'Ice Switch Room NE'),
    ('Mire Lone Shooter ES', 'Mire Falling Bridge WS'),  # technically one-way
    ('Mire Falling Bridge W', 'Mire Failure Bridge E'),  # technically one-way
    ('Mire Falling Bridge WN', 'Mire Map Spike Side EN'),  # technically one-way
    ('Mire Hidden Shooters WS', 'Mire Cross ES'),  # technically one-way
    ('Mire Hidden Shooters NE', 'Mire Minibridge SE'),
    ('Mire Spikes NW', 'Mire Ledgehop SW'),
    ('Mire Spike Barrier ES', 'Mire Square Rail WS'),
    ('Mire Square Rail NW', 'Mire Lone Warp SW'),
    ('Mire Wizzrobe Bypass WN', 'Mire Compass Room EN'),  # technically one-way
    ('Mire Conveyor Crystal WS', 'Mire Tile Room ES'),
    ('Mire Tile Room NW', 'Mire Compass Room SW'),
    ('Mire Neglected Room SE', 'Mire Chest View NE'),
    ('Mire BK Chest Ledge WS', 'Mire Warping Pool ES'),  # technically one-way
    ('Mire Torches Top SW', 'Mire Torches Bottom NW'),
    ('Mire Torches Bottom WS', 'Mire Attic Hint ES'),
    ('Mire Dark Shooters SE', 'Mire Key Rupees NE'),
    ('Mire Dark Shooters SW', 'Mire Block X NW'),
    ('Mire Tall Dark and Roomy WS', 'Mire Crystal Right ES'),
    ('Mire Tall Dark and Roomy WN', 'Mire Shooter Rupees EN'),
    ('Mire Crystal Mid NW', 'Mire Crystal Top SW'),
    ('TR Tile Room NE', 'TR Refill SE'),
    ('TR Pokey 1 NW', 'TR Chain Chomps SW'),
    ('TR Twin Pokeys EN', 'TR Dodgers WN'),
    ('TR Twin Pokeys SW', 'TR Hallway NW'),
    ('TR Hallway ES', 'TR Big View WS'),
    ('TR Big Chest NE', 'TR Dodgers SE'),
    ('TR Dash Room ES', 'TR Tongue Pull WS'),
    ('TR Dash Room NW', 'TR Crystaroller SW'),
    ('TR Tongue Pull NE', 'TR Rupees SE'),
    ('GT Torch EN', 'GT Hope Room WN'),
    ('GT Torch SW', 'GT Big Chest NW'),
    ('GT Tile Room EN', 'GT Speed Torch WN'),
    ('GT Speed Torch WS', 'GT Pots n Blocks ES'),
    ('GT Crystal Conveyor WN', 'GT Compass Room EN'),
    ('GT Conveyor Cross WN', 'GT Hookshot EN'),
    ('GT Hookshot ES', 'GT Map Room WS'),
    ('GT Double Switch EN', 'GT Spike Crystals WN'),
    ('GT Firesnake Room SW', 'GT Warp Maze (Rails) NW'),
    ('GT Ice Armos NE', 'GT Big Key Room SE'),
    ('GT Ice Armos WS', 'GT Four Torches ES'),
    ('GT Four Torches NW', 'GT Fairy Abyss SW'),
    ('GT Crystal Paths SW', 'GT Mimics 1 NW'),
    ('GT Mimics 1 ES', 'GT Mimics 2 WS'),
    ('GT Mimics 2 NE', 'GT Dash Hall SE'),
    ('GT Cannonball Bridge SE', 'GT Refill NE'),
    ('GT Gauntlet 1 WN', 'GT Gauntlet 2 EN'),
    ('GT Gauntlet 2 SW', 'GT Gauntlet 3 NW'),
    ('GT Gauntlet 4 SW', 'GT Gauntlet 5 NW'),
    ('GT Beam Dash WS', 'GT Lanmolas 2 ES'),
    ('GT Lanmolas 2 NW', 'GT Quad Pot SW'),
    ('GT Wizzrobes 1 SW', 'GT Dashing Bridge NW'),
    ('GT Dashing Bridge NE', 'GT Wizzrobes 2 SE'),
    ('GT Torch Cross ES', 'GT Staredown WS'),
    ('GT Falling Torches NE', 'GT Mini Helmasaur Room SE'),
    ('GT Mini Helmasaur Room WN', 'GT Bomb Conveyor EN'),
    ('GT Bomb Conveyor SW', 'GT Crystal Circles NW')
]

key_doors = [
    ('Sewers Key Rat Key Door N', 'Sewers Secret Room Key Door S'),
    ('Sewers Dark Cross Key Door N', 'Sewers Dark Cross Key Door S'),
    ('Eastern Dark Square Key Door WN', 'Eastern Cannonball Ledge Key Door EN'),
    ('Eastern Darkness Up Stairs', 'Eastern Attic Start Down Stairs'),
    ('Eastern Big Key NE', 'Eastern Hint Tile Blocked Path SE'),
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

default_small_key_doors = {
    'Hyrule Castle': [
        ('Sewers Key Rat Key Door N', 'Sewers Secret Room Key Door S'),
        ('Sewers Dark Cross Key Door N', 'Sewers Dark Cross Key Door S'),
        ('Hyrule Dungeon Map Room Key Door S', 'Hyrule Dungeon North Abyss Key Door N'),
        ('Hyrule Dungeon Armory Interior Key Door N', 'Hyrule Dungeon Armory Interior Key Door S')
    ],
    'Eastern Palace': [
        ('Eastern Dark Square Key Door WN', 'Eastern Cannonball Ledge Key Door EN'),
        'Eastern Darkness Up Stairs',
    ],
    'Desert Palace': [
        ('Desert East Wing Key Door EN', 'Desert Compass Key Door WN'),
        'Desert Tiles 1 Up Stairs',
        ('Desert Beamos Hall NE', 'Desert Tiles 2 SE'),
        ('Desert Tiles 2 NE', 'Desert Wall Slide SE'),
    ],
    'Tower of Hera': [
        'Hera Lobby Key Stairs'
    ],
    'Agahnims Tower': [
        'Tower Room 03 Up Stairs',
        ('Tower Dark Maze ES', 'Tower Dark Chargers WS'),
        'Tower Dark Archers Up Stairs',
        ('Tower Circle of Pots WS', 'Tower Pacifist Run ES'),
    ],
    'Palace of Darkness': [
        ('PoD Middle Cage N', 'PoD Pit Room S'),
        ('PoD Arena Main NW', 'PoD Falling Bridge SW'),
        ('PoD Falling Bridge WN', 'PoD Dark Maze EN'),
        'PoD Basement Ledge Up Stairs',
        ('PoD Compass Room SE', 'PoD Harmless Hellway NE'),
        ('PoD Dark Pegs WN', 'PoD Lonely Turtle EN')
    ],
    'Swamp Palace': [
        'Swamp Entrance Down Stairs',
        ('Swamp Pot Row WS', 'Swamp Trench 1 Approach ES'),
        ('Swamp Trench 1 Key Ledge NW', 'Swamp Hammer Switch SW'),
        ('Swamp Hub WN', 'Swamp Crystal Switch EN'),
        ('Swamp Hub North Ledge N', 'Swamp Push Statue S'),
        ('Swamp Waterway NW', 'Swamp T SW')
    ],
    'Skull Woods': [
        ('Skull 1 Lobby WS', 'Skull Pot Prison ES'),
        ('Skull Map Room SE', 'Skull Pinball NE'),
        ('Skull 2 West Lobby NW', 'Skull X Room SW'),
        ('Skull 3 Lobby NW', 'Skull Star Pits SW'),
        ('Skull Spike Corner ES', 'Skull Final Drop WS')
    ],
    'Thieves Town': [
        ('Thieves Hallway WS', 'Thieves Pot Alcove Mid ES'),
        'Thieves Spike Switch Up Stairs',
        ('Thieves Conveyor Bridge WS', 'Thieves Big Chest Room ES')
    ],
    'Ice Palace': [
        'Ice Jelly Key Down Stairs',
        ('Ice Conveyor SW', 'Ice Bomb Jump NW'),
        ('Ice Spike Cross ES', 'Ice Spike Room WS'),
        ('Ice Tall Hint SE', 'Ice Lonely Freezor NE'),
        'Ice Backwards Room Down Stairs',
        ('Ice Switch Room ES', 'Ice Refill WS')
    ],
    'Misery Mire': [
        ('Mire Hub WS', 'Mire Conveyor Crystal ES'),
        ('Mire Hub Right EN', 'Mire Map Spot WN'),
        ('Mire Spikes NW', 'Mire Ledgehop SW'),
        ('Mire Fishbone SE', 'Mire Spike Barrier NE'),
        ('Mire Conveyor Crystal WS', 'Mire Tile Room ES'),
        ('Mire Dark Shooters SE', 'Mire Key Rupees NE')
    ],
    'Turtle Rock': [
        ('TR Hub NW', 'TR Pokey 1 SW'),
        ('TR Pokey 1 NW', 'TR Chain Chomps SW'),
        'TR Chain Chomps Down Stairs',
        ('TR Pokey 2 ES', 'TR Lava Island WS'),
        'TR Crystaroller Down Stairs',
        ('TR Dash Bridge WS', 'TR Crystal Maze ES')
    ],
    'Ganons Tower': [
        ('GT Torch EN', 'GT Hope Room WN'),
        ('GT Tile Room EN', 'GT Speed Torch WN'),
        ('GT Hookshot ES', 'GT Map Room WS'),
        ('GT Double Switch EN', 'GT Spike Crystals WN'),
        ('GT Firesnake Room SW', 'GT Warp Maze (Rails) NW'),
        ('GT Conveyor Star Pits EN', 'GT Falling Bridge WN'),
        ('GT Mini Helmasaur Room WN', 'GT Bomb Conveyor EN'),
        ('GT Crystal Circles SW', 'GT Left Moldorm Ledge NW')
    ]
}

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
    ('Eastern Lobby Bridge N', 'Eastern Cannonball S'),
    ('Eastern Cannonball N', 'Eastern Courtyard Ledge S'),
    ('Eastern Cannonball Ledge WN', 'Eastern Big Key EN'),
    ('Eastern Cannonball Ledge Key Door EN', 'Eastern Dark Square Key Door WN'),
    ('Eastern Courtyard Ledge W', 'Eastern West Wing E'),
    ('Eastern Courtyard Ledge E', 'Eastern East Wing W'),
    ('Eastern Hint Tile EN', 'Eastern Courtyard WN'),
    ('Eastern Big Key NE', 'Eastern Hint Tile Blocked Path SE'),
    ('Eastern Courtyard EN', 'Eastern Map Valley WN'),
    ('Eastern Courtyard N', 'Eastern Darkness S'),
    ('Eastern Map Valley SW', 'Eastern Dark Square NW'),
    ('Eastern Attic Start WS', 'Eastern False Switches ES'),
    ('Eastern Cannonball Hell WS', 'Eastern Single Eyegore ES'),
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
    ('Skull 1 Lobby WS', 'Skull Pot Prison ES'),
    ('Skull Map Room SE', 'Skull Pinball NE'),
    ('Skull Pinball WS', 'Skull Compass Room ES'),
    ('Skull Compass Room NE', 'Skull Pot Prison SE'),
    ('Skull 2 East Lobby WS', 'Skull Small Hall ES'),
    ('Skull 3 Lobby NW', 'Skull Star Pits SW'),
    ('Skull Vines NW', 'Skull Spike Corner SW'),
    ('Thieves Lobby E', 'Thieves Compass Room W'),
    ('Thieves Ambush E', 'Thieves Rail Ledge W'),
    ('Thieves Rail Ledge NW', 'Thieves Pot Alcove Bottom SW'),
    ('Thieves BK Corner NE', 'Thieves Hallway SE'),
    ('Thieves Pot Alcove Mid WS', 'Thieves Spike Track ES'),
    ('Thieves Hellway NW', 'Thieves Spike Switch SW'),
    ('Thieves Triple Bypass EN', 'Thieves Conveyor Maze WN'),
    ('Thieves Basement Block WN', 'Thieves Conveyor Bridge EN'),
    ('Thieves Lonely Zazak WS', 'Thieves Conveyor Bridge ES'),
    ('Ice Cross Bottom SE', 'Ice Compass Room NE'),
    ('Ice Cross Right ES', 'Ice Pengator Switch WS'),
    ('Ice Conveyor SW', 'Ice Bomb Jump NW'),
    ('Ice Pengator Trap NE', 'Ice Spike Cross SE'),
    ('Ice Spike Cross ES', 'Ice Spike Room WS'),
    ('Ice Tall Hint SE', 'Ice Lonely Freezor NE'),
    ('Ice Tall Hint EN', 'Ice Hookshot Ledge WN'),
    ('Iced T EN', 'Ice Catwalk WN'),
    ('Ice Catwalk NW', 'Ice Many Pots SW'),
    ('Ice Many Pots WS', 'Ice Crystal Right ES'),
    ('Ice Switch Room ES', 'Ice Refill WS'),
    ('Ice Switch Room SE', 'Ice Antechamber NE'),
    ('Mire 2 NE', 'Mire Hub SE'),
    ('Mire Hub ES', 'Mire Lone Shooter WS'),
    ('Mire Hub E', 'Mire Failure Bridge W'),
    ('Mire Hub NE', 'Mire Hidden Shooters SE'),
    ('Mire Hub WN', 'Mire Wizzrobe Bypass EN'),
    ('Mire Hub WS', 'Mire Conveyor Crystal ES'),
    ('Mire Hub Right EN', 'Mire Map Spot WN'),
    ('Mire Hub Top NW', 'Mire Cross SW'),
    ('Mire Hidden Shooters ES', 'Mire Spikes WS'),
    ('Mire Minibridge NE', 'Mire Right Bridge SE'),
    ('Mire BK Door Room EN', 'Mire Ledgehop WN'),
    ('Mire BK Door Room N', 'Mire Left Bridge S'),
    ('Mire Spikes SW', 'Mire Crystal Dead End NW'),
    ('Mire Ledgehop NW', 'Mire Bent Bridge SW'),
    ('Mire Bent Bridge W', 'Mire Over Bridge E'),
    ('Mire Over Bridge W', 'Mire Fishbone E'),
    ('Mire Fishbone SE', 'Mire Spike Barrier NE'),
    ('Mire Spike Barrier SE', 'Mire Wizzrobe Bypass NE'),
    ('Mire Conveyor Crystal SE', 'Mire Neglected Room NE'),
    ('Mire Tile Room SW', 'Mire Conveyor Barrier NW'),
    ('Mire Block X WS', 'Mire Tall Dark and Roomy ES'),
    ('Mire Crystal Left WS', 'Mire Falling Foes ES'),
    ('TR Lobby Ledge NE', 'TR Hub SE'),
    ('TR Compass Room NW', 'TR Hub SW'),
    ('TR Hub ES', 'TR Torches Ledge WS'),
    ('TR Hub EN', 'TR Torches WN'),
    ('TR Hub NW', 'TR Pokey 1 SW'),
    ('TR Hub NE', 'TR Tile Room SE'),
    ('TR Torches NW', 'TR Roller Room SW'),
    ('TR Pipe Pit WN', 'TR Lava Dual Pipes EN'),
    ('TR Lava Island ES', 'TR Pipe Ledge WS'),
    ('TR Lava Dual Pipes WN', 'TR Pokey 2 EN'),
    ('TR Lava Dual Pipes SW', 'TR Twin Pokeys NW'),
    ('TR Pokey 2 ES', 'TR Lava Island WS'),
    ('TR Dodgers NE', 'TR Lava Escape SE'),
    ('TR Lava Escape NW', 'TR Dash Room SW'),
    ('TR Hallway WS', 'TR Lazy Eyes ES'),
    ('TR Dark Ride SW', 'TR Dash Bridge NW'),
    ('TR Dash Bridge SW', 'TR Eye Bridge NW'),
    ('TR Dash Bridge WS', 'TR Crystal Maze ES'),
    ('GT Torch WN', 'GT Conveyor Cross EN'),
    ('GT Hope Room EN', 'GT Tile Room WN'),
    ('GT Big Chest SW', 'GT Invisible Catwalk NW'),
    ('GT Bob\'s Room SE', 'GT Invisible Catwalk NE'),
    ('GT Speed Torch NE', 'GT Trap Room SE'),
    ('GT Speed Torch SE', 'GT Crystal Conveyor NE'),
    ('GT Warp Maze (Pits) ES', 'GT Invisible Catwalk WS'),
    ('GT Hookshot NW', 'GT DMs Room SW'),
    ('GT Hookshot SW', 'GT Double Switch NW'),
    ('GT Warp Maze (Rails) WS', 'GT Randomizer Room ES'),
    ('GT Conveyor Star Pits EN', 'GT Falling Bridge WN'),
    ('GT Falling Bridge WS', 'GT Hidden Star ES'),
    ('GT Dash Hall NE', 'GT Hidden Spikes SE'),
    ('GT Hidden Spikes EN', 'GT Cannonball Bridge WN'),
    ('GT Gauntlet 3 SW', 'GT Gauntlet 4 NW'),
    ('GT Gauntlet 5 WS', 'GT Beam Dash ES'),
    ('GT Wizzrobes 2 NE', 'GT Conveyor Bridge SE'),
    ('GT Conveyor Bridge EN', 'GT Torch Cross WN'),
    ('GT Crystal Circles SW', 'GT Left Moldorm Ledge NW')
]

default_one_way_connections = [
    ('Sewers Pull Switch S', 'Sanctuary N'),
    ('Eastern Duo Eyegores NE', 'Eastern Boss SE'),
    ('Desert Wall Slide NW', 'Desert Boss SW'),
    ('Tower Altar NW', 'Tower Agahnim 1 SW'),
    ('PoD Harmless Hellway SE', 'PoD Arena Main NE'),
    ('PoD Dark Alley NE', 'PoD Boss SE'),
    ('Swamp T NW', 'Swamp Boss SW'),
    ('Thieves Hallway NE', 'Thieves Boss SE'),
    ('Mire Antechamber NW', 'Mire Boss SW'),
    ('TR Final Abyss NW', 'TR Boss SW'),
    ('GT Invisible Bridges WS', 'GT Invisible Catwalk ES'),
    ('GT Validation WS', 'GT Frozen Over ES'),
    ('GT Brightly Lit Hall NW', 'GT Agahnim 2 SW')
]

# For crossed
default_dungeon_sets = [
    ['Hyrule Castle Lobby', 'Hyrule Castle West Lobby', 'Hyrule Castle East Lobby', 'Sewers Rat Path', 'Sanctuary',
     'Hyrule Dungeon Cellblock'],
    ['Eastern Lobby', 'Eastern Boss'],
    ['Desert Back Lobby', 'Desert Boss', 'Desert Main Lobby', 'Desert West Lobby', 'Desert East Lobby'],
    ['Hera Lobby', 'Hera Boss'],
    ['Tower Lobby', 'Tower Agahnim 1'],
    ['PoD Lobby', 'PoD Boss'],
    ['Swamp Lobby', 'Swamp Boss'],
    ['Skull 1 Lobby', 'Skull Pinball', 'Skull Left Drop', 'Skull Pot Circle', 'Skull 2 East Lobby',
     'Skull 2 West Lobby', 'Skull Back Drop', 'Skull 3 Lobby', 'Skull Boss'],
    ['Thieves Lobby', 'Thieves Attic Window', 'Thieves Blind\'s Cell', 'Thieves Boss'],
    ['Ice Lobby', 'Ice Boss'],
    ['Mire Lobby', 'Mire Boss'],
    ['TR Main Lobby', 'TR Boss', 'TR Eye Bridge', 'TR Big Chest Entrance', 'TR Lazy Eyes'],
    ['GT Lobby', 'GT Agahnim 2']
]

dungeon_x_idx_to_name = {
    0: 'Hyrule Castle',
    1: 'Eastern Palace',
    2: 'Desert Palace',
    3: 'Tower of Hera',
    4: 'Agahnims Tower',
    5: 'Palace of Darkness',
    6: 'Swamp Palace',
    7: 'Skull Woods',
    8: 'Thieves Town',
    9: 'Ice Palace',
    10: 'Misery Mire',
    11: 'Turtle Rock',
    12: 'Ganons Tower'
}
