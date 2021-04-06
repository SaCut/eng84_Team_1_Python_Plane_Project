import pyodbc
from people.passenger import Passenger
from flight_trip import FlightTrip


class DbWrapper:

    # Opens a file called server_info.cfg and pulls connection info from there
    def __init__(self):
        try:
            file_lines = open("server_info.cfg", "r").readlines()
            self.ip = file_lines[0].strip("\n")
            self.uname = file_lines[1].strip("\n")
            self.password = file_lines[2].strip("\n")
            self.db_name = file_lines[3].strip("\n")

            self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' +
                                             f'SERVER={self.ip};DATABASE={self.db_name};'
                                             f'UID={self.uname};PWD={self.password}')

            self.cursor = self.connection.cursor()
        except FileNotFoundError:
            print(f"server_info.config not found!")
            exit(1)

    # Will be used to pull information from the database
    def load_all_passengers(self):
        dict_passengers = {}
        self.cursor.execute("SELECT * FROM passengers")
        temp_passenger_list = self.cursor.fetchall()
        for val in temp_passenger_list:
            passenger = Passenger()
            passenger.make_from_db(val[0], val[1], val[2], val[3], val[4])
            dict_passengers[val[0]] = passenger

        # for passenger in list_passengers:
        #     print(f"{passenger.pid} {passenger.first_name} {passenger.last_name}")

        return dict_passengers

    # Will be used to store information in the database
    def save_all_passengers(self, dict_passengers):
        # passenger = Passenger()
        # passenger.make_from_db(None, "Isobel", "Fitt-Conway", "aasdasdas", "98989922")
        # list_passengers.append(passenger)

        for passenger in dict_passengers.values():
            self.save_single_passenger(passenger, dict_passengers)

        # self.cursor.execute("SELECT * FROM passengers")
        # print(self.cursor.fetchall())

    # allows the creation of a single passenger in the db and adds it to the dict
    def save_single_passenger(self, passenger, passenger_dict):
        first_name = passenger.first_name
        last_name = passenger.last_name
        tax_number = passenger.tax_number
        passport_number = passenger.passport_number

        self.cursor.execute(
            f"INSERT INTO passengers "
            + f"VALUES ('{first_name}', '{last_name}', '{tax_number}', '{passport_number}');")

        self.connection.commit()

        # Update the dictionary so that this is always correct
        self.cursor.execute("SELECT MAX(passenger_id) FROM passengers")
        pid = self.cursor.fetchone()[0]
        psg = Passenger()
        psg.make_from_db(pid, first_name, last_name, tax_number, passport_number)
        passenger_dict[pid] = psg

    def get_flight_passengers(self, flight_id, passenger_list):
        self.cursor.execute(f"SELECT passenger_id FROM flight_order WHERE flight_id = {flight_id}")
        flight_passengers = []
        for entry in self.cursor.fetchall():
            flight_passengers.append(passenger_list[entry[0]])

        return flight_passengers

    def load_all_flights(self, passenger_list):
        list_flights = []
        self.cursor.execute("SELECT * FROM flight_trip_table")
        temp_flight_list = self.cursor.fetchall()
        for val in temp_flight_list:
            flight = FlightTrip()
            flight.make_from_db(val[0], val[1], val[2], val[3], val[4], val[5], self.get_flight_passengers(val[0], passenger_list))
            list_flights.append(flight)

        print(list_flights[0].passenger_list[0])
        return list_flights

    def save_all_flights(self, flight_list):
        for flight in flight_list:

            # If flight doesnt exist at the moment
            if flight.flight_id is None:
                first_name = passenger.first_name
                last_name = passenger.last_name
                tax_number = passenger.tax_number
                passport_number = passenger.passport_number

                self.cursor.execute(
                    f"INSERT INTO flight_trip_table "
                    + f"VALUES ('{first_name}', '{last_name}', '{tax_number}', '{passport_number}');")

                self.connection.commit()


if __name__ == "__main__":
    db = DbWrapper()
    psg = db.load_all_passengers()
    db.load_all_flights(psg)