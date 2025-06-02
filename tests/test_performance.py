"""Performance tests for banking system following TDD principles."""

import pytest
import time
import psutil
import os
from decimal import Decimal
from src.bank_account import BankAccount


class TestLargeVolumeTransactions:
    """Test cases for large volume transaction performance."""
    
    def test_1000_deposit_operations_performance(self):
        """Test performance with 1000 deposit operations."""
        # Arrange
        account = BankAccount("123456789", 0.0)
        num_operations = 1000
        deposit_amount = 1.0
        
        # Act
        start_time = time.time()
        
        for i in range(num_operations):
            account.deposit(deposit_amount)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        assert account.balance == num_operations * deposit_amount
        assert len(account.get_transaction_history()) == num_operations
        assert execution_time < 1.0  # Should complete within 1 second
        print(f"1000 deposits completed in {execution_time:.3f} seconds")
    
    def test_1000_withdrawal_operations_performance(self):
        """Test performance with 1000 withdrawal operations."""
        # Arrange
        initial_balance = 2000.0
        account = BankAccount("123456789", initial_balance)
        num_operations = 1000
        withdrawal_amount = 1.0
        
        # Act
        start_time = time.time()
        
        for i in range(num_operations):
            account.withdraw(withdrawal_amount)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        expected_balance = initial_balance - (num_operations * withdrawal_amount)
        assert account.balance == expected_balance
        assert len(account.get_transaction_history()) == num_operations
        assert execution_time < 1.0  # Should complete within 1 second
        print(f"1000 withdrawals completed in {execution_time:.3f} seconds")
    
    def test_5000_mixed_operations_performance(self):
        """Test performance with 5000 mixed operations."""
        # Arrange
        account = BankAccount("123456789", 10000.0)
        num_operations = 5000
        
        # Act
        start_time = time.time()
        
        for i in range(num_operations):
            if i % 2 == 0:
                account.deposit(1.0)
            else:
                account.withdraw(0.5)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        # Net change: 2500 deposits of 1.0 and 2500 withdrawals of 0.5 = +1250.0
        expected_balance = 10000.0 + 1250.0
        assert account.balance == expected_balance
        assert len(account.get_transaction_history()) == num_operations
        assert execution_time < 2.0  # Should complete within 2 seconds
        print(f"5000 mixed operations completed in {execution_time:.3f} seconds")
    
    def test_transaction_history_retrieval_performance(self):
        """Test performance of transaction history retrieval with large datasets."""
        # Arrange
        account = BankAccount("123456789", 1000.0)
        num_operations = 1000
        
        # Create large transaction history
        for i in range(num_operations):
            account.deposit(1.0)
        
        # Act - Test history retrieval performance
        start_time = time.time()
        
        for _ in range(100):  # Retrieve history 100 times
            history = account.get_transaction_history()
            assert len(history) == num_operations
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        assert execution_time < 0.5  # Should complete 100 retrievals within 0.5 seconds
        print(f"100 history retrievals (1000 transactions each) completed in {execution_time:.3f} seconds")


class TestMemoryUsage:
    """Test cases for memory usage patterns."""
    
    def test_memory_usage_with_large_transaction_history(self):
        """Test memory usage patterns with large transaction histories."""
        # Arrange
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        account = BankAccount("123456789", 1000.0)
        num_operations = 2000
        
        # Act
        for i in range(num_operations):
            account.deposit(1.0)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Assert
        assert len(account.get_transaction_history()) == num_operations
        assert memory_increase < 50  # Should not increase memory by more than 50MB
        print(f"Memory increase for 2000 transactions: {memory_increase:.2f} MB")
    
    def test_memory_efficiency_multiple_accounts(self):
        """Test memory efficiency with multiple accounts."""
        # Arrange
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        num_accounts = 100
        accounts = []
        
        # Act
        for i in range(num_accounts):
            account = BankAccount(f"1234567{i:02d}", 1000.0)
            
            # Perform some operations on each account
            for j in range(10):
                account.deposit(10.0)
                account.withdraw(5.0)
            
            accounts.append(account)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Assert
        assert len(accounts) == num_accounts
        for account in accounts:
            assert len(account.get_transaction_history()) == 20
        
        assert memory_increase < 100  # Should not increase memory by more than 100MB
        print(f"Memory increase for 100 accounts (20 transactions each): {memory_increase:.2f} MB")


class TestConcurrentOperationSimulation:
    """Test cases simulating concurrent operations."""
    
    def test_rapid_successive_operations_same_account(self):
        """Test rapid successive operations on the same account."""
        # Arrange
        account = BankAccount("123456789", 10000.0)
        operations = []
        
        # Prepare operation sequence
        for i in range(1000):
            if i % 3 == 0:
                operations.append(('deposit', 10.0))
            elif i % 3 == 1:
                operations.append(('withdraw', 5.0))
            else:
                operations.append(('deposit', 15.0))
        
        # Act
        start_time = time.time()
        
        for operation_type, amount in operations:
            if operation_type == 'deposit':
                account.deposit(amount)
            else:
                account.withdraw(amount)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        # Calculate expected balance: 334 deposits of 10.0, 333 withdrawals of 5.0, 333 deposits of 15.0
        # Net: (334 * 10.0) + (333 * 15.0) - (333 * 5.0) = 3340 + 4995 - 1665 = 6670
        expected_balance = 10000.0 + 6670.0
        assert account.balance == expected_balance
        assert len(account.get_transaction_history()) == 1000
        assert execution_time < 1.0
        print(f"1000 rapid operations completed in {execution_time:.3f} seconds")
    
    def test_interleaved_operations_multiple_accounts(self):
        """Test interleaved operations across multiple accounts."""
        # Arrange
        accounts = [BankAccount(f"12345678{i}", 1000.0) for i in range(10)]
        num_operations_per_account = 100
        
        # Act
        start_time = time.time()
        
        for i in range(num_operations_per_account):
            for j, account in enumerate(accounts):
                if (i + j) % 2 == 0:
                    account.deposit(5.0)
                else:
                    account.withdraw(2.0)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        total_operations = len(accounts) * num_operations_per_account
        assert total_operations == 1000
        
        for account in accounts:
            assert len(account.get_transaction_history()) == num_operations_per_account
        
        assert execution_time < 1.0
        print(f"1000 interleaved operations across 10 accounts completed in {execution_time:.3f} seconds")


class TestEdgeCasePerformance:
    """Test cases for edge case performance scenarios."""
    
    def test_precision_intensive_operations_performance(self):
        """Test performance with precision-intensive decimal operations."""
        # Arrange
        account = BankAccount("123456789", 0.0)
        num_operations = 1000
        precise_amount = Decimal('0.01')
        
        # Act
        start_time = time.time()
        
        for i in range(num_operations):
            account.deposit(precise_amount)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        expected_balance = num_operations * precise_amount
        assert account.balance == expected_balance
        assert execution_time < 1.0
        print(f"1000 precision operations completed in {execution_time:.3f} seconds")
    
    def test_large_amount_operations_performance(self):
        """Test performance with very large transaction amounts."""
        # Arrange
        large_balance = Decimal('1000000000.00')  # 1 billion
        account = BankAccount("123456789", large_balance)
        large_amount = Decimal('1000000.00')  # 1 million
        num_operations = 100
        
        # Act
        start_time = time.time()
        
        for i in range(num_operations // 2):
            account.withdraw(large_amount)
            account.deposit(large_amount)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        assert account.balance == large_balance  # Should be back to original
        assert len(account.get_transaction_history()) == num_operations
        assert execution_time < 0.5
        print(f"100 large amount operations completed in {execution_time:.3f} seconds")
    
    def test_boundary_value_operations_performance(self):
        """Test performance with boundary value operations."""
        # Arrange
        account = BankAccount("123456789", 1000.0)
        min_amount = Decimal('0.01')
        num_operations = 500
        
        # Act
        start_time = time.time()
        
        for i in range(num_operations):
            account.deposit(min_amount)
            account.withdraw(min_amount)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        assert account.balance == 1000.0  # Should be unchanged
        assert len(account.get_transaction_history()) == num_operations * 2
        assert execution_time < 1.0
        print(f"1000 boundary value operations completed in {execution_time:.3f} seconds")