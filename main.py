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
    return ''.join(result)

def main():
    print(f"Initial board:\n{board_to_string(board)}")

if __name__ == "__main__":
    main()
