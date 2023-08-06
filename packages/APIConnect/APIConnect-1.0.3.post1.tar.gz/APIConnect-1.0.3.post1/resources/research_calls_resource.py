import json
import logging

LOGGER = logging.getLogger(__name__)

class ResearchCallsResource :
    def __init__(self, response : str) -> None:

        LOGGER.debug("ResearchCallsResource object is being created.")

        self._response = response
        self.__response_dict = json.loads(self._response)
        self.__messageID = self.__response_dict['msgID']
        self.__serverTime = self.__response_dict['srvTm']
        self.__data = self.__response_dict['data']

    def _getCallsFormatted(self) -> 'ResearchCallsResource' :
        LOGGER.debug("inside _getCallsFormatted method")

        formatted_resp_dict = {
                            'data' : self.__data,
                            'msgID' : self.__messageID,
                            'srvTm' : self.__serverTime
                            }
        self._response = json.dumps(formatted_resp_dict)
        return self

    def _filterCalls(self, market_cap : str = None) -> 'ResearchCallsResource' :

        LOGGER.debug("inside _filterCalls method")
        self.__response_dict = json.loads(self._response)
        if market_cap:
            filtered_calls = []
            for r_call in self.__response_dict.get('data').get('lst') :
                if 'cap' in r_call and r_call.get('cap').lower() == market_cap.lower() :
                    filtered_calls.append(r_call)
            self.__response_dict['data']['lst'] = filtered_calls

        self._response = json.dumps(self.__response_dict)
        return self