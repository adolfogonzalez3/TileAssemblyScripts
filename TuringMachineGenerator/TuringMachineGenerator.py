import sys
print(sys.path)
sys.path.append("Common/")
print(sys.path)
from Tile import Tile

class transition_obj:
    def __init__(self,inputs, place, currentState, nextState, direction):
        self.inputs = inputs
        self.place = place
        self.currentState = currentState
        self.nextState = nextState
        self.direction = direction


def parse(filename):
    transitions = []
    with open(filename, 'rt') as csv:
        for i, line in enumerate(csv):
            if line != '\n':
                line = line.rstrip().split(',')
                for transition in line:
                    a = transition.split('>')
                    b = a[1]
                    a = a[0]
                    inputs = ['{!s}'.format(j) for j in a.split('/')]
                    b = b.split('/')
                    if i == 9:
                        print(b[2])
                    current = 'h_{!s}'.format(i)
                    direction = b[1]
                    nextState = 'h_{!s}'.format(b[2])
                    place = '{!s}'.format(b[0])
                    transitions.append(transition_obj(inputs,place,current,nextState,direction))
            else:
                print("Skipped: {!s}".format(i))
    return transitions

def create_tiles_and_glues(transitions,symbols):
    #glues = [str(i) for i in range(len(transitions))]
    #glues = []
    tiles = []
    strong = []
    weak = []
    for i, tran in enumerate(transitions):
        state = tran.currentState
        nextState = tran.nextState
        if state == 'h_13':
            print(tran.inputs)
        if tran.direction == 'R':
            for a in tran.inputs:
                if tran.place == '_':
                    place = a
                else:
                    place = tran.place
                tiles.append(Tile(place, '{!s}/seq{!s}'.format(state,i),
                            '{!s}/{!s}'.format(state, a), 'BL', str(a)))
                strong.append('{!s}/{!s}'.format(state, a))
                weak.append('{!s}/seq{!s}'.format(state,i))
            for a in symbols:
                tiles.append(Tile('{!s}/{!s}'.format(nextState, a), 'BR', a,
                            '{!s}/seq{!s}'.format(state, i), str(a)))
                strong.append('{!s}/{!s}'.format(nextState, a))
                weak.append('{!s}/seq{!s}'.format(state,i))
        else:
            for a in tran.inputs:
                if tran.place == '_':
                    place = a
                else:
                    place = tran.place
                tiles.append(Tile(place, 'BR', '{!s}/{!s}'.format(state, a),
                            '{!s}/seq{!s}'.format(state,i), str(a)))
                strong.append('{!s}/{!s}'.format(state, a))
                weak.append('{!s}/seq{!s}'.format(state,i))
            for a in symbols:
                tiles.append(Tile('{!s}/{!s}'.format(nextState, a),
                            '{!s}/seq{!s}'.format(state, i), a, 'BL', str(a)))
                strong.append('{!s}/{!s}'.format(nextState, a))
                weak.append('{!s}/seq{!s}'.format(state,i))
    return tiles, set(strong), set(weak)

def write(tiles, glues):
    with open('test.xml', 'wt') as xml:
        xml.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        xml.write('<TileConfiguration>\n')
        xml.write('<GlueFunction>\n')
        for g in glues:
            xml.write('<Function>\n')
            xml.write('<Labels L1="{!s}" L2="{!s}"/>\n'.format(g[0], g[1]))
            xml.write('<Strength>{!s}</Strength>\n'.format(g[2]))
            xml.write('</Function>\n')
        xml.write('</GlueFunction>\n')

        for t in tiles:
            xml.write('<TileType Label="{!s}" Color="00FFFF">\n'.format(t.name))
            xml.write('<Tile>\n')
            xml.write('<Location x="0" y="0"/>\n')
            xml.write('<Color>00FFFF</Color>\n')
            xml.write('<NorthGlue>{!s}</NorthGlue>\n'.format(t.north))
            xml.write('<EastGlue>{!s}</EastGlue>\n'.format(t.east))
            xml.write('<SouthGlue>{!s}</SouthGlue>\n'.format(t.south))
            xml.write('<WestGlue>{!s}</WestGlue>\n'.format(t.west))
            xml.write('<label>{!s}</label>\n'.format(t.name))
            xml.write('</Tile>\n')
            xml.write('<concentration>-1.0</concentration>\n')
            xml.write('<count>-1</count>\n')
            xml.write('</TileType>\n')
        xml.write('</TileConfiguration>\n')

if __name__ == '__main__':
    symbols = ['0', '1', 's0', 's1', '0c', '1c', 'A', '#', 'S']
    transitions = parse('turing_machine.txt')
    tiles, strong, weak = create_tiles_and_glues(transitions,symbols)
    glues = []
    for g in strong:
        glues.append((g,g,2))
    for g in weak:
        glues.append((g,g,1))
    for g in symbols:
        glues.append((g,g,1))
        tiles.append(Tile(g, 'BR', g, 'BR', g))
        tiles.append(Tile(g, 'BL', g, 'BL', g))
    glues.append(('BR','BR',1))
    glues.append(('BL','BL',1))
    tiles.append(Tile('h_0/1', 'seed_0','B','B', '1'))
    tiles.append(Tile('0', 'seed_1','B','seed_0', '0'))
    tiles.append(Tile('1', 'seed_2','B','seed_1', '1'))
    tiles.append(Tile('#', 'seed_3','B','seed_2', '#'))
    tiles.append(Tile('1', 'seed_4','B','seed_3', '1'))
    tiles.append(Tile('1', 'GROWT','B','seed_4', '1'))

    tiles.append(Tile('GROW', 'seed_','B','GROWT', 'GROW'))
    tiles.append(Tile('#', 'GROWT','GROW','BR', '#'))
    glues.append(('GROW','GROW',1))
    glues.append(('GROWT','GROWT',2))
    for i in range(5):
        glues.append(('seed_{!s}'.format(i), 'seed_{!s}'.format(i), 2))

    write(tiles,glues)
