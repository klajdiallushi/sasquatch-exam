from my_app.config.mysqlconnection import connect_to_mysql

class Skeptic:
    db_name = 'finalexampy'

    @classmethod
    def mark_as_skeptic(cls, data):
        # Check if the user is already a skeptic
        if cls.has_marked_as_skeptic(data):
            return False
        
        # Remove the user from believers if they are switching to skeptic
        delete_believer_query = "DELETE FROM believers WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;"
        connect_to_mysql(cls.db_name).query_db(delete_believer_query, data)
        
        # Add the user to skeptics
        query = "INSERT INTO skeptics (user_id, sighting_id) VALUES (%(user_id)s, %(sighting_id)s);"
        connect_to_mysql(cls.db_name).query_db(query, data)
        return True

    @classmethod
    def get_skeptic_count(cls, sighting_id):
        query = "SELECT COUNT(*) AS count FROM skeptics WHERE sighting_id = %(sighting_id)s;"
        data = {'sighting_id': sighting_id}
        result = connect_to_mysql(cls.db_name).query_db(query, data)
        return result[0]['count'] if result else 0

    @classmethod
    def has_marked_as_skeptic(cls, data):
        query = "SELECT * FROM skeptics WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;"
        result = connect_to_mysql(cls.db_name).query_db(query, data)
        return len(result) > 0