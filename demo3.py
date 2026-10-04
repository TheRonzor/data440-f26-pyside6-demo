import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from src.pysidecomponents import TwoPanelLayout, CollapsibleSection, ButtonBox, ButtonRow, ORIENTATION_HORIZONTAL

class LayoutDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Layouts")

        # Left Panel: Collapsible buttons
        row1 = ButtonRow(["Save", "Load"])
        row2 = ButtonRow(["Clear", "Reset"])
        bbox = ButtonBox()
        bbox.add_row(row1)
        bbox.add_row(row2)

        collapse = CollapsibleSection("File Operations", bbox)
        
        # Right Panel: Text Area
        self.log = QTextEdit("Activity Log...")

        # Combine into horizontal split
        self.main_split = TwoPanelLayout(collapse, self.log, ORIENTATION_HORIZONTAL, ratios=(1, 3))
        self.setCentralWidget(self.main_split)
        
        row1.buttonClicked.connect(lambda b: self.log.append(f"Clicked: {b}"))
        row2.buttonClicked.connect(lambda b: self.log.append(f"Clicked: {b}"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LayoutDemo()
    win.show()
    app.exec()
