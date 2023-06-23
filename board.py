import numpy as np
import kernel


class BinaryBoard():
  def __init__(self, width: int, height: int, kernel):
    self.width = width
    self.height = height

    self.board = np.zeros((height, width), dtype=np.int32)
    self.kernel = kernel

    self.history = []

  def resize(self, width: int, height: int):
    # Resets the board
    self.board = np.zeros((height, width), dtype=np.int32)
    self.kernel.reset(self.board.shape)
    self.width = width
    self.height = height

  def evolve(self, n=1, keep_history=False):
    """
    Evolves the board n steps
    """
    for i in range(n):
      if keep_history:
        self.history.append(self.board.copy())
      self.board = self.kernel(self.board)


if __name__ == "__main__":
  board = BinaryBoard(10, 10, kernel.GameOfLifeKernel())
  board.board[5, 5] = 1
  board.board[5, 6] = 1
  board.board[5, 4] = 1
  print(board.board[:])
  board.evolve(n=4)
  print(board.board[:])
