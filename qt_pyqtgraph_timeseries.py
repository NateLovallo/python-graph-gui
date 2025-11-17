import sys
import numpy as np

from PySide6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg


class TimeSeriesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Series Viewer - PyQtGraph")

        # Create a PlotWidget and set it as the central widget
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        # Generate some sample time-series data
        t = np.linspace(0, 10, 2000)  # time in seconds
        y = np.sin(2 * np.pi * 1.0 * t) + 0.1 * np.random.randn(t.size)

        # Plot the data
        self.curve = self.plot_widget.plot(t, y, pen="y")

        # Make it look nice for time series
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setLabel("left", "Value")
        self.plot_widget.showGrid(x=True, y=True)

        # Enable mouse interaction (pan/zoom)
        self.plot_widget.setMouseEnabled(x=True, y=True)
        self.plot_widget.setDownsampling(mode="peak")
        self.plot_widget.setClipToView(True)


def main():
    app = QApplication(sys.argv)
    win = TimeSeriesWindow()
    win.resize(800, 500)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
