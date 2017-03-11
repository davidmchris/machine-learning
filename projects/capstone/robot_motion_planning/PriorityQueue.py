class PriorityQueue:
    def __init__(self):
        self.priorities_index = {}
        self.items_index = {}

    def insert(self, priority, item):
        # type: (int, object) -> None
        if self.items_index.has_key(item):
            raise Exception("Item already in queue. Did you mean to use update_priority?")
        entry = PriorityQueueEntry(priority, item)
        if priority in self.priorities_index:
            self.priorities_index[priority].append(entry)
        else:
            self.priorities_index[priority] = [entry]
        self.items_index[item] = entry

    def pop_min(self):
        min_entry = self.priorities_index.popitem()
        priority = min_entry[0]
        elements = min_entry[1]
        value_to_pop = elements.pop()
        if len(elements) != 0:
            self.priorities_index[priority] = elements
        return value_to_pop.item

    def update_priority(self, item, priority):
        self.items_index[item].priority = priority

    def __len__(self):
        """This returns the number of values in the queue."""
        return len(self.items_index)

    def __contains__(self, item):
        return self.items_index.has_key(item)


class PriorityQueueEntry:
    def __init__(self, priority, item):
        self.priority = priority
        self.item = item
