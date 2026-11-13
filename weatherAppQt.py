import sys
import requests
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QGridLayout,QLineEdit, QPushButton
from PySide6.QtCore import Qt
from rich import padding

url : str ="https://api.open-meteo.com/v1/forecast?"
location_url : str = "https://geocoding-api.open-meteo.com/v1/search?name="

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")

        # --- Variables ---
        self.location : str = 'Lahore'
        self.locationUrl : str = location_url
        self.url : str = url
        self.latitude : int = 0
        self.longitude : int = 0
        self.params : dict  = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": "temperature_2m",
            "daily": ["temperature_2m_min", "temperature_2m_max"],
            "timezone": "auto"
        }

        # --- Layout ---
        contanior = QWidget()
        self.setCentralWidget(contanior)
        layout = QVBoxLayout(contanior)

        # --- Top Section ---

                # Section Layout
        section_frame : QFrame = QFrame()
        section_layout = QHBoxLayout(section_frame)

                # App Lable
        self.appLable = QLabel("Light's weather")
        section_layout.addWidget(self.appLable)

                # Enter Location area
        self.locationEdit : QLineEdit = QLineEdit()
        self.locationEdit.setPlaceholderText("Enter a location")
        section_layout.addWidget(self.locationEdit)

                # Get Location button
        location_button : QPushButton = QPushButton("Get Location")
        location_button.clicked.connect(self.fetcRequest)
        section_layout.addWidget(location_button)


        layout.addWidget(section_frame)

        # --- Frame for temperature ---
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)

                # First section layout
        section_temp = QHBoxLayout()

                # Country info
        self.contry = QLabel(self.location, font=QFont("Arial", 14, QFont.Bold))
        self.contry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        section_temp.addWidget(self.contry)

                # Temperature
        self.Temperature = QLabel("-", font=QFont("Arial", 14, QFont.Bold))
        self.Temperature.setAlignment(Qt.AlignmentFlag.AlignRight)
        section_temp.addWidget(self.Temperature)

                # adding layout
        frame_layout.addLayout(section_temp)

                # Separator
        separator = QFrame()
        separator.setStyleSheet("background-color: grey;")
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        frame_layout.addWidget(separator)

         # --- temperature secrion 2 ---

                # seconde layout
        section_temp2 = QHBoxLayout()

                # Highest temp
        self.high_temp_lable = QLabel('<img src="./assets/thermometer_red.svg" width="16" height="16">  (high)')
        section_temp2.addWidget(self.high_temp_lable)

                # Lowest Temp
        self.low_temp_lable = QLabel('<img src="./assets/thermometer_blue.svg" width="16" height="16">  (low)')
        section_temp2.addWidget(self.low_temp_lable)

                # adding layout
        section_temp2.addStretch()
        frame_layout.addLayout(section_temp2)

        frame.setStyleSheet(f"background-color: black; border-radius: 10px;")
        layout.addWidget(frame)

        # --- functions ---
        self.fetcRequest()

    def getCoordinates(self) -> None:
        self.location = self.location if self.locationEdit.text() == '' else self.locationEdit.text()
        city = self.locationUrl + self.location
        response = dict(requests.get(city).json())
        print(response)
        print(self.location)
        self.latitude, self.longitude, self.location = response["results"][0]["latitude"], response["results"][0]["longitude"], response["results"][0]["name"]

    def fetcRequest(self) -> None:
        self.getCoordinates()
        self.info = dict(requests.get(self.url, params=self.params).json())
        self.update_app()

    def update_app(self) -> None:
        temperature = self.info["current"]["temperature_2m"]
        temperature_max = self.info["daily"]["temperature_2m_max"][0]
        temperature_min = self.info["daily"]["temperature_2m_min"][0]

        self.high_temp_lable.setText(f'<img src="./assets/thermometer_red.svg" width="16" height="16">  {temperature_max}C')
        self.low_temp_lable.setText(f'<img src="./assets/thermometer_blue.svg" width="16" height="16">  {temperature_min}C')

        self.Temperature.setText(f"{temperature}C°")
        self.contry.setText(self.location)
        print(temperature)
        print(self.info)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())