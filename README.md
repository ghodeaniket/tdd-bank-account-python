# Banking System TDD Implementation - Phase 1

A Test-Driven Development (TDD) implementation of a simple banking system in Python, focusing on foundation and account creation functionality.

## Project Overview

This project implements a BankAccount class following strict TDD principles with the Red-Green-Refactor cycle. Phase 1 covers basic account creation and validation functionality.

## Features Implemented

### ✅ Phase 1: Foundation and Account Creation
- **Basic Account Creation**: Create bank accounts with account numbers and initial balances
- **Account Validation**: Comprehensive input validation for account creation
- **Error Handling**: Custom exception handling for invalid inputs

## Project Structure

```
BankAccount/
├── src/
│   ├── __init__.py
│   └── bank_account.py          # Main BankAccount class
├── tests/
│   ├── __init__.py
│   └── test_bank_account.py     # Comprehensive test suite
├── docs/                        # Documentation directory
├── requirements.txt             # Project dependencies
├── setup_venv.sh               # Virtual environment setup script
├── pytest.ini                 # Pytest configuration
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

## Setup Instructions

### 1. Virtual Environment Setup
```bash
# Make setup script executable and run
chmod +x setup_venv.sh
./setup_venv.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test class
pytest tests/test_bank_account.py::TestBankAccountCreation
```

## API Reference

### BankAccount Class

#### Constructor
```python
BankAccount(account_number: str, initial_balance: Union[int, float])
```

**Parameters:**
- `account_number`: Must be exactly 9 digits (string)
- `initial_balance`: Cannot be negative (int or float)

**Raises:**
- `ValueError`: If account_number is invalid or initial_balance is negative

**Example:**
```python
from src.bank_account import BankAccount

# Valid account creation
account = BankAccount("123456789", 100.0)
print(f"Account: {account.account_number}, Balance: {account.balance}")

# Invalid examples (will raise ValueError)
BankAccount("12345", 100.0)        # Too short
BankAccount("123456789", -50.0)    # Negative balance
BankAccount("", 100.0)             # Empty account number
```

## Test Coverage

- **Coverage**: 100% (11/11 statements)
- **Test Cases**: 6 comprehensive test methods
- **Test Categories**:
  - Basic account creation and instantiation
  - Account number and balance storage verification
  - Input validation (negative balance, invalid account format, empty account number)

## TDD Principles Followed

1. ✅ **Red-Green-Refactor Cycle**: All features implemented following strict TDD
2. ✅ **Test-First Development**: No production code without failing tests
3. ✅ **Minimal Implementation**: Simplest code to make tests pass
4. ✅ **Comprehensive Testing**: One test per specific behavior
5. ✅ **Descriptive Test Names**: Clear test naming convention
6. ✅ **Arrange-Act-Assert Pattern**: Consistent test structure

## Next Steps

Phase 1 is complete with all requirements met:
- ✅ Project structure properly initialized
- ✅ All tests for account creation written and passing
- ✅ Account validation fully tested and implemented
- ✅ 100% test coverage achieved
- ✅ TDD principles strictly followed
- ✅ Clean, readable, and well-documented code

Ready for Phase 2: Deposit Functionality Implementation.