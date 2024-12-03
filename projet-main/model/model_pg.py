import psycopg
from psycopg import sql
from logzero import logger
import random


def count_instances(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL(
        'SELECT COUNT(*) AS nb FROM {table}').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)


'''Top-5 des couleurs ayant le plus de briques ;'''


def top_couleurs_nb_briques(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL(
        'SELECT couleur, COUNT(id) AS total_briques FROM {table} group by couleur ORDER BY total_briques DESC LIMIT 5').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)


def score_min_max(connexion, JOUEUSE, LIER, PARTIE):
    query = sql.SQL('SELECT j.prenom, MAX(p.score) , MIN(p.score) FROM  legos.JOUEUSE j JOIN  legos.LIER l ON j.prenom = l.prenom JOIN  legos.PARTIE p ON l.score = p.score GROUP BY  j.prenom;').format(
        table=sql.Identifier(JOUEUSE, LIER, PARTIE))
    return execute_select_query(connexion, query)


''' Parties avec le plus petit et plus grand nombre de pièces défaussées, de pièces piochées '''


def parties_pieces_defaussees_piochees(connexion, table):
    try:
        query_pioches_petite = sql.SQL('SELECT p_piochees FROM {table} ORDER BY p_piochees ASC LIMIT 1;').format(
            table=sql.Identifier(table))
        query_pioches_petite = execute_select_query(
            connexion, query_pioches_petite)

        query_pioches_grand = sql.SQL('SELECT p_piochees FROM {table} ORDER BY p_piochees DESC LIMIT 1;').format(
            table=sql.Identifier(table))
        query_pioches_grand = execute_select_query(
            connexion, query_pioches_grand)

        query_defaussees_petite = sql.SQL('SELECT p_defaussees FROM {table} ORDER BY p_defaussees ASC LIMIT 1;').format(
            table=sql.Identifier(table))
        query_defaussees_petite = execute_select_query(
            connexion, query_defaussees_petite)

        query_defaussees_grand = sql.SQL('SELECT p_defaussees FROM {table} ORDER BY p_defaussees DESC LIMIT 1;').format(
            table=sql.Identifier(table))
        query_defaussees_grand = execute_select_query(
            connexion, query_defaussees_grand)
        results_list = [query_pioches_petite[0], query_pioches_grand[0],
                        query_defaussees_petite[0], query_defaussees_grand[0]]

        return results_list

    except psycopg.Error as e:
        logger.error(e)
    return None


'''Le nombre moyen de tours, pour chaque couple (mois, année) '''


def nmbr_moy_tours(connexion, parties, tours):
    query = sql.SQL('SELECT EXTRACT(MONTH FROM p.date_debut) AS mois, EXTRACT(YEAR FROM p.date_debut) AS annee, COUNT(t.numero) / COUNT(DISTINCT p.date_debut) AS avg_tours FROM {parties} p JOIN {tours} t ON p.date_debut = t.date_debut AND p.date_fin = t.date_fin GROUP BY mois, annee ORDER BY annee, mois').format(
        parties=sql.Identifier(parties),
        tours=sql.Identifier(tours)
    )
    return execute_select_query(connexion, query)


'''Top-3 des parties dans lesquelles les plus grandes pièces avec un tri
décroissant sur le nombre de pièces utilisées '''


def trie_nmbr_pieces_used(connexion, tours, parties):
    query = sql.SQL('SELECT p.date_debut AS partie_date, p.date_fin AS partie_end, COUNT(t.numero) AS total_pieces_used FROM {tours} t JOIN {parties} p ON p.date_debut = t.date_debut AND p.date_fin = t.date_fin GROUP BY p.date_debut, p.date_fin ORDER BY total_pieces_used DESC LIMIT 3;').format(
        tours=sql.Identifier(tours),
        parties=sql.Identifier(parties)
    )
    return execute_select_query(connexion, query)


def top_partie_grand_piece(connexion):
    query = '''SELECT p.date_debut AS partie_date, p.date_fin AS partie_end,
SUM(pi.longueur * pi.largeur) AS total_piece_size
FROM tours t
JOIN piece pi USING(id)
JOIN partie p ON p.date_debut = t.date_debut AND p.date_fin = t.date_fin
GROUP BY p.date_debut, p.date_fin
ORDER BY total_piece_size DESC
LIMIT 3;'''
    return execute_select_query(connexion, query)


def execute_select_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête SELECT (qui peut retourner plusieurs instances).
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except psycopg.Error as e:
            logger.error(e)
    return None


def execute_other_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête INSERT, UPDATE, DELETE.
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.rowcount
            return result
        except psycopg.Error as e:
            logger.error(e)
    return None


def get_instances(connexion, nom_table):
    """
    Retourne les instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL(
        'SELECT * FROM {table}').format(table=sql.Identifier(nom_table), )
    return execute_select_query(connexion, query)

def insert_joueuse(connexion, nom_joueuse, date):
    query = 'INSERT INTO joueuse (prenom, date_inscription) VALUES (%s, %s)'
    params = [nom_joueuse, date]

    return execute_other_query(connexion, query, params)






def insert_partie(connexion, date_debut, date_fin, score, name, p_defaussees, p_piochees):
    query = 'INSERT INTO partie (date_debut, date_fin, score, gagnante, p_defaussees, p_piochees) VALUES(%s,%s,%s,%s,%s,%s)'
    params = [date_debut, date_fin, score, name, p_defaussees, p_piochees]
    return execute_other_query(connexion, query, params )


def get_episodes_for_num(connexion, numero):
    """
    Retourne le titre des épisodes numérotés numero
    Integer numero : numéro des épisodes
    """
    query = 'SELECT titre FROM episodes where numéro=%s'
    return execute_select_query(connexion, query, [numero])


def get_serie_by_name(connexion, nom_serie):
    """
    Retourne les informations sur la série nom_serie (utilisé pour vérifier qu'une série existe)
    String nom_serie : nom de la série
    """
    query = 'SELECT * FROM series where nomsérie=%s'
    return execute_select_query(connexion, query, [nom_serie])




def insert_critique(connexion, date_critique, pseudo, texte, nom_serie):

    query = 'INSERT INTO critiques (datecritique, pseudo, texte, nomsérie) VALUES (%s, %s, %s, %s)'
    params = [date_critique, pseudo, texte, nom_serie]

    return execute_other_query(connexion, query, params)


def get_table_like(connexion, nom_table, like_pattern):
    """
    Retourne les instances de la table nom_table dont le nom correspond au motif like_pattern
    String nom_table : nom de la table
    String like_pattern : motif pour une requête LIKE
    """
    motif = '%' + like_pattern + '%'
    nom_att = 'nomsérie'  # nom attribut dans séries (à éviter)
    if nom_table == 'actrices':  # à éviter
        nom_att = 'nom'  # nom attribut dans actrices (à éviter)
    query = sql.SQL("SELECT * FROM {} WHERE {} ILIKE {}").format(
        sql.Identifier(nom_table),
        sql.Identifier(nom_att),
        sql.Placeholder())
    #    like_pattern=sql.Placeholder(name=like_pattern))
    return execute_select_query(connexion, query, [motif])


'''Fonctionnalité 2'''

# easy level for small breaks




def get_random_brick(connexion):

    query= "SELECT * FROM piece WHERE longueur <= %s OR largeur <= %s ORDER BY random() LIMIT 1;" 
    print(query)
    params = [2, 2]

    
    brick = execute_select_query(connexion, query, params)

    return brick
