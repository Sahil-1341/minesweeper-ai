import random


class Minesweeper:
    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.mines = set()
        self.board = [[False for _ in range(width)] for _ in range(height)]

        while len(self.mines) < mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.board[i][j] = True
                self.mines.add((i, j))

        self.mines_found = set()

    def is_mine(self, cell):
        return self.board[cell[0]][cell[1]]

    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence:
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def known_mines(self):
        if self.count > 0 and len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        self.cells.discard(cell)


class MinesweeperAI:
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbors = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.append((i, j))

        cells = []
        for n in neighbors:
            if n in self.mines:
                count -= 1
            elif n not in self.safes:
                cells.append(n)

        new_sentence = Sentence(cells, count)
        if new_sentence not in self.knowledge and len(cells) > 0:
            self.knowledge.append(new_sentence)

        self.update_knowledge()

    def update_knowledge(self):
        changed = True
        while changed:
            changed = False

            safes = set()
            mines = set()

            for sentence in self.knowledge:
                safes |= sentence.known_safes()
                mines |= sentence.known_mines()

            for cell in safes:
                if cell not in self.safes:
                    self.mark_safe(cell)
                    changed = True

            for cell in mines:
                if cell not in self.mines:
                    self.mark_mine(cell)
                    changed = True

            new_sentences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 != s2 and s1.cells.issubset(s2.cells):
                        diff_cells = s2.cells - s1.cells
                        diff_count = s2.count - s1.count
                        if diff_cells and diff_count >= 0:
                            sentence = Sentence(diff_cells, diff_count)
                            if sentence not in self.knowledge:
                                new_sentences.append(sentence)

            if new_sentences:
                self.knowledge.extend(new_sentences)
                changed = True

            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        choices = [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]
        return random.choice(choices) if choices else None
