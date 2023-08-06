"""Boggler Demo"""
import sys
from pathlib import Path
from boggler_utils import BoggleBoard, build_full_boggle_tree, read_boggle_file

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print('Usage: python3 boggler.py <BOARD_FILE> <WORDLISTS_DIR> [MAX_WORD_LENGTH]')
        sys.exit(1)

    board = read_boggle_file(Path(sys.argv[1]))
    if len(sys.argv) == 3:
        boggle_board = BoggleBoard(board)
    elif len(sys.argv) == 4:
        try:
            boggle_board = BoggleBoard(board, int(sys.argv[3]))
        except ValueError:
            print("Invalid MAX_WORD_LENGTH. Please try again with a valid integer.")
            sys.exit(1)
    try:
        boggle_tree = build_full_boggle_tree(boggle_board, Path(sys.argv[2]))

        print("\nBOARD")
        print(boggle_board)

        for start_pos, tree in boggle_tree.items():
            print(f"\nStarting @ {start_pos}...")
            for word in tree.word_paths:
                print(f"{word[0]: <{boggle_board.max_word_len}}: {word[1]}")

    except ValueError as e:
        print("The [MAX_WORD_LENGTH] argument must be an integer.")
        print("Please try again.")
        sys.exit(1)
