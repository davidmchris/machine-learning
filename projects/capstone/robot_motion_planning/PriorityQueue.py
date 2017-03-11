class PriorityQueue:
    def __init__(self):
        self.queue = {}

    def insert(self, priority, item):
        # type: (int, object) -> None
        if priority in self.queue:
            self.queue[priority].append(item)
        else:
            self.queue[priority] = [item]

    def pop_min(self):
        min_entry = self.queue.popitem()
        priority = min_entry[0]
        elements = min_entry[1]
        value_to_pop = elements.pop()
        if len(elements) != 0:
            self.queue[priority] = elements
        return value_to_pop

    def __len__(self):
        """This doesn't return the number of values left, it returns the number of priority entries."""
        return len(self.queue)

