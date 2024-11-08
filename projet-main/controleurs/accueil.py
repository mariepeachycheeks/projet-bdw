"""
ce fichier est vide, il faudra y mettre du code (question TP5)
"""

from model.model_pg import count_instances

res = count_instances(SESSION['CONNEXION'], 'legos.piece')
REQUEST_VARS['nb_piece'] = res[0]
