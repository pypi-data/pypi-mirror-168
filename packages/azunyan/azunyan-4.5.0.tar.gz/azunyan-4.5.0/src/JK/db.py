class SQLite:
    def __init__(self, database, logger):
        self.database = database
        self.cursor = database.cursor()
        self.logger = logger

    def get(self, table, searchColumn, searchValue):
        try:
            SQLline = F"SELECT * FROM `{table}` WHERE `{searchColumn}` = '{searchValue}';"
            self.cursor.execute(SQLline)
            result = self.cursor.fetchone()
            return result
        except:
            logline = F"SQLite get failed!\n{SQLline}"
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def getall(self, table, searchColumn, searchValue):
        try:
            SQLline = F"SELECT * FROM `{table}` WHERE `{searchColumn}` = '{searchValue}';"
            self.cursor.execute(SQLline)
            result = self.cursor.fetchall()
            return result
        except:
            logline = F"SQLite getall failed!\n{SQLline}"
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def update(self, table, updateColumn, updateValue, searchColumn, searchValue):
        try:
            SQLline = F"UPDATE `{table}` SET `{updateColumn}` = '{updateValue}' WHERE `{searchColumn}` = '{searchValue}';"
            self.cursor.execute(SQLline)
            self.database.commit()
            result = self.cursor.rowcount
            return result
        except:
            logline = F"SQLite update failed!\n{SQLline}"
            self.database.rollback()
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def insert(self, table, columns, values):
        try:
            SQLline = F"""INSERT INTO `{table}` (`{'`,`'.join(columns.split(','))}`) VALUES ('{"','".join(values.split(','))}');"""
            self.cursor.execute(SQLline)
            self.database.commit()
            result = self.cursor.rowcount
            return result
        except:
            logline = F"SQLite insert failed!\n{SQLline}"
            self.database.rollback()
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def query(self, SQLline):
        try:
            self.cursor.execute(str(SQLline))
            result = self.cursor.fetchall()
            return result
        except:
            logline = F"SQLite query failed!\n{str(SQLline)}"
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def exec(self, SQLline):
        try:
            self.cursor.execute(str(SQLline).strip())
            self.database.commit()
            result = self.cursor.rowcount
            return result
        except:
            logline = F"SQLite exec failed!\n{str(SQLline)}"
            self.database.rollback()
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()


class MySQL:
    def __init__(self, database, cursor, logger=False):
        self.database = database
        self.cursor = cursor
        self.logger = logger

    def get(self, table, searchColumn, searchValue):
        try:
            SQLline = F"SELECT * FROM `{table}` WHERE `{searchColumn}` = '{searchValue}';"
            self.database.connect()
            self.cursor.execute(SQLline)
            result = self.cursor.fetchone()
            return result
        except:
            logline = F"SQLite get failed!\n{SQLline}"
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def getall(self, table, searchColumn, searchValue):
        try:
            SQLline = F"SELECT * FROM `{table}` WHERE `{searchColumn}` = '{searchValue}';"
            self.database.connect()
            self.cursor.execute(SQLline)
            result = self.cursor.fetchall()
            return result
        except:
            logline = F"SQLite getall failed!\n{SQLline}"
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def update(self, table, updateColumn, updateValue, searchColumn, searchValue):
        try:
            SQLline = F"UPDATE `{table}` SET `{updateColumn}` = '{updateValue}' WHERE `{searchColumn}` = '{searchValue}';"
            self.database.connect()
            self.cursor.execute(SQLline)
            self.database.commit()
            result = self.cursor.rowcount
            return result
        except:
            logline = F"SQLite update failed!\n{SQLline}"
            self.database.rollback()
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def insert(self, table, columns, values):
        try:
            SQLline = F"""INSERT INTO `{table}` (`{'`,`'.join(columns.split(','))}`) VALUES ('{"','".join(values.split(','))}');"""
            self.database.connect()
            self.cursor.execute(SQLline)
            self.database.commit()
            result = self.cursor.rowcount
            return result
        except:
            logline = F"SQLite insert failed!\n{SQLline}"
            self.database.rollback()
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def query(self, SQLline):
        try:
            self.database.connect()
            self.cursor.execute(str(SQLline))
            result = self.cursor.fetchall()
            return result
        except:
            logline = F"SQLite query failed!\n{str(SQLline)}"
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()

    def exec(self, SQLline):
        try:
            self.database.connect()
            self.cursor.execute(str(SQLline))
            self.database.commit()
            result = self.cursor.rowcount
            return result
        except:
            logline = F"SQLite exec failed!\n{str(SQLline)}"
            self.database.rollback()
            self.database.close()
            try:
                self.logger.exception(logline)
            except:
                print(logline)
            quit()
