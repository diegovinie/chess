# -*- coding: utf-8 -*-

"""Juego de ajedrés.
Para iniciar una partida:
    from chess import mainloop
    mainloop()

Movimientos: forward (peón, torre, reina, rey) => steps
    backward (torre, reina, rey) => steps
    aside (torre, reina, rey) => (left|right) steps
    diagonal (alfil, reina, rey, peón al atacar) => (NW|NE|SE|SW) steps
    jump (caballo) => (NW|NE|EN|ES|SE|SW|WS|WN)
"""

import random
import sys
import constants

class Piece(object):
    "Las piezas del juego."

    def __init__(self, pos, faction, kind):
        kindattr = constants.PIECES[kind]
        self.faction = faction
        self.start = False
        self.kind = kind
        self.pos = pos
        self.fac = 'w' if faction == 'whites' else 'b'
        self.ltr = kindattr['ltr']
        self.move = kindattr['onMove']
        self.attack = kindattr['onAttack']    

    def forward(self, steps, backward=False):
        """Mueve la pieza hacia el frente.
        param: (int) pasos, (bool) retroceso"""

        vdirec = -1 if bool(backward) else 1
        direc = 1 if self.faction == 'whites' else -1
        for _ in range(int(steps)):
            yield sumtuples(self.pos, (0, vdirec*direc))

    def backward(self, steps):
        """Mueve la pieza hacia atrás. Envoltura para forward"""
        return self.forward(int(steps), True)

    def aside(self, side, steps):
        """Mueve la pieza hacia un lado.
        param: (str) dirección
        devuelve: yield"""

        direc = 1 if side.lower() == 'right' else -1
        tranpos = self.pos

        for _ in range(int(steps)):
            yield sumtuples(tranpos, (direc*steps, 0))

    def diagonal(self, *args):
        """Mueve la pieza en diagonal.
        params: (str) dirección, (int) pasos
        devuelve: yield"""

        diag, steps = args
        direc = {
            'NE': (1, 1),
            'SE': (1, -1),
            'SW': (-1, -1),
            'NW': (-1, 1)
        }.get(diag.upper(), False)

        tranpos = self.pos
        for _ in range(int(steps)):
            tranpos = sumtuples(tranpos, direc)
            yield tranpos

    def jump(self, direction):
        """Mueve el caballo.
        param: (str) dirección
        devuelve: yield"""

        tranpos = self.pos
        direc, frst, scnd = {
            "NW": ('v', 2, -1),
            'NE': ('v', 2, 1),
            'EN': ('h', 2, 1),
            'ES': ('h', 2, -1),
            'SE': ('v', -2, 1),
            'SW': ('v', -2, -1),
            'WS': ('h', -2, -1),
            'WN': ('h', -2, -1)
            }.get(direction.upper(), False)

        newpos = (frst, scnd) if direc == 'h' else (scnd, frst)
        yield sumtuples(tranpos, newpos)

class TableBoard(object):
    "Tablero."

    def __init__(self, options=None):
        self.options = options
        self.tiles = {(x, y): None for x in range(1, 9) for y in range(1, 9)}
        return

    def set_piece(self, piece, pos):
        "Coloca una pieza."
        self.tiles[pos] = piece
        return

    def checkmov(self, piece, newpos):
        """Si la nueva pos está en Tiles la ejecuta.
        param: (Piece), (duple) nueva posición
        devuelve: (bool)"""

        ntile_cont = self.tiles[newpos]
        enemy = isinstance(ntile_cont, Piece) and ntile_cont.faction != piece.faction

        if newpos in self.tiles:
            if ntile_cont is None:
                self.tiles[piece.pos] = None
                self.tiles[newpos] = piece
                piece.pos = newpos
                return True
            elif enemy:
                self.tiles[piece.pos] = None
                self.tiles[newpos] = piece
                piece.pos = newpos
                piece.active = False
                print "%s (%s) eliminado." % (ntile_cont.kind, ntile_cont.faction)
                return True
            else:
                print "Movimiento no posible."
                return False
        else:
            print "Movimiento fuera del tablero."
            return False

    def show(self):
        "Imprime las posiciones."
        for tile, val in self.tiles.items():
            if isinstance(val, Piece):
                print "%s (%s) en %s" % (val.kind, val.faction, tile)

    def show_graph(self):
        "Imprime el tablero."

        for ypos in reversed(range(1, 9)):
            line = ''
            for xpos in range(1, 9):
                piec = self.tiles[xpos, ypos]
                if isinstance(piec, Piece):
                    line += " " + piec.ltr + piec.fac + " "
                else:
                    line += " -- "
            print line
            print

class Game(TableBoard):
    "El juego."

    def __init__(self):
        super(self.__class__, self).__init__()
        self.deploy()
        self.list = {}

    def deploy(self):
        "Pone las piezas en el tablero."

        for faction, combo in constants.START_POSITIONS.items():
            for pos, name in combo.items():
                piece = Piece(pos, faction, name)
                self.set_piece(piece, piece.pos)

    def get_piece(self, pos):
        """Devuelve una pieza según la posición.
        param: (tuple) posición
        devuelve: (Piece)|(bool) La pieza o falso"""

        piece = self.tiles[pos]
        if isinstance(piece, Piece):
            return piece
        else:
            return False

    def move(self, piece, method_name, *args):
        """Mueve la pieza en el tablero.
        params: (Piece) la pieza, (str) la acción, lista de argumentos
        devuelve: (bool)"""

        if method_name not in piece.move:
            print "%s no permitido para %s" % (method_name, piece.kind)
            return False

        action = {
            'forward': Piece.forward,
            'backward': Piece.backward,
            'aside': Piece.aside,
            'diagonal': Piece.diagonal,
            'jump': Piece.jump
            }.get(method_name, None)

        movs = action(piece, *args)
        success = False

        for newpos in movs:
            if self.checkmov(piece, newpos) is False:
                break
            success = True

        return success

    def getlist(self, faction):
        """Devuelve la lista de piezas.
        param: (str) facción
        devuelve: (dic) lista de piezas para mover."""

        self.list = {}
        i = 0
        for pos, val in self.tiles.items():            
            if isinstance(val, Piece) and val.faction == faction:
                i += 1
                print "%s %s %s" % (i, val.kind, pos)
                self.list[i] = pos
        return self.list


def sumtuples(frst, scnd):
    "Suma dos tuplas."
    return tuple(sum(x) for x in zip(frst, scnd))

def multuples(tup, mult):
    "Multiplica dos tuplas."
    return tuple(mult * x for x in tup)

def change(faction):
    "Cambia de facción."
    return 'blacks' if faction == 'whites' else 'whites'

def mainloop():
    "Main loop."

    game = Game()

    faction = 'whites'
    while True:
        print constants.FACTIONS[faction]['msg']
        game.show_graph()
        lis = game.getlist(faction)

        res = False
        while not res:
            sel = raw_input('Seleccione pieza (<q> para salir): ')

            if str(sel) == 'q':
                print "\nSaliendo de la partida."
                sys.exit()
            try:
                pie = game.get_piece(lis[int(sel)])
            except ValueError:
                print "Comando no reconocido."
                continue
            except KeyError:
                print "selector %s no reconocido" % sel
                continue
            print "'%s' en %s" % (pie.kind, pie.pos)
            mov = raw_input("Seleccione jugada (<b> para retroceder): ")
            if str(mov) == 'b':
                continue
            instr = raw_input("Instrucciones: ")

            try:
                res = game.move(pie, mov, *tuple(instr.split()))
            except ValueError:
                print "Acción no permitida."

        faction = change(faction)


