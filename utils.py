import secrets
import sqlite3

# Liste des caractères qui composent les id
ID_CHARACTERS = '23456789ABCDEFGHJKMNPQRSTUVWXYZ'
# Fichier de la base utilisée par l'appli
DB_PATH = 'yarn.db'


def generate_id(length=6):
    new_id = ''
    for _ in range(length):
        new_id += secrets.choice(ID_CHARACTERS)
    return new_id

def make_placeholders(values):
    return ', '.join(['?'] * len(values))

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute('PRAGMA foreign_keys = ON')
    return connection