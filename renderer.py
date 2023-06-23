import time

import numpy as np
import glfw
import OpenGL.GL as gl
import ctypes as ct

import imgui
from imgui.integrations.glfw import GlfwRenderer

from shader import Shader


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

    imgui.create_context()
    self.impl = GlfwRenderer(self.window)

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

    # ssbo test
    self.ssbo = None
    self.ssbo = gl.glGenBuffers(1, gl.GL_SHADER_STORAGE_BUFFER)
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.ssbo)
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 1, self.ssbo)
    dummy_data = np.zeros((104), dtype=np.int32)
    dummy_data[0] = 10
    dummy_data[1] = 10
    dummy_data[2] = 100
    dummy_data[3] = 100
    gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER,
                    size=ct.sizeof(gl.GLint) * len(dummy_data),
                    data=dummy_data.ctypes.data_as(ct.POINTER(ct.c_int32)),
                    usage=gl.GL_STATIC_READ)

  def render_loop(self, board):

    last_render = time.monotonic()
    last_tick = time.monotonic()

    while not glfw.window_should_close(self.window):
      # Poll for and process events

      glfw.poll_events()
      gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

      self.impl.process_inputs()

      now = time.monotonic()
      if now - last_tick > self.tick_delta:
        board.evolve()
        board_data = board.board
        gl.glBufferSubData(gl.GL_SHADER_STORAGE_BUFFER,
                         offset=4 * ct.sizeof(gl.GLint),
                         size=ct.sizeof(gl.GLint) * 100,
                         data=board_data.ctypes.data_as(ct.POINTER(ct.c_int32)))
        last_tick = time.monotonic()

      now = time.monotonic()
      if now - last_render < self.delta:
        time.sleep(self.delta - now + last_render)

      self.render_board()
      self.render_imgui()
      # Swap front and back buffers
      glfw.swap_buffers(self.window)
      last_render = time.monotonic()

  def render_imgui(self):
    imgui.new_frame()
    imgui.begin("Your first window!", True)
    imgui.text("Hello world!")
    # close current window context
    imgui.end()
    imgui.end_frame()
    imgui.render()
    self.impl.render(imgui.get_draw_data())

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
