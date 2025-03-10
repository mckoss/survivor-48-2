#!/usr/bin/env python3

from sympy.combinatorics import Permutation
import heapq

# The zeroth element is the free space for a tile that
# has been knocked off it's row.  The zero moves into the
# empty slot left vacant by shifting the row left.

dumping_row_perms = (
    ('P1-', Permutation(0, 5, 4, 3, 2, 1)),
    ('P2-', Permutation(0, 10, 9, 8, 7, 6)),
    ('P3-', Permutation(0, 15, 14, 13, 12, 11))
)

filling_row_perms = (
    ('P1+', Permutation(0, 5)),
    ('P2+', Permutation(0, 10)),
    ('P3+', Permutation(0, 15))
)

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
    result.append(f"In hand: {a.index(0):2}\n")
    result.append(f"Distance: {distance(board)}")
    return ''.join(result)

def distance(board):
    """Calculate the distance of the board from the goal state.

    Use the sum of the differences of the elements from the home
    position.
    """
    deltas = [abs(i - j) for i, j in zip(board.array_form, range(0, 16))]
    if deltas[0] != 0:
        deltas[0] = 1
    return sum(deltas)

def slide_row_perm(board, row):
    """ Determine which permutation to use if the row is slid to the left.

    Determine if the row has an empty slot in which case to use the
    filling row permutation, otherwise use the dumping row permutation.
    """
    if board.array_form[0] == (row + 1) * 5:
        return filling_row_perms[row]
    else:
        return dumping_row_perms[row]

def search(board, max_depth=3):
    frontier = [(distance(board), 0, tuple(board.array_form), [])]
    explored = set()
    best_distance = distance(board)
    best_sequence = []

    positions_searched = 0

    while frontier:
        current_distance, depth, current_board_tuple, sequence = heapq.heappop(frontier)
        # Shouldn't we not every queue an already queue board?
        if current_board_tuple in explored:
            continue

        explored.add(current_board_tuple)
        current_board = Permutation(list(current_board_tuple))

        for name, perm in (slide_row_perm(current_board, row) for row in range(3)):
            new_board = current_board * perm
            new_sequence = sequence + [name]

            if tuple(new_board.array_form) in explored:
                continue

            new_distance = distance(new_board)
            if new_distance < best_distance:
                best_distance = new_distance
                best_sequence = new_sequence
                print(f"Depth {depth + 1}:\n{board_to_string(new_board)}")
                print(f"Permutation Sequence: {' -> '.join(best_sequence)}")

            if new_distance == 0:
                return new_sequence

            if depth + 1 < max_depth:
                heapq.heappush(frontier, (new_distance, depth + 1, tuple(new_board.array_form), new_sequence))

            positions_searched += 1

            if positions_searched % 10000 == 0:
                print(f"Progress: {positions_searched:,} positions examined (at depth {depth})")
                min_dist = 9999
                max_dist = -1
                for i in range(len(frontier)):
                    if frontier[i][0] < min_dist:
                        min_dist = frontier[i][0]
                    if frontier[i][0] > max_dist:
                        max_dist = frontier[i][0]
                print(f"Current distance range of {len(frontier):,} boards remaining in frontier: {min_dist} - {max_dist}")
                if positions_searched % 100000 == 0:
                    print(f"Current best sequence: {' -> '.join(best_sequence)}")
                    print(f"Current best distance: {best_distance}")
                    print(f"Current board: {board_to_string(current_board)}")
                    print(f"Current sequence: {' -> '.join(sequence)}")

    return best_sequence

def main():
    print(f"Initial board:\n{board_to_string(board)}")
    best_sequence = search(board, 500)
    print(f"Best sequence found: {' -> '.join(best_sequence)}")

if __name__ == "__main__":
    main()
