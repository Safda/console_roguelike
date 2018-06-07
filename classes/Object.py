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

    def move(self, dx, dy, game_map, objects):
        from classes import Tile as Tile
        
        if not Tile.Tile.blocked(self.x + dx, self.y + dy, game_map, objects):
            self.x += dx
            self.y += dy

    def move_attack(self, dx, dy, game_map, objects):
        from classes import Tile as Tile
        print('x{} y{} dx{} dy{}'.format(self.x, self.y, dx, dy))
        x = self.x + dx
        y = self.y + dy

        target = None
        for object in objects:
            if object.x == x and object.y == y:
                target = object
                break
        if target is not None:
            print('Attacking {} {}'.format(object.name, objects.index(object)))
        else:
            self.move(dx, dy, game_map, objects)
            fov_recompute = True
            return fov_recompute

    def draw(self, con, fov_map):
        con = con
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            libtcod.console_set_default_foreground(con, self.colour)
            libtcod.console_put_char(con, int(self.x), int(self.y), self.char, libtcod.BKGND_NONE)

    def clear(self, con):
        con = con
        libtcod.console_put_char(con, int(self.x), int(self.y), ' ', libtcod.BKGND_NONE)

class Monster(Object):
    pass