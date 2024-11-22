"""
ce fichier est vide, il faudra y mettre du code (question TP5)
"""
# from server import SESSION, REQUEST_VARS
from model.model_pg import count_instances, parties_pieces_defaussees_piochees, top_couleurs_nb_briques, score_min_max, nmbr_moy_tours, top_partie_grand_piece
try:
    res_piece = count_instances(SESSION['CONNEXION'], 'piece')
    # print(res_piece)
   # if res_piece:
    REQUEST_VARS['nb_piece'] = res_piece[0]
    # else:
    # print("Error: res_piece is None or empty.")

    res_partie = count_instances(SESSION['CONNEXION'], 'partie')
    # if res_partie:
    REQUEST_VARS['nb_parties'] = res_partie[0]
    # else:
    #  print("Error: res_partie is None or empty.")

    res_joueuses = count_instances(SESSION['CONNEXION'], 'joueuse')
    # if res_joueuses:
    REQUEST_VARS['nb_JOUEUSE'] = res_joueuses[0]
   # else:
    # print("Error: res_joueuses is None or empty.")

    res_top_couleurs = top_couleurs_nb_briques(
        SESSION['CONNEXION'], 'piece')
    # if res_top_couleurs:
    print(res_top_couleurs)
    REQUEST_VARS['top_couleurs'] = res_top_couleurs
    # else:
    # print("Error: res_joueuses is None or empty.")

    res_max_min_score = score_min_max(
        SESSION['CONNEXION'], 'JOUEUSE', 'LIER', 'PARTIE')
    # if res_max_min_score:
    print(res_max_min_score)
    REQUEST_VARS['max_min_score'] = res_max_min_score
    # else:
    # print("Error: res_max_min_score is None or empty.")
    res_pieces_defaussees_piochees = parties_pieces_defaussees_piochees(
        SESSION['CONNEXION'], 'partie')

    print(res_pieces_defaussees_piochees)
    REQUEST_VARS['piochees_min'] = res_pieces_defaussees_piochees[0][0]
    REQUEST_VARS['piochees_max'] = res_pieces_defaussees_piochees[1][0]
    REQUEST_VARS['defaussees_min'] = res_pieces_defaussees_piochees[2][0]
    REQUEST_VARS['defaussees_max'] = res_pieces_defaussees_piochees[3][0]

    res_nmbr_moy_tours = nmbr_moy_tours(
        SESSION['CONNEXION'], 'partie',  'tours')
    print(res_nmbr_moy_tours)
    REQUEST_VARS['nmbr_moy_tours'] = res_nmbr_moy_tours

    res_top3_parties = top_partie_grand_piece(
        SESSION['CONNEXION'])
    print(res_top3_parties)
    REQUEST_VARS['top3_parties'] = res_top3_parties


except Exception as e:
    print(f"An error occurred: {e}")


'''
    

    
    

    res_pieces_defaussees_piochees = parties_pieces_defaussees_piochees(
        SESSION['CONNEXION'], 'legos.PARTIE')
    if res_pieces_defaussees_piochees:
        REQUEST_VARS['piochees_min'] = res_pieces_defaussees_piochees[0]
        REQUEST_VARS['piochees_max'] = res_pieces_defaussees_piochees[1]
        REQUEST_VARS['defaussees_min'] = res_pieces_defaussees_piochees[2]
        REQUEST_VARS['defaussees_max'] = res_pieces_defaussees_piochees[3]
    else:
        print("Error: res_pieces_defaussees_piochees is None or empty.")

    res_nmbr_moy_tours = nmbr_moy_tours(
        SESSION['CONNEXION'], 'legos.PARTIE',  'legos.TOURS')
    if res_nmbr_moy_tours:
        REQUEST_VARS['nmbr_moy_tours'] = res_nmbr_moy_tours
    else:
        print("Error: res_nmbr_moy_tours is None or empty.")

    res_top3_parties = top_partie_grand_piece(
        SESSION['CONNEXION'], 'legos.PARTIE',  'legos.TOURS', 'legos.piece')
    if res_top3_parties:
        REQUEST_VARS['top3_parties'] = res_top3_parties
    else:
        print("Error: res_top3_parties is None or empty.")

'''
