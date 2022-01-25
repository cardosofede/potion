# %%
from potion.client import NotionService
import ujson
import pprint
import pandas as pd

notion = NotionService(token='secret_ajWv3kiGIDiXz427A48zROIvNCegMgByXiHTt1aJvxl')

# search = notion.search(query='51549ef7-8244-43f4-88f1-6e9ca2f0ad55')
# page = notion.get_page(page_id='51549ef7-8244-43f4-88f1-6e9ca2f0ad55')
# block = notion.get_block(block_id='51549ef7-8244-43f4-88f1-6e9ca2f0ad55')
# block_children = notion.get_block_children(block_id='51549ef7-8244-43f4-88f1-6e9ca2f0ad55')
query = notion.query_database(database_id='7bef5982-81d0-4784-80a5-171ec02eaa43')
# database = notion.get_database(database_id='7bef5982-81d0-4784-80a5-171ec02eaa43')
pprint.pprint(query)

# %%
from glom import *

def get_table(data_json):
    spec = {'properties': (T['properties'].items(),
                           Iter({T[0]: (T[1], Coalesce('number',
                                                       'select.name',
                                                       'checkbox',
                                                       'date.start',
                                                       # ({'start': 'date.start', 'end': 'date.end'}),
                                                       ('title', ['plain_text'], lambda x: x[0]),
                                                       default=0))}),
                           Merge()),
            'id': Coalesce('id')
            }
    table = [glom(result, spec)['properties'] for result in data_json['results']]
    return table

df = pd.DataFrame(get_table(query))
# %%
test = query['results'][0]['properties']
print(test)

Assign(test,
       (Iter({T[0]: (T[1],Coalesce('price_ceiling.id', 'price_ceiling.number', default=0))})),
       'fibo')
print(test)


