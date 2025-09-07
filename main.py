import json

from ci_dict import CaseInsensitiveDict
from constants import NEW_PRICES, POSSIBLE_IDENTIFIERS


def load() -> list[CaseInsensitiveDict]:
    """
    Loads the input JSON data as a `CaseInsensitiveDict`.

    :return: input JSON data as a `CaseInsensitiveDict`
    """
    with open('data/test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
        return [CaseInsensitiveDict(data) for data in test_data]


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
                    #print(key)
                    return key
    return None


def update_prices(carwash: CaseInsensitiveDict, tariff_name: str) -> None:
    """
    updates given tariff's prices for a given carwash.

    :param carwash: Carwash to update the tariff pricing for.
    :param tariff_name: Name of the Tariff to update its pricing.
    """
    for tariff in carwash['tariffs']:
        identifier = find_identifier(tariff)

        if tariff[identifier].lower() == tariff_name.lower():
            for element in tariff['priceelements']:
                price_component = element['pricecomponent']
                for car_type, amount in NEW_PRICES[tariff_name].items():
                    car_data = price_component[car_type.lower()]
                    car_data['includeserviceamount'] = amount


def save_data_to_json(input_data: list[CaseInsensitiveDict]) -> None:
    """
    Converts `CaseInsensitiveDict` back to dict and saves it into a JSON file.
    """
    serializable_data = [carwash.to_dict() for carwash in input_data]

    with open('data/test_data_new.json', 'w', encoding='utf-8') as f:
        json.dump(serializable_data, f, indent=2, ensure_ascii=False)


def main() -> None:
    input_data = load()

    # updates specific tariff's prices for specific carwashes
    update_prices(input_data[0], 'express')
    update_prices(input_data[1], 'complex')
    update_prices(input_data[2], 'standart')

    save_data_to_json(input_data)


if __name__ == '__main__':
    main()
