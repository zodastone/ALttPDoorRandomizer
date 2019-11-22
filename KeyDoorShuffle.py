import collections

from Regions import dungeon_events
from Dungeons import dungeon_keys, dungeon_bigs
from DungeonGenerator import ExplorationState


class KeySphere(object):

    def __init__(self):
        self.access_doors = set()
        self.free_locations = []
        self.prize_region = False
        self.key_only_locations = []
        self.child_doors = set()
        self.bk_locked = False
        self.parent_sphere = None

    def __eq__(self, other):
        if self.prize_region != other.prize_region:
            return False
        if self.bk_locked != other.bk_locked:
            return False
        if len(self.free_locations) != len(other.free_locations):
            return False
        if len(self.key_only_locations) != len(other.key_only_locations):
            return False
        if len(set(self.free_locations).difference(set(other.free_locations))) > 0:
            return False
        if len(set(self.key_only_locations).difference(set(other.key_only_locations))) > 0:
            return False
        if not self.check_child_dest(self.child_doors, other.child_doors, other.access_doors):
            return False
        if not self.check_child_dest(other.child_doors, self.child_doors, self.access_doors):
            return False
        return True

    @staticmethod
    def check_child_dest(child_doors, other_child, other_access):
        for child in child_doors:
            if child in other_child:
                continue
            else:
                found = False
                for access in other_access:
                    if access.dest == child:
                        found = True
                        break
                if not found:
                    return False
        return True

    # def issubset(self, other):
    #     if self.prize_region != other.prize_region:
    #         return False
    #     if self.bk_locked != other.bk_locked:
    #         return False
    #     if not set(self.free_locations).issubset(set(other.free_locations)):
    #         return False
    #     if not set(self.key_only_locations).issubset(set(other.key_only_locations)):
    #         return False
    #     if not set(self.child_doors).issubset(set(other.child_doors)):
    #         return False
    #     return True
    #
    # def issuperset(self, other):
    #     if self.prize_region != other.prize_region:
    #         return False
    #     if self.bk_locked != other.bk_locked:
    #         return False
    #     if not set(self.free_locations).issuperset(set(other.free_locations)):
    #         return False
    #     if not set(self.key_only_locations).issuperset(set(other.key_only_locations)):
    #         return False
    #     if not set(self.child_doors).issuperset(set(other.child_doors)):
    #         return False
    #     return True


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


class KeyCounter(object):

    def __init__(self, max_chests):
        self.max_chests = max_chests
        self.free_locations = set()
        self.key_only_locations = set()
        self.child_doors = set()
        self.open_doors = set()
        self.used_keys = 0
        self.big_key_opened = False

    def update(self, key_sphere):
        self.free_locations.update(key_sphere.free_locations)
        self.key_only_locations.update(key_sphere.key_only_locations)
        self.child_doors.update(key_sphere.child_doors)

    def open_door(self, door, flat_proposal):
        if door in flat_proposal:
            self.used_keys += 1
            self.child_doors.remove(door)
            self.open_doors.add(door)
            if door.dest in flat_proposal:
                self.open_doors.add(door.dest)
        elif door.bigKey:
            self.big_key_opened = True
            self.child_doors.remove(door)
            self.open_doors.add(door)

    def used_smalls_loc(self):
        return max(self.used_keys - len(self.key_only_locations), 0)

    def copy(self):
        ret = KeyCounter(self.max_chests)
        ret.free_locations.update(self.free_locations)
        ret.key_only_locations.update(self.key_only_locations)
        ret.child_doors.update(self.child_doors)
        ret.used_keys = self.used_keys
        ret.open_doors.update(self.open_doors)
        return ret


def analyze_dungeon(key_layout, world, player):
    key_layout = KeyLayout(key_layout.sector, key_layout.start_regions, key_layout.proposal)
    key_layout.flat_prop = flatten_pair_list(key_layout.proposal)
    key_layout.key_spheres = create_key_spheres(key_layout, world, player)
    key_logic = key_layout.key_logic
    key_layout.max_chests = len(world.get_dungeon(key_layout.sector.name, player).small_keys)

    find_bk_locked_sections(key_layout)

    key_counter = KeyCounter(key_layout.max_chests)
    key_counter.update(key_layout.key_spheres['Origin'])
    queue = collections.deque([(key_layout.key_spheres['Origin'], key_counter)])

    while len(queue) > 0:
        key_sphere, key_counter = queue.popleft()
        chest_keys = available_chest_small_keys(key_counter, False, world)  # todo: when to count the bk chests
        # chest_keys_bk = available_chest_small_keys(key_counter, True, world)
        available = chest_keys + len(key_counter.key_only_locations) - key_counter.used_keys
        possible_smalls = count_unique_small_doors(key_counter, key_layout.flat_prop)
        # todo: big chest counts?
        if chest_keys == count_locations_big_optional(key_counter.free_locations) and available <= possible_smalls:
            key_logic.bk_restricted.update(key_counter.free_locations)
            # logic min
            if not key_sphere.bk_locked and big_chest_in_locations(key_counter.free_locations):
                key_logic.sm_restricted.update(find_big_chest_locations(key_counter.free_locations))
        # if available <= possible_smalls:
            # in this case, at least 1 child must have the available rule - unless relaxing is possible
        # try to relax the rules here?
        for child in key_sphere.child_doors:
            next_sphere = key_layout.key_spheres[child.name]
            if not empty_sphere(next_sphere):
                if not child.bigKey:
                    # todo: calculate based on big key doors vs smalls - eastern dark square
                    rule = DoorRules(min(available, possible_smalls) + key_counter.used_keys)
                    key_logic.door_rules[child.name] = rule
                next_counter = increment_key_counter(child, next_sphere, key_counter, key_layout.flat_prop)
                queue.append((next_sphere, next_counter))
    return key_layout


    # for child in key_sphere.child_doors:
    #     next_sphere = key_spheres[child.name]
    #     if not empty_sphere(next_sphere):
    #         sm_rule = calc_basic_small_key_rule(key_sphere, key_spheres, key_layout, flat_proposal, world, player)


def find_bk_locked_sections(key_layout):
    key_spheres = key_layout.key_spheres
    key_logic = key_layout.key_logic

    bk_key_not_required = set()
    big_chest_allowed_big_key = True
    for key in key_spheres.keys():
        sphere = key_spheres[key]
        key_layout.all_chest_locations.update(sphere.free_locations)
        if sphere.bk_locked and sphere.prize_region:
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


def increment_key_counter(door, sphere, key_counter, flat_proposal):
    new_counter = key_counter.copy()
    new_counter.open_door(door, flat_proposal)
    new_counter.update(sphere)
    return new_counter


def check_for_big_doors(door, key_counter, key_layout):
    big_doors = set()
    for other in key_counter.child_doors:
        if other != door and other.bigKey:
            big_doors.add(other)
    big_key_available = len(key_counter.free_location) - key_counter.used_smalls_loc > 0
    if len(big_doors) == 0 or not big_key_available:
        return key_counter
    new_counter = key_counter
    for big_door in big_doors:
        big_sphere = key_layout.key_spheres[big_door.name]
        new_counter = increment_key_counter(big_door, big_sphere, new_counter, key_layout.flat_prop)
    # nested big key doors?
    old_counter = None
    while old_counter != new_counter:
        old_counter = new_counter
        new_counter = check_for_big_doors(door, old_counter, key_layout)
    # I think I've opened them all!
    return new_counter


# def calc_basic_small_key_rule(key_sphere, key_spheres, key_layout, flat_proposal, world, player):
#     free_locations = set()
#     key_only_locations = set()
#     offshoot_doors = set()
#     queue = collections.deque()
#     parent = key_sphere.parent_sphere
#     while parent is not None:
#         queue.append(parent)
#         parent = parent.parent_sphere
#     while len(queue) > 0:
#         previous = queue.popleft()
#         free_locations.update(previous.free_locations)
#         key_only_locations.update(previous.key_only_locations)
#         for other_door in parent.child_doors:
#             if other_door not in key_sphere.access_doors:
#                 offshoot_doors.add(other_door)
#     # todo: bk versions
#     chest_keys = available_chest_small_keys(key_layout, free_locations, key_sphere.bk_locked, world, player)
#     parent_avail = chest_keys + len(key_only_locations)
#
#     usuable_elsewhere = 0
#     open_set = set()
#     queue = collections.deque(offshoot_doors)
#     while len(queue) > 0:
#         offshoot = queue.popleft()
#         open_set.add(offshoot)
#         if offshoot in flat_proposal:
#             usuable_elsewhere += 1
#         # else bk door
#         if offshoot.dest in flat_proposal:
#             open_set.add(offshoot.dest)
#         off_sphere = key_spheres[offshoot.name]
#         free_locations.update(off_sphere.free_locations)
#         key_only_locations.update(off_sphere.key_only_locations)
#         for other_door in off_sphere.child_doors:
#             if other_door not in key_sphere.access_doors and other_door not in open_set:
#                 queue.append(other_door)
#     # todo: bk versions
#     offshoot_chest = available_chest_small_keys(key_layout, free_locations, key_sphere.bk_locked, world, player)
#     offshoot_avail = offshoot_chest + len(key_only_locations)
#
#     if usuable_elsewhere == parent_avail and offshoot_avail > parent_avail:
#         return usuable_elsewhere + 1
#     if usuable_elsewhere == parent_avail and offshoot_avail == parent_avail:
#         return usuable_elsewhere
#     if usuable_elsewhere < parent_avail:
#         return usuable_elsewhere + 1
#     return 10


def available_chest_small_keys(key_counter, bk, world):
    if not world.keysanity and world.mode != 'retro':
        cnt = 0
        for loc in key_counter.free_locations:
            if bk or '- Big Chest' not in loc.name:
                cnt += 1
        return min(cnt, key_counter.max_chests)
    else:
        return key_counter.max_chests

    # derive key rules from key regions
    #   how many small key available at a given point (locations found / keysanity / retro)
    #   how many doors can be opened before you vs. smalls available
    #     soft lock detection - should it be run here?
    #   run with both bk off (locked behind current door) and bk found (elsewhere in the dungeon)
    #     rules generally smaller if bk locked behind current door
    #   big key restriction based on bk_locked
    #   prize regions - TT is weird as there are intermediate goals - assume child doors as well?


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
            check_for_duplicates_sub_super_set(key_spheres, child_kr, door.name)
            queue.append((child_kr, child_state))
    return key_spheres


def check_for_duplicates_sub_super_set(key_spheres, new_kr, door_name):
    is_new = True
    for kr in key_spheres.values():
        if new_kr == kr:  # todo: what about parent regions...
            kr.access_doors.update(new_kr.access_doors)
            kr.child_doors.update(new_kr.child_doors)
            key_spheres[door_name] = kr
            is_new = False
            break
        # if new_kr.issubset(kr):
        #     break
        # if new_kr.issuperset(kr):
        #     break
    if is_new:
        key_spheres[door_name] = new_kr


def create_key_sphere(state, parent_sphere, door):
    key_sphere = KeySphere()
    key_sphere.parent_sphere = parent_sphere
    p_region = parent_sphere
    parent_doors = set()
    parent_locations = set()
    while p_region is not None:
        parent_doors.update(p_region.child_doors)
        parent_locations.update(p_region.free_locations+p_region.key_only_locations)
        p_region = p_region.parent_sphere
    u_doors = unique_doors(state.small_doors+state.big_doors).difference(parent_doors)
    key_sphere.child_doors.update(u_doors)
    region_locations = set(state.found_locations).difference(parent_locations)
    for loc in region_locations:
        if '- Prize' in loc.name or loc.name in ['Agahnim 1', 'Agahnim 2']:
            key_sphere.prize_region = True
        elif loc.event and 'Small Key' in loc.item.name:
            key_sphere.key_only_locations.append(loc)
        elif loc.name not in dungeon_events:
            key_sphere.free_locations.append(loc)
    # todo: Cellblock in a dungeon with a big_key door or chest - Crossed Mode
    key_sphere.bk_locked = state.big_key_opened if not state.big_key_special else False
    if door is not None:
        key_sphere.access_doors.add(door)
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


## vanilla validation code

def validate_vanilla_key_logic(world, player):
    validators = {
        'Hyrule Castle': val_unimplemented,
        'Eastern Palace': val_eastern,
        'Desert Palace': val_desert,
        'Tower of Hera': val_hera,
        'Agahnims Tower': val_tower,
        'Palace of Darkness': val_unimplemented,
        'Swamp Palace': val_unimplemented,
        'Skull Woods': val_unimplemented,
        'Thieves Town': val_unimplemented,
        'Ice Palace': val_unimplemented,
        'Misery Mire': val_unimplemented,
        'Turtle Rock': val_unimplemented,
        'Ganons Tower': val_unimplemented
    }
    key_logic_dict = world.key_logic[player]
    for key, key_logic in key_logic_dict.items():
        validators[key](key_logic)


def val_unimplemented(key_logic):
    assert True


def val_eastern(key_logic):
    dark_square_rule = key_logic.door_rules['Eastern Dark Square Key Door WN']
    assert dark_square_rule.small_key_num == 2
    # todo: allow big_key behind the door
    # assert dark_square_rule.alternate_small_key == 1
    # assert 'Eastern Palace - Big Key Chest' in dark_square_rule.alternat_big_key_loc
    # assert len(dark_square_rule.alternat_big_key_loc) == 1
    assert key_logic.door_rules['Eastern Darkness Up Stairs'].small_key_num == 2
    assert 'Eastern Palace - Big Chest' in key_logic.bk_restricted
    assert 'Eastern Palace - Boss' in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 2


def val_desert(key_logic):
    assert key_logic.door_rules['Desert East Wing Key Door EN'].small_key_num == 2
    assert key_logic.door_rules['Desert Tiles 1 Up Stairs'].small_key_num == 2
    assert key_logic.door_rules['Desert Beamos Hall NE'].small_key_num == 3
    assert key_logic.door_rules['Desert Tiles 2 NE'].small_key_num == 4
    assert 'Desert Palace - Big Chest' in key_logic.bk_restricted
    assert 'Desert Palace - Boss' in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 2


def val_hera(key_logic):
    assert key_logic.door_rules['Hera Lobby Key Stairs'].small_key_num == 1
    assert 'Tower of Hera - Big Chest' in key_logic.bk_restricted
    assert 'Tower of Hera - Compass Chest' in key_logic.bk_restricted
    assert 'Tower of Hera - Boss' in key_logic.bk_restricted
    assert len(key_logic.bk_restricted) == 3


def val_tower(key_logic):
    assert key_logic.door_rules['Tower Room 03 Up Stairs'].small_key_num == 1
    assert key_logic.door_rules['Tower Dark Maze ES'].small_key_num == 2
    assert key_logic.door_rules['Tower Dark Chargers Up Stairs'].small_key_num == 3
    assert key_logic.door_rules['Tower Circle of Pots WS'].small_key_num == 4
