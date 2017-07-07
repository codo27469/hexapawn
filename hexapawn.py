#!/usr/bin/env python3

import sys


def print_board(board):
    num_col = len(board[0])
    num_row = len(board)
    for row in range(num_row):
        for col in range(num_col):
            print(board[row][col], end=' ')
        print('')


def check_moves(board, turn, row, col):
    moves = []
    num_col = len(board[0])
    num_row = len(board)
    if board[row][col] == 'p' and turn == 'B':  # black can only move south
        if row + 1 >= num_row:
            return moves
        # move S
        if board[row + 1][col] == '.':
            # print('can move south at row {}, col {}'.format(row, col))
            m = ((row, col), (row + 1, col))
            moves.append(m)
        # take SE
        if col - 1 >= 0 and board[row + 1][col - 1] == 'P':
            # print('can take se at row {}, col {}'.format(row, col))
            m = ((row, col), (row + 1, col - 1))
            moves.append(m)
        # take SW
        if col + 1 < num_col and board[row + 1][col + 1] == 'P':
            # print('can take sw at row {}, col {}'.format(row, col))
            m = ((row, col), (row + 1, col + 1))
            moves.append(m)

    elif board[row][col] == 'P' and turn == 'W':  # white con only move north
        if row - 1 < 0:
            return moves
        # move N
        if board[row - 1][col] == '.':
            # print('can move north at row {}, col {}'.format(row, col)
            m = ((row, col), (row - 1, col))
            moves.append(m)
        # take NE
        if col - 1 >= 0 and board[row - 1][col - 1] == 'p':
            # print('can move north at row {}, col {}'.format(row, col)
            m = ((row, col), (row - 1, col - 1))
            moves.append(m)
        # take NW
        if col + 1 < num_col and board[row - 1][col + 1] == 'p':
            # print('can move north at row {}, col {}'.format(row, col)
            m = ((row, col), (row - 1, col + 1))
            moves.append(m)

    return moves


def get_moves_for_player(turn, board):
    num_col = len(board[0])
    num_row = len(board)
    moves = []
    for row in range(num_row):
        for col in range(num_col):
            if board[row][col] != '.':
                mv = check_moves(board, turn, row, col)
                if len(mv) > 0:
                    [moves.append(m) for m in mv]
    return moves


def check_win(turn, board):
    num_row = len(board)
    # if a piece makes it to last rank, they win
    for piece in board[0]:
        if piece == 'P' and turn == 'W':
            return True
    for piece in board[num_row - 1]:
        if piece == 'p' and turn == 'B':
            return True
    return False


def apply_move(turn, board, move):
    start_pos = move[0]
    moving_pos = move[1]
    board[start_pos[0]][start_pos[1]] = '.'
    value = 'p' if turn == 'B' else 'P'
    original = board[moving_pos[0]][moving_pos[1]]
    board[moving_pos[0]][moving_pos[1]] = value
    return original


def undo_move(turn, board, move, original_val):
    start_pos = move[0]
    moving_pos = move[1]
    value = 'p' if turn == 'B' else 'P'
    board[start_pos[0]][start_pos[1]] = value
    board[moving_pos[0]][moving_pos[1]] = original_val
    return


def heuristic_sort(moves, board, turn):
    num_row = len(board)
    first_moves = []
    sorted_moves = [m for m in moves]
    for m in sorted_moves:
        if m[1][0] == 0 or m[1][0] == num_row - 1:
            sorted_moves.remove(m)
            first_moves.append(m)
    return first_moves + sorted_moves


def solve(turn, board):
    moves = get_moves_for_player(turn, board)
    if len(moves) == 0:
        return -1  # no moves available, game over
    max_val = -1
    next_turn = 'W' if turn == 'B' else 'B'
    for move in heuristic_sort(moves, board, turn):
        orig_val = apply_move(turn, board, move)
        win = check_win(turn, board)
        if win is True:
            undo_move(turn, board, move, orig_val)
            return 1
        else:
            val = -(solve(next_turn, board))
        max_val = max(max_val, val)
        undo_move(turn, board, move, orig_val)
    return max_val


def parse_input():
    input_lines = sys.stdin.readlines()
    side_to_move = str(input_lines[0].strip())
    board_lines = input_lines[1:]
    board = [[piece for piece in line.strip()] for line in board_lines]
    return side_to_move, board


if __name__ == '__main__':
    side, b = parse_input()
    print(solve(side, b))
