from enum import Enum
import glfw
import os
import OpenGL.GL as gl


class ShaderType(Enum):
  UNDEFINED = 1,
  RENDER_PIPELINE = 2,
  COMPUTE = 3


class Shader():
  def __init__(self, name: str, vertex_source=None, fragment_source=None, compute_source=None):
    self.name = name
    self.id = 0

    self.shader_type: ShaderType = ShaderType.UNDEFINED

    self.sources = {}
    self.timestamps = {}
    self.setSource(gl.GL_VERTEX_SHADER, vertex_source)
    self.setSource(gl.GL_FRAGMENT_SHADER, fragment_source)
    self.setSource(gl.GL_COMPUTE_SHADER, compute_source)
    self.compile()

  def __del__(self):
    self.clear()

  def clear(self):
    if gl.glIsProgram(self.id) == gl.GL_TRUE:
      gl.glDeleteProgram(id)
    self.id = 0
    self.sources = {}
    self.timestamps = {}
    self.shader_type = ShaderType.UNDEFINED

  def setSource(self, type: gl.GLenum, source: str):
    if source is None:
      return

    if type in [gl.GL_VERTEX_SHADER, gl.GL_FRAGMENT_SHADER] and self.shader_type != ShaderType.COMPUTE:
      self.sources[type] = source
      self.shader_type = ShaderType.RENDER_PIPELINE
    elif type == gl.GL_COMPUTE_SHADER and self.shader_type != ShaderType.RENDER_PIPELINE:
      self.sources[type] = source
      self.shader_type = ShaderType.COMPUTE
    else:
      print("Shader type and source not compatible")

  def compile(self):
    program = gl.glCreateProgram()
    for type, source in self.sources.items():
      shader = self.__compileShader(type, source)
      if shader == 0:
        gl.glDeleteProgram(program)
        return
      gl.glAttachShader(program, shader)

    gl.glLinkProgram(program)
    linkOk = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
    if linkOk != gl.GL_TRUE:
      print("Failed to link shader")
      return
    self.id = program

  def __compileShader(self, type, source_file):
    print(f"Loading {source_file} ...")
    with open(source_file, 'r') as f:
      source = f.read()
    self.timestamps[type] = os.path.getmtime(source_file)
    shader = gl.glCreateShader(type)
    gl.glShaderSource(shader, source)
    gl.glCompileShader(shader)

    status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
    if status != gl.GL_TRUE:
      print("Failed to compile shader")
      # TODO print meaningful error message
      gl.glDeleteShader(shader)
      return 0
    return shader

  def reload(self):
    for type, source in self.sources.items():
      if os.path.getmtime(source) != self.timestamps[type]:
        compile()
        return

  def bind(self):
    gl.glUseProgram(self.id)

  def unbind(self):
    gl.glUseProgram(0)


if __name__ == "__main__":
  if not glfw.init():
    exit(1)

  # Create a windowed mode window and its OpenGL context
  window = glfw.create_window(100, 100, "Hello World", None, None)

  if not window:
    glfw.terminate()
    exit(1)

  # Make the window's context current
  glfw.make_context_current(window)

  # imgui.create_context()
  # impl = GlfwRenderer(window)

  program = Shader("Test shader", vertex_source="shaders/vertex.glsl", fragment_source="shaders/fragment.glsl")
  program.compile()
