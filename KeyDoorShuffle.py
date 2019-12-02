import collections

from Regions import dungeon_events
from Dungeons import dungeon_keys, dungeon_bigs
from DungeonGenerator import ExplorationState


class KeySphere(object):

    def __init__(self):
        self.access_door = None
        self.free_locations = set()
        self.prize_region = False
        self.key_only_locations = set()
        self.child_doors = set()
        self.bk_locked = False
        self.parent_sphere = None
        self.other_locations = set()


class KeyLayout(object):

    def __init__(self, sector, starts, proposal):
        self.sector = sector
        self.start_regions = starts
        self.proposal = proposal
        self.key_logic = KeyLogic(sector.name)
        self.checked_states = {}

        self.key_spheres = None
        self.flat_prop = None
        self.max_chests = None
        self.all_chest_locations = set()

        # bk special?
        # bk required? True if big chests or big doors exists

    def reset(self, proposal):
        self.proposal = proposal
        self.key_logic = KeyLogic(self.sector.name)
        self.checked_states = {}


class KeyLogic(object):

    def __init__(self, dungeon_name):
        self.door_rules = {}
        self.bk_restricted = set()
        self.sm_restricted = set()
        self.small_key_name = dungeon_keys[dungeon_name]
        self.bk_name = dungeon_bigs[dungeon_name]
        self.logic_min = {}
        self.logic_max = {}


class DoorRules(object):

    def __init__(self, number):
        self.small_key_num = number
        # allowing a different number if bk is behind this door in a set of locations
        self.alternate_small_key = None
        self.alternate_big_key_loc = set()
        # for a place with only 1 free location/key_only_location behind it ... no goals and locations
        self.allow_small = False
        self.small_location = None


class KeyCounter(object):

    def __init__(self, max_chests):
        self.max_chests = max_chests
        self.free_locations = set()
        self.key_only_locations = set()
        self.child_doors = set()
        self.open_doors = set()
        self.used_keys = 0
        self.big_key_opened = False
        self.important_location = False

    def update(self, key_sphere):
        self.free_locations.update(key_sphere.free_locations)
        self.key_only_locations.update(key_sphere.key_only_locations)
        self.child_doors.update([x for x in key_sphere.child_doors if x not in self.open_doors and x.dest not in self.open_doors])
        self.important_location = self.important_location or key_sphere.prize_region or self.special_region(key_sphere)

    @staticmethod
    def special_region(key_sphere):
        for other in key_sphere.other_locations:
            # todo: zelda's cell is special in standard, and probably crossed too
            if other.name in ['Attic Cracked Floor', 'Suspicious Maiden']:
                return True
        return False

    def open_door(self, door, flat_proposal):
        if door in flat_proposal:
            self.used_keys += 1
            self.child_doors.remove(door)
            self.open_doors.add(door)
            if door.dest in flat_proposal:
                self.open_doors.add(door.dest)
                if door.dest in self.child_doors:
                    self.child_doors.remove(door.dest)
        elif door.bigKey:
            self.big_key_opened = True
            self.child_doors.remove(door)
            self.open_doors.add(door)

    def used_smalls_loc(self, reserve=0):
        return max(self.used_keys + reserve - len(self.key_only_locations), 0)

    def copy(self):
        ret = KeyCounter(self.max_chests)
        ret.free_locations.update(self.free_locations)
        ret.key_only_locations.update(self.key_only_locations)
        ret.child_doors.update(self.child_doors)
        ret.used_keys = self.used_keys
        ret.open_doors.update(self.open_doors)
        ret.big_key_opened = self.big_key_opened
        ret.important_location = self.important_location
        return ret


def analyze_dungeon(key_layout, world, player):
    key_layout = KeyLayout(key_layout.sector, key_layout.start_regions, key_layout.proposal)
    key_layout.flat_prop = flatten_pair_list(key_layout.proposal)
    key_layout.key_spheres = create_key_spheres(key_layout, world, player)
    key_logic = key_layout.key_logic
    key_layout.max_chests = len(world.get_dungeon(key_layout.sector.name, player).small_keys)

    find_bk_locked_sections(key_layout, world)

    key_counter = KeyCounter(key_layout.max_chests)
    key_counter.update(key_layout.key_spheres['Origin'])
    queue = collections.deque([(key_layout.key_spheres['Origin'], key_counter)])
    doors_completed = set()

    while len(queue) > 0:
        key_sphere, key_counter = queue.popleft()
        chest_keys = available_chest_small_keys(key_counter, False, world)
        # chest_keys_bk = available_chest_small_keys(key_counter, True, world)
        available = chest_keys + len(key_counter.key_only_locations) - key_counter.used_keys
        possible_smalls = count_unique_small_doors(key_counter, key_layout.flat_prop)
        if not key_counter.big_key_opened:
            if chest_keys == count_locations_big_optional(key_counter.free_locations) and available <= possible_smalls:
                key_logic.bk_restricted.update(key_counter.free_locations)
                # logic min?
                if not key_sphere.bk_locked and big_chest_in_locations(key_counter.free_locations):
                    key_logic.sm_restricted.update(find_big_chest_locations(key_counter.free_locations))
        # todo: this feels like big key doors aren't accounted for - you may or may not find the big_key door at this point
        minimal_keys = available + key_counter.used_keys
        minimal_satisfied = False
        # todo: detect forced subsequent keys - see keypuzzles
        # try to relax the rules here? - smallest requirement that doesn't force a softlock
        childqueue = collections.deque()
        for child in sorted(list(key_sphere.child_doors), key=lambda x: x.name):
            next_sphere = key_layout.key_spheres[child.name]
            if not empty_sphere(next_sphere) and child not in doors_completed:
                childqueue.append((child, next_sphere))
        while len(childqueue) > 0:
            child, next_sphere = childqueue.popleft()
            if not child.bigKey:
                expanded_counter = expand_counter_to_last_door(child, key_counter, key_layout, set())
                parent_rule = find_best_parent_rule(key_layout, child)
                if parent_rule is not None:
                    true_min = max(minimal_keys, parent_rule.small_key_num + 1)
                else:
                    true_min = minimal_keys
                last_small_child = len([x for x in childqueue if not x[0].bigKey]) == 0
                force_min = not minimal_satisfied and last_small_child
                rule = create_rule(expanded_counter, key_layout, true_min, force_min, world)
                minimal_satisfied = minimal_satisfied or rule.small_key_num <= minimal_keys
                check_for_self_lock_key(rule, next_sphere, key_layout, world)
                bk_restricted_rules(rule, next_sphere, key_counter, key_layout, true_min, force_min, world)
                key_logic.door_rules[child.name] = rule
            doors_completed.add(next_sphere.access_door)
            next_counter = increment_key_counter(child, next_sphere, key_counter, key_layout.flat_prop)
            queue.append((next_sphere, next_counter))
    return key_layout


def find_bk_locked_sections(key_layout, world):
    key_spheres = key_layout.key_spheres
    key_logic = key_layout.key_logic

    bk_key_not_required = set()
    big_chest_allowed_big_key = world.accessibility != 'locations'
    for key in key_spheres.keys():
        sphere = key_spheres[key]
        key_layout.all_chest_locations.update(sphere.free_locations)
        if sphere.bk_locked and (sphere.prize_region or KeyCounter.special_region(sphere)):
            big_chest_allowed_big_key = False
        if not sphere.bk_locked:
            bk_key_not_required.update(sphere.free_locations)
    key_logic.bk_restricted.update(key_layout.all_chest_locations.difference(bk_key_not_required))
    if not big_chest_allowed_big_key:
        key_logic.bk_restricted.update(find_big_chest_locations(key_layout.all_chest_locations))


def empty_sphere(sphere):
    if len(sphere.key_only_locations) != 0 or len(sphere.free_locations) != 0 or len(sphere.child_doors) != 0:
        return False
    return not sphere.prize_region


def find_best_parent_rule(key_layout, child):
    best = None
    for door_name, sphere in key_layout.key_spheres.items():
        if sphere.access_door is not None and child in sphere.child_doors:
            if door_name in key_layout.key_logic.door_rules.keys():
                rule = key_layout.key_logic.door_rules[door_name]
                if best is None or rule.small_key_num < best.small_key_num:
                    best = rule
    return best


def relative_empty_sphere(sphere, key_counter):
    if len(sphere.key_only_locations.difference(key_counter.key_only_locations)) > 0:
        return False
    if len(sphere.free_locations.difference(key_counter.free_locations)) > 0:
        return False
    new_child_door = False
    for child in sphere.child_doors:
        if unique_child_door(child, key_counter):
            new_child_door = True
            break
    if new_child_door:
        return False
    return True


def unique_child_door(child, key_counter):
    if child in key_counter.child_doors or child.dest in key_counter.child_doors:
        return False
    if child in key_counter.open_doors or child.dest in key_counter.child_doors:
        return False
    if child.bigKey and key_counter.big_key_opened:
        return False
    return True


# def relative_empty_sphere2(expanded_sphere, key_counter):
#     return len(expanded_sphere.free_locations.difference(key_counter.free_locations)) == 0
#
#
# def expand_sphere(sphere, key_layout):
#     counter = KeyCounter(key_layout.max_chests)
#     counter.update(sphere)
#     queue = collections.deque(counter.child_doors)
#     already_queued = set(counter.child_doors)
#     while len(queue) > 0:
#         child = queue.popleft()
#         if child not in counter.open_doors:
#             counter = increment_key_counter(child, key_layout.key_spheres[child.name], counter, key_layout.flat_prop)
#             for new_door in counter.child_doors:
#                 if new_door not in already_queued:
#                     queue.append(new_door)
#                     already_queued.add(new_door)
#     return counter


def increment_key_counter(door, sphere, key_counter, flat_proposal):
    new_counter = key_counter.copy()
    new_counter.open_door(door, flat_proposal)
    new_counter.update(sphere)
    return new_counter


def expand_counter_to_last_door(door, key_counter, key_layout, ignored_doors):
    door_sphere = key_layout.key_spheres[door.name]
    small_doors = set()
    big_doors = set()
    for other in key_counter.child_doors:
        if other != door and other not in ignored_doors:
            if other.bigKey:
                big_doors.add(other)
            elif other.dest not in small_doors:
                small_doors.add(other)
    # I feel bk might be available if the current small door could use a key_only_loc - the param might cover this case
    big_key_available = len(key_counter.free_locations) - key_counter.used_smalls_loc(1) > 0
    if len(small_doors) == 0 and (len(big_doors) == 0 or not big_key_available):
        return key_counter
    new_counter = key_counter
    last_counter = key_counter
    new_ignored = set(ignored_doors)
    for new_door in small_doors.union(big_doors):
        new_sphere = key_layout.key_spheres[new_door.name]
        new_counter = increment_key_counter(new_door, new_sphere, new_counter, key_layout.flat_prop)
        # this means the new_door invalidates the door / leads to the same stuff
        if relative_empty_sphere(door_sphere, new_counter):
            new_counter = last_counter
            new_ignored.add(new_door)
        else:
            last_counter = new_counter
    old_counter = None
    while old_counter != new_counter:
        old_counter = new_counter
        new_counter = expand_counter_to_last_door(door, old_counter, key_layout, new_ignored)
    return new_counter


def create_rule(key_counter, key_layout, minimal_keys, force_min, world):
    chest_keys = available_chest_small_keys(key_counter, key_counter.big_key_opened, world)
    available = chest_keys + len(key_counter.key_only_locations) - key_counter.used_keys
    possible_smalls = count_unique_small_doors(key_counter, key_layout.flat_prop)
    required_keys = min(available, possible_smalls) + key_counter.used_keys
    if not force_min or required_keys <= minimal_keys:
        return DoorRules(required_keys)
    else:
        return DoorRules(minimal_keys)


def check_for_self_lock_key(rule, sphere, key_layout, world):
    if world.accessibility != 'locations':
        counter = KeyCounter(key_layout.max_chests)
        counter.update(sphere)
        if not self_lock_possible(counter):
            return
        queue = collections.deque(counter.child_doors)
        already_queued = set(counter.child_doors)
        while len(queue) > 0:
            child = queue.popleft()
            if child not in counter.open_doors:
                counter = increment_key_counter(child, key_layout.key_spheres[child.name], counter, key_layout.flat_prop)
                if not self_lock_possible(counter):
                    return
                for new_door in counter.child_doors:
                    if new_door not in already_queued:
                        queue.append(new_door)
                        already_queued.add(new_door)
        if len(counter.free_locations) == 1 and len(counter.key_only_locations) == 0 and not counter.important_location:
            rule.allow_small = True
            rule.small_location = next(iter(counter.free_locations))


def self_lock_possible(counter):
    return len(counter.free_locations) <= 1 and len(counter.key_only_locations) == 0 and not counter.important_location


def available_chest_small_keys(key_counter, bk, world):
    if not world.keysanity and world.mode != 'retro':
        cnt = 0
        for loc in key_counter.free_locations:
            if bk or '- Big Chest' not in loc.name:
                cnt += 1
        return min(cnt, key_counter.max_chests)
    else:
        return key_counter.max_chests


def bk_restricted_rules(rule, sphere, key_counter, key_layout, minimal_keys, force_min, world):
    if sphere.bk_locked:
        return
    expanded_counter = expand_counter_no_big_doors(sphere.access_door, key_counter, key_layout, set())
    bk_number = create_rule(expanded_counter, key_layout, minimal_keys, force_min, world).small_key_num
    if bk_number == rule.small_key_num:
        return
    post_counter = KeyCounter(key_layout.max_chests)
    post_counter.update(sphere)
    other_doors_beyond_me = [x for x in post_counter.child_doors if not x.bigKey]
    queue = collections.deque(other_doors_beyond_me)
    already_queued = set(other_doors_beyond_me)
    while len(queue) > 0:
        child = queue.popleft()
        if child not in post_counter.open_doors:
            post_counter = increment_key_counter(child, key_layout.key_spheres[child.name], post_counter, key_layout.flat_prop)
            for new_door in post_counter.child_doors:
                if not new_door.bigKey and new_door not in already_queued and new_door.dest not in already_queued:
                    queue.append(new_door)
                    already_queued.add(new_door)
    unique_loc = post_counter.free_locations.difference(expanded_counter.free_locations)
    if len(unique_loc) > 0:
        rule.alternate_small_key = bk_number
        rule.alternate_big_key_loc.update(unique_loc)


def expand_counter_no_big_doors(door, key_counter, key_layout, ignored_doors):
    door_sphere = key_layout.key_spheres[door.name]
    small_doors = set()
    for other in key_counter.child_doors:
        if other != door and other not in ignored_doors:
            if other.dest not in small_doors and not other.bigKey:
                small_doors.add(other)
    if len(small_doors) == 0:
        return key_counter
    new_counter = key_counter
    last_counter = key_counter
    new_ignored = set(ignored_doors)
    for new_door in small_doors:
        new_sphere = key_layout.key_spheres[new_door.name]
        new_counter = increment_key_counter(new_door, new_sphere, new_counter, key_layout.flat_prop)
        # this means the new_door invalidates the door / leads to the same stuff
        if relative_empty_sphere(door_sphere, new_counter):
            new_counter = last_counter
            new_ignored.add(new_door)
        else:
            last_counter = new_counter
    old_counter = None
    while old_counter != new_counter:
        old_counter = new_counter
        new_counter = expand_counter_no_big_doors(door, old_counter, key_layout, new_ignored)
    return new_counter


def create_key_spheres(key_layout, world, player):
    key_spheres = {}
    flat_proposal = key_layout.flat_prop
    state = ExplorationState()
    state.key_locations = len(world.get_dungeon(key_layout.sector.name, player).small_keys)
    state.big_key_special = world.get_region('Hyrule Dungeon Cellblock', player) in key_layout.sector.regions
    for region in key_layout.start_regions:
        state.visit_region(region, key_checks=True)
        state.add_all_doors_check_keys(region, flat_proposal, world, player)
    expand_key_state(state, flat_proposal, world, player)
    key_spheres['Origin'] = create_key_sphere(state, None, None)
    queue = collections.deque([(key_spheres['Origin'], state)])
    while len(queue) > 0:
        next_key_sphere, parent_state = queue.popleft()
        for door in next_key_sphere.child_doors:
            child_state = parent_state.copy()
            # open the door
            open_a_door(door, child_state, flat_proposal)
            expand_key_state(child_state, flat_proposal, world, player)
            child_kr = create_key_sphere(child_state, next_key_sphere, door)
            if door.name not in key_spheres.keys():
                key_spheres[door.name] = child_kr
                queue.append((child_kr, child_state))
            else:
                old_sphere = key_spheres[door.name]
                old_sphere.bk_locked = old_sphere.bk_locked and child_kr.bk_locked
    return key_spheres


def create_key_sphere(state, parent_sphere, door):
    key_sphere = KeySphere()
    key_sphere.parent_sphere = parent_sphere
    p_region = parent_sphere
    parent_doors = set()
    parent_locations = set()
    while p_region is not None:
        parent_doors.update(p_region.child_doors)
        parent_locations.update(p_region.free_locations)
        parent_locations.update(p_region.key_only_locations)
        parent_locations.update(p_region.other_locations)
        p_region = p_region.parent_sphere
    u_doors = unique_doors(state.small_doors+state.big_doors).difference(parent_doors)
    key_sphere.child_doors.update(u_doors)
    region_locations = set(state.found_locations).difference(parent_locations)
    for loc in region_locations:
        if '- Prize' in loc.name or loc.name in ['Agahnim 1', 'Agahnim 2']:
            key_sphere.prize_region = True
            key_sphere.other_locations.add(loc)
        elif loc.event and 'Small Key' in loc.item.name:
            key_sphere.key_only_locations.add(loc)
        elif loc.name not in dungeon_events:
            key_sphere.free_locations.add(loc)
        else:
            key_sphere.other_locations.add(loc)
    # todo: Cellblock in a dungeon with a big_key door or chest - Crossed Mode
    key_sphere.bk_locked = state.big_key_opened if not state.big_key_special else False
    if door is not None:
        key_sphere.access_door = door
    return key_sphere


def open_a_door(door, child_state, flat_proposal):
    if door.bigKey:
        child_state.big_key_opened = True
        child_state.avail_doors.extend(child_state.big_doors)
        child_state.opened_doors.extend(set([d.door for d in child_state.big_doors]))
        child_state.big_doors.clear()
    else:
        child_state.opened_doors.append(door)
        doors_to_open = [x for x in child_state.small_doors if x.door == door]
        child_state.small_doors[:] = [x for x in child_state.small_doors if x.door != door]
        child_state.avail_doors.extend(doors_to_open)
        dest_door = door.dest
        if dest_door in flat_proposal:
            child_state.opened_doors.append(dest_door)
            if child_state.in_door_list_ic(dest_door, child_state.small_doors):
                now_available = [x for x in child_state.small_doors if x.door == dest_door]
                child_state.small_doors[:] = [x for x in child_state.small_doors if x.door != dest_door]
                child_state.avail_doors.extend(now_available)


# allows dest doors
def unique_doors(doors):
    unique_d_set = set()
    for d in doors:
        if d.door not in unique_d_set:
            unique_d_set.add(d.door)
    return unique_d_set


# doesn't count dest doors
def count_unique_small_doors(key_counter, proposal):
    cnt = 0
    counted = set()
    for door in key_counter.child_doors:
        if door in proposal and door not in counted:
            cnt += 1
            counted.add(door)
            counted.add(door.dest)
    return cnt


def count_locations_big_optional(locations, bk=False):
    cnt = 0
    for loc in locations:
        if bk or '- Big Chest' not in loc.name:
            cnt += 1
    return cnt


def big_chest_in_locations(locations):
    return len(find_big_chest_locations(locations)) > 0


def find_big_chest_locations(locations):
    ret = []
    for loc in locations:
        if 'Big Chest' in loc.name:
            ret.append(loc)
    return ret


def expand_key_state(state, flat_proposal, world, player):
    while len(state.avail_doors) > 0:
        exp_door = state.next_avail_door()
        door = exp_door.door
        connect_region = world.get_entrance(door.name, player).connected_region
        if state.validate(door, connect_region, world, player):
            state.visit_region(connect_region, key_checks=True)
            state.add_all_doors_check_keys(connect_region, flat_proposal, world, player)


def flatten_pair_list(paired_list):
    flat_list = []
    for d in paired_list:
        if type(d) is tuple:
            flat_list.append(d[0])
            flat_list.append(d[1])
        else:
            flat_list.append(d)
    return flat_list


# Soft lock stuff
class SoftLockException(Exception):
    pass


# vanilla validation code
def validate_vanilla_key_logic(world, player):
    validators = {
        'Hyrule Castle': val_hyrule,
        'Eastern Palace': val_eastern,
        'Desert Palace': val_desert,
        'Tower of Hera': val_hera,
        'Agahnims Tower': val_tower,
        'Palace of Darkness': val_pod,
        'Swamp Palace': val_swamp,
        'Skull Woods': val_skull,
        'Thieves Town': val_thieves,
        'Ice Palace': val_ice,
        'Misery Mire': val_mire,
        'Turtle Rock': val_turtle,
        'Ganons Tower': val_ganons
    }
    key_logic_dict = world.key_logic[player]
    for key, key_logic in key_logic_dict.items():
        validators[key](key_logic, world, player)


def val_hyrule(key_logic, world, player):
    val_rule(key_logic.door_rules['Sewers Secret Room Key Door S'], 2)
    val_rule(key_logic.door_rules['Sewers Dark Cross Key Door N'], 3)
    val_rule(key_logic.door_rules['Hyrule Dungeon Map Room Key Door S'], 3)
    val_rule(key_logic.door_rules['Hyrule Dungeon Armory Interior Key Door N'], 4, True, 'Hyrule Castle - Zelda\'s Chest')
    # why is allow_small actually false?
    # val_rule(key_logic.door_rules['Hyrule Dungeon Armory Interior Key Door N'], 4)


def val_eastern(key_logic, world, player):
    # val_rule(key_logic.door_rules['Eastern Dark Square Key Door WN'], 2, False, None, 1, {'Eastern Palace - Big Key Chest'})
    val_rule(key_logic.door_rules['Eastern Dark Square Key Door WN'], 1)
    val_rule(key_logic.door_rules['Eastern Darkness Up Stairs'], 2)
    assert world.get_location('Eastern Palace - Big Chest', player) in key_logic.bk_restricted
    assert world.get_location('Eastern Palace - Boss', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 2


def val_desert(key_logic, world, player):
    val_rule(key_logic.door_rules['Desert East Wing Key Door EN'], 4)
    val_rule(key_logic.door_rules['Desert Tiles 1 Up Stairs'], 2)
    val_rule(key_logic.door_rules['Desert Beamos Hall NE'], 3)
    val_rule(key_logic.door_rules['Desert Tiles 2 NE'], 4)
    assert world.get_location('Desert Palace - Big Chest', player) in key_logic.bk_restricted
    assert world.get_location('Desert Palace - Boss', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 2


def val_hera(key_logic, world, player):
    val_rule(key_logic.door_rules['Hera Lobby Key Stairs'], 1, True, 'Tower of Hera - Big Key Chest')
    assert world.get_location('Tower of Hera - Big Chest', player) in key_logic.bk_restricted
    assert world.get_location('Tower of Hera - Compass Chest', player) in key_logic.bk_restricted
    assert world.get_location('Tower of Hera - Boss', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 3


def val_tower(key_logic, world, player):
    val_rule(key_logic.door_rules['Tower Room 03 Up Stairs'], 1)
    val_rule(key_logic.door_rules['Tower Dark Maze ES'], 2)
    val_rule(key_logic.door_rules['Tower Dark Archers Up Stairs'], 3)
    val_rule(key_logic.door_rules['Tower Circle of Pots WS'], 4)


def val_pod(key_logic, world, player):
    val_rule(key_logic.door_rules['PoD Arena Main NW'], 4)
    val_rule(key_logic.door_rules['PoD Basement Ledge Up Stairs'], 6, True, 'Palace of Darkness - Big Key Chest')
    val_rule(key_logic.door_rules['PoD Compass Room SE'], 6, True, 'Palace of Darkness - Harmless Hellway')
    val_rule(key_logic.door_rules['PoD Falling Bridge WN'], 6)
    val_rule(key_logic.door_rules['PoD Dark Pegs WN'], 6)
    assert world.get_location('Palace of Darkness - Big Chest', player) in key_logic.bk_restricted
    assert world.get_location('Palace of Darkness - Boss', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 2


def val_swamp(key_logic, world, player):
    val_rule(key_logic.door_rules['Swamp Entrance Down Stairs'], 1)
    val_rule(key_logic.door_rules['Swamp Pot Row WS'], 2)
    val_rule(key_logic.door_rules['Swamp Trench 1 Key Ledge NW'], 3)
    val_rule(key_logic.door_rules['Swamp Hub North Ledge N'], 5)
    val_rule(key_logic.door_rules['Swamp Hub WN'], 6)
    val_rule(key_logic.door_rules['Swamp Waterway NW'], 6)
    assert world.get_location('Swamp Palace - Entrance', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 1


def val_skull(key_logic, world, player):
    val_rule(key_logic.door_rules['Skull 3 Lobby NW'], 4)
    val_rule(key_logic.door_rules['Skull Spike Corner ES'], 5)


def val_thieves(key_logic, world, player):
    val_rule(key_logic.door_rules['Thieves Hallway WS'], 1)
    val_rule(key_logic.door_rules['Thieves Spike Switch Up Stairs'], 3)
    val_rule(key_logic.door_rules['Thieves Conveyor Bridge WS'], 3, True, 'Thieves\' Town - Big Chest')
    assert world.get_location('Thieves\' Town - Attic', player) in key_logic.bk_restricted
    assert world.get_location('Thieves\' Town - Boss', player) in key_logic.bk_restricted
    assert world.get_location('Thieves\' Town - Blind\'s Cell', player) in key_logic.bk_restricted
    assert world.get_location('Thieves\' Town - Big Chest', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 4


def val_ice(key_logic, world, player):
    val_rule(key_logic.door_rules['Ice Jelly Key Down Stairs'], 1)
    val_rule(key_logic.door_rules['Ice Conveyor SW'], 2)
    val_rule(key_logic.door_rules['Ice Backwards Room Down Stairs'], 5)
    assert world.get_location('Ice Palace - Boss', player) in key_logic.bk_restricted
    assert world.get_location('Ice Palace - Big Chest', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 2


def val_mire(key_logic, world, player):
    mire_west_wing = {'Misery Mire - Big Key Chest', 'Misery Mire - Compass Chest'}
    val_rule(key_logic.door_rules['Mire Spikes NW'], 4)  # todo: crystal state in key door analysis
    val_rule(key_logic.door_rules['Mire Hub WS'], 5, False, None, 4, mire_west_wing)
    val_rule(key_logic.door_rules['Mire Conveyor Crystal WS'], 6, False, None, 5, mire_west_wing)
    assert world.get_location('Misery Mire - Boss', player) in key_logic.bk_restricted
    assert world.get_location('Misery Mire - Big Chest', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 2


def val_turtle(key_logic, world, player):
    val_rule(key_logic.door_rules['TR Hub NW'], 1)
    val_rule(key_logic.door_rules['TR Pokey 1 NW'], 2)
    val_rule(key_logic.door_rules['TR Chain Chomps Down Stairs'], 3)
    val_rule(key_logic.door_rules['TR Pokey 2 ES'], 6, True, 'Turtle Rock - Big Key Chest', 4, {'Turtle Rock - Big Key Chest'})
    val_rule(key_logic.door_rules['TR Crystaroller Down Stairs'], 5)
    val_rule(key_logic.door_rules['TR Dash Bridge WS'], 6)
    assert world.get_location('Turtle Rock - Eye Bridge - Bottom Right', player) in key_logic.bk_restricted
    assert world.get_location('Turtle Rock - Eye Bridge - Top Left', player) in key_logic.bk_restricted
    assert world.get_location('Turtle Rock - Eye Bridge - Top Right', player) in key_logic.bk_restricted
    assert world.get_location('Turtle Rock - Eye Bridge - Bottom Left', player) in key_logic.bk_restricted
    assert world.get_location('Turtle Rock - Boss', player) in key_logic.bk_restricted
    assert world.get_location('Turtle Rock - Crystaroller Room', player) in key_logic.bk_restricted
    assert world.get_location('Turtle Rock - Big Chest', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 7


def val_ganons(key_logic, world, player):
    rando_room = {'Ganons Tower - Randomizer Room - Top Left', 'Ganons Tower - Randomizer Room - Top Right', 'Ganons Tower - Randomizer Room - Bottom Left', 'Ganons Tower - Randomizer Room - Bottom Right'}
    compass_room = {'Ganons Tower - Compass Room - Top Left', 'Ganons Tower - Compass Room - Top Right', 'Ganons Tower - Compass Room - Bottom Left', 'Ganons Tower - Compass Room - Bottom Right'}
    gt_middle = {'Ganons Tower - Big Key Room - Left', 'Ganons Tower - Big Key Chest', 'Ganons Tower - Big Key Room - Right', 'Ganons Tower - Bob\'s Chest', 'Ganons Tower - Big Chest'}
    val_rule(key_logic.door_rules['GT Double Switch EN'], 7, False, None, 5, rando_room.union({'Ganons Tower - Firesnake Room'}))
    val_rule(key_logic.door_rules['GT Hookshot ES'], 8, True, 'Ganons Tower - Map Chest', 6, {'Ganons Tower - Map Chest'})
    val_rule(key_logic.door_rules['GT Tile Room EN'], 6, False, None, 5, compass_room)
    val_rule(key_logic.door_rules['GT Firesnake Room SW'], 8, False, None, 6, rando_room)
    val_rule(key_logic.door_rules['GT Conveyor Star Pits EN'], 7, False, None, 6, gt_middle)
    val_rule(key_logic.door_rules['GT Mini Helmasaur Room WN'], 7)
    val_rule(key_logic.door_rules['GT Crystal Circles SW'], 8)
    assert world.get_location('Ganons Tower - Mini Helmasaur Room - Left', player) in key_logic.bk_restricted
    assert world.get_location('Ganons Tower - Mini Helmasaur Room - Right', player) in key_logic.bk_restricted
    assert world.get_location('Ganons Tower - Big Chest', player) in key_logic.bk_restricted
    assert world.get_location('Ganons Tower - Pre-Moldorm Chest', player) in key_logic.bk_restricted
    assert world.get_location('Ganons Tower - Validation Chest', player) in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 5


def val_rule(rule, skn, allow=False, loc=None, askn=None, setCheck=None):
    if setCheck is None:
        setCheck = set()
    assert rule.small_key_num == skn
    assert rule.allow_small == allow
    assert rule.small_location == loc or rule.small_location.name == loc
    assert rule.alternate_small_key == askn
    assert len(setCheck) == len(rule.alternate_big_key_loc)
    for loc in rule.alternate_big_key_loc:
        assert loc.name in setCheck
