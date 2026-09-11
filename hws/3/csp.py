import time

class Skyscraper:
    def __init__(self, n, constraints,mrv_flag):
        self.size = n
        self.board = [[0] * self.size for _ in range(self.size)]
        self.constraints = constraints
        self.nodes_visited = 0
        self.mrv_flag=mrv_flag

    def check_duplicate(self, row, col, num):
        for i in range(self.size):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        return True

    def count_visible(self, buildings):
        max_height = 0
        count = 0
        for height in buildings:
            if height > max_height:
                count += 1
                max_height = height
        return count

    def full(self):
        return all(self.board[i][j] > 0 for i in range(self.size) for j in range(self.size))
    
    def check_constraints(self):

        for col in range(self.size):
            if self.constraints['top'][col] is not None:
                if self.count_visible([self.board[i][col] for i in range(self.size)]) != self.constraints['top'][col]:
                    return False

        for col in range(self.size):
            if self.constraints['bottom'][col] is not None:
                if self.count_visible([self.board[i][col] for i in range(self.size-1, -1, -1)]) != self.constraints['bottom'][col]:
                    return False

        for row in range(self.size):
            if self.constraints['left'][row] is not None:
                if self.count_visible(self.board[row]) != self.constraints['left'][row]:
                    return False

        for row in range(self.size):
            if self.constraints['right'][row] is not None:
                if self.count_visible(self.board[row][::-1]) != self.constraints['right'][row]:
                    return False
        return True
    

    def set_fixed_values(self, fixed_values):
        for (row, col, value) in fixed_values:
            self.board[row][col] = value
    
    def solve(self):
        self.nodes_visited += 1

        if self.full():
            return self.check_constraints()
        
        empty = self.mrv() if self.mrv_flag else self.not_mrv()
        
        if not empty:
            return False
        row, col = empty
        
        for num in range(1, self.size + 1):
            if self.check_duplicate(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        
        return False

    def mrv(self):
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    legal_values = sum(1 for num in range(1, self.size + 1) if self.check_duplicate(i,j,num))
                    empty_cells.append((legal_values, i, j))
    
        if empty_cells:
            empty_cells.sort(key=lambda x: x[0])
            return (empty_cells[0][1], empty_cells[0][2])
        return None
    
    def not_mrv(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def display_board(self):
        for row in self.board:
            print(" ".join(str(x) for x in row))
            
if __name__ == "__main__":

    while(True):
        n = int(input("enter the board size :"))
        mrv_value = bool(int(input("use mrv enter 1 else enter 0 :")))

        left=[]
        right=[]
        top=[]
        bottom =[]

        for i in range(n):
            while True:
                try:
                    x, y = input(f"Left and Right constraints for row {i + 1}: ").split()
                    left.append(int(x))
                    right.append(int(y))
                    break 
                except ValueError:
                    print("incorrect input! try again.")

        for i in range(n):
            while True:
                try:
                    x, y = input(f"Top and Bottom constraints for column {i + 1}: ").split()
                    top.append(int(x))
                    bottom.append(int(y))
                    break 
                except ValueError:
                    print("incorrect input! try again.")  

        constraints = {
            'top': top,
            'bottom': bottom,
            'left': left,
            'right': right
        }
        use_fixed_values = input("if you wanna enter fixed values enter 1 else 0 : ")
        fixed_values = []

        # fixed_values = [   for 6x6
        # (0, 0, 1), 
        # (0, 5, 6),
        # (2, 4, 5),
        # (4, 0, 5), 
        # (5, 2, 3)
        # ]
        if use_fixed_values == '1':
            m = int(input("how many fixed valuse : "))
            for i in range(m):
                while True:
                    try:
                        row, col, value = map(int, input("enter row , col , value: ").split())
                        if 0 <= row < n and 0 <= col < n and 1 <= value <= n:
                            fixed_values.append((row, col, value))
                            print("added!")
                            break
                    except ValueError:
                        print("invalid input. try again.")

        game = Skyscraper(n, constraints, mrv_value)
        game.set_fixed_values(fixed_values)
   
        start_time = time.time()

        if game.solve():

            game.display_board()
            print("time:", time.time() - start_time,"s")
            print("visited nodes:",game.nodes_visited)

        else:
            print("No solution found.")
        
   
        
