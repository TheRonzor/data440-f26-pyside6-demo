# Reusable PySide6 Components

A small collection of PySide6 widgets and layout components for assembling
desktop interfaces in Python. The examples are intentionally compact: they are
teaching demos, not production-ready applications.

The main design idea is **composition**. Each class handles one part of an
interface, and application code combines those parts and connects their signals
to ordinary Python functions.

## Run the examples

Use the project's existing Python environment from the repository root:

```bash
uv run demo1.py
uv run demo2.py
uv run demo3.py
uv run demo4.py
```

`live_demo.py` (we will build in class) is a short example built directly from standard PySide6
widgets. The numbered demos use the reusable components in
`src/pysidecomponents.py`.

## A useful mental model

A small PySide6 application can be understood as four interacting pieces:

- **State:** the data the application currently knows.
- **Widgets:** visible or interactive objects such as labels, sliders, and
  buttons.
- **Layouts:** rules that arrange widgets and respond to window resizing.
- **Signals and slots:** connections that say what function should run when an
  event occurs.

For example:

```text
user moves a slider
        ↓
the slider emits valueChanged
        ↓
a connected Python function runs
        ↓
the interface displays the new result
```

Every widget application also creates one `QApplication` and calls
`app.exec()` to start Qt's event loop. Unlike a script that runs from top to
bottom and exits, a GUI spends most of its time waiting for events.

## Component menu

| Component | Purpose |
|---|---|
| `LabeledInput` | Label plus a single-line text input |
| `LabeledSlider` | Label, integer slider, and live value display |
| `LabeledComboBox` | Label plus a dropdown selection |
| `LabeledSpinBox` | Label plus an integer spin box |
| `CheckBoxGroup` | Group of independent checkbox choices |
| `RadioButtonGroup` | Group of mutually exclusive choices |
| `StatusBarSimple` | Lightweight text status display |
| `ProgressBar` | Progress display accepting values from 0.0 to 1.0 |
| `TwoPanelLayout` | Resizable horizontal or vertical two-panel container |
| `ControlPanel` | Vertical container for application controls |
| `FigureDisplayArea` | Static image, Matplotlib figure, or HTML display |
| `WindowWithFigureAbove` | Figure area above a control panel |
| `ButtonRow` | Horizontal buttons with one unified signal |
| `ButtonBox` | Vertical collection of button rows |
| `CollapsibleSection` | Expandable container for another widget |

## Demo map

| File | Main ideas |
|---|---|
| `live_demo.py` | Raw widgets, layout, state, and a slider signal |
| `demo1.py` | Reusable inputs, custom signals, and status updates |
| `demo2.py` | Control-panel composition and embedded Matplotlib |
| `demo3.py` | Splitters, button rows, and collapsible content |
| `demo4.py` | Loading an image with a system file dialog |

## Minimal component example

The component module is imported as `src.pysidecomponents` when examples run
from the repository root:

```python
import sys

from PySide6.QtWidgets import QApplication

from src.pysidecomponents import (
    ButtonRow,
    ControlPanel,
    LabeledInput,
    LabeledSlider,
)


app = QApplication(sys.argv)

controls = ControlPanel()
name_input = LabeledInput("Name:", "Example")
size_slider = LabeledSlider("Size:", 1, 10)
buttons = ButtonRow(["Run", "Reset"])

controls.add_widget(name_input)
controls.add_widget(size_slider)
controls.add_widget(buttons)

controls.resize(420, 180)
controls.show()
app.exec()
```

The component's custom signals keep application code independent of its
internal child widgets. For example, application code can connect to
`size_slider.valueChanged` without reaching into `size_slider.slider`.

## Figures, images, and HTML

`FigureDisplayArea` can switch between three kinds of content:

- `update_image(path)` displays a local image.
- `update_matplotlib(figure)` embeds a Matplotlib `Figure`.
- `update_plotly(html)` displays HTML in `QWebEngineView`.
- `clear()` restores the empty display.

This project includes Plotly, which can generate the HTML passed to
`update_plotly()`. The display component itself consumes an HTML string rather
than a Plotly object.

Qt documents a 2 MB limit for HTML passed directly to
`QWebEngineView.setHtml()`. Large self-contained visualizations should instead
be loaded from a file or URL. See the
[QWebEngineView documentation](https://doc.qt.io/qtforpython-6/PySide6/QtWebEngineWidgets/QWebEngineView.html).

## Keep slow work out of the GUI thread

The event loop normally runs on the main thread. A long calculation in a button
handler prevents Qt from repainting the window or processing more input, so the
application appears frozen. The demos only perform short operations. Larger
applications should move expensive work to a worker thread or process and send
results back to the interface, commonly with signals.

## Using AI for GUI development

AI is especially useful for quickly scaffolding an interface, translating a
rough layout idea into widgets, or diagnosing an error. Give it concrete
constraints:

```text
Build a minimal PySide6 widget that lets a user choose a threshold and shows
how many values pass it. Use a layout and signals, keep everything in one file,
and avoid styling, extra classes, and new dependencies.
```

Then work in small steps:

1. Run the generated code before adding features.
2. Paste exact tracebacks or describe the incorrect behavior.
3. Ask for one change at a time and request that existing APIs stay intact.
4. Verify imports, signal argument types, file handling, and responsiveness.
5. Simplify code that is harder to explain than the problem requires.

AI can produce the first draft quickly; the developer still decides what the
interface should do and checks that it behaves correctly.

## References

- [Qt for Python documentation](https://doc.qt.io/qtforpython-6/)
- [First Qt Widgets application](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/widgets.html)
- [Signals and slots](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signals_and_slots.html)
- [Object trees and ownership](https://doc.qt.io/qtforpython-6/overviews/qtcore-objecttrees.html)
