# As an airport Assistant, I want to be able to create a passenger with a name and Passport number, so that I can add them to a flight
# User should be able to create a new object of the Passenger class
# A passenger should only be created if all information is provided
# class Passenger (inherits from Person)
from people.people import Person


class Passenger(Person):
    def __init__(self):
        super().__init__(None, "passengers")
        self.passport_number = None

    # helpful for debugging
    def __str__(self):
        return f"{self.oid}. {self.first_name} {self.last_name} {self.tax_number} {self.passport_number}"

    def make_from_db(self, oid, first_name, last_name, tax_no, passport_no):
        super().init_person_data(oid, first_name, last_name, tax_no)
        self.passport_number = passport_no
        return self

    def __save_and_regenerate_with_id(self, db_wrapper):
        first_name = self.first_name
        last_name = self.last_name
        tax_number = self.tax_number
        passport_number = self.passport_number

        db_wrapper.cursor.execute(
            f"INSERT INTO passengers "
            + f"VALUES ('{first_name}', '{last_name}', '{tax_number}', '{passport_number}');")

        db_wrapper.connection.commit()

        # Update the dictionary so that this is always correct
        psg = Passenger().make_from_db(self.get_max_id(db_wrapper), first_name, last_name, tax_number, passport_number)

        return psg

    def delete_from_db(self, db_wrapper):
        super().delete_from_db(db_wrapper)
        db_wrapper.cursor.execute(f"DELETE FROM flight_orders WHERE {self.table}_id = {self.oid}")
        db_wrapper.connection.commit()

    def make_manual(self, first_name, last_name, tax_no, passport_no, db_wrapper):
        # make a place holder passenger
        self.make_from_db(None, first_name, last_name, tax_no, passport_no)

        # save it and regenerate it
        return self.__save_and_regenerate_with_id(db_wrapper)
