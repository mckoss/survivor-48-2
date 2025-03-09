#!/usr/bin/env python3

from sympy.combinatorics import Permutation
import heapq

named_permutations = (
    ('P1', Permutation(1, 5, 4, 3, 2)),
    ('P2', Permutation(6, 10, 9, 8, 7)),
    ('P3', Permutation(11, 15, 14, 13, 12)),
    ('P12', Permutation(1, 10, 9, 8, 7, 6, 5, 4, 3, 2)),
    # Push 2nd row deeper before placing tile in first row
    ('P12+', Permutation(1, 9, 7, 5, 4, 3, 2)(10, 8, 6)),
    ('P12++', Permutation(1, 8, 6, 9, 5, 4, 3, 2)(7, 10)),
    ('P12+++', Permutation(1, 7, 9, 5, 4, 3, 2)(6, 8, 10)),
    ('P12++++', Permutation(1, 6, 7, 8, 9, 10, 5, 4, 3, 2)),
    # ('P13', Permutation(1, 15, 14, 13, 12, 11, 5, 4, 3, 2)),
    ('P23', Permutation(6, 15, 14, 13, 12, 11, 10, 9, 8, 7)),

    ('P123', Permutation(1, 10, 9, 8, 7, 6, 15, 14, 13, 12, 11, 5, 4, 3, 2)),
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
    frontier = [(distance(board), 0, tuple(board.array_form), [])]
    explored = set()
    best_distance = distance(board)
    best_sequence = []

    positions_searched = 0

    while frontier:
        current_distance, depth, current_board_tuple, sequence = heapq.heappop(frontier)
        if depth > max_depth:
            continue
        # BUG: Is this ever possible?
        if current_board_tuple in explored:
            continue

        explored.add(current_board_tuple)
        current_board = Permutation(list(current_board_tuple))

        for name, perm in named_permutations:
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

            heapq.heappush(frontier, (new_distance, depth + 1, tuple(new_board.array_form), new_sequence))

            positions_searched += 1

            if positions_searched % 10000 == 0:
                distances = [item[0] for item in frontier]
                print(f"Progress: {positions_searched:,} positions examined (at depth {depth})")
                print(f"Current distance range of {len(distances):,} boards remaining in frontier: {min(distances)} - {max(distances)}")
                if positions_searched % 100000 == 0:
                    print(f"Current best sequence: {' -> '.join(best_sequence)}")
                    print(f"Current best distance: {best_distance}")

    return best_sequence

def main():
    print(f"Initial board:\n{board_to_string(board)}")
    best_sequence = search(board, 20)
    print(f"Best sequence found: {' -> '.join(best_sequence)}")

if __name__ == "__main__":
    main()
