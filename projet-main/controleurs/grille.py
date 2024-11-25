
from model.model_pg import get_instances, get_episodes_for_num


# from controleurs.includes import add_activity


# add_activity(SESSION['HISTORIQUE'], "affichage des données")

'''Fonctionnalité 2'''
'''

REQUEST_VARS['piece'] = get_random_brick(SESSION['CONNEXION'])

 if REQUEST_VARS['piece']  is None:
        logger.warning("Il y a plus de bricks dans BD")
       #return []



initialize_pioche(SESSION['CONNEXION'], 4)

selected_id = REQUEST_VARS['selected_id']

if selected_id:
    REQUEST_VARS['piece'] = replace_selected_brick(
        SESSION['CONNEXION'], selected_id)
else:
    logger.error("Selected brick ID is missing.")
'''

'''pioche = []

REQUEST_VARS['piece']


if b is None:
    logger.warning("Il y a plus de bricks dans BD")
    # return []


if 'pioche' not in SESSION:
    SESSION['pioche'] = get_random_brick(SESSION['CONNEXION'], 4)

    if form_submitted:

        if b in SESSION['pioche']:

            SESSION['pioche'].remove(b)

    SESSION['pioche'].extend(get_random_brick(SESSION['CONNEXION'], 1))'''


def generate_random_grid(width, height):
    import random
    total_cells = width * height

    # Le nombre de cases cibles est un nombre aléatoire compris entre 10% et 20% du nombre total de cases ;
    num_targets = random.randint(
        int(0.1 * total_cells), int(0.2 * total_cells))

    # Initialiser une grille vide
    grid = [["empty" for _ in range(width)] for _ in range(height)]

    # Sélectionner aléatoirement une première case cible ;
    first_target = (random.randint(0, height - 1),
                    random.randint(0, width - 1))
    grid[first_target[0]][first_target[1]] = "target"

    targets = [first_target]
    max_attempts = 100  # Nombre maximal d'essais pour ajouter une nouvelle cible
    attempts = 0

    while len(targets) < num_targets:
        current_target = random.choice(targets)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = current_target[0] + dx
            new_y = current_target[1] + dy

            if 0 <= new_x < height and 0 <= new_y < width and grid[new_x][new_y] == "empty":
                grid[new_x][new_y] = "target"
                targets.append((new_x, new_y))
                break
        else:
            # Si on a essayé toutes les directions sans succès, on incrémente le nombre d'essais
            attempts += 1
            # Si trop d'essais ont échoué, on sort de la boucle
            if attempts >= max_attempts:
                print("Échec de la génération des cibles après plusieurs tentatives.")
                break

    return grid


print(POST)
if POST and "submit" in POST:

    width = int(POST["width"][0])
    height = int(POST["height"][0])

    print(width, height)

    SESSION['grid'] = generate_random_grid(width, height)

    print(SESSION['grid'])

    '''





"""Fonctionnalité 4"""



'
"""''Pour chaque case cible à ajouter, choisir une direction aléatoire(parmi haut, bas, gauche, droite) et vérifier
si la case correspondante(première case cible + direction choisie) est valide(i.e., dans la grille et case
vide): si oui, la transformer en case cible et répéter, sinon choisir une autre direction; '''


'''Gérer les situations exceptionnelles(e.g., pas suffisamment de cases cibles car le motif est en forme de
           # ”spirale”).'''""
