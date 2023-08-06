from enum import Enum, unique


@unique
class TermEnum(str, Enum) :
    '''
    Enum class for all the allowed types of Terms in Research Calls.
    '''
    LONGTERM = 'LONGTERM'
    MIDTERM = 'MIDTERM'
    SHORTTERM = 'SHORTTERM'
