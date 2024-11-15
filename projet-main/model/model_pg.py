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

        query_defaussees_petite = sql.SQL('SELECT p_defausees FROM {table} ORDER BY p_defausees ASC LIMIT 1;').format(
            table=sql.Identifier(table))
        query_defaussees_petite = execute_select_query(
            connexion, query_defaussees_petite)

        query_defaussees_grand = sql.SQL('SELECT p_defausees FROM {table} ORDER BY p_defausees DESC LIMIT 1;').format(
            table=sql.Identifier(table))
        query_defaussees_grand = execute_select_query(
            connexion, query_defaussees_grand)
        results_list = [query_pioches_petite, query_pioches_grand,
                        query_defaussees_petite, query_defaussees_grand]

        return results_list

    except psycopg.Error as e:
        logger.error(e)
    return None


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


def insert_serie(connexion, nom_serie):
    """
    Insère une nouvelle série dans la BD
    String nom_serie : nom de la série
    Retourne le nombre de tuples insérés, ou None
    """
    query = 'INSERT INTO series VALUES(%s)'
    return execute_other_query(connexion, query, [nom_serie])


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


def get_random_bricks(connexion):
    query = "SELECT * FROM BRIQUE WHERE length <= %s OR width <= %s"
    params = [2, 2]

    # Exécuter la requête
    bricks = execute_select_query(connexion, query, params)

    if bricks is None:
        logger.warning("No bricks found or error during fetching.")
        return []

    if len(bricks) >= 4:
        return random.sample(bricks, 4)
    else:
        return bricks


def replace_selected_brick(connexion, selected_id):
    """
    Remplace une brique sélectionnée par une autre brique avec length <= 2 ou width <= 2.
    La brique remplacée est exclue de la sélection grâce à son ID.
    """
    query = "SELECT * FROM BRIQUE WHERE (length <= %s OR width <= %s) AND id != %s"
    params = [2, 2, selected_id]

    # Exécuter la requête avec la méthode générique
    bricks = execute_select_query(connexion, query, params)

    if bricks is None or len(bricks) == 0:
        logger.warning(
            f"No valid bricks found to replace the brick with ID {selected_id}.")
        return None

    # Choisir une brique aléatoire parmi celles disponibles
    new_brick = random.choice(bricks)
    return new_brick
