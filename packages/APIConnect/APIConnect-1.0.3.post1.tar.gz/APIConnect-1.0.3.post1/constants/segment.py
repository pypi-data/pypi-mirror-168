from enum import Enum, unique


@unique
class SegmentEnum(str, Enum) :
    '''
    Enum class for all the allowed types of Segments in Research Calls.
    '''
    EQ  = 'EQ'
    FNO = 'FNO'
    CUR = 'CUR'