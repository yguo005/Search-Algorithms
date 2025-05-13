
## Assignment Overview

This assignment focuses on implementing and comparing different search algorithms to solve the "word ladder" puzzle. The goal is to find a sequence of words, starting from a given `start_word` and ending with an `end_word`, where each consecutive word in the sequence differs by only one character, and all words are valid English words of the same length.

Four search algorithms were implemented and analyzed:
1.  Breadth-First Search (BFS)
2.  Depth-First Search (DFS)
3.  Iterative Deepening Search (IDS)
4.  A* Search

## Algorithm Analysis

### 1. Breadth-First Search (BFS)

*   **Shortest Path Guarantee:** No, not in all cases. BFS guarantees the shortest path in *unweighted graphs* or graphs where all edge weights are equal.
*   **In this problem:** Yes, BFS will find the shortest path.
    *   The graph is effectively unweighted: each edge (a single character change between words) has an implicit weight of 1.
    *   The graph is undirected: changing a character in a word is a reversible operation.
*   **Example Output (cats to quiz):** `['cats', 'tats', 'tuts', 'tuis', 'quis', 'quiz']` (Length 6)

### 2. Depth-First Search (DFS)

*   **Shortest Path Guarantee:** No. DFS explores as far as possible along each branch before backtracking. It might find a longer path first depending on the exploration order.
*   **Example Output (cats to quiz):** (A very long path is shown in the document, demonstrating its non-optimality)

### 3. Iterative Deepening Search (IDS)

*   **Shortest Path Guarantee:** Yes. IDS combines DFS and BFS strategies. It performs a series of depth-limited searches, incrementing the depth limit with each iteration (depth 0, then depth 1, then depth 2, etc.). The first time it reaches the end word, it will be through the shortest possible path.
*   **Example Output (cats to quiz):** `['cats', 'caws', 'laws', 'lags', 'lugs', 'luis', 'quis', 'quiz']` (Length 8 - Note: The document example shows a different path than BFS/A*, which might imply a different dictionary or graph construction for that specific run, or an error in the transcription. Typically IDS should also find a path of length 6 if one exists and is found by BFS).

### 4. A* Search

*   **Shortest Path Guarantee:** Yes, if the heuristic used is admissible (never overestimates the cost to the goal) and consistent (optional, but good for efficiency).
*   **Heuristic Used:** Hamming distance between two words (number of positions where characters differ).
    *   **Admissibility:** Yes, Hamming distance is admissible because each differing character requires at least one change.
    *   **Consistency:** Yes, the estimated cost from any word to the goal is no greater than the cost of changing one letter plus the estimated cost from the resulting word.
*   **Mechanism:** Nodes are ordered in a priority queue by `total_cost = actual_cost (g(n)) + heuristic_cost (h(n))`.
*   **Example Output (cats to quiz):** `['cats', 'cuts', 'tuts', 'tuis', 'quis', 'quiz']` (Length 6)

## Efficiency Analysis

The efficiency of these algorithms was considered for words that are fairly similar (>50% characters in common) and words that are not similar (<50% characters in common), as well as for determining if no path exists.

**Key:**
*   `b`: branching factor
*   `d`: depth of the solution (shortest path length)
*   `m`: maximum path length

### For Fairly Similar Words (>50% characters in common - `d` is small):

*   **DFS:**
    *   Time: O(b^m)
    *   Space: O(bm)
    *   Efficiency: May not be efficient; can explore deep, irrelevant paths.
*   **BFS:**
    *   Time: O(b^(d+1))
    *   Space: O(b^(d+1))
    *   Efficiency: Excels at finding short paths quickly. Likely more efficient than IDS as it doesn't repeat work.
*   **IDS:**
    *   Time: O(b^d)
    *   Space: O(bd)
    *   Efficiency: Better than DFS, but still explores unnecessary paths in early (shallow depth) iterations.
*   **A* Search:**
    *   Time: O(b^d) in worst case, often better in practice.
    *   Space: O(b^d) in worst case.
    *   Efficiency: **Most efficient**. The heuristic (Hamming distance) directly relates to word similarity, prioritizing exploration of more similar words and reducing unnecessary searches.

**Time Efficiency Comparison (Similar Words):** `A* > BFS > IDS > DFS`

### For Not Similar Words (<50% characters in common - `d` is large):

*   **BFS:** Guaranteed to find the shortest path but may explore many irrelevant paths first. High memory usage.
*   **DFS:** May get stuck in deep, irrelevant paths. Space-efficient but time-inefficient.
*   **IDS:** More space-efficient than BFS. Can be more time-efficient than BFS for longer paths as it doesn't store all nodes at each level.
*   **A* Search:** Potentially most efficient if the heuristic guides the search effectively. For very dissimilar words, the heuristic might provide less benefit.

**Time Efficiency Comparison (Dissimilar Words):** `A* > IDS > BFS > DFS` (A*'s advantage depends heavily on heuristic quality for large `d`)

### For Determining No Path Exists:

*   **BFS:** Explores all possibilities in order of edit distance. Guarantees exhausting all possibilities in the shortest number of steps before concluding no path exists.
*   **DFS:** Explores all possibilities but may get stuck in deep, irrelevant paths before concluding no path exists.
*   **IDS:** Eventually explores all possibilities with some repeated work. More space-efficient than BFS. Good balance of completeness and space efficiency.
*   **A* Search:** Potentially as efficient as BFS. Can be more efficient if the heuristic quickly identifies dead-ends.

## Heuristic Choice for A* Search

*   **Heuristic:** Hamming Distance (counts positions where characters differ between two equal-length words).
*   **Why appropriate:**
    *   **Admissible:** It never overestimates the true cost (minimum number of single-character changes) to reach the goal word. Each differing character requires at least one change.
    *   **Consistent:** The cost from any word `n` to the goal `g` (h(n)) is no greater than the cost of changing one letter to reach a neighbor `n'` (cost(n, n')) plus the heuristic cost from `n'` to `g` (h(n')). `h(n) <= cost(n, n') + h(n')`.

## Extension: Path Including a Set of Required Words

**Problem:** Find the shortest path from `start_word` to `end_word` that *must* include every word in a given set of `required_words` (order doesn't matter).

**Proposed Solution (using A*):**

1.  **State Representation:** The state in the A* search needs to include not just the `current_word` but also the `set_of_remaining_required_words`. A tuple like `(current_word, frozenset(remaining_required_words))` can be used for visited states to handle immutability.
2.  **Modified Heuristic:**
    ```python
    def heuristic(current_word: str, end_word: str, remaining_required: set[str]) -> int:
        # Heuristic component 1: Distance to the end word
        h_to_end = hamming_distance(current_word, end_word)

        # Heuristic component 2: Number of remaining required words
        # Each required word will need at least one step to "visit" it if not the current word.
        # A more sophisticated heuristic might consider distances to the nearest required word.
        h_remaining_count = len(remaining_required)

        # Heuristic component 3 (optional, more complex):
        # If remaining_required is not empty, we still need to reach one of them.
        # Add the minimum Hamming distance from current_word to any word in remaining_required.
        # And then, from that chosen required word, the distance to the end_word (or next required word).
        # For simplicity, we can use a simpler form for now.
        # A basic version:
        h_to_closest_required = 0
        if remaining_required:
             h_to_closest_required = min(hamming_distance(current_word, req_word) for req_word in remaining_required)
             # This part is tricky because visiting a required word might not be on the shortest path to the *next* required or end word.
             # A simpler, admissible heuristic for the "visit all" part is just the count.

        # Combine:
        # The core idea is that we need to visit all remaining_required words
        # and then get to the end_word.
        # A simple admissible heuristic:
        return h_to_end + len(remaining_required)
    ```
    *A more accurate heuristic would involve solving a form of the Traveling Salesperson Problem (TSP) on the required words, which is complex. The `hamming_distance(current_word, end_word) + len(remaining_required)` is a simpler, admissible heuristic: you still need to reach the end and "pass through" or transform into each remaining required word (at least one step per remaining required word).*

3.  **Goal State:** The goal is reached when `current_word == end_word` AND `len(remaining_required) == 0`.
4.  **Transitions:** When moving from `current_word` to `neighbor_word`:
    *   Update `actual_cost` (g(n)) as usual.
    *   If `neighbor_word` is in `remaining_required`, create the new state with `neighbor_word` removed from the `remaining_required` set for the child node.
5.  **Initialization:** Start the search with `(start_word, initial_set_of_all_required_words)`. If `start_word` is in `required_words`, remove it from the initial set.

## Development Details

*   **Time Taken:** 2 days
*   **Collaboration:** Discussed the `NodePathWord` class properties, usage in a priority queue, and the `get_path_to_root()` method with another student.
*   **Resources Used:**
    *   Dictionary: [dwyl/english-words](https://github.com/dwyl/english-words/blob/master/words_alpha.txt)
    *   Heuristics (Amit Patel's Game Programming Pages): [Stanford Theory - Heuristics](https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#S7)

## Challenges and Learnings

*   **Most Difficult Part:**
    *   Defining the heuristic cost function for A*.
    *   Resolving a `TypeError` in A* when comparing custom `WordPathNode` objects in the `heapq` priority queue. This occurs because Python doesn't know how to compare custom objects by default.
    *   **Fix:** Implemented the `__lt__` (less than) special method in the `WordPathNode` class, comparing nodes based on their total cost (`f_cost = g_cost + h_cost`). Alternatively, push tuples `(cost, node)` onto the heap.
        ```python
        # In WordPathNode class:
        def __lt__(self, other):
            return self.node_cost() < other.node_cost() # Assuming node_cost() calculates f_cost

        # Or when pushing to heapq:
        # heapq.heappush(priority_queue, (calculate_total_cost(node), node))
        ```
        The document describes defining a `node_cost` method and using it in the `__lt__` method or directly when pushing to the heap:
        ```python
        def node_cost(node): # Calculates f-cost
            return len(node.get_path_to_root()) - 1 + heuristic(node.word, end_word)
        ```

*   **Most Rewarding Part:**
    *   Comparing the efficiency of BFS, DFS, IDS, and A* in a practical character comparison (word ladder) scenario.
    *   Gaining a better understanding of heuristic selection.

*   **What was Learned:**
    *   The differences between these search algorithms.
    *   How to use different data structures for each search (e.g., queue for BFS/A*, stack for DFS/IDS).

