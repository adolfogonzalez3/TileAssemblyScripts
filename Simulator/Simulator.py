import numpy as np
from multiprocessing import Pool, TimeoutError
import itertools
from time import time
from scipy.signal import convolve2d
from concurrent.futures import ThreadPoolExecutor

class Simulator:
    def __init__(self, tiles, glues, temperature=2, width=32, height=32):
        #self.tiles = tiles
        self.glues = np.array(glues)
        self.N = 2**10
        self.temperature = temperature
        self.area = np.zeros((height, width)).astype(np.int8)
        if type(tiles) is np.ndarray:
            self.npTiles = tiles
        else:
            self.npTiles = np.array([t.glues for t in tiles])
        self.area[-3, 2] = 1

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
            #print(surrounding_glues)
            #input()
            #print(np.repeat(surrounding_glues, 4, axis=0))
            #input()
            #a = self.npTiles != np.repeat(surrounding_glues, 4, axis=0).reshape(surrounding_glues.shape + (4,))
            #print(a.shape)
            #print(self.npTiles.shape)
            #print(np.repeat(self.npTiles, len(a)).reshape(len(a), 4, 4)[a])
            for glue, y, x in zip(surrounding_glues, Y, X):
                candidate_tiles = np.copy(self.npTiles).astype(np.int8)
                #print(candidate_tiles.shape)
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
                #self.print_array()
                self.area[y, x] = tiles[0]




class Tile:
    def __init__(self, north, east, south, west, label=''):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.glues = np.array([north, east, south, west])
        self.label = label

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def create_tiles(N, set_of_labels):
    possible_tiles = itertools.product(range(2), repeat=4)
    #gen = (np.array(i) for i in itertools.combinations(possible_tiles, N))
    count = 0
    for tiles in grouper(itertools.combinations(possible_tiles, N), 100, ((-1,-1,-1,-1),)*4):
        #print(np.shape(tiles))
        for labels in grouper(itertools.product(set_of_labels, repeat=N), 100, (0,)*N):
            #array[:] = tiles
            #n = tiles[0::4]
            #e = tiles[1::4]
            #s = tiles[2::4]
            #w = tiles[3::4]
            #t = [tiles[(4*i):(4*(i+1))] for i in range(int(len(tiles)/4))]
            #tiles = (n, e, s, w)
            #tiles_list = [Tile(n, e, s, w, l) for (n, e, s, w), l in zip(tiles, labels)]
            glues = np.array(labels)
            tiles_list = np.zeros((100, N+1, 4))
            tiles_list[:, 1:, :] = np.array(tiles).reshape((100, N, 4))
            tiles_list.astype(np.int8)
            yield tiles_list, glues
        #yield sum((1 for _ in itertools.combinations_with_replacement(range(N), 4*N)))

def build(tiles, final_assembly):
    seed = tiles[0]
    if seed.label != final_assembly[0,0]:
        return False

def func(tiles):
    s = Simulator(tiles, [i for i in range(3*4)])
    s.build()

if __name__ == '__main__':
    found = False
    number_of_tiles = 4
    N = number_of_tiles
    print('Starting...')
    begin = time()
    print(sum((1 for _ in create_tiles(N, [0, 1]))))
    print('Time Elapsed: {:4.4f}'.format(time()-begin))
    #with ThreadPoolExecutor(max_workers=8) as executor:
    #print('Starting...')
    begin = time()
    array = np.empty((N, 5))
    count = 0
    for tiles, labels in create_tiles(number_of_tiles, [0, 1]):
        #print(tiles.shape)
        for t, l in zip(tiles, labels):
            #print(t)
            #print(g)
            s = Simulator(t, [0, 2])
            s.build()
            count += 1
        s.print_array()
        print()
        #input()
        #print(len(tiles))
        #s = Simulator(tiles, [i for i in range(N*4)])
        #s.build()
        #pass
            #executor.submit(func, tiles)
    print('Time Elapsed: {:4.4f}'.format(time()-begin))
    print(count)
    tiles = []
    glues = [0, 1] + [2]*8
    tiles.append(Tile(0, 0, 0, 0, 'e'))
    tiles.append(Tile(N+1, N+1, 0, 0, 's'))
    tiles.extend([Tile(i+2, N, i+1, 0) for i in range(N, N+4)])
    tiles.extend([Tile(N, i+2, 0, i+1) for i in range(N, N+4)])
    #tiles.append(Tile(1, 1, 1, 1))
    s = Simulator(tiles, glues)
    #for _ in s.build():
    #    s.print_array()
    s.build()
    s.print_array()
