import numpy as np #arrays
import pygame

#source venv/bin/activate

# chess pieces
# -1=black pawn   1=white pawn
# -2=black knight 2=white knight
# -3=black bishop 3=white bishop
# -4=black rook   4=white rook
# -5=black queen  5=white queen
# -6=black king   6=white king
# 0 means an empty square

chessboard= np.array([
    [-4, -2, -3, -5, -6, -3, -2, -4],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 1,  1,  1,  1,  1,  1,  1,  1],
    [ 4,  2,  3,  5,  6,  3,  2,  4]
])

pygame.init()

screen = pygame.display.set_mode((800, 800))
#Creating chess board
chess_board_white=(255,240,219)
chess_board_black=(75,115,153)
square=100
png_load = {
    1: 'chess_pieces/p_white/w_pawn_png_1024px.png',
    2: 'chess_pieces/p_white/w_knight_png_1024px.png',
    3: 'chess_pieces/p_white/w_bishop_png_1024px.png',
    4: 'chess_pieces/p_white/w_rook_png_1024px.png',
    5: 'chess_pieces/p_white/w_queen_png_1024px.png',
    6: 'chess_pieces/p_white/w_king_png_1024px.png',
    -1: 'chess_pieces/p_black/b_pawn_png_1024px.png',
    -2: 'chess_pieces/p_black/b_knight_png_1024px.png',
    -3: 'chess_pieces/p_black/b_bishop_png_1024px.png',
    -4: 'chess_pieces/p_black/b_rook_png_1024px.png',
    -5: 'chess_pieces/p_black/b_queen_png_1024px.png',
    -6: 'chess_pieces/p_black/b_king_png_1024px.png',
}

Pieces = {}
for key, path in png_load.items():
    img = pygame.image.load(path)
    Pieces[key] = pygame.transform.smoothscale(img, (square - 20, square - 20))

def is_in_check(board, color, state):
    king_pos = None
    king_value = 6 * color
    for i in range(8):
        for j in range(8):
            if board[i, j] == king_value:
                king_pos = [i, j]
                break
        if king_pos is not None:
            if king_pos is None:
                return True
            break
    for i in range(8):
        for j in range(8):
            current_piece = board[i, j]
            if current_piece!=0 and (current_piece * color<0):
                enemy_pos = [i,j]
                can_attack=movesets(current_piece, enemy_pos, king_pos, board, state)
                if can_attack:
                    return True
    return False

def has_legal_moves(board, color, state):
    #checking every piece
    for r_start in range(8):
        for c_start in range(8):
            piece = board[r_start, c_start]
            
            if piece != 0 and (piece * color > 0):
                start_pos = [r_start, c_start]
                
                for r_dest in range(8):
                    for c_dest in range(8):

                        target_piece = board[r_dest, c_dest]
                        if piece * target_piece > 0:
                            continue

                        dest_pos = [r_dest, c_dest]
                        
                        #is the move correct checking movesets
                        legal = movesets(piece, start_pos, dest_pos, board, state)
                        
                        if legal:
                            #simulating moves
                            temp_board = board.copy()
                            temp_board[r_start, c_start] = 0
                            temp_board[r_dest, c_dest] = piece
                            
                            if legal == "en_passant":
                                temp_board[r_start, c_dest] = 0
                                
                            #checking if that moves saves the king
                            if not is_in_check(temp_board, color, state):
                                return True #A legal move has been found
                                
    return False #Check Mate end of the game

#x is piece type and y list piece_clicked meaning starting pos and z is distatination pos
def movesets(x, y, z, board, state):

    diff_vertical = abs(y[0]-z[0]) # subtraction vertical
    diff_horizontal = abs(y[1]-z[1]) # subtraction horizontal
    #knight moveset
    if abs(x)==2:  #
        if (diff_vertical == 1 and diff_horizontal == 2) or (diff_vertical == 2 and diff_horizontal == 1):
            return True
        #bishop moveset
    elif abs(x)==3: 
        if diff_vertical == diff_horizontal and diff_vertical > 0:
            step_vertical = 1 if z[0] > y[0] else -1
            step_horizontal = 1 if z[1] > y[1] else -1

            for i in range(1, diff_vertical):
                check_vertical =y[0] + (i * step_vertical)
                check_horizontal =y[1] + (i * step_horizontal)
                if board[check_vertical, check_horizontal] != 0:
                    return False
            return True
    elif abs(x)==4:
        vertical_pos=y[0]
        horizontal_pos=y[1]
        if (diff_vertical>0 and diff_horizontal==0):
            diff_vertical_not_abs=y[0]-z[0]
            if diff_vertical_not_abs<0:
                for i in range (diff_vertical-1):
                    vertical_pos+=1
                    current_position=board[vertical_pos,y[1]]
                    if current_position!=0:
                        return False
                return True
            else:
                for i in range (diff_vertical-1):
                    vertical_pos-=1
                    current_position=board[vertical_pos,y[1]]
                    if current_position!=0:
                        return False
                return True

        if (diff_vertical==0 and diff_horizontal>0):
            diff_horizontal_not_abs=y[1]-z[1]
            if diff_horizontal_not_abs<0:
                for i in range (diff_horizontal-1):
                    horizontal_pos+=1
                    current_position=board[y[0],horizontal_pos]
                    if current_position!=0:
                        return False
                return True
            else:
                for i in range (diff_horizontal-1):
                    horizontal_pos-=1
                    current_position=board[y[0],horizontal_pos]
                    if current_position!=0:
                        return False
                return True
            
    #queen moveset
    elif abs(x) == 5:
        return movesets(3, y, z, board, state) or movesets(4, y, z, board, state)
    
    #king moveset
    elif abs(x) == 6:
        # 1. normal moves
        if diff_horizontal <= 1 and diff_vertical <= 1:
            return True
        # 2 Castling
        if diff_vertical==0 and diff_horizontal==2:
            #white king
            if x==6 and y[0]==7 and y[1]==4 and not state.white_king_moved:
                #castle right side
                if z[0]==7 and z[1]==6 and not state.white_rook_right_moved:
                    if board[7,5]==0 and board[7,6]==0:
                        return "castle_right"
                #castle left side
                if z[0]==7 and z[1]==2 and not state.white_rook_left_moved:
                    if board[7, 1] == 0 and board[7, 2] == 0 and board[7, 3] == 0:
                        return "castle_left"
            #black king
            elif x == -6 and y[0] == 0 and not state.black_king_moved:
                #short
                if z[1] == 6 and not state.black_rook_right_moved:
                    if board[0, 5] == 0 and board[0, 6] == 0:
                        return "castle_right"
                #Long
                elif z[1] == 2 and not state.black_rook_left_moved:
                    if board[0, 1] == 0 and board[0, 2] == 0 and board[0, 3] == 0:
                        return "castle_left"

    elif abs(x) == 1:
        direction = -1 if x > 0 else 1
        start_row = 6 if x > 0 else 1

        # 1. move forward 1
        if diff_horizontal == 0 and (z[0] - y[0]) == direction:
            if board[z[0], z[1]] == 0:
                return True

        # 2. move forward 2
        elif diff_horizontal == 0 and (z[0] - y[0]) == 2 * direction and y[0] == start_row:
            middle_row = y[0] + direction
            if board[middle_row, y[1]] == 0 and board[z[0], z[1]] == 0:
                return True

        # diagonal moves
        elif diff_horizontal == 1 and (z[0] - y[0]) == direction:
            
            # 3. normal capture
            if board[z[0], z[1]] != 0:
                return True
                
            # 4. en passant
            elif board[z[0], z[1]] == 0 and state.last_move is not None:
                last_start, last_dest = state.last_move
                enemy_piece = board[last_dest[0], last_dest[1]]
                
                # Check if last move was an enemy pawn moving 2 squares
                if abs(enemy_piece) == 1 and abs(last_start[0] - last_dest[0]) == 2:
                    # Check if that pawn landed right next to our pawn
                    if last_dest[0] == y[0] and last_dest[1] == z[1]:
                        return "en_passant"

    return False

class GameState:
    def __init__(self):

        self.white_king_moved = False
        self.black_king_moved = False
        
        self.white_rook_left_moved = False
        self.white_rook_right_moved = False
        
        self.black_rook_left_moved = False
        self.black_rook_right_moved = False
        
        self.moves_done = 2
        self.last_move = None


state = GameState()
piece_clicked = None
running = True
game_over = False
invalid_king_pos = None

while running:
    if not game_over:
        if state.moves_done % 2 == 0:
            white_or_black = 1
        else:
            white_or_black = -1
            
        # Checking for checkmate or tie
        if not has_legal_moves(chessboard, white_or_black, state):
            if is_in_check(chessboard, white_or_black, state):
                if white_or_black == 1:
                    print("Check Mate Black won")
                else:
                    print("Check Mate White won")
            else:
                print("Tie")
            
            #blocking the game 
            game_over = True
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                #reseting the chessboard
                chessboard = np.array([
                    [-4, -2, -3, -5, -6, -3, -2, -4],
                    [-1, -1, -1, -1, -1, -1, -1, -1],
                    [ 0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0],
                    [ 1,  1,  1,  1,  1,  1,  1,  1],
                    [ 4,  2,  3,  5,  6,  3,  2,  4]
                ])
                # reseting
                state = GameState()
                piece_clicked = None
                invalid_king_pos = None
                game_over = False
                print("Game restarted")

                
        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            pos_tup=pygame.mouse.get_pos()
            #destination position x y
            pos=[pos_tup[1]//square,pos_tup[0]//square]

            if piece_clicked==None:
                if chessboard[pos[0],pos[1]]!=0:
                    #start position
                    piece_clicked=[pos[0],pos[1]]
                    #piece type for example -5 meaning a chess piece
                    piece_type=chessboard[pos[0],pos[1]]
                    
            else:
                legal = movesets(piece_type, piece_clicked, pos, chessboard, state)
                if pos==piece_clicked:
                    piece_clicked=None
                else:
                    piece=chessboard[piece_clicked[0],piece_clicked[1]]
                    target=chessboard[pos[0],pos[1]]


                    if piece * target > 0:
                        piece_clicked=None
                    else:

                        if legal:
                            if piece_type * white_or_black > 0:

                                #creating copy of the board 
                                temp_board = chessboard.copy()
                                
                                temp_board[piece_clicked[0], piece_clicked[1]] = 0
                                temp_board[pos[0], pos[1]] = piece
                                
                                if legal == "en_passant":
                                    temp_board[piece_clicked[0], pos[1]] = 0
                                    
                                #checking if the move is legal because of the potential king attack
                                if not is_in_check(temp_board, white_or_black, state):
                                    
                                    #the move is legal procceding as intended
                                    invalid_king_pos = None #reseting red king square
                                    chessboard[piece_clicked[0], piece_clicked[1]] = 0
                                    chessboard[pos[0], pos[1]] = piece
                                    
                                    if legal == "en_passant":
                                        chessboard[piece_clicked[0], pos[1]] = 0
                                    elif legal == "castle_right":
                                        chessboard[pos[0], 5] = chessboard[pos[0], 7] 
                                        chessboard[pos[0], 7] = 0
                                    elif legal == "castle_left":
                                        chessboard[pos[0], 3] = chessboard[pos[0], 0]
                                        chessboard[pos[0], 0] = 0
                                        
                                    #Castling info, checking if a crucial piece has moved and blocking potential castling bugs
                                    if piece == 6: state.white_king_moved = True
                                    elif piece == -6: state.black_king_moved = True
                                    elif piece == 4:
                                        if piece_clicked[1] == 0: state.white_rook_left_moved = True
                                        elif piece_clicked[1] == 7: state.white_rook_right_moved = True
                                    elif piece == -4:
                                        if piece_clicked[1] == 0: state.black_rook_left_moved = True
                                        elif piece_clicked[1] == 7: state.black_rook_right_moved = True
                                        
                                    state.last_move = (piece_clicked, pos)
                                    piece_clicked = None
                                    state.moves_done += 1
                                    
                                else:
                                    #illegal move because the king is not protected
                                    king_value = 6 * white_or_black
                                    for r in range(8):
                                        for c in range(8):
                                            if chessboard[r, c] == king_value:
                                                invalid_king_pos = [r, c]
                                    piece_clicked = None    
                            else:
                                piece_clicked = None
    #building the chessboard
    for r in range(8):

        y=r*100

        for c in range(8):

            x=c*100
            
            if (r+c)%2==0:
                
                pygame.draw.rect(screen,(chess_board_white),(x,y,square,square))
                
            else:

                pygame.draw.rect(screen,(chess_board_black),(x,y,square,square))
            chess_piece=chessboard[r,c]
            if chess_piece!=0:

                screen.blit(Pieces[chess_piece], (c * square + 10, r * square + 10))

    if piece_clicked is not None:
        pygame.draw.rect(screen,(255, 255, 0), pygame.Rect(piece_clicked[1]*square, piece_clicked[0]*square, square, square), 4)

    if invalid_king_pos is not None:

        pygame.draw.rect(screen, (201, 57, 30), pygame.Rect(invalid_king_pos[1]*square, invalid_king_pos[0]*square, square, square), 4)

    pygame.display.flip()

pygame.quit()