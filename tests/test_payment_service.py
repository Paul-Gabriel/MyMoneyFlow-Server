import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from models.plata import Plata

from services.payment_service import (
    add_payment,
    get_payments_by_user,
    get_payment_by_id,
    update_payment_by_id,
    delete_payment_by_id,
)

@pytest.fixture
def mock_payments_collection():
    with patch("services.payment_service.payments_collection") as mock_collection:
        yield mock_collection

@pytest.fixture
def mock_get_user_by_id():
    with patch("services.payment_service.get_user_by_id") as mock_user_service:
        yield mock_user_service

def test_add_payment_success(mock_payments_collection, mock_get_user_by_id):
    mock_get_user_by_id.return_value = {"id": "user123"}
    payment = Plata(user_ref="user123", suma=100.0, descriere="Test payment")
    add_payment(payment)
    mock_payments_collection.add.assert_called_once_with(payment.model_dump())

def test_add_payment_user_not_found(mock_get_user_by_id):
    mock_get_user_by_id.return_value = None
    payment = Plata(user_ref="user123", suma=100.0, descriere="Test payment")
    with pytest.raises(HTTPException) as exc_info:
        add_payment(payment)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

def test_add_payment_negative_sum(mock_get_user_by_id):
    mock_get_user_by_id.return_value = {"id": "user123"}
    payment = Plata(user_ref="user123", suma=-50.0, descriere="Invalid payment")
    with pytest.raises(ValueError) as exc_info:
        add_payment(payment)
    assert str(exc_info.value) == "Suma trebuie să fie pozitivă."

def test_get_payments_by_user_success(mock_payments_collection):
    mock_payments_collection.where.return_value.stream.return_value = [
        MagicMock(id="payment1", to_dict=lambda: {"suma": 100.0, "descriere": "Test payment"})
    ]
    result = get_payments_by_user("user123")
    assert result == [{"plata_id": "payment1", "suma": 100.0, "descriere": "Test payment"}]

def test_get_payments_by_user_not_found(mock_payments_collection):
    mock_payments_collection.where.return_value.stream.return_value = []
    with pytest.raises(HTTPException) as exc_info:
        get_payments_by_user("user123")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "No payments found for this user"

def test_get_payment_by_id_success(mock_payments_collection):
    mock_payments_collection.document.return_value.get.return_value = MagicMock(
        exists=True, id="payment1", to_dict=lambda: {"suma": 100.0, "descriere": "Test payment"}
    )
    result = get_payment_by_id("payment1")
    assert result == {"plata_id": "payment1", "suma": 100.0, "descriere": "Test payment"}

def test_get_payment_by_id_not_found(mock_payments_collection):
    mock_payments_collection.document.return_value.get.return_value = MagicMock(exists=False)
    with pytest.raises(HTTPException) as exc_info:
        get_payment_by_id("payment1")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Payment not found"

def test_update_payment_by_id_success(mock_payments_collection):
    mock_payments_collection.document.return_value.get.return_value = MagicMock(exists=True)
    payment = Plata(user_ref="user123", suma=150.0, descriere="Updated payment")
    update_payment_by_id("payment1", payment)
    mock_payments_collection.document.return_value.update.assert_called_once_with(payment.model_dump())

def test_update_payment_by_id_not_found(mock_payments_collection):
    mock_payments_collection.document.return_value.get.return_value = MagicMock(exists=False)
    payment = Plata(user_ref="user123", suma=150.0, descriere="Updated payment")
    with pytest.raises(HTTPException) as exc_info:
        update_payment_by_id("payment1", payment)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Payment not found"

def test_delete_payment_by_id_success(mock_payments_collection):
    mock_payments_collection.document.return_value.get.return_value = MagicMock(exists=True)
    delete_payment_by_id("payment1")
    mock_payments_collection.document.return_value.delete.assert_called_once()

def test_delete_payment_by_id_not_found(mock_payments_collection):
    mock_payments_collection.document.return_value.get.return_value = MagicMock(exists=False)
    with pytest.raises(HTTPException) as exc_info:
        delete_payment_by_id("payment1")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Payment not found"