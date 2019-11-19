import collections

from Regions import dungeon_events
from DungeonGenerator import ExplorationState


class KeyRegion(object):

    def __init__(self):
        self.access_doors = set()
        self.free_locations = []
        self.prize_region = False
        self.key_only_locations = []
        self.child_doors = set()
        self.bk_locked = False
        self.parent_region = None

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


def analyze_dungeon(key_layout, world, player):
    flat_proposal = flatten_pair_list(key_layout.proposal)
    key_regions = create_key_regions(key_layout, flat_proposal, world, player)
    start = key_regions['Origin']


def create_key_regions(key_layout, flat_proposal, world, player):
    key_regions = {}
    state = ExplorationState()
    state.key_locations = len(world.get_dungeon(key_layout.sector.name, player).small_keys)
    state.big_key_special = world.get_region('Hyrule Dungeon Cellblock', player) in key_layout.sector.regions
    for region in key_layout.start_regions:
        state.visit_region(region, key_checks=True)
        state.add_all_doors_check_keys(region, flat_proposal, world, player)
    expand_key_state(state, flat_proposal, world, player)
    key_regions['Origin'] = create_key_region(state, None, None)
    queue = collections.deque([(key_regions['Origin'], state)])
    while len(queue) > 0:
        next_key_region, parent_state = queue.popleft()
        for door in next_key_region.child_doors:
            child_state = parent_state.copy()
            # open the door
            open_a_door(door, child_state, flat_proposal)
            expand_key_state(child_state, flat_proposal, world, player)
            child_kr = create_key_region(child_state, next_key_region, door)
            check_for_duplicates_sub_super_set(key_regions, child_kr, door.name)
            queue.append((child_kr, child_state))
    return key_regions


def check_for_duplicates_sub_super_set(key_regions, new_kr, door_name):
    is_new = True
    for kr in key_regions.values():
        if new_kr == kr:
            kr.access_doors.update(new_kr.access_doors)
            kr.child_doors.update(new_kr.child_doors)
            key_regions[door_name] = kr
            is_new = False
            break
        # if new_kr.issubset(kr):
        #     break
        # if new_kr.issuperset(kr):
        #     break
    if is_new:
        key_regions[door_name] = new_kr


def create_key_region(state, parent_region, door):
    key_region = KeyRegion()
    key_region.parent_region = parent_region
    p_region = parent_region
    parent_doors = set()
    parent_locations = set()
    while p_region is not None:
        parent_doors.update(p_region.child_doors)
        parent_locations.update(p_region.free_locations+p_region.key_only_locations)
        p_region = p_region.parent_region
    u_doors = unique_doors(state.small_doors+state.big_doors).difference(parent_doors)
    key_region.child_doors.update(u_doors)
    region_locations = set(state.found_locations).difference(parent_locations)
    for loc in region_locations:
        if '- Prize' in loc.name or loc.name in ['Agahnim 1', 'Agahnim 2']:
            key_region.prize_region = True
        elif loc.event and 'Small Key' in loc.item.name:
            key_region.key_only_locations.append(loc)
        elif loc.name not in dungeon_events:
            key_region.free_locations.append(loc)
    key_region.bk_locked = state.big_key_opened
    if door is not None:
        key_region.access_doors.add(door)
    return key_region


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


def unique_doors(doors):
    unique_d_set = set()
    for d in doors:
        if d.door not in unique_d_set:
            unique_d_set.add(d.door)
    return unique_d_set


def expand_key_state(state, flat_proposal, world, player):
    while len(state.avail_doors) > 0:
        exp_door = state.next_avail_door()
        door = exp_door.door
        connect_region = world.get_entrance(door.name, player).connected_region
        if state.validate(door, connect_region, world):
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
