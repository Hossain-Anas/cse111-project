from tkinter import *
import copy
from operator import itemgetter


class Tic_Tac_toe:
    winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                            [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    buttons = []

    def __init__(self):
        self.board = [" "] * 9
        self.moves = [StringVar() for i in range(9)]
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.current_player = 'X'
        self.move_number = 0
        self.game_over = None

        self.set_moves(lambda x: x.set(" "), self.moves)

    @staticmethod
    def set_moves(do, inp):
        for i in inp:
            do(i)

    def reset(self):
        ai_switch.config(state='normal')
        self.current_player = "X"
        self.move_number = 0
        self.game_over = False

        info_text.set("It is X's turn")

        self.board = [" " for i in self.board]
        self.update_board()

        for b in Tic_Tac_toe.buttons:
            b.config(state="normal")
            b.config(disabledforeground="black")
            b.config(text="", bg="#F0F0F0")

    def make_move(self, move):
        ai_switch.config(state='disabled')
        self.move_number += 1
        if self.current_player == "X":
            self.board[move] = "X"
            info_text.set("It is O's turn")
            self.current_player = "O"

            if ai_switch_control.get() and self.move_number < 9:
                self.ai_mm_init()
        else:
            self.board[move] = "O"
            info_text.set("It is X's turn")
            self.current_player = "X"

        if self.game_over:
            return

        self.buttons[move].config(state="disabled")

        winner = self.game_won(self.board)
        if winner is not None:
            self.get_winner(winner)
            self.game_over = True

        elif self.move_number == 9 and self.check_move_available(self.board):
            info_text.set("DRAW!")
            self.get_winner(winner)
            self.draws += 1
            self.set_moves(lambda x: x.config(bg="yellow", fg='black'), self.buttons)
            self.game_over = True

        self.update_board()

    def update_board(self):
        for i in range(9):
            self.moves[i].set(self.board[i])

    @staticmethod
    def change_player(current_player):
        if current_player == "X":
            return "O"
        else:
            return "X"

    def game_won(self, gameboard):

        check = self.any_return([self.three_in_a_row(gameboard, c) for c in Tic_Tac_toe.winning_combinations])
        if check:
            return check
        else:

            return None

    @staticmethod
    def any_return(combinations):
        for i in combinations:
            if i:
                return i
        return False

    @staticmethod
    def check_move_available(board):
        for s in board:
            if s == " ":
                return False

        return True

    def three_in_a_row(self, gameboard, squares):

        combo = set(itemgetter(squares[0], squares[1], squares[2])(gameboard))
        if len(combo) == 1 and combo.pop() != " ":
            self.winning_squares = squares
            return gameboard[squares[0]]
        else:
            return None

    def get_winner(self, winner):
        if winner == "X":
            info_text.set("X wins!!!")
            self.x_wins += 1
        elif winner == 'O':
            info_text.set("O wins!!!")
            self.o_wins += 1

        else:
            self.draws += 1

        count_text.set("X: " + str(self.x_wins) + "  O: " + str(self.o_wins) + "  Draw: " + str(self.draws))

        self.set_moves(lambda x: x.config(bg="green"),
                       [self.buttons[s] for s in self.winning_squares])

        for b in self.buttons:
            b.config(state="disabled")

    def ai_mm_init(self):
        player = "O"
        a = -1000
        b = 1000

        board_copy = copy.deepcopy(self.board)

        best_outcome = -100

        best_move = None

        for i in range(9):
            if board_copy[i] == " ":
                board_copy[i] = player
                val = self.minimax(self.change_player(player), board_copy, a, b)
                board_copy[i] = " "
                if player == "O":
                    if val > best_outcome:
                        best_outcome = val
                        best_move = i
                else:
                    if val < best_outcome:
                        best_outcome = val
                        best_move = i

        self.make_move(best_move)

    def minimax(self, player, board, alpha, beta):
        board_copy = copy.deepcopy(board)

        winner = self.game_won(board_copy)

        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif self.check_move_available(board_copy):
            return 0

        best_outcome = -100 if player == "O" else 100

        for i in range(9):
            if board_copy[i] == " ":
                board_copy[i] = player
                val = self.minimax(self.change_player(player), board_copy, alpha, beta)
                board_copy[i] = " "
                if player == "O":
                    best_outcome = max(best_outcome, val)
                    alpha = min(alpha, best_outcome)
                else:
                    best_outcome = min(best_outcome, val)
                    beta = max(beta, best_outcome)

                if beta <= alpha:
                    return best_outcome

        return best_outcome


root = Tk()
root.title("Tic_tac_toe!")

game = Tic_Tac_toe()


welcome_text = StringVar()
welcome_text.set("welcome!")
welcome = Label(root, textvariable=welcome_text)
welcome.grid(row=0, column=0, columnspan=3)


count_text = StringVar()
count_text.set("X: " + str(game.x_wins) + "  O: " + str(game.o_wins) + "  Draw: " + str(game.draws))
count = Label(root, textvariable=count_text)
count.grid(row=1, column=0, columnspan=3)


info_text = StringVar()
info_text.set("It is X's turn")
info = Label(root, textvariable=info_text)
info.grid(row=2, column=0, columnspan=3)


for i in range(9):
    temp_button = Button(root, textvariable=game.moves[i], command=lambda s=i: game.make_move(s))
    temp_button.grid(row=int((i / 3)) + 3, column=(i % 3), sticky=NSEW)
    game.buttons.append(temp_button)


restart_button_text = StringVar()
restart_button_text.set("Restart")
restart_button = Button(root, textvariable=restart_button_text, command=game.reset)
restart_button.grid(row=1, column=0)


ai_switch_control = IntVar()
ai_switch = Checkbutton(root, text="Turn on AI", variable=ai_switch_control)
ai_switch.grid(row=1, column=2)


root.columnconfigure(0, minsize=200)
root.columnconfigure(1, minsize=200)
root.columnconfigure(2, minsize=200)
root.rowconfigure(3, minsize=200)
root.rowconfigure(4, minsize=200)
root.rowconfigure(5, minsize=200)


root.mainloop()
