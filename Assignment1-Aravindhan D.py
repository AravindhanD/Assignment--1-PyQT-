import sys
import csv
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget
from PyQt5.QtCore import Qt

class CSVGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV Graph Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.load_button = QPushButton("Load CSV")
        self.load_button.clicked.connect(self.load_csv)
        self.layout.addWidget(self.load_button)

        self.status_label = QLabel("Status: Ready")
        self.layout.addWidget(self.status_label)

        self.data = None  # Variable to store loaded CSV data

    def load_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    data = [list(map(float, row)) for row in reader]

                    if len(header) != 5:  # Check if there are five columns (5 y-axis)
                        raise ValueError("CSV file must have five columns (5 y-axis)")

                    self.data = {'x': list(range(1, len(data)+1)), 'y1': [row[0] for row in data],
                                 'y2': [row[1] for row in data], 'y3': [row[2] for row in data],
                                 'y4': [row[3] for row in data], 'y5': [row[4] for row in data]}

                    self.plot_data()
                    self.status_label.setText(f"Status: Loaded {len(data)} samples from {file_name}")

            except Exception as e:
                self.status_label.setText(f"Status: Error loading file - {str(e)}")

    def plot_data(self):
        self.plot_widget.clear()
        self.plot_widget.plot(self.data['x'], self.data['y1'], pen=pg.mkPen(color='r', width=2), name='y1')
        self.plot_widget.plot(self.data['x'], self.data['y2'], pen=pg.mkPen(color='g', width=2), name='y2')
        self.plot_widget.plot(self.data['x'], self.data['y3'], pen=pg.mkPen(color='b', width=2), name='y3')
        self.plot_widget.plot(self.data['x'], self.data['y4'], pen=pg.mkPen(color='c', width=2), name='y4')
        self.plot_widget.plot(self.data['x'], self.data['y5'], pen=pg.mkPen(color='m', width=2), name='y5')

def main():
    app = QApplication(sys.argv)
    window = CSVGraphApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
