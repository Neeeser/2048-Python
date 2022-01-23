#!/usr/bin/env python
# Modular 2048 game written in python using a 2D array

import random
from colour import Color as Color
import sys


class Tile:

    def __init__(self, value=2 if random.randint(0, 10) < 9 else 4): # Random choose value 90% 2 10% 4 # Private
        self.__value = value
        self.__color = Color("brown")  # TODO not sure what I am going to use this for yet...

    def __repr__(self):
        return repr(self.__value)

    def __str__(self):
        return str(self.__value)

    # Asks the tile if it can merge with another tile
    def canmerge(self, mergetile):
        return mergetile.getvalue() == self.__value

    def getvalue(self):
        return self.__value

    def merge(self, mergetile):
        self.__value += mergetile.getvalue()


class Board:
    def __init__(self, width, height):
        # Tile location is based on [row, column]
        # Creates board that is filled with None (empty spaces) for the width given and the height given
        self.__grid = [[Tile(0)]*width for _ in range(height)]  # Private
        self.__width = self.__grid.__len__()
        self.__height = self.__grid[0].__len__()
        self.__playing = True  # Private

    # Prints out the board in a neat way
    def printgrid(self):
        for row in self.__grid:
            for column in row:
                print("[" + str(column) + "]", end='')
            print("\n")

    # A new tile at column
    def newtile(self, column, row):
        self.__grid[column][row] = Tile()

    def getplayingstatus(self):
        return self.__playing

    def allemptytiles(self):
        emptytiles = []
        for i in range(self.__height):
            for c in range(self.__width):
                if self.__grid[i][c].getvalue() == 0:
                    emptytiles.append([i, c])
        return emptytiles

    def newrandomtile(self):
        # Basically if the board has no more empty tiles then you lose
        if not self.allemptytiles():
            self.__playing = False
        else:
            randomtile = random.choice(self.allemptytiles())
            # random 0 get x randomtile get y
            self.__grid[randomtile[0]][randomtile[1]] = Tile()

    # def move(self, row):
    #     success = False
    #     col = 0
    #     # Check from left to right for 2 of the same tiles
    #     while col <= self.__width-1:
    #         if self.__grid[row][col] is not None:
    #             # 	If the same tile value
    #             if col+1 < self.__grid[row].__len__() and self.__grid[row][col].canmerge(self.__grid[row][col+1]):
    #                 # merge
    #                 self.__grid[row][col+1].merge(self.__grid[row][col])
    #                 self.__grid[row][col] = None
    #                 success = True
    #             # If last space was null
    #             elif col + 1 < self.__grid[row].__len__() and self.__grid[row][col+1] is None:
    #                 # Move tile left
    #                 self.__grid[row][col+1] = self.__grid[row][col]
    #                 self.__grid[row][col] = None
    #                 success = True
    #         col += 1
    #     return success
    #
    # def move(self, row):
    #     success = False
    #     col = len(self.__grid[0])-2
    #     while col >= 0:
    #         if(self.__grid[row][col]).getvalue() != 0:
    #             tile = col
    #             while self.__grid[row][tile+1].getvalue() != 0 or tile < self.__width:
    #                 if self.__grid[row][tile+1] is None:
    #                     self.__grid[row][tile + 1] = self.__grid[row][tile]
    #                     self.__grid[row][tile] = None
    #                     success = True
    #                 if self.__grid[row][tile].canmerge(self.__grid[row][tile+1]):
    #                     self.__grid[row][tile + 1].merge(self.__grid[row][tile])
    #                     self.__grid[row][tile] = None
    #                     success = True
    #                 tile += 1
    #         col -= 1
    #     return success

    def move(self, row):
        col = len(self.__grid[0])-2
        succes = False
        for tile in range(len(self.__grid[0])-1):
            if tile == 0:
                continue
            if self.__grid[row][tile].canmerge(self.__grid[row][tile + 1]):
                self.__grid[row][tile + 1].merge(self.__grid[row][tile])
                self.__grid[row][tile] = Tile(0)
                succes = True
        tile = col
        while(tile >= 0):
            if self.__grid[row][tile+1].getvalue() == 0 and self.__grid[row][tile].getvalue() is not 0:
                self.__grid[row][tile+1] = self.__grid[row][tile]
                self.__grid[row][tile] = Tile(0)
                if tile < col:
                    if self.__grid[row][tile+1].canmerge(self.__grid[row][tile+2]):
                        self.__grid[row][tile+2].merge(self.__grid[row][tile +1])
                        self.__grid[row][tile + 1] = Tile(0)
                        succes = True
                tile += 1
            tile -= 1



        return succes



    def right(self):
        success = False
        for i in range(self.__height):
            success = self.move(i)
        return success

    def left(self):
        success = False
        for i in range(2):
            self.rotateclockwise()
        for i in range(self.__height):
            success = self.move(i)
        for i in range(2):
            self.rotateclockwise()
        return success

    def up(self):
        success = False
        self.rotateclockwise()
        for i in range(self.__height):
            success = self.move(i)
        self.rotatecounter()
        return success

    def down(self):
        success = False
        self.rotatecounter()
        for i in range(self.__height):
            success = self.move(i)
        self.rotateclockwise()
        return success

    def rotateclockwise(self):
        rotate = list(zip(*reversed(self.__grid)))
        self.__grid = list([list(element) for element in rotate])

    def rotatecounter(self):
        rotate = list(zip(*reversed(self.__grid)))
        self.__grid = list([list(element)[::-1] for element in rotate][::-1])


class Game:
    def newgame(self):
        gametype = input("Game type (normal/debug): ")
        if gametype == "normal":
            self.normalgame()
        elif gametype == "debug":
            self.debuggame()
        else:
            print("Choose the type of game")
            self.newgame()

    def normalgame(self):
        board = Board(3, 3)
        board.newrandomtile()
        board.printgrid()
        while board.getplayingstatus() is True:
            move = input("Move: ")
            if "left" in move.lower():
                board.left()
            elif "right" in move.lower():
                board.right()
            elif "up" in move.lower():
                board.up()
            elif "down" in move.lower():
                board.down()
            board.newrandomtile()
            board.printgrid()

    def debuggame(self):
        board = Board(3,3)
        board.printgrid()
        while board.getplayingstatus() is True:
            move = input("Move (direction / row,column): ")
            print("\n")
            if "left" in move.lower():
                board.left()
            elif "right" in move.lower():
                board.right()
            elif "up" in move.lower():
                board.up()
            elif "down" in move.lower():
                board.down()
            else:
                row, column = move.split(",")


                board.newtile(int(row),int(column))
            board.printgrid()





game = Game()
game.newgame()
