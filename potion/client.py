import requests
import ujson
from typing import Optional
import logging
import time


class NotionService:
    def __init__(self, token: str):
        self._token = token
        self._base_url = 'https://api.notion.com/v1/'
        self._headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2021-08-16'}

    @staticmethod
    def handle_response_status_code(response):
        if response.status_code == 200:
            r = ujson.loads(response.text)
        elif response.status_code == 400:
            r = ujson.loads(response.text)
            logging.error(r)
        elif response.status_code == 401:
            r = ujson.loads(response.text)
            logging.error(r)
        else:
            r = ujson.loads(response.text)
            logging.error(r)
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
        An list with the response of the search.

        """
        params = [('query', query), ('sort', sort), ('filter', filter), ('start_cursor', start_cursor),
                  ('page_size', page_size)]
        params_dict = {p[0]: p[1] for p in params if p[1] is not None}
        payload = ujson.dumps(params_dict)
        for i in range(max_retries):
            response = requests.request('POST', self._base_url + 'search', headers=self._headers, data=payload)
            search = self.handle_response_status_code(response)
            if search is not None:
                break
        if search is None:
            logging.error('Max retries reached and connection is not available')
        return search

    def get_page(self, page_id: str, max_retries: Optional[int] = 2):
        """
        Retrieves a Page object using the ID specified.

        Parameters
        ----------
        page_id     : Identifier for a Notion page.
        max_retries : If there is an error of connection, how many times to retry.

        Returns
        -------
        Page object
        """
        endpoint = f'pages/{page_id}'
        for i in range(max_retries):
            response = requests.request('GET', self._base_url + endpoint, headers=self._headers)
            page_response = self.handle_response_status_code(response)
            if page_response is not None:
                break
        if page_response is None:
            logging.error('Max retries reached and connection is not available')
        return page_response

    def get_block(self, block_id: str, max_retries: Optional[int] = 2):
        """
        Retrieves a Block object using the ID specified.

        Parameters
        ----------
        block_id    : Identifier for a Notion block.
        max_retries : If there is an error of connection, how many times to retry.

        Returns
        -------
        Block object.
        """
        endpoint = f'blocks/{block_id}'
        for i in range(max_retries):
            response = requests.request('GET', self._base_url + endpoint, headers=self._headers)
            block_response = self.handle_response_status_code(response)
            if block_response is not None:
                break
        if block_response is None:
            logging.error('Max retries reached and connection is not available')
        return block_response

    def get_block_children(self, block_id: str, start_cursor: Optional[str] = None, page_size: Optional[int] = 100,
                           max_retries: Optional[int] = 2):
        """
        Returns a paginated array of child block objects contained in the block using the ID specified.
        In order to receive a complete representation of a block, you may need to recursively retrieve
        the block children of child blocks.

        Parameters
        ----------
        block_id     : Identifier for a block
        start_cursor : If supplied, this endpoint will return a page of results starting after the cursor provided.
                       If not supplied, this endpoint will return the first page of results.
        page_size    : The number of items from the full list desired in the response. Maximum: 100
        max_retries  : If there is an error of connection, how many times to retry.

        Returns
        -------
        A list of the children of the block.
        """
        endpoint = f'blocks/{block_id}/children'
        params = [('start_cursor', start_cursor), ('page_size', page_size)]
        params_dict = {p[0]: p[1] for p in params if p[1] is not None}
        for i in range(max_retries):
            response = requests.request('GET', self._base_url + endpoint, headers=self._headers, params=params_dict)
            block_children = self.handle_response_status_code(response)
            if block_children is not None:
                break
        if block_children is None:
            logging.error('Max retries reached and connection is not available')
        return block_children

    def get_database(self, database_id: str, max_retries: Optional[int] = 2):
        """
        Retrieves a Database object using the ID specified.

        Parameters
        ----------
        database_id : Identifier for a Notion database
        max_retries : If there is an error of connection, how many times to retry.

        Returns
        -------
        Database object
        """
        endpoint = f'databases/{database_id}'
        for i in range(max_retries):
            response = requests.request('GET', self._base_url + endpoint, headers=self._headers)
            database = self.handle_response_status_code(response)
            if database is not None:
                break
        if database is None:
            logging.error('Max retries reached and connection is not available')
        return database

    def query_database(self, database_id: str, filter: Optional[dict] = None, sorts: Optional[dict] = None, start_cursor: Optional[str] = None, page_size: Optional[int] = 100, max_retries: Optional[int] = 2):
        endpoint = f'databases/{database_id}/query'
        params = [('filter', filter), ('sorts', sorts), ('start_cursor', start_cursor), ('page_size', page_size)]
        params_dict = {p[0]: p[1] for p in params if p[1] is not None}
        payload = ujson.dumps(params_dict)
        for i in range(max_retries):
            response = requests.request('POST', self._base_url + endpoint, headers=self._headers, data=payload)
            query = self.handle_response_status_code(response)
            if query is not None:
                break
        if query is None:
            logging.error('Max retries reached and connection is not available')
        return query

