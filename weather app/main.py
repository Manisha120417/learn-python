import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)

        self.temperature_label = QLabel("--°C", self)
        self.emoji_label = QLabel("", self)
        self.description_label = QLabel("", self)
        self.humidity_label = QLabel("", self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.resize(500, 550)

        layout = QVBoxLayout()

        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.humidity_label)

        self.setLayout(layout)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.humidity_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.humidity_label.setObjectName("humidity_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Calibri;
            }

            QLabel#city_label{
                font-size:40px;
                font-style:italic;
            }

            QLineEdit#city_input{
                font-size:30px;
                padding:5px;
            }

            QPushButton#get_weather_button{
                font-size:25px;
                font-weight:bold;
                padding:10px;
            }

            QLabel#temperature_label{
                font-size:75px;
            }

            QLabel#emoji_label{
                font-size:90px;
                font-family:"Segoe UI Emoji";
            }

            QLabel#description_label{
                font-size:35px;
            }

            QLabel#humidity_label{
                font-size:30px;
                font-weight:bold;
                color:blue;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = ""

        city = self.city_input.text().strip()

        if city == "":
            self.display_error("Please enter a city name.")
            return

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            self.display_weather(data)

        except requests.exceptions.HTTPError:

            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nCheck city name.")

                case 401:
                    self.display_error("Invalid API Key.")

                case 404:
                    self.display_error("City Not Found.")

                case 500:
                    self.display_error("Internal Server Error.")

                case _:
                    self.display_error("HTTP Error.")

        except requests.exceptions.ConnectionError:
            self.display_error("No Internet Connection.")

        except requests.exceptions.Timeout:
            self.display_error("Request Timed Out.")

        except requests.exceptions.RequestException as e:
            self.display_error(str(e))

    def display_error(self, message):
        self.city_label.setText("Enter city name:")
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText("--°C")
        self.emoji_label.setText("❌")
        self.description_label.setText(message)
        self.humidity_label.setText("")

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size:75px;")

        city = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.city_label.setText(f"{city}, {country}")
        self.temperature_label.setText(f"{temperature:.1f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(description.title())
        self.humidity_label.setText(f"Humidity: {humidity}%")

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"

        elif 300 <= weather_id <= 321:
            return "🌦️"

        elif 500 <= weather_id <= 531:
            return "🌧️"

        elif 600 <= weather_id <= 622:
            return "❄️"

        elif 701 <= weather_id <= 741:
            return "🌫️"

        elif weather_id == 751:
            return "🏜️"

        elif weather_id == 761:
            return "🌪️"

        elif weather_id == 762:
            return "🌋"

        elif weather_id == 771:
            return "💨"

        elif weather_id == 781:
            return "🌪️"

        elif weather_id == 800:
            return "☀️"

        elif 801 <= weather_id <= 804:
            return "☁️"

        else:
            return "❓"


if __name__ == "__main__":
    app = QApplication(sys.argv)

    weather_app = WeatherApp()
    weather_app.show()

    sys.exit(app.exec_())