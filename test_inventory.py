import pytest
import utils
from database import create_tables
from catalogue import add_catalogue_item
from inventory import add_inventory_item


@pytest.fixture
def empty_db(tmp_path, monkeypatch):
    # base vide dans un dossier temporaire, jetée après le test
    monkeypatch.setattr(utils, 'DB_PATH', tmp_path / 'test.db')
    create_tables()


def test_add_inventory_item_returns_id(empty_db):
    # la pelote a besoin d'une référence au catalogue
    add_catalogue_item(None, 'Scheepjes', 'Catona', 125, 50, 'fingering', '162',
                       'solid', 'marron', 'coton', None, None, None)
    item_id = add_inventory_item('Scheepjes', 'Catona', '162', 51.3)
    # l'id doit faire 6 caractères
    assert len(item_id) == 6


def test_add_inventory_item_refuses_absent_reference(empty_db):
    # il n'y a pas de référence dans le catalogue
    with pytest.raises(ValueError):
        add_inventory_item('Scheepjes', 'Catona', '162', 51.3)


def test_add_inventory_item_refuses_duplicate(empty_db):
    # un doublon sans confirm=True est refusé
    add_catalogue_item(None, 'Scheepjes', 'Catona', 125, 50, 'fingering', '162',
                       'solid', 'marron', 'coton', None, None, None)
    add_inventory_item('Scheepjes', 'Catona', '162', 51.3, added_at='2026-11-27')
    with pytest.raises(ValueError):
        add_inventory_item('Scheepjes', 'Catona', '162', 51.3, added_at='2026-11-27')


def test_add_inventory_item_accepts_duplicate_with_confirm(empty_db):
    # un doublon avec confirm=True (refusé puis confirmé) est accepté, et les deux pelotes ont des id différents
    add_catalogue_item(None, 'Scheepjes', 'Catona', 125, 50, 'fingering', '162',
                       'solid', 'marron', 'coton', None, None, None)
    item_id_1 = add_inventory_item('Scheepjes', 'Catona', '162', 51.3, added_at='2026-11-27')
    item_id_2 = add_inventory_item('Scheepjes', 'Catona', '162', 51.3, added_at='2026-11-27', confirm=True)
    assert item_id_1 != item_id_2

def test_add_inventory_item_accepts_other_dye_lot(empty_db):
    # un doublon sans confirm=True est accepté si les numéros de bain sont différents
    add_catalogue_item(None, 'Scheepjes', 'Catona', 125, 50, 'fingering', '162',
                       'solid', 'marron', 'coton', None, None, None)
    item_id_1 = add_inventory_item('Scheepjes', 'Catona', '162', 51.3, added_at='2026-11-27', dye_lot='123')
    item_id_2 = add_inventory_item('Scheepjes', 'Catona', '162', 51.3, added_at='2026-11-27', dye_lot='125')
    assert item_id_1 != item_id_2

@pytest.mark.parametrize('weight', ['lourd', 0, -5])
def test_add_inventory_item_refuses_wrong_weight(empty_db, weight):
    # le poids est mal renseigné
    add_catalogue_item(None, 'Scheepjes', 'Catona', 125, 50, 'fingering', '162',
                       'solid', 'marron', 'coton', None, None, None)
    with pytest.raises(ValueError):
        add_inventory_item('Scheepjes', 'Catona', '162', weight)