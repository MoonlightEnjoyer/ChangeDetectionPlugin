from .list_element import ListElement

class CycleList:
    def __init__(self, size):
        self.size = size
        self.head = ListElement(True)
        self.current_element = self.head
        for i in range(size - 1):
            self.current_element.next = ListElement()
            self.current_element = self.current_element.next
        
        self.current_element.next = self.head
        self.current_element = self.head

    def insert(self, value):
        cur = self.current_element.value
        for i in range(self.size):
            temp = self.current_element.next.value
            self.current_element.next.value = cur
            self.current_element = self.current_element.next
            cur = temp

        self.current_element.value = value

    def to_list(self):
        result = []

        for i in range(self.size):
            result.append(self.head.value)
            self.head = self.head.next

        return result