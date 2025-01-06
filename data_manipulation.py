import sqlite3 as sql
import datetime as dt
import pandas as pd

from typing import List
from categories import CATEGORIES
import random

class DataHandler:
    def __init__(self, db_name = "expenditrue.db"):
        self._db_name = db_name
        self._connection = sql.connect(db_name)
        self._cursor = self._connection.cursor()
        self._temp_rec = pd.DataFrame(columns = ["id", "Date", "Category", "Amount", "Type"])
        self.create_rec_table()

    def create_rec_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS expenditure (
            id INTEGER PRIMARY KEY,
            Date TEXT NOT NULL,
            Category TEXT NOT NULL,
            Amount REAL NOT NULL,
            Type TEXT NOT NULL
        );
        """

        self._cursor.execute(query)
        self._connection.commit()
    
    def _add_record(self, date: dt.date, category: str, amount: float, type_: str):
        record_id = generate_id(date)
        date = dt.date.strftime(date, "%Y-%m-%d")

        if type_ not in ["Exp", "Rev"]:
            raise ValueError(f"type_ argument must be either 'Exp' or 'Rev', {type_} instead.")
        
        query = """
        INSERT INTO expenditure (id, Date, Category, Amount, Type)
        VALUES (?, ?, ?, ?, ?);
        """

        self._cursor.execute(query, (record_id, date, category, amount, type_))

        ## Perhaps don't need commit every time after insertion.
        self._connection.commit()

    def _add_records(self, records = None):
        if records is not None:
            if not isinstance(records, pd.DataFrame):
                raise TypeError("The records must be pd.DataFrame to insert into the database.")
            
            records.to_sql("expenditure", self._connection, if_exists = "append", index = False)
        
        else:
            self._temp_rec.to_sql("expenditure", self._connection, if_exists = "append", index = False)

    def add_temp_rec(self, date: dt.date, category: str, amount: float, type_: str) -> pd.DataFrame:
        record_id = generate_id(date)

        if type_ not in ["Exp", "Rev"]:
            raise ValueError(f"type_ argument must be either 'Exp' or 'Rev', {type_} instead.")
        
        temp_df = pd.DataFrame({
            "id": [record_id],
            "Date": [date],
            "Category": [category],
            "Amount": [amount],
            "Type": [type_]
        })

        self._temp_rec = safe_concat(self._temp_rec, temp_df)

        return self._temp_rec

    def get_temp_rec(self):
        return self._temp_rec
    
    def get_records(self, dates: List[dt.date] = [], categories: List[str] = CATEGORIES, 
                    group_date = False, group_category = False, 
                    include_id = False, 
                    include_exp = True, include_rev = True) -> pd.DataFrame:
        
        """
        Retrieving records from the database, and grouping data if needed.
        ## Parameters:
        - `dates`: `List[dt.date]`, default `[]`. If it's specified, it must include a start date (`dates[0]`) and an end date (`dates[1]`)
                   and the method returns the records from the start date to the end date (both included); otherwise, the date 
                   range is by default the whole date range.
        - `categories`: `List[str]`, default the preset category list `CATEGORIES`. The method returns the records where the Category is in
                        `categories`.
        - `group_date`: `bool`, default `False`. Whether grouping the data by Date.
        - `group_category`: `bool`, default `False`. Whether grouping the data by Category.
        - `include_id`: `bool`, default `False`. Whether returning the id of the records.
        """

        if dates:
            query = """
                SELECT id, Date, Category, Amount, Type
                FROM expenditure 
                WHERE Date BETWEEN ? AND ?
            """
            self._cursor.execute(query, (dates[0], dates[1]))
        
        else:
            query = """
                SELECT id, Date, Category, Amount, Type
                FROM expenditure 
            """
            self._cursor.execute(query)

        column_names = [desc[0] for desc in self._cursor.description]
        temp = pd.DataFrame(self._cursor.fetchall(), columns = column_names)
        temp = temp.query("Category in @categories").reset_index(drop = True)

        ### Whether including the id column.
        if not include_id:
            temp = temp.drop("id", axis = 1)

        if group_date and group_category:
            records = temp.groupby(["Date", "Category", "Type"])["Amount"].sum()\
                                                                  .reset_index()\
                                                                  .sort_values(by = "Date", ascending = True)\
                                                                  .reset_index(drop = True)
            
        elif group_date and (not group_category):
            records = temp.groupby(["Date", "Type"])["Amount"].sum()\
                                                      .reset_index()\
                                                      .sort_values(by = "Date", ascending = True)\
                                                      .reset_index(drop = True)
            
        elif (not group_date) and group_category:
            records = temp.groupby(["Category", "Type"])["Amount"].sum().reset_index()
        else:
            records = temp.sort_values(by = "Date", ascending = True).reset_index(drop = True)
        
        types = []
        if include_exp:
            types.append("Exp")
        if include_rev:
            types.append("Rev")

        records = records[records["Type"].isin(types)].reset_index(drop = True)
        if include_exp and include_rev:
            records["Type"] = records["Type"].map({"Exp": 1, "Rev": -1})
            records["Amount"] = records["Amount"] * records["Type"]

        records.drop("Type", axis = 1, inplace = True)

        return records

    def get_all_records(self, include_id = False, include_exp = True, include_rev = True):
        query = """
        SELECT id, Date, Category, Amount, Type
        FROM expenditure
        """

        self._cursor.execute(query)
        column_names = [desc[0] for desc in self._cursor.description]

        records = pd.DataFrame(self._cursor.fetchall(), columns = column_names)
        records = records.sort_values(by = "Date", ascending = True).reset_index(drop = True)

        if not include_id:
            records = records.drop("id", axis = 1)
        
        types = []
        if include_exp:
            types.append("Exp")
        if include_rev:
            types.append("Rev")

        records = records[records["Type"].isin(types)].reset_index(drop = True)
        if include_exp and include_rev:
            records["Type"] = records["Type"].map({"Exp": 1, "Rev": -1})
            records["Amount"] = records["Amount"] * records["Type"]

        records.drop("Type", axis = 1, inplace = True)

        return records

    def update_record(self, id_: int, date: dt.date, category: str, amount: float):
        query = """
            UPDATE expenditure
            SET Date = ?, Category = ?, Amount = ?
            WHERE id = ?;
        """

        self._cursor.execute(query, (date, category, amount, id_))
        self._connection.commit()
    
    def delete_records(self, *record_ids):
        self._cursor.executemany(
            "DELETE FROM expenditure WHERE id = ?;",
            [(record_id, ) for record_id in record_ids]
        )
   
        self._connection.commit()

    def close_connection(self):
        self._add_records()
        self._connection.close()


def safe_concat(base: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    """
    assert isinstance(base, pd.DataFrame) or isinstance(base, pd.Series), \
    f"cannot concatenate object of type '{type(base)}';only Series and DataFrame objs are valid"

    assert isinstance(new, pd.DataFrame) or isinstance(new, pd.Series), \
    f"cannot concatenate object of type '{type(new)}';only Series and DataFrame objs are valid"

    assert len(base.columns) == len(new.columns), "Lengths must match to compare"
    assert all(base.columns == new.columns), "Columns must match to concatenate"
    """

    if base.empty:
        return new
    else:
        updated = pd.concat([base, new], ignore_index = True)
        return updated

def generate_id(date: dt.date) -> int:
    """
    Generating unique id for records. 
    Note that if the number of daily records is large, there might be key collisions.
    """
    date_id = dt.date.strftime(date, "%Y%m%d")
    random_id = str(random.random()).split(".")[1][:4]

    return int(date_id + random_id)