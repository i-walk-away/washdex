import json
import random
import re
from datetime import datetime, timezone
from uuid import uuid4


class CarwashConstructor:
    def __init__(self, input_data):
        self.input_data = input_data

    @staticmethod
    def _camel_to_snake(input_string: str):
        input_string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', input_string).lower()

    @staticmethod
    def _update_prices(component):
        """
        Update price component with random service amount.
        """
        return {
            key: {
                **value,
                'include_service_amount': random.randint(100000, 5000000)
            } if isinstance(value, dict) else value
            for key, value in component.items()
        }

    def _convert_keys_to_snake_case_recursive(self, data):
        """
        Recursively convert all dictionary keys to snake case.

        Args:
            data: The data structure to process (dict, list, or primitive)

        Returns:
            Data structure with all keys converted to snake_case
        """
        if isinstance(data, dict):
            return {
                self._camel_to_snake(key): self._convert_keys_to_snake_case_recursive(value)
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
        Append the newly created carwash to an existing JSON file.
        """
        try:
            # Load existing data
            with open(path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)

            # Append new carwash
            existing_data.append(carwash)

            # Save back to file
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)

            print(f"Appended new carwash to {path}. Total carwashes: {len(existing_data)}")

        except Exception as e:
            print(f'Failed to append carwash to {path}: {e}')

    def create_new_carwash(self) -> dict:
        """
        Create a new carwash object with all keys in snake_case.
        """
        now = datetime.now(timezone.utc).isoformat()
        source = self.input_data[0]

        # Create initial carwash structure with original keys
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

        # Convert ALL keys to snake case recursively (including nested ones)
        return self._convert_keys_to_snake_case_recursive(carwash)
