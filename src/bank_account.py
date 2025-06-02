"""BankAccount class implementation following TDD principles."""

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Union


# Constants
ACCOUNT_NUMBER_LENGTH = 9
CURRENCY_PRECISION = '0.01'


class BankAccount:
    """A simple bank account implementation."""
    
    def __init__(self, account_number: str, initial_balance: Union[int, float, Decimal]) -> None:
        """Initialize a bank account with account number and initial balance.
        
        Args:
            account_number: The account number as a string
            initial_balance: The initial balance for the account
            
        Raises:
            ValueError: If account_number is invalid or initial_balance is negative
        """
        # Validate account number
        if not account_number:
            raise ValueError("Account number cannot be empty")
        
        if not account_number.isdigit() or len(account_number) != ACCOUNT_NUMBER_LENGTH:
            raise ValueError(f"Account number must be exactly {ACCOUNT_NUMBER_LENGTH} digits")
        
        # Validate initial balance
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        self.account_number = account_number
        # Convert to Decimal for precise currency calculations
        self._balance = Decimal(str(initial_balance)).quantize(Decimal(CURRENCY_PRECISION), rounding=ROUND_HALF_UP)
        self._transaction_history: List[Dict[str, Union[str, Decimal]]] = []
    
    def _validate_amount(self, amount: Union[int, float, Decimal]) -> Decimal:
        """Validate that an amount is numeric and positive, returning a Decimal.
        
        Args:
            amount: The amount to validate
            
        Returns:
            The amount as a Decimal rounded to 2 decimal places
            
        Raises:
            TypeError: If amount is not numeric
            ValueError: If amount is not positive
        """
        if not isinstance(amount, (int, float, Decimal)):
            raise TypeError("Amount must be numeric")
        
        # Convert to Decimal for precise calculations
        decimal_amount = Decimal(str(amount)).quantize(Decimal(CURRENCY_PRECISION), rounding=ROUND_HALF_UP)
        
        if decimal_amount <= 0:
            raise ValueError("Amount must be positive")
        
        return decimal_amount
    
    def deposit(self, amount: Union[int, float, Decimal]) -> bool:
        """Deposit money into the account.
        
        Args:
            amount: The amount to deposit
            
        Returns:
            True if deposit was successful
            
        Raises:
            ValueError: If amount is not positive
            TypeError: If amount is not numeric
        """
        decimal_amount = self._validate_amount(amount)
        self._balance += decimal_amount
        self._record_transaction('deposit', decimal_amount)
        return True
    
    def withdraw(self, amount: Union[int, float, Decimal]) -> bool:
        """Withdraw money from the account.
        
        Args:
            amount: The amount to withdraw
            
        Returns:
            True if withdrawal was successful
            
        Raises:
            ValueError: If amount is not positive or insufficient funds available
            TypeError: If amount is not numeric
        """
        decimal_amount = self._validate_amount(amount)
        
        if decimal_amount > self._balance:
            raise ValueError("Insufficient funds")
        
        self._balance -= decimal_amount
        self._record_transaction('withdrawal', decimal_amount)
        return True
    
    @property
    def balance(self) -> Decimal:
        """Get the current account balance.
        
        Returns:
            The current balance of the account as a Decimal
        """
        return self._balance
    
    
    def _record_transaction(self, transaction_type: str, amount: Decimal) -> None:
        """Record a transaction in the transaction history.
        
        Args:
            transaction_type: The type of transaction ('deposit' or 'withdrawal')
            amount: The transaction amount as a Decimal
        """
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }
        self._transaction_history.append(transaction)
    
    def get_transaction_history(self) -> List[Dict[str, Union[str, Decimal]]]:
        """Get the transaction history for this account.
        
        Returns:
            A list of transaction dictionaries containing type, amount, and timestamp
        """
        return self._transaction_history.copy()