from model.model_pg import get_random_brick,  get_instances, insert_joueuse, insert_partie
from datetime import datetime

 
    
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
                #changer au update_partie
                insert_partie(SESSION['CONNEXION'], SESSION['date_debut'], str(datetime.now()), SESSION['score'],  SESSION['joueuse'], None, None)
                
                
#si tu perts
if POST and "quit" in POST:
   SESSION['score'] = 999
    #changer au update_partie
   insert_partie(SESSION['CONNEXION'], SESSION['date_debut'], str(datetime.now()), SESSION['score'],  SESSION['joueuse'], None, None)

   #ici il faut ajouter affichage 

if POST and "change" in POST:
    print('change')
    print(POST['brique'])
    change_brique(SESSION['pioche'], POST['brique'])
    




    

    

