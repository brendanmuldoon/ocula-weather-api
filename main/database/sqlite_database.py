from main.database.abstract_database import AbstractDatabase
from main.database.sqlite_database_singleton import SQLiteDatabaseSingleton
from main.entity.error_weather_response import ErrorResponse
from main.entity.success_weather_response import SuccessResponse


class SQLiteDatabase(AbstractDatabase):

    def __init__(self):
        self.db_singleton = SQLiteDatabaseSingleton()
        self.connection = self.db_singleton.get_connection()
        self.cursor = self.db_singleton.get_cursor()

    def insert(self, weather_data: SuccessResponse):
        data = {
            'date': weather_data.date,
            'city': weather_data.city,
            'min_temp': float(weather_data.min_temp),
            'max_temp': float(weather_data.max_temp),
            'avg_temp': float(weather_data.avg_temp),
            'humidity': int(weather_data.humidity)
        }

        check_sql = 'SELECT 1 FROM weather WHERE date = ? AND city = ?'
        self.cursor.execute(check_sql, (data['date'], data['city']))
        if self.cursor.fetchone() is not None:
            return ErrorResponse(error_message="Record already exists.", http_code="400")

        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        sql = f'INSERT INTO weather ({columns}) VALUES ({placeholders})'

        # Execute the SQL statement
        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()
        weather_data.http_code = "201"
        return weather_data

    def get_all(self):
        sql = f'SELECT * FROM weather'
        print(self.cursor.execute(sql).fetchall())

