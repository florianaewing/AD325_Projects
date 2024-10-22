class LinkedDeque:
    class DLNode:
        def __init__(self, previous_node=None, data=None, next_node=None):
            self.previous_node = previous_node
            self.data = data
            self.next_node = next_node

    def __init__(self):
        self.head = None  # Front of the deque
        self.tail = None  # Back of the deque
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def add_to_front(self, new_data):
        new_node = self.DLNode(None, new_data, self.head)
        if self.is_empty():
            self.tail = new_node  # If deque is empty, new node is both head and tail
        else:
            self.head.previous_node = new_node
        self.head = new_node
        self.size += 1

    def add_to_back(self, new_data):
        new_node = self.DLNode(self.tail, new_data, None)
        if self.is_empty():
            self.head = new_node  # If deque is empty, new node is both head and tail
        else:
            self.tail.next_node = new_node
        self.tail = new_node
        self.size += 1

    def remove_front(self):
        if self.is_empty():
            return None
        removed_data = self.head.data
        self.head = self.head.next_node
        if self.head is not None:
            self.head.previous_node = None
        else:
            self.tail = None  # If the deque becomes empty
        self.size -= 1
        return removed_data

    def remove_back(self):
        if self.is_empty():
            return None
        removed_data = self.tail.data
        self.tail = self.tail.previous_node
        if self.tail is not None:
            self.tail.next_node = None
        else:
            self.head = None  # If the deque becomes empty
        self.size -= 1
        return removed_data

    def peek_front(self):
        if self.is_empty():
            return None
        return self.head

    def peek_back(self):
        if self.is_empty():
            return None
        return self.tail

    def display(self):
        current = self.front
        while current is not None:
            print(current.get_data(), end=" ")
            current = current.get_next_node()
        print()  # for new line

    def __iter__(self):
        current = self.front
        while current:
            yield current.get_data()
            current = current.get_next_node()
