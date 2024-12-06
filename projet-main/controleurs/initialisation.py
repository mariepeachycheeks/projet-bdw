
from model.model_pg import get_random_brick, get_instances, insert_joueuse
import datetime
 
def generate_random_grid(width, height):
    import random
    total_cells = width * height

    # Le nombre de cases cibles est un nombre aléatoire compris entre 10% et 20% du nombre total de cases ;
    num_targets = random.randint(
        int(0.2 * total_cells), int(0.3 * total_cells))

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


 
REQUEST_VARS['liste_joueuse'] = []
joueueses = get_instances(SESSION['CONNEXION'], 'joueuse')
for i in joueueses:
    REQUEST_VARS['liste_joueuse'].append(i[0])
print(REQUEST_VARS['liste_joueuse'])

print(POST)
if POST and "init" in POST:

    SESSION['width'] = int(POST["width"][0])
    SESSION['height'] = int(POST["height"][0])

    if "Name" in POST and POST["Name"]:
        SESSION['joueuse'] = POST["Name"]
       # insert_joueuse(SESSION['CONNEXION'], SESSION['joueuse'], str(datetime.now()))

    elif "joueuses" in POST and POST["joueuses"]:
        SESSION['joueuse'] = POST["joueuses"]

    #print(SESSION['width'], SESSION['height'])

    SESSION['grid'] = generate_random_grid(SESSION['width'], SESSION['height'])
    SESSION['nombre_target'] = 0
    for row in SESSION['grid']:
        for item in row:
            if item == "target":
                SESSION['nombre_target']+=1
    
    print(SESSION['grid'])
    print("Nombre target ")
    print (SESSION['nombre_target'])
    #if 'date_debut' not in SESSION:
       # pass
        #SESSION['date_debut'] = str(datetime.now())
    #print(SESSION['date_debut'])


    SESSION['score'] = 0
    pioche = []

    # Check if 'pioche' is already in the session
    if 'pioche' not in SESSION:
        # Call the get_random_brick function 4 times to get 4 bricks
        for _ in range(4):
            brick = get_random_brick(SESSION['CONNEXION'])  # Fetch one random brick
            pioche.append(brick)  # Add the brick to the list
        
        # Store the list of 4 bricks in the session
        SESSION['pioche'] = pioche

        print(SESSION['pioche'] )

#insert_partie(SESSION['CONNEXION'], SESSION['date_debut'], str(datetime.now()), SESSION['score'],  SESSION['joueuse'], None, None)
