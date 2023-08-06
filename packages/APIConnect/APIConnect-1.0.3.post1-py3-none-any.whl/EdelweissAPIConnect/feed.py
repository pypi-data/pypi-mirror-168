import configparser
import errno
import json
import logging
from os import path
import os
import socket
from threading import Thread

logging.basicConfig(filename = 'edlwsapi.log',
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
LOGGER = logging.getLogger(__name__)

def init_logger(conf) -> None:
    """
    Method to initialize logger configuration via provided configuration object.
    - Parameters:\n
    `conf`: ConfigParser object of provided settings.ini file.
    """
    LOG_LEVELS = {
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

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


class Feed:

    def __init__(self, accid, userid, conf):

        '''
        Streamer

        To subscribe to the streamer, Create the single instance of this mentioning `callback` method. After successsful subscription, `callback` method will be called whenever packet is available at the streamer.

         - symbols: Symbol list for subscription : Symbol_exchange to be obtained from Contract File

         - accid: Customer Account ID

         - messageCallback: Callback to receive the Feed in

         - subscribe_order

         - subscribe_quote

        '''
        self.__conf = None
        self.__init_logger = init_logger
        self.__appID = None
        if conf:
            self.__conf = configparser.ConfigParser()
            try:
                if path.exists(conf):
                    self.__conf.read(conf)
                    self.__init_logger(self.__conf)
                    LOGGER.info("Loggers initiated with provided configuration.")
                    self.__appID = self.__conf['GLOBAL'].get('AppIdKey')
                else:
                    raise FileNotFoundError(
                        errno.ENOENT, os.strerror(errno.ENOENT), conf)
            except Exception as ex:
                LOGGER.exception("Error occurred while parsing provided configuaration file: %s", ex)
                raise ex
        else:
            LOGGER.info("Feed object initiated with default values.")
        self.userid = userid
        self.accid = accid
        self.__host = self.__conf['STREAM'].get('HOST')
        self.__port = int(self.__conf['STREAM'].get('PORT'))

        # New code TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10000)

        try:
            self.sock.connect((self.__host, self.__port))
        except OSError as e:
            self.sock.close()
            LOGGER.error("Failed to establish connection with subscriber.")
            raise e
        self.sock.setblocking(True)
        self.socket_fs = self.sock.makefile('rw')
        LOGGER.info("Connection established with subscriber.")

    def __read_stream_data(self):
        while True:
            try :
                resp = self.socket_fs.readline()
            except (OSError, socket.error) as e:
                self.sock.close()
                LOGGER.error("Socket error occured.", e)
                raise

            LOGGER.debug("Response recevied: %s", resp)
            if not resp:
                LOGGER.error("Socket Connection seems to be closed. Please try to subscribe again.")
                print("Socket Connection seems to be closed. Please try to subscribe again.")
                break
            else:
                self.callback(resp)

        self.sock.close()

    def subscribe(self, symbols, callBack, subscribe_order: bool = True, subscribe_quote: bool = True):
        # blocking socket connection, using file stream to send and recieve data line wise
        self.callback = callBack
        self.symbols = symbols

        # Send data
        if subscribe_quote:
            quote = self.__CreateMessage_quote(self.symbols)
            LOGGER.debug("Requesting subscriber with quote: %s", quote)
            self.socket_fs.writelines(quote)
            self.socket_fs.flush()

        if subscribe_order:
            orderfiler = self.__CreateMessage_OrderFiler()
            LOGGER.debug("Requesting subscriber with order: %s", orderfiler)
            self.socket_fs.writelines(quote)
            self.socket_fs.flush()

        t1 = Thread(target=self.__read_stream_data)
        t1.start()

    def __CreateMessage_quote(self, symbols):

        symset = []
        for syms in symbols:
            symset.append({"symbol": syms})

        req = {
            "request":
                {
                    "streaming_type": "quote3",
                    "data":
                        {
                            "accType": "EQ",
                            "symbols": symset
                        },
                    "formFactor": "P",
                    "appID": self.__appID,
                    "response_format": "json",
                    "request_type": "subscribe"
                },
            "echo": {}
        }
        return json.dumps(req) + "\n"

    def __CreateMessage_OrderFiler(self):

        req = {
            "request":
                {
                    "streaming_type": "orderFiler",
                    "data":
                        {
                            "accType": "EQ",
                            "userID": self.userid,
                            "accID": self.accid,
                            "responseType": ["ORDER_UPDATE", "TRADE_UPDATE"]
                        },
                    "formFactor": "P",
                    "appID": self.__appID,
                    "response_format": "json",
                    "request_type": "subscribe",
                },
            "echo": {}
        }
        return json.dumps(req) + "\n"

    def unsubscribe(self, symbols=None):
        '''

         This method will unsubscribe the symbols from the streamer. After successful invokation of this, will stop the streamer packets of these symbols.

         symbols: `streaming symbol` for the scrips which need to be unsubscribed

         void
        '''
        symset = []
        for syms in symbols:
            symset.append({"symbol": syms})
        req = {
            "request":
                {
                    "streaming_type": "quote3",
                    "data":
                        {
                            "accType": "EQ",
                            "symbols": symset
                        },
                    "formFactor": "P",
                    "appID": self.__appID,
                    "response_format": "json",
                    "request_type": "unsubscribe"
                },
            "echo": {}
        }
        LOGGER.debug("Unsubscribing with request: %s", req)
        self.sock.send(bytes(json.dumps(req) + "\n", "UTF-8"))