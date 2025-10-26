import sys
import math
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QDoubleSpinBox, QComboBox, QPushButton
)
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

# Alamat server backend Rust Anda
BACKEND_URL = "http://127.0.0.1:8080/simulate"

class SignalSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulasi Kombinasi Sinyal (Rust + Qt)")
        self.setGeometry(100, 100, 1200, 800)
        
        # Timer untuk simulasi real-time 
        self.timer = QTimer()
        self.timer.setInterval(100) # Update setiap 100 ms
        self.timer.timeout.connect(self.update_plot)
        self.is_running = False
        
        self.init_ui()

    def init_ui(self):
        # --- Widget Utama ---
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # --- Panel Kontrol (Kiri) ---
        control_panel = QWidget()
        control_layout = QVBoxLayout()
        control_panel.setLayout(control_layout)
        control_panel.setMaximumWidth(350)

        # Parameter Sinyal x1(t) [cite: 66, 67, 68]
        form_layout_1 = QFormLayout()
        self.a1_input = QDoubleSpinBox(value=1.0)
        self.f1_input = QDoubleSpinBox(value=5.0)
        self.p1_input = QDoubleSpinBox(value=0.0, minimum=-360, maximum=360)
        form_layout_1.addRow(QLabel("<b>Sinyal 1 (x1)</b>"), None)
        form_layout_1.addRow("Amplitudo (A1):", self.a1_input)
        form_layout_1.addRow("Frekuensi (f1, Hz):", self.f1_input)
        form_layout_1.addRow("Fase (φ1, derajat):", self.p1_input)

        # Parameter Sinyal x2(t) [cite: 66, 67, 68]
        form_layout_2 = QFormLayout()
        self.a2_input = QDoubleSpinBox(value=0.5)
        self.f2_input = QDoubleSpinBox(value=10.0)
        self.p2_input = QDoubleSpinBox(value=0.0, minimum=-360, maximum=360)
        form_layout_2.addRow(QLabel("<b>Sinyal 2 (x2)</b>"), None)
        form_layout_2.addRow("Amplitudo (A2):", self.a2_input)
        form_layout_2.addRow("Frekuensi (f2, Hz):", self.f2_input)
        form_layout_2.addRow("Fase (φ2, derajat):", self.p2_input)
        
        # Pilihan Operasi [cite: 69]
        operation_layout = QFormLayout()
        self.op_combo = QComboBox()
        self.op_combo.addItems(["add", "subtract", "multiply"])
        operation_layout.addRow(QLabel("<b>Operasi Sinyal</b>"), None)
        operation_layout.addRow("Operasi (y):", self.op_combo)

        # Tombol Kontrol [cite: 71, 72]
        button_layout = QHBoxLayout()
        self.start_stop_btn = QPushButton("Start Simulation")
        self.start_stop_btn.clicked.connect(self.toggle_simulation)
        self.export_btn = QPushButton("Export CSV")
        # self.export_btn.clicked.connect(self.export_data) # TODO
        button_layout.addWidget(self.start_stop_btn)
        button_layout.addWidget(self.export_btn)

        # Tambahkan semua ke panel kontrol
        control_layout.addLayout(form_layout_1)
        control_layout.addLayout(form_layout_2)
        control_layout.addLayout(operation_layout)
        control_layout.addLayout(button_layout)
        control_layout.addStretch() # Mendorong semua ke atas

        # --- Panel Plot (Kanan) --- 
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'Amplitudo')
        self.plot_widget.setLabel('bottom', 'Waktu (s)')
        self.plot_widget.addLegend()
        self.plot_widget.showGrid(x=True, y=True)
        
        # Siapkan 3 kurva sinyal [cite: 70]
        self.plot_x1 = self.plot_widget.plot(pen=pg.mkPen('b', width=2), name="x1(t)")
        self.plot_x2 = self.plot_widget.plot(pen=pg.mkPen('g', width=2), name="x2(t)")
        self.plot_y = self.plot_widget.plot(pen=pg.mkPen('r', width=3, style=pg.QtCore.Qt.DashLine), name="y(t)")

        # --- Gabungkan Panel Kontrol dan Panel Plot ---
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.plot_widget)

    def toggle_simulation(self):
        """Mengaktifkan atau menonaktifkan timer simulasi"""
        if self.is_running:
            self.timer.stop()
            self.start_stop_btn.setText("Start Simulation")
        else:
            self.timer.start()
            self.start_stop_btn.setText("Stop Simulation")
        self.is_running = not self.is_running

    def update_plot(self):
        """Fungsi inti: Ambil data dari GUI, kirim ke Rust, terima JSON, update plot"""
        try:
            # 1. Kumpulkan semua parameter dari GUI
            params1 = {
                "amplitude": self.a1_input.value(),
                "frequency": self.f1_input.value(),
                "phase": math.radians(self.p1_input.value()) # Konversi derajat ke radian
            }
            params2 = {
                "amplitude": self.a2_input.value(),
                "frequency": self.f2_input.value(),
                "phase": math.radians(self.p2_input.value()) # Konversi derajat ke radian
            }
            
            # Siapkan JSON payload untuk dikirim ke backend Rust
            payload = {
                "params1": params1,
                "params2": params2,
                "operation": self.op_combo.currentText(),
                "fs": 1000.0,           # Frekuensi sampling (hardcoded)
                "duration_secs": 1.0    # Durasi plot (hardcoded)
            }
            
            # 2. Kirim request POST ke backend Rust
            response = requests.post(BACKEND_URL, json=payload, timeout=0.09)
            
            if response.status_code == 200:
                # 3. Terima respons JSON
                data = response.json()
                
                # 4. Update data plot [cite: 70]
                self.plot_x1.setData(data['t'], data['x1'])
                self.plot_x2.setData(data['t'], data['x2'])
                self.plot_y.setData(data['t'], data['y'])
            else:
                print(f"Error dari server: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Gagal terhubung ke backend: {e}")
            # Hentikan simulasi jika backend mati
            if self.is_running:
                self.toggle_simulation()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = SignalSimulatorApp()
    main_app.show()
    sys.exit(app.exec_())