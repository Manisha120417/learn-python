

import sys
from PyQt5.QtWidgets import QApplication

from weather_app import WeatherApp


def main():
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
