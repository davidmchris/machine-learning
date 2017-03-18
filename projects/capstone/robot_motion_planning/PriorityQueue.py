from collections import deque

class PriorityQueue:
    def __init__(self, lifo=True):
        self.is_lifo = lifo
        self.q = {}
        self.insert_count = 0

    def insert(self, priority, item):
        # type: (int, object) -> None
        if item in self.q:
            raise Exception("Item already in queue. Use update_priority instead.")
        self.q[item] = (priority, self.insert_count)
        self.insert_count += 1

    def pop_min(self):
        key, value = self.q.popitem()
        self.q[key] = value
        min_priority = value[0]
        best_insert_index = value[1]
        min_item = key
        for i in self.q:
            priority = self.q[i][0]
            insert_index = self.q[i][1]
            if priority < min_priority:
                min_priority = priority
                best_insert_index = insert_index
                min_item = i
            elif priority == min_priority:
                if best_insert_index > insert_index == self.is_lifo:
                    min_priority = priority
                    best_insert_index = insert_index
                    min_item = i
        self.q.pop(min_item)
        return min_item

    def update_priority(self, item, priority):
        self.q[item] = (priority, self.insert_count)
        self.insert_count += 1

    def get_priority(self, item):
        return self.q[item][0]

    def __len__(self):
        """This returns the number of values in the queue."""
        return len(self.q)

    def __contains__(self, item):
        return item in self.q
