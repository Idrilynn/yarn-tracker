import pytest
import utils
import sqlite3
from database import create_tables
from catalogue import add_catalogue_item


@pytest.fixture
def empty_db(tmp_path, monkeypatch):
    # base vide dans un dossier temporaire, jetée après le test
    monkeypatch.setattr(utils, 'DB_PATH', tmp_path / 'test.db')
    create_tables()


def test_add_catalogue_item_returns_id(empty_db):
    item_id = add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                                 'solid', 'rouge', None, None, None, None)
    # l'id doit faire 6 caractères
    assert len(item_id) == 6

def test_add_catalogue_item_refuses_duplicate(empty_db):
    add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                                 'solid', 'rouge', None, None, None, None)
    with pytest.raises(sqlite3.IntegrityError):
        add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                           'solid', 'rouge', None, None, None, None)