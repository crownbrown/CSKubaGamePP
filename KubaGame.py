# Author: Steve Thatcher
# Date: 06-09-2021
# Description: This file contains a class that that allows a game of Kuba to be played, including initializing
#       a new game via two passed tuples, each with a player name and B/W for game piece color.
#       The class has many methods that check passed moves to see if they are valid, recording the move
#       and updating winner and current turn, where appropriate, or returning False if the move is not valid.
#       Game rules can be found here: https://sites.google.com/site/boardandpieces/list-of-games/kuba
#       An example video can be found here: https://www.youtube.com/watch?v=XglqkfzsXYc

import copy  # imported to create deep copy of boards (lists) to check past board states

class KubaGame:
    """
    This class initializes a game of Kuba with two passed tuples via two passed tuples,
    each with a player name and B/W for game piece color. All variables are private and have
    appropriate getters and setter methods as needed. All methods for a game of Kuba are included
    within this class.
   """
    def __init__(self, player1, player2):
        self._player1_name = player1[0]  # Paring the user name and color from each tuple
        self._player1_color = player1[1]
        self._player2_name = player2[0]
        self._player2_color = player2[1]
        self._player1_red_captured = 0  # Both "red_captured" initialize to 0 at the start of game
        self._player2_red_captured = 0
        self._past_board = [["W", "W", " ", " ", " ", "B", "B"], ["W", "W", " ", "R", " ", "B", "B"],
                       [" ", " ", "R", "R", "R", " ", " "], [" ", "R", "R", "R", "R", "R", " "],
                       [" ", " ", "R", "R", "R", " ", " "], ["B", "B", " ", "R", " ", "W", "W"],
                       ["B", "B", " ", " ", " ", "W", "W"]]  # for tracking board state reversal moves
        self._starting_board = [["W", "W", " ", " ", " ", "B", "B"], ["W", "W", " ", "R", " ", "B", "B"],
                       [" ", " ", "R", "R", "R", " ", " "], [" ", "R", "R", "R", "R", "R", " "],
                       [" ", " ", "R", "R", "R", " ", " "], ["B", "B", " ", "R", " ", "W", "W"],
                       ["B", "B", " ", " ", " ", "W", "W"]]  # the main, current working board
        self._current_turn = None  # Because either player can start the game initializes to "None"
        self._winner = None  # No winner set at the beginning of game

    def get_player1_name(self):
        """Returns private player 1 name variable"""
        return self._player1_name

    def get_player2_name(self):
        """Returns private player 2 name variable"""
        return self._player2_name

    def get_winner(self):
        """Returns private winner variable"""
        return self._winner

    def set_winner(self, playername):
        """Receives passed playername and sets the private winner variable to the current player"""
        if playername == self.get_player1_name():  # Uses getter method to access private variable
            self._winner = self.get_player1_name()
        if playername == self.get_player2_name():
            self._winner = self.get_player2_name()

    def get_player_color(self, playername):
        """Returns player color ("B" or "W") from passed playername"""
        if playername == self.get_player1_name():  # Uses getter method to access private variable
            return self._player1_color
        if playername == self.get_player2_name():
            return self._player2_color

    def get_player_name(self, playername):
        """Returns player name from passed playername"""
        if playername == self.get_player1_name():  # Uses getter method to access private variable
            return self.get_player1_name()
        if playername == self.get_player2_name():
            return self.get_player2_name()

    def get_current_board(self):
        """Getter method for private variable starting_board"""
        return self._starting_board  # starting board is the main board, used in shallow/deep copies throughout

    def replace_current_board(self, replacement_board):
        """'Setter' method to replace the current 'starting' board with a passed board list"""
        self._starting_board = replacement_board

    def get_past_board(self):
        """Getter method for private variable past_board"""
        return self._past_board

    def replace_past_board(self, replacement_board):
        """'Setter' method to replace the past board with a passed board list"""
        self._past_board = replacement_board

    def get_captured(self, playername):
        """Getter method for private variable 'red_captured' for the passed playername"""
        if playername == self.get_player1_name():  # Uses getter method to access private variable
            return self._player1_red_captured
        if playername == self.get_player2_name():
            return self._player2_red_captured

    def update_captured(self, playername):
        """'Setter' method to update the private 'red_captured' variables for the passed playername """
        if playername == self.get_player1_name():  # Uses getter method to access private variable
            self._player1_red_captured += 1
        if playername == self.get_player2_name():
            self._player2_red_captured += 1

    def get_current_turn(self):
        """Getter method for private variable current_turn"""
        return self._current_turn

    def set_current_turn(self, playername):
        """'Setter' method to update the private 'current_turn' variable for the passed playername """
        if playername == self.get_player1_name():
            self._current_turn = self.get_player1_name()  # Uses getter method to access private variable
        elif playername == self.get_player2_name():
            self._current_turn = self.get_player2_name()

    def set_next_turn(self):
        """'Setter' method to update the private 'current_turn' variable to the other/next player"""
        if self.get_current_turn() == self.get_player1_name():  # Uses getter method to access private variable
            self.set_current_turn(self.get_player2_name())
        elif self.get_current_turn() == self.get_player2_name():
            self.set_current_turn(self.get_player1_name())

    def get_marble(self, coordinates):
        """Returns the contents of a given board space, either B/W/R for a marble, or X for empty space"""
        row = coordinates[0]
        col = coordinates[1]
        temp_board = self.get_current_board()  # shallow copy of current board
        if temp_board[row][col] == " ":
            return "X"  # returns "X" for a board space that is empty
        else:
            return temp_board[row][col]  # Otherwise returns the marble color in the space

    def get_marble_count(self):
        """Returns a tuple with the count of the marbles still on the board, in W/B/R order"""
        white_count = 0
        black_count = 0
        red_count = 0
        temp_board = self.get_current_board()  # shallow copy of current board
        for row in temp_board:  # iterates through rows in the board list
            for space in row:  # iterates through spaces in the current board list row
                if "W" in space:
                    white_count += 1
                elif "B" in space:
                    black_count += 1
                elif "R" in space:
                    red_count += 1
        marble_count = [white_count, black_count, red_count]
        return tuple(marble_count)

    def print_board(self, board_to_print):
        """Prints out a visual representation of the passing board list"""
        for row in board_to_print:
            print("–––––––––––––––––––––––––––––")
            for space in row:
                print("|", space, end="")
                print(end=" ")
            print("|", end="")
            print("\r")
        print("–––––––––––––––––––––––––––––", end="\n")

    def find_index_of_EOL_of_contig_pieces(self, coordinates, direction):
        """
        Starting at the 'current piece' which is the piece "pushing" in the direction of the move,
        this method works along the direction requested move to find the index of the row (F or B) or col (R or L)
        of the last line in a contiguous line of pieces in the direction of the move from the 'current piece'.
        Knowing this 'end of line' index allows other methods to determine if that move can be made and how many
        piece will be moved, including the 'current piece' and 'end of line' piece, which will be the same piece
        if only a single piece is being moved.
        """
        temp_board = self.get_current_board()  # shallow copy of current board
        current_space_row_index = coordinates[0]
        current_space_col_index = coordinates[1]

        if direction == "L" or direction == "F":  # sets variable for movement direction
            change_amount = -1
        elif direction == "R" or direction == "B":
            change_amount = 1

        if direction == "R" or direction == "L":
            end_of_line_of_contig_pieces_index = current_space_col_index  # Start at current piece col (b/c R/L)
            while 0 <= end_of_line_of_contig_pieces_index <= 6:
                if temp_board[current_space_row_index][end_of_line_of_contig_pieces_index] != " ":  # not empty
                    end_of_line_of_contig_pieces_index += change_amount  # moves to next square along movement line
                else:
                    end_of_line_of_contig_pieces_index -= change_amount
                    return end_of_line_of_contig_pieces_index
        elif direction == "F" or direction == "B":
            end_of_line_of_contig_pieces_index = current_space_row_index  # Start at current piece row (b/c F/B)
            while 0 <= end_of_line_of_contig_pieces_index <= 6:
                if temp_board[end_of_line_of_contig_pieces_index][current_space_col_index] != " ":  # not empty
                    end_of_line_of_contig_pieces_index += change_amount  # moves to next square along movement line
                else:
                    end_of_line_of_contig_pieces_index -= change_amount
                    return end_of_line_of_contig_pieces_index
        return end_of_line_of_contig_pieces_index

    def check_valid_player_name_direction_coordinates(self, playername, coordinates, direction):
        """
        Basic validation that the playername, direction, and coordinates passed to make_move are valid
        at a basic level (that playername is one of the player's names, that direction is one of the
        four allowed directions, and that the intergers in the coordinates are [0-6].
        """
        if playername == self.get_player_name(playername):
            if direction == "R" or "L" or "F" or "B":
                if 0 <= coordinates[0] <= 6:  # checking row integer
                    if 0 <= coordinates[1] <= 6:  # checking col integer
                        return True
        else:
            return False

    def check_piece_matches_player(self, playername, coordinates):
        """
        Basic validation that the 'current piece' which is the piece "pushing" in the direction of the move,
        matches the color of the current player.
        """
        temp_board = self.get_current_board()  # shallow copy of current board
        current_space_row_index = coordinates[0]
        current_space_col_index = coordinates[1]

        if temp_board[current_space_row_index][current_space_col_index] == self.get_player_color(playername):
            return True
        else:
            return False

    def check_proceeding_space(self, coordinates, direction):
        """
        Checks that the space "before" the 'current piece', which is the piece "pushing" in the direction of the move,
        is either an empty space or is the edge of the board, otherwise returns false.
        """
        temp_board = self.get_current_board()  # shallow copy of current board
        current_space_row_index = coordinates[0]
        current_space_col_index = coordinates[1]

        # Checking pieces on the edge, which can be pushed "into" the board, but not "outward" as single pieces
        if (current_space_col_index == 0 and direction == "L") or (current_space_col_index == 6 and direction == "R"):
            return False
        elif (current_space_row_index == 0 and direction == "F") or (current_space_row_index == 6 and direction == "B"):
            return False
        elif (current_space_col_index == 0 and direction == "R") or (current_space_col_index == 6 and direction == "L"):
            return True
        elif (current_space_row_index == 0 and direction == "B") or (current_space_row_index == 6 and direction == "F"):
            return True

        if direction == "L" or direction == "F":  # sets variable for movement direction
            change_amount = -1
        elif direction == "R" or direction == "B":
            change_amount = 1

        if direction == "R" or direction == "L":
            proceeding_space_index = (current_space_col_index - change_amount)  # col space "before" current piece
            if temp_board[current_space_row_index][proceeding_space_index] != " ":  # False if not empty
                return False
            elif temp_board[current_space_row_index][proceeding_space_index] == " ":  # True if not empty
                return True
        elif direction == "F" or direction == "B":
            proceeding_space_index = (current_space_row_index - change_amount)  # row space "before" current piece
            if temp_board[proceeding_space_index][current_space_col_index] != " ":  # False if not empty
                return False
            elif temp_board[proceeding_space_index][current_space_col_index] == " ":  # True if not empty
                return True

    def check_end_of_line_of_contig_pieces(self, playername, coordinates, direction):
        """
        Checks to see that the last piece in a contiguous line of pieces in the direction of the move 
        from the 'current piece' is NOT the same color as the current player, otherwise it is an invalid move
        ("False") in the rules of the game to push your own piece off the board.
        """
        temp_board = self.get_current_board()  # shallow copy of current board
        current_space_row_index = coordinates[0]
        current_space_col_index = coordinates[1]

        # calls method to find index of the "end of line" piece
        end_of_line_of_contig_pieces_index = self.find_index_of_EOL_of_contig_pieces(coordinates,direction)
        if 0 < end_of_line_of_contig_pieces_index < 6:  #
            return True  # if the "end of line" piece is not on edge of board, it can be moved by owner without issue
        else:
            if end_of_line_of_contig_pieces_index < 0:
                end_of_line_of_contig_pieces_index = 0  # corrects for out of bounds index values
            elif end_of_line_of_contig_pieces_index > 6:
                end_of_line_of_contig_pieces_index = 6  # corrects for out of bounds index values

            if direction == "R" or direction == "L":
                if temp_board[current_space_row_index][end_of_line_of_contig_pieces_index] == self.get_player_color(
                        playername) and (current_space_col_index != end_of_line_of_contig_pieces_index):
                    return False  # if the color at the "end of the line" on the edge of the board matches can't move
                else:
                    return True
            elif direction == "F" or direction == "B":
                if temp_board[end_of_line_of_contig_pieces_index][current_space_row_index] == self.get_player_color(
                        playername) and (current_space_row_index != end_of_line_of_contig_pieces_index):
                    return False  # if the color at the "end of the line" on the edge of the board matches can't move
                else:
                    return True

    def check_and_record_captured_red(self, playername, coordinates_of_captured_piece):
        """
        Called by other methods to check whether the piece just moved off the board is R,
        if it is it updates the player 'captured_red' variable through setter method.
        """
        temp_board = self.get_current_board()  # shallow copy of current board
        if temp_board[coordinates_of_captured_piece[0]][coordinates_of_captured_piece[1]] == "R":
            self.update_captured(playername)
        else:
            pass

    def winner_check(self, playername):
        """
        Called after a move is recorded to see if the current player has won, either by 1) capturing all red
        marbles, or 2) having pushed all opponent's marbles off the board.
        """
        if self.get_captured(playername) == 13:  # if player has captured all 13 red marbles, they have won
            self.set_winner(playername)

        current_player_color = self.get_player_color(playername)
        current_marble_count = self.get_marble_count()
        if current_player_color == "W":
            if current_marble_count[1] == 0:  # check to see if all black marbles are off board, if so, W won
                self.set_winner(playername)
        elif current_player_color == "B":
            if current_marble_count[0] == 0:  # check to see if all white marbles are off board, if so, B won
                self.set_winner(playername)

    def move_the_pieces(self, playername, coordinates, direction):
        """
        Calls to find the "end of line" index, then starting at the end of line, copies each piece over one space
        along the line of movement, then replaces the original piece/space with empty. Writes changes to a deep copy
        of the current board, which is then passed back to make_move to be checked. All moves all valid because
        the conditions have been checked by other methods.
        """
        temp_board = copy.deepcopy(self.get_current_board())  # deep copy of current board
        current_space_row_index = coordinates[0]
        current_space_col_index = coordinates[1]

        if direction == "L" or direction == "F":  # sets variable for movement direction
            change_amount = -1
        elif direction == "R" or direction == "B":
            change_amount = 1

        # Calls method to find index of the end of the line
        end_of_line_of_contig_pieces_index = self.find_index_of_EOL_of_contig_pieces(coordinates,direction)

        if end_of_line_of_contig_pieces_index < 0:
            end_of_line_of_contig_pieces_index = 0  # corrects for out of bounds index values
            piece_being_moved_index = end_of_line_of_contig_pieces_index
        elif end_of_line_of_contig_pieces_index > 6:
            end_of_line_of_contig_pieces_index = 6  # corrects for out of bounds index values
            piece_being_moved_index = end_of_line_of_contig_pieces_index
        else:
            piece_being_moved_index = end_of_line_of_contig_pieces_index

        if direction == "R" or direction == "L":  # calculates the total number of pieces to be moved this turn
            pieces_to_move = (abs(end_of_line_of_contig_pieces_index - current_space_col_index) + 1)
        elif direction == "F" or direction == "B":
            pieces_to_move = (abs(end_of_line_of_contig_pieces_index - current_space_row_index) + 1)

        # If the piece at the end of the line being moved is on an edge, updates edge space only
        if end_of_line_of_contig_pieces_index == 0 and (direction == "L" or direction == "F"):
            if direction == "L":
                # calls to check if removed piece is red
                self.check_and_record_captured_red(playername, (current_space_row_index, piece_being_moved_index))
                temp_board[current_space_row_index][piece_being_moved_index] = " "
                piece_being_moved_index -= change_amount
                pieces_to_move -= 1
            elif direction == "F":
                # If the piece at the end of the line being moved is on an edge, updates edge space only
                self.check_and_record_captured_red(playername, (piece_being_moved_index, current_space_col_index))
                temp_board[piece_being_moved_index][current_space_col_index] = " "
                piece_being_moved_index -= change_amount
                pieces_to_move -= 1
        elif end_of_line_of_contig_pieces_index == 6 and (direction == "R" or direction == "B"):
                # If the piece at the end of the line being moved is on an edge, updates edge space only
            if direction == "R":
                self.check_and_record_captured_red(playername, (current_space_row_index, piece_being_moved_index))
                temp_board[current_space_row_index][piece_being_moved_index] = " "
                piece_being_moved_index -= change_amount
                pieces_to_move -= 1
            elif direction == "B":
                # If the piece at the end of the line being moved is on an edge, updates edge space only
                self.check_and_record_captured_red(playername, (piece_being_moved_index, current_space_col_index))
                temp_board[piece_being_moved_index][current_space_col_index] = " "
                piece_being_moved_index -= change_amount
                pieces_to_move -= 1

        # Moving piece that are not falling off an edge
        if direction == "R" or direction == "L":
            while pieces_to_move > 0:  # sets loop counter using total number of pieces to be moved
                # moves contents of current space being "moved" to the next space along movement line
                temp_board[current_space_row_index][piece_being_moved_index + change_amount] = \
                temp_board[current_space_row_index][piece_being_moved_index]
                piece_being_moved_index -= change_amount
                pieces_to_move -= 1
            if pieces_to_move == 0:  # if there are no pieces left to move, the original starting space made empty
                temp_board[current_space_row_index][current_space_col_index] = " "
            elif piece_being_moved_index == 0 and direction == "R":  # set to empty because no proceeding space
                temp_board[current_space_row_index][piece_being_moved_index] = " "
                pieces_to_move -= 1
            elif piece_being_moved_index == 6 and direction == "L":  # set to empty because no proceeding space
                temp_board[current_space_row_index][piece_being_moved_index] = " "
                pieces_to_move -= 1
            elif pieces_to_move == 0 and temp_board[current_space_row_index][current_space_col_index] != " ":
                temp_board[current_space_row_index][current_space_col_index] = " "
        elif direction == "F" or direction == "B":
            while pieces_to_move > 0:  # sets loop counter using total number of pieces to be moved
                # moves contents of current space being "moved" to the next space along movement line
                temp_board[piece_being_moved_index + change_amount][current_space_col_index] = \
                temp_board[piece_being_moved_index][current_space_col_index]
                piece_being_moved_index -= change_amount
                pieces_to_move -= 1
            if pieces_to_move == 0:  # if there are no pieces left to move, the original starting space made empty
                temp_board[current_space_row_index][current_space_col_index] = " "
            elif piece_being_moved_index == 0 and direction == "B":  # set to empty because no proceeding space
                temp_board[piece_being_moved_index][current_space_col_index] = " "
                pieces_to_move -= 1
            elif piece_being_moved_index == 6 and direction == "F":  # set to empty because no proceeding space
                temp_board[piece_being_moved_index][current_space_col_index] = " "
                pieces_to_move -= 1
            elif pieces_to_move == 0 and temp_board[current_space_row_index][current_space_col_index] != " ":
                temp_board[current_space_row_index][current_space_col_index] = " "
        return temp_board  # returns deep copy of the post_move board to make_move

    def make_move(self, playername, coordinates, direction):
        """
        Main method that received passed playername, coordinate of the starting piece being "pushed", and
        the direction of the movement. Calls multiple other functions to validate the move before calling
        move_the_pieces to actually make the moves. It then checks the "proposed" move again a deep copy save
        of the board state before the last player's turn. If they match, the move is not valid, and the move
        is not recorded, False is returned. Otherwise the move is recorded, the past_board is updated with the
        appropriate deep copy, and methods are called to check for a winner and update the current turn.
        """
        if self.check_valid_player_name_direction_coordinates(playername, coordinates, direction):
            if self.get_winner() is None:
                if self.get_current_turn() is None:  # for the inital move of the game as either player can start
                    self.set_current_turn(playername)
                if self.get_current_turn() == self.get_player_name(playername):  # check it is player's turn
                    if self.check_piece_matches_player(playername, coordinates):  # checks piece is player's
                        if self.check_proceeding_space(coordinates, direction):  # checks for edge/space "before" piece
                            if self.check_end_of_line_of_contig_pieces(playername, coordinates, direction):
                                # move is validates at this point, so move_the_pieces is called
                                post_movement_board = self.move_the_pieces(playername, coordinates, direction)
                                past_board = self.get_past_board()  # shallow copy of past board for checking
                                if post_movement_board == past_board:  # previous board state check
                                    return False
                                else:
                                    self.replace_past_board(copy.deepcopy(self.get_current_board()))  # deepcopy 2 past
                                    self.replace_current_board(copy.deepcopy(post_movement_board))  # deepcopy 2 current
                                    self.set_next_turn()  # sets turn too next player
                                    self.winner_check(playername)  # checks for winner, sets if winner
                                    self.print_board(post_movement_board)
                                    return True
                        return False
                    return False
                return False
            return False
        return False


if __name__ == '__main__':
    """
    g = KubaGame(("playerA", 'W'), ("playerB", 'B'))
    print(g.make_move("playerA", (1, 0), 'R'))
    print(g.make_move("playerB", (1, 6), 'L'))
    print(g.make_move("playerA", (1, 1), 'R'))
    print(g.make_move("playerB", (0, 6), 'B'))
    print(g.make_move("playerA", (1, 2), 'R'))
    print(g.make_move("playerB", (0, 5), 'B'))
    print(g.make_move("playerA", (1, 3), 'R'))
    print(g.make_move("playerB", (2, 6), 'F'))
    print(g.make_move("playerA", (1, 4), 'R'))
    print(g.make_move("playerB", (0, 6), 'B'))
    print(g.make_move("playerA", (1, 5), 'R'))
    print(g.make_move("playerB", (6, 0), 'R'))
    print(g.make_move("playerA", (2, 6), 'L'))
    print(g.make_move("playerB", (6, 1), 'R'))
    print(g.make_move("playerA", (2, 5), 'L'))
    print(g.make_move("playerB", (6, 2), 'R'))
    print(g.make_move("playerA", (2, 4), 'L'))
    print(g.make_move("playerB", (6, 3), 'R'))
    print(g.make_move("playerA", (2, 3), 'L'))
    print(g.make_move("playerB", (6, 4), 'R'))
    print(g.make_move("playerA", (2, 2), 'L'))
    print(g.make_move("playerB", (6, 6), 'F'))
    print(g.make_move("playerA", (2, 1), 'L'))
    print(g.make_move("playerB", (5, 6), 'F'))
    print(g.make_move("playerA", (3, 6), 'L'))
    print(g.make_move("playerB", (4, 6), 'F'))
    print(g.make_move("playerA", (5, 5), 'L'))
    print(g.make_move("playerB", (3, 6), 'F'))
    print(g.make_move("playerA", (3, 5), 'L'))
    print(g.make_move("playerB", (2, 6), 'F'))
    print(g.make_move("playerA", (3, 4), 'L'))
    print(g.make_move("playerB", (1, 6), 'F'))
    print(g.make_move("playerA", (3, 3), 'L'))
    print("Marble count: ",g.get_marble_count())
    """

    """
    g = KubaGame(("playerA", 'W'), ("playerB", 'B'))
    print("White 1,0 move right",g.make_move("playerA", (1, 0), 'R'))
    print("Black 1,6 move left",g.make_move("playerB", (1, 6), 'L'))
    print("White 1,1 move right",g.make_move("playerA", (1, 1), 'R'))
    print("Black 0,6 move backward",g.make_move("playerB", (0, 6), 'B'))
    print("White 1,2 move right",g.make_move("playerA", (1, 2), 'R'))
    print("Black 0,5 move backward",g.make_move("playerB", (0, 5), 'B'))
    print("White 1,3 move right",g.make_move("playerA", (1, 3), 'R'))
    print("Black 2,6 move forward",g.make_move("playerB", (2, 6), 'F'))
    print("White 1,4 move right",g.make_move("playerA", (1, 4), 'R'))
    print("Black 0,6 move backward",g.make_move("playerB", (0, 6), 'B'))
    print("White 1,5 move right",g.make_move("playerA", (1, 5), 'R'))
    print("Marble count: ",g.get_marble_count())
    """

    """
    #Win scenario test
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    print("White 0,0 move backward", game.make_move("PlayerA", (0, 0), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (0, 6), "B"))
    print("White 0,0 move backward", game.make_move("PlayerA", (1, 0), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (2, 6), "F"))
    print("White 0,0 move backward", game.make_move("PlayerA", (2, 0), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (0, 6), "B"))
    print("White 0,0 move backward", game.make_move("PlayerA", (3, 0), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (2, 6), "F"))
    print("White 0,0 move backward", game.make_move("PlayerA", (4, 0), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (0, 6), "B"))
    print("White 0,0 move backward", game.make_move("PlayerA", (0, 1), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (2, 6), "F"))
    print("White 0,0 move backward", game.make_move("PlayerA", (1, 1), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (0, 6), "B"))
    print("White 0,0 move backward", game.make_move("PlayerA", (2, 1), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (2, 6), "F"))
    print("White 0,0 move backward", game.make_move("PlayerA", (3, 1), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (0, 6), "B"))
    print("White 0,0 move backward", game.make_move("PlayerA", (4, 1), "B"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (2, 6), "F"))
    print("White 0,0 move backward", game.make_move("PlayerA", (6, 5), "F"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (0, 6), "B"))
    print("White 0,0 move backward", game.make_move("PlayerA", (5, 5), "F"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (2, 6), "F"))
    print("White 0,0 move backward", game.make_move("PlayerA", (4, 5), "F"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (0, 6), "B"))
    print("White 0,0 move backward", game.make_move("PlayerA", (3, 5), "F"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (2, 6), "F"))
    print("White 0,0 move backward", game.make_move("PlayerA", (2, 5), "F"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (0, 6), "B"))
    print("White 0,0 move backward", game.make_move("PlayerA", (1, 5), "R"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (2, 6), "F"))
    print("White 0,0 move backward", game.make_move("PlayerA", (6, 0), "F"))
    print("Black 0,6 move backward", game.make_move("PlayerB", (1, 6), "F"))
    print("White 0,0 move backward", game.make_move("PlayerA", (0, 5), "R"))
    print("Current winner: ",game.get_winner())
    """

    """
    # Reverse board state test
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    print("White 1,0 move right", game.make_move("PlayerA", (1, 0), "R"))
    print("Black 1,6 move left", game.make_move("PlayerB", (1, 6), "L"))
    print("White 1,1 move right", game.make_move("PlayerA", (1, 1), "R"))
    print("This should fail because it return board to previous state", game.make_move("PlayerB", (1, 6), "L"))
    print("Black 6,0 move forward", game.make_move("PlayerB", (6, 0), "F"))
    print("Get marble: ", game.get_marble((0, 0)))  # returns 'X'
    print("White 0,0 move backward", game.make_move("PlayerA", (0, 0), "B"))
    print("Black 1,6 move left", game.make_move("PlayerB", (1, 6), "L"))
    """
    """
    # Numerous move, capture, pushing oppponent off board tests
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    print("Get marble: ", game.get_marble((5, 5)))  # returns 'W'
    print(game.get_marble_count())
    print("Player A Captured", game.get_captured('PlayerA'))  # returns 0
    print(game.print_board(game.get_current_board()))
    print("White 0,0 move right", game.make_move("PlayerA", (0, 0), "R"))
    print("Black 0,5 move backward", game.make_move("PlayerB", (0, 5), "B"))
    print("White 0,1 move backward", game.make_move("PlayerA", (0, 1), "B"))
    print("Black 2,5 move left", game.make_move("PlayerB", (2, 5), "L"))
    print("White 2,0 move forward", game.make_move("PlayerA", (2, 0), "F"))
    print("Black 2,4 move left", game.make_move("PlayerB", (2, 4), "L"))
    print("White 0,0 move backward", game.make_move("PlayerA", (0, 0), "B"))
    print(game.get_marble_count())
    print("Black 2,3 move left", game.make_move("PlayerB", (2, 3), "L"))
    print(game.get_marble_count())
    print("White 5,6 move left", game.make_move("PlayerA", (5, 6), "L"))
    print(game.get_marble_count())
    print("Black 2,2 move left", game.make_move("PlayerB", (2, 2), "L"))
    print(game.get_marble_count())
    print("Player B Captured", game.get_captured('PlayerB'))  # returns 0
    print("White 5,5 move left", game.make_move("PlayerA", (5, 5), "L"))
    print("Black 2,1 move left", game.make_move("PlayerB", (2, 1), "L"))
    print("White 5,4 move left", game.make_move("PlayerA", (5, 4), "L"))
    print(game.get_marble_count())
    print("Current winner: ",game.get_winner())
    print("Black 5,0 move right", game.make_move("PlayerB", (5, 0), "R"))
    print("White 5,4 move left", game.make_move("PlayerA", (5, 4), "L"))
    #print("Get marble: ", game.get_marble((0, 2)))  # returns 'R'
    #print("White 0,1 move backward", game.make_move("PlayerA", (0, 1), "B"))
    #print("Get marble: ", game.get_marble((2, 0)))  # returns 'R'
    #print("Get marble: ", game.get_marble((0, 1)))  # returns 'X'
    #print("Get marble: ", game.get_marble((2, 5)))  # returns 'X'
    #print("Get marble: ", game.get_marble((2, 6)))  # returns 'X'
    # print(game.print_board(game.get_current_board()))
    """

