# Banking System Usage Examples

## Table of Contents
1. [Quick Start](#quick-start)
2. [Basic Account Operations](#basic-account-operations)
3. [Advanced Scenarios](#advanced-scenarios)
4. [Error Handling Examples](#error-handling-examples)
5. [Performance Scenarios](#performance-scenarios)
6. [Integration Patterns](#integration-patterns)

## Quick Start

### Installation and Setup

```bash
# Clone the repository
git clone <repository-url>
cd BankAccount

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests to verify installation
pytest
```

### Your First Bank Account

```python
from src.bank_account import BankAccount

# Create your first account
my_account = BankAccount("123456789", 1000.0)

# Check initial balance
print(f"Starting balance: ${my_account.balance}")  # $1000.00

# Make a deposit
my_account.deposit(250.0)
print(f"After deposit: ${my_account.balance}")     # $1250.00

# Make a withdrawal
my_account.withdraw(100.0)
print(f"After withdrawal: ${my_account.balance}")  # $1150.00
```

## Basic Account Operations

### Account Creation

```python
from src.bank_account import BankAccount
from decimal import Decimal

# Standard account creation
account1 = BankAccount("111111111", 500.0)

# Account with Decimal initial balance
account2 = BankAccount("222222222", Decimal('1000.00'))

# Account starting with zero balance
account3 = BankAccount("333333333", 0)

print(f"Account 1: {account1.account_number} - ${account1.balance}")
print(f"Account 2: {account2.account_number} - ${account2.balance}")
print(f"Account 3: {account3.account_number} - ${account3.balance}")
```

### Deposit Operations

```python
account = BankAccount("123456789", 1000.0)

# Various deposit amounts
account.deposit(100)           # Integer
account.deposit(50.75)         # Float
account.deposit(Decimal('25.25'))  # Decimal

# Check balance after deposits
print(f"Balance after deposits: ${account.balance}")  # $1176.00

# Deposit with precise decimal handling
account.deposit(0.1)
account.deposit(0.2)
# Result is exactly 0.30, not 0.30000000000000004
print(f"Precise balance: ${account.balance}")
```

### Withdrawal Operations

```python
account = BankAccount("123456789", 500.0)

# Regular withdrawals
account.withdraw(100.0)        # Successful withdrawal
account.withdraw(50.25)        # Partial amount

# Withdraw exact balance
remaining = account.balance
account.withdraw(remaining)    # Balance becomes 0.00

print(f"Final balance: ${account.balance}")
```

### Balance Inquiry

```python
account = BankAccount("123456789", 1000.0)

# Access balance property
current_balance = account.balance
print(f"Current balance: ${current_balance}")

# Balance is read-only
try:
    account.balance = 9999.0  # This won't work
except AttributeError:
    print("Balance is protected from direct modification")

# Balance updates automatically after operations
account.deposit(100.0)
print(f"Updated balance: ${account.balance}")
```

### Transaction History

```python
account = BankAccount("123456789", 1000.0)

# Perform some operations
account.deposit(200.0)
account.withdraw(50.0)
account.deposit(100.0)

# Get complete transaction history
history = account.get_transaction_history()

print(f"Total transactions: {len(history)}")

# Print detailed history
for i, transaction in enumerate(history, 1):
    print(f"Transaction {i}:")
    print(f"  Type: {transaction['type']}")
    print(f"  Amount: ${transaction['amount']}")
    print(f"  Timestamp: {transaction['timestamp']}")
    print(f"  Balance After: ${transaction['balance_after']}")
    print()
```

## Advanced Scenarios

### Multi-Account Management

```python
# Create a portfolio of accounts
accounts = {
    'savings': BankAccount("111111111", 5000.0),
    'checking': BankAccount("222222222", 1500.0),
    'emergency': BankAccount("333333333", 10000.0)
}

# Display all account balances
def show_portfolio():
    total = Decimal('0.00')
    for name, account in accounts.items():
        balance = account.balance
        total += balance
        print(f"{name.capitalize()}: ${balance}")
    print(f"Total Portfolio: ${total}")
    print("-" * 30)

print("Initial Portfolio:")
show_portfolio()

# Simulate monthly operations
# Salary deposit to checking
accounts['checking'].deposit(3000.0)

# Transfer to savings (simulate transfer)
transfer_amount = 1000.0
accounts['checking'].withdraw(transfer_amount)
accounts['savings'].deposit(transfer_amount)

# Emergency fund contribution
accounts['emergency'].deposit(500.0)

print("After Monthly Operations:")
show_portfolio()
```

### Budget Tracking System

```python
class BudgetTracker:
    def __init__(self, account: BankAccount, monthly_budget: float):
        self.account = account
        self.monthly_budget = Decimal(str(monthly_budget))
        self.monthly_spent = Decimal('0.00')
    
    def spend(self, amount: float, category: str) -> bool:
        """Track spending against budget."""
        spend_amount = Decimal(str(amount))
        
        if self.monthly_spent + spend_amount > self.monthly_budget:
            print(f"Warning: Would exceed monthly budget!")
            print(f"Budget: ${self.monthly_budget}")
            print(f"Spent: ${self.monthly_spent}")
            print(f"Remaining: ${self.monthly_budget - self.monthly_spent}")
            return False
        
        # Perform withdrawal
        try:
            self.account.withdraw(amount)
            self.monthly_spent += spend_amount
            print(f"Spent ${amount} on {category}")
            print(f"Remaining budget: ${self.monthly_budget - self.monthly_spent}")
            return True
        except ValueError as e:
            print(f"Transaction failed: {e}")
            return False

# Usage example
checking = BankAccount("123456789", 2000.0)
budget = BudgetTracker(checking, 1500.0)

# Track expenses
budget.spend(200.0, "Groceries")
budget.spend(150.0, "Utilities")
budget.spend(500.0, "Rent")
budget.spend(800.0, "Entertainment")  # This might trigger budget warning
```

### Automated Savings System

```python
class AutoSaver:
    def __init__(self, checking: BankAccount, savings: BankAccount, save_percentage: float):
        self.checking = checking
        self.savings = savings
        self.save_percentage = save_percentage / 100
    
    def process_income(self, amount: float) -> None:
        """Automatically save percentage of income."""
        total_amount = Decimal(str(amount))
        save_amount = total_amount * Decimal(str(self.save_percentage))
        spend_amount = total_amount - save_amount
        
        # Deposit total to checking first
        self.checking.deposit(total_amount)
        
        # Transfer savings portion
        self.checking.withdraw(save_amount)
        self.savings.deposit(save_amount)
        
        print(f"Income processed: ${total_amount}")
        print(f"Saved: ${save_amount}")
        print(f"Available for spending: ${spend_amount}")
        print(f"Checking balance: ${self.checking.balance}")
        print(f"Savings balance: ${self.savings.balance}")

# Usage
checking = BankAccount("111111111", 1000.0)
savings = BankAccount("222222222", 0.0)
auto_saver = AutoSaver(checking, savings, 20.0)  # Save 20%

# Process monthly salary
auto_saver.process_income(3000.0)
```

## Error Handling Examples

### Comprehensive Error Handling

```python
def safe_account_operation(account, operation, amount):
    """Safely perform account operations with comprehensive error handling."""
    try:
        if operation == 'deposit':
            result = account.deposit(amount)
            print(f"✓ Deposited ${amount}. New balance: ${account.balance}")
            return result
        elif operation == 'withdraw':
            result = account.withdraw(amount)
            print(f"✓ Withdrew ${amount}. New balance: ${account.balance}")
            return result
        else:
            print(f"✗ Unknown operation: {operation}")
            return False
            
    except ValueError as e:
        print(f"✗ Transaction failed: {e}")
        return False
    except TypeError as e:
        print(f"✗ Invalid input type: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

# Usage examples
account = BankAccount("123456789", 1000.0)

# Valid operations
safe_account_operation(account, 'deposit', 100.0)
safe_account_operation(account, 'withdraw', 50.0)

# Invalid operations
safe_account_operation(account, 'withdraw', 2000.0)  # Insufficient funds
safe_account_operation(account, 'deposit', -100.0)   # Negative amount
safe_account_operation(account, 'deposit', "invalid") # Invalid type
```

### Account Creation Validation

```python
def create_account_safely(account_number, initial_balance):
    """Safely create an account with validation."""
    try:
        account = BankAccount(account_number, initial_balance)
        print(f"✓ Account {account_number} created successfully")
        print(f"  Initial balance: ${account.balance}")
        return account
    
    except ValueError as e:
        print(f"✗ Account creation failed: {e}")
        if "account number" in str(e).lower():
            print("  Hint: Account number must be exactly 9 digits")
        elif "balance" in str(e).lower():
            print("  Hint: Initial balance must be non-negative")
        return None
    
    except Exception as e:
        print(f"✗ Unexpected error during account creation: {e}")
        return None

# Test various scenarios
print("Testing account creation:")
create_account_safely("123456789", 1000.0)    # Valid
create_account_safely("12345", 1000.0)        # Too short
create_account_safely("123456789", -100.0)    # Negative balance
create_account_safely("", 1000.0)             # Empty account number
```

## Performance Scenarios

### High-Volume Transaction Processing

```python
import time

def process_high_volume_transactions(account, num_transactions=1000):
    """Demonstrate high-volume transaction processing."""
    print(f"Processing {num_transactions} transactions...")
    
    start_time = time.time()
    
    for i in range(num_transactions):
        if i % 2 == 0:
            account.deposit(1.0)
        else:
            account.withdraw(0.5)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"✓ Processed {num_transactions} transactions in {processing_time:.3f} seconds")
    print(f"✓ Rate: {num_transactions/processing_time:.0f} transactions/second")
    print(f"✓ Final balance: ${account.balance}")
    print(f"✓ Transaction history size: {len(account.get_transaction_history())}")

# Performance test
account = BankAccount("123456789", 10000.0)
process_high_volume_transactions(account, 5000)
```

### Memory Efficiency Testing

```python
import psutil
import os

def test_memory_efficiency():
    """Test memory usage with large datasets."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"Initial memory usage: {initial_memory:.2f} MB")
    
    # Create multiple accounts with transaction histories
    accounts = []
    for i in range(50):
        account = BankAccount(f"12345{i:04d}", 1000.0)
        
        # Generate transaction history
        for j in range(100):
            account.deposit(10.0)
            account.withdraw(5.0)
        
        accounts.append(account)
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    print(f"After creating 50 accounts with 200 transactions each:")
    print(f"Final memory usage: {final_memory:.2f} MB")
    print(f"Memory increase: {memory_increase:.2f} MB")
    print(f"Average per account: {memory_increase/50:.3f} MB")

test_memory_efficiency()
```

## Integration Patterns

### Banking Service Layer

```python
class BankingService:
    """Service layer for banking operations."""
    
    def __init__(self):
        self.accounts = {}
    
    def create_account(self, account_number: str, initial_balance: float) -> bool:
        """Create a new account."""
        if account_number in self.accounts:
            print(f"Account {account_number} already exists")
            return False
        
        try:
            account = BankAccount(account_number, initial_balance)
            self.accounts[account_number] = account
            print(f"Account {account_number} created successfully")
            return True
        except (ValueError, TypeError) as e:
            print(f"Failed to create account: {e}")
            return False
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> bool:
        """Transfer money between accounts."""
        if from_account not in self.accounts:
            print(f"Source account {from_account} not found")
            return False
        
        if to_account not in self.accounts:
            print(f"Destination account {to_account} not found")
            return False
        
        try:
            # Perform transfer (atomic operation)
            self.accounts[from_account].withdraw(amount)
            self.accounts[to_account].deposit(amount)
            
            print(f"Transferred ${amount} from {from_account} to {to_account}")
            return True
            
        except ValueError as e:
            print(f"Transfer failed: {e}")
            return False
    
    def get_account_summary(self, account_number: str) -> dict:
        """Get account summary."""
        if account_number not in self.accounts:
            return {"error": "Account not found"}
        
        account = self.accounts[account_number]
        history = account.get_transaction_history()
        
        return {
            "account_number": account_number,
            "balance": float(account.balance),
            "transaction_count": len(history),
            "last_transaction": history[-1] if history else None
        }

# Usage example
banking = BankingService()

# Create accounts
banking.create_account("111111111", 5000.0)
banking.create_account("222222222", 1000.0)

# Perform transfer
banking.transfer("111111111", "222222222", 500.0)

# Get summaries
print("Account summaries:")
for account_num in ["111111111", "222222222"]:
    summary = banking.get_account_summary(account_num)
    print(f"Account {account_num}: ${summary['balance']}")
```

### Event-Driven Architecture

```python
from typing import List, Callable

class TransactionEvent:
    def __init__(self, account_number: str, transaction_type: str, 
                 amount: float, balance_after: float):
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after

class EventDrivenAccount:
    """Account with event publishing capabilities."""
    
    def __init__(self, account_number: str, initial_balance: float):
        self.account = BankAccount(account_number, initial_balance)
        self.listeners: List[Callable] = []
    
    def add_listener(self, listener: Callable):
        """Add event listener."""
        self.listeners.append(listener)
    
    def _publish_event(self, transaction_type: str, amount: float):
        """Publish transaction event."""
        event = TransactionEvent(
            self.account.account_number,
            transaction_type,
            amount,
            float(self.account.balance)
        )
        
        for listener in self.listeners:
            listener(event)
    
    def deposit(self, amount: float) -> bool:
        """Deposit with event publishing."""
        try:
            result = self.account.deposit(amount)
            self._publish_event('deposit', amount)
            return result
        except (ValueError, TypeError):
            raise
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw with event publishing."""
        try:
            result = self.account.withdraw(amount)
            self._publish_event('withdrawal', amount)
            return result
        except (ValueError, TypeError):
            raise
    
    @property
    def balance(self):
        return self.account.balance
    
    @property
    def account_number(self):
        return self.account.account_number

# Event listeners
def audit_logger(event: TransactionEvent):
    """Log all transactions for audit."""
    print(f"AUDIT: {event.account_number} - {event.transaction_type} "
          f"${event.amount} - Balance: ${event.balance_after}")

def fraud_detector(event: TransactionEvent):
    """Simple fraud detection."""
    if event.amount > 10000:
        print(f"ALERT: Large transaction detected on {event.account_number}")

def notification_service(event: TransactionEvent):
    """Send notifications for transactions."""
    if event.transaction_type == 'withdrawal' and event.balance_after < 100:
        print(f"NOTIFICATION: Low balance warning for {event.account_number}")

# Usage
account = EventDrivenAccount("123456789", 5000.0)

# Add listeners
account.add_listener(audit_logger)
account.add_listener(fraud_detector)
account.add_listener(notification_service)

# Perform transactions (events will be published)
account.deposit(500.0)
account.withdraw(15000.0)  # Will trigger fraud alert
account.withdraw(5400.0)   # Will trigger low balance warning
```

This comprehensive set of examples demonstrates the flexibility and robustness of the banking system across various real-world scenarios.