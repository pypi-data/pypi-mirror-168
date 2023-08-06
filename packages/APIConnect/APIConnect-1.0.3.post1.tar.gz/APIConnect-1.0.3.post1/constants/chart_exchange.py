from enum import Enum, unique


@unique
class ChartExchangeEnum(str, Enum) :
    '''
    Enum class for all the allowed types of Exchanges for Charts.
    '''
    NSE = 'NSE'
    BSE = 'BSE'
    NFO = 'NFO'
    CDS = 'CDS'
    MCX = 'MCX'
    NCDEX = 'NCDEX'
    INDEX = 'INDEX'