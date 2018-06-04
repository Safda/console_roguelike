class Room:
    #Rectangle on the map for room creation

    def __init__(self,x,y,w,h):
        self.x1=x
        self.y1=y
        self.x2=x+w
        self.y2=y+h

    def create_room(room,game_map):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                game_map[x][y].blocked = False
                game_map[x][y].block_sight = False

    def create_h_tunnel(x1,x2,y,game_map):
        for x in range( min(x1,x2), max(x2,x2)+1 ):
            game_map[x][y].blocked = False
            game_map[x][y].block_sight = False

    def create_v_tunnel(y1, y2, x, game_map):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            game_map[x][y].blocked = False
            game_map[x][y].block_sight = False

    def center(self):
        center_x = int((self.x1+self.x2)/2)
        center_y = int((self.y1+self.y2)/2)
        return center_x,center_y

    def intersect(self,other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
