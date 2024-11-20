import os
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open

try:
    from task2.solution import count_category_fst_letters, save_dict_to_csv
except ImportError as e:
    raise unittest.SkipTest("Task 2 is not completed yet")


class TestTask2_CountCategoryFstLetters(unittest.TestCase):
    @patch('requests.Session.get')
    def test_no_pagination(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'query': {
                'categorymembers': [
                    {'title': 'Аксолотль'},
                    {'title': 'Альбатрос'},
                    {'title': 'Броненосец'},
                    {'title': 'Ворона'},
                ],
            },
        }
        mock_get.return_value = mock_response

        res = count_category_fst_letters()

        self.assertEqual(res['А'], 2)
        self.assertEqual(res['Б'], 1)
        self.assertEqual(res['В'], 1)
        self.assertEqual(len(res), 3)

    @patch('requests.Session.get')
    def test_with_pagination(self, mock_get):
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = {
            'query': {
                'categorymembers': [
                    {'title': 'Аксолотль'},
                    {'title': 'Альбатрос'},
                    {'title': 'Броненосец'},
                    {'title': 'Ворона'},
                ],
            },
            'continue': {'next': 5},
        }

        mock_response_2 = MagicMock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = {
            'query': {
                'categorymembers': [
                    {'title': 'Абиссинский заяц'},
                    {'title': 'Волк'},
                    {'title': 'Гиена'},
                ],
            },
        }

        mock_get.side_effect = [mock_response_1, mock_response_2]

        res = count_category_fst_letters()

        self.assertEqual(res['А'], 3)
        self.assertEqual(res['Б'], 1)
        self.assertEqual(res['В'], 2)
        self.assertEqual(res['Г'], 1)
        self.assertEqual(len(res), 4)

    @patch('requests.Session.get')
    def test_404(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(RuntimeError):
            count_category_fst_letters()

    @patch('requests.Session.get')
    def test_incorrect_response1(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'continue': {'next': 5},
        }
        mock_get.return_value = mock_response

        with self.assertRaises(RuntimeError):
            count_category_fst_letters()

    @patch('requests.Session.get')
    def test_incorrect_response2(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'query': 'abc',
            'continue': {'next': 5},
        }
        mock_get.return_value = mock_response

        with self.assertRaises(RuntimeError):
            count_category_fst_letters()

    @patch('requests.Session.get')
    def test_incorrect_response3(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'query': {
                'categorymembers': ['a'],
            },
        }
        mock_get.return_value = mock_response

        with self.assertRaises(RuntimeError):
            count_category_fst_letters()


class TestTask2_SaveDictToCSV(unittest.TestCase):
    def setUp(self):
        self.test_dict = {'A': 2, 'B': 1, 'C': 3}
        self.test_file_path = 'test_beasts.csv'

    @patch('builtins.open', new_callable=mock_open)
    def test_no_errors(self, mock_file):
        save_dict_to_csv(self.test_dict, self.test_file_path)

        mock_file.assert_called_once_with(self.test_file_path, 'w')
        mock_file().write.assert_any_call(f'A,2{os.sep}')
        mock_file().write.assert_any_call(f'B,1{os.sep}')
        mock_file().write.assert_any_call(f'C,3{os.sep}')

    @patch('builtins.open', side_effect=OSError)
    @patch('sys.stdout', new_callable=StringIO)
    def test_with_os_error(self, mock_stdout, mock_open):
        save_dict_to_csv(self.test_dict, self.test_file_path)

        output = mock_stdout.getvalue()
        self.assertIn('A,2', output)
        self.assertIn('B,1', output)
        self.assertIn('C,3', output)

        mock_open.assert_called_once_with(self.test_file_path, 'w')
