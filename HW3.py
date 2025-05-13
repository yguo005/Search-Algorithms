from __future__ import annotations  # for type hints in recursive node structure
from Levenshtein import distance
import heapq  # min heap

# Get start and end words from user
start_word = input('Please enter the start word: ').strip()  # remove newline character
SIZE = len(start_word)
end_word = input('Please enter the end word (same length as start word): ').strip()
while len(end_word) != SIZE:
    end_word = input(f'Please enter an end word of length {SIZE}: ').strip()

# Get a dictionary, maybe https://github.com/dwyl/english-words/blob/master/words_alpha.txt
dictionary = [word.strip() for word in open('/Users/mac/Desktop/5100/HW3/words_alpha.txt', 'r').readlines()]

# Limit dictionary to words of certain size
dictionary_small = [word for word in dictionary if len(word) == SIZE]

# Graph adjacency list
# dictionary: keys: strings (words), values: sets of strings (sets of words one character away)
single_char_apart: dict[str, set[str]] = {}

# enumerate: gives both the index (idx) and the word (word1)
for idx, word1 in enumerate(dictionary_small):
    # For each word1, it initializes an empty set in single_char_apart to store word
    single_char_apart[word1] = set()
    for word2 in dictionary_small[:idx]:  # before the current word1
        # If the distance is less than or equal to 1
        if distance(word1, word2, score_cutoff=1) <= 1:
            single_char_apart[word1].add(word2)
            single_char_apart[word2].add(word1)
print(f"Graph adjacency list created with {len(single_char_apart)} entries.")

# create a node in a path of words. Each node stores a word and a reference to its parent node in the path.
class WordPathNode:
    def __init__(self, word: str, parent: WordPathNode = None):
        self.word = word
        self.parent = parent

    # Two WordPathNodes are equal if they both have the same word
    def __eq__(self, other: WordPathNode) -> bool:
        return self.word == other.word

    # The hashcode is the hashcode of the word
    # Hashing is a process of converting an object into a unique integer representation
    def __hash__(self) -> int:
        return self.word.__hash__()

    # Returns the path from the current node to the root.
    # as a list of str
    def get_path_to_root(self) -> list[str]:
        current = self
        list_of_words = []
        while current is not None:
            list_of_words.append(current.word)
            current = current.parent
        return list_of_words[::-1] # reverse the list to get the path from root to current node
    
     # define how WordPathNodes should be compared for less-than
    def __lt__(self, other):
      # Compare nodes based on their node_cost
      return node_cost(self) < node_cost(other)  
    

def find_edit_path_bfs(start_word: str, end_word: str) -> list[str]:
    # Initialize the frontier queue and visited set
    frontier = [WordPathNode(start_word)]
    visited = {start_word}

    while len(frontier) > 0:  # check if frontier queue is not empty
        current_node = frontier.pop(0)
        current_word = current_node.word

        # Check if we reached the end word
        if current_word == end_word:
            return current_node.get_path_to_root()

        # Explore neighbors
        for neighbor in single_char_apart.get(current_word, []):  # If current_word is not found in the single_char_apart dictionary, returns default value an empty list
            if neighbor not in visited:
                visited.add(neighbor)
                # Add the neighbor to the frontier with the current node as parent
                frontier.append(WordPathNode(neighbor, current_node))

    return []

def find_edit_path_dfs(start_word: str, end_word: str) -> list[str]:
    # Initialize the stack and visited set
    stack = [WordPathNode(start_word)]
    visited = {start_word}

    while len(stack) > 0:
        current_node = stack.pop()  # Pop the last node
        current_word = current_node.word

        # Check if we reached the end word
        if current_word == end_word:
            return current_node.get_path_to_root()

        # Explore neighbors
        for neighbor in single_char_apart.get(current_word, []):
            if neighbor not in visited:
                visited.add(neighbor)
                # Add the neighbor to the stack with the current node as parent
                stack.append(WordPathNode(neighbor, current_node))
    return []

def find_edit_path_iterative_deepening(start_word: str, end_word: str) -> list[str]:
    depth = 0
    found_path = False

    while not found_path:  # not found_path evaluates to True, allowing the loop to execute
        visited = set()
        stack = [WordPathNode(start_word)]

        while len(stack) > 0:
            current_node = stack.pop()
            current_word = current_node.word

            if current_word == end_word:
                found_path = True
                return current_node.get_path_to_root()

            # get_path_to_root() return the nodes from current node back to root, the depth is the edges from root to that node
            if len(current_node.get_path_to_root()) - 1 < depth:
                visited.add(current_word)

                for neighbor in single_char_apart.get(current_word, []):
                    if neighbor not in visited:
                        neighbor_node = WordPathNode(neighbor, current_node)
                        stack.append(neighbor_node)
        depth += 1
    return []

def heuristic(word1: str, word2: str) -> int:
    difference_count = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            difference_count += 1
    return difference_count

def node_cost(node):
    # Calculates the total cost of a node (existing cost from start node to current node + heuristic cost: the estimated cost from current node to end node)
    return len(node.get_path_to_root()) - 1 + heuristic(node.word, end_word) 

def find_edit_path_a_star_search(start_word: str, end_word: str) -> list[str]:
    # the nodes in the priority_queue are prioritized based on their total cost, which is the sum of the actual cost to reach the node and the estimated cost to reach the goal from that node (the heuristic).
    priority_queue = []
    start_node = WordPathNode(start_word)
    # push a new item tuple onto the priority_queue list
    # (0, WordPathNode(start_word): 0: the initial total cost of the starting node
    # WordPathNode(start_word): create a new instance initializing with start_word, is the current state in the search
    heapq.heappush(priority_queue, (node_cost(start_node), WordPathNode(start_word)))  # (cost, node)
    
    visited = set()

    while len(priority_queue) > 0:
        # Get the node with the lowest total_cost (actual_cost + heuristic)
        # since priority_queue contains tuple (how data push onto the heap)
        current_cost, current_node = heapq.heappop(priority_queue)
        current_word = current_node.word

        if current_word == end_word:
            return current_node.get_path_to_root()
        
        if current_word in visited:
            continue

        visited.add(current_word)

        for neighbor in single_char_apart.get(current_word, []):
            if neighbor not in visited:
                new_node = WordPathNode(neighbor, current_node)
                heapq.heappush(priority_queue, (node_cost(new_node), WordPathNode(neighbor, current_node)))
            

    return []

bfs_result = find_edit_path_bfs(start_word, end_word)
print(f"\nBFS Path from {start_word} to {end_word}: {bfs_result}")

dfs_result = find_edit_path_dfs(start_word, end_word)
print(f"\nDFS Path from {start_word} to {end_word}: {dfs_result}")

iterative_deepening_result = find_edit_path_iterative_deepening(start_word, end_word)
print(f"\nIterative Deepening Path from {start_word} to {end_word}: {iterative_deepening_result}")

a_star_result = find_edit_path_a_star_search(start_word, end_word)
print(f"\nA* Path from {start_word} to {end_word}: {a_star_result}")