import json

from src.case_insensitive_dict import CaseInsensitiveDict
from src.constants import NEW_PRICES, POSSIBLE_IDENTIFIERS


class CarwashEditor:
    def __init__(self, input_data):
        self.input_data = input_data
        self.processed_data = []

    @staticmethod
    def convert_dict(input_data: dict) -> CaseInsensitiveDict:
        """
        Loads the input JSON data as a `CaseInsensitiveDict`.

        :return: input JSON data as a `CaseInsensitiveDict`
        """
        return CaseInsensitiveDict(input_data)

    @staticmethod
    def find_identifier(tariff: dict) -> str | None:
        """
        Looks for possible names of the ID key field in a given
        Tariff and returns the exact name of the key.
        `POSSIBLE_IDENTIFIERS` is a tuple which contains possible names of the ID key.
        """
        for identifier in POSSIBLE_IDENTIFIERS:
            if identifier in tariff:
                for key in tariff.keys():
                    if key.lower() == identifier.lower():
                        return key
        return None

    def update_prices(self, input_carwash: dict, tariff_name: str) -> None:
        """
        updates given tariff's prices for a given carwash.

        :param input_carwash: Carwash to update the tariff pricing for.
        :param tariff_name: Name of the Tariff to update its pricing.
        """
        carwash = self.convert_dict(input_carwash)

        for tariff in carwash['tariffs']:
            identifier = self.find_identifier(tariff)

            if identifier and tariff[identifier].lower() == tariff_name.lower():
                for element in tariff['priceelements']:
                    price_component = element['pricecomponent']
                    for car_type, amount in NEW_PRICES[tariff_name].items():
                        car_data = price_component[car_type.lower()]
                        car_data['includeserviceamount'] = amount

        # Add the processed carwash to the list instead of saving immediately
        self.processed_data.append(carwash.to_dict())

    def save_all_data_to_json(self, path) -> None:
        """
        Saves all processed carwashes to a JSON file.
        """
        with open(path, 'w', encoding='utf-8') as f:
            try:
                json.dump(self.processed_data, f, indent=2, ensure_ascii=False)
                print('carwash data saved successfully')
            except Exception as e:
                print(f'failed to save edited carwash data: {e}')
