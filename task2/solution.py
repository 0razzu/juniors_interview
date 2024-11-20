import os
from itertools import count

import requests

CATEGORY_NAME = 'Категория:Животные по алфавиту'
FILE_PATH = 'beasts.csv'


def count_category_fst_letters(category: str = CATEGORY_NAME) -> dict[str, int]:
    url = 'https://ru.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'cmtitle': category,
        'cmlimit': 10000,
        'cmprop': 'title',
        'list': 'categorymembers',
        'format': 'json',
    }

    fst_letter_2_quan = {}

    with requests.Session() as session:
        last_continue = {}
        for i in count(1):
            print(f'Sending request #{i}')
            response = session.get(url=url, params=(params | last_continue))

            if response.status_code != 200:
                raise RuntimeError(f'Error: Received status code {response.status_code} for request #{i}')

            data = response.json()

            try:
                pages = data['query']['categorymembers']

                for page in pages:
                    fst_letter = page['title'][0]
                    fst_letter_2_quan[fst_letter] = fst_letter_2_quan.get(fst_letter, 0) + 1
            except (KeyError, TypeError):
                raise RuntimeError(f'Error: No pages found in response for request #{i}')

            if 'continue' not in data:
                break

            last_continue = data['continue']

    print(f'Got {sum(fst_letter_2_quan.values())} titles')

    return fst_letter_2_quan


def save_dict_to_csv(d: dict, path: str = FILE_PATH) -> None:
    print(f'Writing to «{path}»')
    try:
        with open(path, 'w') as f:
            for k, v in d.items():
                f.write(f'{k},{v}{os.sep}')
        print('Done')
    except OSError:
        print(f'Failed to open file «{path}» – writing to stdout')
        for k, v in d.items():
            print(f'{k},{v}')


if __name__ == '__main__':
    save_dict_to_csv(count_category_fst_letters())
