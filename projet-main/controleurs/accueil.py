"""
ce fichier est vide, il faudra y mettre du code (question TP5)
"""

from model.model_pg import count_instances

res = count_instances(SESSION['CONNEXION'], 'legos.piece')
REQUEST_VARS['nb_piece'] = res[0]
    if res_partie:
        REQUEST_VARS['nb_parties'] = res_partie[0]
    else:
        print("Error: res_partie is None or empty.")

    res_joueuses = count_instances(SESSION['CONNEXION'], 'legos.JOUEUSE')
    if res_joueuses:
        REQUEST_VARS['nb_JOUEUSE'] = res_joueuses[0]
    else:
        print("Error: res_joueuses is None or empty.")
except Exception as e:
    print(f"An error occurred: {e}")
