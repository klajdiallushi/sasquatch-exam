from datetime import datetime
from my_app.config.mysqlconnection import connect_to_mysql
from my_app.models.skeptic import Skeptic
from my_app.models.believer import Believer

class Sighting:
    db_name = 'finalexampy'
    
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.date_of_sighting = data['date_of_sighting']
        self.number_of_sasquatches = data['number_of_sasquatches']
        self.description = data['description']
        self.reported_by = data['reported_by']
        self.reported_by_name = f"{data['first_name']} {data['last_name']}"
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.skeptic_count = Skeptic.get_skeptic_count(self.id)
        self.believer_count = Believer.get_believer_count(self.id)
        
    @classmethod
    def get_all_sightings(cls):
        query = "SELECT * FROM sightings;"
        results = connect_to_mysql(cls.db_name).query_db(query)
        sightings = []
        if results:
            for row in results:
                # Get the name of the user who reported the sighting
                user_query = "SELECT first_name, last_name FROM users WHERE id = %(reported_by)s;"
                user_data = {'reported_by': row['reported_by']}
                user_result = connect_to_mysql(cls.db_name).query_db(user_query, user_data)
                if user_result:
                    row['first_name'] = user_result[0]['first_name']
                    row['last_name'] = user_result[0]['last_name']
                sightings.append(cls(row))
        return sightings
    
    @classmethod
    def create_sighting(cls, data):
        query = """
        INSERT INTO sightings (location, date_of_sighting, number_of_sasquatches, description, reported_by)
        VALUES (%(location)s, %(date_of_sighting)s, %(number_of_sasquatches)s, %(description)s, %(reported_by)s);
        """
        return connect_to_mysql(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_sighting(cls, data):
        query = """
        UPDATE sightings 
        SET location = %(location)s, date_of_sighting = %(date_of_sighting)s, 
            number_of_sasquatches = %(number_of_sasquatches)s, description = %(description)s 
        WHERE id = %(id)s;
        """
        return connect_to_mysql(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_sighting(cls, sighting_id):
        # Delete related records in believers and skeptics tables
        delete_believers_query = "DELETE FROM believers WHERE sighting_id = %(id)s;"
        delete_skeptics_query = "DELETE FROM skeptics WHERE sighting_id = %(id)s;"
        data = {'id': sighting_id}
        connect_to_mysql(cls.db_name).query_db(delete_believers_query, data)
        connect_to_mysql(cls.db_name).query_db(delete_skeptics_query, data)
        
        delete_sighting_query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connect_to_mysql(cls.db_name).query_db(delete_sighting_query, data)

    @classmethod
    def get_sighting_by_id(cls, sighting_id):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        data = {'id': sighting_id}
        result = connect_to_mysql(cls.db_name).query_db(query, data)
        if result:
            row = result[0]
            # Get the name of the user who reported the sighting
            user_query = "SELECT first_name, last_name FROM users WHERE id = %(reported_by)s;"
            user_data = {'reported_by': row['reported_by']}
            user_result = connect_to_mysql(cls.db_name).query_db(user_query, user_data)
            if user_result:
                row['first_name'] = user_result[0]['first_name']
                row['last_name'] = user_result[0]['last_name']
            return cls(row)
        return None