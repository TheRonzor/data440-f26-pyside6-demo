import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QSlider, QVBoxLayout, QWidget

def main() -> None:
    '''
    Simple demo app to adjust a threshold
    via a slider and display how many values
    are less than or equal to the threshold
    '''

    values = [12, 37, 42, 55, 67, 84]

    # Set up the application
    app = QApplication(sys.argv)

    # Set up the main window
    window = QWidget()
    window.setWindowTitle('Threshold Thingy')

    # Create a vertical layout and put it inside the window
    layout = QVBoxLayout(window)

    # Set up display components
    values_list = QLabel(f'Values: {values}')

    # Set up the slider
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(0, max(values)+10)
    slider.setValue(0)

    # Set up readouts
    threshold_label = QLabel('thresh')
    result_label = QLabel('result')

    def update_result(threshold: int) -> None:
        '''
        Update the readouts based on the 
        threshold provided.
        '''
        n = sum(value <= threshold for value in values)
        threshold_label.setText(f'Threshold: {threshold}')
        result_label.setText(f'Number of values <= {n}')
        return None

    # When the slider bar changes, call the function
    slider.valueChanged.connect(update_result)

    # Call the function once upon initialization
    update_result(slider.value())

    # Put the components in the layout
    layout.addWidget(values_list)
    layout.addWidget(slider)
    layout.addWidget(threshold_label)
    layout.addWidget(result_label)

    window.resize(420, 160)
    window.show()

    # Run the application
    app.exec()
    return None

if __name__ == '__main__':
    main()