from model.model_pg import get_instances, get_episodes_for_num, add_activity


add_activity(SESSION['HISTORIQUE'], "affichage des données")

"""Fonctionnalité 2"""


REQUEST_VARS['piece'] = get_random_brick(SESSION['CONNEXION'])

if piece is None:
    logger.warning("Il y a plus de bricks dans BD")
    # return []


initialize_pioche(SESSION['CONNEXION'], 4)

selected_id = REQUEST_VARS['selected_id']

if selected_id:
    REQUEST_VARS['piece'] = replace_selected_brick(
        SESSION['CONNEXION'], selected_id)
else:
    logger.error("Selected brick ID is missing.")


'''doma screen '''

pioche = []

REQUEST_VARS['piece'] = b


if b is None:
        logger.warning("Il y a plus de bricks dans BD")
        # return []


if 'pioche' not in SESSION:
    SESSION['pioche'] = get_random_brick(SESSION['CONNEXION'], 4)

    if form_submitted:

        if b in SESSION['pioche']:

         SESSION['pioche'].remove(b)

     SESSION['pioche'].extend(get_random_brick(SESSION['CONNEXION'], 1))



"""Fonctionnalité 4"""

if POST and "submit" in POST:

    width=POST["width"]
 
    height=POST["height"]

    generate_random_grid(SESSION['CONNEXION'], width, height)