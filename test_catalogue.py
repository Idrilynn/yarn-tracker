import pytest
import utils
import sqlite3
from database import create_tables
from catalogue import add_catalogue_item, list_catalogue
from inventory import add_inventory_item


@pytest.fixture
def empty_db(tmp_path, monkeypatch):
    # base vide dans un dossier temporaire, jetée après le test
    monkeypatch.setattr(utils, 'DB_PATH', tmp_path / 'test.db')
    create_tables()


def test_add_catalogue_item_returns_id(empty_db):
    # l'id doit faire 6 caractères
    item_id = add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                                 'solid', 'rouge', None, None, None, None)
    assert len(item_id) == 6


def test_add_catalogue_item_refuses_duplicate(empty_db):
    # pas de doublons dans le catalogue
    add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                       'solid', 'rouge', None, None, None, None)
    with pytest.raises(sqlite3.IntegrityError):
        add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                           'solid', 'rouge', None, None, None, None)


def test_add_catalogue_item_refuses_duplicate_other_case(empty_db):
    # pas de doublons dans le catalogue, refus d'une référence même si la casse est différente
    add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                       'solid', 'rouge', None, None, None, None)
    with pytest.raises(sqlite3.IntegrityError):
        add_catalogue_item(None, 'DROPS', 'SAFRAN', 160, 50, None, '99',
                           'solid', 'rouge', None, None, None, None)


def test_list_catalogue_shows_reference_without_ball(empty_db):
    add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                       'solid', 'rouge', None, None, None, None)
    assert list_catalogue() == [('Drops', 'Safran', '99', 0)]


def test_list_catalogue_counts_balls(empty_db):
    add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                       'solid', 'rouge', None, None, None, None)
    add_inventory_item('Drops', 'Safran', '99', 50.3, '123')
    add_inventory_item('Drops', 'Safran', '99', 50.6, '123')
    assert list_catalogue() == [('Drops', 'Safran', '99', 2)]


def test_list_catalogue_hides_reference_with_filter(empty_db):
    add_catalogue_item(None, 'Drops', 'Safran', 160, 50, None, '99',
                       'solid', 'rouge', None, None, None, None)
    assert list_catalogue(statuses=['in_stock']) == []


@pytest.mark.parametrize('weight', ['lourd', 0, -5, None])
def test_add_catalogue_item_refuses_wrong_weight(empty_db, weight):
    # le poids est mal renseigné
    with pytest.raises(ValueError):
        add_catalogue_item(None, 'Drops', 'Safran', 160, weight, None, '99',
                           'solid', 'rouge', None, None, None, None)


@pytest.mark.parametrize('length', ['long', 0, -5, None])
def test_add_catalogue_item_refuses_wrong_length(empty_db, length):
    # la longueur est mal renseignée
    with pytest.raises(ValueError):
        add_catalogue_item(None, 'Drops', 'Safran', length, 50, None, '99',
                           'solid', 'rouge', None, None, None, None)

@pytest.mark.parametrize('brand', ['', '     ', None])
def test_add_catalogue_item_refuses_no_brand(empty_db, brand):
    # la marque est mal renseignée
    with pytest.raises(ValueError):
        add_catalogue_item(None, brand, 'Safran', 160, 50, None, '99',
                           'solid', 'rouge', None, None, None, None)

@pytest.mark.parametrize('yarn', ['', '     ', None])
def test_add_catalogue_item_refuses_no_yarn(empty_db, yarn):
    # la gamme est mal renseignée
    with pytest.raises(ValueError):
        add_catalogue_item(None, 'Drops', yarn, 160, 50, None, '99',
                           'solid', 'rouge', None, None, None, None)
