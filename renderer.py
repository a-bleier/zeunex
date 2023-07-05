import time

import numpy as np
import glfw
import OpenGL.GL as gl
import ctypes as ct


from shader import Shader
from gui import Gui
from shader_storage import ShaderStorage


import ipdb

MAX_BOARD_BUFFER_SIZE = 512*512

class Renderer:

  def __init__(self, width: int, height: int):
    self.width: int = width
    self.height: int = height

    # time delta in s
    self.delta = 1 / 30
    self.tick_delta = 0.5

    if not glfw.init():
      return
    # Create a windowed mode window and its OpenGL context
    self.window = glfw.create_window(self.width, self.height, "Hello World", None, None)

    if not self.window:
      glfw.terminate()
      return

    # Make the window's context current
    glfw.make_context_current(self.window)

    self.gui = Gui(self.window)
    self.center = (int(self.gui.width/2), int(self.gui.height/2))

    # program defining the graphics pipeline
    self.pipeline_shader = Shader("Pipeline",
                                 vertex_source="shaders/vertex.glsl",
                                 fragment_source="shaders/fragment.glsl")

    vertices = [
      -1.0, 1.0, 0.0,
      -1.0, -1.0, 0.0,
      1.0, -1.0, 0.0,

      1.0, 1.0, 0.0,
      -1.0, 1.0, 0.0,
      1.0, -1.0, 0.0,
    ]

    vertices = (gl.GLfloat * len(vertices))(*vertices)

    vbo = None
    vbo = gl.glGenBuffers(1, vbo)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

    # send the data  
    gl.glBufferData(gl.GL_ARRAY_BUFFER, ct.sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    # create vao object
    self.vao = None
    self.vao = gl.glGenVertexArrays(1, self.vao)

    # enable VAO and then finally binding to VBO object what we created before.
    gl.glBindVertexArray(self.vao)

    # we activated to the slot of position in VAO (vertex array object)
    gl.glEnableVertexAttribArray(0)

    # explaining to the VAO what data will be used for slot 0 (position slot)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * ct.sizeof(gl.GLfloat), ct.c_void_p(0))

    self.ssbo = ShaderStorage(MAX_BOARD_BUFFER_SIZE + 4*4, 1)
    self.ssbo.bind()
    self.ssbo.subData(self.gui.width, 0)
    self.ssbo.subData(self.gui.height, 1)
    self.ssbo.subData(100, 2)
    self.ssbo.subData(100, 3)
    self.ssbo.unbind()
    self.ssbo.bindBase()

  def render_loop(self, board):

    last_render = time.monotonic()
    last_tick = time.monotonic()

    while not glfw.window_should_close(self.window):
      # Poll for and process events

      glfw.poll_events()
      gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

      self.gui.process_input()

      now = time.monotonic()
      if now - last_tick > self.tick_delta:
        board.evolve()
        # TODO Check whether window (width, height), exceeds board boundary
        self.center = (board.board.shape[1]//2, board.board.shape[0]//2)
        board_data: np.ndarray = np.copy(board.board[int(self.center[1]-self.gui.height/2):int(self.center[1]+self.gui.height/2),
                                         int(self.center[0]-self.gui.width/2):int(self.center[0]+self.gui.width/2)])
        self.ssbo.subData(board_data, 4)
        if self.gui.changed:
          print(f"{self.gui.width}, {self.gui.height}")
          self.ssbo.subData(self.gui.width, 0)
          self.ssbo.subData(self.gui.height, 1)
          self.ssbo.subData(100, 2)
          self.ssbo.subData(100, 3)
          self.gui.changed = False

        last_tick = time.monotonic()

      now = time.monotonic()
      if now - last_render < self.delta:
        time.sleep(self.delta - now + last_render)

      self.render_board()
      self.gui.render()
      # Swap front and back buffers
      glfw.swap_buffers(self.window)
      last_render = time.monotonic()

      if self.gui.close_app:
        break

  def render_board(self):
    self.pipeline_shader.bind()
    gl.glBindVertexArray(self.vao)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 6)
    # self.pipeline_shader.unbind()

  def __reload_shaders(self):
    # TODO check if shader sources are null or have changed
    # TODO How and when to check changed shaders?
    with open("shaders/vertex.glsl", 'r') as f:
      self.vertex_shader_source = f.read()

    with open("shaders/fragment.glsl", 'r') as f:
      self.fragment_shader_source = f.read()

  def terminate(self):
    glfw.terminate()
