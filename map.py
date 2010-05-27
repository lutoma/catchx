TPBUS="bus"
TPTRM="tram"
TPTXI="taxi"
TPSHP="ship"

getmap=lambda: [
    [0, [0045, 0022]],
    [1, [0045, 0022]],
]

getconn=lambda: {
    [0,1]: [[TPBUS, TPTXI], [[60, 246], [84, 268], [200,285], [113,293], [121,300],]],
}
