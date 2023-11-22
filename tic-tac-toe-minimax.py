import graphviz

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.score = 0

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter) != 0:
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([s == letter for s in row]):
            self.score = 10 if letter == 'X' else -10
            return self.score

        # Check column
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([s == letter for s in column]):
            self.score = 10 if letter == 'X' else -10
            return self.score

        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                self.score = 10 if letter == 'X' else -10
                return self.score
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                self.score = 10 if letter == 'X' else -10
                return self.score
        self.score = 0
        return self.score

def board_to_str(board):
    return '\n'.join(['|'.join(board[i:i + 3]) for i in range(0, len(board), 3)])


def print_tree(node, depth, maximizing_player, graph, parent=None):
    if depth == 0 or not node.empty_squares():
        return

    if maximizing_player:
        for move in node.available_moves():
            child = TicTacToe()
            child.board = node.board.copy()
            child.make_move(move, 'X')
            child_node = board_to_str(child.board)
            graph.node(child_node, label=f'X\'s Move\n{child_node}\nScore: {child.score}', fontname='Consolas')
            if parent is not None:
                graph.edge(parent, child_node)
            print_tree(child, depth - 1, False, graph, child_node)
    else:
        for move in node.available_moves():
            child = TicTacToe()
            child.board = node.board.copy()
            child.make_move(move, 'O')
            child_node = board_to_str(child.board)
            graph.node(child_node, label=f'O\'s Move\n{child_node}\nScore: {child.score}', fontname='Consolas')
            if parent is not None:
                graph.edge(parent, child_node)
            print_tree(child, depth - 1, True, graph, child_node)

def main():
    game = TicTacToe()
    dot = graphviz.Digraph(comment='The Minimax Tree', format='pdf', 
                           graph_attr={'label': 'TicTacToe Minimax Tree',
                                       'labelloc': 't',
                                       'ranksep': '1.5 equally'},
                            strict=True)
    initial_node = board_to_str(game.board)
    dot.node(initial_node, label=f'Start\n{initial_node}\nScore: {game.score}', fontname='Consolas')
    print_tree(game, 5, True, dot, initial_node)
    dot.render('minimax_tree', view=True)


if __name__ == '__main__':
    main()
