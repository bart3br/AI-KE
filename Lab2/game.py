from constants import EMPTY_CELL_VALUE

class Game:
    def __init__(self, game_state: list) -> None:
        self.board = []
        self.__init_board(game_state)
        self.turn = 1
        self.winner = 0
        self.BOARD_SIZE = len(self.board)
        
    def __init_board(self, game_state: list) -> None:
        for i in range(len(game_state)):
            self.board.append([])
            for j in range(len(game_state[i])):
                self.board[i].append(Cell(i, j, game_state[i][j]))
                
    def __str__(self) -> str:
        board_str = f'turn={self.turn}, winner={self.winner}\n'
        for line in self.board:
            for cell in line:
                board_str += str(cell.symbol) + ' '
            board_str += '\n'
        return board_str
    
    def get_cell_val(self, x: int, y: int) -> int:
        return self.board[x][y].symbol
    
    def set_cell_val(self, x: int, y: int, value: int) -> None:
        self.board[x][y].symbol = value
        
    def switch_cells_vals(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.board[x1][y1].symbol, self.board[x2][y2].symbol = self.board[x2][y2].symbol, self.board[x1][y1].symbol
        
    def move_pawn(self, player_num: int, pos_x: int, pos_y: int, target_pos_x: int, target_pos_y: int) -> None:
        if (self.get_cell_val(pos_x, pos_y) != player_num):
            raise ValueError('Trying to move other players pawn')
        if (self.get_cell_val(target_pos_x, target_pos_y) != EMPTY_CELL_VALUE):
            raise ValueError('Cell is already occupied by other pawn')
        self.switch_cells_vals(pos_x, pos_y, target_pos_x, target_pos_y)
        self.turn += 1
        # check for winner
                       
        
class Cell:
    def __init__(self, pos_x: int, pos_y: int, symbol: int) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.symbol = symbol
    
    def __str__(self) -> str:
        return f'position({self.pos_x}, {self.pos_y}), symbol = {self.symbol}'

        
if __name__ == "__main__":
    pass
        