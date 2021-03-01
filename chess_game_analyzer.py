# Libraries
import chess
import chess.engine
import pandas as pd
import os
import re
import sys
import csv

# Getting path to stockfish engine, in this case, in same directory
path = os.getcwd()
engine = chess.engine.SimpleEngine.popen_uci(path+'/'+'stockfish')

# Some defaults on game settings for testing purposes. If we don't want defauls, ask for user input. 
# 1st argument: ponder time in sec, 2nd argument: max number of desired moves, 3rd argument: max number of games to play
def board_generator(arguments = [0.01,10,2]):
    
    # Outputs who is playing a certain move, white or black
    dictsidetomove = {True:'white',False:'black'}
    notationdict = {True:'.', False:'...'}

    board_positions = set(['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1']) # Start off set. 
    for i in range(arguments[2]):
        board = chess.Board() # Give starting position. No argument means starting board. 
        while not board.is_game_over() and board.fullmove_number<=arguments[1]:
            result = engine.play(board,chess.engine.Limit(time=arguments[0]))
            new_board = board.fen()
            board_positions.add(new_board)
            board.push(result.move)
    # engine.quit()
    all_board_positions = list(board_positions)
    return all_board_positions

# FEN is starting position of chess, for simplicity:
def single_move_evaluator(fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
    current_fen, player, move, piece, score, mate = [],[],[],[],[],[]
    board = chess.Board(fen) 
    for el in board.legal_moves:
        info = engine.analyse(board, chess.engine.Limit(time=.1), root_moves=[el])
        t = str(info["score"])
        price = re.search('-?\d+\.?\d*',t)[0]
        current_fen.append(fen)
        move.append(str(board.san(el)))
        score.append(round(int(price)/100.,2))
        mate.append(str(board.san(el)).endswith('+'))
        if "BLACK" in str(info["score"]):
            player.append("BLACK")
        else:
            player.append("WHITE")
        if len(board.san(el).replace("x","").replace("+","")) == 2:
            piece.append("P")
        else: piece.append(board.san(el).replace("x","").replace("+","")[0].upper())
    df2 = pd.DataFrame({'FEN':current_fen,'Player':player, 'Move':move, 'Piece':piece, 'Score':score, 'Mate':mate})
    return df2
        
    # engine.quit()

def game_analyzer(flat_list = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1']):
    current_fen = []
    player = []
    move = []
    piece = []
    score = []
    mate = []

    for fen in flat_list:
        board = chess.Board(fen)
        for el in board.legal_moves:
            info = engine.analyse(board, chess.engine.Limit(time=.1), root_moves=[el])
            t = str(info["score"])
            price = re.search('-?\d+\.?\d*',t)[0]
            current_fen.append(fen)
            move.append(str(board.san(el)))
            score.append(round(int(price)/100.,2))
            mate.append(str(board.san(el)).endswith('+'))
            if "BLACK" in str(info["score"]):
                player.append("BLACK")
            else:
                player.append("WHITE")
            if len(board.san(el).replace("x","").replace("+","")) == 2:
                piece.append("P")
            else: piece.append(board.san(el).replace("x","").replace("+","")[0].upper())
    # engine.quit()

    df2 = pd.DataFrame({'FEN':current_fen,'Player':player, 'Move':move, 'Score':score, 'Mate':mate})
    return df2


################################################ Testing ####################################################

# arguments = [0.01,10,1]
# print(board_generator(arguments))

fen = sys.argv[1]
sys.stdout.write(single_move_evaluator(fen).to_string())

# arguments = [0.01,20,1]
# print(game_analyzer(board_generator(arguments)))



# Run at the end of any program using the chess.engine.
engine.quit()
