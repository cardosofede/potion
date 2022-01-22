# %%
from potion.client import Notion
import json
import pprint

notion = Notion(token='secret_ajWv3kiGIDiXz427A48zROIvNCegMgByXiHTt1aJvx')

r = notion.search(query='Strategy')


# %%
pprint.pprint(r)
