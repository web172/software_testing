def transfer(accountA, accountB, amount):
    if amount <= 0:
        raise ValueError("转账金额必须为正数")
    if accountA['balance'] < amount:
        raise ValueError("余额不足")
    accountA['balance'] -= amount
    accountB['balance'] += amount
    return True
import pytest
def test_transfer_normal():
    a = {"balance": 100}
    b = {"balance": 50}
    assert transfer(a, b, 30) == True
    assert a["balance"] == 70
    assert b["balance"] == 80
def test_transfer_negative():
    a  , b = {"balance": 100}, {"balance": 50}
    with pytest.raises(ValueError):
        transfer(a, b, -10)
def test_transfer_insufficient_balance():
    a, b = {"balance": 20}, {"balance": 50}
    with pytest.raises(ValueError):
        transfer(a, b, 50)