import requests
import json
from typing import Optional
import logging

class Notion:
    def __init__(self, token: str):
        self._token = token
        self._base_url = 'https://api.notion.com/v1/'
        self._headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2021-05-13'}

    @classmethod
    def handle_response_status_code(self, response):
        if response.status_code == 200:
            r = json.loads(response.text)
        elif response.status_code == 400:
            r = json.loads(response.text)
            logging.error(r)
        elif response.status_code == 401:
            r = json.loads(response.text)
            logging.error(r)
        else:
            print(response)
            r = None
        return r

    def search(self,
               query: Optional[str] = None,
               sort: Optional[dict] = None,
               filter: Optional[dict] = None,
               start_cursor: Optional[str] = None,
               page_size: Optional[int] = 100,
               max_retries: Optional[int] = 2) -> object:
        """
        Method to search in all the shared Notion elements with the Integration.

        Parameters
        ----------
        query        : When supplied, limits which pages are returned by comparing the query to the page title.
        sort         : When supplied, sorts the results based on the provided criteria.
                       Limitation: Currently only a single sort is allowed and is limited to last_edited_time.
                       Dict params: direction [ascending/descending] | timestamp [last_edited_time]
        filter       : When supplied, filters the results based on the provided criteria.
                       Dict params: value [page/database] | property [object]

        start_cursor : If supplied, this endpoint will return a page of results starting after the cursor provided.
                       If not supplied, this endpoint will return the first page of results.
        page_size    : The number of items from the full list desired in the response. Maximum: 100

        max_retries  : If there is an error of connection, how many times to retry.

        Returns
        -------
        An object with the response of the search.

        """
        params = [('query', query), ('sort', sort), ('filter', filter), ('start_cursor', start_cursor), ('page_size', page_size)]
        params_dict = {p[0]: p[1] for p in params if p[1] is not None}
        payload = json.dumps(params_dict)
        for i in range(max_retries):
            response = requests.request('POST', self._base_url + 'search', headers=self._headers, data=payload)
            search = self.handle_response_status_code(response)
            if search is not None:
                break
        if search is None:
            logging.error('Max retries reached and connection is not available')
        return search
