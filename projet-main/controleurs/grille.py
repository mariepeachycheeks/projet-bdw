
from model.model_pg import get_instances, get_episodes_for_num


pioche = []

# Check if 'pioche' is already in the session
if 'pioche' not in SESSION:
    # Call the get_random_brick function 4 times to get 4 bricks
    for _ in range(4):
        brick = get_random_brick(SESSION['CONNEXION'])  # Fetch one random brick
        pioche.append(brick)  # Add the brick to the list
    
    # Store the list of 4 bricks in the session
    SESSION['pioche'] = pioche
 
    



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


print(POST)
if POST and "submit" in POST:

    SESSION['width'] = int(POST["width"][0])
    SESSION['height'] = int(POST["height"][0])

    print(SESSION['width'], SESSION['height'])

    SESSION['grid'] = generate_random_grid(SESSION['width'], SESSION['height'])

    print(SESSION['grid'])

if POST and "play" in POST:
    # Initialize 'checkedboxes' if not in session
    if 'checkedboxes' not in SESSION:
        SESSION['checkedboxes'] = []
    
    # Now append the checked boxes from POST
    if "checkbox" in POST:
        for item in POST["checkbox"]:
            SESSION['checkedboxes'].append(item)
    else:
        print("No checkboxes selected.")
        
    print(SESSION['checkedboxes'])  # Debugging output



    # Check if any checkboxes were selected
    # checked_boxes = request.POST.getlist("checkbox")  # Safely handle multiple values


# REQUEST_VARS['cases'] = POST["checkboxes"]

# print(REQUEST_VARS['cases'])


def check_largeur_longeur(brique_longeur, brique_largeur, liste_coordinates):
    # Ensure there are no non-adjacent boxes in the list
    checked_set = set(liste_coordinates)

    # Check if all coordinates in a row are contiguous horizontally
    def check_horizontal_adjacency():
        for y in range(max_y + 1):  # For each row
            row_coordinates = [x for x, y_coord in checked_set if y_coord == y]
            row_coordinates.sort()

            # Ensure the row coordinates are contiguous
            for i in range(len(row_coordinates) - 1):
                if row_coordinates[i] + 1 != row_coordinates[i + 1]:
                    return False  # Found a gap between coordinates
            if len(row_coordinates) >= brique_longeur:
                return True  # Found a valid horizontal placement
        return False

    # Check if all coordinates in a column are contiguous vertically
    def check_vertical_adjacency():
        for x in range(max_x + 1):  # For each column
            col_coordinates = [y for x_coord, y in checked_set if x_coord == x]
            col_coordinates.sort()

            # Ensure the column coordinates are contiguous
            for i in range(len(col_coordinates) - 1):
                if col_coordinates[i] + 1 != col_coordinates[i + 1]:
                    return False  # Found a gap between coordinates
            if len(col_coordinates) >= brique_largeur:
                return True  # Found a valid vertical placement
        return False

    if not liste_coordinates:
        return False

    # Determine the grid dimensions
    max_x = max(coord[0] for coord in liste_coordinates)
    max_y = max(coord[1] for coord in liste_coordinates)

    # Ensure the checked boxes are contiguous either horizontally or vertically
    if check_horizontal_adjacency() or check_vertical_adjacency():
        return True
    return False


def check_brique(brique_longeur, brique_largeur, liste_coordinates):
    nmbr_briques = len(liste_coordinates)
    if (nmbr_briques !=brique_longeur*brique_largeur):
        return False
    x = []
    y = []
    for coord in liste_coordinates:
        x.append(coord[0])

    

