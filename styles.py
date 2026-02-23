MAIN_LABEL_STYLE = ("Color: rgb(4, 43, 94);"
                    "Background-Color: rgb(209, 232, 235);"
                    "Border-radius: 5px")

TRACK_SLIDER_STYLE = """
                    QSlider::groove:horizontal {
                        height: 6px;
                        background: rgb(26, 25, 107);
                        border-radius: 3px;
                        border: 1px solid white;
                    }
                    QSlider::handle:horizontal {
                        background: white;
                        width: 16px;
                        height: 16px;
                        margin: -5px 0;
                        border-radius: 8px;
                    }
                    QSlider::sub-page:horizontal {
                        background: rgb(209, 232, 235);
                        border-radius: 3px;
                    }
                """

BUTTON_STYLE = """
            QPushButton {
                font-family: consolas;
                font-size: 16pt;
                color: rgb(4, 43, 94);
                background-color: white;
            }
            QPushButton:hover {
                background-color: rgb(230, 230, 230);
            }
            QPushButton:pressed {
                background-color: rgb(4, 43, 94);
                color: white;
            }
        """

VOLUME_SLIDER_STYLE = """
            QSlider::groove:horizontal {
                height: 6px;
                background: rgb(26, 25, 107);
                border-radius: 3px;
                border: 1px solid white;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: rgb(209, 232, 235);
                border-radius: 3px;
            }
        """

LIST_WIDGET_STYLE = """
            QListWidget {
                background-color: rgb(26, 25, 107);
                color: White;
                border: 1px solid white;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QListWidget:focus {
                outline: none;
            }
            QListWidget::item:hover {
                Color: rgb(4, 43, 94);
                background-color: #b8b8e3;
            }
            QListWidget::item:selected:hover {
                Color: White;
                background-color: #2c2cf5;
            }
            QScrollBar:vertical {
                background: rgb(26, 25, 107);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgb(209, 232, 235);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: white;
            }
            QScrollBar::add-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """