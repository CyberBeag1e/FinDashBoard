BACKGROUND_COLOR = "#dee8fb"

GLOBAL_STYLES = """
    /* General Widgets */
    QWidget {
        background-color: #dee8fb;
        color: #1b2350;
    }

    /* Buttons */
    QPushButton {
        background-color: #dee8fb;
        color: #1b2350;
        font-size: 12px;
        border-radius: 5px;
        padding: 10px 10px;
    }
    QPushButton:hover {
        background-color: #9bbff5;
    }
    QPushButton:pressed {
        background-color: #487ae9;
    }

    /* Tables */
    QTableView {
        background-color: #dee8fb;
        gridline-color: #1b2350;
        border: 1px solid #1b2350;
    }
    QHeaderView::section {
        background-color: #5991ed;
        color: #f0f5fe;
        font-size: 14px;
        border: 1px solid #1b2350;
    }

    /* Normal Text */
    QLabel {                    
        color: #1b2350;
        font-size: 12px;
        font-weight: normal;
    }

    /* Calendar Widget: Overall color*/
    QCalendarWidget QWidget {
        background-color: #dee8fb;
        alternate-background-color: #9bbff5;
        color: #1b2350;
    }

    /* Calendar Widget: Calendar Table */
    QCalendarWidget QAbstractItemView:enabled {
        selection-background-color: #487ae9;
        selection-color: #f0f5fe;
        font-size: 11px;
        color: #1b2350;
    }
    QCalendarWidget QAbstractItemView:disabled {
        color: #9bbff5;
    }
    
    /* Calendar Widget: Navigation Bar*/
    #qt_calendar_navigationbar {
        background-color: #dee8fb;
    }

    /* Calendar Widget: Left and Right Arrows*/
    #qt_calendar_prevmonth,
    #qt_calendar_nextmonth {
        border: none;
        background-color: transparent;
        qproperty-icon: none;
        width: 15px;
        height: 15px;
        border-radius: 5px;
        padding: 5px;
    }
    #qt_calendar_prevmonth {
        image: url(./Icons/left.png);
        margin-left: 3px;
    }
    #qt_calendar_nextmonth {
        image: url(./Icons/right.png);
        margin-right: 3px;
    }
    #qt_calendar_prevmonth:hover {
        background-color: #9bbff5;
    }
    #qt_calendar_nextmonth:hover {
        background-color: #9bbff5;
    }
    #qt_calendar_prevmonth:pressed {
        background-color: #487ae9;
    }
    #qt_calendar_nextmonth:pressed {
        background-color: #487ae9;
    }

    /* Calendar Widget: Month and Year Navigation*/
    #qt_calendar_yearbutton {
        color: #1b2350;
        margin: 5px;
        border-radius: 5px;
        font-size: 12px;
    }
    #qt_calendar_monthbutton {
        width: 100px;
        color: #1b2350;
        margin: 5px;
        border-radius: 5px;
        font-size: 12px;
    }
    #qt_calendar_yearbutton:hover, 
    #qt_calendar_monthbutton:hover {
        background-color: #9bbff5;
    }
    #qt_calendar_yearbutton:pressed, 
    #qt_calendar_monthbutton:pressed {
        background-color: #487ae9;
    }

    /* Calendar Widget: Year SpinBox */
    #qt_calendar_yearedit {
        min-width: 53px;
        color: #1b2350;
        background-color: transparent;
        font-size: 11px;
    }
    #qt_calendar_yearedit::down-button {
        image: url(./Icons/down.png);
        subcontrol-position: right;
    }
    #qt_calendar_yearedit::up-button {
        image: url(./Icons/up.png);
        subcontrol-position: left;
    }
    #qt_calendar_yearedit::down-button,
    #qt_calendar_yearedit::up-button {
        width: 10px;
        height: 10px;
        padding: 2px;
        border-radius: 3px;
    }
    #qt_calendar_yearedit::down-button:hover,
    #qt_calendar_yearedit::up-button:hover {
        background-color: #9bbff5;
    }

    /* Calendar Widget: Month Selection Box */
    QCalendarWidget QToolButton QMenu {
        background-color: #dee8fb;
    }
    QCalendarWidget QToolButton QMenu::item:selected:enabled {
        background-color: #487ae9;
    }
    QCalendarWidget QToolButton::menu-indicator {
        image: url(./Icons/down.png);
        width: 10px;
        subcontrol-position: right center;
        margin-top: 2px;
    }
    
    QDateEdit {
        background-color: #f0f5fe;
        border: 1px solid #263882;
        border-radius: 5px;
    }
    QDateEdit::down-arrow {
        max-height: 2px;
        image: url(./Icons/down.png);
    }
    QDateEdit::drop-down {
        border: none;
    }
    
    /* ComboBox */
    QComboBox {
        background-color: #f0f5fe;
        border: 1px solid #263882;
        border-radius: 5px;
    }
    QComboBox::down-arrow {
        max-height: 2px;
        image: url(./Icons/down.png);
    }
    QComboBox::drop-down {
        border: none;
    }
    QComboBox QAbstractItemView {
        background-color: #f0f5fe;
        border: 1px solid #263882;
        selection-background-color: #487ae9;
        selection-color: #f0f5fe;
        padding-left: 10px;
    }
    QComboBox QAbstractItemView::item {
        padding: 4px;
    }
    QComboBox QListView {
        font-size: 12px;
        border: 1px solid #487ae9;
        padding: 5px;
        background-color: #c4d8f9;
        outline: 0px;
    }

    /* ScrollBar */
    QScrollBar:vertical {
        border: 1px solid #263882;
        background: #dee8fb;
        width: 10px;
        margin: 0px 0px 0px 0px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: #9bbff5;
        min-height: 20px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical:hover {
        background: #487ae9;
    }
    QScrollBar:horizontal {
        border: 1px solid #263882;
        background: #dee8fb;
        width: 10px;
        margin: 0px 0px 0px 0px;
        border-radius: 4px;
    }
    QScrollBar::handle:horizontal {
        background: #9bbff5;
        min-height: 20px;
        border-radius: 4px;
    }
    QScrollBar::handle:horizontal:hover {
        background: #487ae9;
    }

    /* LineEdit */
    QLineEdit {
        background-color: #f0f5fe;
        border: 1px solid #263882;
        border-radius: 5px;
    }
"""

PAGE_BUTTON_STYLE = """
    QPushButton {
        background-color: #5991ed;
        color: #f0f5fe;
        font-size: 16px;
        border-radius: 5px;
        padding: 10px 15px;
    }
    QPushButton:hover {
        background-color: #335cdd;
    }
    QPushButton:pressed {
        background-color: #2a49cb;
    }
"""

GREETING_LABEL_STYLE = """
    QLabel {
        font-size: 24px;
        font-weight: bold;
    }
"""

TIME_LABEL_STYLE = """
    QLabel {
        font-size: 16px;
        font-weight: bold;
    }
"""

LABEL_STYLE = """
    QLabel {
        color: #1b2350;
        font-size: 13px;
        font-weight: bold;
    }
"""

NORMAL_TEXT_STYLE = """
    QLabel {
        color: #1b2350;
        font-size: 12px;
        font-weight: normal;
    }
"""

HIDDEN_WIDGET_STYLE = """
    background-color: #dee8fb;
    border: none;
"""

OPAQUE_WIDGET_STYLE = """
    QTableView {
        background-color: #d0d0d0;
        gridline-color: #dcdcdc;
        border: 2px solid #dcdcdc;
        border-radius: 10px;
    }
    QHeaderView::section {
        background-color: #e6e6e6;
        color: #333;
        font-size: 14px;
        border: 1px solid #dcdcdc;
    }
"""

CALENDAR_STYLE = """
    QCalendarWidget QAbstractItemView::item:hover {
        background-color: #f0f0f0;
    }
"""