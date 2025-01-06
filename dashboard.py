from PyQt5.QtWidgets import (
    QApplication, QMainWindow, 
    QWidget, QListWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy,
    QLabel, QPushButton, QCheckBox, QLineEdit, QComboBox, 
    QDateEdit, QTableView, QMessageBox, QRadioButton, QButtonGroup,
    QFileDialog, QItemDelegate, QStyledItemDelegate
)
from PyQt5.QtCore import (
    Qt, QTimer, QDate, QAbstractTableModel, QSize
)

from PyQt5.QtGui import QIcon, QDoubleValidator

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import datetime as dt
from dateutil.relativedelta import relativedelta

from data_manipulation import *
from style_sheet import *
from categories import CATEGORIES


class DashBoard(QMainWindow):

    def __init__(self, db: DataHandler):
        
        ## Initialize the window
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(200, 200, 900, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self._layout = QVBoxLayout()
        self.central_widget.setLayout(self._layout)

        ## Icons
        self._home_icon = QIcon("./Icons/home.png")
        self._check_icon = QIcon("./Icons/check.png")
        self._add_icon = QIcon("./Icons/add.png")
        self._delete_icon = QIcon("./Icons/delete.png")
        self._lock_icon = QIcon("./Icons/lock.png")
        self._unlock_icon = QIcon("./Icons/unlock.png")
        self._search_icon = QIcon("./Icons/search.png")
        self._download_icon = QIcon("./Icons/download.png")

        ## Date
        today = dt.date.today()
        self._today = QDate(today.year, today.month, today.day)
        yesterday = today - dt.timedelta(1)
        self._yesterday = QDate(yesterday.year, yesterday.month, yesterday.day)
        week_ago = yesterday - dt.timedelta(7)
        self._week_ago = QDate(week_ago.year, week_ago.month, week_ago.day)
        month_ago = yesterday - relativedelta(months = 1)
        self._month_ago = QDate(month_ago.year, month_ago.month, month_ago.day)

        ## Connected Database
        self._db = db

        ## Attributes for expenditure page
        self._init_ledger_page()

        ## Attributes for data viewing page
        self._init_viewing_page()        

        ## Attributes for summary page
        self._init_summary_page()

        ## Interface
        self._pages = QStackedWidget()
        self._layout.addWidget(self._pages)

        self._home_page = self.create_home_page()
        self._pages.addWidget(self._home_page)

        self._exp_page = self.create_exp_page()
        self._viewing_page = self.create_viewing_page()
        self._summary_page = self.create_summary_page()

        self._pages.addWidget(self._exp_page)
        self._pages.addWidget(self._viewing_page)
        self._pages.addWidget(self._summary_page)

        self._pages.setCurrentWidget(self._home_page)

    ##----- Home Page -----##
    def create_home_page(self):
        home = QWidget()
        layout = QVBoxLayout(home)

        greeting_layout = QHBoxLayout()
        self._greeting_label = QLabel()
        self._greeting_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._greeting_label.setStyleSheet(GREETING_LABEL_STYLE)

        self._time_label = QLabel()
        self._time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._time_label.setStyleSheet(TIME_LABEL_STYLE)

        greeting_layout.addWidget(self._greeting_label)
        greeting_layout.addWidget(self._time_label)

        layout.addLayout(greeting_layout)

        self._update_time_greeting()
        timer = QTimer(self)
        timer.timeout.connect(self._update_time_greeting)
        timer.start(1000)

        layout.addStretch()
        nevigation_layout = QVBoxLayout()

        button_exp = QPushButton("Track Expenditure")
        button_exp.clicked.connect(lambda: self._pages.setCurrentWidget(self._exp_page))
        button_exp.setFixedSize(240, 80)
        button_exp.setStyleSheet(PAGE_BUTTON_STYLE)
        button_exp.setToolTip("Nevigate to the page to track your daily expenditure.")
        nevigation_layout.addWidget(button_exp)

        button_viewing = QPushButton("View")
        button_viewing.clicked.connect(lambda: self._pages.setCurrentWidget(self._viewing_page))
        button_viewing.setFixedSize(240, 80)
        button_viewing.setStyleSheet(PAGE_BUTTON_STYLE)
        button_viewing.setToolTip("Nevigate to the page to view your expenditure history.")
        nevigation_layout.addWidget(button_viewing)

        button_summary = QPushButton("Summarize")
        button_summary.clicked.connect(lambda: self._pages.setCurrentWidget(self._summary_page))
        button_summary.setFixedSize(240, 80)
        button_summary.setStyleSheet(PAGE_BUTTON_STYLE)
        button_summary.setToolTip("Nevigate to the page to summarize your past expenditure.")
        nevigation_layout.addWidget(button_summary)

        nevigation_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(nevigation_layout)
        layout.addStretch()

        return home
    
    ## Update the greetings on the home page
    def _update_time_greeting(self):
        """
        Update the greeting text according to current time
        """
        now = dt.datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%a, %b %d, %Y")
        self._time_label.setText(f"{current_time}\n{current_date}")

        hour = now.hour
        if 5 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon"
        elif 18 <= hour < 23:
            greeting = "Good Evening"
        else:
            greeting = "Good Night"
        
        self._greeting_label.setText(greeting)

    ##----- Tracking Expenditure Page -----##
    ## Initialization
    def _init_ledger_page(self):
        self._temp_df = pd.DataFrame(columns = ["Date", "Category", "Amount", "Type"])
        self._ledger_table = QTableView()
        self._temp_model = TableModel(self._temp_df)
        self._ledger_table.setModel(self._temp_model)
        self._ledger_table.hideColumn(0)

        ## Date Input
        self._ledger_date_input = QDateEdit()
        self._ledger_date_input.setCalendarPopup(True)
        self._ledger_date_input.setDate(self._today)

        ## Category Input
        self._ledger_category_input = QComboBox()
        self._ledger_category_input.addItems(CATEGORIES)

        ## Amount Input
        self._ledger_amount_input = QLineEdit()
        self._ledger_amount_input.setText("0.0")

        ## Type Input
        self._ledger_radio_rev = QRadioButton("Revenue")
        self._ledger_radio_exp = QRadioButton("Expenditure")
        self._ledger_radio_exp.setChecked(True)
        self._ledger_button_group = QButtonGroup()
        self._ledger_button_group.addButton(self._ledger_radio_exp)
        self._ledger_button_group.addButton(self._ledger_radio_rev)

        ## Button
        self._ledger_add_button = QPushButton()
        self._ledger_add_button.setIcon(self._add_icon)
        self._ledger_add_button.clicked\
                               .connect(lambda: self.add_exp_records(date = self._ledger_date_input.date().toPyDate(),
                                                                     category = self._ledger_category_input.currentText(),
                                                                     amount = self._ledger_amount_input.text(), 
                                                                     type_ = self._ledger_button_group.checkedButton().text()))

    ## Page Layout
    def create_exp_page(self):
        exp_page = QWidget()
        layout = QVBoxLayout(exp_page)

        home_button = QPushButton()
        home_button.clicked.connect(lambda: self._pages.setCurrentWidget(self._home_page))
        home_button.setIcon(self._home_icon)
        
        layout.addWidget(home_button)

        ## Date Layout
        input_layout = QGridLayout()

        date_layout = QVBoxLayout()
        date_label = QLabel("Date: ")
        date_layout.addWidget(date_label)
        date_layout.addWidget(self._ledger_date_input)

        input_layout.addLayout(date_layout, 0, 0)

        ## Category Layout
        category_layout = QVBoxLayout()
        category_label = QLabel("Category: ")
        category_layout.addWidget(category_label)
        category_layout.addWidget(self._ledger_category_input)

        input_layout.addLayout(category_layout, 0, 1)

        ## Amount Layout
        amount_layout = QVBoxLayout()
        amount_label = QLabel("Amount: ")
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self._ledger_amount_input)
        input_layout.addLayout(amount_layout, 1, 0)

        ## Type Layout
        type_layout = QGridLayout()
        type_label = QLabel("Type: ")
        type_layout.addWidget(type_label, 0, 0)
        type_layout.addWidget(self._ledger_radio_exp, 1, 0)
        type_layout.addWidget(self._ledger_radio_rev, 1, 1)
        input_layout.addLayout(type_layout, 1, 1)

        ## Button
        input_layout.addWidget(self._ledger_add_button, 2, 1, alignment = Qt.AlignmentFlag.AlignRight)

        ## Spacing
        input_layout.setColumnMinimumWidth(0, 400)
        input_layout.setColumnMinimumWidth(1, 400)
        input_layout.setColumnStretch(0, 1)
        input_layout.setColumnStretch(1, 1)

        layout.addLayout(input_layout)
        layout.addWidget(self._ledger_table)

        ## UI
        date_label.setStyleSheet(LABEL_STYLE)
        category_label.setStyleSheet(LABEL_STYLE)
        amount_label.setStyleSheet(LABEL_STYLE)
        type_label.setStyleSheet(LABEL_STYLE)
        home_button.setFixedSize(30, 30)
        self._ledger_add_button.setFixedSize(30, 30)
        self._ledger_table.setStyleSheet(HIDDEN_WIDGET_STYLE)
        self._ledger_date_input.calendarWidget().setFixedSize(QSize(300, 200))

        return exp_page
    
    ## Verify user inputs and update the table
    def add_exp_records(self, date: dt.date, category: str, amount: str, type_: str):
        """
        Track expenditure: verify the input and update the displayed table.
        """
        try:
            amount = float(amount)
            self._temp_df = self._db.add_temp_rec(date, category, amount, type_[:3])
            self._temp_model._data = self._temp_df
            self._temp_model.layoutChanged.emit()
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("The input must be a non-negative number.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.exec_()

            return
    

    ##----- Data viewing Page -----##
    ## Initialization: buttons, table views
    def _init_viewing_page(self):
        
        ## Date Input
        self._view_start_date = QDateEdit()
        self._view_start_date.setCalendarPopup(True)
        self._view_end_date = QDateEdit()
        self._view_end_date.setCalendarPopup(True)
        
        self._view_start_date.setDate(self._month_ago)
        self._view_end_date.setDate(self._yesterday)

        ## Category Input
        self._view_category_select = QListWidget()
        self._view_category_select.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self._view_category_select.addItems(["All"] + CATEGORIES)

        ## Type Input
        self._view_type_exp = QCheckBox("Expenditure")
        self._view_type_rev = QCheckBox("Revenue")

        ## Apply Button
        self._view_apply_button = QPushButton()
        self._view_apply_button.setIcon(self._search_icon)
        self._view_apply_button.setFixedSize(30, 30)
        self._view_apply_button.clicked\
                               .connect(lambda: self._update_data_viewing(
                                                    self._view_start_date.date().toPyDate(),
                                                    self._view_end_date.date().toPyDate(),
                                                    [item.text() for item in self._view_category_select.selectedItems()], 
                                                    self._view_type_exp.isChecked(), 
                                                    self._view_type_rev.isChecked()))
        
        ## Table View
        self._view_df = self._db.get_all_records(include_id = True)
        self._view_table = QTableView()
        self._table_model = EditableTableModel(self._view_df)
        self._view_table.setModel(self._table_model)
        self._view_table.hideColumn(0)
        self._view_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._view_table.setItemDelegate(TableDelegate())
        self._view_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        ## Buttons
        self._lock_button = QPushButton()
        self._lock_button.setCheckable(True)
        self._lock_button.clicked.connect(self._toggle_lock)
        self._lock_button.setIcon(self._lock_icon)
        self._lock_button.setToolTip("Click this button to lock/unlock the above table. The table can be modified when it's unlocked.")

        self._confirm_button = QPushButton()
        self._confirm_button.setIcon(self._check_icon)
        self._confirm_button.clicked.connect(self._apply_changes)
        self._confirm_button.setToolTip("Confirm the changes you've made.")

        self._delete_button = QPushButton()
        self._delete_button.setIcon(self._delete_icon)
        self._delete_button.clicked.connect(self._delete_records)
        self._delete_button.setToolTip("Click this button to delete the selected record.")

        self._save_button = QPushButton()
        self._save_button.setIcon(self._download_icon)
        self._save_button.clicked.connect(self._save_files)
        self._save_button.setToolTip("Click this button to save the records to local.")

    
    ## Toggle the lock status of table
    def _toggle_lock(self):
        if self._lock_button.isChecked():
            self._lock_button.setIcon(self._unlock_icon)
            self._view_table.setEditTriggers(QTableView.EditTrigger.AllEditTriggers)
        else:
            self._lock_button.setIcon(self._lock_icon)
            self._view_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
    
    ## Test: apply changes to the data base
    def _apply_changes(self):
        if self._table_model._modified_rows:
            confirm_box = QMessageBox.question(
                self, "Confirm Changes",
                "Are you sure to apply these changes? Note that changes cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm_box == QMessageBox.StandardButton.Yes:
                for data in self._table_model._modified_rows.values():
                    new_id = data["id"]
                    new_date = data["Date"]
                    new_category = data["Category"]
                    new_amount = data["Amount"]

                    self._db.update_record(new_id, new_date, new_category, new_amount)
                
                self._table_model._modified_rows.clear()
                QMessageBox.information(self, "Success", "Changes have been applied!")
    
    ## Delete records
    def _delete_records(self):
        selected_index = self._view_table.selectionModel().selectedRows()

        if not selected_index:
            QMessageBox.warning(
                self, "No Selection",
                "If you want to delete some records, please select at least one."
            )
            return
        
        confirm_box = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure to delete the selected record? Note that this cannot be undone!", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm_box == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Success", "The record have been deleted.")
            selected_row = selected_index[0].row()
            record_id = int(self._table_model._data.iloc[selected_row]["id"])

            self._db.delete_records(record_id)
            self._table_model._data = self._table_model._data[self._table_model._data["id"] != record_id]
            self._table_model.layoutChanged.emit()
    
    ## Save File
    def _save_files(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Table As",
            "",
            "CSV File (*.csv);;Excel Files (*.xlsx);;JSON Files (*.json)",
            options = options
        )

        if file_path:
            if file_path.endswith(".csv"):
                self._view_df.to_csv(file_path, index = False)
            elif file_path.endswith(".xlsx"):
                self._view_df.to_excel(file_path, index = False)
            elif file_path.endswith(".json"):
                self._view_df.to_json(file_path, orient = "records")
            
            QMessageBox.information(self, "Success", f"File has been successfully saved to {file_path}")

    ## Initializing the viewing page
    def create_viewing_page(self):
        """Tab for viewing and filtering data."""
        viewing_page = QWidget()
        layout = QHBoxLayout(viewing_page)
    
        input_layout = QVBoxLayout()

        ## Home Button
        home_button = QPushButton()
        home_button.setIcon(self._home_icon)
        home_button.setFixedSize(30, 30)
        home_button.clicked.connect(lambda: self._pages.setCurrentWidget(self._home_page))
        input_layout.addWidget(home_button)
        
        ## Date Layout
        date_layout = QGridLayout()
        start_label = QLabel("Start Date:")
        end_label = QLabel("End Date:")
        date_layout.addWidget(start_label, 0, 0)
        date_layout.addWidget(end_label, 0, 1)
        date_layout.addWidget(self._view_start_date, 1, 0)
        date_layout.addWidget(self._view_end_date, 1, 1)

        input_layout.addLayout(date_layout)

        ## Category Layout
        category_label = QLabel("Categories: ")
        input_layout.addWidget(category_label)
        input_layout.addWidget(self._view_category_select)

        ## Type Layout
        type_label = QLabel("Type: ")
        type_layout = QHBoxLayout()
        type_layout.addWidget(type_label)
        type_layout.addWidget(self._view_type_exp)
        type_layout.addWidget(self._view_type_rev)
        input_layout.addLayout(type_layout)

        input_layout.addWidget(self._view_apply_button, alignment = Qt.AlignmentFlag.AlignRight)
        input_layout.addStretch()
        layout.addLayout(input_layout)
        layout.addStretch()

        ## Output Layout
        output_layout = QVBoxLayout()
        output_layout.addWidget(self._view_table)
        
        ## Buttons for modifying the table
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self._delete_button)
        buttons_layout.addWidget(self._lock_button)
        buttons_layout.addWidget(self._confirm_button)
        buttons_layout.addWidget(self._save_button)
        output_layout.addLayout(buttons_layout)

        layout.addLayout(output_layout)
        layout.addStretch()

        ## UI
        start_label.setStyleSheet(LABEL_STYLE)
        end_label.setStyleSheet(LABEL_STYLE)
        category_label.setStyleSheet(LABEL_STYLE)
        type_label.setStyleSheet(LABEL_STYLE)
        self._view_category_select.setFixedSize(QSize(400, 400))
        self._view_table.setFixedWidth(400)
        self._lock_button.setFixedSize(30, 30)
        self._confirm_button.setFixedSize(30, 30)
        self._delete_button.setFixedSize(30, 30)
        self._save_button.setFixedSize(30, 30)

        self._view_start_date.calendarWidget().setFixedSize(QSize(300, 200))
        self._view_end_date.calendarWidget().setFixedSize(QSize(300, 200))

        return viewing_page
    
    ## Update table based on user input
    def _update_data_viewing(self, start_date: dt.date, end_date: dt.date, categories: List[str], 
                             include_exp: bool, include_rev: bool):
        if categories:
            if "All" in categories:
                cats = CATEGORIES
            else:
                cats = categories
        else:
            cats = CATEGORIES
        
        self._view_df = self._db.get_records(dates = [start_date, end_date], categories = cats, 
                                             group_date = False, group_category = False, 
                                             include_id = True, 
                                             include_exp = include_exp, include_rev = include_rev)
        
        self._table_model._data = self._view_df
        self._table_model.layoutChanged.emit()

    ##----- Summary Page -----##
    def _init_summary_page(self):
        ## Category Selection
        self._summary_category_select = QListWidget()
        self._summary_category_select.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self._summary_category_select.addItems(["All"] + CATEGORIES)
        
        ## Date Input
        self._summary_start_date = QDateEdit()
        self._summary_start_date.setCalendarPopup(True)
        self._summary_end_date = QDateEdit()
        self._summary_end_date.setCalendarPopup(True)

        self._summary_start_date.setDate(self._week_ago)
        self._summary_end_date.setDate(self._yesterday)

        ## Type Input
        self._summary_radio_exp = QRadioButton("Expenditure")
        self._summary_radio_rev = QRadioButton("Revenue")
        self._summary_radio_exp.setChecked(True)
        self._summary_button_group = QButtonGroup()
        self._summary_button_group.addButton(self._summary_radio_exp)
        self._summary_button_group.addButton(self._summary_radio_rev)

        ## Summary Criteria
        self._summary_category_checkbox = QCheckBox("Category")
        self._summary_date_checkbox = QCheckBox("Date")

        ## Apply Button
        self._summary_apply_button = QPushButton()
        self._summary_apply_button.setIcon(self._check_icon)
        
        self._summary_apply_button.clicked\
                                  .connect(lambda: self._display_summary(
                                                       dates = [self._summary_start_date.date().toPyDate(), 
                                                                self._summary_end_date.date().toPyDate()], 
                                                       categories = [item.text() for item in self._summary_category_select.selectedItems()],
                                                       group_date = self._summary_date_checkbox.isChecked(),
                                                       group_category = self._summary_category_checkbox.isChecked(), 
                                                       included_type = self._summary_button_group.checkedButton().text()))

        ## Table & Text & Canvas
        self._canvas = MplCanvas(self)
        self._summary_df = pd.DataFrame()
        self._summary_table = QTableView()
        self._summary_text = QLabel()

    def _display_summary(self, dates: List[dt.date], categories: List[str], 
                         group_date: bool, group_category: bool, 
                         included_type: str):
        
        if not group_date and not group_category:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Please select at least one of Date and Category for summarizing.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.exec_()

            return
        
        if "All" in categories:
            categories = CATEGORIES
        
        if included_type == "Expenditure":
            include_exp = True
            include_rev = False
        else:
            include_exp = False
            include_rev = True

        self._summary_df = self._db.get_records(dates, categories, 
                                                group_date = group_date, 
                                                group_category = group_category, 
                                                include_exp = include_exp,
                                                include_rev = include_rev)
        
        if included_type == "Expenditure":
            total_exp = self._summary_df["Amount"].sum()
            summary_text = f"From {dates[0]} to {dates[1]}, total expenditure is ${total_exp:.2f}."
        
        else:
            total_rev = self._summary_df["Amount"].sum()
            summary_text = f"From {dates[0]} to {dates[1]}, total revenue is ${total_rev:.2f}."

        self._summary_text.setText(summary_text)
        self._summary_table.setModel(TableModel(self._summary_df))

        if group_date and group_category:
            summary_table = self._summary_df.groupby("Category")["Amount"].sum().reset_index()
        elif (not group_date) and group_category:
            summary_table = self._summary_df
        else:
            summary_table = self._db.get_records(dates, categories, 
                                                 group_date = False, 
                                                 group_category = True, 
                                                 include_exp = include_exp,
                                                 include_rev = include_rev)

        self._canvas._ax.clear()
        wedges, texts, autotexts = self._canvas._ax.pie(
            summary_table["Amount"],
            labels = None,
            autopct = "%1.1f%%",
            textprops = dict(color = "black", 
                             fontsize = 4, 
                             fontfamily = "Arial")
        )
        legend = self._canvas._ax.legend(
            wedges, summary_table["Category"],
            title = "Categories",
            loc = "center left",
            bbox_to_anchor = (1, 0.5),
            fontsize = 3,
            title_fontsize = 4
        )
        
        legend.get_frame().set_linewidth(0)
        legend.get_frame().set_edgecolor("none")
        legend.get_frame().set_color(BACKGROUND_COLOR)
        self._canvas._fig.tight_layout()
        self._canvas.draw()

    def create_summary_page(self):
        """Tab for summary and visualization."""
        summary_page = QWidget()
        layout = QVBoxLayout(summary_page)

        ## Home Button
        home_button = QPushButton()
        home_button.setIcon(self._home_icon)
        home_button.setFixedSize(30, 30)
        home_button.clicked.connect(lambda: self._pages.setCurrentWidget(self._home_page))
        layout.addWidget(home_button)
        
        ## Input: category selection
        input_layout = QHBoxLayout()
        category_layout = QVBoxLayout()
        category_label = QLabel("Select categories: ")
        category_layout.addWidget(category_label)
        category_layout.addWidget(self._summary_category_select)
        input_layout.addLayout(category_layout)

        ## Input: dates
        date_layout = QVBoxLayout()
        date_label = QLabel("Select a date range: ")
        start_label = QLabel("From: ")
        date_layout.addWidget(date_label)
        date_layout.addWidget(start_label)
        date_layout.addWidget(self._summary_start_date)

        end_label = QLabel("To: ")
        date_layout.addWidget(end_label)
        date_layout.addWidget(self._summary_end_date)
        date_layout.addStretch()

        input_layout.addLayout(date_layout)

        input_layout.setStretch(0, 1)
        input_layout.setStretch(1, 1)
        layout.addLayout(input_layout)

        ## Input: type
        type_label = QLabel("Type: ")
        type_layout = QHBoxLayout()
        type_layout.addWidget(type_label)
        type_layout.addWidget(self._summary_radio_exp)
        type_layout.addWidget(self._summary_radio_rev)
        type_layout.addStretch()
        layout.addLayout(type_layout)

        ## Criteria
        criteria_layout = QHBoxLayout()
        summary_label = QLabel("Summarize by: ")
        criteria_layout.addWidget(summary_label)
        criteria_layout.addWidget(self._summary_category_checkbox)
        criteria_layout.addWidget(self._summary_date_checkbox)
        criteria_layout.addStretch()
        layout.addLayout(criteria_layout)
        layout.addWidget(self._summary_apply_button)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self._summary_table)
        text_graph_layout = QVBoxLayout()
        text_graph_layout.addWidget(self._summary_text)
        text_graph_layout.addWidget(self._canvas)
        output_layout.addLayout(text_graph_layout)
    
        layout.addLayout(output_layout)

        ## UI
        self._summary_table.setStyleSheet(HIDDEN_WIDGET_STYLE)
        date_label.setStyleSheet(LABEL_STYLE)
        start_label.setStyleSheet(LABEL_STYLE)
        end_label.setStyleSheet(LABEL_STYLE)
        category_label.setStyleSheet(LABEL_STYLE)
        type_label.setStyleSheet(LABEL_STYLE)
        summary_label.setStyleSheet(LABEL_STYLE)
        self._summary_apply_button.setFixedSize(30, 30)

        self._summary_start_date.calendarWidget().setFixedSize(QSize(300, 200))
        self._summary_end_date.calendarWidget().setFixedSize(QSize(300, 200))

        return summary_page
    
    def closeEvent(self, event):
        self._db.close_connection()
        print("Database connection closed")
        event.accept()

## Class for displaying pandas data frames (pd.DataFrame)
class TableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self._data = data
    
    def rowCount(self, parent = None):
        return self._data.shape[0]

    def columnCount(self, parent = None):
        return self._data.shape[1]

    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])

        return None

    def headerData(self, section, orientation, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            elif orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
        
        return None

## Editable table model: displaying pandas data frames, and allowing users to edit rows/columns
class EditableTableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame, categories = CATEGORIES, id_col = 0):
        super().__init__()
        self._data = data
        self._categories = categories
        self._id_col = id_col
        self._modified_rows = {}
    
    def rowCount(self, parent = None):
        return self._data.shape[0]

    def columnCount(self, parent = None):
        return self._data.shape[1]

    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])

        return None

    def setData(self, index, value, role = Qt.ItemDataRole.EditRole):
        if index.isValid() and role == Qt.ItemDataRole.EditRole:
            if index.column() != self._id_col:
                self._data.iloc[index.row(), index.column()] = value
                self._modified_rows[index.row()] = self._data.iloc[index.row()].to_dict()
                self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])
            return True

        return False

    def flags(self, index):
        if index.isValid():
            if index.column() == self._id_col:
                return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
            
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
        
        return Qt.ItemFlag.ItemIsEnabled

    def headerData(self, section, orientation, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._data.columns[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(section)
        
        return None

class TableDelegate(QStyledItemDelegate):
    def __init__(self, categories = CATEGORIES, 
                 id_col = 0, date_col = 1, 
                 category_col = 2, amount_col = 3):
        
        super().__init__()
        self._categories = categories
        self._id_col = id_col
        self._date_col = date_col
        self._category_col = category_col
        self._amount_col = amount_col
    
    def createEditor(self, parent, option, index):
        
        if index.column() == self._date_col:
            editor = QDateEdit(parent)
            editor.setCalendarPopup(True)
            editor.calendarWidget().setFixedSize(QSize(300, 200))
            editor.setDate(dt.datetime.strptime(index.data(), "%Y-%m-%d"))

            return editor
        
        elif index.column() == self._category_col:
            editor = QComboBox(parent)
            editor.addItems(self._categories)

            return editor
        
        elif index.column() == self._amount_col:
            editor = super().createEditor(parent, option, index)
            validator = QDoubleValidator(0.0, float('inf'), 2, parent)
            editor.setValidator(validator)

            return editor
    
        return super().createEditor(parent, option, index)
    
    def setModelData(self, editor, model, index):
        if index.column() == self._date_col:
            model.setData(index, editor.date().toPyDate(), Qt.ItemDataRole.EditRole)
        elif index.column() == self._category_col:
            model.setData(index, editor.currentText(), Qt.ItemDataRole.EditRole)
        elif index.column() == self._amount_col:
            try:
                value = float(editor.text())
                model.setData(index, max(0.0, value), Qt.ItemDataRole.EditRole)
            except ValueError:
                pass

## Class for canvas and graphs
class MplCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 2, height = 2, dpi = 240, bg_color = BACKGROUND_COLOR):
        self._fig = Figure(figsize = (width, height), dpi = dpi)
        self._ax = self._fig.add_subplot(111)
        self._ax.axis("off")
        self._fig.patch.set_facecolor(bg_color)
        super().__init__(self._fig)