# Name: Matt Chalabian
# OSU Email: chalabim@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: March 11, 2022
# Description: HashMap class that uses the open addressing method with a DynamicArray.
#   Contains various methods including put(), get(), remove(), resize(), get_keys(), etc.


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the hash table of all key/value pairs.
        """
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(None)
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns the value of key argument in hash table if present, otherwise returns None
        """
        probe_val = 0
        hash_val = self.hash_function(key) % self.capacity
        index = (hash_val + probe_val ** 2) % self.capacity
        while self.buckets[index] is not None:
            if self.buckets[index].key == key and not self.buckets[index].is_tombstone:
                return self.buckets[index].value
            probe_val += 1
            index = (hash_val + probe_val ** 2) % self.capacity
        return None

    def put(self, key: str, value: object) -> None:
        """
        Inserts a new key/value pair in the hash table or replaces a value if the
        key argument already exists in the hash table.  Resizes the table if the load is
        greater than or equal to 0.5.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)

        probe_val = 0
        hash_val = self.hash_function(key)
        index = (hash_val + probe_val ** 2) % self.capacity
        while self.buckets[index] is not None:
            if self.buckets[index].key == key and not self.buckets[index].is_tombstone:
                self.buckets[index].value = value
                return
            elif self.buckets[index].is_tombstone:
                self.buckets[index] = HashEntry(key, value)
                self.size += 1
                return
            probe_val += 1
            index = (hash_val + probe_val ** 2) % self.capacity

        self.buckets[index] = HashEntry(key, value)
        self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes a key/value pair from hash table if key argument is present.
        """
        probe_val = 0
        hash_val = self.hash_function(key)
        index = (hash_val + probe_val ** 2) % self.capacity
        while self.buckets[index] is not None:
            if self.buckets[index].key == key and not self.buckets[index].is_tombstone:
                self.buckets[index].is_tombstone = True
                self.size -= 1
            probe_val += 1
            index = (hash_val + probe_val ** 2) % self.capacity

    def contains_key(self, key: str) -> bool:
        """
        Returns a boolean for if a key is present in the hash table.
        """
        probe_val = 0
        hash_val = self.hash_function(key)
        index = (hash_val + probe_val ** 2) % self.capacity
        while self.buckets[index] is not None:
            if self.buckets[index].key == key and not self.buckets[index].is_tombstone:
                return True
            probe_val += 1
            index = (hash_val + probe_val ** 2) % self.capacity
        return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_counter = 0
        for index in range(self.capacity):
            if self.buckets[index] is None:
                empty_counter += 1
        return empty_counter

    def table_load(self) -> float:
        """
        Returns the hash table's load factor.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table if arguments is greater than 0.
        """
        if new_capacity < 1 or new_capacity < self.size:
            return

        new_map = HashMap(new_capacity, self.hash_function)
        for index in range(self.capacity):
            if self.buckets[index] is not None and not self.buckets[index].is_tombstone:
                new_map.put(self.buckets[index].key, self.buckets[index].value)
        self.capacity = new_map.capacity
        self.buckets = new_map.buckets

    def get_keys(self) -> DynamicArray:
        """
        Returns a Dynamic Array containing all keys in hash map.
        """
        key_array = DynamicArray()
        for index in range(self.capacity):
            if self.buckets[index] is not None and not self.buckets[index].is_tombstone:
                key_array.append(self.buckets[index].key)
        return key_array


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
