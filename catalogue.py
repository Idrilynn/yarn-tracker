import sqlite3
from datetime import datetime
from utils import generate_id, make_placeholders

def add_catalogue_item(picture, brand_name, yarn_name,
                       length, weight, weight_cat, colour_id,
                       colour_type, colour, fibers, texture,
                       place, where_to_order):
    # date et heure de l'ajout, stockées en texte
    now = datetime.now().isoformat(timespec='seconds')
    connection = sqlite3.connect('yarn.db')
    connection.execute('PRAGMA foreign_keys = ON')

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
    connection.close()
    return item_id


def list_catalogue(statuses=None):
    connection = sqlite3.connect('yarn.db')
    if statuses is None:
        rows = connection.execute('''SELECT catalogue.brand_name, catalogue.yarn_name, catalogue.colour_id,
                           COUNT(inventory.id)
                           FROM catalogue
                           LEFT JOIN inventory ON inventory.catalogue_id = catalogue.id
                           GROUP BY catalogue.id'''
                           ).fetchall()
        connection.close()
        for row in rows:
            print(f'{row[0]} {row[1]} {row[2]} : {row[3]} pelote(s)')
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
        connection.close()
        for row in rows:
            print(f'{row[0]} {row[1]} {row[2]} : {row[3]} pelote(s)')


#TESTS
if __name__ == '__main__':
# test : une référence fictive
    add_catalogue_item(picture=None, brand_name='Drops', yarn_name='Safran',
                   length=160, weight=50, weight_cat='fingering',
                   colour_id='99', colour_type='solid', colour='rouge',
                   fibers='coton', texture=None, place=None, where_to_order=None)# lecture de la table

    add_catalogue_item(picture=None, brand_name='Scheepjes', yarn_name='Catona',
                   length=125, weight=50, weight_cat='fingering',
                   colour_id='162', colour_type='solid', colour='marron',
                   fibers='coton', texture='4 brins', place=None, where_to_order=None)# lecture de la table

    list_catalogue()
    list_catalogue(['in_stock'])
