# %%
from potion.client import NotionService
from potion.notion_database import NotionDatabase
import ujson
import pprint
import pandas as pd

notion = NotionService(token='secret_ajWv3kiGIDiXz427A48zROIvNCegMgByXiHTt1aJvxl')

# search = notion.search(query='51549ef7-8244-43f4-88f1-6e9ca2f0ad55')
# page = notion.get_page(page_id='51549ef7-8244-43f4-88f1-6e9ca2f0ad55')
# block = notion.get_block(block_id='51549ef7-8244-43f4-88f1-6e9ca2f0ad55')
block_children = notion.get_block_children(block_id='51549ef7-8244-43f4-88f1-6e9ca2f0ad55')
query = notion.query_database(database_id='7bef5982-81d0-4784-80a5-171ec02eaa43')
database = notion.get_database(database_id='7bef5982-81d0-4784-80a5-171ec02eaa43')
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
       (Iter({T[0]: (T[1], Coalesce('price_ceiling.id', 'price_ceiling.number', default=0))})),
       'fibo')
print(test)

# %%
trading_pair = 'BTCUSDT'
start = '2022-01-25'
end = '2022-01-29'
exchange = 'FTX'
initial_portfolio_value = 25000
initial_base_asset_price = 2400
order_amount = 10
bid_spread = 0.3
ask_spread = 0.4
order_refresh_time = 50
ping_pong_enabled = True
order_levels = 2
order_level_amount = 5
order_level_spread = 0.2
filled_order_delay = 8
hanging_orders_enabled = True
order_optimization_enabled = False
inventory_skew_enabled = True
inventory_range_multiplier = 43
ask_order_optimization_depth = 0.5
bid_order_optimization_depth = 0.4
price_ceiling = 2500
price_floor = None


properties = {
    'trading_pair': {
        'title': [
            {
                'text': {
                    'content': trading_pair
                }
            }
        ]
    },
    'start': {
        'date': {
            'start': start
        }
    },
    'end': {
        'date': {
            'start': end
        }
    },
    'exchange': {
        'select': {
            'name': exchange
        }
    },
    'initial_portfolio_value': {
        'number': initial_portfolio_value
    },
    'initial_base_asset_price': {
        'number': initial_base_asset_price
    },
    'order_amount': {
        'number': order_amount
    },
    'bid_spread': {
        'number': bid_spread
    },
    'ask_spread': {
        'number': ask_spread
    },
    'order_refresh_time': {
        'number': order_refresh_time
    },
    'ping_pong_enabled': {
        'checkbox': ping_pong_enabled
    },
    'order_levels': {
        'number': order_levels
    },
    'order_level_amount': {
        'number': order_level_amount
    },
    'order_level_spread': {
        'number': order_level_spread
    },
    'filled_order_delay': {
        'number': filled_order_delay
    },
    'hanging_orders_enabled': {
        'checkbox': hanging_orders_enabled
    },
    'order_optimization_enabled': {
        'checkbox': order_optimization_enabled
    },
    'inventory_skew_enabled': {
        'checkbox': inventory_skew_enabled
    },
    'inventory_target_base_pct': {
        'number': 50
    },
    'inventory_range_multiplier': {
        'number': inventory_range_multiplier
    },
    'ask_order_optimization_depth': {
        'number': ask_order_optimization_depth
    },
    'bid_order_optimization_depth': {
        'number': bid_order_optimization_depth
    },
    'price_ceiling': {
        'number': price_ceiling
    },
    'price_floor': {
        'number': price_floor
    }
}
notion.create_page(parent={'database_id': '7bef5982-81d0-4784-80a5-171ec02eaa43'},
                   properties=properties)

# %%
pprint.pprint(query._notion_response)

#%%
print(query.df)


# %%
import os

os.system("say 'Oh mr dardo man'")
os.system("say 'You know what Im talking about O G'")
os.system("say 'in grita'")
# %%
