import utils


def test_generate_id_uses_allowed_characters():
    # 1000 tirages pour augmenter les chances de tomber sur un caractère interdit
    for _ in range(1000):
        new_id = utils.generate_id()
        for character in new_id:
            assert character in utils.ID_CHARACTERS

def test_id_characters_excludes_ambiguous():
    # pas de caractère ambigu dans les ids
    for character in '0O1IL':
        assert character not in utils.ID_CHARACTERS

def test_generate_id_respects_length():
    # les ids sont de la bonne longueur
    id_1 = utils.generate_id()
    id_2 = utils.generate_id(10)
    assert len(id_1) == 6
    assert len(id_2) == 10