from __future__ import annotations

import matplotlib.pyplot as plt
from .observer_utils import Observable
from matplotlib.widgets import TextBox 


class UIComponents(Observable):
    def __init__(self, ax: plt.Axes):
        super().__init__()
        self.ax = ax
        self.fig = ax.figure
        self.buttons: dict[str, dict[str, plt.Axes | str | function]] = {
            "switch": {
                "axis": self.fig.add_axes([0.01, 0.01, 0.20, 0.05]),
                "label": "Switch to Drones",
                "callback": self.on_switch_mode,
            },
            "reset": {
                "axis": self.fig.add_axes([0.22, 0.01, 0.1, 0.05]),
                "label": "Reset",
                "callback": self.on_reset,
            },
            "create_json": {
                "axis": self.fig.add_axes([0.33, 0.01, 0.15, 0.05]),
                "label": "Create JSON",
                "callback": self.on_json,
            },
            "load_json": {
                "axis": self.fig.add_axes([0.49, 0.01, 0.15, 0.05]),
                "label": "Load JSON",
                "callback": self.on_load,
            },
        }

        # Initialize buttons and register callbacks
        for key, btn_info in self.buttons.items():
            button = plt.Button(btn_info["axis"], btn_info["label"])
            button.on_clicked(btn_info["callback"])
            self.buttons[key]["button"] = button

        #create textbox, color is (r,g,b,alpha)
        self.axbox = self.fig.add_axes([0.72, 0.01, 0.2, 0.05])
        self.text_box = EnterTextBox(self.axbox, "Path:",
                                label_pad = 0.1, 
                                textalignment="left",
                                hovercolor=(0,1,0,0.2))
        
        self.text_box.on_submit(self.on_text_box)
        self.text_box.on_submit
        self.text_box.set_val("")  # Trigger `submit` with the initial string.

    def submit(self, text: str) -> None:
        # self.notify_observers("evaluate", text)
        print(text)

    def rename_button(self, button_key: str, new_label: str) -> None:
        if button_key in self.buttons:
            self.buttons[button_key]["button"].label.set_text(new_label)
        else:
            raise ValueError(f"No button found with the key '{button_key}'")

    def on_switch_mode(self, event):
        self.notify_observers("switch_mode")

    def on_reset(self, event):
        self.notify_observers("reset")

    def on_json(self, event):
        self.notify_observers("create_json")

    def on_load(self,event):
        self.notify_observers("load_json", input = self.text_box.text)

    def on_text_box(self, text):
        self.notify_observers('text_box_submit', input=text)



class EnterTextBox(TextBox):
    def stop_typing(self, event=None):
        """
        Override the default behavior to not submit when focus is lost.
        ie don't submit when clicking outside of the textbox,
        only submit if enter is pressed
        """
        self.capturekeystrokes = False
        self.cursor.set_visible(False)
        self.ax.figure.canvas.draw()
        pass

    def _submit(self, event):
        if event.key == 'enter':
            super()._submit(event)