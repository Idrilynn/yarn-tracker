from src.connection import get_connection

def insert_yarn_stock(catalog_id, initial_weight, dye_lot=None, misc=None):
    conn = get_connection()
    cur = conn.cursor()
    current_weight = initial_weight
    cur.execute("INSERT INTO stock_yarn (catalog_id, initial_weight, current_weight, dye_lot, misc) VALUES "
                "(%s, %s, %s, %s, %s)",
                (catalog_id, initial_weight, current_weight, dye_lot, misc))
    conn.commit()
    cur.close()
    conn.close()

def update_yarn_stock(id, current_weight, misc=None):
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []
    if current_weight is not None:
        fields.append("current_weight = %s")
        values.append(current_weight)
    if misc is not None:
        fields.append("misc = %s")
        values.append(misc)
    if not fields:
        return
    query = "UPDATE stock_yarn SET " + ", ".join(fields) + " WHERE id = %s"
    values.append(id)
    cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()

def delete_yarn_stock(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM stock_yarn WHERE id = %s ", (id,))
    conn.commit()
    cur.close()
    conn.close()

def select_yarn_stock():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stock_yarn ")
    results= cur.fetchall()
    cur.close()
    conn.close()
    return results