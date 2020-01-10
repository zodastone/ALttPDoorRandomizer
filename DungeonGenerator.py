import random
import collections
from collections import defaultdict
from enum import Enum, unique
import logging
from functools import reduce
import operator as op
from typing import List

from BaseClasses import DoorType, Direction, CrystalBarrier, RegionType, Polarity, flooded_keys
from Regions import key_only_locations, dungeon_events, flooded_keys_reverse
from Dungeons import dungeon_regions


@unique
class Hook(Enum):
    North = 0
    West = 1
    South = 2
    East = 3
    Stairs = 4


class GraphPiece:

    def __init__(self):
        self.hanger_info = None
        self.hanger_crystal = None
        self.hooks = {}
        self.visited_regions = set()
        self.possible_bk_locations = set()


def generate_dungeon(name, available_sectors, entrance_region_names, split_dungeon, world, player):
    logger = logging.getLogger('')
    entrance_regions = convert_regions(entrance_region_names, world, player)
    doors_to_connect = set()
    all_regions = set()
    bk_needed = False
    bk_special = False
    for sector in available_sectors:
        for door in sector.outstanding_doors:
            doors_to_connect.add(door)
        all_regions.update(sector.regions)
        bk_needed = bk_needed or determine_if_bk_needed(sector, split_dungeon, world, player)
        bk_special = bk_special or check_for_special(sector)
    proposed_map = {}
    choices_master = [[]]
    depth = 0
    dungeon_cache = {}
    backtrack = False
    itr = 0
    finished = False
    # last_choice = None
    while not finished:
        # what are my choices?
        itr += 1
        if itr > 5000:
            raise Exception('Generation taking too long. Ref %s' % name)
        if depth not in dungeon_cache.keys():
            dungeon, hangers, hooks = gen_dungeon_info(name, available_sectors, entrance_regions, proposed_map,
                                                       doors_to_connect, bk_needed, bk_special, world, player)
            dungeon_cache[depth] = dungeon, hangers, hooks
            valid = check_valid(dungeon, hangers, hooks, proposed_map, doors_to_connect, all_regions, bk_needed)
        else:
            dungeon, hangers, hooks = dungeon_cache[depth]
            valid = True
        if valid:
            if len(proposed_map) == len(doors_to_connect):
                finished = True
                continue
            prev_choices = choices_master[depth]
            # make a choice
            hanger, hook = make_a_choice(dungeon, hangers, hooks, prev_choices)
            if hanger is None:
                backtrack = True
            else:
                logger.debug(' ' * depth + "%d: Linking %s to %s", depth, hanger.name, hook.name)
                proposed_map[hanger] = hook
                proposed_map[hook] = hanger
                last_choice = (hanger, hook)
                choices_master[depth].append(last_choice)
                depth += 1
                choices_master.append([])
        else:
            backtrack = True
        if backtrack:
            backtrack = False
            choices_master.pop()
            dungeon_cache.pop(depth, None)
            depth -= 1
            if depth < 0:
                raise Exception('Invalid dungeon. Ref %s' % name)
            a, b = choices_master[depth][-1]
            logger.debug(' ' * depth + "%d: Rescinding %s, %s", depth, a.name, b.name)
            proposed_map.pop(a, None)
            proposed_map.pop(b, None)
    queue = collections.deque(proposed_map.items())
    while len(queue) > 0:
        a, b = queue.pop()
        connect_doors(a, b, world, player)
        queue.remove((b, a))
    master_sector = available_sectors.pop()
    for sub_sector in available_sectors:
        master_sector.regions.extend(sub_sector.regions)
    master_sector.outstanding_doors.clear()
    master_sector.r_name_set = None
    return master_sector


def determine_if_bk_needed(sector, split_dungeon, world, player):
    if not split_dungeon:
        for region in sector.regions:
            for ext in region.exits:
                door = world.check_for_door(ext.name, player)
                if door is not None and door.bigKey:
                    return True
    return False


def check_for_special(sector):
    return 'Hyrule Dungeon Cellblock' in sector.region_set()


def gen_dungeon_info(name, available_sectors, entrance_regions, proposed_map, valid_doors, bk_needed, bk_special, world, player):
    # step 1 create dungeon: Dict<DoorName|Origin, GraphPiece>
    dungeon = {}
    start = ExplorationState(dungeon=name)
    start.big_key_special = bk_special
    original_state = extend_reachable_state_improved(entrance_regions, start, proposed_map,
                                                     valid_doors, bk_needed, world, player)
    dungeon['Origin'] = create_graph_piece_from_state(None, original_state, original_state, proposed_map)
    hanger_set = set()
    o_state_cache = {}
    for sector in available_sectors:
        for door in sector.outstanding_doors:
            if not door.stonewall and door not in proposed_map.keys():
                hanger_set.add(door)
                parent = parent_region(door, world, player).parent_region
                init_state = ExplorationState(dungeon=name)
                init_state.big_key_special = start.big_key_special
                o_state = extend_reachable_state_improved([parent], init_state, proposed_map,
                                                          valid_doors, False, world, player)
                o_state_cache[door.name] = o_state
                piece = create_graph_piece_from_state(door, o_state, o_state, proposed_map)
                dungeon[door.name] = piece
    check_blue_states(hanger_set, dungeon, o_state_cache, proposed_map, valid_doors, world, player)

    # catalog hooks: Dict<Hook, List<Door, Crystal, Door>>
    # and hangers: Dict<Hang, List<Door>>
    avail_hooks = defaultdict(list)
    hangers = defaultdict(list)
    for key, piece in dungeon.items():
        door_hang = piece.hanger_info
        if door_hang is not None:
            hanger = hanger_from_door(door_hang)
            hangers[hanger].append(door_hang)
        for door, crystal in piece.hooks.items():
            hook = hook_from_door(door)
            avail_hooks[hook].append((door, crystal, door_hang))

    # thin out invalid hanger
    winnow_hangers(hangers, avail_hooks)
    return dungeon, hangers, avail_hooks


def check_blue_states(hanger_set, dungeon, o_state_cache, proposed_map, valid_doors, world, player):
    not_blue = set()
    not_blue.update(hanger_set)
    doors_to_check = set()
    doors_to_check.update(hanger_set)  # doors to check, check everything on first pass
    blue_hooks = []
    blue_hangers = []
    new_blues = True
    while new_blues:
        new_blues = False
        for door in doors_to_check:
            piece = dungeon[door.name]
            for hook, crystal in piece.hooks.items():
                if crystal == CrystalBarrier.Blue or crystal == CrystalBarrier.Either:
                    h_type = hook_from_door(hook)
                    if h_type not in blue_hooks:
                        new_blues = True
                        blue_hooks.append(h_type)
            if piece.hanger_crystal == CrystalBarrier.Either:
                h_type = hanger_from_door(piece.hanger_info)
                if h_type not in blue_hangers:
                    new_blues = True
                    blue_hangers.append(h_type)
        doors_to_check = set()
        for door in not_blue:  # am I now blue?
            hang_type = hanger_from_door(door)  # am I hangable on a hook?
            hook_type = hook_from_door(door)  # am I hookable onto a hanger?
            if (hang_type in blue_hooks and not door.stonewall) or hook_type in blue_hangers:
                explore_blue_state(door, dungeon, o_state_cache[door.name], proposed_map, valid_doors, world, player)
                doors_to_check.add(door)
        not_blue.difference_update(doors_to_check)


def explore_blue_state(door, dungeon, o_state, proposed_map, valid_doors, world, player):
    parent = parent_region(door, world, player).parent_region
    blue_start = ExplorationState(CrystalBarrier.Blue, o_state.dungeon)
    blue_start.big_key_special = o_state.big_key_special
    b_state = extend_reachable_state_improved([parent], blue_start, proposed_map, valid_doors, False, world, player)
    dungeon[door.name] = create_graph_piece_from_state(door, o_state, b_state, proposed_map)


def make_a_choice(dungeon, hangers, avail_hooks, prev_choices):
    # choose a hanger
    all_hooks = {}
    origin = dungeon['Origin']
    for key in avail_hooks.keys():
        for hstuff in avail_hooks[key]:
            all_hooks[hstuff[0]] = None
    candidate_hangers = []
    for key in hangers.keys():
        candidate_hangers.extend(hangers[key])
    candidate_hangers.sort(key=lambda x: x.name)  # sorting to create predictable seeds
    random.shuffle(candidate_hangers)  # randomize if equal preference
    stage_2_hangers = []
    if len(prev_choices) > 0:
        prev_hanger = prev_choices[0][0]
        if prev_hanger in candidate_hangers:
            stage_2_hangers.append(prev_hanger)
            candidate_hangers.remove(prev_hanger)
    hookable_hangers = collections.deque()
    queue = collections.deque(candidate_hangers)
    while len(queue) > 0:
        c_hang = queue.pop()
        if c_hang in all_hooks.keys():
            hookable_hangers.append(c_hang)
        else:
            stage_2_hangers.append(c_hang)  # prefer hangers that are not hooks
    # todo : prefer hangers with fewer hooks at some point? not sure about this
    # this prefer hangers of the fewest type - to catch problems fast
    hookable_hangers = sorted(hookable_hangers, key=lambda door: len(hangers[hanger_from_door(door)]), reverse=True)
    origin_hangers = []
    while len(hookable_hangers) > 0:
        c_hang = hookable_hangers.pop()
        if c_hang in origin.hooks.keys():
            origin_hangers.append(c_hang)
        else:
            stage_2_hangers.append(c_hang)  # prefer hangers that are not hooks on the 'origin'
    stage_2_hangers.extend(origin_hangers)

    hook = None
    next_hanger = None
    while hook is None:
        if len(stage_2_hangers) == 0:
            return None, None
        next_hanger = stage_2_hangers.pop(0)
        next_hanger_type = hanger_from_door(next_hanger)
        hook_candidates = []
        for door, crystal, orig_hang in avail_hooks[next_hanger_type]:
            if filter_choices(next_hanger, door, orig_hang, prev_choices, hook_candidates):
                hook_candidates.append(door)
        if len(hook_candidates) > 0:
            hook_candidates.sort(key=lambda x: x.name)  # sort for deterministic seeds
            hook = random.choice(tuple(hook_candidates))
        else:
            return None, None

    return next_hanger, hook


def filter_choices(next_hanger, door, orig_hang, prev_choices, hook_candidates):
    if (next_hanger, door) in prev_choices or (door, next_hanger) in prev_choices:
        return False
    return next_hanger != door and orig_hang != next_hanger and door not in hook_candidates


def check_valid(dungeon, hangers, hooks, proposed_map, doors_to_connect, all_regions, bk_needed):
    # evaluate if everything is still plausible

    # only origin is left in the dungeon and not everything is connected
    if len(dungeon.keys()) <= 1 and len(proposed_map.keys()) < len(doors_to_connect):
        return False
    # origin has no more hooks, but not all doors have been proposed
    possible_bks = len(dungeon['Origin'].possible_bk_locations)
    true_origin_hooks = [x for x in dungeon['Origin'].hooks.keys() if not x.bigKey or possible_bks > 0 or not bk_needed]
    if len(true_origin_hooks) == 0 and len(proposed_map.keys()) < len(doors_to_connect):
        return False
    if len(true_origin_hooks) == 0 and bk_needed and possible_bks == 0 and len(proposed_map.keys()) == len(
         doors_to_connect):
        return False
    for key in hangers.keys():
        if len(hooks[key]) > 0 and len(hangers[key]) == 0:
            return False
    # todo: stonewall - check that there's no hook-only that is without a matching hanger
    must_hang = defaultdict(list)
    all_hooks = set()
    for key in hooks.keys():
        for hook in hooks[key]:
            all_hooks.add(hook[0])
    for key in hangers.keys():
        for hanger in hangers[key]:
            if hanger not in all_hooks:
                must_hang[key].append(hanger)
    for key in must_hang.keys():
        if len(must_hang[key]) > len(hooks[key]):
            return False
    outstanding_doors = defaultdict(list)
    for d in doors_to_connect:
        if d not in proposed_map.keys():
            outstanding_doors[hook_from_door(d)].append(d)
    for key in outstanding_doors.keys():
        opp_key = opposite_h_type(key)
        if len(outstanding_doors[key]) > 0 and len(hangers[key]) == 0 and len(hooks[opp_key]) == 0:
            return False
    all_visited = set()
    bk_possible = not bk_needed
    for piece in dungeon.values():
        all_visited.update(piece.visited_regions)
        if not bk_possible and len(piece.possible_bk_locations) > 0:
            bk_possible = True
    if len(all_regions.difference(all_visited)) > 0:
        return False
    if not bk_possible:
        return False
    new_hangers_found = True
    accessible_hook_types = []
    hanger_matching = set()
    all_hangers = set()
    origin_hooks = set(dungeon['Origin'].hooks.keys())
    for door_hook in origin_hooks:
        h_type = hook_from_door(door_hook)
        if h_type not in accessible_hook_types:
            accessible_hook_types.append(h_type)
    while new_hangers_found:
        new_hangers_found = False
        for hanger_set in hangers.values():
            for hanger in hanger_set:
                all_hangers.add(hanger)
                h_type = hanger_from_door(hanger)
                if (h_type in accessible_hook_types or hanger in origin_hooks) and hanger not in hanger_matching:
                    new_hangers_found = True
                    hanger_matching.add(hanger)
                    matching_hooks = dungeon[hanger.name].hooks.keys()
                    origin_hooks.update(matching_hooks)
                    for door_hook in matching_hooks:
                        new_h_type = hook_from_door(door_hook)
                        if new_h_type not in accessible_hook_types:
                            accessible_hook_types.append(new_h_type)
    return len(all_hangers.difference(hanger_matching)) == 0


def winnow_hangers(hangers, hooks):
    removal_info = []
    for hanger, door_set in hangers.items():
        for door in door_set:
            hook_set = hooks[hanger]
            if len(hook_set) == 0:
                removal_info.append((hanger, door))
            else:
                found_valid = False
                for door_hook, crystal, orig_hanger in hook_set:
                    if orig_hanger != door:
                        found_valid = True
                        break
                if not found_valid:
                    removal_info.append((hanger, door))
    for hanger, door in removal_info:
        hangers[hanger].remove(door)


def create_graph_piece_from_state(door, o_state, b_state, proposed_map):
    # todo: info about dungeon events - not sure about that
    graph_piece = GraphPiece()
    all_unattached = {}
    for exp_d in o_state.unattached_doors:
        all_unattached[exp_d.door] = exp_d.crystal
    for exp_d in b_state.unattached_doors:
        d = exp_d.door
        if d in all_unattached.keys():
            if all_unattached[d] != exp_d.crystal:
                if all_unattached[d] == CrystalBarrier.Orange and exp_d.crystal == CrystalBarrier.Blue:
                    all_unattached[d] = CrystalBarrier.Null
                elif all_unattached[d] == CrystalBarrier.Blue and exp_d.crystal == CrystalBarrier.Orange:
                    # the swapping case
                    logging.getLogger('').warning('Mismatched state @ %s (o:%s b:%s)', d.name, all_unattached[d],
                                                  exp_d.crystal)
                elif all_unattached[d] == CrystalBarrier.Either:
                    all_unattached[d] = exp_d.crystal  # pessimism, and if not this, leave it alone
        else:
            all_unattached[exp_d.door] = exp_d.crystal
    h_crystal = door.crystal if door is not None else None
    for d, crystal in all_unattached.items():
        if (door is None or d != door) and not d.blocked and d not in proposed_map.keys():
            graph_piece.hooks[d] = crystal
        if d == door:
            h_crystal = crystal
    graph_piece.hanger_info = door
    graph_piece.hanger_crystal = h_crystal
    graph_piece.visited_regions.update(o_state.visited_blue)
    graph_piece.visited_regions.update(o_state.visited_orange)
    graph_piece.visited_regions.update(b_state.visited_blue)
    graph_piece.visited_regions.update(b_state.visited_orange)
    graph_piece.possible_bk_locations.update(filter_for_potential_bk_locations(o_state.bk_found))
    graph_piece.possible_bk_locations.update(filter_for_potential_bk_locations(b_state.bk_found))
    return graph_piece


def filter_for_potential_bk_locations(locations):
    return [x for x in locations if
            '- Big Chest' not in x.name and '- Prize' not in x.name and x.name not in dungeon_events
            and x.name not in key_only_locations.keys() and x.name not in ['Agahnim 1', 'Agahnim 2']]


def parent_region(door, world, player):
    return world.get_entrance(door.name, player)


def opposite_h_type(h_type):
    type_map = {
        Hook.Stairs: Hook.Stairs,
        Hook.North: Hook.South,
        Hook.South: Hook.North,
        Hook.West: Hook.East,
        Hook.East: Hook.West,

    }
    return type_map[h_type]


def hook_from_door(door):
    if door.type == DoorType.SpiralStairs:
        return Hook.Stairs
    if door.type == DoorType.Normal:
        dir = {
            Direction.North: Hook.North,
            Direction.South: Hook.South,
            Direction.West: Hook.West,
            Direction.East: Hook.East,
        }
        return dir[door.direction]
    return None


def hanger_from_door(door):
    if door.type == DoorType.SpiralStairs:
        return Hook.Stairs
    if door.type == DoorType.Normal:
        dir = {
            Direction.North: Hook.South,
            Direction.South: Hook.North,
            Direction.West: Hook.East,
            Direction.East: Hook.West,
        }
        return dir[door.direction]
    return None


def connect_doors(a, b, world, player):
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
        dep_doors, target = [], None
        if len(a.dependents) > 0:
            dep_doors, target = a.dependents, b
        elif len(b.dependents) > 0:
            dep_doors, target = b.dependents, a
        if target is not None:
            target_region = world.get_entrance(target.name, player).parent_region
            for dep in dep_doors:
                connect_simple_door(dep, target_region, world, player)
        return
    # If we failed to account for a type, panic
    raise RuntimeError('Unknown door type ' + a.type.name)


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


def connect_simple_door(exit_door, region, world, player):
    world.get_entrance(exit_door.name, player).connect(region)
    exit_door.dest = region


class ExplorationState(object):

    def __init__(self, init_crystal=CrystalBarrier.Orange, dungeon=None):

        self.unattached_doors = []
        self.avail_doors = []
        self.event_doors = []

        self.visited_orange = []
        self.visited_blue = []
        self.events = set()
        self.crystal = init_crystal

        # key region stuff
        self.door_krs = {}

        # key validation stuff
        self.small_doors = []
        self.big_doors = []
        self.opened_doors = []
        self.big_key_opened = False
        self.big_key_special = False

        self.found_locations = []
        self.ttl_locations = 0
        self.used_locations = 0
        self.key_locations = 0
        self.used_smalls = 0
        self.bk_found = set()

        self.non_door_entrances = []
        self.dungeon = dungeon

    def copy(self):
        ret = ExplorationState(dungeon=self.dungeon)
        ret.unattached_doors = list(self.unattached_doors)
        ret.avail_doors = list(self.avail_doors)
        ret.event_doors = list(self.event_doors)
        ret.visited_orange = list(self.visited_orange)
        ret.visited_blue = list(self.visited_blue)
        ret.events = set(self.events)
        ret.crystal = self.crystal
        ret.door_krs = self.door_krs.copy()

        ret.small_doors = list(self.small_doors)
        ret.big_doors = list(self.big_doors)
        ret.opened_doors = list(self.opened_doors)
        ret.big_key_opened = self.big_key_opened
        ret.big_key_special = self.big_key_special
        ret.ttl_locations = self.ttl_locations
        ret.key_locations = self.key_locations
        ret.used_locations = self.used_locations
        ret.used_smalls = self.used_smalls
        ret.found_locations = list(self.found_locations)
        ret.bk_found = set(self.bk_found)

        ret.non_door_entrances = list(self.non_door_entrances)
        return ret

    def next_avail_door(self):
        self.avail_doors.sort(key=lambda x: 0 if x.flag else 1 if x.door.bigKey else 2)
        exp_door = self.avail_doors.pop()
        self.crystal = exp_door.crystal
        return exp_door

    def visit_region(self, region, key_region=None, key_checks=False, bk_Flag=False):
        if self.crystal == CrystalBarrier.Either:
            if region not in self.visited_blue:
                self.visited_blue.append(region)
            if region not in self.visited_orange:
                self.visited_orange.append(region)
        elif self.crystal == CrystalBarrier.Orange:
            self.visited_orange.append(region)
        elif self.crystal == CrystalBarrier.Blue:
            self.visited_blue.append(region)
        if region.type == RegionType.Dungeon:
            for location in region.locations:
                if key_checks and location not in self.found_locations:
                    if location.name in key_only_locations and 'Small Key' in location.item.name:
                        self.key_locations += 1
                    if location.name not in dungeon_events and '- Prize' not in location.name and location.name not in ['Agahnim 1', 'Agahnim 2']:
                        self.ttl_locations += 1
                if location not in self.found_locations:
                    self.found_locations.append(location)
                    if not bk_Flag:
                        self.bk_found.add(location)
                if location.name in dungeon_events and location.name not in self.events:
                    if self.flooded_key_check(location):
                        self.perform_event(location.name, key_region)
                if location.name in flooded_keys_reverse.keys() and self.location_found(
                     flooded_keys_reverse[location.name]):
                    self.perform_event(flooded_keys_reverse[location.name], key_region)
        if key_checks and region.name == 'Hyrule Dungeon Cellblock' and not self.big_key_opened:
            self.big_key_opened = True
            self.avail_doors.extend(self.big_doors)
            self.big_doors.clear()

    def flooded_key_check(self, location):
        if location.name not in flooded_keys.keys():
            return True
        return flooded_keys[location.name] in [x.name for x in self.found_locations]

    def location_found(self, location_name):
        for l in self.found_locations:
            if l.name == location_name:
                return True
        return False

    def perform_event(self, location_name, key_region):
        self.events.add(location_name)
        queue = collections.deque(self.event_doors)
        while len(queue) > 0:
            exp_door = queue.pop()
            if exp_door.door.req_event == location_name:
                self.avail_doors.append(exp_door)
                self.event_doors.remove(exp_door)
                if key_region is not None:
                    d_name = exp_door.door.name
                    if d_name not in self.door_krs.keys():
                        self.door_krs[d_name] = key_region

    def add_all_entrance_doors_check_unattached(self, region, world, player):
        door_list = [x for x in get_doors(world, region, player) if x.type in [DoorType.Normal, DoorType.SpiralStairs]]
        door_list.extend(get_entrance_doors(world, region, player))
        for door in door_list:
            if self.can_traverse(door):
                if door.dest is None and not self.in_door_list_ic(door, self.unattached_doors):
                    self.append_door_to_list(door, self.unattached_doors)
                elif door.req_event is not None and door.req_event not in self.events and not self.in_door_list(door,
                                                                                                                self.event_doors):
                    self.append_door_to_list(door, self.event_doors)
                elif not self.in_door_list(door, self.avail_doors):
                    self.append_door_to_list(door, self.avail_doors)
        for entrance in region.entrances:
            door = world.check_for_door(entrance.name, player)
            if door is None:
                self.non_door_entrances.append(entrance)

    def add_all_doors_check_unattached(self, region, world, player):
        for door in get_doors(world, region, player):
            if self.can_traverse(door):
                if door.dest is None and not self.in_door_list_ic(door, self.unattached_doors):
                    self.append_door_to_list(door, self.unattached_doors)
                elif door.req_event is not None and door.req_event not in self.events and not self.in_door_list(door,
                                                                                                                self.event_doors):
                    self.append_door_to_list(door, self.event_doors)
                elif not self.in_door_list(door, self.avail_doors):
                    self.append_door_to_list(door, self.avail_doors)

    def add_all_doors_check_proposed(self, region, proposed_map, valid_doors, flag, world, player):
        for door in get_doors(world, region, player):
            if self.can_traverse(door):
                if door.controller is not None:
                    door = door.controller
                if door.dest is None and door not in proposed_map.keys() and door in valid_doors:
                    if not self.in_door_list_ic(door, self.unattached_doors):
                        self.append_door_to_list(door, self.unattached_doors, flag)
                    else:
                        other = self.find_door_in_list(door, self.unattached_doors)
                        if self.crystal != other.crystal:
                            other.crystal = CrystalBarrier.Either
                elif door.req_event is not None and door.req_event not in self.events and not self.in_door_list(door,
                                                                                                                self.event_doors):
                    self.append_door_to_list(door, self.event_doors, flag)
                elif not self.in_door_list(door, self.avail_doors):
                    self.append_door_to_list(door, self.avail_doors, flag)

    def add_all_doors_check_key_region(self, region, key_region, world, player):
        for door in get_doors(world, region, player):
            if self.can_traverse(door):
                if door.req_event is not None and door.req_event not in self.events and not self.in_door_list(door,
                                                                                                              self.event_doors):
                    self.append_door_to_list(door, self.event_doors)
                elif not self.in_door_list(door, self.avail_doors):
                    self.append_door_to_list(door, self.avail_doors)
                    if door.name not in self.door_krs.keys():
                        self.door_krs[door.name] = key_region
            else:
                if door.name not in self.door_krs.keys():
                    self.door_krs[door.name] = key_region

    def add_all_doors_check_keys(self, region, key_door_proposal, world, player):
        for door in get_doors(world, region, player):
            if self.can_traverse(door):
                if door in key_door_proposal and door not in self.opened_doors:
                    if not self.in_door_list(door, self.small_doors):
                        self.append_door_to_list(door, self.small_doors)
                elif door.bigKey and not self.big_key_opened:
                    if not self.in_door_list(door, self.big_doors):
                        self.append_door_to_list(door, self.big_doors)
                elif door.req_event is not None and door.req_event not in self.events:
                    if not self.in_door_list(door, self.event_doors):
                        self.append_door_to_list(door, self.event_doors)
                elif not self.in_door_list(door, self.avail_doors):
                    self.append_door_to_list(door, self.avail_doors)

    def visited(self, region):
        if self.crystal == CrystalBarrier.Either:
            return region in self.visited_blue and region in self.visited_orange
        elif self.crystal == CrystalBarrier.Orange:
            return region in self.visited_orange
        elif self.crystal == CrystalBarrier.Blue:
            return region in self.visited_blue
        return False

    def visited_at_all(self, region):
        return region in self.visited_blue or region in self.visited_orange

    def can_traverse(self, door):
        if door.blocked:
            return False
        if door.crystal not in [CrystalBarrier.Null, CrystalBarrier.Either]:
            return self.crystal == CrystalBarrier.Either or door.crystal == self.crystal
        return True

    def can_traverse_bk_check(self, door, isOrigin):
        if door.blocked:
            return False
        if door.crystal not in [CrystalBarrier.Null, CrystalBarrier.Either]:
            return self.crystal == CrystalBarrier.Either or door.crystal == self.crystal
        return not isOrigin or not door.bigKey or self.count_locations_exclude_specials() > 0
        # return not door.bigKey or len([x for x in self.found_locations if '- Prize' not in x.name]) > 0

    def count_locations_exclude_specials(self):
        cnt = 0
        for loc in self.found_locations:
            if '- Big Chest' not in loc.name and '- Prize' not in loc.name and loc.name not in dungeon_events and loc.name not in key_only_locations.keys():
                cnt += 1
        return cnt

    def validate(self, door, region, world, player):
        return self.can_traverse(door) and not self.visited(region) and valid_region_to_explore(region, self.dungeon,
                                                                                                world, player)

    def in_door_list(self, door, door_list):
        for d in door_list:
            if d.door == door and d.crystal == self.crystal:
                return True
        return False

    @staticmethod
    def in_door_list_ic(door, door_list):
        for d in door_list:
            if d.door == door:
                return True
        return False

    @staticmethod
    def find_door_in_list(door, door_list):
        for d in door_list:
            if d.door == door:
                return d
        return None

    def append_door_to_list(self, door, door_list, flag=False):
        if door.crystal == CrystalBarrier.Null:
            door_list.append(ExplorableDoor(door, self.crystal, flag))
        else:
            door_list.append(ExplorableDoor(door, door.crystal, flag))

    def key_door_sort(self, d):
        if d.door.smallKey:
            if d.door in self.opened_doors:
                return 1
            else:
                return 0
        return 2


class ExplorableDoor(object):

    def __init__(self, door, crystal, flag):
        self.door = door
        self.crystal = crystal
        self.flag = flag

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s (%s)' % (self.door.name, self.crystal.name)


# todo: delete this
def extend_reachable_state(search_regions, state, world, player):
    local_state = state.copy()
    for region in search_regions:
        local_state.visit_region(region)
        local_state.add_all_doors_check_unattached(region, world, player)
    while len(local_state.avail_doors) > 0:
        explorable_door = local_state.next_avail_door()
        connect_region = world.get_entrance(explorable_door.door.name, player).connected_region
        if connect_region is not None:
            if valid_region_to_explore(connect_region, local_state.dungeon, world, player) and not local_state.visited(
                 connect_region):
                local_state.visit_region(connect_region)
                local_state.add_all_doors_check_unattached(connect_region, world, player)
    return local_state


def extend_reachable_state_improved(search_regions, state, proposed_map, valid_doors, isOrigin, world, player):
    local_state = state.copy()
    for region in search_regions:
        local_state.visit_region(region)
        local_state.add_all_doors_check_proposed(region, proposed_map, valid_doors, False, world, player)
    while len(local_state.avail_doors) > 0:
        explorable_door = local_state.next_avail_door()
        if explorable_door.door.bigKey:
            if isOrigin:
                big_not_found = not special_big_key_found(local_state, world, player) if local_state.big_key_special else local_state.count_locations_exclude_specials() == 0
                if big_not_found:
                    continue  # we can't open this door
        if explorable_door.door in proposed_map:
            connect_region = world.get_entrance(proposed_map[explorable_door.door].name, player).parent_region
        else:
            connect_region = world.get_entrance(explorable_door.door.name, player).connected_region
        if connect_region is not None:
            if valid_region_to_explore(connect_region, local_state.dungeon, world, player) and not local_state.visited(
                 connect_region):
                flag = explorable_door.flag or explorable_door.door.bigKey
                local_state.visit_region(connect_region, bk_Flag=flag)
                local_state.add_all_doors_check_proposed(connect_region, proposed_map, valid_doors, flag, world, player)
    return local_state


def special_big_key_found(state, world, player):
    cellblock = world.get_region('Hyrule Dungeon Cellblock', player)
    return state.visited(cellblock)


# cross-utility methods
def valid_region_to_explore(region, name, world, player):
    if region is None:
        return False
    return (region.type == RegionType.Dungeon and region.dungeon.name == name) or region.name in world.inaccessible_regions[player]


def get_doors(world, region, player):
    res = []
    for exit in region.exits:
        door = world.check_for_door(exit.name, player)
        if door is not None:
            res.append(door)
    return res


def get_dungeon_doors(region, world, player):
    res = []
    for ext in region.exits:
        door = world.check_for_door(ext.name, player)
        if door is not None and ext.parent_region.type == RegionType.Dungeon:
            res.append(door)
    return res


def get_entrance_doors(world, region, player):
    res = []
    for exit in region.entrances:
        door = world.check_for_door(exit.name, player)
        if door is not None:
            res.append(door)
    return res


def convert_regions(region_names, world, player):
    region_list = []
    for name in region_names:
        region_list.append(world.get_region(name, player))
    return region_list


# Begin crossed mode sector shuffle

class DungeonBuilder(object):

    def __init__(self, name):
        self.name = name
        self.sectors = []
        self.location_cnt = 0
        self.key_drop_cnt = 0
        self.bk_required = False
        self.bk_provided = False
        self.c_switch_required = False
        self.c_switch_present = False
        self.dead_ends = 0
        self.branches = 0
        self.mag_needed = [False, False, False]
        self.unfulfilled = defaultdict(int)
        self.all_entrances = None  # used for sector segration/branching
        self.entrance_list = None  # used for overworld accessibility
        self.layout_starts = None  # used for overworld accessibility
        self.master_sector = None
        self.path_entrances = None  # used for pathing/key doors, I think

        self.candidates = None
        self.key_doors_num = None
        self.combo_size = None
        self.flex = 0

    def polarity_complement(self):
        pol = Polarity()
        for sector in self.sectors:
            pol += sector.polarity()
        return pol.complement()

    def polarity(self):
        pol = Polarity()
        for sector in self.sectors:
            pol += sector.polarity()
        return pol


def simple_dungeon_builder(name, sector_list, world, player):
    define_sector_features(sector_list, world, player)
    builder = DungeonBuilder(name)
    dummy_pool = dict.fromkeys(sector_list)
    for sector in sector_list:
        assign_sector(sector, builder, dummy_pool)
    return builder


def create_dungeon_builders(all_sectors, world, player, dungeon_entrances=None):
    logger = logging.getLogger('')
    logger.info('Shuffling Dungeon Sectors')
    if dungeon_entrances is None:
        dungeon_entrances = default_dungeon_entrances
    define_sector_features(all_sectors, world, player)
    candidate_sectors = dict.fromkeys(all_sectors)

    dungeon_map = {}
    for key in dungeon_regions.keys():
        dungeon_map[key] = DungeonBuilder(key)
    for key in dungeon_boss_sectors.keys():
        current_dungeon = dungeon_map[key]
        for r_name in dungeon_boss_sectors[key]:
            assign_sector(find_sector(r_name, candidate_sectors), current_dungeon, candidate_sectors)
        if key == 'Hyrule Castle' and world.mode == 'standard':
            for r_name in ['Hyrule Dungeon Cellblock', 'Sanctuary']:  # need to deliver zelda
                assign_sector(find_sector(r_name, candidate_sectors), current_dungeon, candidate_sectors)
    for key in dungeon_entrances.keys():
        current_dungeon = dungeon_map[key]
        current_dungeon.all_entrances = dungeon_entrances[key]
        for r_name in current_dungeon.all_entrances:
            assign_sector(find_sector(r_name, candidate_sectors), current_dungeon, candidate_sectors)
    # categorize sectors
    free_location_sectors = {}
    crystal_switches = {}
    crystal_barriers = {}
    polarized_sectors = {}
    neutral_sectors = {}
    for sector in candidate_sectors:
        if sector.chest_locations > 0:
            free_location_sectors[sector] = None
        elif sector.c_switch:
            crystal_switches[sector] = None
        elif sector.blue_barrier:
            crystal_barriers[sector] = None
        elif sector.polarity().is_neutral():
            neutral_sectors[sector] = None
        else:
            polarized_sectors[sector] = None
    logger.info('-Assigning Chest Locations')
    assign_location_sectors(dungeon_map, free_location_sectors)
    logger.info('-Assigning Crystal Switches and Barriers')
    leftover = assign_crystal_switch_sectors(dungeon_map, crystal_switches)
    for sector in leftover:
        if sector.polarity().is_neutral():
            neutral_sectors[sector] = None
        else:
            polarized_sectors[sector] = None
    # blue barriers
    assign_crystal_barrier_sectors(dungeon_map, crystal_barriers)
    # polarity:
    logger.info('-Balancing Doors')
    assign_polarized_sectors(dungeon_map, polarized_sectors, logger)
    # the rest
    assign_the_rest(dungeon_map, neutral_sectors)
    return dungeon_map


def define_sector_features(sectors, world, player):
    for sector in sectors:
        if 'Hyrule Dungeon Cellblock' in sector.region_set():
            sector.bk_provided = True
        if 'Thieves Blind\'s Cell' in sector.region_set():
            sector.bk_required = True
        for region in sector.regions:
            for loc in region.locations:
                if '- Prize' in loc.name or loc.name in ['Agahnim 1', 'Agahnim 2', 'Hyrule Castle - Big Key Drop']:
                    pass
                elif loc.event and 'Small Key' in loc.item.name:
                    sector.key_only_locations += 1
                elif loc.name not in dungeon_events:
                    sector.chest_locations += 1
                    if '- Big Chest' in loc.name:
                        sector.bk_required = True
            for ext in region.exits:
                door = world.check_for_door(ext.name, player)
                if door is not None:
                    if door.crystal == CrystalBarrier.Either:
                        sector.c_switch = True
                    elif door.crystal == CrystalBarrier.Orange:
                        sector.orange_barrier = True
                    elif door.crystal == CrystalBarrier.Blue:
                        sector.blue_barrier = True
                    if door.bigKey:
                        sector.bk_required = True


def assign_sector(sector, dungeon, candidate_sectors):
    if sector is not None:
        del candidate_sectors[sector]
        dungeon.sectors.append(sector)
        dungeon.location_cnt += sector.chest_locations
        dungeon.key_drop_cnt += sector.key_only_locations
        if sector.c_switch:
            dungeon.c_switch_present = True
        if sector.blue_barrier:
            dungeon.c_switch_required = True
        if sector.bk_required:
            dungeon.bk_required = True
        if sector.bk_provided:
            dungeon.bk_provided = True
        if sector.outflow() == 1:
            dungeon.dead_ends += 1
        if sector.outflow() > 2:
            dungeon.branches += sector.outflow() - 2


def find_sector(r_name, sectors):
    for s in sectors:
        if r_name in s.region_set():
            return s
    return None


def assign_location_sectors(dungeon_map, free_location_sectors):
    valid = False
    choices = None
    sector_list = list(free_location_sectors)
    random.shuffle(sector_list)
    while not valid:
        choices, d_idx, totals = weighted_random_locations(dungeon_map, sector_list)
        for i, sector in enumerate(sector_list):
            choice = d_idx[choices[i].name]
            totals[choice] += sector.chest_locations
        valid = True
        for d_name, idx in d_idx.items():
            if totals[idx] < minimal_locations(d_name):
                valid = False
                break
    for i, choice in enumerate(choices):
        builder = dungeon_map[choice.name]
        assign_sector(sector_list[i], builder, free_location_sectors)


def weighted_random_locations(dungeon_map, free_location_sectors):
    population = []
    ttl_assigned = 0
    weights = []
    totals = []
    d_idx = {}
    for i, dungeon_builder in enumerate(dungeon_map.values()):
        population.append(dungeon_builder)
        totals.append(dungeon_builder.location_cnt)
        ttl_assigned += dungeon_builder.location_cnt
        weights.append(6.375)
        d_idx[dungeon_builder.name] = i
    average = ttl_assigned / 13
    for i, db in enumerate(population):
        if db.location_cnt < average:
            weights[i] += average - db.location_cnt
        if db.location_cnt > average:
            weights[i] = max(0, weights[i] - db.location_cnt + average)

    choices = random.choices(population, weights, k=len(free_location_sectors))
    return choices, d_idx, totals


def minimal_locations(dungeon_name):
    # bump to 5 if maps do something useful for all these dungeons
    if dungeon_name == 'Hyrule Castle':
        return 4  # bk + compass + 2 others
    if dungeon_name == 'Agahnims Tower':
        return 4
    if dungeon_name == 'Ganons Tower':
        return 4
    # reduce gt to 4 once compasses work
    return 5


def assign_crystal_switch_sectors(dungeon_map, crystal_switches, assign_one=False):
    population = []
    some_c_switches_present = False
    for name, builder in dungeon_map.items():
        if builder.c_switch_required and not builder.c_switch_present:
            population.append(name)
        if builder.c_switch_present:
            some_c_switches_present = True
    if len(population) == 0:  # nothing needs a switch
        if assign_one and not some_c_switches_present:  # something should have one
            choice = random.choice(list(dungeon_map.keys()))
            builder = dungeon_map[choice]
            assign_sector(random.choice(list(crystal_switches)), builder, crystal_switches)
        return crystal_switches
    sector_list = list(crystal_switches)
    choices = random.sample(sector_list, k=len(population))
    for i, choice in enumerate(choices):
        builder = dungeon_map[population[i]]
        assign_sector(choice, builder, crystal_switches)
    return crystal_switches


def assign_crystal_barrier_sectors(dungeon_map, crystal_barriers):
    population = []
    for name, builder in dungeon_map.items():
        if builder.c_switch_present:
            population.append(name)
    sector_list = list(crystal_barriers)
    random.shuffle(sector_list)
    choices = random.choices(population, k=len(sector_list))
    for i, choice in enumerate(choices):
        builder = dungeon_map[choice]
        assign_sector(sector_list[i], builder, crystal_barriers)


def identify_polarity_issues(dungeon_map):
    unconnected_builders = {}
    for name, builder in dungeon_map.items():
        if len(builder.sectors) == 1:
            continue
        if len(builder.sectors) == 2:
            def sector_filter(x, y):
                return x != y
        else:
            def sector_filter(x, y):
                return x != y and x.outflow() > 1
        for sector in builder.sectors:
            others = [x for x in builder.sectors if sector_filter(x, sector)]
            other_mag = sum_magnitude(others)
            sector_mag = sector.magnitude()
            for i in range(len(sector_mag)):
                if sector_mag[i] > 0 and other_mag[i] == 0:
                    builder.mag_needed[i] = True
                    if name not in unconnected_builders.keys():
                        unconnected_builders[name] = builder
    return unconnected_builders


def identify_branching_issues(dungeon_map):
    unconnected_builders = {}
    for name, builder in dungeon_map.items():
        unsatisfied_doors = defaultdict(list)
        satisfying_doors = defaultdict(list)
        entrance_doors = defaultdict(list)
        multi_purpose = defaultdict(list)
        for sector in builder.sectors:
            is_entrance = is_entrance_sector(builder, sector)
            if is_entrance:
                for door in sector.outstanding_doors:
                    dependent_doors = [x for x in sector.outstanding_doors if x != door]
                    if not door.blocked:
                        entrance_doors[hook_from_door(door)].append((door, dependent_doors))
                    else:
                        unsatisfied_doors[hook_from_door(door)].append((door, dependent_doors))
            else:
                outflow = sector.outflow()
                outflow -= len([x for x in sector.outstanding_doors if x.dead])
                other_doors = []
                one_way_flag = False
                for door in sector.outstanding_doors:
                    dependent_doors = [x for x in sector.outstanding_doors if x != door]
                    if door.blocked or door.dead or (outflow <= 1 and len(dependent_doors) == 0):
                        unsatisfied_doors[hook_from_door(door)].append((door, dependent_doors))
                        one_way_flag = True
                    else:
                        other_doors.append((door, dependent_doors))
                if not one_way_flag and outflow >= 2:
                    for door, deps in other_doors:
                        multi_purpose[hook_from_door(door)].append((door, deps))
                elif one_way_flag or outflow <= 1:
                    for door, deps in other_doors:
                        satisfying_doors[hook_from_door(door)].append((door, deps))
        used_doors = set()
        satisfied = is_satisfied([unsatisfied_doors, entrance_doors, satisfying_doors, multi_purpose])
        while not satisfied:
            candidate_is_unsated = True
            candidate, dep_list = choose_candidate([unsatisfied_doors])
            if candidate is None:
                candidate_is_unsated = False
                candidate, dep_list = choose_candidate([multi_purpose, satisfying_doors, entrance_doors])  # consider satifying doors here?
            match_list = [satisfying_doors, multi_purpose, entrance_doors]
            match_maker, match_deps = find_candidate_match(candidate, dep_list, candidate_is_unsated, match_list)
            if match_maker is None:
                unconnected_builders[name] = builder
                builder.unfulfilled[hook_from_door(candidate)] += 1
                for hook, door_list in unsatisfied_doors.items():
                    builder.unfulfilled[hook] += len(door_list)
                satisfied = True
                continue
            used_doors.add(candidate)
            used_doors.add(match_maker)
            if candidate_is_unsated and len(match_deps) == 1:
                for door in match_deps:
                    door_list = multi_purpose[hook_from_door(door)]
                    pair = find_door_in_list(door, door_list)
                    if pair[0] is not None:
                        door_list.remove(pair)
                        unsatisfied_doors[hook_from_door(door)].append((pair))
            satisfied = is_satisfied([unsatisfied_doors, entrance_doors, satisfying_doors, multi_purpose])
    return unconnected_builders


def is_entrance_sector(builder, sector):
    for entrance in builder.all_entrances:
        r_set = sector.region_set()
        if entrance in r_set:
            return True
    return False


def is_satisfied(door_dict_list):
    for door_dict in door_dict_list:
        for door_list in door_dict.values():
            if len(door_list) > 0:
                return False
    return True


def choose_candidate(door_dict_list):
    for door_dict in door_dict_list:
        min_len = None
        candidate_list = None
        for dir, door_list in door_dict.items():
            curr_len = len(door_list)
            if curr_len > 0 and (min_len is None or curr_len < min_len):
                candidate_list = door_list
                min_len = curr_len
        if min_len is not None:
            candidate, dep_list = candidate_list.pop()
            return candidate, dep_list
    return None, None


def find_candidate_match(candidate, dep_list, check_deps, door_dict_list):
    dir = hanger_from_door(candidate)
    backup_pair = None
    backup_list = None
    for door_dict in door_dict_list:
        door_list = door_dict[dir]
        pair = None
        for match, match_deps in door_list:
            if not check_deps or match not in dep_list:
                pair = match, match_deps
                break
            elif len(filter_match_deps(candidate, match_deps)) > 0:
                backup_pair = match, match_deps
                backup_list = door_list
        if pair is not None:
            door_list.remove(pair)
            return pair
    if backup_pair is not None:
        backup_list.remove(backup_pair)
        logging.getLogger('').debug('Matching %s to %s unsure if safe', candidate, backup_pair[0])
        return backup_pair
    return None, None


def find_door_in_list(door, door_list):
    for d, deps in door_list:
        if d == door:
            return d, deps
    return None, None


# todo: maybe filter by used doors too
# todo: I want the number of door that match is accessible by still
def filter_match_deps(candidate, match_deps):
    return [x for x in match_deps if x != candidate]


def sum_magnitude(sector_list):
    result = [0, 0, 0]
    for sector in sector_list:
        vector = sector.magnitude()
        for i in range(len(result)):
            result[i] = result[i] + vector[i]
    return result


def sum_polarity(sector_list):
    pol = Polarity()
    for sector in sector_list:
        pol += sector.polarity()
    return pol


def assign_polarized_sectors(dungeon_map, polarized_sectors, logger):
    # step 1: fix polarity connection issues
    logger.info('--Basic Traversal')
    unconnected_builders = identify_polarity_issues(dungeon_map)
    while len(unconnected_builders) > 0:
        for name, builder in unconnected_builders.items():
            candidates = find_connection_candidates(builder.mag_needed, polarized_sectors)
            if len(candidates) == 0:
                raise Exception('Cross Dungeon Builder: Cannot find a candidate for connectedness - restart?')
            sector = random.choice(candidates)
            assign_sector(sector, builder, polarized_sectors)
            builder.mag_needed = [False, False, False]
        unconnected_builders = identify_polarity_issues(dungeon_map)

    # step 2: fix neutrality issues
    builder_order = list(dungeon_map.values())
    random.shuffle(builder_order)
    for builder in builder_order:
        logger.info('--Balancing %s', builder.name)
        while not builder.polarity().is_neutral():
            candidates = find_neutralizing_candidates(builder.polarity(), polarized_sectors)
            sectors = random.choice(candidates)
            for sector in sectors:
                assign_sector(sector, builder, polarized_sectors)

    # step 3: fix dead ends
    problem_builders = identify_branching_issues(dungeon_map)
    neutral_choices: List[List] = neutralize_the_rest(polarized_sectors)
    while len(problem_builders) > 0:
        for name, builder in problem_builders.items():
            candidates = find_branching_candidates(builder, neutral_choices)
            choice = random.choice(candidates)
            if valid_polarized_assignment(builder, choice):
                neutral_choices.remove(choice)
                for sector in choice:
                    assign_sector(sector, builder, polarized_sectors)
            builder.unfulfilled.clear()
        problem_builders = identify_branching_issues(dungeon_map)

    # step 4: assign randomly until gone - must maintain connectedness, neutral polarity
    while len(polarized_sectors) > 0:
        choices = random.choices(list(dungeon_map.keys()), k=len(neutral_choices))
        for i, choice in enumerate(choices):
            builder = dungeon_map[choice]
            if valid_polarized_assignment(builder, neutral_choices[i]):
                for sector in neutral_choices[i]:
                    assign_sector(sector, builder, polarized_sectors)


def find_connection_candidates(mag_needed, sector_pool):
    candidates = []
    for sector in sector_pool:
        if sector.outflow() < 2:
            continue
        mag = sector.magnitude()
        matches = False
        for i, need in enumerate(mag_needed):
            if need and mag[i] > 0:
                matches = True
                break
        if matches:
            candidates.append(sector)
    return candidates


def find_neutralizing_candidates(polarity, sector_pool):
    candidates = defaultdict(list)
    original_charge = polarity.charge()
    best_charge = original_charge
    main_pool = list(sector_pool)
    last_r = 0
    while len(candidates) == 0:
        r_range = range(last_r + 1, last_r + 3)
        for r in r_range:
            if r > len(main_pool):
                if len(candidates) == 0:
                    raise Exception('Cross Dungeon Builder: No possible neutralizers left')
                else:
                    continue
            last_r = r
            combinations = ncr(len(main_pool), r)
            for i in range(0, combinations):
                choice = kth_combination(i, main_pool, r)
                p_charge = (polarity + sum_polarity(choice)).charge()
                if p_charge < original_charge and p_charge <= best_charge:
                    candidates[p_charge].append(choice)
                    if p_charge < best_charge:
                        best_charge = p_charge
    candidate_list = candidates[best_charge]
    best_len = 10
    official_cand = []
    for cand in candidate_list:
        size = len(cand)
        if size < best_len:
            best_len = size
            official_cand = [cand]
        elif size == best_len:
            official_cand.append(cand)
    return official_cand


def find_branching_candidates(builder, neutral_choices):
    candidates = []
    for choice in neutral_choices:
        door_match = False
        flow_match = False
        for sector in choice:
            if sector.adj_outflow() >= 2:
                flow_match = True
            for door in sector.outstanding_doors:
                if builder.unfulfilled[hanger_from_door(door)] > 0:
                    door_match = True
        if door_match and flow_match:
            candidates.append(choice)
    if len(candidates) == 0:
        raise Exception('Cross Dungeon Builder: No more branching candidates!')
    return candidates


def neutralize_the_rest(sector_pool):
    neutral_choices = []
    main_pool = list(sector_pool)
    failed_pool = []
    r_size = 1
    while len(main_pool) > 0 or len(failed_pool) > 0:
        if len(main_pool) <= r_size:
            main_pool.extend(failed_pool)
            failed_pool.clear()
            r_size += 1
        candidate = random.choice(main_pool)
        main_pool.remove(candidate)
        if r_size > len(main_pool):
            raise Exception("Cross Dungeon Builder: no more neutral pairings possible")
        combinations = ncr(len(main_pool), r_size)
        itr = 0
        done = False
        while not done:
            ttl_polarity = candidate.polarity()
            choice_set = kth_combination(itr, main_pool, r_size)
            for choice in choice_set:
                ttl_polarity += choice.polarity()
            if ttl_polarity.is_neutral():
                choice_set.append(candidate)
                neutral_choices.append(choice_set)
                main_pool = [x for x in main_pool if x not in choice_set]
                failed_pool = [x for x in failed_pool if x not in choice_set]
                done = True
            else:
                itr += 1
            if itr >= combinations:
                failed_pool.append(candidate)
                done = True
    return neutral_choices


def valid_polarized_assignment(builder, sector_list):
    full_list = sector_list + builder.sectors
    for sector in full_list:
        others = [x for x in full_list if x != sector]
        other_mag = sum_magnitude(others)
        sector_mag = sector.magnitude()
        hookable = False
        for i in range(len(sector_mag)):
            if sector_mag[i] > 0 and other_mag[i] > 0:
                hookable = True
        if not hookable:
            return False
    # dead_ends = 0
    # branches = 0
    # for sector in sector_list:
    #     if sector.outflow == 1:
    #         dead_ends += 1
    #     if sector.outflow() > 2:
    #         branches += sector.outflow() - 2
    # if builder.dead_ends + dead_ends > builder.branches + branches:
    #     return False
    return (sum_polarity(sector_list) + sum_polarity(builder.sectors)).is_neutral()


def assign_the_rest(dungeon_map, neutral_sectors):
    while len(neutral_sectors) > 0:
        sector_list = list(neutral_sectors)
        choices = random.choices(list(dungeon_map.keys()), k=len(sector_list))
        for i, choice in enumerate(choices):
            builder = dungeon_map[choice]
            if valid_polarized_assignment(builder, [sector_list[i]]):
                assign_sector(sector_list[i], builder, neutral_sectors)


def split_dungeon_builder(builder, split_list):
    logger = logging.getLogger('')
    logger.info('Splitting Up Desert/Skull')
    candidate_sectors = dict.fromkeys(builder.sectors)

    dungeon_map = {}
    for name, split_entrances in split_list.items():
        key = builder.name + ' ' + name
        dungeon_map[key] = sub_builder = DungeonBuilder(key)
        sub_builder.all_entrances = split_entrances
        for r_name in split_entrances:
            assign_sector(find_sector(r_name, candidate_sectors), sub_builder, candidate_sectors)

    # categorize sectors
    crystal_switches = {}
    crystal_barriers = {}
    polarized_sectors = {}
    neutral_sectors = {}
    for sector in candidate_sectors:
        if sector.c_switch:
            crystal_switches[sector] = None
        elif sector.blue_barrier:
            crystal_barriers[sector] = None
        elif sector.polarity().is_neutral():
            neutral_sectors[sector] = None
        else:
            polarized_sectors[sector] = None
    leftover = assign_crystal_switch_sectors(dungeon_map, crystal_switches, len(crystal_barriers) > 0)
    for sector in leftover:
        if sector.polarity().is_neutral():
            neutral_sectors[sector] = None
        else:
            polarized_sectors[sector] = None
    # blue barriers
    assign_crystal_barrier_sectors(dungeon_map, crystal_barriers)
    # polarity:
    logger.info('-Re-balancing Desert/Skull')
    assign_polarized_sectors(dungeon_map, polarized_sectors, logger)
    # the rest
    assign_the_rest(dungeon_map, neutral_sectors)
    return dungeon_map


# common functions - todo: move to a common place
def kth_combination(k, l, r):
    if r == 0:
        return []
    elif len(l) == r:
        return l
    else:
        i = ncr(len(l) - 1, r - 1)
        if k < i:
            return l[0:1] + kth_combination(k, l[1:], r - 1)
        else:
            return kth_combination(k - i, l[1:], r)


def ncr(n, r):
    if r == 0:
        return 1
    r = min(r, n - r)
    numerator = reduce(op.mul, range(n, n - r, -1), 1)
    denominator = reduce(op.mul, range(1, r + 1), 1)
    return int(numerator / denominator)


dungeon_boss_sectors = {
    'Hyrule Castle': [],
    'Eastern Palace': ['Eastern Boss'],
    'Desert Palace': ['Desert Boss'],
    'Tower of Hera': ['Hera Boss'],
    'Agahnims Tower': ['Tower Agahnim 1'],
    'Palace of Darkness': ['PoD Boss'],
    'Swamp Palace': ['Swamp Boss'],
    'Skull Woods': ['Skull Boss'],
    'Thieves Town': ['Thieves Blind\'s Cell', 'Thieves Boss'],
    'Ice Palace': ['Ice Boss'],
    'Misery Mire': ['Mire Boss'],
    'Turtle Rock': ['TR Boss'],
    'Ganons Tower': ['GT Agahnim 2']
}

default_dungeon_entrances = {
    'Hyrule Castle': ['Hyrule Castle Lobby', 'Hyrule Castle West Lobby', 'Hyrule Castle East Lobby', 'Sewers Rat Path',
                      'Sanctuary'],
    'Eastern Palace': ['Eastern Lobby'],
    'Desert Palace': ['Desert Back Lobby', 'Desert Main Lobby', 'Desert West Lobby', 'Desert East Lobby'],
    'Tower of Hera': ['Hera Lobby'],
    'Agahnims Tower': ['Tower Lobby'],
    'Palace of Darkness': ['PoD Lobby'],
    'Swamp Palace': ['Swamp Lobby'],
    'Skull Woods': ['Skull 1 Lobby', 'Skull Pinball', 'Skull Left Drop', 'Skull Pot Circle', 'Skull 2 East Lobby',
                    'Skull 2 West Lobby', 'Skull Back Drop', 'Skull 3 Lobby'],
    'Thieves Town': ['Thieves Lobby'],
    'Ice Palace': ['Ice Lobby'],
    'Misery Mire': ['Mire Lobby'],
    'Turtle Rock': ['TR Main Lobby', 'TR Eye Bridge', 'TR Big Chest Entrance', 'TR Lazy Eyes'],
    'Ganons Tower': ['GT Lobby']
}
