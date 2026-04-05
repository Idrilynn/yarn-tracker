from src.connection import get_connection

def insert_yarn(product, brand, colour, material, weight, length, dye=None, misc=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO catalog_yarn (product, brand, colour, material, weight, length, dye, misc) VALUES "
                "(%s, %s, %s, %s, %s, %s, %s, %s)",
                (product, brand, colour, material, weight, length, dye, misc))
    conn.commit()
    cur.close()
    conn.close()

def update_yarn(id, availability=None, misc=None):
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []
    if availability is not None:
        fields.append("availability = %s")
        values.append(availability)
    if misc is not None:
        fields.append("misc = %s")
        values.append(misc)
    if not fields:
        return
    query = "UPDATE catalog_yarn SET " + ", ".join(fields) + " WHERE id = %s"
    values.append(id)
    cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()

def delete_yarn(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM catalog_yarn WHERE id = %s ", (id,))
    conn.commit()
    cur.close()
    conn.close()

def select_yarn():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM catalog_yarn ")
    results= cur.fetchall()
    cur.close()
    conn.close()
    return results