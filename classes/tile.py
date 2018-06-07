class Tile:
    #A single tile on the map and their properties

    def __init__(self, blocked_status, block_sight = None):
        self.blocked = blocked_status

        self.explored = False

        if block_sight is None: block_sight = blocked_status
        self.block_sight = block_sight

    def blocked(x, y, game_map, objects):
        if game_map[x][y].blocked:
            return True
        for blinkybill in objects:
            if blinkybill.blocks and blinkybill.x == x and blinkybill.y == y:
                return True
        return False

    def populate_room(room, game_map, objects):
        import libtcodpy as libtcod
        from classes import Object as Object
        MAX_ROOM_MONSTERS = 2
        num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

        for i in range(num_monsters):
            x = libtcod.random_get_int(0, room.x1, room.x2)
            y = libtcod.random_get_int(0, room.y1, room.y2)
            
            if not Tile.blocked(x, y, game_map, objects):

                if libtcod.random_get_int(0,0,100) < 80:
                    monster = Object.Monster(x, y, '8', 'Orc', libtcod.desaturated_green, True)
                else:
                    monster = Object.Monster(x, y, 'x', 'Troll', libtcod.desaturated_fuchsia, True)
                
                objects.append(monster)

    def make_map(MAP_HEIGHT,MAP_WIDTH,player,objects):
        from classes import Room as Room
        from classes import Object as Object
        import libtcodpy as libtcod
        global game_map
        
        ROOM_MAX_SIZE = 10
        ROOM_MIN_SIZE = 6
        MAX_ROOMS = 30
        rooms = []
        num_rooms = 0

        #fill map with unblocked tiles
        game_map = [[ Tile(True,None)
            for y in range(MAP_HEIGHT) ]
                for x in range(MAP_WIDTH) ]

        for r in range(MAX_ROOMS):
            #random width and height
            w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            #random position without going out of the boundaries of the map
            x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
            y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

            new_room = Room.Room(x, y, w, h)

            if rooms:
                other_room = rooms[num_rooms-1]
            else:
                other_room = Room.Room(0,0,0,0)        

            #run through the other rooms and see if they intersect with this onee
            if not new_room.intersect(other_room):
                #this means there are no intersections, so this room is valid
                #"paint" it to the map's tiles

                Room.Room.create_room(new_room,game_map)
                #center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    #this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y

                else:
                    #all rooms after the first:
                    #connect it to the previous room with a tunnel

                    #center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms-1].center()

                    #draw a coin (random number that is either 0 or 1)
                    if libtcod.random_get_int(0, 0, 1) == 1:
                        #first move horizontally, then vertically
                        Room.Room.create_h_tunnel(prev_x, new_x, prev_y,game_map)
                        Room.Room.create_v_tunnel(prev_y, new_y, new_x,game_map)
                    else:
                        #first move vertically, then horizontally
                        Room.Room.create_v_tunnel(prev_y, new_y, prev_x,game_map)
                        Room.Room.create_h_tunnel(prev_x, new_x, new_y,game_map)

                Tile.populate_room(new_room, game_map, objects)
                #finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        return game_map
