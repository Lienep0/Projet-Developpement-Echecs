knight_offsets = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]

def compute_knight_masks():
    masks = []
    for i in range(64):
        base = 0
        x = i % 8
        y = i // 8

        for offset in knight_offsets:
            new_x = x + offset[0]
            new_y = y + offset[1]
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                base |= 1 << (new_x + new_y * 8)

        masks.append(base)
    return masks

def compute_sliding_rays(direction):
    masks = []
    for i in range(64):
        base = []
        x = i % 8
        y = i // 8

        new_x = x + direction[0]
        new_y = y + direction[1]
        while 0 <= new_x < 8 and 0 <= new_y < 8:
            base.append(new_x + new_y * 8)
            new_x = new_x + direction[0]
            new_y = new_y + direction[1]

        masks.append(base)
    return masks

def print_valid_positions(startpos, offsets):
    positions = list(map(lambda x: (startpos[0] + x[0], startpos[1] + x[1]), offsets))
    for i in range(8):
        for j in range(8):
            if (i, j) == startpos:
                print("#", end="")
            elif (i, j) in positions:
                print("X", end="")
            else:
                print(".", end="")
        print()

def print_masks(masks):
    for mask in masks:
        l = format(mask, "064b")
        for i in range(8):
            for j in range(8):
                if l[i * 8 + j] == '1':
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print()