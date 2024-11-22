from model.model_pg import get_instances, get_episodes_for_num
from controleurs.includes import add_activity


add_activity(SESSION['HISTORIQUE'], "affichage des données")

# récupérer les séries
REQUEST_VARS['series'] = get_instances(SESSION['CONNEXION'], 'series')

# récupérer les actrices
REQUEST_VARS['actrices'] = get_instances(SESSION['CONNEXION'], 'actrices')

REQUEST_VARS['critiques'] =  get_instances(SESSION['CONNEXION'], 'critiques')

"""
À vous de jouer : lister les critiques en vous inspirant du code ci-dessus.
Vous pourrez plus tard améliorer le code en affichant chaque série avec les
critiques qui la concernent !
"""

# récupérer les épisodes 1 et 2
#TODO avec psycopg3, utiliser une requête préparée
REQUEST_VARS['episodes1'] = get_episodes_for_num(SESSION['CONNEXION'], 1)
REQUEST_VARS['episodes2'] = get_episodes_for_num(SESSION['CONNEXION'], 2)



"""Fonctionnalité 2


REQUEST_VARS['piece'] = get_random_brick(SESSION['CONNEXION'])

 if piece is None:
        logger.warning("Il y a plus de bricks dans BD")
        return []

    
    
initialize_pioche(SESSION['CONNEXION'], 4)

selected_id = REQUEST_VARS['selected_id']

if selected_id:
    REQUEST_VARS['piece'] = replace_selected_brick(SESSION['CONNEXION'], selected_id)
else:
    logger.error("Selected brick ID is missing.")
"""




'''doma screen '''

pioche=[]

REQUEST_VARS['piece'] = b


if b is None:
        logger.warning("Il y a plus de bricks dans BD")
        return []

    
if 'pioche' not in SESSION:
    SESSION['pioche']=get_random_brick(SESSION['CONNEXION'], 4)

    if form_submitted:

        if b in SESSION['pioche']:

         SESSION['pioche'].remove(b)

     SESSION['pioche'].extend(get_random_brick(SESSION['CONNEXION'], 1))



"""Fonctionnalité 4""""

if POST and "submit" in POST:

    width=POST["width"]
 
    height=POST["height"]

   grid = generate_random_grid(width, height)

   
    print(grid)  

 python server.py