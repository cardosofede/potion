import pandas as pd
from glom import *


class NotionDatabase:
    def __init__(self, response):
        self._notion_response = response
        self._df = self.transform_json_to_df()

    @property
    def df(self):
        return self._df

    def transform_json_to_df(self):
        spec = {'properties': (T['properties'].items(),
                               Iter({T[0]: (T[1], Coalesce('number',
                                                           'select.name',
                                                           'checkbox',
                                                           'date.start',
                                                           ('multi_select', ['name']),
                                                           # ({'start': 'date.start', 'end': 'date.end'}),
                                                           ('title', ['plain_text'], lambda x: x[0]),
                                                           default=0))}),
                               Merge()),
                'id': Coalesce('id')
                }
        table = [glom(result, spec)['properties'] for result in self._notion_response['results']]
        return pd.DataFrame(table)
