"""Test module for BankAccount class following TDD principles."""

import pytest
from decimal import Decimal
from src.bank_account import BankAccount


class TestBankAccountCreation:
    """Test cases for BankAccount creation and instantiation."""
    
    def test_bank_account_can_be_instantiated_when_given_valid_account_number_and_initial_balance(self):
        """Test that BankAccount can be instantiated with valid parameters."""
        # Arrange
        account_number = "123456789"
        initial_balance = 100.0
        
        # Act
        account = BankAccount(account_number, initial_balance)
        
        # Assert
        assert account is not None
        assert isinstance(account, BankAccount)
    
    def test_bank_account_stores_account_number_when_created_with_valid_account_number(self):
        """Test that BankAccount correctly stores the account number."""
        # Arrange
        account_number = "123456789"
        initial_balance = 100.0
        
        # Act
        account = BankAccount(account_number, initial_balance)
        
        # Assert
        assert account.account_number == account_number
    
    def test_bank_account_stores_initial_balance_when_created_with_valid_balance(self):
        """Test that BankAccount correctly stores the initial balance."""
        # Arrange
        account_number = "123456789"
        initial_balance = 100.0
        
        # Act
        account = BankAccount(account_number, initial_balance)
        
        # Assert
        assert account.balance == initial_balance


class TestBankAccountValidation:
    """Test cases for BankAccount validation logic."""
    
    def test_bank_account_creation_fails_when_given_negative_initial_balance(self):
        """Test that BankAccount creation fails with negative initial balance."""
        # Arrange
        account_number = "123456789"
        negative_balance = -100.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Initial balance cannot be negative"):
            BankAccount(account_number, negative_balance)
    
    def test_bank_account_creation_fails_when_given_invalid_account_number_format(self):
        """Test that BankAccount creation fails with invalid account number format."""
        # Arrange
        invalid_account_number = "12345"  # Too short
        initial_balance = 100.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Account number must be exactly 9 digits"):
            BankAccount(invalid_account_number, initial_balance)
    
    def test_bank_account_creation_fails_when_given_empty_account_number(self):
        """Test that BankAccount creation fails with empty account number."""
        # Arrange
        empty_account_number = ""
        initial_balance = 100.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Account number cannot be empty"):
            BankAccount(empty_account_number, initial_balance)


class TestBankAccountDeposit:
    """Test cases for BankAccount deposit functionality."""
    
    def test_deposit_increases_balance_when_given_valid_amount(self):
        """Test that deposit increases account balance by the deposited amount."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        deposit_amount = 50.0
        expected_balance = 150.0
        
        # Act
        result = account.deposit(deposit_amount)
        
        # Assert
        assert account.balance == expected_balance
        assert result is True
    
    def test_deposit_fails_when_given_negative_amount(self):
        """Test that deposit fails when given a negative amount."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        negative_amount = -50.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Amount must be positive"):
            account.deposit(negative_amount)
    
    def test_deposit_fails_when_given_zero_amount(self):
        """Test that deposit fails when given zero amount."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        zero_amount = 0.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Amount must be positive"):
            account.deposit(zero_amount)
    
    def test_deposit_fails_when_given_non_numeric_amount(self):
        """Test that deposit fails when given non-numeric amount."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        
        # Act & Assert
        with pytest.raises(TypeError):
            account.deposit("not_a_number")


class TestBankAccountWithdraw:
    """Test cases for BankAccount withdraw functionality."""
    
    def test_withdraw_decreases_balance_when_given_valid_amount(self):
        """Test that withdraw decreases account balance by the withdrawn amount."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        withdraw_amount = 30.0
        expected_balance = 70.0
        
        # Act
        result = account.withdraw(withdraw_amount)
        
        # Assert
        assert account.balance == expected_balance
        assert result is True
    
    def test_withdraw_fails_when_amount_exceeds_balance(self):
        """Test that withdraw fails when amount exceeds current balance."""
        # Arrange
        account = BankAccount("123456789", 50.0)
        withdraw_amount = 100.0
        original_balance = 50.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Insufficient funds"):
            account.withdraw(withdraw_amount)
        
        # Verify balance unchanged
        assert account.balance == original_balance
    
    def test_withdraw_succeeds_when_withdrawing_exact_balance(self):
        """Test that withdraw succeeds when withdrawing exact balance amount."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        withdraw_amount = 100.0
        expected_balance = 0.0
        
        # Act
        result = account.withdraw(withdraw_amount)
        
        # Assert
        assert account.balance == expected_balance
        assert result is True
    
    def test_withdraw_fails_when_given_negative_amount(self):
        """Test that withdraw fails when given a negative amount."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        negative_amount = -50.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Amount must be positive"):
            account.withdraw(negative_amount)
    
    def test_withdraw_fails_when_given_zero_amount(self):
        """Test that withdraw fails when given zero amount."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        zero_amount = 0.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Amount must be positive"):
            account.withdraw(zero_amount)
    
    def test_withdraw_fails_when_given_non_numeric_amount(self):
        """Test that withdraw fails when given non-numeric amount."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        
        # Act & Assert
        with pytest.raises(TypeError):
            account.withdraw("not_a_number")


class TestBankAccountBalanceInquiry:
    """Test cases for BankAccount balance inquiry functionality."""
    
    def test_balance_property_returns_current_balance(self):
        """Test that balance property returns the current account balance."""
        # Arrange
        account = BankAccount("123456789", 150.0)
        expected_balance = 150.0
        
        # Act
        actual_balance = account.balance
        
        # Assert
        assert actual_balance == expected_balance
    
    def test_balance_reflects_balance_after_deposit(self):
        """Test that balance property returns updated balance after deposit operations."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        deposit_amount = 50.0
        expected_balance = 150.0
        
        # Act
        account.deposit(deposit_amount)
        actual_balance = account.balance
        
        # Assert
        assert actual_balance == expected_balance
    
    def test_balance_reflects_balance_after_withdrawal(self):
        """Test that balance property returns updated balance after withdrawal operations."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        withdraw_amount = 30.0
        expected_balance = 70.0
        
        # Act
        account.withdraw(withdraw_amount)
        actual_balance = account.balance
        
        # Assert
        assert actual_balance == expected_balance
    
    def test_balance_cannot_be_modified_directly(self):
        """Test that balance attribute cannot be modified directly from outside."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        original_balance = 100.0
        
        # Act - Attempt to modify balance directly
        try:
            account.balance = 999.0  # This should not change the actual balance
            modified_balance = account.balance
        except AttributeError:
            # If balance is properly protected, this exception is expected
            modified_balance = account.balance
        
        # Assert - Balance should remain unchanged or properly protected
        assert modified_balance == original_balance


class TestBankAccountTransactionHistory:
    """Test cases for BankAccount transaction history functionality."""
    
    def test_get_transaction_history_returns_empty_list_for_new_account(self):
        """Test that get_transaction_history returns empty list for new account."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        
        # Act
        transactions = account.get_transaction_history()
        
        # Assert
        assert transactions == []
        assert len(transactions) == 0
    
    def test_deposit_transaction_is_recorded_in_history(self):
        """Test that deposit transactions are recorded in transaction history."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        deposit_amount = 50.0
        
        # Act
        account.deposit(deposit_amount)
        transactions = account.get_transaction_history()
        
        # Assert
        assert len(transactions) == 1
        assert transactions[0]['type'] == 'deposit'
        assert transactions[0]['amount'] == deposit_amount
    
    def test_withdrawal_transaction_is_recorded_in_history(self):
        """Test that withdrawal transactions are recorded in transaction history."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        withdraw_amount = 30.0
        
        # Act
        account.withdraw(withdraw_amount)
        transactions = account.get_transaction_history()
        
        # Assert
        assert len(transactions) == 1
        assert transactions[0]['type'] == 'withdrawal'
        assert transactions[0]['amount'] == withdraw_amount
    
    def test_transaction_includes_timestamp(self):
        """Test that each transaction includes a timestamp."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        
        # Act
        account.deposit(25.0)
        transactions = account.get_transaction_history()
        
        # Assert
        assert len(transactions) == 1
        assert 'timestamp' in transactions[0]
        assert isinstance(transactions[0]['timestamp'], str)
    
    def test_multiple_transactions_are_preserved_in_order(self):
        """Test that multiple transactions are preserved in chronological order."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        
        # Act
        account.deposit(50.0)  # First transaction
        account.withdraw(20.0)  # Second transaction
        account.deposit(30.0)  # Third transaction
        transactions = account.get_transaction_history()
        
        # Assert
        assert len(transactions) == 3
        assert transactions[0]['type'] == 'deposit'
        assert transactions[0]['amount'] == 50.0
        assert transactions[1]['type'] == 'withdrawal'
        assert transactions[1]['amount'] == 20.0
        assert transactions[2]['type'] == 'deposit'
        assert transactions[2]['amount'] == 30.0


class TestBankAccountEdgeCases:
    """Test cases for BankAccount edge cases and precision handling."""
    
    def test_floating_point_precision_deposit(self):
        """Test that floating-point precision issues are handled correctly for deposits."""
        # Arrange
        account = BankAccount("123456789", 0.1)
        
        # Act - This is known to cause floating-point precision issues
        account.deposit(0.2)
        
        # Assert - With Decimal precision, should be exactly 0.30
        balance = account.balance
        assert balance == Decimal('0.30')
    
    def test_floating_point_precision_withdrawal(self):
        """Test that floating-point precision issues are handled correctly for withdrawals."""
        # Arrange
        account = BankAccount("123456789", 1.0)
        
        # Act
        account.withdraw(0.9)
        
        # Assert - With Decimal precision, should be exactly 0.10
        balance = account.balance
        assert balance == Decimal('0.10')
    
    def test_multiple_small_deposits_precision(self):
        """Test precision with multiple small decimal deposits."""
        # Arrange
        account = BankAccount("123456789", 0.0)
        
        # Act - Add 0.01 ten times
        for _ in range(10):
            account.deposit(0.01)
        
        # Assert - With Decimal precision, should be exactly 0.10
        balance = account.balance
        assert balance == Decimal('0.10')
    
    def test_very_large_deposit_amount(self):
        """Test handling of very large deposit amounts."""
        # Arrange
        account = BankAccount("123456789", 0)
        large_amount = Decimal('999999999.99')
        
        # Act
        result = account.deposit(large_amount)
        
        # Assert
        assert result is True
        assert account.balance == large_amount
    
    def test_very_large_withdrawal_amount(self):
        """Test handling of very large withdrawal amounts."""
        # Arrange
        large_balance = Decimal('1000000000.00')
        account = BankAccount("123456789", large_balance)
        withdraw_amount = Decimal('999999999.99')
        
        # Act
        result = account.withdraw(withdraw_amount)
        
        # Assert
        assert result is True
        assert account.balance == Decimal('0.01')
    
    def test_maximum_decimal_precision(self):
        """Test that amounts are properly rounded to 2 decimal places."""
        # Arrange
        account = BankAccount("123456789", 0)
        precise_amount = 10.999  # Should round to 11.00
        
        # Act
        account.deposit(precise_amount)
        
        # Assert
        assert account.balance == Decimal('11.00')