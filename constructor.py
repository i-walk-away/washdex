import json

import random
import re
from datetime import datetime, timezone
from uuid import uuid4


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def update_prices(component):
    return {k: {**v, 'include_service_amount': random.randint(100000, 5000000)} if isinstance(v, dict) else v
            for k, v in component.items()}


def create_new_carwash(source):
    now = datetime.now(timezone.utc).isoformat()

    return {
        '_id': uuid4().hex,
        'carwash_id': uuid4().hex,
        'network_id': uuid4().hex,
        'date_create': {'$date': now},
        'start_date_time': {'$date': now},
        'end_date_time': None,
        'tariffs': [{
            camel_to_snake(k): [{
                camel_to_snake(pk): update_prices(pv) if pk == 'PriceComponent' else pv
                for pk, pv in pe.items()
            } for pe in v] if k == 'PriceElements' else v
            for k, v in t.items()
        } for t in source['Tariffs']]
    }


# Usage
with open('data/test_data.json', 'r') as f:
    source_data = json.load(f)[0]

result = create_new_carwash(source_data)

with open('data/new_carwash.json', 'w') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)