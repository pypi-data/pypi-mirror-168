#####################
# DataInputForm - a simple, consistent interface for basic data input screens
#####################

from . import fmActionFormV2

class DataInputForm(fmActionFormV2.ActionFormV2):
    MOVEMENT_HELP = """Cursor movement:
        arrow keys: up, down, left, right - move between and within fields
        Space, Enter, click: select item
        Tab, Backtab: move to next/previous field
        """

    def __init__(self, help='', left_button_text="Cancel", right_button_text="OK"):
        self.help = help + self.MOVEMENT_HELP
        self.CANCEL_BUTTON_TEXT = left_button_text
        self.OK_BUTTON_TEXT = right_button_text
        #self.parentApp = parentApp
        super().__init__()

    # always use next editable field, don't re-arrange them as the base code does
    def pre_edit_loop(self):
        if not self.preserve_selected_widget:
            self.editw = 0
        if not self._widgets__[self.editw].editable:
            self.find_next_editable()

