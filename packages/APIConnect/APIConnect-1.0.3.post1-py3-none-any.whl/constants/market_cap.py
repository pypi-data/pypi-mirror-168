from enum import Enum, unique


@unique
class MarketCapEnum(str, Enum) :
    '''
    Enum class for all the allowed types of Market Caps in Research Calls.
    '''
    Large = 'Large'
    Medium = 'Medium'
    Small = 'Small'
