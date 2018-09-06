import csv
from datetime import datetime
from typing import Dict

PATH_TO_RESULT = "result.csv"
ERROR_MESSAGE_WHEN_CANNOT_FIND_LAST_ACTIVATION_DATE = "Huhm! Weird! How can it is possible that all starting date " \
                                                      "has a corresponding ending date. " \
                                                      "It must be the case that there always exist one starting date without a corresponding ending date!"
BIT_MASK_FOR_ENDING_DATE = 0b10
BIT_MASK_FOR_STARTING_DATE = 0b01
ERROR_MESSAGE_WHEN_DUPLICATION_OCCURS = "Something weird happen. How comes existing two records with same {}?"


# Note the time complexity of the whole program is O(2n) and space complexity is O(n)
def is_starting_date_already_exist(date_nature):
    return date_nature & BIT_MASK_FOR_STARTING_DATE != 0


def is_ending_date_already_exist(date_nature):
    return date_nature & BIT_MASK_FOR_ENDING_DATE != 0


def check_date_user_supply_valid(date_nature, is_starting_date):
    if is_starting_date:
        if is_starting_date_already_exist(date_nature):
            raise Exception(ERROR_MESSAGE_WHEN_DUPLICATION_OCCURS.format("starting date"))
        date_nature += BIT_MASK_FOR_STARTING_DATE
    if not is_starting_date:
        if is_ending_date_already_exist(date_nature):
            raise Exception(ERROR_MESSAGE_WHEN_DUPLICATION_OCCURS.format("ending date"))


class PhoneNumber:
    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number
        # Note number of phone numbers [1; n].
        self.date_dictionary = dict()
        # Note observation: number_of_date_added_so_far is approximately equal to number_of_record_in_input_file
        # assume two of them are equal to make further calculation
        self.number_of_date_added_so_far = 0
        self.number_of_record_in_input_file = 0
        super().__init__()

    # Note this method allocate O(c) memory
    def add_record(self, record):
        activation_date = datetime.strptime(record[1], "%Y-%m-%d")
        deactivation_date = datetime.strptime(record[2], "%Y-%m-%d")
        self.add_date(activation_date, True)
        self.add_date(deactivation_date, False)
        self.number_of_record_in_input_file += 1

    # Note this method allocate O(c) memory if date_nature = None, else not allocate new memory
    def add_date(self, date_user_supply: datetime, is_activation_date: bool):
        # Date nature has only three possible values:
        # 0b01 (if the date is starting date),
        # 0b10 (ending date),
        # 0b11 (both)
        if date_user_supply is None:
            return
        # Note access elements in dict takes O(c)
        date_nature = self.date_dictionary.get(date_user_supply)

        if date_nature:
            check_date_user_supply_valid(date_nature, is_activation_date)
            if is_activation_date:
                # Note modify the value corresponding with the key takes O(c) time
                self.date_dictionary[date_user_supply] += BIT_MASK_FOR_STARTING_DATE
            else:
                self.date_dictionary[date_user_supply] += BIT_MASK_FOR_ENDING_DATE
        else:
            if is_activation_date:
                # Note allocate O(c) memory
                self.date_dictionary[date_user_supply] = BIT_MASK_FOR_STARTING_DATE
            else:
                self.date_dictionary[date_user_supply] = BIT_MASK_FOR_ENDING_DATE
            self.number_of_date_added_so_far += 1

    # Note takes O(number_of_date_added_so_far) in time
    def find_last_activation_dates(self) -> datetime:
        max_date = None
        # Note takes O(number_of_date_added_so_far) in time
        for date, date_nature in self.date_dictionary.items():
            if date_nature == BIT_MASK_FOR_STARTING_DATE:
                if max_date and date > max_date:
                    max_date = date
                else:
                    max_date = date
        return max_date

    # def number_of_records_in_original_file(self):
    #     number_of_records = self.number_of_date_added_so_far / 2
    #     if self.number_of_date_added_so_far % 2 == 0:
    #         return number_of_records
    #     else:
    #         return math.ceil(number_of_records)


class FindLastActivationDate:

    def __init__(self, path_to_file_containing_phone_number: str, containing_header=True,
                 path_to_result: str=PATH_TO_RESULT) -> None:
        self.path_to_file_containing_phone_number = path_to_file_containing_phone_number
        self.containing_header = containing_header
        self.path_to_result = path_to_result
        self.phone_numbers = self.initialize_phone_numbers(path_to_file_containing_phone_number)

    # Note this method takes O(n) time, O(n) memory
    def initialize_phone_numbers(self, path_to_file_containing_phone_number: str) -> Dict[str, PhoneNumber]:
        phone_numbers = dict()
        with open(path_to_file_containing_phone_number, 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if self.containing_header:
                next(reader)
            # Note this takes O(n) time, O(2n) memory
            for record in reader:
                phone_number = record[0]
                # TODOx check month format
                if not phone_numbers[phone_number]:
                    #  Note memory allocate O(c) here
                    phone_numbers[phone_number] = PhoneNumber(phone_number)
                phone_number_object = phone_numbers[phone_number]
                # TODOx check time complexity
                # TODOx check allocate memory
                # Note this method allocates O(c) memory)
                phone_number_object.add_record(record)

        return phone_numbers

    # Note time complexity of this method is O(n), O(c) memory
    def run(self):
        with open(self.path_to_result, 'w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["PHONE_NUMBER", "REAL_ACTIVATION_DATE"])

            # this method takes:
            # SUM(i_frst=0, i_last=number_of_phone_numbers, number_of_date_added_so_far) ~=
            # SUM(i_frst=0, i_last=number_of_phone_numbers, number_of_record_in_input_file) = n
            # Therefore, time complexity of this method is O(n)
            # TODOx checking my assumption
            for phone_number, phone_number_object in self.phone_numbers.items():
                # TODOx check time complexity of this method
                last_activation_date = phone_number_object.find_last_activation_dates()
                writer.writerow([phone_number, last_activation_date])
