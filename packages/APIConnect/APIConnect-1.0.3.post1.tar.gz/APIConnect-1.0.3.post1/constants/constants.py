from enum import Enum, unique


@unique
class BaseUrl(str, Enum) :
    '''
    Enum class for all the allowed types of Orders.
    '''
    BASE_EQ = "https://client.edelweiss.in/edelmw-eq/eq/"
    BASE_COMM = "https://client.edelweiss.in/edelmw-comm/comm/"
    BASE_CONTENT = "https://client.edelweiss.in/edelmw-content/content/"
    BASE_LOGIN = "https://client.edelweiss.in/edelmw-login/login/"
    BASE_MF_LOGIN = "https://client.edelweiss.in/edelmw-mf/mf/"
    EQ_CONTRACT = "https://client.edelweiss.in/app/toccontracts/instruments.zip"
    MF_CONTRACT = "https://client.edelweiss.in/app/toccontracts/mfInstruments.zip"