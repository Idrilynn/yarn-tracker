import sqlite3
from datetime import datetime, date

from utils import generate_id


# ligne 1: paramètres pour retrouver la référence catalogue item_id
# ligne 2: paramètres de la pelote
def add_inventory_item(brand_name, yarn_name, colour_id,
                       weight_init, dye_lot=None, added_at=None, confirm=False):
    # date et heure de l'ajout, stockées en texte
    now = datetime.now().isoformat(timespec='seconds')
    connection = sqlite3.connect('yarn.db')
    connection.execute('PRAGMA foreign_keys = ON')

    row = connection.execute('SELECT id FROM catalogue WHERE brand_name = ?'
                                       ' AND yarn_name = ? '
                                       ' AND colour_id = ?',
                                       (brand_name, yarn_name, colour_id)).fetchone()
    if row is None:
        connection.close()
        raise ValueError(f"La référence {brand_name} {yarn_name} {colour_id} n'existe pas en catalogue")

    if added_at is None:
        added_at = date.today().isoformat()

    item_id = generate_id()
    # tant que cet id existe déjà dans l'inventaire, on en tire un autre
    while connection.execute('SELECT 1 FROM inventory WHERE id = ?',
                             (item_id,)).fetchone() is not None:
        item_id = generate_id()

    catalogue_id = row[0]
    weight_remain = weight_init
    status = 'in_stock'

    duplicate_insert = connection.execute('SELECT id FROM inventory WHERE catalogue_id = ?'
                                   ' AND weight_init = ?'
                                   ' AND added_at = ?'
                                   ' AND dye_lot IS ?',
                                          (catalogue_id, weight_remain, added_at, dye_lot)).fetchone()
    if duplicate_insert is not None and not confirm:
        connection.close()
        raise ValueError(f"La pelote semble déjà saisie en base de données [ID: {duplicate_insert[0]}]. "
                         f" Relance avec confirm=True si c’est voulu")

    connection.execute('''INSERT INTO inventory (id, catalogue_id, weight_init, weight_remain,
                                                 dye_lot, added_at, status, modified_at)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (item_id, catalogue_id, weight_init, weight_remain,
                        dye_lot, added_at, status, now))

    connection.commit()
    connection.close()
    return item_id


if __name__ == '__main__':
    print(add_inventory_item('Scheepjes', 'Catona', '162', 51.3))