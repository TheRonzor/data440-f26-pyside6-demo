import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from src.pysidecomponents import LabeledSlider, LabeledComboBox, RadioButtonGroup, StatusBarSimple

class InputDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Dashboard")
        central = QWidget()
        layout = QVBoxLayout(central)

        self.status = StatusBarSimple()
        self.slider = LabeledSlider("Brightness", 0, 100)
        self.combo = LabeledComboBox("Theme", ["Light", "Dark", "High Contrast"])
        self.radio = RadioButtonGroup("Mode", ["Manual", "Auto", "Override"])

        # Connect signals to status bar
        self.slider.valueChanged.connect(lambda v: self.status.show_message(f"Slider: {v}"))
        self.combo.selectionChanged.connect(lambda s: self.status.show_message(f"Selected: {s}"))
        self.radio.selectionChanged.connect(lambda r: self.status.show_message(f"Mode: {r}"))

        layout.addWidget(self.slider)
        layout.addWidget(self.combo)
        layout.addWidget(self.radio)
        layout.addWidget(self.status)
        self.setCentralWidget(central)
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = InputDemo()
    win.show()
    app.exec()
