import time


x = 'X'
o = 'O'
r = 'R'
board = 10
neg_inf = -10000000
pos_inf = 10000000

class Connect4:

    def __init__(self):

        self.board = [[' ' for _ in range(board)] for _ in range(board)]
        self.current_player = x
        self.num = 0 

    def print_board(self):
        print('--' *2* len(self.board[0]))
        for line in self.board:
            print('| ' + ' | '.join(line) + ' |')
            print('--' *2* len(self.board[0]))
        print(' ',0,' ',1,' ',2,' ',3,' ',4,' ',5,' ',6,' ',7,' ',8,' ',9)   

    def position(self, column, player):
        line = board - 1 
        while line >= 0:
            if self.board[line][column] == ' ':
                self.board[line][column] = player 
                return (line, column)
            line -= 1 
        return None  

    def check_winner(self, player):
        for line in range(board):
            for col in range(board):
                if (self.check_dir(line, col, 0, 1, player) or self.check_dir(line, col, 1, 0, player) or self.check_dir(line, col, 1, 1, player) or self.check_dir(line, col, 1, -1, player)):  
                    return True
        return False
    
    def check_dir(self, line, col, diff_line, diff_col, player):
        count = 0
        for i in range(4):
            li = line + i * diff_line
            co = col + i * diff_col
            if 0 <= li < board and 0 <= co < board and self.board[li][co] == player:
                count += 1
            else:
                break
        if count==4 :
            return True

    def is_full(self):
        for line in range(board):
            for col in range(board):
                if self.board[line][col] == ' ':
                    return False  
        return True

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        self.num += 1  

        if self.check_winner(r):
            return 10 - depth
        if self.check_winner(x) or self.check_winner(o):
            return depth - 10
        if self.is_full() or depth == 0:  
            return 0

        if maximizingPlayer:
            max_eval = neg_inf
            for col in range(board):
                if self.board[0][col] == ' ':
                    line, column = self.position(col, r)
                    eval = self.minimax(depth - 1, alpha, beta, False)
                    self.board[line][col] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
    
        else:
            min_eval = pos_inf
            for col in range(board):
                if self.board[0][col] == ' ':
                    line, column = None, None
                    if self.current_player == o:
                        line, column = self.position(col, o)
                        eval = self.minimax(depth - 1, alpha, beta, True)
                        self.board[line][col] = ' '

                    elif self.current_player == x:
                        line, column = self.position(col, x)
                        eval = self.minimax(depth - 1, alpha, beta, True)
                        self.board[line][col] = ' '

                if line is not None and column is not None:
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval
        

    def robot_move(self):

        for col in range(board):
            if self.board[0][col] == ' ':
                line, column = self.position(col, r)
                if self.check_winner(r):
                    self.board[line][col] = ' '  
                    return col
                self.board[line][col] = ' '          

        for col in range(board):
            if self.board[0][col] == ' ':
                line, column = self.position(col, o)
                if self.check_winner(o):
                    self.board[line][col] = ' '  
                    return col
            self.board[line][col] = ' '            
        
        for col in range(board):
            if self.board[0][col] == ' ':
                line, column = self.position(col, x)
                if self.check_winner(x):
                    self.board[line][col] = ' '  
                    return col
            self.board[line][col] = ' ' 


         ### the code above will prevent the wining of x and o : meaning if x and o can make a move to win, r will prevent it by taking that position
         ### this can be deleted cause it is not causing problem for minimax algorithm

        best_eval = neg_inf
        move = None
        for col in range(board):
            if self.board[0][col] == ' ':
                line, column = self.position(col, r)
                eval = self.minimax(7, neg_inf, pos_inf, False)
                self.board[line][col] = ' '  
                if eval > best_eval:
                    best_eval = eval
                    move = col
        return move

    
    def play(self):
        start_time = time.time()

        while True:
            self.print_board()
            
            if self.current_player == x:
                col = int(input("player X :"))
                if 0 <= col < board:
                    if self.position(col, x):
                        if self.check_winner(x):
                            self.print_board()
                            print("player X wins!")
                            break
                        self.current_player = o
                    else:
                        print("column already taken")
                else:
                    print("invalid input")

            elif self.current_player == o:
                col = int(input("player O :"))
                if 0 <= col < board :
                    if self.position(col, o):
                        if self.check_winner(o):
                            self.print_board()
                            print("player O wins!")
                            break

                        self.current_player = r
                    else:
                        print("column already taken")
                else:
                    print("invalid input")

            else:
                col = self.robot_move()
                if self.position(col, r):
                    if self.check_winner(r):
                        self.print_board()
                        print("robot wins!")
                        break

                    self.current_player = x

            if self.is_full():
                self.print_board()
                print("no winner!")
                break
        end_time = time.time()

        print("time : ",end_time-start_time)    
        print("visited nodes :",self.num)

if __name__ == "__main__":
    game = Connect4()
    game.play()
