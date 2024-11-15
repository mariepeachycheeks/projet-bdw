import psycopg
from psycopg import sql
from logzero import logger

"""from flask import Flask, render_template, request, redirect"""
import random

"""nadia dodala:"""
"""
def create_connection():
    try:
        # Connect to PostgreSQL
        conn = psycopg.connect("dbname=bd-project.sql user=myuser password=mypassword host=localhost")
        logger.info("Connection to PostgreSQL successful.")
        return conn
    except psycopg.Error as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        return None
"""


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
        'SELECT couleur, COUNT(id) AS total_briques FROM {table}} group by couleur ORDER BY total_briques DESC LIMIT 5').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)


def score_min_max(connexion, JOUEUSE, LIER, PARTIE):
    query = sql.SQL('SELECT j.prenom, MAX(p.score) , MIN(p.score) FROM  legos.JOUEUSE j JOIN  legos.LIER l ON j.prenom = l.prenom JOIN  legos.PARTIE p ON l.score = p.score GROUP BY  j.prenom;').format(
        table=sql.Identifier(JOUEUSE, LIER, PARTIE))
    return execute_select_query(connexion, query)


''' Parties avec le plus petit et plus grand nombre de pièces défaussées, de pièces piochées '''


def parties_pieces_defaussees_piochees(connexion):
    try:
        query = sql.SQL('SELECT j.prenom, MAX(p.score) , MIN(p.score) FROM  legos.JOUEUSE j JOIN  legos.LIER l ON j.prenom = l.prenom JOIN  legos.PARTIE p ON l.score = p.score GROUP BY  j.prenom;').format(
            table=sql.Identifier(JOUEUSE, LIER, PARTIE))
        return execute_select_query(connexion, query)
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

''' # Function to get 4 random bricks with length or width <= 2
def get_random_bricks(connexion):
    cursor.execute("SELECT * FROM BRIQUE WHERE length <= 2 OR width <= 2")
    bricks = cursor.fetchall()
    if len(bricks) >= 4:
        return random.sample(bricks, 4)
    else:
        return bricks  # Return whatever is available if there are fewer than 4

# Function to replace a brick after selection


def replace_selected_brick(connexion, selected_id):
    cursor.execute(
        "SELECT * FROM BRIQUE WHERE (length <= 2 OR width <= 2) AND id != %s", (selected_id,))
    bricks = cursor.fetchall()
    if bricks:
        new_brick = random.choice(bricks)
        return new_brick
    else:
        return None  # If no valid bricks are found


# Sample usage
selected_brick = replace_selected_brick(connexion, selected_id=1)
if selected_brick:
    print("New brick added:", selected_brick)
else:
    print("No valid brick available for replacement.")


app = Flask(__name__)

# Function to simulate fetching random bricks


def get_bricks(connexion):
    # Fetch bricks with length or width <= 2 from the database
    bricks = get_random_bricks()
    return bricks


@app.route("/")
def index(connexion):
    bricks = get_bricks()
    return render_template("index.html", bricks=bricks)


@app.route("/select-brick", methods=["POST"])
def select_brick(connexion):
    selected_id = int(request.form["brick_id"])
    new_brick = replace_selected_brick(selected_id)
    return render_template("index.html", bricks=new_brick)


if __name__ == "__main__":
    app.run()

'''
