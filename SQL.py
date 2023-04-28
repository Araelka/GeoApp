import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

con = QSqlDatabase.addDatabase("QSQLITE")
con.setDatabaseName("contacts.sqlite")

if not con.open():
    print("Database Error: %s" % con.lastError().databaseText())
    sys.exit(1)

Query = QSqlQuery()
# Query.exec("DROP TABLE temperature_air")
# Query.exec("DROP TABLE RH")
# Query.exec("DROP TABLE temperature_air")
# Query.exec("DROP TABLE water_content")
# Query.exec("DROP TABLE PAR")
# Query.exec("DROP TABLE rain")
# Query.exec("DROP TABLE current")
# Query.exec("DROP TABLE pressure")
# Query.exec("DROP TABLE gust_speed")
# Query.exec("DROP TABLE wind_speed")
# Query.exec("DROP TABLE solar_radiation")
# Query.exec("DROP TABLE wind_direction")
# Query.exec("DROP TABLE temperature_ground")
# Query.exec("DROP TABLE observations")
# Query.exec("DROP TABLE sensors")
# Query.exec("DROP TABLE type_sensors")

# Query.exec(
#     """
#     DELETE FROM sensors WHERE uid_sensor >= 0;
#     """
# )

Query.exec(
    """
    CREATE TABLE IF NOT EXISTS type_sensors (
        uid_type INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        type VARCHAR(60)
    )
    """
)

Query.exec(
    """
    CREATE TABLE IF NOT EXISTS sensors (
        uid_sensor INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        name VARCHAR(60),
        serial_number INTEGER NOT NULL,
        uid_type INTEGER,
        N_S FLOAT NOT NULL,
        E_W FLOAT NOT NULL,
        installation_date TEXT NOT NULL,
        location VARCHAR(60),
        status BOOLEAN NOT NULL DEFAULT 1,
        FOREIGN KEY (uid_type) REFERENCES type_sensors (uid_type)
    )
    """
)

Query.exec(
    """
    CREATE TABLE IF NOT EXISTS observations (
        uid_observations INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        uid_sensor INTEGER,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        temperature_air FLOAT,
        RH FLOAT,
        water_content FLOAT,
        PAR FLOAT,
        rain FLOAT,
        pressure FLOAT,
        gust_speed FLOAT,
        wind_speed FLOAT,
        solar_radiation FLOAT,
        wind_direction FLOAT,
        temperature_ground FLOAT,
        mark BOOLEAN NOT NULL DEFAULT 1,
        FOREIGN KEY (uid_sensor) REFERENCES sensors (uid_sensor)
    )
    """
)

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS temperature_air (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS RH (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS water_content (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS PAR (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS rain (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS current (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS pressure (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS gust_speed (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS wind_speed (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS solar_radiation (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS wind_direction (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )

# Query.exec(
#     """
#     CREATE TABLE IF NOT EXISTS temperature_ground (
#         number INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#         uid_observations INTEGER,
#         value FLOAT NOT NULL,
#         FOREIGN KEY (uid_observations) REFERENCES observations (uid_observations)
#     )
#     """
# )


# Добавление записи в таблицу

# Query.exec(
#     """
#     INSERT INTO type_sensors (type)
#     VALUES ('Общий'), ('Наземный'), ('Воздушный');
#     """
# )

# Query.exec(
#     """
#     SELECT uid_sensor, uid_type location
#     FROM sensors
#     """
# )

# while Query.next():
#     print(Query.value(0), Query.value(1), Query.value(2), Query.value(3))

# print(con.tables())