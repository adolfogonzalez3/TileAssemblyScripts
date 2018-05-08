import numpy as np
from scipy.signal import convolve2d


class Simulator:
    def __init__(self, tiles, glues, temperature=2):
        self.tiles = tiles
        self.glues = np.array(glues)
        self.N = 2**4
        self.temperature = temperature
        self.area = np.zeros((2**4, 2**4)).astype(int)
        self.npTiles = np.array([t.glues for t in tiles])
        self.area[-2, 1] = 1

    def print_array(self):
        print(self.area)

    def tile_placing_generator(self):
        '''Generator that outputs locations and tiles that can be placed in the locations.'''
        # Construct a cross shape in order to test if there exists possible
        # spots where a tile may go. This is detected if there are tiles in
        # the north, east, south, or west of the spot
        cross = np.array([[0,1,0],[1,-5,1],[0,1,0]])
        # convolute the cross to determine where these spots occur
        # then get the indices of these spots
        # Use mode valid to get convolutions without padding
        Y, X = np.where(convolve2d(self.area > 0, cross, mode='valid') > 0)
        Y = Y + 1
        X = X + 1
        if len(Y) > 0:
            # Next get the tiles surrounding the candidate spots
            # this is done by creating a len(Y) by 4 vector that contains the
            # y axis indices of the surrounding tiles and creating a len(X) by 4
            # vector that contains the x axis indices of the surrounding tiles
            rows = np.tile([-1, 0, 1, 0], (len(Y), 1))
            columns = np.tile([0, 1, 0, -1], (len(X), 1))
            rows = rows + Y.reshape((-1, 1))
            columns = columns + X.reshape((-1, 1))
            surrounding_tiles = self.area[rows, columns]
            # Get the glues surrounding the candidate spots
            surrounding_glues = self.npTiles[surrounding_tiles, [2, 3, 0, 1]]
            for glue, y, x in zip(surrounding_glues, Y, X):
                candidate_tiles = np.copy(self.npTiles)
                candidate_tiles[self.npTiles != glue] = 0
                strengths = np.sum(self.glues[candidate_tiles], axis=1)
                strengths = np.where(strengths >= self.temperature)[0]
                if len(strengths) > 0:
                    yield (y, x, strengths)



    def build(self):
        building = True
        while building is True:
            building = False
            for y, x, tiles in self.tile_placing_generator():
                building = True
                self.area[y, x] = tiles[0]




class Tile:
    def __init__(self, north, east, south, west, label=''):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.glues = np.array([north, east, south, west])
        self.label = label

def create_tiles(N, labels):
    for l in labels:
        for t in (Tile(i[0],j[1],i[2],i[3], l) for i in
                  itertools.combination_with_replacement(range(36),4)):
            yield [t] + create_tiles(N-1, labels)

def build(tiles, final_assembly):
    seed = tiles[0]
    if seed.label != final_assembly[0,0]:
        return False



if __name__ == '__main__':
    found = False
    number_of_tiles = 1
    #while not found:
    #    for tiles in create_tiles(number_of_tiles, [0, 1]):
    tiles = []
    glues = [0, 1] + [2]*8
    tiles.append(Tile(0, 0, 0, 0, 'e'))
    tiles.append(Tile(2, 2, 0, 0, 's'))
    tiles.extend([Tile(i+3, 1, i+2, 0) for i in range(8)])
    tiles.extend([Tile(1, i+3, 0, i+2) for i in range(8)])
    tiles.append(Tile(1, 1, 1, 1))
    s = Simulator(tiles, glues)
    #for _ in s.build():
    #    s.print_array()
    s.build()
    s.print_array()
