class Object:
    global libtcod
    import libtcodpy as libtcod

    def __init__(self, x, y, char, name, colour, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.colour = colour
        self.blocks = blocks

    def blocked(x, y, game_map, objects):
        if game_map[x][y].blocked:
            return True
        for object in objects:
            if object.blocked and object.x == x and object.y == y:
                return True
        return False

    def move(self, dx, dy, game_map, objects):
        if not Object.blocked(self.x + dx, self.y + dy, game_map, objects):
            self.x += dx
            self.y += dy

    def draw(self, con, fov_map):
        con = con
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_set_default_foreground(con, self.colour)
            libtcod.console_put_char(con, int(self.x), int(self.y), self.char, libtcod.BKGND_NONE)

    def clear(self, con):
        con = con
        libtcod.console_put_char(con, int(self.x), int(self.y), ' ', libtcod.BKGND_NONE)

class Monster(Object):
    global libtcod
    import libtcodpy as libtcod

    def __init__(self):
        super(Monster, self).__init__()

    def populate_room(room,objects):
        MAX_ROOM_MONSTERS = 2
        num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

        for i in range(num_monsters):
            x = libtcod.random_get_int(0, room.x1, room.x2)
            y = libtcod.random_get_int(0, room.y1, room.y2)
            
            if not blocked(x, y):

                if libtcod.random_get_int(0,0,100) < 80:
                    monster = Orc(x, y, '8', 'Orc', libtcod.desaturated_green, True)
                else:
                    monster = Troll(x, y, 'x', 'Troll', libtcod.desaturated_fuchsia, True)
                
                objects.append(monster)

class Orc(Monster):
    type = 'Orc'

    def __init__(self, x, y, char, name, colour, blocks=False):
        self.name = type
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.blocks = blocks

class Troll(Monster):
    type = 'Troll'

    def __init__(self, x, y, char, name, colour, blocks=False):
        self.name = type
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.blocks = blocks