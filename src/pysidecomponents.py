from typing import List, Optional, Union, Any, Tuple
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QSlider, QComboBox, QSpinBox, QGroupBox, QCheckBox, 
    QRadioButton, QProgressBar, QPushButton, QFrame, 
    QSplitter, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView

# --- Constants ---
# Default spacing and margins for layouts
DEFAULT_SPACING = 10
DEFAULT_MARGINS = 5

# Default stretch ratios for splitters
DEFAULT_STRETCH_FIGURE = 70
DEFAULT_STRETCH_CONTROLS = 30

# Orientation Constants
ORIENTATION_HORIZONTAL = Qt.Orientation.Horizontal
ORIENTATION_VERTICAL = Qt.Orientation.Vertical

# --- Simple Components ---

class LabeledInput(QWidget):
    '''
    A text input field paired with a label on its left.

    Inputs
        label_text:   The text to display in the label.
        default_text: The initial text inside the input field.
    '''
    valueChanged = Signal(str)

    def __init__(self, label_text: str, default_text: str = "") -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label_text)
        self.input_field = QLineEdit(default_text)
        
        # Connect internal signal to the custom unified signal
        self.input_field.textChanged.connect(self.valueChanged.emit)

        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        return None

    def get_value(self) -> str:
        '''
        Returns the current text in the input field.
        '''
        return self.input_field.text()


class LabeledSlider(QWidget):
    '''
    A slider with a name label and a live value display label.

    Inputs
        label_text:  The name of the parameter.
        min_val:     Minimum integer value.
        max_val:     Maximum integer value.
        orientation: Either ORIENTATION_HORIZONTAL or ORIENTATION_VERTICAL.
    '''
    valueChanged = Signal(int)

    def __init__(self, label_text: str, min_val: int, max_val: int, 
                 orientation: Qt.Orientation = ORIENTATION_HORIZONTAL) -> None:
        super().__init__()
        self.main_layout = QHBoxLayout(self) if orientation == ORIENTATION_HORIZONTAL else QVBoxLayout(self)
        
        self.name_label = QLabel(label_text)
        self.value_label = QLabel(str(min_val))
        self.slider = QSlider(orientation)
        self.slider.setRange(min_val, max_val)

        # Update the value label whenever the slider moves
        self.slider.valueChanged.connect(self._update_label)
        self.slider.valueChanged.connect(self.valueChanged.emit)

        if orientation == ORIENTATION_HORIZONTAL:
            self.main_layout.addWidget(self.name_label)
            self.main_layout.addWidget(self.slider)
            self.main_layout.addWidget(self.value_label)
        else:
            # Vertical: value on top, name on bottom
            self.main_layout.addWidget(self.value_label, alignment=Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return None

    def _update_label(self, value: int) -> None:
        '''
        Internal helper to sync the text label with the slider value.
        '''
        self.value_label.setText(str(value))
        return None

    def get_value(self) -> int:
        '''
        Returns the current integer value of the slider.
        '''
        return self.slider.value()


class LabeledComboBox(QWidget):
    '''
    A dropdown selection box with a label on the left.

    Inputs
        label_text: The text to display in the label.
        items:      A list of strings to populate the dropdown.
    '''
    selectionChanged = Signal(str)

    def __init__(self, label_text: str, items: List[str]) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        
        self.label = QLabel(label_text)
        self.combo = QComboBox()
        self.combo.addItems(items)
        
        self.combo.currentTextChanged.connect(self.selectionChanged.emit)

        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        return None

    def get_value(self) -> str:
        '''
        Returns the currently selected string.
        '''
        return self.combo.currentText()


class LabeledSpinBox(QWidget):
    '''
    A numeric spinbox with a label on the left.

    Inputs
        label_text: The text to display in the label.
        min_val:    Minimum integer value.
        max_val:    Maximum integer value.
    '''
    valueChanged = Signal(int)

    def __init__(self, label_text: str, min_val: int, max_val: int) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        
        self.label = QLabel(label_text)
        self.spin = QSpinBox()
        self.spin.setRange(min_val, max_val)
        
        self.spin.valueChanged.connect(self.valueChanged.emit)

        layout.addWidget(self.label)
        layout.addWidget(self.spin)
        return None

    def get_value(self) -> int:
        '''
        Returns the current numeric value.
        '''
        return self.spin.value()


class CheckBoxGroup(QGroupBox):
    '''
    A titled group of checkboxes.

    Inputs
        title:   The title of the group box.
        options: A list of strings, each representing a checkbox.
    '''
    stateChanged = Signal(list)

    def __init__(self, title: str, options: List[str]) -> None:
        super().__init__(title)
        self.layout_inner = QVBoxLayout(self)
        self.checkboxes = []

        for opt in options:
            cb = QCheckBox(opt)
            cb.stateChanged.connect(self._emit_checked_list)
            self.layout_inner.addWidget(cb)
            self.checkboxes.append(cb)
        return None

    def _emit_checked_list(self) -> None:
        '''
        Internal helper to emit the full list of currently selected items.
        '''
        self.stateChanged.emit(self.get_selected())
        return None

    def get_selected(self) -> List[str]:
        '''
        Returns a list of labels for all checked boxes.
        '''
        return [cb.text() for cb in self.checkboxes if cb.isChecked()]


class RadioButtonGroup(QGroupBox):
    '''
    A titled group of mutually exclusive radio buttons.

    Inputs
        title:   The title of the group box.
        options: A list of strings, each representing a radio button.
    '''
    selectionChanged = Signal(str)

    def __init__(self, title: str, options: List[str]) -> None:
        super().__init__(title)
        self.layout_inner = QVBoxLayout(self)
        self.buttons = []

        for i, opt in enumerate(options):
            rb = QRadioButton(opt)
            if i == 0: rb.setChecked(True) # Ensure one is always selected
            rb.toggled.connect(self._emit_selection)
            self.layout_inner.addWidget(rb)
            self.buttons.append(rb)
        return None

    def _emit_selection(self, checked: bool) -> None:
        '''
        Internal helper to emit only the newly selected button text.
        '''
        if checked:
            self.selectionChanged.emit(self.get_selected())
        return None

    def get_selected(self) -> str:
        '''
        Returns the label of the currently selected radio button.
        '''
        for rb in self.buttons:
            if rb.isChecked():
                return rb.text()
        return ""


class StatusBarSimple(QLabel):
    '''
    A simple status display area for text messages.
    '''
    def __init__(self) -> None:
        super().__init__("Ready")
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        return None

    def show_message(self, message: str) -> None:
        '''
        Updates the status bar with the provided message.

        Inputs
            message: The string to display.
        '''
        self.setText(message)
        return None


class ProgressBar(QWidget):
    '''
    A wrapper for a progress bar that handles values from 0.0 to 1.0.
    '''
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        layout.addWidget(self.bar)
        return None

    def set_progress(self, value: float) -> None:
        '''
        Updates the progress bar.

        Inputs
            value: A float between 0.0 and 1.0.
        '''
        percentage = int(value * 100)
        self.bar.setValue(percentage)
        return None

# --- Composite Components ---

class TwoPanelLayout(QWidget):
    '''
    A container that splits the space between two widgets.

    Inputs
        panel_1:     The first (top/left) widget.
        panel_2:     The second (bottom/right) widget.
        orientation: ORIENTATION_HORIZONTAL or ORIENTATION_VERTICAL.
        ratios:      A tuple of two ints representing the stretch factors.
    '''
    def __init__(self, panel_1: QWidget, panel_2: QWidget, 
                 orientation: Qt.Orientation = ORIENTATION_HORIZONTAL,
                 ratios: Tuple[int, int] = (1, 1)) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        self.splitter = QSplitter(orientation)
        
        self.splitter.addWidget(panel_1)
        self.splitter.addWidget(panel_2)
        
        # Set stretch factors based on ratios input
        self.splitter.setStretchFactor(0, ratios[0])
        self.splitter.setStretchFactor(1, ratios[1])
        
        layout.addWidget(self.splitter)
        return None


class ControlPanel(QFrame):
    '''
    A container for organizing various control widgets.
    '''
    def __init__(self) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.layout_inner = QVBoxLayout(self)
        self.layout_inner.setAlignment(Qt.AlignmentFlag.AlignTop)
        return None

    def add_widget(self, widget: QWidget) -> None:
        '''
        Adds a widget to the control panel.

        Inputs
            widget: The widget to be added.
        '''
        self.layout_inner.addWidget(widget)
        return None


class FigureDisplayArea(QWidget):
    '''
    A widget designed to render various types of figure content.
    '''
    def __init__(self) -> None:
        super().__init__()
        self.layout_main = QVBoxLayout(self)
        self.content_widget: Optional[QWidget] = None
        self.clear()
        return None

    def _clear_layout(self) -> None:
        '''
        Removes the current content widget from the layout.
        '''
        if self.content_widget is not None:
            self.layout_main.removeWidget(self.content_widget)
            self.content_widget.deleteLater()
            self.content_widget = None
        return None

    def _set_content(self, widget: QWidget) -> None:
        '''
        Replaces the current display widget.
        '''
        self._clear_layout()
        self.content_widget = widget
        self.layout_main.addWidget(self.content_widget)
        return None

    def clear(self) -> None:
        '''
        Restores the default empty display.
        '''
        placeholder = QLabel("Figure Display Area")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_content(placeholder)
        return None

    def update_image(self, file_path: str) -> None:
        '''
        Displays a static image.

        Inputs
            file_path: Path to the image file.
        '''
        image_label = QLabel()
        pixmap = QPixmap(file_path)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        self._set_content(image_label)
        return None

    def update_matplotlib(self, figure: Figure) -> None:
        '''
        Displays a Matplotlib figure.

        Inputs
            figure: A Matplotlib figure object.
        '''
        self._set_content(FigureCanvas(figure))
        return None

    def update_plotly(self, html_content: str) -> None:
        '''
        Displays Plotly content via HTML.

        Inputs
            html_content: The HTML string representing the Plotly figure.
        '''
        web_view = QWebEngineView()
        web_view.setHtml(html_content)
        self._set_content(web_view)
        return None


class WindowWithFigureAbove(TwoPanelLayout):
    '''
    A vertical layout with a figure area on top and controls below.

    Inputs
        figure_area:   The FigureDisplayArea widget.
        control_panel: The ControlPanel (or other) widget.
        ratios:        The stretch ratio (Figure, Control).
    '''
    def __init__(self, figure_area: QWidget, control_panel: QWidget, 
                 ratios: Tuple[int, int] = (DEFAULT_STRETCH_FIGURE, DEFAULT_STRETCH_CONTROLS)) -> None:
        super().__init__(figure_area, control_panel, ORIENTATION_VERTICAL, ratios)
        return None


class ButtonRow(QWidget):
    '''
    A horizontal row of buttons.

    Inputs
        button_labels: A list of strings for button text.
    '''
    buttonClicked = Signal(str)

    def __init__(self, button_labels: List[str]) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        for label in button_labels:
            btn = QPushButton(label)
            # Use lambda to pass the label string to the signal
            btn.clicked.connect(lambda checked=False, l=label: self.buttonClicked.emit(l))
            layout.addWidget(btn)
        return None


class ButtonBox(QWidget):
    '''
    A vertical container holding multiple ButtonRows.
    '''
    def __init__(self) -> None:
        super().__init__()
        self.layout_inner = QVBoxLayout(self)
        self.layout_inner.setContentsMargins(0, 0, 0, 0)
        return None

    def add_row(self, row: ButtonRow) -> None:
        '''
        Adds a ButtonRow to the box.

        Inputs
            row: A ButtonRow instance.
        '''
        self.layout_inner.addWidget(row)
        return None


class CollapsibleSection(QWidget):
    '''
    A section with a toggleable header to show or hide its content.

    Inputs
        title:   The text shown on the toggle button.
        content: The widget to be collapsed/expanded.
    '''
    def __init__(self, title: str, content: QWidget) -> None:
        super().__init__()
        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)

        self.toggle_btn = QPushButton(f"▼ {title}")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(True)
        self.toggle_btn.clicked.connect(self.toggle)

        self.content = content
        
        self.layout_main.addWidget(self.toggle_btn)
        self.layout_main.addWidget(self.content)
        return None

    def toggle(self) -> None:
        '''
        Switches between expanded and collapsed states.
        '''
        is_visible = self.content.isVisible()
        self.content.setVisible(not is_visible)
        
        # Update button arrow indicator
        prefix = "▼" if not is_visible else "▶"
        # We assume the label starts after the arrow and space
        clean_title = self.toggle_btn.text()[2:]
        self.toggle_btn.setText(f"{prefix} {clean_title}")
        return None
