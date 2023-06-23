import numpy as np
from numpy.lib.stride_tricks import as_strided


class GameOfLifeKernel():

  def __init__(self):
    self.neighbors = np.zeros((1, 1))
    pass

  def __call__(self, board: np.ndarray) -> np.ndarray:
    if self.neighbors.shape != board.shape:
      self.neighbors = np.zeros(board.shape)
    y, x = board.shape[0:2]
    rel_board = board[1:y-1, 1:x-1]
    new_board = np.zeros_like(rel_board)
    nei = as_strided(board, shape=(y - 2, x - 2, 3, 3), strides=board.strides + board.strides)
    nei_counts = np.apply_over_axes(np.sum, nei, [2, 3]).reshape(y - 2, x - 2)
    nei = nei_counts - nei[:, :, 1, 1]
    new_board[(((nei==2) | (nei==3)) & (rel_board==1)) | ((nei==3) & (rel_board==0))] = 1
    board[1:y - 1, 1:x - 1] = new_board
    return board

  def reset(self, new_shape):
    self.neighbors = np.zeros(new_shape)

