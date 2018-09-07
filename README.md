# Find newest phone activation date

## Overview

### 1. The data is transformed into a dictionary (FindLastActivationDate.phone_numbers)

The key of the dictionary is the phone number, the value is a Phone number object. 
The core of the PhoneNumber object is PhoneNumber.date_dictionary. 
The key of this dictionary is a distinct date and the value can either of these three values:

- 0b01 (if the date only appear as activation date) 
- 0b10 (if the date only appear as deactivation date),
- 0b11 (if both) 

### 2. For each phone number, find the newest activation date (PhoneNumber.find_last_activation_date)

We now look at PhoneNumber.date_dictionary of each phone number. 
For each date in PhoneNumber.date_dictionary, we look for the date with corresponding value =  0b01. Why?
Obviously we don't care about deactivation date so we don't care those with 0b10. 
Those with value of 0b11 represents transition from prepaid to postpaid or vice versa.
Therefore, 0b01 is what we are interested.

## Complexity analysis

### Time

The whole algorithm takes O(n) in terms of time. The two key steps of the program is 
FindLastActivationDate.initialize_phone_numbers and FindLastActivationDate.run. 
As these two run sequentially and each takes O(n), the whole algorithm time complexity is O(n).
Please refer to comment throughout the code for detailed proof of these two statements:
- Time complexity of FindLastActivationDate.initialize_phone_numbers is O(n)
- Time complexity of FindLastActivationDate.run is O(n)

### Space

The whole algorithm takes O(n) in terms of space. 
FindLastActivationDate.initialize_phone_numbers allocates O(n) memory while 
FindLastActivationDate.run allocates O(c).
Therefore, the whole algorithm space complexity is O(n).

### Data structure processing time

As the data structure using here is Python dictionary which basically is a hash table, 
searching for an element, insertion, and deletion all takes O(c) on average.
However, in worse case (when needs to allocate more space), the whole data structure needs to be clone.
In this case, searching for an element, insertion, and deletion all takes O(n).  