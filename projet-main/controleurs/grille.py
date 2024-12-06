from model.model_pg import get_random_brick,  get_instances, insert_joueuse, insert_partie
from datetime import datetime

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
 
    
def change_brique(briques, brique_a_supprimer):
    from model.model_pg import get_random_brick
    print("Original pioche:", briques)
    print("Brique à supprimer:", brique_a_supprimer)

    # Convert brique_a_supprimer to a tuple
    brique_a_supprimer = eval(brique_a_supprimer[0])  # Convert string to tuple
    
    # Iterate through the nested briques
    for i, sublist in enumerate(briques):
        for j, brick in enumerate(sublist):
            if brick == brique_a_supprimer:  # Compare tuples
                print("Brique trouvée:", brick)
                briques[i][j] = get_random_brick(SESSION['CONNEXION'])  # Replace with a new random brick
                print("Nouvelle brique:", briques[i][j])

    print("Pioche mise à jour:", briques)



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



def check_brique(brique_longeur, brique_largeur, liste_coordinates):
    nmbr_briques = len(liste_coordinates)
    if (nmbr_briques !=brique_longeur*brique_largeur):
        print('nmbr_briques !=brique_longeur*brique_largeur')
        return False 
    
    parsed_coordinates = [tuple(map(int, coord.split(","))) for coord in liste_coordinates]
    max_x = max(coord[0] for coord in parsed_coordinates)
    max_y = max(coord[1] for coord in parsed_coordinates)
    min_x = min(coord[0] for coord in parsed_coordinates)
    min_y = min(coord[1] for coord in parsed_coordinates)
    dx = max_x - min_x +1
    dy = max_y - min_y +1
    print(dx, dy)
    if (dx!= brique_longeur) or (dy != brique_largeur):
        print('(dx!= brique_longeur) or (dy != brique_largeur)')
        return False
    if (dx*dy != nmbr_briques):
        print('(dx*dy != nmbr_briques)')
        return False
    return True

REQUEST_VARS['liste_joueuse'] = []
joueueses = get_instances(SESSION['CONNEXION'], 'joueuse')
for i in joueueses:
    REQUEST_VARS['liste_joueuse'].append(i[0])
print(REQUEST_VARS['liste_joueuse'])



print(POST)
if POST and "submit" in POST:

    SESSION['width'] = int(POST["width"][0])
    SESSION['height'] = int(POST["height"][0])

    if "Name" in POST and POST["Name"]:
        SESSION['joueuse'] = POST["Name"]
        insert_joueuse(SESSION['CONNEXION'], SESSION['joueuse'], str(datetime.now()))

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
    if 'date_debut' not in SESSION:
        SESSION['date_debut'] = str(datetime.now())
    print(SESSION['date_debut'])







if POST and "select" in POST:


    if 'score' not in SESSION:
        SESSION['score'] = 0

    # Initialize 'checkedboxes' if not in session
    if 'checkedboxes' not in SESSION:
        SESSION['checkedboxes'] = []

    liste_checkbox  =[]
    # Now append the checked boxes from POST
    if "checkbox" in POST:
        for item in POST["checkbox"]:
            liste_checkbox.append(item)
            #SESSION['checkedboxes'].append(item)
    else:
        print("No checkboxes selected.")
        
    print(SESSION['checkedboxes'])  # Debugging output

    SESSION['selected_brique'] = POST['brique']
    print('This is my brique')
    print (POST['brique'])
    print(SESSION['selected_brique'][0])
    liste_brique = SESSION['selected_brique'][0].split(",")
    longeur = int(liste_brique[1])
    largeur = int(liste_brique[2])
    print(longeur, largeur)

    fit = check_brique( longeur, largeur,liste_checkbox)
    print(fit)
    check_game = True
    if fit:
        for item in POST["checkbox"]:
             if item in SESSION['checkedboxes']:
                check_game = False
                SESSION['selected_brique'] = []
        if check_game:
            SESSION['score'] += 1
            if "checkbox" in POST:
                for item in POST["checkbox"]:
                    SESSION['checkedboxes'].append(item)
            #change selected brique
            change_brique(SESSION['pioche'], POST['brique'])
            #ici si tu gagne 
            if len(SESSION['checkedboxes']) == SESSION['nombre_target'] :
                print("won")
                insert_partie(SESSION['CONNEXION'], SESSION['date_debut'], str(datetime.now()), SESSION['score'],  SESSION['joueuse'], None, None)
                
                
#si tu perts
if POST and "quit" in POST:
   SESSION['score'] = 999
   insert_partie(SESSION['CONNEXION'], SESSION['date_debut'], str(datetime.now()), SESSION['score'],  SESSION['joueuse'], None, None)
   SESSION['score'] = 0
   SESSION['checkedboxes'] = []

   #ici il faut ajouter affichage 

if POST and "change" in POST:
    print('change')
    print(POST['brique'])
    change_brique(SESSION['pioche'], POST['brique'])
    
# REQUEST_VARS['cases'] = POST["checkboxes"]

# print(REQUEST_VARS['cases'])


def trierBriques(liste_coordinates):
    coordonnees_tries = sorted(liste_coordinates, key=lambda coord: (coord[1], coord[0]))
    return coordonnees_tries




    

    

