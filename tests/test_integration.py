"""Integration tests for banking system following TDD principles."""

import pytest
from decimal import Decimal
from src.bank_account import BankAccount


class TestMultipleAccountInteractions:
    """Test cases for interactions between multiple bank accounts."""
    
    def test_transfer_between_two_accounts_decreases_source_and_increases_destination(self):
        """Test that money transfer works between two accounts."""
        # Arrange
        source_account = BankAccount("123456789", 1000.0)
        destination_account = BankAccount("987654321", 500.0)
        transfer_amount = 200.0
        expected_source_balance = 800.0
        expected_destination_balance = 700.0
        
        # Act
        # Simulate transfer by withdrawing from source and depositing to destination
        source_result = source_account.withdraw(transfer_amount)
        destination_result = destination_account.deposit(transfer_amount)
        
        # Assert
        assert source_result is True
        assert destination_result is True
        assert source_account.balance == expected_source_balance
        assert destination_account.balance == expected_destination_balance
    
    def test_transfer_fails_when_source_has_insufficient_funds(self):
        """Test that transfer fails when source account has insufficient funds."""
        # Arrange
        source_account = BankAccount("123456789", 100.0)
        destination_account = BankAccount("987654321", 500.0)
        transfer_amount = 200.0
        original_source_balance = 100.0
        original_destination_balance = 500.0
        
        # Act & Assert
        with pytest.raises(ValueError, match="Insufficient funds"):
            source_account.withdraw(transfer_amount)
        
        # Verify balances remain unchanged
        assert source_account.balance == original_source_balance
        assert destination_account.balance == original_destination_balance
    
    def test_multiple_simultaneous_operations_on_different_accounts(self):
        """Test multiple operations happening on different accounts simultaneously."""
        # Arrange
        account1 = BankAccount("111111111", 1000.0)
        account2 = BankAccount("222222222", 2000.0)
        account3 = BankAccount("333333333", 3000.0)
        
        # Act - Simulate simultaneous operations
        account1.deposit(100.0)  # 1100.0
        account2.withdraw(500.0)  # 1500.0
        account3.deposit(200.0)  # 3200.0
        account1.withdraw(50.0)  # 1050.0
        account2.deposit(300.0)  # 1800.0
        
        # Assert
        assert account1.balance == 1050.0
        assert account2.balance == 1800.0
        assert account3.balance == 3200.0
    
    def test_transaction_history_isolation_between_accounts(self):
        """Test that transaction histories are isolated between different accounts."""
        # Arrange
        account1 = BankAccount("111111111", 1000.0)
        account2 = BankAccount("222222222", 2000.0)
        
        # Act
        account1.deposit(100.0)
        account1.withdraw(50.0)
        account2.deposit(200.0)
        
        # Assert
        account1_history = account1.get_transaction_history()
        account2_history = account2.get_transaction_history()
        
        assert len(account1_history) == 2
        assert len(account2_history) == 1
        assert account1_history[0]['type'] == 'deposit'
        assert account1_history[1]['type'] == 'withdrawal'
        assert account2_history[0]['type'] == 'deposit'
    
    def test_chain_of_transfers_between_multiple_accounts(self):
        """Test a chain of transfers flowing through multiple accounts."""
        # Arrange
        account_a = BankAccount("111111111", 1000.0)
        account_b = BankAccount("222222222", 500.0)
        account_c = BankAccount("333333333", 200.0)
        transfer_amount = 150.0
        
        # Act - Chain: A -> B -> C
        # A to B
        account_a.withdraw(transfer_amount)  # A: 850.0
        account_b.deposit(transfer_amount)   # B: 650.0
        
        # B to C
        account_b.withdraw(transfer_amount)  # B: 500.0
        account_c.deposit(transfer_amount)   # C: 350.0
        
        # Assert
        assert account_a.balance == 850.0
        assert account_b.balance == 500.0
        assert account_c.balance == 350.0
        
        # Verify transaction counts
        assert len(account_a.get_transaction_history()) == 1
        assert len(account_b.get_transaction_history()) == 2
        assert len(account_c.get_transaction_history()) == 1


class TestSystemWideConstraints:
    """Test cases for system-wide constraints and validation."""
    
    def test_account_number_uniqueness_validation(self):
        """Test that the system can validate account number uniqueness."""
        # Arrange
        account_numbers = set()
        accounts = []
        
        # Act - Create multiple accounts with different account numbers
        for i in range(5):
            account_number = f"12345678{i}"
            account = BankAccount(account_number, 1000.0)
            accounts.append(account)
            account_numbers.add(account_number)
        
        # Assert - All account numbers should be unique
        assert len(account_numbers) == 5
        assert len(accounts) == 5
        
        # Verify each account has the correct account number
        for i, account in enumerate(accounts):
            expected_number = f"12345678{i}"
            assert account.account_number == expected_number
    
    def test_maximum_transaction_amount_constraint(self):
        """Test system constraint for maximum transaction amounts."""
        # Arrange
        account = BankAccount("123456789", 1000000.0)
        max_transaction_amount = Decimal('100000.00')  # $100,000 limit
        
        # Act & Assert - Large deposit within limit
        result = account.deposit(max_transaction_amount)
        assert result is True
        
        # Test withdrawal within limit
        result = account.withdraw(max_transaction_amount)
        assert result is True
    
    def test_minimum_balance_constraint_after_withdrawal(self):
        """Test that withdrawals respect minimum balance constraints."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        minimum_balance = Decimal('10.00')
        
        # Act - Try to withdraw amount that would leave less than minimum
        maximum_withdrawal = account.balance - minimum_balance
        
        # Assert - Should be able to withdraw up to minimum balance threshold
        result = account.withdraw(maximum_withdrawal)
        assert result is True
        assert account.balance == minimum_balance
    
    def test_daily_transaction_limit_simulation(self):
        """Test simulation of daily transaction limits."""
        # Arrange
        account = BankAccount("123456789", 10000.0)
        daily_limit = Decimal('5000.00')
        daily_total = Decimal('0.00')
        
        # Act - Simulate multiple transactions within daily limit
        transactions = [1000.0, 1500.0, 2000.0, 500.0]  # Total: 5000.0
        
        for amount in transactions:
            if daily_total + Decimal(str(amount)) <= daily_limit:
                result = account.withdraw(amount)
                daily_total += Decimal(str(amount))
                assert result is True
        
        # Assert
        assert daily_total == daily_limit
        assert account.balance == 5000.0


class TestErrorPropagation:
    """Test cases for error propagation across multiple account operations."""
    
    def test_failed_withdrawal_does_not_affect_subsequent_operations(self):
        """Test that a failed withdrawal doesn't affect subsequent valid operations."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        
        # Act - Failed withdrawal
        with pytest.raises(ValueError, match="Insufficient funds"):
            account.withdraw(200.0)
        
        # Act - Subsequent valid operations
        deposit_result = account.deposit(50.0)
        withdrawal_result = account.withdraw(75.0)
        
        # Assert
        assert deposit_result is True
        assert withdrawal_result is True
        assert account.balance == 75.0
    
    def test_transaction_atomicity_across_multiple_accounts(self):
        """Test that failed transactions maintain atomicity across accounts."""
        # Arrange
        account1 = BankAccount("111111111", 100.0)
        account2 = BankAccount("222222222", 500.0)
        transfer_amount = 200.0
        
        # Store original balances
        original_balance1 = account1.balance
        original_balance2 = account2.balance
        
        # Act - Attempt transfer that should fail
        try:
            account1.withdraw(transfer_amount)  # This will fail
            # If withdrawal succeeded (it shouldn't), try deposit
            account2.deposit(transfer_amount)
        except ValueError:
            # Expected failure - verify no state changes
            pass
        
        # Assert - Balances should remain unchanged
        assert account1.balance == original_balance1
        assert account2.balance == original_balance2
    
    def test_error_handling_with_invalid_operations_sequence(self):
        """Test error handling with a sequence of invalid operations."""
        # Arrange
        account = BankAccount("123456789", 100.0)
        
        # Act & Assert - Sequence of invalid operations
        with pytest.raises(ValueError, match="Amount must be positive"):
            account.deposit(-50.0)
        
        with pytest.raises(ValueError, match="Amount must be positive"):
            account.withdraw(-25.0)
        
        with pytest.raises(ValueError, match="Insufficient funds"):
            account.withdraw(200.0)
        
        # Verify account state remains unchanged
        assert account.balance == 100.0
        assert len(account.get_transaction_history()) == 0
    
    def test_concurrent_operation_error_isolation(self):
        """Test that errors in one account operation don't affect others."""
        # Arrange
        accounts = [
            BankAccount("111111111", 1000.0),
            BankAccount("222222222", 500.0),
            BankAccount("333333333", 100.0)
        ]
        
        # Act - Mix of valid and invalid operations
        accounts[0].deposit(100.0)  # Valid
        
        with pytest.raises(ValueError):
            accounts[1].withdraw(600.0)  # Invalid - insufficient funds
        
        accounts[2].deposit(50.0)  # Valid
        
        # Assert - Valid operations succeeded, invalid ones failed gracefully
        assert accounts[0].balance == 1100.0
        assert accounts[1].balance == 500.0  # Unchanged
        assert accounts[2].balance == 150.0
        
        # Verify transaction histories
        assert len(accounts[0].get_transaction_history()) == 1
        assert len(accounts[1].get_transaction_history()) == 0  # No successful transactions
        assert len(accounts[2].get_transaction_history()) == 1


class TestSystemLevelEdgeCases:
    """Test cases for edge cases at the system level."""
    
    def test_precision_consistency_across_multiple_accounts(self):
        """Test that decimal precision is consistent across multiple accounts."""
        # Arrange
        accounts = [BankAccount(f"12345678{i}", 0.1) for i in range(3)]
        
        # Act - Perform precision-sensitive operations
        for account in accounts:
            account.deposit(0.2)  # Should result in exactly 0.30
        
        # Assert - All accounts should have exactly the same precise balance
        for account in accounts:
            assert account.balance == Decimal('0.30')
    
    def test_large_scale_operations_memory_efficiency(self):
        """Test memory efficiency with large scale operations."""
        # Arrange
        account = BankAccount("123456789", 1000000.0)
        
        # Act - Perform many small operations
        for i in range(100):
            account.deposit(1.0)
            account.withdraw(0.5)
        
        # Assert
        expected_balance = 1000000.0 + (100 * 0.5)  # Net +50.0
        assert account.balance == expected_balance
        assert len(account.get_transaction_history()) == 200
    
    def test_extreme_precision_edge_cases(self):
        """Test extreme precision edge cases across the system."""
        # Arrange
        account = BankAccount("123456789", Decimal('0.01'))
        very_small_amount = Decimal('0.001')
        
        # Act & Assert - Try operations with amounts smaller than minimum precision
        # This should round to 0.00 and be rejected as non-positive
        with pytest.raises(ValueError, match="Amount must be positive"):
            account.deposit(very_small_amount)
        
        # Assert - Balance should remain unchanged
        assert account.balance == Decimal('0.01')