import sys
from matplotlib.figure import Figure
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from src.pysidecomponents import WindowWithFigureAbove, FigureDisplayArea, ControlPanel, LabeledSpinBox

class VizDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fig_area = FigureDisplayArea()
        self.controls = ControlPanel()
        
        self.points_input = LabeledSpinBox("Data Points", 10, 500)
        btn = QPushButton("Generate Plot")
        btn.clicked.connect(self.plot_data)

        self.controls.add_widget(self.points_input)
        self.controls.add_widget(btn)

        self.layout_container = WindowWithFigureAbove(self.fig_area, self.controls)
        self.setCentralWidget(self.layout_container)
        self.resize(800, 600)

    def plot_data(self):
        n = self.points_input.get_value()
        fig = Figure()
        ax = fig.subplots()
        ax.plot(range(n), [i**2 for i in range(n)])
        ax.set_title(f"Parabola with {n} points")
        self.fig_area.update_matplotlib(fig)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = VizDemo()
    win.show()
    app.exec()
