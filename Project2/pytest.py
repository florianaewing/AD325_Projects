import csv
import time


class HashTable:
    def __init__(self, size, collision_avoidance="Separate Chaining"):
        self.size = size
        self.table = [None] * size
        self.collision_avoidance = collision_avoidance
        self.item_count = (
            0  # Track the number of items for load factor management
        )
        self.collisions = 0  # Track the number of collisions

    def hash(self, key):
        return hash(key) % self.size

    def second_hash(self, key):
        return 1 + (hash(key) % (self.size - 1))

    def insert(self, key, value):
        index = self.hash(key)

        if self.collision_avoidance == "Separate Chaining":
            if self.table[index] is None:
                self.table[index] = []
            # Check if key exists, and append the item if it's a new item
            for pair in self.table[index]:
                if pair[0] == key:
                    if value not in pair[1]:  # Avoid duplicate items
                        pair[1].append(value)
                    return
            self.table[index].append([key, [value]])
        elif self.collision_avoidance == "Quadratic Probing":
            step = 1
            original_index = index
            while self.table[index] is not None:
                self.collisions += 1  # Count collision
                if self.table[index][0] == key:
                    if value not in self.table[index][1]:
                        self.table[index][1].append(value)
                    return
                index = (original_index + step**2) % self.size
                step += 1
            self.table[index] = [key, [value]]

        self.item_count += 1

    def retrieve(self, key):
        index = self.hash(key)
        retrieval_start_time = time.time()  # Start timing retrieval

        if self.collision_avoidance == "Separate Chaining":
            if self.table[index] is not None:
                for pair in self.table[index]:
                    if pair[0] == key:
                        retrieval_time = time.time() - retrieval_start_time
                        return (
                            pair[1],
                            retrieval_time,
                        )  # Return items and retrieval time
        elif self.collision_avoidance == "Quadratic Probing":
            step = 1
            original_index = index
            while self.table[index] is not None:
                if self.table[index][0] == key:
                    retrieval_time = time.time() - retrieval_start_time
                    return (
                        self.table[index][1],
                        retrieval_time,
                    )  # Return items and retrieval time
                index = (original_index + step**2) % self.size
                step += 1

        return None, time.time() - retrieval_start_time  # Key not found

    def load_data_from_csv(self, filename):
        insertion_start_time = time.time()  # Start timing insertion
        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                user_id, item_id = row
                self.insert(user_id, item_id)
        return (
            time.time() - insertion_start_time
        )  # Return total insertion time


# Create an instance of the hash table and load data from CSV
hash_table = HashTable(size=100, collision_avoidance="Separate Chaining")
hash_table.load_data_from_csv("user_item_data.csv")

# Example retrieval
print(hash_table.retrieve("user6"))
print()


class MaxHeap:
    def __init__(self):
        self.heap = []  # Each element is a tuple (priority, item)

    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    def has_left(self, index):
        return self.left_child(index) < len(self.heap)

    def has_right(self, index):
        return self.right_child(index) < len(self.heap)

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def percolate_up(self, index):
        while index > 0:
            parent_index = self.parent(index)
            if (
                self.heap[index][0] > self.heap[parent_index][0]
            ):  # Compare priorities
                self.swap(index, parent_index)
                index = parent_index
            else:
                break

    def percolate_down(self, index):
        while self.has_left(index):
            largest_child_index = self.left_child(index)
            if self.has_right(index):
                right_index = self.right_child(index)
                if (
                    self.heap[right_index][0]
                    > self.heap[largest_child_index][0]
                ):
                    largest_child_index = right_index

            if self.heap[index][0] < self.heap[largest_child_index][0]:
                self.swap(index, largest_child_index)
                index = largest_child_index
            else:
                break

    def push(self, priority, item):
        self.heap.append((priority, item))
        self.percolate_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()  # Move the last item to the root
        self.percolate_down(0)
        return root

    def top_n(self, n):
        return sorted(self.heap, key=lambda x: x[0], reverse=True)[:n]


# Example usage:
max_heap = MaxHeap()
max_heap.push(5, "Item A")
max_heap.push(3, "Item B")
max_heap.push(10, "Item C")
max_heap.push(1, "Item D")

print(max_heap.pop())  # Should return (10, "Item C")
print(max_heap.top_n(2))  # Should return the top 2 items by priority
print()


class RecommendationSystem:
    def __init__(self, user_item_file):
        self.user_item_file = user_item_file
        self.hash_table = (
            None  # Will be initialized in `build_recommendation_system`
        )

    def load_data(self):
        if self.hash_table:
            self.hash_table.load_data_from_csv(self.user_item_file)
        else:
            raise ValueError(
                "Hash table has not been initialized. Call build_recommendation_system first."
            )

    def build_recommendation_system(self, technique="Separate Chaining"):
        self.hash_table = HashTable(size=100, collision_avoidance=technique)
        self.load_data()

    def jaccard_similarity(self, set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0

    def recommend_items_with_jaccard(
        self, target_user, technique="Separate Chaining", top_n=5
    ):
        if not self.hash_table:
            self.build_recommendation_system(technique)

        # Retrieve items for the target user
        target_items, _ = self.hash_table.retrieve(
            target_user
        )  # Unpack the tuple
        if not target_items:
            print(f"No data available for user {target_user}")
            return []

        target_set = set(target_items)  # Create a set of target items
        max_heap = MaxHeap()

        # Iterate over all users in the hash table
        for index in range(self.hash_table.size):
            bucket = self.hash_table.table[index]
            if bucket is not None:
                for user_items_pair in bucket:
                    user, items = user_items_pair
                    if user != target_user:
                        similarity = self.jaccard_similarity(
                            target_set, set(items)
                        )
                        if similarity > 0:
                            max_heap.push(similarity, user)

        # Collect the top n similar users
        similar_users = max_heap.top_n(top_n)

        # Compile recommended items from top similar users
        recommended_items = set()
        for _, similar_user in similar_users:
            similar_user_items, _ = self.hash_table.retrieve(
                similar_user
            )  # Unpack the tuple again
            if similar_user_items:
                recommended_items.update(similar_user_items)

        # Filter out items the target user has already interacted with
        recommended_items.difference_update(target_set)

        return list(recommended_items)[:top_n]


# Example usage:
recommendation_system = RecommendationSystem("user_item_data.csv")
recommendation_system.build_recommendation_system(
    technique="Separate Chaining"
)
recommendations = recommendation_system.recommend_items_with_jaccard(
    "user6", technique="Separate Chaining", top_n=5
)
print("Recommended items for user6:", recommendations)
print()


class Main:
    def __init__(self):
        self.run_tests()

    def run_tests(self):
        self.test_hash_table()
        self.test_max_heap()
        self.test_recommendation_system()
        self.print_reports()  # Call the method to print reports

    def test_hash_table(self):
        print("Testing HashTable...")
        print()

        # Test Separate Chaining
        hash_table = HashTable(
            size=10, collision_avoidance="Separate Chaining"
        )
        insertion_time = hash_table.load_data_from_csv(
            "user_item_data.csv"
        )  # Load data and time it
        hash_table.insert("user1", "Item A")
        hash_table.insert("user1", "Item B")
        hash_table.insert("user2", "Item C")
        hash_table.insert("user3", "Item D")

        # Retrieve data and print results
        user1_items, retrieval_time = hash_table.retrieve(
            "user1"
        )  # Timing retrieval
        print(
            "Retrieve user1 items:", user1_items
        )  # Expected: ['Item A', 'Item B']
        print()
        print(
            "Retrieve user2 items:", hash_table.retrieve("user2")[0]
        )  # Expected: ['Item C']
        print()
        print(
            "Retrieve user3 items:", hash_table.retrieve("user3")[0]
        )  # Expected: ['Item D']
        print()
        print(
            "Retrieve non-existent user:", hash_table.retrieve("user99")[0]
        )  # Expected: None

        # Print number of collisions for separate chaining
        print("Collisions (Separate Chaining):", hash_table.collisions)

        # Test Quadratic Probing
        hash_table_quad = HashTable(
            size=10, collision_avoidance="Quadratic Probing"
        )
        hash_table_quad.insert("user4", "Item E")
        hash_table_quad.insert("user4", "Item F")
        user4_items, retrieval_time_quad = hash_table_quad.retrieve(
            "user4"
        )  # Timing retrieval
        print(
            "Retrieve user4 items (Quadratic Probing):", user4_items
        )  # Expected: ['Item E', 'Item F']
        print("Collisions (Quadratic Probing):", hash_table_quad.collisions)

        print("HashTable tests completed.\n")

    def test_max_heap(self):
        print("Testing MaxHeap...")

        max_heap = MaxHeap()
        max_heap.push(10, "Item A")
        max_heap.push(20, "Item B")
        max_heap.push(5, "Item C")
        max_heap.push(15, "Item D")

        # Test pop and top_n
        print("Max item popped:", max_heap.pop())  # Expected: (20, "Item B")
        print(
            "Top 2 items:", max_heap.top_n(2)
        )  # Expected: [('Item A', 10), ('Item D', 15)]

        print("MaxHeap tests completed.\n")

    def test_recommendation_system(self):
        print("Testing RecommendationSystem...")

        # Initialize the recommendation system
        recommendation_system = RecommendationSystem("user_item_data.csv")
        recommendation_system.build_recommendation_system(
            technique="Separate Chaining"
        )

        # Test recommendations for valid users
        for user in [
            "user1",
            "user2",
            "user3",
            "user4",
            "user5",
            "user6",
            "user7",
        ]:
            recommendations = (
                recommendation_system.recommend_items_with_jaccard(
                    user, top_n=3
                )
            )
            print(f"Recommendations for {user}:", recommendations)

        # Test with a user that doesn't exist
        recommendations_empty = (
            recommendation_system.recommend_items_with_jaccard(
                "user99", top_n=3
            )
        )
        print(
            "Recommendations for non-existent user99:", recommendations_empty
        )

        print("RecommendationSystem tests completed.\n")

    def print_reports(self):
        users = [
            f"user{i}" for i in range(1, 8)
        ]  # List of users from user1 to user7

        # Create the report for separate chaining
        hash_table_separate_chaining = HashTable(
            size=10, collision_avoidance="Separate Chaining"
        )
        insertion_time_separate = (
            hash_table_separate_chaining.load_data_from_csv(
                "user_item_data.csv"
            )
        )

        print("\n" + "=" * 50)  # Header line
        print("Using collision avoidance technique: Separate Chaining")
        print("-" * 50)  # Separator line

        for user in users:
            recommendations = hash_table_separate_chaining.retrieve(user)[
                0
            ]  # Get items for the user
            print(f"Recommendations for {user}:")
            print(
                "  • " + "\n  • ".join(recommendations)
            )  # Format list nicely
            retrieval_time = hash_table_separate_chaining.retrieve(user)[
                1
            ]  # Time for retrieval
            print(
                f"Insertion Time: {insertion_time_separate:.10f} seconds"
            )  # Assuming you want 10 decimal places
            print(
                f"Retrieval Time: {retrieval_time:.10f} seconds"
            )  # Time for retrieval
            print(f"Collisions: {hash_table_separate_chaining.collisions}")
            print("=" * 50)  # End section line for each user

        # Create the report for quadratic probing
        hash_table_quadratic_probing = HashTable(
            size=10, collision_avoidance="Quadratic Probing"
        )
        insertion_time_quad = hash_table_quadratic_probing.load_data_from_csv(
            "user_item_data.csv"
        )

        print("\n" + "=" * 50)  # Header line
        print("Using collision avoidance technique: Quadratic Probing")
        print("-" * 50)  # Separator line

        for user in users:
            recommendations_quad = hash_table_quadratic_probing.retrieve(user)[
                0
            ]  # Get items for the user
            print(f"Recommendations for {user}:")
            print(
                "  • " + "\n  • ".join(recommendations_quad)
            )  # Format list nicely
            retrieval_time_quad = hash_table_quadratic_probing.retrieve(user)[
                1
            ]  # Time for retrieval
            print(
                f"Insertion Time: {insertion_time_quad:.10f} seconds"
            )  # Assuming you want 10 decimal places
            print(
                f"Retrieval Time: {retrieval_time_quad:.10f} seconds"
            )  # Time for retrieval
            print(f"Collisions: {hash_table_quadratic_probing.collisions}")
            print("=" * 50)  # End section line for each user


# Run the main test suite
if __name__ == "__main__":
    Main()
