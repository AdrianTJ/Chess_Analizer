# Libraries
import chess
import chess.engine
import pandas as pd
import numpy as np
import os
import re
import sys

# Getting path to stockfish engine, in this case, in same directory
path = os.getcwd()
engine = chess.engine.SimpleEngine.popen_uci(path+'/'+'stockfish')

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
    df2 = pd.DataFrame({'Move':move, 'Piece':piece, 'Score':score})
    return df2

def best_move_by_piece(allmoves):
    df3 = pd.DataFrame(columns = ['Move', 'Piece', 'Score'])
    uniqueValues = allmoves['Piece'].unique()
    i = 0
    for piece in uniqueValues:
        column = allmoves.where(allmoves["Piece"] == piece).dropna().reset_index(drop=True)
        df3.loc[i] = column.loc[np.argmax(column['Score']), :].values.tolist()
        i = i+1
    return df3


################################################ Testing ####################################################

fen = sys.argv[1]
sys.stdout.write(best_move_by_piece(single_move_evaluator(fen)).to_string())

# Run at the end of any program using the chess.engine.
engine.quit()