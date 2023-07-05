import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer


class Gui:

  def __init__(self, gl_window):
    imgui.create_context()
    self.impl = GlfwRenderer(gl_window)
    self.close_app = False
    self.file_menu_opened = False

    # width and height of the visible part of the board
    self.width: int = 10
    self.height: int = 10

    self.changed: bool = False

  def process_input(self):
    self.impl.process_inputs()

  def render(self):
    imgui.new_frame()

    imgui.begin("Zeunex", flags=imgui.WINDOW_MENU_BAR)
    with imgui.begin_menu_bar() as menu_bar:
      if menu_bar.opened:
        with imgui.begin_menu("File") as file_menu:
          if file_menu.opened:
            self.file_menu_opened |= imgui.menu_item("Load")[0]
            self.close_app = imgui.menu_item("Close")[0]
    imgui.text("Hello world!")

    changed_w, self.width = imgui.input_int("Width", self.width)
    changed_h, self.height = imgui.input_int("height", self.height)
    self.changed = self.changed or changed_h or changed_w

    # TODO resolution menu
    imgui.end()

    if self.file_menu_opened:
      # TODO file menu to load patterns
      imgui.begin("Open", flags=imgui.WINDOW_MENU_BAR)
      imgui.end()

    # close current window context
    imgui.end_frame()
    imgui.render()
    self.impl.render(imgui.get_draw_data())

