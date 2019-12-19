import collections
from collections import defaultdict

from Regions import dungeon_events
from Dungeons import dungeon_keys, dungeon_bigs
from DungeonGenerator import ExplorationState


class KeySphere(object):

    def __init__(self):
        self.access_door = None
        self.free_locations = {}
        self.prize_region = False
        self.key_only_locations = {}
        self.child_doors = {}
        self.bk_locked = False
        self.parent_sphere = None
        self.other_locations = {}

    def __eq__(self, other):
        if self.prize_region != other.prize_region:
            return False
        # already have merge function for this
        # if self.bk_locked != other.bk_locked:
        #     return False
        if len(self.free_locations) != len(other.free_locations):
            return False
        if len(self.key_only_locations) != len(other.key_only_locations):
            return False
        if len(set(self.free_locations).symmetric_difference(set(other.free_locations))) > 0:
            return False
        if len(set(self.key_only_locations).symmetric_difference(set(other.key_only_locations))) > 0:
            return False
        if len(set(self.child_doors).symmetric_difference(set(other.child_doors))) > 0:
            return False
        return True


class KeyLayout(object):

    def __init__(self, sector, starts, proposal):
        self.sector = sector
        self.start_regions = starts
        self.proposal = proposal
        self.key_logic = KeyLogic(sector.name)

        self.key_spheres = None
        self.key_counters = None
        self.flat_prop = None
        self.max_chests = None
        self.max_drops = None
        self.all_chest_locations = {}

        # bk special?
        # bk required? True if big chests or big doors exists

    def reset(self, proposal):
        self.proposal = proposal
        self.flat_prop = flatten_pair_list(self.proposal)
        self.key_logic = KeyLogic(self.sector.name)


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
        self.free_locations = {}
        self.key_only_locations = {}
        self.child_doors = {}
        self.open_doors = {}
        self.used_keys = 0
        self.big_key_opened = False
        self.important_location = False

    def update(self, key_sphere):
        self.free_locations.update(key_sphere.free_locations)
        self.key_only_locations.update(key_sphere.key_only_locations)
        self.child_doors.update(dict.fromkeys([x for x in key_sphere.child_doors if x not in self.open_doors and x.dest not in self.open_doors]))
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
            del self.child_doors[door]
            self.open_doors[door] = None
            if door.dest in flat_proposal:
                self.open_doors[door.dest] = None
                if door.dest in self.child_doors:
                    del self.child_doors[door.dest]
        elif door.bigKey:
            self.big_key_opened = True
            del self.child_doors[door]
            self.open_doors[door] = None

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


def build_key_layout(sector, start_regions, proposal, world, player):
    key_layout = KeyLayout(sector, start_regions, proposal)
    key_layout.flat_prop = flatten_pair_list(key_layout.proposal)
    key_layout.max_chests = len(world.get_dungeon(key_layout.sector.name, player).small_keys)
    key_layout.max_drops = count_key_drops(key_layout.sector)
    return key_layout


def analyze_dungeon(key_layout, world, player):
    key_layout.key_counters = create_key_counters(key_layout, world, player)
    key_layout.key_spheres = create_key_spheres(key_layout, world, player)
    key_logic = key_layout.key_logic

    find_bk_locked_sections(key_layout, world)

    init_bk = check_special_locations(key_layout.key_spheres['Origin'].free_locations.keys())
    key_counter = key_layout.key_counters[counter_id({}, init_bk, key_layout.flat_prop)]
    queue = collections.deque([(key_layout.key_spheres['Origin'], key_counter)])
    doors_completed = set()

    while len(queue) > 0:
        queue = collections.deque(sorted(queue, key=queue_sorter))
        key_sphere, key_counter = queue.popleft()
        chest_keys = available_chest_small_keys(key_counter, world)
        raw_avail = chest_keys + len(key_counter.key_only_locations)
        available = raw_avail - key_counter.used_keys
        possible_smalls = count_unique_small_doors(key_counter, key_layout.flat_prop)
        if not key_counter.big_key_opened:
            if chest_keys == count_locations_big_optional(key_counter.free_locations) and available <= possible_smalls:
                key_logic.bk_restricted.update(filter_big_chest(key_counter.free_locations))
                if not key_sphere.bk_locked and big_chest_in_locations(key_counter.free_locations):
                    key_logic.sm_restricted.update(find_big_chest_locations(key_counter.free_locations))
        # todo: detect forced subsequent keys - see keypuzzles
        # try to relax the rules here? - smallest requirement that doesn't force a softlock
        child_queue = collections.deque()
        for child in sorted(list(key_sphere.child_doors), key=lambda x: x.name):
            next_sphere = key_layout.key_spheres[child.name]
            # todo: empty_sphere are not always empty, Mire spike barrier is not empty if other doors open first
            if not empty_sphere(next_sphere) and child not in doors_completed:
                child_queue.append((child, next_sphere))
        while len(child_queue) > 0:
            child, next_sphere = child_queue.popleft()
            if not child.bigKey:
                best_counter = find_best_counter(child, key_counter, key_layout, world, False)
                rule = create_rule(best_counter, key_counter, key_layout, world)
                check_for_self_lock_key(rule, next_sphere, key_layout, world)
                bk_restricted_rules(rule, next_sphere, key_counter, key_layout, world)
                key_logic.door_rules[child.name] = rule
            doors_completed.add(next_sphere.access_door)
            next_counter = find_next_counter(child, key_counter, next_sphere, key_layout)
            queue.append((next_sphere, next_counter))
    check_rules(key_layout)
    return key_layout


def count_key_drops(sector):
    cnt = 0
    for region in sector.regions:
        for loc in region.locations:
            if loc.event and 'Small Key' in loc.item.name:
                cnt += 1
    return cnt


def queue_sorter(queue_item):
    sphere, counter = queue_item
    if sphere.access_door is None:
        return 0
    return 1 if sphere.access_door.bigKey else 0


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
    key_logic.bk_restricted.update(dict.fromkeys(set(key_layout.all_chest_locations).difference(bk_key_not_required)))
    if not big_chest_allowed_big_key:
        key_logic.bk_restricted.update(find_big_chest_locations(key_layout.all_chest_locations))


def empty_sphere(sphere):
    if len(sphere.key_only_locations) != 0 or len(sphere.free_locations) != 0 or len(sphere.child_doors) != 0:
        return False
    return not sphere.prize_region


def relative_empty_sphere(sphere, key_counter):
    if len(set(sphere.key_only_locations).difference(key_counter.key_only_locations)) > 0:
        return False
    if len(set(sphere.free_locations).difference(key_counter.free_locations)) > 0:
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


def increment_key_counter(door, sphere, key_counter, flat_proposal):
    new_counter = key_counter.copy()
    new_counter.open_door(door, flat_proposal)
    new_counter.update(sphere)
    return new_counter


def find_best_counter(door, key_counter, key_layout, world, skip_bk):  # try to waste as many keys as possible?
    door_sphere = key_layout.key_spheres[door.name]
    ignored_doors = {door, door.dest}
    finished = False
    opened_doors = dict(key_counter.open_doors)
    bk_opened = key_counter.big_key_opened
    # new_counter = key_counter
    last_counter = key_counter
    while not finished:
        door_set = find_potential_open_doors(last_counter, ignored_doors, skip_bk)
        if door_set is None or len(door_set) == 0:
            finished = True
            continue
        for new_door in door_set:
            proposed_doors = {**opened_doors, **dict.fromkeys([new_door, new_door.dest])}
            bk_open = bk_opened or new_door.bigKey
            new_counter = find_counter(proposed_doors, bk_open, key_layout)
            bk_open = new_counter.big_key_opened
            # this means the new_door invalidates the door / leads to the same stuff
            if relative_empty_sphere(door_sphere, new_counter):
                ignored_doors.add(new_door)
            else:
                if not key_wasted(new_door, last_counter, new_counter, key_layout, world):
                    ignored_doors.add(new_door)
                else:
                    last_counter = new_counter
                    opened_doors = proposed_doors
                    bk_opened = bk_open
    return last_counter


def find_potential_open_doors(key_counter, ignored_doors, skip_bk):
    small_doors = []
    big_doors = []
    for other in key_counter.child_doors:
        if other not in ignored_doors and other.dest not in ignored_doors:
            if other.bigKey:
                if not skip_bk:
                    big_doors.append(other)
            elif other.dest not in small_doors:
                small_doors.append(other)
    big_key_available = len(key_counter.free_locations) - key_counter.used_smalls_loc(1) > 0
    if len(small_doors) == 0 and (not skip_bk and (len(big_doors) == 0 or not big_key_available)):
        return None
    return small_doors + big_doors


def key_wasted(new_door, old_counter, new_counter, key_layout, world):
    if new_door.bigKey:  # big keys are not wastes - it uses up a location
        return True
    chest_keys = available_chest_small_keys(old_counter, world)
    old_avail = chest_keys + len(old_counter.key_only_locations) - old_counter.used_keys
    new_chest_keys = available_chest_small_keys(new_counter, world)
    new_avail = new_chest_keys + len(new_counter.key_only_locations) - new_counter.used_keys
    if new_avail < old_avail:
        return True
    if new_avail == old_avail:
        old_children = old_counter.child_doors.keys()
        new_children = [x for x in new_counter.child_doors.keys() if x not in old_children and x.dest not in old_children]
        current_counter = new_counter
        opened_doors = dict(current_counter.open_doors)
        bk_opened = current_counter.big_key_opened
        for new_child in new_children:
            proposed_doors = {**opened_doors, **dict.fromkeys([new_child, new_child.dest])}
            bk_open = bk_opened or new_door.bigKey
            new_counter = find_counter(proposed_doors, bk_open, key_layout)
            if key_wasted(new_child, current_counter, new_counter, key_layout, world):
                return True  # waste is possible
    return False


def find_next_counter(new_door, old_counter, next_sphere, key_layout):
    proposed_doors = {**old_counter.open_doors, **dict.fromkeys([new_door, new_door.dest])}
    bk_open = old_counter.big_key_opened or new_door.bigKey or check_special_locations(next_sphere.free_locations)
    return key_layout.key_counters[counter_id(proposed_doors, bk_open, key_layout.flat_prop)]


def check_special_locations(locations):
    for loc in locations:
        if loc.name == 'Hyrule Castle - Zelda\'s Chest':
            return True
    return False


def calc_avail_keys(key_counter, world):
    chest_keys = available_chest_small_keys(key_counter, world)
    raw_avail = chest_keys + len(key_counter.key_only_locations)
    return raw_avail - key_counter.used_keys


def create_rule(key_counter, prev_counter, key_layout, world):
    prev_chest_keys = available_chest_small_keys(prev_counter, world)
    prev_avail = prev_chest_keys + len(prev_counter.key_only_locations)
    chest_keys = available_chest_small_keys(key_counter, world)
    key_gain = len(key_counter.key_only_locations) - len(prev_counter.key_only_locations)
    raw_avail = chest_keys + len(key_counter.key_only_locations)
    available = raw_avail - key_counter.used_keys
    possible_smalls = count_unique_small_doors(key_counter, key_layout.flat_prop)
    required_keys = min(available, possible_smalls) + key_counter.used_keys
    # if prev_avail < required_keys:
    #     required_keys = prev_avail + prev_counter.used_keys
    #     return DoorRules(required_keys)
    # else:
    adj_chest_keys = min(chest_keys, required_keys)
    needed_chests = required_keys - len(key_counter.key_only_locations)
    unneeded_chests = min(key_gain, adj_chest_keys - needed_chests)
    rule_num = required_keys - unneeded_chests
    return DoorRules(rule_num)


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


def available_chest_small_keys(key_counter, world):
    if not world.keysanity and world.mode != 'retro':
        cnt = 0
        for loc in key_counter.free_locations:
            if key_counter.big_key_opened or '- Big Chest' not in loc.name:
                cnt += 1
        return min(cnt, key_counter.max_chests)
    else:
        return key_counter.max_chests


def bk_restricted_rules(rule, sphere, key_counter, key_layout, world):
    if sphere.bk_locked:
        return
    best_counter = find_best_counter(sphere.access_door, key_counter, key_layout, world, True)
    bk_number = create_rule(best_counter, key_counter, key_layout, world).small_key_num
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
    unique_loc = set(post_counter.free_locations).difference(set(best_counter.free_locations))
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
    state = ExplorationState(dungeon=key_layout.sector.name)
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
                merge_sphere = old_sphere = key_spheres[door.name]
                if empty_sphere(old_sphere) and not empty_sphere(child_kr):
                    key_spheres[door.name] = merge_sphere = child_kr
                    queue.append((child_kr, child_state))
                if not empty_sphere(old_sphere) and not empty_sphere(child_kr) and not old_sphere == child_kr:
                    # ugly sphere merge function - just union locations - ugh
                    if old_sphere.bk_locked != child_kr.bk_locked:
                        if old_sphere.bk_locked:
                            merge_sphere.child_doors = child_kr.child_doors
                            merge_sphere.free_locations = child_kr.free_locations
                            merge_sphere.key_only_locations = child_kr.key_only_locations
                    else:
                        merge_sphere.child_doors = {**old_sphere.child_doors, **child_kr.child_doors}
                        merge_sphere.free_locations = {**old_sphere.free_locations, **child_kr.free_locations}
                        merge_sphere.key_only_locations = {**old_sphere.key_only_locations, **child_kr.key_only_locations}
                merge_sphere.bk_locked = old_sphere.bk_locked and child_kr.bk_locked
                # this feels so ugly, key counters are much smarter than this - would love to get rid of spheres
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
    u_doors = [x for x in unique_doors(state.small_doors+state.big_doors) if x not in parent_doors]
    key_sphere.child_doors.update(dict.fromkeys(u_doors))
    region_locations = [x for x in state.found_locations if x not in parent_locations]
    for loc in region_locations:
        if '- Prize' in loc.name or loc.name in ['Agahnim 1', 'Agahnim 2']:
            key_sphere.prize_region = True
            key_sphere.other_locations[loc] = None
        elif loc.event and 'Small Key' in loc.item.name:
            key_sphere.key_only_locations[loc] = None
        elif loc.name not in dungeon_events:
            key_sphere.free_locations[loc] = None
        else:
            key_sphere.other_locations[loc] = None
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
    unique_d_set = []
    for d in doors:
        if d.door not in unique_d_set:
            unique_d_set.append(d.door)
    return unique_d_set


# does not allow dest doors
def count_unique_sm_doors(doors):
    unique_d_set = set()
    for d in doors:
        if d not in unique_d_set and d.dest not in unique_d_set and not d.bigKey:
            unique_d_set.add(d)
    return len(unique_d_set)


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


def filter_big_chest(locations):
    return [x for x in locations if '- Big Chest' not in x.name]


def count_locations_exclude_big_chest(state):
    cnt = 0
    for loc in state.found_locations:
        if '- Big Chest' not in loc.name and '- Prize' not in loc.name:
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


def check_rules(key_layout):
    all_key_only = set()
    key_only_map = {}
    for sphere in key_layout.key_spheres.values():
        for loc in sphere.key_only_locations:
            if loc not in all_key_only:
                all_key_only.add(loc)
                access_rules = []
                key_only_map[loc] = access_rules
            else:
                access_rules = key_only_map[loc]
            if sphere.access_door is None or sphere.access_door.name not in key_layout.key_logic.door_rules.keys():
                access_rules.append(DoorRules(0))
            else:
                access_rules.append(key_layout.key_logic.door_rules[sphere.access_door.name])
    min_rule_bk = defaultdict(list)
    min_rule_non_bk = defaultdict(list)
    check_non_bk = False
    for loc, rule_list in key_only_map.items():
        m_bk = None
        m_nbk = None
        for rule in rule_list:
            if m_bk is None or rule.small_key_num <= m_bk:
                min_rule_bk[loc].append(rule)
                m_bk = rule.small_key_num
            if rule.alternate_small_key is None:
                ask = rule.small_key_num
            else:
                check_non_bk = True
                ask = rule.alternate_small_key
            if m_nbk is None or ask <= m_nbk:
                min_rule_non_bk[loc].append(rule)
                m_nbk = rule.alternate_small_key
    adjust_key_location_mins(key_layout, min_rule_bk, lambda r: r.small_key_num, lambda r, v: setattr(r, 'small_key_num', v))
    if check_non_bk:
        adjust_key_location_mins(key_layout, min_rule_non_bk, lambda r: r.small_key_num if r.alternate_small_key is None else r.alternate_small_key,
                                 lambda r, v: r if r.alternate_small_key is None else setattr(r, 'alternate_small_key', v))


def adjust_key_location_mins(key_layout, min_rules, getter, setter):
    collected_keys = key_layout.max_chests
    collected_locs = set()
    changed = True
    while changed:
        changed = False
        for_removal = []
        for loc, rules in min_rules.items():
            if loc in collected_locs:
                for_removal.append(loc)
            for rule in rules:
                if getter(rule) <= collected_keys and loc not in collected_locs:
                    changed = True
                    collected_keys += 1
                    collected_locs.add(loc)
                    for_removal.append(loc)
        for loc in for_removal:
            del min_rules[loc]
    if len(min_rules) > 0:
        for loc, rules in min_rules.items():
            for rule in rules:
                setter(rule, collected_keys)


# Soft lock stuff
def validate_key_layout_ex(key_layout, world, player):
    return validate_key_layout_main_loop(key_layout, world, player)


def validate_key_layout_main_loop(key_layout, world, player):
    flat_proposal = key_layout.flat_prop
    state = ExplorationState(dungeon=key_layout.sector.name)
    state.key_locations = len(world.get_dungeon(key_layout.sector.name, player).small_keys)
    state.big_key_special = world.get_region('Hyrule Dungeon Cellblock', player) in key_layout.sector.regions
    for region in key_layout.start_regions:
        state.visit_region(region, key_checks=True)
        state.add_all_doors_check_keys(region, flat_proposal, world, player)
    return validate_key_layout_sub_loop(state, {}, flat_proposal, world, player)


def validate_key_layout_sub_loop(state, checked_states, flat_proposal, world, player):
    expand_key_state(state, flat_proposal, world, player)
    smalls_avail = len(state.small_doors) > 0
    num_bigs = 1 if len(state.big_doors) > 0 else 0  # all or nothing
    if not smalls_avail and num_bigs == 0:
        return True   # I think that's the end
    ttl_locations = state.ttl_locations if state.big_key_opened else count_locations_exclude_big_chest(state)
    available_small_locations = min(ttl_locations - state.used_locations, state.key_locations - state.used_smalls)
    available_big_locations = ttl_locations - state.used_locations if not state.big_key_special else 0
    if (not smalls_avail or available_small_locations == 0) and (state.big_key_opened or num_bigs == 0 or available_big_locations == 0):
        return False
    else:
        if smalls_avail and available_small_locations > 0:
            for exp_door in state.small_doors:
                state_copy = state.copy()
                open_a_door(exp_door.door, state_copy, flat_proposal)
                state_copy.used_locations += 1
                state_copy.used_smalls += 1
                code = state_id(state_copy, flat_proposal)
                if code not in checked_states.keys():
                    valid = validate_key_layout_sub_loop(state_copy, checked_states, flat_proposal, world, player)
                    checked_states[code] = valid
                else:
                    valid = checked_states[code]
                if not valid:
                    return False
        if not state.big_key_opened and available_big_locations >= num_bigs > 0:
            state_copy = state.copy()
            open_a_door(state.big_doors[0].door, state_copy, flat_proposal)
            state_copy.used_locations += 1
            code = state_id(state_copy, flat_proposal)
            if code not in checked_states.keys():
                valid = validate_key_layout_sub_loop(state_copy, checked_states, flat_proposal, world, player)
                checked_states[code] = valid
            else:
                valid = checked_states[code]
            if not valid:
                return False
    return True


def create_key_counters(key_layout, world, player):
    key_counters = {}
    flat_proposal = key_layout.flat_prop
    state = ExplorationState(dungeon=key_layout.sector.name)
    state.key_locations = len(world.get_dungeon(key_layout.sector.name, player).small_keys)
    state.big_key_special = world.get_region('Hyrule Dungeon Cellblock', player) in key_layout.sector.regions
    for region in key_layout.start_regions:
        state.visit_region(region, key_checks=True)
        state.add_all_doors_check_keys(region, flat_proposal, world, player)
    expand_key_state(state, flat_proposal, world, player)
    code = state_id(state, key_layout.flat_prop)
    key_counters[code] = create_key_counter_x(state, key_layout, world, player)
    queue = collections.deque([(key_counters[code], state)])
    while len(queue) > 0:
        next_key_sphere, parent_state = queue.popleft()
        for door in next_key_sphere.child_doors:
            child_state = parent_state.copy()
            # open the door
            open_a_door(door, child_state, flat_proposal)
            expand_key_state(child_state, flat_proposal, world, player)
            code = state_id(child_state, key_layout.flat_prop)
            if code not in key_counters.keys():
                child_kr = create_key_counter_x(child_state, key_layout, world, player)
                key_counters[code] = child_kr
                queue.append((child_kr, child_state))
    return key_counters


def create_key_counter_x(state, key_layout, world, player):
    key_counter = KeyCounter(key_layout.max_chests)
    key_counter.child_doors.update(dict.fromkeys(unique_doors(state.small_doors+state.big_doors)))
    for loc in state.found_locations:
        if '- Prize' in loc.name or loc.name in ['Agahnim 1', 'Agahnim 2']:
            key_counter.important_location = True
        # todo: zelda's cell is special in standard, and probably crossed too
        elif loc.name in ['Attic Cracked Floor', 'Suspicious Maiden']:
            key_counter.important_location = True
        elif loc.event and 'Small Key' in loc.item.name:
            key_counter.key_only_locations[loc] = None
        elif loc.name not in dungeon_events:
            key_counter.free_locations[loc] = None
    key_counter.open_doors.update(dict.fromkeys(state.opened_doors))
    key_counter.used_keys = count_unique_sm_doors(state.opened_doors)
    if state.big_key_special:
        key_counter.big_key_opened = state.visited(world.get_region('Hyrule Dungeon Cellblock', player))
    else:
        key_counter.big_key_opened = state.big_key_opened
    # if soft_lock_check:
    #     avail_chests = available_chest_small_keys(key_counter, key_counter.big_key_opened, world)
    #     avail_keys = avail_chests + len(key_counter.key_only_locations)
    #     if avail_keys <= key_counter.used_keys and avail_keys < key_layout.max_chests + key_layout.max_drops:
    #         raise SoftLockException()
    return key_counter


def state_id(state, flat_proposal):
    s_id = '1' if state.big_key_opened else '0'
    for d in flat_proposal:
        s_id += '1' if d in state.opened_doors else '0'
    return s_id


def find_counter(opened_doors, bk_hint, key_layout):
    counter = find_counter_hint(opened_doors, bk_hint, key_layout)
    if counter is not None:
        return counter
    more_doors = []
    for door in opened_doors.keys():
        more_doors.append(door)
        if door.dest not in opened_doors.keys():
            more_doors.append(door.dest)
    if len(more_doors) > len(opened_doors.keys()):
        counter = find_counter_hint(dict.fromkeys(more_doors), bk_hint, key_layout)
        if counter is not None:
            return counter
    raise Exception('Unable to find door permutation. Init CID: %s' % counter_id(opened_doors, bk_hint, key_layout.flat_prop))


def find_counter_hint(opened_doors, bk_hint, key_layout):
    cid = counter_id(opened_doors, bk_hint, key_layout.flat_prop)
    if cid in key_layout.key_counters.keys():
        return key_layout.key_counters[cid]
    if not bk_hint:
        cid = counter_id(opened_doors, True, key_layout.flat_prop)
        if cid in key_layout.key_counters.keys():
            return key_layout.key_counters[cid]
    return None


def counter_id(opened_doors, bk_unlocked, flat_proposal):
    s_id = '1' if bk_unlocked else '0'
    for d in flat_proposal:
        s_id += '1' if d in opened_doors.keys() else '0'
    return s_id


# class SoftLockException(Exception):
#     pass


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
    val_rule(key_logic.door_rules['Sewers Secret Room Key Door S'], 3)
    val_rule(key_logic.door_rules['Sewers Dark Cross Key Door N'], 3)
    val_rule(key_logic.door_rules['Hyrule Dungeon Map Room Key Door S'], 2)
    # why is allow_small actually false? - because chest key is forced elsewhere?
    val_rule(key_logic.door_rules['Hyrule Dungeon Armory Interior Key Door N'], 3, True, 'Hyrule Castle - Zelda\'s Chest')
    # val_rule(key_logic.door_rules['Hyrule Dungeon Armory Interior Key Door N'], 4)


def val_eastern(key_logic, world, player):
    val_rule(key_logic.door_rules['Eastern Dark Square Key Door WN'], 2, False, None, 1, {'Eastern Palace - Big Key Chest'})
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
    # val_rule(key_logic.door_rules['Mire Spikes NW'], 3)  # todo: is sometimes 3 or 5? best_counter order matters
    val_rule(key_logic.door_rules['Mire Hub WS'], 5, False, None, 3, mire_west_wing)
    val_rule(key_logic.door_rules['Mire Conveyor Crystal WS'], 6, False, None, 4, mire_west_wing)
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
    val_rule(key_logic.door_rules['GT Double Switch EN'], 6, False, None, 4, rando_room.union({'Ganons Tower - Firesnake Room'}))
    val_rule(key_logic.door_rules['GT Hookshot ES'], 8, True, 'Ganons Tower - Map Chest', 5, {'Ganons Tower - Map Chest'})
    val_rule(key_logic.door_rules['GT Tile Room EN'], 7, False, None, 5, compass_room)
    val_rule(key_logic.door_rules['GT Firesnake Room SW'], 8, False, None, 5, rando_room)
    val_rule(key_logic.door_rules['GT Conveyor Star Pits EN'], 8, False, None, 6, gt_middle)  # should be 7?
    val_rule(key_logic.door_rules['GT Mini Helmasaur Room WN'], 6)  # not sure about 6 this...
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
