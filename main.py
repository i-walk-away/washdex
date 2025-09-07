import json

from src.carwash_constructor import CarwashConstructor
from src.carwash_editor import CarwashEditor


def load() -> list[dict]:
    with open('data/test_data.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
        return test_data


def edit_carwashes():
    input_data = load()
    editor = CarwashEditor(input_data)

    editor.update_prices(input_data[0], 'express')
    editor.update_prices(input_data[1], 'complex')
    editor.update_prices(input_data[2], 'standart')

    editor.save_all_data_to_json('data/test_data_new.json')


def create_new_carwash():
    input_data = load()
    constructor = CarwashConstructor(input_data)

    new_carwash = constructor.create_new_carwash()
    constructor.save_carwash_to_json('data/new_carwash.json', new_carwash)


def main() -> None:
    edit_carwashes()
    create_new_carwash()


if __name__ == '__main__':
    main()
