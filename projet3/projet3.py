"""
Auteur: Loïc Bernard
Matricule: 000469510
Etudes: B1 Info
Date: 11/11/2018
But: Le but de ce projet est de créer un jeu de labyrinthe dans lequel
un oersonnage doit trouver la sortie (s'il y en a une) du labyrinthe
en longeant le mur soit vers la gauche soit vers la droite
Entrées: le labyrinthe a explorer et la direction dans laquelle l'agent
doit longer le mur
Sorites: Le labyrinthe après chaque avancement de l'agent ainsi que l'interface turtle du labyrinthe et
du chemin suivi pas l'agent
"""
import sys, turtle, time


def square(l, x, y):
    """Cette fonction dessine un carré en utilisant
    le module turtle"""
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    turtle.begin_fill()
    for i in range(1, 5):
        turtle.forward(l)
        turtle.right(90)
    turtle.end_fill()


def print_plateau():
    """Cette fonction imprime le plateau de jeu"""
    for i in plateau:
        for j in i:
            print(j, end = "")

def turn_right():
    """Cette fonction tourne le joueur vers la droite"""
    global agent
    if agent == "^":
        agent = ">"
    elif agent == ">":
        agent = "v"
    elif agent == "v":
        agent = "<"
    elif agent == "<":
        agent = "^"


def turn_left():
    """Cette fonction tourne le joueur vers la gauche"""
    global agent
    if agent == "^":
        agent = "<"
    elif agent == "<":
        agent = "v"
    elif agent == "v":
        agent = ">"
    elif agent == ">":
        agent = "^"


def wall_right(player, mat,i, j):
    """Cette fonction vérifie qu'il y a toujours un mur à droite de l'agent"""
    return (player == "v" and mat[i][j - 1] == "#") or (player == "^" and mat[i][j + 1] == "#") or \
           (player == "<" and mat[i - 1][j] == "#") or (player == ">" and mat[i + 1][j] == "#")


def wall_left(player, mat, i, j):
    """Cette finction vérifie qu'il y a toujours un mur à gauche de l'agent"""
    return (player == "v" and mat[i][j + 1] == "#") or (player == "^" and mat[i][j - 1] == "#") or \
           (player == "<" and mat[i + 1][j] == "#") or (player == ">" and mat[i - 1][j] == "#")


def wall_forward(player, mat, i, j):
    """Cette fontion vérifie qu'il y a toujours un mur en face de l'agenz"""
    return (player == "v" and mat[i + 1][j] == "#") or (player == "^" and mat[i - 1][j] == "#") or \
           (player == "<" and mat[i][j - 1] == "#") or (player == ">" and mat[i][j + 1] == "#")


def forward(mat):
    """Cette fonction fait avancer l'agent de une case"""
    global x, y, pos_agent, agent
    if agent == "v" and mat[y + 1][x] == " ":
        mat[y][x] = " "
        y += 1
        mat[y][x] = agent
    elif agent == "^" and mat[y - 1][x] == " ":
        mat[y][x] = " "
        y -= 1
        mat[y][x] = agent
    elif agent == ">" and mat[y][x + 1] == " ":
        mat[y][x] = " "
        x += 1
        mat[y][x] = agent
    elif agent == "<" and mat[y][x - 1] == " ":
        mat[y][x] = " "
        x -= 1
        mat[y][x] = agent
    pos_agent = (x, y, agent)


MSG_BOUCLE = "Boucle détectée, cases visitées:"
MSG_SORTIE = "Sortie trouvée, cases visitées:"
agent = "v"
visited_pos = []
x = 1
y = 0
play = True
counter = 0
visited_pos1 = []
# ouvre le fichier donné en argument
with open(sys.argv[1]) as f:
    plateau = [[elem for elem in line] for line in f]  # fait une matrice du fichier texte
    plateau[y][x] = agent
    print_plateau()
    print()
    pos_agent = (x, y, agent)
    while play:
        if pos_agent == (len(plateau[0]) - 3, len(plateau) - 1, agent):
            print(MSG_SORTIE)
            visited_pos.append(pos_agent)
            for i in visited_pos:
                visited_pos1.append(i[:2])
            print(visited_pos1)
            play = False
        elif (pos_agent in visited_pos) and counter > 1:
            print(MSG_BOUCLE)
            visited_pos.append(pos_agent)
            for i in visited_pos:
                visited_pos1.append(i[:2])
            print(visited_pos1)
            play = False
        elif sys.argv[2] == "d":
            if wall_right(agent, plateau, y, x) and not wall_forward(agent, plateau, y, x):
                visited_pos.append(pos_agent)
                forward(plateau)
                print_plateau()
                print()
            elif wall_right(agent, plateau, y, x) and wall_forward(agent, plateau, y, x):
                turn_left()
            else:
                visited_pos.append(pos_agent)
                turn_right()
                forward(plateau)
                print_plateau()
                print()
        elif sys.argv[2] == "g":
            if wall_left(agent, plateau, y, x) and not wall_forward(agent, plateau, y, x):
                visited_pos.append(pos_agent)
                forward(plateau)
                print_plateau()
                print()
            elif wall_left(agent, plateau, y, x) and wall_forward(agent, plateau, y, x):
                turn_right()
            else:
                visited_pos.append(pos_agent)
                turn_left()
                forward(plateau)
                print_plateau()
                print()
        counter += 1
        #time.sleep(1)

    # Transforme les tuples dans la liste visited_pos en liste
    i = 0
    while i < len(visited_pos1):
        visited_pos1[i] = list(visited_pos1[i])
        i += 1
    visited_pos1 = [pos[::-1] for pos in visited_pos1]
    for i in range(0, len(visited_pos1)):
        plateau[visited_pos1[i][0]][visited_pos1[i][1]] = "-"
    print_plateau()
    turtle.tracer(0, 0)
    # Affiche le labyrinthe à l'aide du module turtle
    for i in range(0, len(plateau)):
        for j in range(0, len(plateau[0]) - 1):
            if plateau[i][j] == "#":
                square(30, j * 30, i * (-30))
    turtle.up()
    turtle.color("red")
    turtle.width(3)
    turtle.tracer(1, 40)
    turtle.setheading(270)
    # Affiche le trajet de l'agent
    for i in range(0, len(visited_pos1) - 1):
        turtle.goto(visited_pos1[i][1] * 30 + 15, visited_pos1[i][0] * (-30) - 15)
        turtle.down()
        if visited_pos[i][0] < visited_pos[i + 1][0]:
            turtle.setheading(0)
        if visited_pos[i][0] > visited_pos[i + 1][0]:
            turtle.setheading(180)
        if visited_pos[i][1] < visited_pos[i + 1][1]:
            turtle.setheading(270)
        if visited_pos[i][1] > visited_pos[i + 1][1]:
            turtle.setheading(90)
    l = len(visited_pos)
    turtle.goto(visited_pos1[l - 1][1] * 30 + 15, visited_pos1[l - 1][0] * (-30) - 15)


    turtle.exitonclick()
