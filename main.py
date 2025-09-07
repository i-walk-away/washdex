import json

from src.carwash_constructor import CarwashConstructor
from src.carwash_editor import CarwashEditor


def load() -> list[dict]:
    with open('data/test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
        return test_data


def edit_carwashes() -> None:
    input_data = load()
    editor = CarwashEditor(input_data)

    editor.update_prices(input_data[0], 'express')
    editor.update_prices(input_data[1], 'complex')
    editor.update_prices(input_data[2], 'standart')

    editor.save_all_data_to_json('data/test_data_new.json')


def create_new_carwash() -> dict:
    input_data = load()
    constructor = CarwashConstructor(input_data)

    new_carwash = constructor.create_new_carwash()

    constructor.append_to_existing_json('data/test_data_new.json', new_carwash)


def main() -> None:
    # edit existing carwashes and save to test_data_new.json
    edit_carwashes()

    # create new carwash
    create_new_carwash()


if __name__ == '__main__':
    main()
