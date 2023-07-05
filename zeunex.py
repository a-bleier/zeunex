from renderer import Renderer
import kernel
import board


class App:

  def __init__(self):
    self.renderer = Renderer(1280, 720)
    self.board = board.BinaryBoard(10, 10, kernel.GameOfLifeKernel())
    self.board.board[5, 4] = 1
    self.board.board[5, 5] = 1
    self.board.board[5, 6] = 1
    self.board.board[6, 6] = 1
    self.board.board[7, 4] = 1

    self.gui = self.renderer.gui
    self.gui.width = 10
    self.gui.height = 10

  def start(self):
    self.renderer.render_loop(self.board)
    self.renderer.terminate()
