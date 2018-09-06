import unittest

from Main import FindLastActivationDate

PATH_TO_RESULT = "result.csv"

PATH_TO_INPUT_FILE = "import.csv"


class TestFindLastActivationDate(unittest.TestCase):

    def setUp(self):
        self.find_last_activation_date = FindLastActivationDate(PATH_TO_INPUT_FILE, path_to_result=PATH_TO_RESULT)

    def test_whole_program(self):
        self.find_last_activation_date.run()
        # TODO check exist result file
        # TODO check exist header
        # TODO check a record have two col
        # TODO check first col is a phone number
        # TODO check second col is a date
        # fixme the date print to csv is not at the correct format

    def test_initialize_phone_numbers(self):
        pass

    def test_add_record(self):
        pass

    def test_add_date(self):
        pass

    def test_find_last_activation_date(self):
        pass
