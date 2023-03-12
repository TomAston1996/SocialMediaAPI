import pytest

from app.calculations import add, BankAccount, InsufficientFunds

# Pytest requires naming convention for the .py file and function of 'test_....'
# Pytest command: pytest -v -s

@pytest.fixture
def zero_bank_account(): 
    return BankAccount()


@pytest.fixture
def bank_account(): 
    return BankAccount(50)


@pytest.mark.parametrize('num1, num2, expected', [
    (3, 2, 5), #test 1: 3+2=5
    (1, 2, 3), #test 2: 1+2=3
    (5, 3, 8)  #test 3: 5+3=8
    ])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account): 
    bank_account.withdraw(5) 
    assert bank_account.balance == 45


def test_deposit(bank_account): 
    bank_account.deposit(5) 
    assert bank_account.balance == 55


def test_collect_interest(bank_account):
    bank_account.collect_interest() 
    assert int(bank_account.balance) == 55


@pytest.mark.parametrize('deposit, withdraw, expected', [
    (200, 50, 150), 
    (50, 10, 40), 
    (1200, 200, 1000) 
    ])
def test_bank_transaction(zero_bank_account, deposit, withdraw, expected): 
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(zero_bank_account): 
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(50)

