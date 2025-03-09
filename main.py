#!/usr/bin/env python3

from sympy.combinatorics import Permutation
import heapq

# Single row rotations
p1 = Permutation(1, 5, 4, 3, 2)
p2 = Permutation(6, 10, 9, 8, 7)
p3 = Permutation(11, 15, 14, 13, 12)

# Push tile from one row to another
p12 = Permutation(1, 10, 9, 8, 7, 6, 5, 4, 3, 2)
p13 = Permutation(1, 15, 14, 13, 12, 11, 5, 4, 3, 2)
p23 = Permutation(6, 15, 14, 13, 12, 11, 10, 9, 8, 7)

named_permutations = [
    ('p1', p1),
    ('p2', p2),
    ('p3', p3),
    ('p12', p12),
    ('p13', p13),
    ('p23', p23)
]

# Cycle notation for the starting position
board = Permutation([[1, 2], [3, 4], [5], [6, 7], [8, 9], [10], [11, 12], [13, 14], [15]])

def board_to_string(board):
    a = board.array_form
    # Pad the array to ensure it has at least 16 elements
    a += [i for i in range(len(a), 16)]
    result = []
    for i in range(1, 16):
        sep = '\n' if i % 5 == 0 else ' '
        result.append(f"{a.index(i):2}{sep}")
    result.append(f"Distance: {distance(board)}")
    return ''.join(result)

def distance(board):
    """Calculate the distance of the board from the goal state.

    Use the sum of the differences of the elements from the home
    position.
    """
    deltas = [abs(i - j) for i, j in zip(board.array_form[1:-1], range(1, 16))]
    return sum(deltas)

def search(board, max_depth=3):
    frontier = [(distance(board), 0, tuple(board.array_form))]
    explored = set()
    best_distance = distance(board)
    positions_searched = 0

    while frontier:
        current_distance, depth, current_board_tuple = heapq.heappop(frontier)
        if depth > max_depth:
            continue
        if current_board_tuple in explored:
            continue
        explored.add(current_board_tuple)
        current_board = Permutation(list(current_board_tuple))

        for name, perm in named_permutations:
            new_board = current_board * perm

            if tuple(new_board.array_form) in explored:
                continue

            new_distance = distance(new_board)
            if new_distance < best_distance:
                best_distance = new_distance
                print(f"Depth {depth + 1} - Board after applying {name}:\n{board_to_string(new_board)}")

            heapq.heappush(frontier, (new_distance, depth + 1, tuple(new_board.array_form)))

            positions_searched += 1

            if positions_searched % 10000 == 0:
                distances = [item[0] for item in frontier]
                print(f"Progress: {positions_searched:,} positions examined")
                print(f"Current distance range of {len(distances):,} boards remain in frontier: {min(distances)} - {max(distances)}")


def main():
    print(f"Initial board:\n{board_to_string(board)}")
    search(board, 10)

if __name__ == "__main__":
    main()
