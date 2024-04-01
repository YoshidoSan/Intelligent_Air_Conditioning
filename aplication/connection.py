import sqlite3
from sqlite3 import Error


class Connection:
    def __init__(self, db_path):
        self.db_file = db_path
        self.conn = self.create_connection()

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        return conn

    def select_all_records(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        times are in '', rest are numbers
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM records")

        rows = cur.fetchall()
        all_records = []
        for row in rows:
            new_row = [row[1], row[2], row[3], row[4]]
            all_records.append(new_row)
        return all_records

    def select_is_schedule_on(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        all are numbers/bools
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM schedule")

        rows = cur.fetchall()
        is_schedule_on = []
        for row in rows:
            is_schedule_on = [row[1]]
        return is_schedule_on

    def select_continous(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        if values are empty then '', else all are numbers/bools
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM continuous")

        rows = cur.fetchall()
        continous_values = []
        for row in rows:
            continous_values = [row[1], row[2], row[3]]
        return continous_values

    def select_tuning(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        all are numbers/bools
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tuning")

        rows = cur.fetchall()
        tuning_values = []
        for row in rows:
            tuning_values = [row[1], row[2], row[3], row[4]]
        return tuning_values

    def change_tuning_state_temperature(self):
        """
        Change some rows in the tasks table
        :param conn: the Connection object
        all are numbers/bools
        """
        cur = self.conn.cursor()
        cur.execute("UPDATE tuning SET temperature = 1, turned_on_temp = 0 WHERE id = 1")
        self.conn.commit()

    def change_tuning_state_humidity(self):
        """
        Change some rows in the tasks table
        :param conn: the Connection object
        all are numbers/bools
        """
        cur = self.conn.cursor()
        cur.execute("UPDATE tuning SET humidity = 1, turned_on_hum = 0 WHERE id = 1")
        self.conn.commit()



# test = Connection(r'C:\Users\48604\Desktop\studia\sem6\PIAR\projekt\z11\aplication\database.db')
# records = test.select_all_records()
# print(records)
# schedule_on = test.select_is_schedule_on()
# print(schedule_on)
# continous_state = test.select_continous()
# print(continous_state)
# tuning = test.select_tuning()
# print(tuning)
# #test.change_tuning_state_temperature()
# #test.change_tuning_state_humidity()
# tuning = test.select_tuning()
# print(tuning)