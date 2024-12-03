
from model.model_pg import get_random_brick


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


if 'score' not in SESSION:
    SESSION['score'] = 0

if POST and "select" in POST:
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



    print(SESSION['checkedboxes'])
        #il faut changer ici le brique





def sontAdjacentes(a,b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

def trierBriques(liste_coordinates):
    coordonnees_tries = sorted(liste_coordinates, key=lambda coord: (coord[1], coord[0]))
    return coordonnees_tries




    

    

