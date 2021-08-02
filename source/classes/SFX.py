import random
from Utils import int16_as_bytes


class SFX(object):

    def __init__(self, name, sfx_set, orig_id, addr, chain, accomp=False):
        self.name = name
        self.sfx_set = sfx_set
        self.orig_id = orig_id
        self.addr = addr
        self.chain = chain
        self.accomp = accomp

        self.target_set = None
        self.target_id = None
        self.target_chain = None


def init_sfx_data():
    sfx_pool = [SFX('Slash1', 0x02, 0x01, 0x2614, []), SFX('Slash2', 0x02, 0x02, 0x2625, []),
                SFX('Slash3', 0x02, 0x03, 0x2634, []), SFX('Slash4', 0x02, 0x04, 0x2643, []),
                SFX('Wall clink', 0x02, 0x05, 0x25DD, []), SFX('Bombable door clink', 0x02, 0x06, 0x25D7, []),
                SFX('Fwoosh shooting', 0x02, 0x07, 0x25B7, []), SFX('Arrow hitting wall', 0x02, 0x08, 0x25E3, []),
                SFX('Boomerang whooshing', 0x02, 0x09, 0x25AD, []), SFX('Hookshot', 0x02, 0x0A, 0x25C7, []),
                SFX('Placing bomb', 0x02, 0x0B, 0x2478, []),
                SFX('Bomb exploding/Quake/Bombos/Exploding wall', 0x02, 0x0C, 0x269C, []),
                SFX('Powder', 0x02, 0x0D, 0x2414, [0x3f]), SFX('Fire rod shot', 0x02, 0x0E, 0x2404, []),
                SFX('Ice rod shot', 0x02, 0x0F, 0x24C3, []), SFX('Hammer use', 0x02, 0x10, 0x23FA, []),
                SFX('Hammering peg', 0x02, 0x11, 0x23F0, []), SFX('Digging', 0x02, 0x12, 0x23CD, []),
                SFX('Flute use', 0x02, 0x13, 0x23A0, [0x3e]), SFX('Cape on', 0x02, 0x14, 0x2380, []),
                SFX('Cape off/Wallmaster grab', 0x02, 0x15, 0x2390, []), SFX('Staircase', 0x02, 0x16, 0x232C, []),
                SFX('Staircase', 0x02, 0x17, 0x2344, []), SFX('Staircase', 0x02, 0x18, 0x2356, []),
                SFX('Staircase', 0x02, 0x19, 0x236E, []), SFX('Tall grass/Hammer hitting bush', 0x02, 0x1A, 0x2316, []),
                SFX('Mire shallow water', 0x02, 0x1B, 0x2307, []), SFX('Shallow water', 0x02, 0x1C, 0x2301, []),
                SFX('Lifting object', 0x02, 0x1D, 0x22BB, []), SFX('Cutting grass', 0x02, 0x1E, 0x2577, []),
                SFX('Item breaking', 0x02, 0x1F, 0x22E9, []), SFX('Item falling in pit', 0x02, 0x20, 0x22DA, []),
                SFX('Bomb hitting ground/General bang', 0x02, 0x21, 0x22CF, []),
                SFX('Pushing object/Armos bounce', 0x02, 0x22, 0x2107, []), SFX('Boots dust', 0x02, 0x23, 0x22B1, []),
                SFX('Splashing', 0x02, 0x24, 0x22A5, [0x3d]), SFX('Mire shallow water again?', 0x02, 0x25, 0x2296, []),
                SFX('Link taking damage', 0x02, 0x26, 0x2844, []), SFX('Fainting', 0x02, 0x27, 0x2252, []),
                SFX('Item splash', 0x02, 0x28, 0x2287, []), SFX('Rupee refill', 0x02, 0x29, 0x243F, [0x3b]),
                SFX('Fire rod shot hitting wall/Bombos spell', 0x02, 0x2A, 0x2033, []),
                SFX('Heart beep/Text box', 0x02, 0x2B, 0x1FF2, []), SFX('Sword up', 0x02, 0x2C, 0x1FD9, [0x3a]),
                SFX('Magic drain', 0x02, 0x2D, 0x20A6, []), SFX('GT opening', 0x02, 0x2E, 0x1FCA, [0x39]),
                SFX('GT opening/Water drain', 0x02, 0x2F, 0x1F47, [0x38]), SFX('Cucco', 0x02, 0x30, 0x1EF1, []),
                SFX('Fairy', 0x02, 0x31, 0x20CE, []), SFX('Bug net', 0x02, 0x32, 0x1D47, []),
                SFX('Teleport2', 0x02, 0x33, 0x1CDC, [], True), SFX('Teleport1', 0x02, 0x34, 0x1F6F, [0x33]),
                SFX('Quake/Vitreous/Zora king/Armos/Pyramid/Lanmo', 0x02, 0x35, 0x1C67, [0x36]),
                SFX('Mire entrance (extends above)', 0x02, 0x36, 0x1C64, [], True),
                SFX('Spin charged', 0x02, 0x37, 0x1A43, []), SFX('Water sound', 0x02, 0x38, 0x1F6F, [], True),
                SFX('GT opening thunder', 0x02, 0x39, 0x1F9C, [], True), SFX('Sword up', 0x02, 0x3A, 0x1FE7, [], True),
                SFX('Quiet rupees', 0x02, 0x3B, 0x2462, [], True), SFX('Error beep', 0x02, 0x3C, 0x1A37, []),
                SFX('Big splash', 0x02, 0x3D, 0x22AB, [], True), SFX('Flute again', 0x02, 0x3E, 0x23B5, [], True),
                SFX('Powder paired', 0x02, 0x3F, 0x2435, [], True),

                SFX('Sword beam', 0x03, 0x01, 0x1A18, []),
                SFX('TR opening', 0x03, 0x02, 0x254E, []), SFX('Pyramid hole', 0x03, 0x03, 0x224A, []),
                SFX('Angry soldier', 0x03, 0x04, 0x220E, []), SFX('Lynel shot/Javelin toss', 0x03, 0x05, 0x25B7, []),
                SFX('BNC swing/Phantom ganon/Helma tail/Arrghus swoosh', 0x03, 0x06, 0x21F5, []),
                SFX('Cannon fire', 0x03, 0x07, 0x223D, []), SFX('Damage to enemy; $0BEX.4=1', 0x03, 0x08, 0x21E6, []),
                SFX('Enemy death', 0x03, 0x09, 0x21C1, []), SFX('Collecting rupee', 0x03, 0x0A, 0x21A9, []),
                SFX('Collecting heart', 0x03, 0x0B, 0x2198, []),
                SFX('Non-blank text character', 0x03, 0x0C, 0x218E, []),
                SFX('HUD heart (used explicitly by sanc heart?)', 0x03, 0x0D, 0x21B5, []),
                SFX('Opening chest', 0x03, 0x0E, 0x2182, []),
                SFX('♪Do do do doooooo♫', 0x03, 0x0F, 0x24B9, [0x3C, 0x3D, 0x3E, 0x3F]),
                SFX('Opening/Closing map (paired)', 0x03, 0x10, 0x216D, [0x3b]),
                SFX('Opening item menu/Bomb shop guy breathing', 0x03, 0x11, 0x214F, []),
                SFX('Closing item menu/Bomb shop guy breathing', 0x03, 0x12, 0x215E, []),
                SFX('Throwing object (sprites use it as well)/Stalfos jump', 0x03, 0x13, 0x213B, []),
                SFX('Key door/Trinecks/Dash key landing/Stalfos Knight collapse', 0x03, 0x14, 0x246C, []),
                SFX('Door closing/OW door opening/Chest opening (w/ $29 in $012E)', 0x03, 0x15, 0x212F, []),
                SFX('Armos Knight thud', 0x03, 0x16, 0x2123, []), SFX('Rat squeak', 0x03, 0x17, 0x25A6, []),
                SFX('Dragging/Mantle moving', 0x03, 0x18, 0x20DD, []),
                SFX('Fireball/Laser shot; Somehow used by Trinexx???', 0x03, 0x19, 0x250A, []),
                SFX('Chest reveal jingle ', 0x03, 0x1A, 0x1E8A, [0x38]),
                SFX('Puzzle jingle', 0x03, 0x1B, 0x20B6, [0x3a]), SFX('Damage to enemy', 0x03, 0x1C, 0x1A62, []),
                SFX('Potion refill/Magic drain', 0x03, 0x1D, 0x20A6, []),
                SFX('Flapping (Duck/Cucco swarm/Ganon bats/Keese/Raven/Vulture)', 0x03, 0x1E, 0x2091, []),
                SFX('Link falling', 0x03, 0x1F, 0x204B, []), SFX('Menu/Text cursor moved', 0x03, 0x20, 0x276C, []),
                SFX('Damage to boss', 0x03, 0x21, 0x27E2, []), SFX('Boss dying/Deleting file', 0x03, 0x22, 0x26CF, []),
                SFX('Spin attack/Medallion swoosh', 0x03, 0x23, 0x2001, [0x39]),
                SFX('OW map perspective change', 0x03, 0x24, 0x2043, []),
                SFX('Pressure switch', 0x03, 0x25, 0x1E9D, []),
                SFX('Lightning/Game over/Laser/Ganon bat/Trinexx lunge', 0x03, 0x26, 0x1E7B, []),
                SFX('Agahnim charge', 0x03, 0x27, 0x1E40, []), SFX('Agahnim/Ganon teleport', 0x03, 0x28, 0x26F7, []),
                SFX('Agahnim shot', 0x03, 0x29, 0x1E21, []),
                SFX('Somaria/Byrna/Ether spell/Helma fire ball', 0x03, 0x2A, 0x1E12, []),
                SFX('Electrocution', 0x03, 0x2B, 0x1DF3, []), SFX('Bees', 0x03, 0x2C, 0x1DC0, []),
                SFX('Milestone, also via text', 0x03, 0x2D, 0x1DA9, [0x37]),
                SFX('Collecting heart container', 0x03, 0x2E, 0x1D5D, [0x35, 0x34]),
                SFX('Collecting absorbable key', 0x03, 0x2F, 0x1D80, [0x33]),
                SFX('Byrna spark/Item plop/Magic bat zap/Blob emerge', 0x03, 0x30, 0x1B53, []),
                SFX('Sprite falling/Moldorm shuffle', 0x03, 0x31, 0x1ACA, []),
                SFX('Bumper boing/Somaria punt/Blob transmutation/Sprite boings', 0x03, 0x32, 0x1A78, []),
                SFX('Jingle (paired $2F→$33)', 0x03, 0x33, 0x1D93, [], True),
                SFX('Depressing jingle (paired $2E→$35→$34)', 0x03, 0x34, 0x1D66, [], True),
                SFX('Ugly jingle (paired $2E→$35→$34)', 0x03, 0x35, 0x1D73, [], True),
                SFX('Wizzrobe shot/Helma fireball split/Mothula beam/Blue balls', 0x03, 0x36, 0x1AA7, []),
                SFX('Dinky jingle (paired $2D→$37)', 0x03, 0x37, 0x1DB4, [], True),
                SFX('Apathetic jingle (paired $1A→$38)', 0x03, 0x38, 0x1E93, [], True),
                SFX('Quiet swish (paired $23→$39)', 0x03, 0x39, 0x2017, [], True),
                SFX('Defective jingle (paired $1B→$3A)', 0x03, 0x3A, 0x20C0, [], True),
                SFX('Petulant jingle (paired $10→$3B)', 0x03, 0x3B, 0x2176, [], True),
                SFX('Triumphant jingle (paired $0F→$3C→$3D→$3E→$3F)', 0x03, 0x3C, 0x248A, [], True),
                SFX('Less triumphant jingle ($0F→$3C→$3D→$3E→$3F)', 0x03, 0x3D, 0x2494, [], True),
                SFX('"You tried, I guess" jingle (paired $0F→$3C→$3D→$3E→$3F)', 0x03, 0x3E, 0x249E, [], True),
                SFX('"You didn\'t really try" jingle (paired $0F→$3C→$3D→$3E→$3F)', 0x03, 0x3F, 0x2480, [], True)]
    return sfx_pool


def shuffle_sfx_data():
    sfx_pool = init_sfx_data()
    sfx_map = {2: {}, 3: {}}
    accompaniment_map = {2: set(), 3: set()}
    candidates = []
    for sfx in sfx_pool:
        sfx_map[sfx.sfx_set][sfx.orig_id] = sfx
        if not sfx.accomp:
            candidates.append((sfx.sfx_set, sfx.orig_id))
        else:
            accompaniment_map[sfx.sfx_set].add(sfx.orig_id)
    chained_sfx = [x for x in sfx_pool if len(x.chain) > 0]

    random.shuffle(candidates)

    # place chained sfx first
    random.shuffle(chained_sfx) # todo: sort largest to smallest
    chained_sfx = sorted(chained_sfx, key=lambda x: len(x.chain), reverse=True)
    for chained in chained_sfx:
        chosen_slot = next(x for x in candidates if len(accompaniment_map[x[0]]) - len(chained.chain) >= 0)
        if chosen_slot is None:
            raise Exception('Something went wrong with sfx chains')
        chosen_set, chosen_id = chosen_slot
        chained.target_set, chained.target_id = chosen_slot
        chained.target_chain = []
        for downstream in chained.chain:
            next_slot = accompaniment_map[chosen_set].pop()
            ds_acc = sfx_map[chained.sfx_set][downstream]
            ds_acc.target_set, ds_acc.target_id = chosen_set, next_slot
            chained.target_chain.append(next_slot)
        candidates.remove(chosen_slot)
        sfx_pool.remove(chained)

    unchained_sfx = [x for x in sfx_pool if not x.accomp]
    # do the rest
    for sfx in unchained_sfx:
        chosen_slot = candidates.pop()
        sfx.target_set, sfx.target_id = chosen_slot

    return sfx_map


sfx_table = {
    2: 0x1a8c29,
    3: 0x1A8D25
}

# 0x1a8c29
# d8059

sfx_accompaniment_table = {
    2: 0x1A8CA7,
    3: 0x1A8DA3
}


def randomize_sfx(rom):
    sfx_map = shuffle_sfx_data()

    for shuffled_sfx in sfx_map.values():
        for sfx in shuffled_sfx.values():
            base_address = sfx_table[sfx.target_set]
            rom.write_bytes(base_address + (sfx.target_id * 2) - 2, int16_as_bytes(sfx.addr))
            ac_base = sfx_accompaniment_table[sfx.target_set]
            last = sfx.target_id
            if sfx.target_chain:
                for chained in sfx.target_chain:
                    rom.write_byte(ac_base + last - 1, chained)
                    last = chained
            rom.write_byte(ac_base + last - 1, 0)









