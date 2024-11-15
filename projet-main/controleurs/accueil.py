"""
ce fichier est vide, il faudra y mettre du code (question TP5)
"""
from server import SESSION, REQUEST_VARS
from model.model_pg import count_instances, parties_pieces_defaussees_piochees, top_couleurs_nb_briques, score_min_max
try:
    res_piece = count_instances(SESSION['CONNEXION'], 'legos.piece')
    if res_piece:
        REQUEST_VARS['nb_piece'] = res_piece[0]
    else:
        print("Error: res_piece is None or empty.")

    res_partie = count_instances(SESSION['CONNEXION'], 'legos.PARTIE')
    if res_partie:
        REQUEST_VARS['nb_parties'] = res_partie[0]
    else:
        print("Error: res_partie is None or empty.")

    res_joueuses = count_instances(SESSION['CONNEXION'], 'legos.JOUEUSE')
    if res_joueuses:
        REQUEST_VARS['nb_JOUEUSE'] = res_joueuses[0]
    else:
        print("Error: res_joueuses is None or empty.")

    res_top_couleurs = top_couleurs_nb_briques(
        SESSION['CONNEXION'], 'legos.piece')
    if res_top_couleurs:
        REQUEST_VARS['top_couleurs'] = res_top_couleurs
    else:
        print("Error: res_joueuses is None or empty.")

    res_max_min_score = score_min_max(
        SESSION['CONNEXION'], 'legos.JOUEUSE', 'legos.LIER', 'legos.PARTIE')
    if res_max_min_score:
        REQUEST_VARS['max_min_score'] = res_top_couleurs
    else:
        print("Error: res_max_min_score is None or empty.")

    res_pieces_defaussees_piochees = parties_pieces_defaussees_piochees(
        SESSION['CONNEXION'], 'legos.PARTIE')
    if res_pieces_defaussees_piochees:
        REQUEST_VARS['piochees_min'] = res_pieces_defaussees_piochees[0]
        REQUEST_VARS['piochees_max'] = res_pieces_defaussees_piochees[1]
        REQUEST_VARS['defaussees_min'] = res_pieces_defaussees_piochees[2]
        REQUEST_VARS['defaussees_max'] = res_pieces_defaussees_piochees[3]
    else:
        print("Error: res_pieces_defaussees_piochees is None or empty.")


except Exception as e:
    print(f"An error occurred: {e}")
