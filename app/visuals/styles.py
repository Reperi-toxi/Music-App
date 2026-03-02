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
CHECKBOX_STYLE = """
                QCheckBox {
                    spacing: 10px;
                    font-family: Consolas;
                    font-size: 14pt;
                    color: white;
                }
                
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border-radius: 5px;
                    border: 2px solid white;
                    background-color: rgb(26, 25, 107);  /* unchecked */
                }
                
                QCheckBox::indicator:hover {
                    background-color: rgb(70, 70, 180); /* hover unchecked: lighter blue */
                }
                
                QCheckBox::indicator:checked {
                    background-color: rgb(209, 232, 235);  /* checked: light accent like your slider sub-page */
                    border: 2px solid rgb(4, 43, 94);
                }
                
                QCheckBox::indicator:checked:hover {
                    background-color: rgb(150, 200, 220);  /* hover checked: slightly darker/light blue */
                }
                
                QCheckBox::indicator:disabled {
                    background-color: rgb(50, 50, 80);
                    border: 2px solid rgb(100, 100, 120);
                }
            """

BUTTON_STYLE = """
                QPushButton {
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 #7850ff, stop:1 #5030cc);
                    border-radius: 15px;
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    min-width: 36px;
                    min-height: 36px;
                    border: none;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 #9070ff, stop:1 #7050ee);
                    /* simulate glow with border */
                    border: 2px solid rgba(120,80,255,0.6);
                }
                QPushButton:pressed {
                    background: rgb(60, 40, 160);
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
                background: rgba(18, 15, 45, 0.95);
                border: 1px solid rgba(120, 80, 255, 0.2);
                border-radius: 12px;
                padding: 4px;
                outline: 0;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 6px 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(120, 80, 255, 0.4);
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(150, 110, 255, 0.7);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """