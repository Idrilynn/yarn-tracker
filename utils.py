import secrets


ID_CHARACTERS = '23456789ABCDEFGHJKMNPQRSTUVWXYZ'


def generate_id(length=6):
    new_id = ''
    for _ in range(length):
        new_id += secrets.choice(ID_CHARACTERS)
    return new_id

def make_placeholders(values):
    return ', '.join(['?'] * len(values))