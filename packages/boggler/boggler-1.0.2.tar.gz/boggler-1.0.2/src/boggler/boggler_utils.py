'''Boggler Utils'''
from __future__ import annotations
from os import path
from multiprocessing import Pool

class BoardCell:
    '''Boggle Board cell'''
    def __init__(self, row: int, col: int, letters: str,
        adjacent_cells: list[BoardCell] = None) -> BoardCell:
        self.__row: int = row
        self.__col: int = col
        self.__pos: (int, int) = (self.__row, self.__col)
        self.__letters: str = letters
        self.__adjacent_cells: list[BoardCell] = adjacent_cells

    @property
    def row(self) -> int:
        '''Getter for row property'''
        return self.__row

    @property
    def col(self) -> int:
        '''Getter for col property'''
        return self.__col

    @property
    def pos(self) -> (int, int):
        '''Getter for pos property'''
        return self.__pos

    @property
    def letters(self) -> str:
        '''Getter for letter property'''
        return self.__letters

    @property
    def adjacent_cells(self) -> list[BoardCell]:
        '''Getter for adjacent_cells property'''
        return self.__adjacent_cells

    @adjacent_cells.setter
    def adjacent_cells(self, value):
        self.__adjacent_cells = value

    def __str__(self):
        return f"({self.__row}, {self.__col}): {self.__letters}"

    def __repr__(self):
        return f"(BoardCell({self.__row}, {self.__col}): {self.__letters}"

class BoggleBoard:
    '''Boggle board structure'''
    def __init__(self, board: list[list[str]], max_word_len: int = 14) -> BoggleBoard:
        self.__height: int = len(board)
        self.__width: int = len(board[0]) if self.__height > 0 else 0
        self.__board_list = board
        self.__board: dict[(int, int), BoardCell] = {}

        # Max word length is limited by size of the board
        self.__max_word_len = min(max_word_len, self.__width * self.__height)

        # Generate BoardCell for each position on the board
        for row in range(0, self.__height):
            for col in range(0, self.__width):
                self.__board[(row, col)] = BoardCell(row, col, board[row][col])

        # Update adjacent cell references for each BoardCell
        for cell in self.__board.values():
            adjacent_indexes = self.__get_adjacent_indexes(cell.row, cell.col)
            cell.adjacent_cells = [self.__board[(x[0], x[1])] for x in adjacent_indexes]

    def __str__(self):
        flattened_board_list = [y for x in self.__board_list for y in x]
        max_len = len(max(flattened_board_list, key=len))
        max_len = max_len + 1 if max_len % 2 == 0 else max_len + 2 # keep header_len odd
        header_len = self.__width * (max_len + 1) - 1
        head = "-" * header_len
        header = f"+{head}+\n"
        body = ""
        for row in self.__board_list:
            body += "|"
            for col in row:
                body += f"{col.upper(): ^{max_len}}|"
            body += "\n"
            body += header
        return f"{header}{body}"

    @property
    def height(self) -> int:
        '''Getter for height property'''
        return self.__height

    @property
    def width(self) -> int:
        '''Getter for width property'''
        return self.__width

    @property
    def max_word_len(self) -> int:
        '''Getter for maximum word length property'''
        return self.__max_word_len

    @property
    def board(self) -> dict[(int, int), BoardCell]:
        '''Getter for board property'''
        return self.__board

    def __get_adjacent_indexes(self, row, col):
        '''Return adjecency list for board of size `row x col`'''
        indexes = []
        if row > 0:
            indexes.append((row-1, col)) # up
            if col > 0:
                indexes.append((row-1, col-1)) # up-left
            if col < self.width - 1:
                indexes.append((row-1, col+1)) # up-right
        if row < self.height - 1:
            indexes.append((row+1, col)) # down
            if col > 0:
                indexes.append((row+1, col-1)) # down-left
            if col < self.width - 1:
                indexes.append((row+1, col+1)) # down-right
        if col > 0:
            indexes.append((row, col-1)) # left
        if col < self.width - 1:
            indexes.append((row, col+1)) # right
        return indexes

    def get_cell(self, row: int, col: int) -> str:
        '''Return the value at the specified row x column'''
        return self.__board[(row, col)]

class WordNode:
    '''A node describing a single letter in a WordTree.'''
    def __init__(self, letters: str, is_word: bool = False, parent: WordNode = None,
        children: dict[str, WordNode] = None, board_pos = None) -> WordNode:
        self.__letters = letters
        self.__is_word = is_word
        self.__children = children if children is not None else {}
        self.__parent = parent
        self.__board_pos = board_pos

    @property
    def letters(self) -> str:
        '''Getter for letter property'''
        return self.__letters

    @property
    def is_word(self) -> bool:
        '''Getter for is_word property'''
        return self.__is_word

    @is_word.setter
    def is_word(self, value):
        self.__is_word = value

    @property
    def children(self) -> dict[str, WordNode]:
        '''Getter for children property'''
        return self.__children

    @property
    def parent(self) -> WordNode:
        '''Getter for parent property'''
        return self.__parent

    @property
    def board_pos(self) -> (int, int):
        '''Getter for board_pos property'''
        return self.__board_pos

    def add_child_node(self, node):
        '''Add child node to `children` dictionary, indexed by the nodes' `letter`'''
        self.children[node.letters] = node

    @property
    def path(self) -> list[WordNode]:
        '''Return list of nodes from current node to the root'''
        curr_node = self
        path = []
        path.append(curr_node.board_pos)
        while curr_node.parent is not None:
            path.append(curr_node.parent.board_pos)
            curr_node = curr_node.parent

        return path

    def get_word(self, board: BoggleBoard) -> str:
        '''Return word or word fragment based on the WordNode's path property'''
        return "".join([board.board[x].letters for x in self.path[::-1]])

    def __str__(self):
        return f"WordNode: {self.letters}, {self.is_word}, {self.board_pos}"

    def __repr__(self):
        return f"WordNode: {self.letters}, {self.is_word}, {self.children}"

class WordTree:
    '''A tree populated by WordNode(s) to complete words from a given root letter and wordlist'''
    def __init__(self, alphabet: list, root: WordNode, words: list[str] = None,
        max_word_len = 16) -> WordTree:
        self.__alphabet: list = alphabet
        self.__wordlist: list[str] = words
        self.__root: WordNode = root
        self.__max_word_len: int = max_word_len
        self.__tree: dict[str, WordNode] = {}
        self.__word_paths: dict[str, list[WordNode]] = []

        # Generate root node
        self.__tree[root.letters] = root
        self.active_node: WordNode = self.__tree[root.letters]

        # Populate tree from wordlist
        if words is not None:
            for word in words:
                self.__insert_word(word)

    @property
    def alphabet(self) -> list:
        '''Getter for alphabet property'''
        return self.__alphabet

    @property
    def wordlist(self) -> list[str]:
        '''Getter for wordlist property'''
        return self.__wordlist

    @property
    def root(self) -> WordNode:
        '''Getter for root property'''
        return self.__root

    @property
    def max_word_len(self) -> int:
        '''Getter for max_word_len property'''
        return self.__max_word_len

    @property
    def tree(self) -> dict[str, WordNode]:
        '''Getter for tree property'''
        return self.__tree

    @property
    def word_paths(self) -> dict[(int, int), WordNode]:
        '''Getter for leaf_nodes property'''
        return self.__word_paths

    @word_paths.setter
    def word_paths(self, value):
        self.__word_paths = value

    def __str__(self):
        return ", ".join(self.wordlist)

    def insert_node(self, letters: str, parent: WordNode, is_word: bool = False,
        children: dict[str, WordNode] = None, board_pos = None):
        '''Create WordNode for `letters` and into WordTree under `parent`'''
        node = WordNode(letters, is_word, parent, children, board_pos)
        parent.add_child_node(node)

    def __insert_word(self, word: str) -> bool:
        '''Returns True if the word could be inserted into the tree with the given alphabet,
        otherwise returns False'''

        # Insert root node
        prefix = word[0:len(self.root.letters)] # prefix = first letter block
        if word is None or prefix != self.root.letters:
            return False
        curr_node = self.tree[prefix]
        word_len = len(word)

        # Insert remaining nodes as letter groups based on alphabet
        skip_cnt = 0
        for i, letter in enumerate(word[len(prefix):self.max_word_len]):
            # Skip word letter iterations for length of a previously inserted letter group
            if skip_cnt > 0:
                skip_cnt -= 1
                continue

            try:
                alpha_index = self.alphabet.index(letter)
            except ValueError: # letters not in given alphabet
                return False

            # Insert letter (single)
            if letter == self.alphabet[alpha_index] and letter not in curr_node.children:
                self.insert_node(letter, curr_node)
                curr_node = curr_node.children[letter]
            # Letter already exists
            elif letter == self.alphabet[alpha_index]:
                curr_node = curr_node.children[letter]
            # Check for letter groups (like "Qu") starting with `letter` in alphabet
            else:
                alpha = self.alphabet[alpha_index]
                # Check that letter group is shorter than and matches in the word remainder
                if len(alpha) < word_len - i and alpha == word[i+1:i+1+len(alpha)]:
                    if alpha not in curr_node.children:
                        self.insert_node(alpha, curr_node)
                        curr_node = curr_node.children[alpha]
                    else: # node already exist
                        curr_node = curr_node.children[alpha]

                    skip_cnt = len(alpha) - 1
                    #print(f"LONG GROUP: {alpha}; {word}")
                else:
                    return False

        # Mark the last node as a word
        curr_node.is_word = len(word) <= self.max_word_len
        return True

    def search(self, word: str, curr_node = None) -> WordNode:
        '''Return leaf (WordNode) if a given word is in the tree otherwise return None'''
        if len(word) == 0 or word is None:
            return curr_node

        if curr_node is None:
            curr_node = self.root
        for letters in curr_node.children:
            if letters == word[len(curr_node.letters):len(curr_node.letters) + len(letters)]:
                return self.search(word[len(curr_node.letters):], curr_node.children[letters])

        # Currently only returns single path for word
        # TODO: return all possible paths, maybe create minature WordTree? Or just of list of paths.
        return curr_node

    def build_boggle_tree(self, board: BoggleBoard, board_cell: BoardCell, subtree: WordTree, word_len: int = 0) -> WordTree:
        '''Return subtree of board given a particular root (first letter).

        Keyword arguments:
        board       -- the board the new tree is based on
        board_node  -- a pointer on the board where new branch nodes can be inserted into the tree
        dict_node   -- a pointer on the dictionary where nodes are read from for validation
        subtree     -- the partial tree passed to the next recursive step for generating branches
        '''

        if word_len > self.max_word_len or word_len >= board.max_word_len:
            #print(f"MAX DEPTH REACHED! Depth = {depth}")
            subtree.active_node = subtree.active_node.parent
            self.active_node = self.active_node.parent
            return

        # TODO rework active_node refs for recursion so don't have to be reset to parent at every point of return
        if self.active_node.is_word and len(self.active_node.children) == 0:
            word_path = subtree.active_node.path[::-1]
            subtree.word_paths.append((subtree.active_node.get_word(board), word_path))
            #print("1: WORD FOUND:", "".join([board.board[x].letters for x in word_path]), word_path)
            self.active_node = self.active_node.parent
            subtree.active_node = subtree.active_node.parent
            return
        elif self.active_node.is_word:
            word_path = subtree.active_node.path[::-1]
            subtree.word_paths.append((subtree.active_node.get_word(board), word_path))
            #print("2: WORD FOUND:", "".join([board.board[x].letters for x in word_path]), word_path)

        # Branch for each adjacent board cell
        for cell in board_cell.adjacent_cells:
            # Check dictionary and exclude nodes already in path
            if cell.letters in self.active_node.children and cell.pos not in subtree.active_node.path:
                new_node = WordNode(cell.letters, self.active_node.is_word, subtree.active_node, board_pos = cell.pos)
                subtree.active_node.add_child_node(new_node)
                subtree.active_node = subtree.active_node.children[cell.letters] # update subtree pointer
                self.active_node = self.active_node.children[cell.letters] # update dictionary tree pointer
                self.build_boggle_tree(board, board.board[cell.pos], subtree, word_len=word_len+len(board_cell.letters))

        self.active_node = self.active_node.parent
        subtree.active_node = subtree.active_node.parent
        return subtree

def build_boggle_tree(args):
    '''Build boggle tree from arguments for process Pool'''
    (alphabet, board, cell, wordlist) = args
    root_node = WordNode(cell.letters)
    dict_tree = WordTree(alphabet, root_node, wordlist)
    sub_tree = WordTree(alphabet, WordNode(cell.letters, False, board_pos=cell.pos))
    return dict_tree.build_boggle_tree(board, cell, sub_tree)

def build_full_boggle_tree(board: BoggleBoard, wordlist_path: str) -> dict[str, WordTree]:
    '''Return dictionary of WordTree(s) for every letter on a BoggleBoard'''
    alphabet = sorted(set([cell.letters for cell in board.board.values()]))
    board_tree = {}
    index = {}

    print("Reading in wordlists...")
    for letters in alphabet:
        if letters == "":
            # Skip wordlist read for blocks with empty string
            index[""] = {}
            continue
        elif letters[0] in index:
            index[letters] = index[letters[0]]
            continue

        filename = "words_" + letters[0] + ".txt"
        try:
            wordlist = read_wordlist(path.join(path.abspath(wordlist_path), filename))
            index[letters] = wordlist
            print(f">> {letters}: {filename}")
        except FileNotFoundError:
            print(f">> {letters}: -- Skipping -- no wordlist found for {letters}")
            index[letters] = {}

    print("Generating WordTrees...")
    params = [ [alphabet, board, cell, index[cell.letters] ] for cell in board.board.values()]
    with Pool(processes=len(board.board)) as pool:
        for i, res in enumerate(pool.map(build_boggle_tree, params)):
            print(f">> {params[i][2]}")
            board_tree[params[i][2].pos] = res

    return board_tree

def read_wordlist(file):
    '''Return dictionary of words with associated word count (1 by default)'''
    with open(file, 'r', encoding='utf-8') as file:
        return {k:1 for k in file.read().split()}

def read_boggle_file(file):
    '''Return list of rows from Boggle board csv file'''
    with open(file, 'r', encoding='utf-8') as file:
        return [x.rstrip().split(',') for x in file.readlines()]
