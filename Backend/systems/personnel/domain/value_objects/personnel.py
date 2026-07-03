"""
Domain Value Objects: Personnel
═════════════════════════════════
قيم ثابتة للفرد.
Python نقي — لا Django.
"""
from enum import Enum


class NationalIdStatus(str, Enum):
    VALID          = 'valid'
    MISSING        = 'missing'
    INVALID_FORMAT = 'invalid_format'
    INVALID_LENGTH = 'invalid_length'


class MilitaryNumberType(str, Enum):
    OFFICER               = 'officer'
    BASIC_PERSONNEL       = 'basic_personnel'
    COMMITTEE_OR_NEWCOMER = 'committee_or_newcomer'
    UNKNOWN               = 'unknown'


class ExpenseStatus(str, Enum):
    HAS_EXPENSES = 'has_expenses'
    NO_EXPENSES  = 'no_expenses'
    EXPENSES     = 'expenses'
