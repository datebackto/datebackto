# Simple Gomoku game: human vs computer
# Board size 15x15

def create_board(size=15):
    return [[0 for _ in range(size)] for _ in range(size)]


def print_board(board):
    size = len(board)
    header = '   ' + ' '.join(f'{i:2}' for i in range(size))
    print(header)
    for i, row in enumerate(board):
        line = ' '.join(' .' if cell == 0 else ' X' if cell == 1 else ' O' for cell in row)
        print(f'{i:2} {line}')


def check_five(board, player):
    size = len(board)
    for x in range(size):
        for y in range(size):
            if board[x][y] != player:
                continue
            # horizontal
            if y <= size-5 and all(board[x][y+i] == player for i in range(5)):
                return True
            # vertical
            if x <= size-5 and all(board[x+i][y] == player for i in range(5)):
                return True
            # diagonal down-right
            if x <= size-5 and y <= size-5 and all(board[x+i][y+i] == player for i in range(5)):
                return True
            # diagonal up-right
            if x >= 4 and y <= size-5 and all(board[x-i][y+i] == player for i in range(5)):
                return True
    return False


def board_full(board):
    return all(cell != 0 for row in board for cell in row)


def get_moves(board):
    moves = []
    size = len(board)
    for x in range(size):
        for y in range(size):
            if board[x][y] == 0:
                moves.append((x, y))
    return moves


import random

def computer_move(board):
    # simple ai: random
    moves = get_moves(board)
    return random.choice(moves) if moves else None


def main():
    board = create_board()
    player = 1  # human starts with X
    while True:
        print_board(board)
        if player == 1:
            try:
                move = input('Your move (row col): ')
                if move.lower() in ['q', 'quit', 'exit']:
                    break
                x, y = map(int, move.split())
            except Exception:
                print('Invalid input. Use row col.')
                continue
            if not (0 <= x < len(board) and 0 <= y < len(board)) or board[x][y] != 0:
                print('Invalid move.')
                continue
        else:
            x, y = computer_move(board)
            print(f'Computer moves: {x} {y}')

        board[x][y] = player
        if check_five(board, player):
            print_board(board)
            winner = 'You' if player == 1 else 'Computer'
            print(f'{winner} win!')
            break
        if board_full(board):
            print_board(board)
            print('Draw!')
            break
        player = 2 if player == 1 else 1

if __name__ == '__main__':
    main()
