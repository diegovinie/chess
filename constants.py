"Las constantes"

FACTIONS = {
    'whites': {
        'msg': '\nJuegan las blancas\n'
    },
    'blacks': {
        'msg': '\nJuegan las negras\n'
    }
}
PIECES = {
    'pawn': {
        'ltr': 'P',
        'rank': 8,
        'limit': True,
        'onMove': {
            'forward'
        },
        'onAttack': {
            'diagonal'
        }
    },
    'tower': {
        'ltr': 'T',
        'rank': 3,
        'limit': False,
        'onMove': {
            'forward', 'backward', 'side'
        },
        'onAttack': {'front', 'backward', 'side'}
    },
    'horse': {
        'ltr': 'H',
        'rank': 5,
        'limit': True,
        'onMove': {
            'jump'
        },
        'onAttack': {
            'jump'
        }
    },
    'bishop': {
        'ltr': 'B',
        'rank': 4,
        'limit': False,
        'onMove': {
            'diagonal'
        },
        'onAttack': {
            'diagonal'
        }
    },
    'queen': {
        'ltr': 'Q',
        'rank': 2,
        'limit': False,
        'onMove': {
            'forward', 'backward', 'side', 'diagonal'
        },
        'onAttack': {
            'forward', 'backward', 'side', 'diagonal'
        }
    },
    'king': {
        'ltr': 'K',
        'rank': 1,
        'limit': True,
        'onMove': {
            'forward', 'backward', 'side', 'diagonal'
        },
        'onAttack': {
            'forward', 'backward', 'side', 'diagonal'
        },
        'leader': True
    }
}

START_POSITIONS = {
    'whites': {
        (1, 1): 'tower',
        (2, 1): 'horse',
        (3, 1): 'bishop',
        (4, 1): 'queen',
        (5, 1): 'king',
        (6, 1): 'bishop',
        (7, 1): 'horse',
        (8, 1): 'tower'
    },
    'blacks': {
        (1, 8): 'tower',
        (2, 8): 'horse',
        (3, 8): 'bishop',
        (4, 8): 'queen',
        (5, 8): 'king',
        (6, 8): 'bishop',
        (7, 8): 'horse',
        (8, 8): 'tower'
    }
}

for faction, attr in START_POSITIONS.items():
    y = 2 if faction == 'whites' else 7
    attr.update({(x, y): 'pawn' for x in range(1, 9)})
