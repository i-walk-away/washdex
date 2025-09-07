import json
import random
import re
from datetime import datetime, timezone
from uuid import uuid4


class CarwashConstructor:
    def __init__(self, input_data):
        self.input_data = input_data

    @staticmethod
    def _str_to_snake_case(input_string: str) -> str:
        """
        Refactor any string into snake_case.

        :param input_string: string to refactor
        :return: snake_cased string
        """
        input_string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', input_string).lower()

    @staticmethod
    def _update_prices(component: dict) -> dict:
        """
        Assign random service price for a given PriceComponent.
        """
        return {
            key: {
                **value,
                'include_service_amount': random.randint(100000, 5000000)
            } if isinstance(value, dict) else value
            for key, value in component.items()
        }

    def _convert_keys_to_snake_case_recursive(self, data: dict | list) -> dict | list:
        """
        Recursively convert all dictionary keys (nested included) to snake_case.
        """
        if isinstance(data, dict):
            return {
                self._str_to_snake_case(key): self._convert_keys_to_snake_case_recursive(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [
                self._convert_keys_to_snake_case_recursive(item)
                for item in data
            ]
        else:
            return data

    @staticmethod
    def append_to_existing_json(path: str, carwash: dict) -> None:
        """
        Append the newly created carwash to an existing JSON file with other carwashes.
        """
        try:
            # load existing data
            with open(path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)

            existing_data.append(carwash)

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)

            print(f"appended new carwash to {path}. total carwashes: {len(existing_data)}")

        except Exception as e:
            print(f'failed to append carwash to {path}: {e}')

    def create_new_carwash(self) -> dict:
        """
        Create a new carwash object with all keys in snake_case.
        """
        now = datetime.now(timezone.utc).isoformat()
        source = self.input_data[0]

        carwash = {
            '_id': uuid4().hex,
            'carwash_id': uuid4().hex,
            'network_id': uuid4().hex,
            'date_create': {'$date': now},
            'start_date_time': {'$date': now},
            'end_date_time': None,
            'tariffs': [
                {
                    key: [
                        {
                            inner_key: (
                                self._update_prices(inner_value)
                                if inner_key == 'PriceComponent'
                                else inner_value
                            )
                            for inner_key, inner_value in element.items()
                        }
                        for element in value
                    ]
                    if key == 'PriceElements'
                    else value
                    for key, value in tariff.items()
                }
                for tariff in source['Tariffs']
            ]
        }

        # convert ALL keys to snake case recursively (including nested keys)
        return self._convert_keys_to_snake_case_recursive(carwash)
