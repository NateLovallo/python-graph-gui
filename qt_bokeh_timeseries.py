import sys
import tempfile
import numpy as np

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.embed import file_html


class BokehTimeSeriesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Series Viewer - Bokeh in Qt")

        # Create the Qt WebEngine view
        self.view = QWebEngineView()
        self.setCentralWidget(self.view)

        # Build the Bokeh plot HTML
        html = self._build_bokeh_html()

        # Write the HTML to a temporary file
        self.temp_file = tempfile.NamedTemporaryFile(
            suffix=".html", delete=False, mode="w", encoding="utf-8"
        )
        print("Temporary file created at:", self.temp_file.name)
        self.temp_file.write(html)
        self.temp_file.flush()

        # Load the HTML file into the web view
        url = QUrl.fromLocalFile(self.temp_file.name)
        self.view.setUrl(url)

        # Debug: report when the page finishes loading
        self.view.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok: bool):
        print(f"WebEngine load finished: ok={ok}")

    def _build_bokeh_html(self) -> str:
        # Generate sample time-series data
        t = np.linspace(0, 10, 2000)
        y = np.sin(2 * np.pi * 1.0 * t) + 0.1 * np.random.randn(t.size)

        # Create Bokeh figure
        p = figure(
            title="Time Series (Bokeh)",
            x_axis_label="Time (s)",
            y_axis_label="Value",
            width=800,
            height=400,
            tools="pan,wheel_zoom,box_zoom,reset,save,hover",
            active_drag="pan",
            active_scroll="wheel_zoom",
        )

        # Plot the time series
        p.line(t, y, line_width=2)

        # Add a hover tooltip
        p.hover.tooltips = [("time", "@x{0.00}"), ("value", "@y{0.00}")]

        # Build a standalone HTML document with INLINE resources
        html = file_html(p, INLINE, "Time Series - Bokeh")
        return html


def main():
    app = QApplication(sys.argv)
    win = BokehTimeSeriesWindow()
    win.resize(900, 600)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
