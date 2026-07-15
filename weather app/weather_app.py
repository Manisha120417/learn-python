import requests
from datetime import datetime, timezone, timedelta
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

import database
from history_window import HistoryWindow


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        # Make sure the SQLite table exists before anything else runs
        database.init_db()

        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.history_button = QPushButton("View History", self)

        self.temperature_label = QLabel("--°C", self)
        self.emoji_label = QLabel("", self)
        self.description_label = QLabel("", self)
        self.humidity_label = QLabel("", self)

        # New: wind speed + sunrise/sunset chip cards for the current weather
        # (Sushma Pandey: wind speed | Manisha Tamang: sunrise/sunset)
        self.details_frame1, self.wind_label = self._make_forecast_card()
        self.details_frame2, self.sunrise_label = self._make_forecast_card()
        self.details_frame3, self.sunset_label = self._make_forecast_card()

        # Forecast heading (styled like an H1, sits above the 3-day group)
        self.forecast_heading = QLabel("Forecast", self)

        # Forecast day "cards" - each is a bordered frame holding one QLabel
        self.day1_frame, self.day1_label = self._make_forecast_card()
        self.day2_frame, self.day2_label = self._make_forecast_card()
        self.day3_frame, self.day3_label = self._make_forecast_card()

        self.initUI()

    def _make_forecast_card(self):
        """Create a bordered card (QFrame) containing a single forecast QLabel."""
        frame = QFrame(self)
        frame.setObjectName("forecast_card")
        label = QLabel("", frame)
        label.setObjectName("forecast_label")
        label.setAlignment(Qt.AlignCenter)

        card_layout = QVBoxLayout(frame)
        card_layout.addWidget(label)
        card_layout.setContentsMargins(0, 0, 0, 0)

        return frame, label

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.resize(500, 800)

        layout = QVBoxLayout()

        # Top section: Input and Current Weather
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)

        # Get Weather + View History side by side
        button_row = QHBoxLayout()
        button_row.addWidget(self.get_weather_button)
        button_row.addWidget(self.history_button)
        layout.addLayout(button_row)

        layout.addWidget(self.temperature_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.humidity_label)

        # Details row: wind speed, sunrise, sunset shown as small chip cards
        details_row = QHBoxLayout()
        details_row.setSpacing(12)
        details_row.addWidget(self.details_frame1)
        details_row.addWidget(self.details_frame2)
        details_row.addWidget(self.details_frame3)
        layout.addLayout(details_row)

        # Middle section: Forecast heading (H1, bold) - clearly comes BEFORE the data
        layout.addWidget(self.forecast_heading)

        # Bottom section: 3-day data grouped together, side-by-side, as cards
        forecast_layout = QHBoxLayout()
        forecast_layout.setSpacing(12)
        forecast_layout.addWidget(self.day1_frame)
        forecast_layout.addWidget(self.day2_frame)
        forecast_layout.addWidget(self.day3_frame)
        layout.addLayout(forecast_layout)

        self.setLayout(layout)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.humidity_label.setAlignment(Qt.AlignCenter)
        self.forecast_heading.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.history_button.setObjectName("history_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.humidity_label.setObjectName("humidity_label")
        self.forecast_heading.setObjectName("forecast_heading")

        self.setStyleSheet("""
            QWidget{
                background-color:#ffffff;
            }

            QLabel, QPushButton{
                font-family: Calibri;
                color:#222222;
            }

            QLabel#city_label{
                font-size:36px;
                font-style:italic;
                font-weight:600;
                color:#1a1a1a;
            }

            QLineEdit#city_input{
                font-size:26px;
                padding:8px 12px;
                background-color:#f5f6fa;
                border:2px solid #dcdfe8;
                border-radius:10px;
                color:#1a1a1a;
                selection-background-color:#5a7dfa;
            }

            QLineEdit#city_input:focus{
                border:2px solid #5a7dfa;
            }

            QPushButton#get_weather_button{
                font-size:22px;
                font-weight:bold;
                padding:10px;
                background-color:#5a7dfa;
                color:#ffffff;
                border:none;
                border-radius:10px;
            }

            QPushButton#get_weather_button:hover{
                background-color:#7593ff;
            }

            QPushButton#get_weather_button:pressed{
                background-color:#4666db;
            }

            QPushButton#history_button{
                font-size:22px;
                font-weight:bold;
                padding:10px;
                background-color:#f5f6fa;
                color:#5a7dfa;
                border:2px solid #5a7dfa;
                border-radius:10px;
            }

            QPushButton#history_button:hover{
                background-color:#eaefff;
            }

            QPushButton#history_button:pressed{
                background-color:#dbe3ff;
            }

            QLabel#temperature_label{
                font-size:70px;
                font-weight:300;
                color:#1a1a1a;
            }

            QLabel#emoji_label{
                font-size:80px;
                font-family:"Segoe UI Emoji";
            }

            QLabel#description_label{
                font-size:30px;
                color:#555b70;
            }

            QLabel#humidity_label{
                font-size:24px;
                font-weight:bold;
                color:#5a7dfa;
                padding-bottom:10px;
            }

            /* Forecast heading styled as a true H1: bold, upright, sits above the data */
            QLabel#forecast_heading{
                font-size:32px;
                font-weight:800;
                font-style:normal;
                color:#1a1a1a;
                letter-spacing:0.5px;
                margin-top:15px;
                border-top:1px solid #e0e2ea;
                padding-top:18px;
                padding-bottom:12px;
            }

            /* Each day is a distinct grouped card, all 3 sit in a row */
            QFrame#forecast_card{
                background-color:#f5f6fa;
                border:1px solid #e0e2ea;
                border-radius:10px;
            }

            QLabel#forecast_label{
                font-size:14px;
                font-family:"Segoe UI Emoji";
                color:#333344;
                padding:12px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)
        self.history_button.clicked.connect(self.open_history)

    def open_history(self):
        """Open the SQLite-backed history window (Manisha's feature)."""
        dialog = HistoryWindow(self)
        dialog.exec_()

    def get_weather(self):
        # Remember to add your actual OpenWeatherMap API key string here
        api_key = ""

        city = self.city_input.text().strip()

        if city == "":
            self.display_error("Please enter a city name.")
            return

        current_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )
        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&appid={api_key}&units=metric"
        )

        try:
            current_response = requests.get(current_url, timeout=10)
            current_response.raise_for_status()
            current_data = current_response.json()

            forecast_response = requests.get(forecast_url, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()

            self.display_weather(current_data)
            self.display_forecast(forecast_data)

        except requests.exceptions.HTTPError:
            status_code = current_response.status_code if 'current_response' in locals() else None
            match status_code:
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
        self.wind_label.setText("")
        self.sunrise_label.setText("")
        self.sunset_label.setText("")
        self.day1_label.setText("")
        self.day2_label.setText("")
        self.day3_label.setText("")

    @staticmethod
    def _format_local_time(unix_ts, tz_offset_seconds):
        """Convert a UTC unix timestamp + timezone offset (seconds) into 'HH:MM AM/PM'."""
        city_tz = timezone(timedelta(seconds=tz_offset_seconds))
        local_dt = datetime.fromtimestamp(unix_ts, tz=city_tz)
        return local_dt.strftime("%I:%M %p").lstrip("0")

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size:75px;")

        city = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        # Wind speed (Sushma Pandey's feature)
        wind_speed = data["wind"]["speed"]

        # Sunrise / Sunset (Manisha Tamang's feature)
        tz_offset = data.get("timezone", 0)
        sunrise_ts = data["sys"]["sunrise"]
        sunset_ts = data["sys"]["sunset"]
        sunrise_time = self._format_local_time(sunrise_ts, tz_offset)
        sunset_time = self._format_local_time(sunset_ts, tz_offset)

        self.city_label.setText(f"{city}, {country}")
        self.temperature_label.setText(f"{temperature:.1f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(description.title())
        self.humidity_label.setText(f"Humidity: {humidity}%")

        self.wind_label.setText(f"🌬️\nWind\n{wind_speed} m/s")
        self.sunrise_label.setText(f"🌅\nSunrise\n{sunrise_time}")
        self.sunset_label.setText(f"🌇\nSunset\n{sunset_time}")

        # Save this search to SQLite (Sushma Pandey's feature)
        database.save_search(
            city=city,
            country=country,
            temperature=temperature,
            humidity=humidity,
            description=description,
            wind_speed=wind_speed,
            sunrise=sunrise_time,
            sunset=sunset_time,
        )

    def display_forecast(self, data):
        labels = [self.day1_label, self.day2_label, self.day3_label]
        indices = [8, 16, 24]

        for label, idx in zip(labels, indices):
            if idx >= len(data["list"]):
                label.setText("")
                continue

            item = data["list"][idx]
            date = item["dt_txt"].split(" ")[0]
            description = item["weather"][0]["description"].title()
            weather_id = item["weather"][0]["id"]
            emoji = self.get_weather_emoji(weather_id)
            temp = item["main"]["temp"]
            humidity = item["main"]["humidity"]
            wind = item["wind"]["speed"]

            label.setText(
                f"{date}\n"
                f"{emoji}\n"
                f"{description}\n"
                f"🌡️ {temp:.1f}°C\n"
                f"💧 {humidity}%\n"
                f"🌬️ {wind} m/s"
            )

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
