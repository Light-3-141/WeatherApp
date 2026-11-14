import sys
import requests
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QFont, QColor, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QGridLayout, \
    QLineEdit, QPushButton, QProgressBar
from PySide6.QtCore import Qt

url: str = "https://api.open-meteo.com/v1/forecast?"
location_url: str = "https://geocoding-api.open-meteo.com/v1/search?name="

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # --- Style ---
        self.card_style = "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #0D1427, stop: 1 #15324B); border-radius: 10px;"

        # --- App ---
        self.setWindowTitle("Weather App")
        self.setStyleSheet("background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 #0D1427, stop: 1 #15324B);")

        # --- Variables ---
        self.location: str = 'Lahore'
        self.locationUrl: str = location_url
        self.url: str = url
        self.latitude: int = 0
        self.longitude: int = 0
        self.params: dict = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": ["temperature_2m", "wind_speed_10m", "relative_humidity_2m"],
            "hourly": ["uv_index"],
            "daily": ["temperature_2m_min", "temperature_2m_max"],
            "timezone": "auto"
        }

        # --- Layout ---
        contanior = QWidget()
        self.setCentralWidget(contanior)
        self.layout = QVBoxLayout(contanior)

        # --- GUI build functions ---
        self.section1()
        self.section2()
        self.section3()
        # self.section3_part2()

        # --- functions ---
        try:
            self.fetch_request()
        except Exception as e:
            print(f"error{e}")

    def section1(self) -> None:
        # --- Top Section ---

        # Section Layout
        section_frame: QFrame = QFrame()
        section_layout = QHBoxLayout(section_frame)

        # App Lable
        self.appLable = QLabel("Light's weather")
        section_layout.addWidget(self.appLable)

        # Enter Location area
        self.locationEdit: QLineEdit = QLineEdit()
        self.locationEdit.setPlaceholderText("Enter a location")
        section_layout.addWidget(self.locationEdit)

        # Get Location button
        location_button: QPushButton = QPushButton("Get Location")
        location_button.clicked.connect(self.fetch_request)
        section_layout.addWidget(location_button)

        self.layout.addWidget(section_frame)

    def section2(self) -> None:
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
        self.Temperature.setStyleSheet("background-color: transparent;")
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

        frame.setStyleSheet(self.card_style)

        self.layout.addWidget(frame)

    def section3(self) -> None:
        # --- Section 3 ---
        #layout
        section3_layout1 = QHBoxLayout()

        # wind speed
        self.wind_frame, self.wind_data = self.make_card("WIND SPEED", "wind")
        section3_layout1.addWidget(self.wind_frame)

        # humidity
        self.humidity_frame, self.humidity_data = self.make_card("HUMIDITY", "droplet", bar=True)
        section3_layout1.addWidget(self.humidity_frame)

        # Uv index
        self.uv_index_frame, self.uv_index_data = self.make_card("UV INDEX", "sun")
        section3_layout1.addWidget(self.uv_index_frame)

        self.layout.addLayout(section3_layout1)

    def section3_part2(self):
        # --- Section 3  part 2---
        #layout
        section3_layout1 = QHBoxLayout()

        # wind speed
        pressure_frame = self.make_card("PRESSURE")
        section3_layout1.addWidget(pressure_frame)

        # humidity
        visibility_frame = self.make_card("VISIBILITY")
        section3_layout1.addWidget(visibility_frame)

        # Uv index
        dew_point_frame = self.make_card("DEW POINT")
        section3_layout1.addWidget(dew_point_frame)

        self.layout.addLayout(section3_layout1)

    def make_card(self, text, icon, data="-", discription=None, bar=False) -> tuple:
        frame = QFrame()
        frame.setStyleSheet(self.card_style)
        frame.setFixedSize(285, 134)

        layout = QGridLayout(frame)
        layout.setVerticalSpacing(2)  # small gap between % and bar

        # row 0: title + icon
        label = QLabel(text, font=QFont("Arial", 9, QFont.Bold))
        label.setStyleSheet("color: grey; background-color: transparent;")
        layout.addWidget(label, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        card_icon = QSvgWidget(f"./assets/{icon}.svg")
        card_icon.setFixedSize(24, 24)
        card_icon.setStyleSheet("background-color: transparent;")
        layout.addWidget(card_icon, 0, 1, Qt.AlignRight | Qt.AlignTop)

        # row 1: empty, absorbs all free space
        layout.setRowStretch(1, 1)

        # row 2: value, hugging the bottom
        data_label = QLabel(data, font=QFont("Arial", 20, QFont.Bold))
        data_label.setStyleSheet("background-color: transparent; padding: 0; margin: 0;")
        data_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(data_label, 2, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)

        # row 3: bar directly under the value
        if bar:
            data_bar = QProgressBar(value=78)
            data_bar.setTextVisible(False)
            data_bar.setFixedHeight(8)
            data_bar.setStyleSheet("""
                QProgressBar { border: none; background-color: #1E293B; border-radius: 4px; }
                QProgressBar::chunk { background-color: #3b82f6; border-radius: 4px; }
            """)
            layout.addWidget(data_bar, 3, 0, 1, 2)

        return frame, data_label

    # --- Backend function ---
    def fetch_request(self) -> None:
        """Sends and API request and retrives data"""

        self.getCoordinates()
        self.info = dict(requests.get(self.url, params=self.params).json())
        self.update_app()

    def getCoordinates(self) -> None:
        """Gets coordinates of requested location"""

        self.location = self.location if self.locationEdit.text() == '' else self.locationEdit.text()
        city = self.locationUrl + self.location
        response = dict(requests.get(city).json())
        print(response)
        print(self.location)
        self.latitude, self.longitude, self.location = response["results"][0]["latitude"], response["results"][0][
            "longitude"], response["results"][0]["name"]
        self.params["latitude"] = self.latitude
        self.params["longitude"] = self.longitude

    def update_app(self) -> None:
        """Updates the app with new data"""

                # temperature Current, daily_Max, daily_min
        temperature = self.info["current"]["temperature_2m"]
        temperature_max = self.info["daily"]["temperature_2m_max"][0]
        temperature_min = self.info["daily"]["temperature_2m_min"][0]

                # section 3 cards
        humidity = str(self.info["current"]["relative_humidity_2m"])
        wind_speed = str(self.info["current"]["wind_speed_10m"])
        uv_index = str(self.info["hourly"]["uv_index"][0])

        self.high_temp_lable.setText(
            f'<img src="./assets/thermometer_red.svg" width="16" height="16">  {temperature_max}C')
        self.low_temp_lable.setText(
            f'<img src="./assets/thermometer_blue.svg" width="16" height="16">  {temperature_min}C')
        self.humidity_data.setText(f"{humidity}%")
        self.wind_data.setText(f"{wind_speed} Km/h")
        self.uv_index_data.setText(f"{uv_index}")

        self.Temperature.setText(f"{temperature}C°")
        self.contry.setText(self.location)
        print(temperature)
        print(self.info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
