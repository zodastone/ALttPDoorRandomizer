import random
import collections
from collections import defaultdict
from enum import Enum, unique
import logging

from BaseClasses import DoorType, Direction, CrystalBarrier, RegionType, flooded_keys
from Regions import key_only_locations, dungeon_events, flooded_keys_reverse


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
    for sector in available_sectors:
        for door in sector.outstanding_doors:
            doors_to_connect.add(door)
        all_regions.update(sector.regions)
        bk_needed = bk_needed or determine_if_bk_needed(sector, split_dungeon, world, player)
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
            raise Exception('Generation taking too long. Ref %s' % entrance_region_names[0])
        if depth not in dungeon_cache.keys():
            dungeon, hangers, hooks = gen_dungeon_info(name, available_sectors, entrance_regions, proposed_map, doors_to_connect, bk_needed, world, player)
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
                logger.debug(' '*depth+"%d: Linking %s to %s", depth, hanger.name, hook.name)
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
                raise Exception('Invalid dungeon. Ref %s' % entrance_region_names[0])
            a, b = choices_master[depth][-1]
            logger.debug(' '*depth+"%d: Rescinding %s, %s", depth, a.name, b.name)
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
    return master_sector


def determine_if_bk_needed(sector, split_dungeon, world, player):
    if not split_dungeon:
        for region in sector.regions:
            for ext in region.exits:
                door = world.check_for_door(ext.name, player)
                if door is not None and door.bigKey:
                    return True
    return False


def gen_dungeon_info(name, available_sectors, entrance_regions, proposed_map, valid_doors, bk_needed, world, player):
    # step 1 create dungeon: Dict<DoorName|Origin, GraphPiece>
    dungeon = {}
    original_state = extend_reachable_state_improved(entrance_regions, ExplorationState(dungeon=name), proposed_map, valid_doors, bk_needed, world, player)
    dungeon['Origin'] = create_graph_piece_from_state(None, original_state, original_state, proposed_map)
    doors_to_connect = set()
    hanger_set = set()
    o_state_cache = {}
    for sector in available_sectors:
        for door in sector.outstanding_doors:
            doors_to_connect.add(door)
            if not door.stonewall and door not in proposed_map.keys():
                hanger_set.add(door)
                parent = parent_region(door, world, player).parent_region
                o_state = extend_reachable_state_improved([parent], ExplorationState(dungeon=name), proposed_map, valid_doors, False, world, player)
                o_state_cache[door.name] = o_state
                piece = create_graph_piece_from_state(door, o_state, o_state, proposed_map)
                dungeon[door.name] = piece
    check_blue_states(hanger_set, dungeon, o_state_cache, proposed_map, valid_doors, world, player)

    # catalog hooks: Dict<Hook, Set<Door, Crystal, Door>>
    # and hangers: Dict<Hang, Set<Door>>
    avail_hooks = defaultdict(set)
    hangers = defaultdict(set)
    for key, piece in dungeon.items():
        door_hang = piece.hanger_info
        if door_hang is not None:
            hanger = hanger_from_door(door_hang)
            hangers[hanger].add(door_hang)
        for door, crystal in piece.hooks.items():
            hook = hook_from_door(door)
            avail_hooks[hook].add((door, crystal, door_hang))

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
    b_state = extend_reachable_state_improved([parent], blue_start, proposed_map, valid_doors, False, world, player)
    dungeon[door.name] = create_graph_piece_from_state(door, o_state, b_state, proposed_map)


def make_a_choice(dungeon, hangers, avail_hooks, prev_choices):
    # choose a hanger
    all_hooks = set()
    origin = dungeon['Origin']
    for key in avail_hooks.keys():
        for hstuff in avail_hooks[key]:
            all_hooks.add(hstuff[0])
    candidate_hangers = []
    for key in hangers.keys():
        candidate_hangers.extend(hangers[key])
    candidate_hangers.sort(key=lambda x: x.name)  # sorting to create predictable seeds
    random.shuffle(candidate_hangers)  # randomize if equal preference
    stage_2_hangers = []
    hookable_hangers = collections.deque()
    queue = collections.deque(candidate_hangers)
    while len(queue) > 0:
        c_hang = queue.pop()
        if c_hang in all_hooks:
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
    if len(true_origin_hooks) == 0 and bk_needed and possible_bks == 0 and len(proposed_map.keys()) == len(doors_to_connect):
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
                    logging.getLogger('').warning('Mismatched state @ %s (o:%s b:%s)', d.name, all_unattached[d], exp_d.crystal)
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
    return [x for x in locations if '- Big Chest' not in x.name and '- Prize' not in x.name and x.name not in dungeon_events and x.name not in key_only_locations.keys() and x.name not in ['Agahnim 1', 'Agahnim 2']]


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
                    if location.name in key_only_locations:
                        self.key_locations += 1
                    if location.name not in dungeon_events and '- Prize' not in location.name:
                        self.ttl_locations += 1
                if location not in self.found_locations:
                    self.found_locations.append(location)
                    if not bk_Flag:
                        self.bk_found.add(location)
                if location.name in dungeon_events and location.name not in self.events:
                    if self.flooded_key_check(location):
                        self.perform_event(location.name, key_region)
                if location.name in flooded_keys_reverse.keys() and self.location_found(flooded_keys_reverse[location.name]):
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
                elif door.req_event is not None and door.req_event not in self.events and not self.in_door_list(door, self.event_doors):
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
                elif door.req_event is not None and door.req_event not in self.events and not self.in_door_list(door, self.event_doors):
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
                elif door.req_event is not None and door.req_event not in self.events and not self.in_door_list(door, self.event_doors):
                    self.append_door_to_list(door, self.event_doors, flag)
                elif not self.in_door_list(door, self.avail_doors):
                    self.append_door_to_list(door, self.avail_doors, flag)

    def add_all_doors_check_key_region(self, region, key_region, world, player):
        for door in get_doors(world, region, player):
            if self.can_traverse(door):
                if door.req_event is not None and door.req_event not in self.events and not self.in_door_list(door, self.event_doors):
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
        return self.can_traverse(door) and not self.visited(region) and valid_region_to_explore(region, self.dungeon, world, player)

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
            if valid_region_to_explore(connect_region, local_state.dungeon, world, player) and not local_state.visited(connect_region):
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
            if isOrigin and local_state.count_locations_exclude_specials() == 0:
                continue  # we can't open this door
        if explorable_door.door in proposed_map:
            connect_region = world.get_entrance(proposed_map[explorable_door.door].name, player).parent_region
        else:
            connect_region = world.get_entrance(explorable_door.door.name, player).connected_region
        if connect_region is not None:
            if valid_region_to_explore(connect_region, local_state.dungeon, world, player) and not local_state.visited(connect_region):
                flag = explorable_door.flag or explorable_door.door.bigKey
                local_state.visit_region(connect_region, bk_Flag=flag)
                local_state.add_all_doors_check_proposed(connect_region, proposed_map, valid_doors, flag, world, player)
    return local_state


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
