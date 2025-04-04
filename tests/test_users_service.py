import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from models.user import User

from services.user_service import (
    add_user,
    get_user_by_id,
    get_all_users,
    get_user_by_email,
    update_user_by_id,
    delete_user_by_id,
)

@pytest.fixture
def mock_users_collection():
    with patch("services.user_service.users_collection") as mock_collection:
        yield mock_collection

def test_add_user_success(mock_users_collection):
    mock_users_collection.where.return_value.get.return_value = []
    user = User(
        email="test@example.com",
        procentNecesitati=50,
        procentDorinte=30,
        procentEconomii=20,
        venit=1000,
    )
    add_user(user)
    mock_users_collection.add.assert_called_once_with(user.model_dump())

def test_add_user_email_exists(mock_users_collection):
    mock_users_collection.where.return_value.get.return_value = [MagicMock()]
    user = User(
        email="test@example.com",
        procentNecesitati=50,
        procentDorinte=30,
        procentEconomii=20,
        venit=1000,
    )
    with pytest.raises(ValueError) as exc_info:
        add_user(user)
    assert str(exc_info.value) == "Un utilizator cu acest email există deja."

def test_add_user_invalid_percentages(mock_users_collection):
    mock_users_collection.where.return_value.get.return_value = []
    user = User(
        email="test@example.com",
        procentNecesitati=40,
        procentDorinte=30,
        procentEconomii=20,
        venit=1000,
    )
    with pytest.raises(ValueError) as exc_info:
        add_user(user)
    assert str(exc_info.value) == "Suma procentelor trebuie să fie 100%."

def test_add_user_negative_income(mock_users_collection):
    mock_users_collection.where.return_value.get.return_value = []
    user = User(
        email="test@example.com",
        procentNecesitati=50,
        procentDorinte=30,
        procentEconomii=20,
        venit=-1000,
    )
    with pytest.raises(ValueError) as exc_info:
        add_user(user)
    assert str(exc_info.value) == "Venitul trebuie să fie pozitiv."

def test_get_user_by_id_success(mock_users_collection):
    mock_users_collection.document.return_value.get.return_value = MagicMock(
        exists=True, id="user123", to_dict=lambda: {"email": "test@example.com"}
    )
    result = get_user_by_id("user123")
    assert result == {"user_id": "user123", "email": "test@example.com"}

def test_get_user_by_id_not_found(mock_users_collection):
    mock_users_collection.document.return_value.get.return_value = MagicMock(exists=False)
    with pytest.raises(HTTPException) as exc_info:
        get_user_by_id("user123")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

def test_get_all_users_success(mock_users_collection):
    mock_users_collection.get.return_value = [
        MagicMock(id="user1", to_dict=lambda: {"email": "user1@example.com"}),
        MagicMock(id="user2", to_dict=lambda: {"email": "user2@example.com"}),
    ]
    result = get_all_users()
    assert result == [
        {"user_id": "user1", "email": "user1@example.com"},
        {"user_id": "user2", "email": "user2@example.com"},
    ]

def test_get_user_by_email_success(mock_users_collection):
    mock_users_collection.where.return_value.get.return_value = [
        MagicMock(id="user123", to_dict=lambda: {"email": "test@example.com"})
    ]
    result = get_user_by_email("test@example.com")
    assert result == {"user_id": "user123", "email": "test@example.com"}

def test_get_user_by_email_not_found(mock_users_collection):
    mock_users_collection.where.return_value.get.return_value = []
    with pytest.raises(HTTPException) as exc_info:
        get_user_by_email("test@example.com")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

def test_update_user_by_id_success(mock_users_collection):
    mock_users_collection.document.return_value.get.return_value = MagicMock(exists=True)
    user = User(
        email="updated@example.com",
        procentNecesitati=50,
        procentDorinte=30,
        procentEconomii=20,
        venit=2000,
    )
    update_user_by_id("user123", user)
    mock_users_collection.document.return_value.update.assert_called_once_with(user.model_dump())

def test_update_user_by_id_not_found(mock_users_collection):
    mock_users_collection.document.return_value.get.return_value = MagicMock(exists=False)
    user = User(
        email="updated@example.com",
        procentNecesitati=50,
        procentDorinte=30,
        procentEconomii=20,
        venit=2000,
    )
    with pytest.raises(HTTPException) as exc_info:
        update_user_by_id("user123", user)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

def test_delete_user_by_id_success(mock_users_collection):
    mock_users_collection.document.return_value.get.return_value = MagicMock(exists=True)
    delete_user_by_id("user123")
    mock_users_collection.document.return_value.delete.assert_called_once()

def test_delete_user_by_id_not_found(mock_users_collection):
    mock_users_collection.document.return_value.get.return_value = MagicMock(exists=False)
    with pytest.raises(HTTPException) as exc_info:
        delete_user_by_id("user123")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"