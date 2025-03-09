#!/usr/bin/env python3

from sympy.combinatorics import Permutation

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

def search(board, depth=1, max_depth=3, best_distance=None):
    if best_distance is None:
        best_distance = distance(board)
    if depth > max_depth:
        return best_distance
    for name, perm in named_permutations:
        new_board = board * perm
        current_distance = distance(new_board)
        if current_distance < best_distance:
            best_distance = current_distance
        print(f"Depth {depth} - Board after applying {name}:\n{board_to_string(new_board)}")
        best_distance = search(new_board, depth + 1, max_depth, best_distance)
    return best_distance

def main():
    print(f"Initial board:\n{board_to_string(board)}")
    search(board, 1, 5)

if __name__ == "__main__":
    main()
