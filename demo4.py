import sys
# We import QFileDialog only for the functional pop-up, not for UI layout construction.
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from src.pysidecomponents import (
    WindowWithFigureAbove, 
    FigureDisplayArea, 
    ControlPanel, 
    ButtonRow,
    StatusBarSimple
)

class ImagePickerApp(QMainWindow):
    '''
    An application that uses a system file dialog to load images into 
    the FigureDisplayArea, using only library components for the UI.
    '''

    def __init__(self) -> None:
        '''
        Sets up the UI using the pysidecomponents library.
        '''
        super().__init__()
        self.setWindowTitle("Library Demo: Standard File Dialog")
        self.resize(1000, 800)

        # 1. Create the Figure Display Area (Top Panel)
        self.display = FigureDisplayArea()

        # 2. Create the Control Panel (Bottom Panel)
        self.controls = ControlPanel()

        # 3. Create a ButtonRow for the browse and clear actions
        self.actions = ButtonRow(["Browse for Image...", "Clear Display"])

        # 4. Create a StatusBarSimple to show the file path currently loaded
        self.path_status = StatusBarSimple()

        # 5. Add our components to the Control Panel
        self.controls.add_widget(self.actions)
        self.controls.add_widget(self.path_status)

        # 6. Assemble the window using the WindowWithFigureAbove composite layout
        # This keeps the display area at 70% and the controls at 30% by default.
        self.main_layout = WindowWithFigureAbove(self.display, self.controls)
        self.setCentralWidget(self.main_layout)

        # 7. Connect the button signal to our handler
        self.actions.buttonClicked.connect(self.on_button_click)
        return None

    def on_button_click(self, button_text: str) -> None:
        '''
        Handles logic for the ButtonRow actions.

        Inputs
            button_text: The label of the button that was clicked.
        '''
        if button_text == "Browse for Image...":
            # Launch the standard system file dialog
            # This is a functional call, not a layout widget
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Open Image File", 
                "", 
                "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.svg)"
            )

            # If the user selected a file (didn't cancel), update the display
            if file_path:
                self.display.update_image(file_path)
                self.path_status.show_message(f"Loaded: {file_path}")

        elif button_text == "Clear Display":
            # Clear the display and reset the status
            self.display.clear()
            self.path_status.show_message("Ready")

        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImagePickerApp()
    window.show()
    app.exec()
