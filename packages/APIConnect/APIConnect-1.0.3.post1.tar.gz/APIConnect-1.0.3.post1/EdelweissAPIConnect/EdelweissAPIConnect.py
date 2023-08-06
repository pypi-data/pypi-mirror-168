import json
import os
import errno
import sys
from os import path
import logging
import configparser
from EdelweissAPIConnect.http import Http, init_proxies
from EdelweissAPIConnect.login_helper import LoginHelper
from constants.asset_type import AssetTypeEnum
from constants.chart_exchange import ChartExchangeEnum
from constants.market_cap import MarketCapEnum
from constants.segment import SegmentEnum
from constants.term import TermEnum
from constants.router import Router
from constants.intraday_interval import IntradayIntervalEnum
from EdelweissAPIConnect.edelweiss_api_utils import EdelApiUtils
from constants.eod_Interval import EODIntervalEnum
from constants.exchange import ExchangeEnum
from constants.order_type import OrderTypeEnum
from constants.product_code import ProductCodeENum
from constants.duration import DurationEnum
from constants.action import ActionEnum
from EdelweissAPIConnect.order import Order
from EdelweissAPIConnect.validator import Validator
from exceptions.validation_exception import ValidationException
from resources.chart_response_formatter import ChartResponseFormatter
from services.live_news_service import LiveNewsService
from services.watchlist_service import WatchlistService
from services.research_calls_service import ResearchCallsService

logging.basicConfig(filename = 'edlwsapi.log',
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
LOGGER = logging.getLogger(__name__)

LOG_LEVELS = {
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

def init_logger(conf) -> None:
    """
    Method to initialize logger configuration via provided configuration object.
    - Parameters:\n
    `conf`: ConfigParser object of provided settings.ini file.
    """

    LOG_LEVEL=None
    LOG_FILE=None
    if 'LOG_LEVEL' in conf['GLOBAL'] and conf['GLOBAL']['LOG_LEVEL'] in LOG_LEVELS:
        LOG_LEVEL = LOG_LEVELS[conf['GLOBAL']['LOG_LEVEL']]
    if 'LOG_FILE' in conf['GLOBAL']:
        LOG_FILE = conf['GLOBAL']['LOG_FILE']
    if LOG_FILE or LOG_LEVEL:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        LOG_FILE = LOG_FILE if LOG_FILE else 'edlwsapi.log'
        LOG_LEVEL = LOG_LEVEL if LOG_LEVEL else logging.INFO
        logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

class EdelweissAPIConnect:

    def __init__(self, ApiKey, Password, reqID, downloadContract: bool, conf=None) -> None:
        self.__conf = None
        self.__init_logger = init_logger
        if conf:
            self.__conf = configparser.ConfigParser()
            try:
                if path.exists(conf):
                    self.__conf.read(conf)
                    self.__init_logger(self.__conf)
                    LOGGER.info("Loggers initiated with provided configuration.")
                else:
                    raise FileNotFoundError(
                        errno.ENOENT, os.strerror(errno.ENOENT), conf)
            except Exception as ex:
                LOGGER.exception("Error occurred while parsing provided configuaration file: %s", ex)
                raise ex
        else:
            LOGGER.info("Logger initiated with default values.")

        self.__version = '1.0.3'
        self.__dc = downloadContract
        self.__filename = "data_" + ApiKey + '.txt'
        self.__router = Router(self.__conf)
        self.__constants = EdelApiUtils()
        self.__init_proxies = init_proxies
        self.__proxies = self.__init_proxies(self.__conf)
        self.__http = Http(self.__constants, self.__proxies)
        self.__constants.Filename = self.__filename
        self.__constants.ApiKey = ApiKey
        self.__login_helper = LoginHelper(self.__http, self.__router, self.__constants)
        AppIdKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImZmIjoiVyIsImJkIjoid2ViLXBjIiwibmJmIjoxNjYxNzUzNzAzLCJzcmMiOiJlbXRtdyIsImF2IjoiMS4wLjMiLCJhcHBpZCI6Ijc2ODkxOTQyMTMwYjI0ZjRmMWMyOWM5MzU5Zjc2M2JhIiwiaXNzIjoiZW10IiwiZXhwIjoxNjYxNzk3ODAwLCJpYXQiOjE2NjE3NTQwMDN9.uUfe3SC3M0W33AZWUYF9jXQvlXWQrZsBSdALRHTX7Lw"

        if conf and self.__conf['GLOBAL'].get('AppIdKey'):
            AppIdKey = self.__conf['GLOBAL'].get('AppIdKey')
        self.__constants.AppIdKey = AppIdKey

        if path.exists(self.__filename):
            LOGGER.info("User data file found, loading data.")
            read = open(self.__filename, 'r').read()
            j = json.loads(read)
            self.__constants.VendorSession = j['vt']
            self.__constants.JSessionId =  j['auth']
            self.__constants.eqAccId = j['eqaccid']
            self.__constants.coAccId = j['coaccid']
            self.__constants.Data = j['data']
            self.__constants.ProfileId = j.get('data').get('data').get('lgnData').get('accs').get('prfId')
            self.__constants.AppIdKey = j['appidkey']
        else:
            self.__login_helper._GenerateVendorSession(ApiKey, Password)
            self.__login_helper._GetAuthorization(reqID)

        self.__CheckUpdate()

        self.__login_helper._Instruments(self.__dc, self.__proxies)

    def __CheckUpdate(self):
        LOGGER.info("Checking for new update.")
        url = self.__router._CheckUpdateURl()
        rep = self.__http._PostMethod(url, json.dumps({"lib": "EAC_PYTHON", "vsn": self.__version}))
        if rep['data']['sts'] is True:
            if rep['data']['msg'] == 'MANDATORY':
                print("Mandatory Update. New version " + rep['data']['vsn'] + '. Update to new version to continue.')
                LOGGER.info("New mandatory update found. Please update to new version.")
                sys.exit(0)
            if rep['data']['msg'] == 'OPTIONAL':
                LOGGER.info("New optional update found.")
                print("New version " + rep['data']['vsn'] + " is available. Stay up to date for better experience")


    def GetLoginData(self) -> str:
        """

        Get Login Info.

        """
        return json.dumps(self.__constants.Data)

# Trade Methods

    def OrderBook(self) -> str:
        """

        This method will retrieve the equity Order Book. Typical order book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Order ID
            - Order Status

        """
        LOGGER.info("OrderBook method is called.")
        if self.__constants.Data['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__router._OrderBookURL().format(userid=self.__constants.eqAccId)
            LOGGER.debug("OrderBook method is called for 'EQ' account type")
            eq = self.__http._GetMethod(url)
            LOGGER.debug("Response received: %s", eq)
            return json.dumps({"eq": eq, "comm": ""})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'CO':
            url = self.__router._OrderBookURL_comm().format(userid=self.__constants.coAccId, reqtype='COMFNO')
            LOGGER.debug("OrderBook method is called for 'CO' account type")
            comm = self.__http._GetMethod(url)
            LOGGER.debug("Response received: %s", comm)
            return json.dumps({"eq": "", "comm": comm})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__router._OrderBookURL().format(userid=self.__constants.eqAccId)
            LOGGER.debug("OrderBook method is called for 'COMEQ' account type")
            url_comm = self.__router._OrderBookURL_comm().format(userid=self.__constants.coAccId, reqtype='COMFNO')
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response for eq: %s", rep)
            rep_comm = self.__http._GetMethod(url_comm)
            LOGGER.debug("Response for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)


    def TradeBook(self) -> str:

        """

          This method will retrieve the Trade Book. Typical trade book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Trade ID
            - Trade Status

        """
        LOGGER.info("TradeBook method is called.")
        if self.__constants.Data['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__router._TradeBookURL().format(userid=self.__constants.eqAccId)
            # return json.dumps({"eq": self.__http.GetMethod(url), "comm": ""})
            LOGGER.debug("TradeBook method is called for 'EQ' account type")
            eq = self.__http._GetMethod(url)
            LOGGER.debug("Response received: %s", eq)
            return json.dumps({"eq": eq, "comm": ""})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'CO':
            url = self.__router._TradeBookURL_comm().format(userid=self.__constants.coAccId)
            # return json.dumps({"eq": "", "comm": self.__http.GetMethod(url)})
            LOGGER.debug("TradeBook method is called for 'CO' account type")
            comm = self.__http._GetMethod(url)
            LOGGER.debug("Response received: %s", comm)
            return json.dumps({"eq": "", "comm": comm})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__router._TradeBookURL().format(userid=self.__constants.eqAccId)
            url_comm = self.__router._TradeBookURL_comm().format(userid=self.__constants.coAccId)
            LOGGER.debug("TradeBook method is called for 'COMEQ' account type")
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response for eq: %s", rep)
            rep_comm = self.__http._GetMethod(url_comm)
            LOGGER.debug("Response for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)


    def NetPosition(self) -> str:
        """
        Net position usually is referred to in context of trades placed during the day in case of Equity, or can refer to carry forward positions in case of Derivatives, Currency and Commodity. It indicates the net obligation (either buy or sell) for the given day in a given symbol. Usually you monitor the net positions screen to track the profit or loss made from the given trades and will have options to square off your entire position and book the entire profit and loss.


       This method will retrieve the Net position. Typical trade book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Trade ID
            - Trade Status

          """
        LOGGER.info("NetPosition method is called.")
        if self.__constants.Data['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__router._NetPositionURL().format(userid=self.__constants.eqAccId)
            # return json.dumps({"eq": self.__http.GetMethod(url), "comm": ""})
            LOGGER.debug("NetPosition method is called for 'EQ' account type")
            eq = self.__http._GetMethod(url)
            LOGGER.debug("Response received: %s", eq)
            return json.dumps({"eq": eq, "comm": ""})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'CO':
            url = self.__router._NetPositionURL_comm().format(userid=self.__constants.coAccId)
            # return json.dumps({"eq": "", "comm": self.__http.GetMethod(url)})
            LOGGER.debug("NetPosition method is called for 'CO' account type")
            comm = self.__http._GetMethod(url)
            LOGGER.debug("Response received: %s", comm)
            return json.dumps({"eq": "", "comm": comm})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__router._NetPositionURL().format(userid=self.__constants.eqAccId)
            url_comm = self.__router._NetPositionURL_comm().format(userid=self.__constants.coAccId)
            LOGGER.debug("TradeBook method is called for 'COMEQ' account type")
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response for eq: %s", rep)
            rep_comm = self.__http._GetMethod(url_comm)
            LOGGER.debug("Response for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)


    @Validator.isRequired(required=['OrderId', 'Exchange'])
    @Validator.ValidateInputDataTypes

    def OrderDetails(self, OrderId , Exchange : ExchangeEnum) -> str:
        """

          Please use this method to retrive the details of single order.
          Response Fields :
           - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Trade ID
            - Trade Status

        """
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            LOGGER.info("OrderDetails method is called for MCX/NCDEX.")
            LOGGER.debug("OrderDetails method is called for MCX/NCDEX.")
            url = self.__router._OrderDetailsURL_comm().format(userid=self.__constants.coAccId, orderid=OrderId)
            resp = self.__http._GetMethod(url)
            LOGGER.debug("Response receieved: %s", resp)
            return json.dumps(resp)
        else:
            LOGGER.info("OrderDetails method is called.")
            LOGGER.debug("OrderDetails method is called.")
            url = self.__router._OrderDetailsURL().format(userid=self.__constants.eqAccId, orderid=OrderId)
            resp = self.__http._GetMethod(url)
            LOGGER.debug("Response receieved: %s", resp)
            return json.dumps(resp)


    def OrderHistory(self, StartDate, EndDate) -> str:
        """

          This method will retrive all the historical orders placed from `StartDate` to `EndDate`

          StartDate : Start Date of Search

          EndDate : End Date of search

        """
        LOGGER.info("OrderHistory method is called.")

        LOGGER.debug("OrderHistory method is called with account type: %s",
            self.__constants.Data['data']['lgnData']['accTyp'])

        if self.__constants.Data['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__router._OrderHistoryURL().format(userid=self.__constants.eqAccId, StartDate=StartDate,
                                                         EndDate=EndDate)
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response receieved: %s", rep)
            return json.dumps({"eq": rep, "comm": ""})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'CO':
            url = self.__router._OrderHistoryURL_comm().format(userid=self.__constants.coAccId,
                                                              StartDate=StartDate,
                                                              EndDate=EndDate)
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response receieved: %s", rep)
            return json.dumps({"eq": "", "comm": rep})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__router._OrderHistoryURL().format(userid=self.__constants.eqAccId, StartDate=StartDate,
                                                         EndDate=EndDate)
            url_comm = self.__router._OrderHistoryURL_comm().format(userid=self.__constants.coAccId,
                                                                   StartDate=StartDate,
                                                                   EndDate=EndDate)
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response receieved for eq: %s", rep)
            rep_comm = self.__http._GetMethod(url_comm)
            LOGGER.debug("Response receieved for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)


    def Holdings(self) -> str:
        """
        Holdings comprises of the user's portfolio of long-term equity delivery stocks. An instrument in a holding's portfolio remains there indefinitely until its sold or is delisted or changed by the exchanges. Underneath it all, instruments in the holdings reside in the user's DEMAT account, as settled by exchanges and clearing institutions.
        """
        LOGGER.info("Holdings method is called.")
        LOGGER.debug("Holdings method is called with account type: %s",
            self.__constants.Data['data']['lgnData']['accTyp'])

        if self.__constants.Data['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__router._HoldingURL().format(userid=self.__constants.eqAccId)
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response receieved: %s", rep)
            return json.dumps({"eq": rep, "comm": ""})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'CO':
            # url = self.__config.HoldingURL_comm().format(userid=self.__constants.coAccId)
            LOGGER.debug("Holdings not available for 'CO' account type.")
            return json.dumps({"eq": "", "comm": ""})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__router._HoldingURL().format(userid=self.__constants.eqAccId)
            # url_comm = self.__config.HoldingURL_comm().format(userid=self.__constants.coAccId)
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response receieved: %s", rep)
            # rep_comm = self.__http.GetMethod(url_comm)
            LOGGER.debug("Holdings not available for 'CO' account type.")
            combine = {"eq": rep, "comm": ""}
            return json.dumps(combine)


    @Validator.isRequired(required=['Trading_Symbol','Exchange','Action','Duration','Order_Type','Quantity','Streaming_Symbol','Limit_Price','TriggerPrice', 'ProductCode'])
    @Validator.ValidateInputDataTypes

    def PlaceTrade(self, Trading_Symbol, Exchange : ExchangeEnum, Action : ActionEnum, Duration : DurationEnum, Order_Type : OrderTypeEnum, Quantity : int, Streaming_Symbol, Limit_Price, Disclosed_Quantity="0", TriggerPrice="0", ProductCode : ProductCodeENum = ProductCodeENum.CNC) -> str :

        """
        Order placement refers to the function by which you as a user can place an order to respective exchanges. Order placement allows you to set various parameters like the symbol, action (buy, sell, stop loss buy, stop loss sell), product type, validity period and few other custom parameters and then finally place the order. Any order placed will first go through a risk validation in our internal systems and will then be sent to exchange. Usually any order successfully placed will have OrderID and ExchangeOrderID fields populated. If ExchangeOrderID is blank it usually means that the order has not been sent and accepted at respective exchange.

        Order placement method

        - `Trading_Symbol` : Trading Symbol of the Scrip

        - `Exchange` : Exchange

        - `Action` : BUY/SELL

        - `Duration` : DAY/IOC/EOS(for BSE)

        - `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        - `Quantity` : Quantity of the scrip

        - `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        - `Limit_Price` : Limit price of scrip

        - `Disclosed_Quantity` : Quantity to be disclosed while order placement

        - `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        - `ProdcutCode` : CNC/MIS/NRML/MTF

        """
        LOGGER.info("PlaceTrade method is called.")

        data = {'trdSym': Trading_Symbol, 'exc': Exchange.value, 'action': Action.value, 'dur': Duration.value,
                'ordTyp': Order_Type.value, 'qty': str(Quantity), 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode.value, 'posSqr': "N",
                'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': '', 'flQty': "0"}

        LOGGER.debug("PlaceTrade method is called with data: %s", data)
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            url = self.__router._PlaceTradeURL_comm().format(userid=self.__constants.coAccId)
            reply = self.__http._PostMethod(url, json.dumps(data))
            LOGGER.debug("Response received for MCX/NCDEX: %s", reply)
            return json.dumps(reply)
        else:
            url = self.__router._PlaceTradeURL().format(userid=self.__constants.eqAccId)
            reply = self.__http._PostMethod(url, json.dumps(data))
            LOGGER.debug("Response received: %s", reply)
            return json.dumps(reply)


    @Validator.isRequired(required=['Trading_Symbol','Exchange','Action','Duration','Order_Type','Quantity','Streaming_Symbol','Limit_Price','TriggerPrice', 'ProductCode'])
    @Validator.ValidateInputDataTypes

    def PlaceCoverTrade(self, Trading_Symbol, Exchange : ExchangeEnum, Action : ActionEnum, Duration : DurationEnum, Order_Type : OrderTypeEnum, Quantity : int, Streaming_Symbol, Limit_Price, Disclosed_Quantity="0", TriggerPrice="0", ProductCode : ProductCodeENum = ProductCodeENum.CNC) -> str or None :

        """

        A Cover Order is an order type for intraday trades. A Cover Order lets you to place trades with very high leverage of up to 20 times the available limits (Cash/Stocks collateral limits)

        Pay a fraction of total order amount (10% or Rs. 20) to own the shares. In case it falls below the following price, sell it off to prevent me losing money from sharp price drops.

        - `Trading_Symbol` : Trading Symbol of the Scrip

        - `Exchange` : Exchange

        - `Action` : BUY/SELL

        - `Duration` : DAY/IOC/EOS(for BSE)

        - `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        - `Quantity` : Quantity of the scrip

        - `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        - `Limit_Price` : Limit price of scrip

        - `Disclosed_Quantity` : Quantity to be disclosed while order placement

        - `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        - `ProdcutCode` : CNC/MIS/NRML/MTF

        """
        LOGGER.info("PlaceCoverTrade is method is called.")
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            print('Operation invalid for Commodities')
            LOGGER.debug("Operation is disabled for commodities.")
            return

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration,
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'posSqr': "false",
                'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': '', 'flQty': "0", }

        LOGGER.debug("PlaceCoverTrade method is called with data: %s", data)
        url = self.__router._PlaceCoverTradeURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._PostMethod(url, json.dumps(data))
        LOGGER.debug("Response receieved: %s", resp)
        return json.dumps(resp)


    @Validator.isRequired(required=['Trading_Symbol','Exchange','Action','Duration','Order_Type','Quantity','Limit_Price','TriggerPrice', 'ProductCode', 'DTDays'])
    @Validator.ValidateInputDataTypes

    def PlaceGtcGtdTrade(self, Trading_Symbol, Exchange : ExchangeEnum, Action : ActionEnum, Duration : DurationEnum, Order_Type : OrderTypeEnum, Quantity : int, streaming_symbol, Limit_Price, Product_Code : ProductCodeENum, DTDays) -> str :

        LOGGER.info("PlaceGtcGtdTrade method is called.")

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'ordTyp': Order_Type,
                'qty': Quantity, 'lmPrc': Limit_Price, 'prdCode': Product_Code,
                'dtDays': DTDays, 'ordSrc': 'API', 'vnCode': '', 'oprtn': '<=', 'srcExp': '', 'tgtId': '',
                'brnchNm': '', 'vlDt': DTDays, 'sym': streaming_symbol,
                'brk': '', }

        LOGGER.debug("PlaceGtcGtdTrade method is called with data: %s", data)
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            url = self.__router._PlaceTradeURL_comm().format(userid=self.__constants.coAccId)
            reply = self.__http._PostMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", reply)
            return json.dumps(reply)
        else:
            url = self.__router._PlaceGtcGtdTradeURL().format(userid=self.__constants.eqAccId)
            reply = self.__http._PostMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", reply)
            return json.dumps(reply)


    @Validator.isRequired(required=['Trading_Symbol','Exchange','Action','Duration','Order_Type','Quantity','Limit_Price','Order_ID','TriggerPrice', 'ProductCode'])
    @Validator.ValidateInputDataTypes

    def ModifyTrade(self, Trading_Symbol, Exchange : ExchangeEnum, Action : ActionEnum, Duration : DurationEnum, Order_Type : OrderTypeEnum, Quantity : int, Streaming_Symbol, Limit_Price, Order_ID, Disclosed_Quantity="0", TriggerPrice="0", ProductCode : ProductCodeENum = ProductCodeENum.CNC) -> str :
        """
        Modify orders allows a user to change certain aspects of the order once it is placed. Depending on the execution state of the order (i.e. either completely open, partially open) there are various levels of modification allowed. As a user you can edit the product type, order quantity, order validity and certain other parameters. Please note that any modifications made to an order will be sent back to the risk system for validation before being submitted and there are chances that an already placed order may get rejected in case of a modification.

        Modify Order

        `Trading_Symbol` : Trading Symbol of the Scrip

        `Exchange` : Exchange

        `Action` : BUY/SELL

        `Duration` : DAY/IOC/EOS(for BSE)

        `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        `Quantity` : Quantity of the scrip

        `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        `Limit_Price` : Limit price of scrip

        `Disclosed_Quantity` : Quantity to be disclosed while order placement

        `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        `ProductCode` : CNC/MIS/NRML/MTF


        """
        LOGGER.info("ModifyTrade method is called.")

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'dtDays': '', 'nstOID': Order_ID}
        LOGGER.debug("ModifyTrade method is called with method: %s", data)
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            url = self.__router._ModifyTradeURL_comm().format(userid=self.__constants.coAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", resp)
            return json.dumps(resp)

        else:
            url = self.__router._ModifyTradeURL().format(userid=self.__constants.eqAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", resp)
            return json.dumps(resp)


    @Validator.isRequired(required=['Trading_Symbol','Exchange','Action','Duration','Order_Type','Quantity','Limit_Price','Order_ID','TriggerPrice', 'ProductCode'])
    @Validator.ValidateInputDataTypes

    def ModifyCoverTrade(self, Trading_Symbol, Exchange : ExchangeEnum, Action : ActionEnum, Duration : DurationEnum, Order_Type : OrderTypeEnum, Quantity : int, Streaming_Symbol, Limit_Price, Order_ID, Disclosed_Quantity="0", TriggerPrice="0", ProductCode : ProductCodeENum = ProductCodeENum.CNC) -> str or None:

        """

        Modify Cover Order

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        TriggerPrice : Trigger Price applicable for SL/SL-M Orders

        ProductCode : CNC/MIS/NRML/MTF

        """
        LOGGER.info("ModifyCoverTrade method is called")
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            print('Operation invalid for Commodities')
            LOGGER.debug("Operation is blocked for commodities.")
            return

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'dtDays': '', 'nstOID': Order_ID}
        LOGGER.debug("ModifyCoverTrade method is called with data: %s", data)
        url = self.__router._ModifyCoverTradeURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._PutMethod(url, json.dumps(data))
        LOGGER.debug("Response recieved: %s", resp)
        return json.dumps(resp)


    @Validator.isRequired(required=['Order_ID','Exchange','Order_Type','ProductCode'])
    @Validator.ValidateInputDataTypes

    def CancelTrade(self, Order_ID, Exchange : ExchangeEnum, Order_Type : OrderTypeEnum, Product_Code : ProductCodeENum) -> str :
        """

        An order can be cancelled, as long as on order is open or pending in the system

        Cancel Order

        OrderId : Nest OrderId

        """
        LOGGER.info("CancelTrade method is called.")

        data = {"nstOID": Order_ID, "exc": Exchange, "prdCode": Product_Code, "ordTyp": Order_Type}
        LOGGER.debug("CancelTrade method is called with data: %s", data)
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            url = self.__router._CancelTradeURL_comm().format(userid=self.__constants.coAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", resp)
            return json.dumps(resp)

        else:
            url = self.__router._CancelTradeURL().format(userid=self.__constants.eqAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", resp)
            return json.dumps(resp)


    def MFOrderBook(self, fromDate, toDate) -> str :
        '''

        This method will retrieve the MF Order Book.
         fromDate: From Date
         toDate: To Date
         :return: MF Order Book

         Typical order book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Order ID
            - Order Status

        '''
        LOGGER.info("MFOrderBook method is called.")
        url = self.__router._OrderBookMFURL().format(userid=self.__constants.eqAccId, fromDate=fromDate,
                                                    toDate=toDate)
        rep = self.__http._GetMethod(url)
        LOGGER.debug("MFOrderBook method is called. Receieved response: %s", rep)
        return json.dumps(rep)


    @Validator.isRequired(required='Order_ID')

    def ExitCoverTrade(self, Order_ID) -> str :
        """
        This functionality allows you to completely exit a cover order which includes cancelling any unplaced orders and also completely squaring off any executed orders. For the orders which were executed it will usually modify the stop loss order leg and place it as a market order to ensure execution, while any non executed quantity order will get cancelled.

       Exit Cover Order

       OrderId : Nest OrderId

        """
        LOGGER.info("ExitCoverTrade method is called.")
        url = self.__router._ExitCoverTradeURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._PutMethod(url, json.dumps({"nstOID": Order_ID}))
        LOGGER.debug("ExitCoverTrade method is called for nstOID: %s", Order_ID)
        LOGGER.debug("Response receieved: %s", resp)
        return json.dumps(resp)


    @Validator.isRequired(required=['Order_ID', 'Syom_Id', 'Status'])

    def ExitBracketTrade(self, Order_Id, Syom_Id, Status) -> str :
        """
        Similar to Exit Cover order the functionality will ensure that any non executed open order will be cancelled. However for any orders which are executed it will automatically cancel one of the target or stop loss legs and modify the other leg to be placed as a market order. This will ensure that any executed orders will be squared off in position terms.

       Exit Bracket Order

       OrderId : Nest OrderId

       Syom_Id : Syom_Id obtained post placing Bracket Order

       Status: Current Status of the Bracket Order

       """
        LOGGER.info("ExitBracketTrade method is called.")
        data = {'nstOrdNo': Order_Id, 'syomID': Syom_Id, 'sts': Status}
        params = locals()
        LOGGER.debug("ExitBracketTrade method is called with data: %s", data)
        url = self.__router._ExitBracketTradeURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._DeleteMethod(url, json.dumps(data))
        del (params["self"])
        LOGGER.debug("Response receieved: %s", resp)
        return json.dumps(resp)


    @Validator.isRequired(required=['Exchange','Streaming_Symbol','Transaction_Type','Quantity','Duration','Limit_Price','Target','StopLoss','Trailing_Stop_Loss', 'Trailing_Stop_Loss_Value'])
    @Validator.ValidateInputDataTypes

    def PlaceBracketTrade(self, Exchange : ExchangeEnum, Streaming_Symbol, Transaction_Type : ActionEnum, Quantity : int, Duration : DurationEnum, Disclosed_Quantity, Limit_Price, Target, StopLoss, Trailing_Stop_Loss='Y', Trailing_Stop_Loss_Value="1") -> str or None:

        """

        Bracket Order

        Exchange : Exchange

        Transaction_Type : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        Target : Absolute Target value

        StopLoss :Absolute Stop Loss value

        Trailing_Stop_Loss : Y/N

        Trailing_Stop_Loss_Value : Number

        """
        LOGGER.info("PlaceBracketTrade method is called.")
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            print('Operation invalid for Commodities')
            LOGGER.debug("Operation invalid for commodities.")
            return

        data = {'exc': Exchange, 'sym': Streaming_Symbol,
                'trnsTyp': Transaction_Type, 'qty': Quantity, 'dur': Duration, 'dsQty': Disclosed_Quantity,
                'prc': Limit_Price, 'trdBsdOn': "LTP", 'sqOffBsdOn': 'Absolute', 'sqOffVal': Target,
                'slBsdOn': 'Absolute', 'slVal': StopLoss, 'trlSl': Trailing_Stop_Loss,
                'trlSlVal': Trailing_Stop_Loss_Value, 'ordSrc': 'API'}
        LOGGER.debug("PlaceBracketTrade method is called with data: %s", data)
        url = self.__router._PlaceBracketTradeURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._PostMethod(url, json.dumps(data))
        LOGGER.debug("Response received: %s", resp)
        return json.dumps(resp)


    def PlaceBasketTrade(self, orderlist : Order) -> str :
        """

        Basket order allows user to place multiple orders at one time. User can place orders for multiple scrips all at once. One just creates multiple orders for same or different securities and club these orders together to be placed in one go. This helps save time.

        orderlist : List of Order to be placed, Refer: Order Class

        """
        LOGGER.info("PlaceBasketTrade method is called.")
        isComm = False
        lst = []
        for x in orderlist:
            if x.exc == ExchangeEnum.MCX or x.exc == ExchangeEnum.NCDEX:
                isComm = True
                continue

            #//FIXME: Find better implementation for validation in this method, current implimentation is redundant.
            data = {'trdSym':   Validator.isRequiredv2('TradingSymbol', x.trdSym),
                    'exc':      Validator.isRequiredv2('Exchange',x.exc),
                    'action':   Validator.isRequiredv2('Action',x.action),
                    'dur':      Validator.isRequiredv2('Duration',x.dur),
                    'ordTyp':   Validator.isRequiredv2('OrderType',x.ordTyp),
                    'qty':      Validator.isRequiredv2('Quantity',x.qty),
                    'dscQty':   x.dscQty,
                    'price':    Validator.isRequiredv2('Price',x.price),
                    'trgPrc':   Validator.isRequiredv2('TriggerPrice',x.trgPrc),
                    'prdCode':  Validator.isRequiredv2('ProductCode',x.prdCode),
                    'vnCode': '',
                    'rmk': ''}
            lst.append(data)

        fd = {
            "ordLst": lst,
            "ordSrc": "API"
        }
        if isComm == True:
            print('Basket Order not available for Commodity')
        LOGGER.debug("PlaceBasketTrade method is called with data: %s", fd)
        url = self.__router._PlaceBasketTradeURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._PostMethod(url, json.dumps(fd))
        LOGGER.debug("Response received: %s", resp)
        return json.dumps(resp)


    def Limits(self) -> str :
        """
        Limits refers to the cumulative margins available in your account which can be used for trading and investing in various products. Limits is a combination of the free cash you have (i.e. un-utilized cash), cash equivalent securities (usually margin pledged securities), any money which is in transit (T1/T2 day sell transaction values) and others, all of which can be used for placing orders. Usually whenever you place an order in a given asset and product type our risk management system assesses your limits available and then lets the orders go through or blocks the orders. Limits are dynamic in nature and can be influenced by the Mark to Markets in your positions and sometimes even by the LTP of your holdings.

        Get limits


        """
        LOGGER.info("Limits method is called.")
        LOGGER.debug("Limits method is called for accout type: %s",
                self.__constants.Data['data']['lgnData']['accTyp'])
        if self.__constants.Data['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__router._LimitsURL().format(userid=self.__constants.eqAccId)
            resp = self.__http._GetMethod(url)
            LOGGER.debug("Response recevied: %s", resp)
            return json.dumps({"eq": resp, "comm": ""})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'CO':
            url = self.__router._LimitsURL_comm().format(userid=self.__constants.coAccId)
            resp = self.__http._GetMethod(url)
            LOGGER.debug("Response recevied: %s", resp)
            return json.dumps({"eq": resp, "comm": resp})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__router._LimitsURL().format(userid=self.__constants.eqAccId)
            url_comm = self.__router._LimitsURL_comm().format(userid=self.__constants.coAccId)
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response recevied for eq: %s", rep)
            rep_comm = self.__http._GetMethod(url_comm)
            LOGGER.debug("Response recevied for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)


    def GetAMOStatus(self) -> str :
        """

        Get AMO status

        """
        LOGGER.info("Limits method is called.")
        LOGGER.debug("Limits method is called for accout type: %s",
                self.__constants.Data['data']['lgnData']['accTyp'])

        if self.__constants.Data['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__router._GetAMOFlag()
            resp = self.__http._GetMethod(url)
            LOGGER.debug("Response recevied: %s", resp)
            return json.dumps({"eq": resp, "comm": ""})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'CO':
            url = self.__router._GetAMOFlag_comm()
            resp = self.__http._GetMethod(url)
            LOGGER.debug("Response recevied: %s", resp)
            return json.dumps({"eq": "", "comm": resp})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__router._GetAMOFlag()
            url_comm = self.__router._GetAMOFlag_comm()
            rep = self.__http._GetMethod(url)
            LOGGER.debug("Response recevied for eq: %s", rep)
            rep_comm = self.__http._GetMethod(url_comm)
            LOGGER.debug("Response recevied for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)


    @Validator.isRequired(required=['Trading_Symbol','Exchange','Action','Duration','Order_Type','Quantity','Streaming_Symbol','Limit_Price','TriggerPrice', 'ProductCode'])
    @Validator.ValidateInputDataTypes

    def PlaceAMOTrade(self, Trading_Symbol, Exchange : ExchangeEnum, Action : ActionEnum, Duration : DurationEnum, Order_Type : OrderTypeEnum, Quantity : int, Streaming_Symbol, Limit_Price, Disclosed_Quantity="0", TriggerPrice="0", ProductCode : ProductCodeENum = ProductCodeENum.CNC) -> str :

        """
        After market order or AMO in short refers to orders which can be placed once the markets or exchanges are closed for trading. You can place AMO post market hours which will result in the order in question being placed automatically by 9:15 AM - 9:30 AM the next business day. AMO orders usually need to be limit orders in order to prevent inadvertent execution in case of adverse price movement in markets at beginning of day. AMO is a useful way to place your orders in case you do not have time to place orders during market hours.

        After Market Order trade

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        TriggerPrice : Trigger Price applicable for SL/SL-M Orders

        ProductCode : CNC/MIS/NRML/MTF

        """
        LOGGER.info("PlaceAMOTrade method is called.")

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'posSqr': "false",
                'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': ''}

        LOGGER.debug("PlaceAMOTrade method is called with data: %s", data)
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            url = self.__router._PlaceAMOTrade_comm().format(userid=self.__constants.coAccId)
            resp = self.__http._PostMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s",resp)
            return json.dumps(resp)

        else:
            url = self.__router._PlaceAMOTrade().format(userid=self.__constants.eqAccId)
            resp = self.__http._PostMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s",resp)
            return json.dumps(resp)


    @Validator.isRequired(required=['Trading_Symbol','Exchange','Action','Duration','Order_Type','Quantity','Streaming_Symbol','Limit_Price','Order_ID','TriggerPrice', 'ProductCode'])
    @Validator.ValidateInputDataTypes

    def ModifyAMOTrade(self, Trading_Symbol, Exchange : ExchangeEnum, Action : ActionEnum, Duration : DurationEnum, Order_Type : OrderTypeEnum, Quantity : int, Streaming_Symbol, Limit_Price, Order_ID, Disclosed_Quantity="0", TriggerPrice="0", ProductCode : ProductCodeENum = "CNC") -> str :

        """

        Modify After Market Order

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        TriggerPrice : Trigger Price applicable for SL/SL-M Orders

        ProductCode : CNC/MIS/NRML/MTF

        """
        LOGGER.info("ModifyAMOTrade method is called.")

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'dtDays': '', 'nstOID': Order_ID}
        LOGGER.debug("ModifyAMOTrade method is called with data: %s", data)

        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            url = self.__router._ModifyAMOTrade_comm().format(userid=self.__constants.coAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s",resp)
            return json.dumps(resp)

        else:
            url = self.__router._ModifyAMOTrade().format(userid=self.__constants.eqAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s",resp)
            return json.dumps(resp)


    @Validator.isRequired(required=['Order_ID','Exchange','Order_Type','ProductCode'])
    @Validator.ValidateInputDataTypes

    def CancelAMOTrade(self, Order_ID, Exchange : ExchangeEnum, Order_Type : OrderTypeEnum, ProductCode : ProductCodeENum) -> str :
        """

        Cancel After Market Order

        OrderId : Nest Order Id

        """
        LOGGER.info("CancelAMOTrade method is called.")
        data = {"nstOID": Order_ID, "exc": Exchange, "prdCode": ProductCode, "ordTyp": Order_Type}
        LOGGER.debug("CancelAMOTrade method is called with data: %s", data)
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            url = self.__router._CancelAMOTrade_comm().format(userid=self.__constants.coAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response received: %s", resp)
            return json.dumps(resp)

        else:
            url = self.__router._CancelAMOTrade().format(userid=self.__constants.eqAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response received: %s", resp)
            return json.dumps(resp)


    def PositionSquareOff(self, orderlist : Order) -> str :
        """

        Square off is a term used in intraday and simply means closing all open positions by the end of the trading day

        orderList : List of orders to be Squared Off. Refer : Orders class.

        """
        lst_eq = []
        lst_comm = []
        LOGGER.info("PositionSquareOff method is called.")
        for x in orderlist:

            if x.exc == ExchangeEnum.MCX or x.exc == "NCDEX":
            #//FIXME: Find better implementation for validation in this method, current implimentation is redundant.
                data = {'trdSym':   Validator.isRequiredv2('TradingSymbol', x.trdSym),
                        'exc':      Validator.isRequiredv2('Exchange', x.exc),
                        'action':   Validator.isRequiredv2('Action', x.action),
                        'dur':      Validator.isRequiredv2('Duration', x.dur),
                        'flQty':    "0",
                        'ordTyp':   Validator.isRequiredv2('OrderType',x.ordTyp),
                        'qty':      Validator.isRequiredv2('Quantity', x.qty),
                        'dscQty':   x.dscQty,
                        'sym':      Validator.isRequiredv2('StreamingSymbol',x.sym),
                        'mktPro':   "",
                        'lmPrc':    Validator.isRequiredv2('Price', x.price),
                        'trgPrc':   Validator.isRequiredv2('TriggerPrice', x.trgPrc),
                        'prdCode':  Validator.isRequiredv2('ProductCode', x.prdCode),
                        'dtDays':   '',
                        'posSqr':   "true",
                        'minQty':   "0",
                        'ordSrc':   "API",
                        'vnCode':   '',
                        'rmk':      ''}
                lst_comm.append(data)
            else:
                data = {'trdSym':   Validator.isRequiredv2('TradingSymbol', x.trdSym),
                        'exc':      Validator.isRequiredv2('Exchange', x.exc),
                        'action':   Validator.isRequiredv2('Action', x.action),
                        'dur':      Validator.isRequiredv2('Duration', x.dur),
                        'flQty':    "0",
                        'ordTyp':   Validator.isRequiredv2('OrderType',x.ordTyp),
                        'qty':      Validator.isRequiredv2('Quantity', x.qty),
                        'dscQty':   x.dscQty,
                        'sym':      Validator.isRequiredv2('StreamingSymbol',x.sym),
                        'mktPro':   "",
                        'lmPrc':    Validator.isRequiredv2('Price', x.price),
                        'trgPrc':   Validator.isRequiredv2('TriggerPrice', x.trgPrc),
                        'prdCode':  Validator.isRequiredv2('ProductCode', x.prdCode),
                        'dtDays':   '',
                        'posSqr':   "true",
                        'minQty':   "0",
                        'ordSrc':   "API",
                        'vnCode':   '',
                        'rmk':      ''}
                lst_eq.append(data)

        resp_eq = ""
        resp_comm = ""

        if len(lst_eq) > 0:
            url = self.__router._PositionSqOffURL().format(userid=self.__constants.eqAccId)
            LOGGER.debug("PositionSquareOff method is called with data: %s.", lst_eq)
            resp_eq = self.__http._PostMethod(url, json.dumps(lst_eq))

        if len(lst_comm) > 0:
            url_comm = self.__router._PositionSqOffURL().format(userid=self.__constants.coAccId)
            LOGGER.debug("PositionSquareOff method is called with data: %s.", lst_comm)
            resp_comm = self.__http._PostMethod(url_comm, json.dumps(lst_comm))

        resp = {"eq": resp_eq, "comm": resp_comm}
        LOGGER.debug("Response received: %s", resp)
        return json.dumps(resp)


    @Validator.isRequired(required=['Order_ID','Fill_Id','New_Product_Code','Old_Product_Code','Exchange','Order_Type','Quantity','Streaming_Symbol','Limit_Price','TriggerPrice', 'ProductCode'])
    @Validator.ValidateInputDataTypes

    def ConvertPosition(self, Order_ID, Fill_Id, New_Product_Code : ProductCodeENum, Old_Product_Code : ProductCodeENum, Exchange : ExchangeEnum, Order_Type : OrderTypeEnum) -> str :
        """

        Convert Position : converts your holding position from MIS to CNC and vice-versa

        Order_ID : Nest Order id

        Fill_Id : Fill Id of the trade obtained from Trade API

        New_Product_Code: New Product code of the trade

        Old_Product_Code : Existing Product Code of the trade

        """
        LOGGER.info("ConvertPosition method is called.")
        data = {'nstOID': Order_ID, 'flID': Fill_Id,
                'prdCodeCh': New_Product_Code, 'prdCode': Old_Product_Code,
                'exc': Exchange, 'ordTyp': Order_Type}

        LOGGER.debug("ConvertPosition method is called with data %s",data)
        if Exchange == ExchangeEnum.MCX or Exchange == ExchangeEnum.NCDEX:
            url = self.__router._ConvertPositionURL_comm().format(userid=self.__constants.coAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s", resp)
            return json.dumps(resp)
        else:
            url = self.__router._ConvertPositionURL().format(userid=self.__constants.eqAccId)
            resp = self.__http._PutMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s", resp)
            return json.dumps(resp)

    # MF Methods


    @Validator.ValidateInputDataTypes

    def PlaceMF(self, Token, ISIN_Code, Transaction_Type, Client_Code, Quantity, Amount, ReInv_Flag, Folio_Number, Scheme_Name, Start_Date, End_Date, SIP_Frequency, Generate_First_Order_Today, Scheme_Plan, Scheme_Code, Mandate_Id) -> str :

        '''

        Token:

        ISIN_Code:

        Transaction_Type:

        Client_Code:

        Quantity:

        Amount:

        ReInv_Flag:

        Folio_Number:

        Order_Type:

        Scheme_Name:

        Start_Date:

        End_Date:

        SIP_Frequency:

        Generate_First_Order_Today:

        Scheme_Plan:

        Scheme_Code:


        '''
        LOGGER.info("PlaceMF method is called.")
        data = {'currentOrdSts': '', 'token': Token, 'isin': ISIN_Code, 'txnTyp': Transaction_Type,
                'clientCode': Client_Code, 'qty': Quantity, 'amt': Amount, 'reInvFlg': ReInv_Flag,
                'reqstdBy': self.__constants.eqAccId, 'folioNo': Folio_Number,
                'ordTyp': 'FRESH', 'txnId': '0', 'schemeName': Scheme_Name, 'rmrk': '',
                'mnRdmFlg': '', 'ordSrc': 'API', 'strtDy': "1", 'strtDt': Start_Date, 'endDt': End_Date,
                'sipFrq': SIP_Frequency, 'gfot': Generate_First_Order_Today, 'tnr': '999',
                'mdtId': Mandate_Id, 'sipregno': '', 'siporderno': '',
                'schemePlan': Scheme_Plan, 'schemeCode': Scheme_Code, 'euinnumber': '', 'dpc': 'Y',
                'closeAccountFlag': 'N',
                'kycflag': '1', 'euinflag': 'N', 'physicalFlag': 'D'}

        LOGGER.info("PlaceMF method is called with data: %s.", data)
        url = self.__router._PlaceMFURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._PostMethod(url, json.dumps(data))
        LOGGER.debug("Response received: %s", resp )
        return json.dumps(resp)


    @Validator.ValidateInputDataTypes

    def ModifyMF(self, Token, ISIN_Code, Transaction_Type, Client_Code, Quantity, Amount, ReInv_Flag, Folio_Number, Scheme_Name, Start_Date, End_Date, SIP_Frequency, Generate_First_Order_Today, Scheme_Plan, Scheme_Code, Transaction_Id, Mandate_Id) -> str :

        '''

        certain attributes of a MF order may be modified., as long as on order is open or pending in the system

        Token:

        ISIN_Code:

        Transaction_Type:

        Client_Code:

        Quantity:

        Amount:

        ReInv_Flag:

        Folio_Number:

        Order_Type:

        Scheme_Name:

        Start_Date:

        End_Date:

        SIP_Frequency:

        Generate_First_Order_Today:

        Scheme_Plan:

        Scheme_Code:


        '''
        LOGGER.info("ModifyMF method is called.")
        data = {'currentOrdSts': 'ACCEPTED', 'token': Token, 'isin': ISIN_Code, 'txnTyp': Transaction_Type,
                'clientCode': Client_Code, 'qty': Quantity, 'amt': Amount, 'reInvFlg': ReInv_Flag,
                'reqstdBy': self.__constants.eqAccId, 'folioNo': Folio_Number,
                'ordTyp': 'MODIFY', 'txnId': Transaction_Id, 'schemeName': Scheme_Name, 'rmrk': '',
                'mnRdmFlg': '', 'ordSrc': 'API', 'strtDy': "1", 'strtDt': Start_Date, 'endDt': End_Date,
                'sipFrq': SIP_Frequency, 'gfot': Generate_First_Order_Today, 'tnr': '999',
                'mdtId': Mandate_Id, 'sipregno': '', 'siporderno': '',
                'schemePlan': Scheme_Plan, 'schemeCode': Scheme_Code, 'euinnumber': '', 'dpc': 'Y',
                'closeAccountFlag': 'N',
                'kycflag': '1', 'euinflag': 'N', 'physicalFlag': 'D'}

        LOGGER.debug("PlaceMF method is called with data: %s.", data)
        url = self.__router._PlaceMFURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._PutMethod(url, json.dumps(data))
        LOGGER.debug("Response received: %s", resp )
        return json.dumps(resp)


    @Validator.ValidateInputDataTypes

    def CancelMF(self, Token, ISIN_Code, Transaction_Type, Client_Code, Quantity, Amount, ReInv_Flag, Folio_Number, Scheme_Name, Start_Date, End_Date, SIP_Frequency, Generate_First_Order_Today, Scheme_Plan, Scheme_Code, Transaction_Id) -> str :

        '''

        Token:

        ISIN_Code:

        Transaction_Type:

        Client_Code:

        Quantity:

        Amount:

        ReInv_Flag:

        Folio_Number:

        Scheme_Name:

        Start_Date:

        End_Date:

        SIP_Frequency:

        Generate_First_Order_Today:

        Scheme_Plan:

        Scheme_Code:

        '''
        LOGGER.info("CancelMF method is called.")
        data = {'currentOrdSts': 'ACCEPTED', 'token': Token, 'isin': ISIN_Code, 'txnTyp': Transaction_Type,
                'clientCode': Client_Code, 'qty': Quantity, 'amt': Amount, 'reInvFlg': ReInv_Flag,
                'reqstdBy': self.__constants.eqAccId, 'folioNo': Folio_Number,
                'ordTyp': 'CANCEL', 'txnId': Transaction_Id, 'schemeName': Scheme_Name, 'rmrk': '',
                'mnRdmFlg': '', 'ordSrc': 'API', 'strtDy': "1", 'strtDt': Start_Date, 'endDt': End_Date,
                'sipFrq': SIP_Frequency, 'gfot': Generate_First_Order_Today, 'tnr': '999',
                'mdtId': '', 'sipregno': '', 'siporderno': '',
                'schemePlan': Scheme_Plan, 'schemeCode': Scheme_Code, 'euinnumber': '', 'dpc': 'Y',
                'closeAccountFlag': 'N',
                'kycflag': '1', 'euinflag': 'N', 'physicalFlag': 'D'}

        LOGGER.debug("CancelMF with data %s", data)
        url = self.__router._CancelMFURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._PutMethod(url, json.dumps(data))
        LOGGER.debug("Response recevied: %s", resp)
        return json.dumps(resp)


    def HoldingsMF(self) -> str :
        LOGGER.info("HoldingsMF method is called.")
        params = locals()
        del (params["self"])
        url = self.__router._HoldingsMFURL().format(userid=self.__constants.eqAccId)
        resp = self.__http._GetMethod(url)
        LOGGER.info("HoldingsMF method is called. Response recevied: %s",resp)
        return json.dumps(resp)

    # Chart methods

    def __getChartDataOfScrip(self, Exchange, AssetType, Streaming_Symbol, Interval, TillDate = None, IncludeContinuousFutures = False) -> str :

        LOGGER.info("Inside __getChartDataOfScrip method.")

        # If asset type is not amongst "FUTCOM", "FUTCUR", "FUTSTK", "FUTIDX", set IncludeContinuousFutures as FALSE
        if AssetType not in [AssetTypeEnum.FUTCOM, AssetTypeEnum.FUTCUR, AssetTypeEnum.FUTIDX, AssetTypeEnum.FUTIDX]:
            IncludeContinuousFutures = False

        data = {'chTyp' : "Interval",
                'conti' : IncludeContinuousFutures,
                'ltt' : TillDate
                }

        LOGGER.debug("__getChartDataOfScrip method is called with data: %s", data)

        url = self.__router._ChartsURL().format(interval = Interval, exc = Exchange, aTyp = AssetType, symbol = Streaming_Symbol)
        reply = self.__http._PostMethod(url, json.dumps(data))

        if reply != "":
            reply = ChartResponseFormatter(reply).getOHCLResponse()
            LOGGER.debug("Response received: %s", reply)
        return json.dumps(reply)


    @Validator.isRequired(required=['Exchange', 'AssetType', 'Interval', 'Streaming_Symbol'])
    @Validator.ValidateInputDataTypes

    def getIntradayChart(self, Exchange : ChartExchangeEnum, AssetType : AssetTypeEnum, Streaming_Symbol, Interval : IntradayIntervalEnum, TillDate = None, IncludeContinuousFutures : bool = False) -> str :
        """
        - `Exchange` : Exchange
        - `AssetType` : AssetType for the chart
        - `Streaming_Symbol` : Symbol to fetch chart data for. Eg: 11536_NSE, 4963_BSE, -29 etc
        - `Interval` : interval for Intraday charts
        - `TillDate` : Charts data to fetch till date (format : yyyy-MM-dd)
        - `IncludeContinuousFutures` : boolean. True -> If Continous Futures required. Valid only for instruments (Asset Types) - FUTIDX,FUTSTk,FUTCUR,FUTCOM
        """

        LOGGER.info("getIntradayChart method is called.")

        response = self.__getChartDataOfScrip(Exchange, AssetType, Streaming_Symbol, Interval, TillDate, IncludeContinuousFutures)

        return response

    @Validator.isRequired(required=['Exchange', 'AssetType', 'Interval', 'Streaming_Symbol'])
    @Validator.ValidateInputDataTypes

    def getEODChart(self, Exchange : ChartExchangeEnum, AssetType : AssetTypeEnum, Streaming_Symbol, Interval : EODIntervalEnum, TillDate = None, IncludeContinuousFutures : bool = False) -> str :
        """
        - `Exchange` : Exchange
        - `AssetType` : AssetType for the chart
        - `Streaming_Symbol` : Symbol to fetch chart data for. Eg: 11536_NSE, 4963_BSE, -29 etc
        - `Interval` : interval for EOD charts
        - `TillDate` : Charts data to fetch till date (format : yyyy-MM-dd)
        - `IncludeContinuousFutures` : boolean. True -> If Continous Futures required. Valid only for instruments (Asset Types) - FUTIDX,FUTSTk,FUTCUR,FUTCOM
        """

        LOGGER.info("getEODChart method is called.")

        response = self.__getChartDataOfScrip(Exchange, AssetType, Streaming_Symbol, Interval, TillDate, IncludeContinuousFutures)

        return response


    # Live News methods

    def getNewsCategories(self) -> str:
        LOGGER.info("getNewsCategories method is called")
        service = LiveNewsService(self.__router, self.__http, self.__constants.Filename)
        try:
            response = service._getNewsCategories()
        except OSError as e:
            raise e
        LOGGER.debug(f"getNewsCategories response is : {response}")
        return response

    @Validator.ValidateInputDataTypes
    def getLiveNews(self, holdings : bool, category : str = None, searchText : str = None, pageNumber : int = None) -> str :
        LOGGER.info("getLiveNews method is called")

        service = LiveNewsService(self.__router, self.__http, self.__constants.Filename)
        try:
            if holdings:
                response = service._getHoldingsNews(category, searchText, pageNumber)
            else:
                response = service._getGeneralNews(category, searchText, pageNumber)
        except OSError as e:
            raise e

        LOGGER.debug(f"getLiveNews response is : {response}")
        return response

    @Validator.ValidateInputDataTypes
    def getNewsForResultsAndStocks(self, holdings : bool, searchText : str = None, pageNumber : int = None) -> str :
        LOGGER.info("getNewsForResultsAndStocks method is called")


        service = LiveNewsService(self.__router, self.__http, self.__constants.Filename)
        try:
            if holdings:
                response = service._getHoldingsNews(["Results", "Stocks in News"], searchText, pageNumber)
            else:
                response = service._getResultsAndStocksNews(searchText, pageNumber)
        except OSError as e:
            raise e

        LOGGER.debug(f"getNewsForResultsAndStocks response is : {response}")
        return response

    @Validator.isRequired(['symbol'])
    @Validator.ValidateInputDataTypes
    def getLatestCorporateActions(self, symbol : str) :
        LOGGER.info("getLatestCorporateActions method is called")

        service = LiveNewsService(self.__router, self.__http, self.__constants.Filename)
        response = service._getLatestCorpActionsAPI(symbol)

        LOGGER.debug(f"getLatestCorporateActions response is : {response}")
        return response


    # Watchlist methods

    def getWatchlistGroups(self):
        LOGGER.info("getWatchlistGroups method is called.")
        service = WatchlistService(self.__router, self.__http, self.__constants)

        response = service._getWatchlistGroups()

        LOGGER.debug(f'getWatchlistGroups response is : {response}')
        return response

    @Validator.isRequired(['GroupName'])
    @Validator.ValidateInputDataTypes

    def getWatchlistScrips(self, GroupName : str):
        LOGGER.info("getWatchlistScrips method is called.")
        service = WatchlistService(self.__router, self.__http, self.__constants)

        response = service._getScripsOfGroup(GroupName)

        LOGGER.debug(f'getWatchlistScrips response is : {response}')
        return response

    @Validator.isRequired(['GroupName', 'Symbols'])
    @Validator.ValidateInputDataTypes

    def createWatchlistGroup(self, GroupName : str, Symbols : list):
        LOGGER.info("createWatchlistGroup method is called.")
        service = WatchlistService(self.__router, self.__http, self.__constants)

        response = service._createGroup(GroupName, Symbols)

        LOGGER.debug(f'createWatchlistGroup response is : {response}')
        return response

    @Validator.isRequired(['GroupName', 'Symbols'])
    @Validator.ValidateInputDataTypes
    def addSymbolsWatchlist(self, GroupName : str, Symbols : list):
        LOGGER.info("addSymbolsWatchlist method is called.")
        service = WatchlistService(self.__router, self.__http, self.__constants)

        response = service._addSymbols(GroupName, Symbols)

        LOGGER.debug(f'addSymbolsWatchlist response is : {response}')
        return response

    @Validator.isRequired(['GroupName', 'Symbols'])
    @Validator.ValidateInputDataTypes
    def deleteSymbolsWatchlist(self, GroupName : str, Symbols : list):
        LOGGER.info("deleteSymbolsWatchlist method is called.")
        service = WatchlistService(self.__router, self.__http, self.__constants)

        response = service._deleteSymbols(GroupName, Symbols)

        LOGGER.debug(f'deleteSymbolsWatchlist response is : {response}')
        return response

    @Validator.isRequired(['GroupNames'])
    @Validator.ValidateInputDataTypes
    def deleteWatchlistGroups(self, GroupNames : list):
        LOGGER.info("deleteWatchlistGroups method is called.")
        service = WatchlistService(self.__router, self.__http, self.__constants)

        response = service._deleteGroups(GroupNames)

        LOGGER.debug(f'deleteWatchlistGroups response is : {response}')
        return response

    @Validator.isRequired(['GroupName', 'NewGroupName'])
    @Validator.ValidateInputDataTypes
    def renameWatchlistGroup(self, GroupName : str, NewGroupName : str):
        LOGGER.info("renameWatchlistGroup method is called.")
        service = WatchlistService(self.__router, self.__http, self.__constants)

        response = service._renameGroup(GroupName, NewGroupName)

        LOGGER.debug(f'renameWatchlistGroup response is : {response}')
        return response


    # Research calls methods

    @Validator.isRequired(["Segment", "Term"])
    @Validator.ValidateInputDataTypes

    def getActiveResearchCalls(self, Segment : SegmentEnum, Term : TermEnum, MarketCap : MarketCapEnum = None) :
        LOGGER.info("getActiveResearchCalls method is called.")

        if MarketCap and Segment != "EQ":
            raise ValidationException("Market Cap is only applicable for EQ segment type. Please try again.")

        service = ResearchCallsService(self.__router, self.__http)
        response = service._getActiveResearchCalls(Segment, Term, MarketCap)
        LOGGER.debug(f'getActiveResearchCalls response is : {response}')
        return response


    @Validator.isRequired(["Segment", "Term"])
    @Validator.ValidateInputDataTypes

    def getClosedResearchCalls(self, Segment : SegmentEnum, Term : TermEnum, Action : ActionEnum = None, FromDate : str = None, ToDate : str = None, RecommendationType : str = None, MarketCap : MarketCapEnum = None) :
        LOGGER.info("getClosedResearchCalls method is called.")

        if FromDate :
            Validator.validate_datetime_format(FromDate, r"%Y-%m-%d")
        if ToDate :
            Validator.validate_datetime_format(ToDate, r"%Y-%m-%d")

        if MarketCap and Segment != "EQ":
            raise ValidationException("Market Cap is only applicable for EQ segment type. Please try again.")

        service = ResearchCallsService(self.__router, self.__http)
        response = service._getClosedResearchCalls(Segment, Term, Action, FromDate, ToDate, RecommendationType, MarketCap)
        LOGGER.debug(f'getClosedResearchCalls response is : {response}')
        return response


    # Login methods

    def Logout(self) -> None:
        LOGGER.info("Logout method called.")
        LOGGER.debug("Logout method called with account type: %s",
            self.__constants.Data['data']['lgnData']['accTyp'])
        params = locals()
        del (params["self"])
        if self.__constants.Data['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__router._LogoutURL().format(userid=self.__constants.eqAccId)
            rep = self.__http._PutMethod(url, {})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'CO':
            url = self.__router._LogoutURL().format(userid=self.__constants.coAccId)
            rep = self.__http._PutMethod(url, {})

        elif self.__constants.Data['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__router._LogoutURL().format(userid=self.__constants.eqAccId)
            rep = self.__http._PutMethod(url, {})

        if rep != "":
            if path.exists(self.__filename):
                LOGGER.debug("File with account related details is removed.")
                os.remove(self.__filename)
            self.__constants.Data = ""