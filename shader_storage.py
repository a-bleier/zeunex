import warnings
import ctypes as ct

import numpy as np
import OpenGL.GL as gl


class ShaderStorage:

  def __init__(self, size: int, index: gl.GLuint):
    self.capacity = size
    self.id = gl.glGenBuffers(1, gl.GL_SHADER_STORAGE_BUFFER)
    self.strides = [0]
    self.types = []
    self.index = index
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.id)
    gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, self.capacity, (gl.GLfloat * self.capacity)(*(self.capacity * [0])), gl.GL_STATIC_DRAW)
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

  def subData(self, data, index=None):
    if index is None:
      gl.glBufferSubData(gl.GL_SHADER_STORAGE_BUFFER, offset=0, size=self.capacity, data=data)
      return

    size = 0
    if isinstance(data, int):
      size = 4
      self.types.append(int)
      self.strides.append(self.strides[-1] + size)
      data = (gl.GLint * 1)(*[data])
    elif isinstance(data, float):
      size = 4
      self.types.append(float)
      self.strides.append(self.strides[-1] + size)
    elif isinstance(data, np.ndarray):
      size=4*data.size
      data=data.ctypes.data_as(ct.POINTER(ct.c_int32))
      self.strides.append(self.strides[-1] + size)
    # TODO: implement this for other types than int
    elif isinstance(data, list):
      # size = ct.sizeof(data)
      # self.types.append(list)
      warnings.warn("Lists not supported right now; use np.ndarray instead")
    else:
      warnings.warn(f"No SSBO support for object of type {type(data)}")
      return
    # TODO Check if element fits into the memory at the specified position at index

    if self.capacity < self.strides[index] + size:
      warnings.warn(f"Allocating new SSBO of size {self.capacity}; data has not been copied")
      return
    
    gl.glBufferSubData(gl.GL_SHADER_STORAGE_BUFFER, offset=self.strides[index], size=size, data=data)

  def bind(self):
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.id)

  def unbind(self):
    gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, 0)

  def bindBase(self):
    gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, self.index, self.id)

