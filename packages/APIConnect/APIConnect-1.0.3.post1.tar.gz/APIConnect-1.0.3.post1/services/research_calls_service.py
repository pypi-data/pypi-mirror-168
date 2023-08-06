import json
import logging
from resources.research_calls_resource import ResearchCallsResource

LOGGER = logging.getLogger(__name__)

class ResearchCallsService:
    def __init__(self, routerObj, httpObj) -> None:
        LOGGER.debug("LiveNewsService object is being created.")

        self.__routerObj = routerObj
        self.__http = httpObj

    def _getActiveResearchCalls(self, Segment, Term, MarketCap = None) -> str :
        LOGGER.debug("inside _getActiveResearchCalls method")

        url = self.__routerObj._ActiveResearchCallsURL()
        queryParams = {"seg" : Segment, "term" : Term}

        response = self.__ActiveResearchCallsAPI(url, queryParams)
        formatted_resp = ResearchCallsResource(response)._getCallsFormatted()._response

        if MarketCap :
            filtered_response = ResearchCallsResource(formatted_resp)._filterCalls(MarketCap)._response
            return filtered_response
        else :
            return formatted_resp

    def _getClosedResearchCalls(self, Segment, Term, Action, FromDate, ToDate, RecommendationType, MarketCap) -> str :
        LOGGER.debug("inside _getClosedResearchCalls method")

        url =  self.__routerObj._ClosedResearchCallsURL()
        queryParams = {"seg": Segment, "term": Term, "bySlTyp": Action,
                       "frDt": FromDate, "toDt": ToDate, "rcTyp": RecommendationType}

        response = self.__ClosedResearchCallsAPI(url, queryParams)
        formatted_resp = ResearchCallsResource(response)._getCallsFormatted()._response

        if MarketCap :
            filtered_response = ResearchCallsResource(formatted_resp)._filterCalls(MarketCap)._response
            return filtered_response
        else :
            return formatted_resp

    def __ActiveResearchCallsAPI(self, url, queryParams) -> str:

        LOGGER.debug("inside __ActiveResearchCallsAPI method")

        reply = self.__http._GetMethod(url, queryParams)

        resp_json = json.dumps(reply)
        LOGGER.debug(f"Response received : {resp_json}")
        return resp_json


    def __ClosedResearchCallsAPI(self, url, queryParams) -> str:

        LOGGER.debug("inside __ClosedResearchCallsAPI method")

        reply = self.__http._GetMethod(url, queryParams)

        resp_json = json.dumps(reply)
        LOGGER.debug(f"Response received : {resp_json}")
        return resp_json
