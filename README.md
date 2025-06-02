# Banking System TDD Implementation

[![CI](https://github.com/ghodeaniket/tdd-bank-account-python/actions/workflows/ci.yml/badge.svg)](https://github.com/ghodeaniket/tdd-bank-account-python/actions/workflows/ci.yml)

A complete Test-Driven Development (TDD) implementation of a banking system in Python with comprehensive testing, CI/CD, and production-ready features.

## Project Overview

This project implements a full-featured BankAccount class following strict TDD principles with the Red-Green-Refactor cycle. All phases completed with 58 comprehensive tests covering unit, integration, and performance testing.

## Features Implemented

### ✅ Phase 1: Foundation and Account Creation
- **Basic Account Creation**: Create bank accounts with account numbers and initial balances
- **Account Validation**: Comprehensive input validation for account creation
- **Error Handling**: Custom exception handling for invalid inputs

### ✅ Phase 2: Deposit Functionality
- **Secure Deposits**: Add money to accounts with validation
- **Amount Validation**: Prevents negative and zero deposits
- **Type Safety**: Handles numeric type validation

### ✅ Phase 3: Withdrawal Functionality
- **Secure Withdrawals**: Remove money with insufficient funds protection
- **Balance Validation**: Prevents overdrafts
- **Edge Case Handling**: Exact balance withdrawals supported

### ✅ Phase 4: Balance Inquiry
- **Real-time Balance**: Current balance property with read-only access
- **Transaction Reflection**: Balance updates with all operations
- **Immutable Design**: Balance cannot be modified directly

### ✅ Phase 5: Transaction History
- **Complete Audit Trail**: Full transaction history with timestamps
- **Chronological Order**: Transactions preserved in execution order
- **Rich Metadata**: Transaction type, amount, and timestamp tracking

### ✅ Phase 6: Integration & Performance
- **Multi-Account Operations**: Account-to-account transfers
- **System Constraints**: Transaction limits and validation
- **Performance Testing**: Large volume transaction handling
- **Memory Efficiency**: Optimized for production workloads

## Project Structure

```
BankAccount/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── src/
│   ├── __init__.py
│   └── bank_account.py         # Complete BankAccount implementation
├── tests/
│   ├── __init__.py
│   ├── test_bank_account.py    # Unit tests (31 tests)
│   ├── test_integration.py    # Integration tests (16 tests)
│   └── test_performance.py    # Performance tests (11 tests)
├── docs/
│   ├── SYSTEM_DOCUMENTATION.md # Complete API documentation
│   └── USAGE_EXAMPLES.md       # Practical usage examples
├── requirements.txt            # Project dependencies
├── setup_venv.sh              # Virtual environment setup script
├── pytest.ini                 # Pytest configuration
├── .gitignore                 # Git ignore file
└── README.md                  # This file
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

- **Coverage**: 100% line coverage
- **Total Tests**: 58 comprehensive test cases
- **Test Categories**:
  - **Unit Tests (31)**: Core functionality, validation, edge cases
  - **Integration Tests (16)**: Multi-account operations, system constraints
  - **Performance Tests (11)**: Large volume operations, memory efficiency
- **CI/CD**: Automated testing on Python 3.8-3.11

## TDD Principles Followed

1. ✅ **Red-Green-Refactor Cycle**: All features implemented following strict TDD
2. ✅ **Test-First Development**: No production code without failing tests
3. ✅ **Minimal Implementation**: Simplest code to make tests pass
4. ✅ **Comprehensive Testing**: One test per specific behavior
5. ✅ **Descriptive Test Names**: Clear test naming convention
6. ✅ **Arrange-Act-Assert Pattern**: Consistent test structure

## Production Ready

All phases complete with production-ready implementation:
- ✅ Complete banking functionality (create, deposit, withdraw, transfer)
- ✅ Comprehensive test suite (58 tests) with 100% coverage
- ✅ Integration and performance testing
- ✅ GitHub Actions CI/CD pipeline
- ✅ Complete documentation and usage examples
- ✅ TDD principles strictly followed throughout
- ✅ Memory efficient and performance optimized
- ✅ Production-ready error handling and validation

## Documentation

For detailed API documentation, see [docs/SYSTEM_DOCUMENTATION.md](docs/SYSTEM_DOCUMENTATION.md)
For usage examples, see [docs/USAGE_EXAMPLES.md](docs/USAGE_EXAMPLES.md)