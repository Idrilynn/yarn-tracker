from datetime import datetime
from utils import generate_id, make_placeholders, get_connection


def add_catalogue_item(picture, brand_name, yarn_name,
                       length, weight, weight_cat, colour_id,
                       colour_type, colour, fibers, texture,
                       place, where_to_order):
    # date et heure de l'ajout, stockées en texte
    now = datetime.now().isoformat(timespec='seconds')
    if not isinstance(weight, (int, float)) or weight <= 0:
        raise ValueError(f"Poids invalide: {weight}. Indiquer une masse en grammes supérieure à 0")
    if not isinstance(length, (int, float)) or length <= 0:
        raise ValueError(f"Longueur invalide: {length}. Indiquer une longueur en mètres supérieure à 0")
    if not isinstance(brand_name, str) or brand_name.strip() == '':
        raise ValueError("Renseigner la marque de la pelote.")
    if not isinstance(yarn_name, str) or yarn_name.strip() == '':
        raise ValueError("Renseigner la gamme de la pelote.")
    connection = get_connection()
    try:
        item_id = generate_id()
        # tant que cet id existe déjà dans le catalogue, on en tire un autre
        while connection.execute('SELECT 1 FROM catalogue WHERE id = ?',
                                 (item_id,)).fetchone() is not None:
            item_id = generate_id()

        connection.execute('''INSERT INTO catalogue (id, picture, brand_name, yarn_name,
                                                     length, weight, weight_cat, colour_id,
                                                     colour_type, colour, fibers, texture, 
                                                     place, where_to_order, modified_at)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (item_id, picture, brand_name, yarn_name,
                            length, weight, weight_cat, colour_id,
                            colour_type, colour, fibers, texture,
                            place, where_to_order, now))

        connection.commit()
    finally:
        connection.close()
    return item_id


def list_catalogue(statuses=None):
    connection = get_connection()
    try:
        if statuses is None:
            rows = connection.execute('''SELECT catalogue.brand_name, catalogue.yarn_name, catalogue.colour_id,
                               COUNT(inventory.id)
                               FROM catalogue
                               LEFT JOIN inventory ON inventory.catalogue_id = catalogue.id
                               GROUP BY catalogue.id'''
                                      ).fetchall()
        else:
            placeholders = make_placeholders(statuses)
            rows = connection.execute(f''' SELECT catalogue.brand_name, catalogue.yarn_name, catalogue.colour_id,
                                COUNT(inventory.id)
                                FROM catalogue
                                JOIN inventory ON inventory.catalogue_id = catalogue.id
                                WHERE inventory.status IN ({placeholders})
                                GROUP BY catalogue.id''',
                                      statuses
                                      ).fetchall()
    finally:
        connection.close()
    return rows