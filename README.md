# FinDashBoard

A simple daily ledger, where you can track your expenditure/revenue, view your expenditure/revenue history, and get the summary of your past expenditure/revenue.

The project was built with PyQt5 version 5.15.11 and Python 3.12.5. Make sure you install the required packages before you run the `main.py` file.

```bash
pip install -r requirements.txt
python main.py
```

The icons are from flaticon.com.

## Kind Reminders
- If you want to customize the categories of your expenditure/revenue, update `categories.py` file.
- The UI of the app is not well designed. If you want to customize the UI or the theme colors, use `style_sheet.py`.

## Notes

This is my first project with PyQt5, if you have any comment or suggestion for the codes, I would welcome and appreciate it. 

Besides, I would be grateful if you could provide me with some guidances for the UI design. 

Question Jan 6th, 2025: When adding the hovering effect for the `QCalendarWidget`, I tried to add the following lines in my style sheets but it didn't work.

```css
QCalendarWidget QAbstractItemView::item:hover {
  background-color: #f0f0f0;
  border-radius: 5px;
}

QCalendarWidget QAbstractItemView::item:selected {
  background-color: #d8d8d8;
  border-radius: 5px;
}
```
