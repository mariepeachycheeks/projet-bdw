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

# easy level for small breaks


def get_random_bricks(connexion):
    query = "SELECT * FROM legos.piece WHERE length <= %s OR width <= %s"
    params = [2, 2]

    brick = execute_select_query(connexion, query, params)

    return brick


'''
#controleur

    if bricks is None:
        logger.warning("Il y a plus de bricks dans BD")
        return []

    if len(bricks) >= 4:
        return random.sample(bricks, 4)









def initialize_pioche(connexion, nombre_briques=4):
    """
    Remplir la pioche avec des briques valides, choisies aléatoirement.
    La pioche est initialisée avec un nombre de briques aléatoires qui respectent
    les conditions de largeur ou longueur <= 2.

    :param connexion: Connexion à la base de données
    :param nombre_briques: Le nombre de briques à ajouter dans la pioche
    """
    try:

        while len(pioche) < nombre_briques:


            bricks = get_random_bricks(connexion)

            if bricks:

                pioche.extend([brick['id'] for brick in bricks])

            # S'assurer que la pioche ne dépasse pas le nombre de briques souhaité
             pioche[:] = pioche[:nombre_briques]

        logger.info(f"Pioche initialisée avec {len(pioche)} briques.")

    except Exception as e:
        logger.error(f"Error initializing the pioche: {e}")


def replace_selected_brick(connexion, selected_id):
    """
    Remplace une brique sélectionnée par une autre brique avec length <= 2 ou width <= 2.
    La brique remplacée est exclue de la sélection grâce à son ID.
    """
    try:
        query = "SELECT * FROM piece WHERE (longueur <= %s OR largeur <= %s) AND id != %s"
        params = [2, 2, selected_id]


        bricks = execute_select_query(connexion, query, params)

        if bricks is None or len(bricks) == 0:
            logger.warning(
                f"No valid bricks found to replace the brick with ID {selected_id}.")
            return None


        new_brick = random.choice(bricks)


        pioche.append(new_brick['id'])

        # Retirer l'ID de la brique remplacée
        if selected_id in pioche:
            pioche.remove(selected_id)

        # Retourner la nouvelle brique
        return new_brick

    except Exception as e:
        logger.error(e)
        return None





'''

'''Fonctionnalité 4'''

'''
        def generate_random_grid(width, height):
    total_cells = width * height

    # Le nombre de cases cibles est un nombre aléatoire compris entre 10% et 20% du nombre total de cases ;
    num_targets = random.randint(
        int(0.1 * total_cells), int(0.2 * total_cells))

    # Initialiser une grille vide
    grid = [["empty" for _ in range(width)] for _ in range(height)]

    # Sélectionner aléatoirement une première case cible ;
    first_target = (random.randint(0, height - 1),
                    random.randint(0, width - 1))
    grid[first_target[0]][first_target[1]] = "target"

    targets = [first_target]
    max_attempts = 100  # Nombre maximal d'essais pour ajouter une nouvelle cible
    attempts = 0

    '''
'''Pour chaque case cible à ajouter, choisir une direction aléatoire(parmi haut, bas, gauche, droite) et vérifier
si la case correspondante(première case cible + direction choisie) est valide(i.e., dans la grille et case
vide): si oui, la transformer en case cible et répéter, sinon choisir une autre direction; 

    while len(targets) < num_targets:
        current_target = random.choice(targets)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = current_target[0] + dx
            new_y = current_target[1] + dy

         # '''
'''Gérer les situations exceptionnelles(e.g., pas suffisamment de cases cibles car le motif est en forme de
           # ”spirale”).'''

''' if 0 <= new_x < height and 0 <= new_y < width and grid[new_x][new_y] == "empty":
            grid[new_x][new_y]="target"
            targets.append((new_x, new_y))
            break
        else:
            # Si on a essayé toutes les directions sans succès, on incrémente le nombre d'essais
            attempts += 1
            # Si trop d'essais ont échoué, on sort de la boucle
            if attempts >= max_attempts:
                print("Échec de la génération des cibles après plusieurs tentatives.")
                break

            return grid'''
