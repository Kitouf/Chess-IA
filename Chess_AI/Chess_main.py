from __future__ import annotations
import chess
import pygame
import math
from pygame.locals import QUIT, MOUSEBUTTONUP
import random

def evaluate(board):

    values = {
        chess.PAWN:100,
        chess.KNIGHT:320,
        chess.BISHOP:330,
        chess.ROOK:500,
        chess.QUEEN:900,
        chess.KING:0
    }

    score = 0

    for piece in values:
        score += len(board.pieces(piece, chess.WHITE)) * values[piece]
        score -= len(board.pieces(piece, chess.BLACK)) * values[piece]

    mobility = len(list(board.legal_moves))

    if board.turn:
        score += mobility
    else:
        score -= mobility

    return score

def order_moves(board):

    captures = []
    others = []

    for move in board.legal_moves:
        if board.is_capture(move):
            captures.append(move)
        else:
            others.append(move)
    return captures + others

def alphabeta(board, depth, alpha, beta, maximizing):

    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing:
        value = -math.inf

        for move in order_moves(board):
            board.push(move)
            value = max(value, alphabeta(board, depth-1, alpha, beta, False))
            board.pop()

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    else:
        value = math.inf

        for move in order_moves(board):
            board.push(move)
            value = min(value, alphabeta(board, depth-1, alpha, beta, True))
            board.pop()

            beta = min(beta, value)

            if alpha >= beta:
                break

        return value

def searchBestMove(board):

    best_move = None
    best_value = math.inf

    for move in board.legal_moves:

        board.push(move)
        value = alphabeta(board, 4, -math.inf, math.inf, True)
        board.pop()

        if value < best_value:
            best_value = value
            best_move = move

    return best_move


# =====================================================
# Chargement des images
# =====================================================

def load_images(square_size):
    pieces = {}
    names = ['p','r','n','b','q','k']
    
    for color in ['w','b']:
        for name in names:
            img = pygame.image.load(f"../Chess_AI/pieces/{color}{name}.png")
            img = pygame.transform.scale(img,(square_size,square_size))
            pieces[color+name] = img
    return pieces

# =====================================================
# Dessiner l'échiquier
# =====================================================

def draw_board(screen, board, pieces, selected_square, possible_moves):
    
    colors = [(240,217,181),(181,136,99)]
    
    for row in range(8):
        for col in range(8):
            color = colors[(row+col)%2]
            rect = pygame.Rect(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE)
            pygame.draw.rect(screen,color,rect)

    if selected_square is not None:
        col = chess.square_file(selected_square)
        row = 7 - chess.square_rank(selected_square)
        pygame.draw.rect(screen,(0,0,255),(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),4)

    for move in possible_moves:
        col = chess.square_file(move)
        row = 7 - chess.square_rank(move)
        pygame.draw.circle(screen,(0,0,255),(col*SQUARE_SIZE+SQUARE_SIZE//2,row*SQUARE_SIZE+SQUARE_SIZE//2),10)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = 'w' if piece.color else 'b'
            name = piece.symbol().lower()
            img = pieces[color+name]

            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)

            screen.blit(img,(col*SQUARE_SIZE,row*SQUARE_SIZE))

# =====================================================
# Programme principal
# =====================================================

if __name__ == "__main__":

    SCREEN_SIZE = 640
    SQUARE_SIZE = SCREEN_SIZE // 8

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
    pygame.display.set_caption("Jeu d'échecs")

    board = chess.Board()

    pieces = load_images(SQUARE_SIZE)

    selected_square = None
    possible_moves = []
    player_turn = True

    while True:

        if not player_turn and not board.is_game_over():
            move = searchBestMove(board)
            board.push(move)
            player_turn = True

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                exit()

            elif event.type == MOUSEBUTTONUP and event.button == 1:

                col = event.pos[0] // SQUARE_SIZE
                row = event.pos[1] // SQUARE_SIZE

                square = chess.square(col,7-row)

                if selected_square is None:
                    piece = board.piece_at(square)

                    if piece and piece.color == board.turn:
                        selected_square = square
                        possible_moves = [m.to_square for m in board.legal_moves if m.from_square == square]

                else:
                    piece = board.piece_at(selected_square)

                    # Promotion automatique en dame
                    if piece.piece_type == chess.PAWN and chess.square_rank(square) in [0, 7]:
                        move = chess.Move(selected_square, square, promotion=chess.QUEEN)
                    else:
                        move = chess.Move(selected_square, square)

                    if move in board.legal_moves:
                        board.push(move)
                        player_turn = False

                    selected_square = None
                    possible_moves = []

        draw_board(screen,board,pieces,selected_square,possible_moves)

        pygame.display.flip()