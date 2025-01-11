from my_app.config.mysqlconnection import connect_to_mysql

class Believer:
    db_name = 'finalexampy'

    @classmethod
    def mark_as_believer(cls, data):
        # Check if the user is already a believer
        if cls.has_marked_as_believer(data):
            return False
        
        # Remove the user from skeptics if they are switching to believer
        delete_skeptic_query = "DELETE FROM skeptics WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;"
        connect_to_mysql(cls.db_name).query_db(delete_skeptic_query, data)
        
        # Add the user to believers
        query = "INSERT INTO believers (user_id, sighting_id) VALUES (%(user_id)s, %(sighting_id)s);"
        connect_to_mysql(cls.db_name).query_db(query, data)
        return True

    @classmethod
    def get_believer_count(cls, sighting_id):
        query = "SELECT COUNT(*) AS count FROM believers WHERE sighting_id = %(sighting_id)s;"
        data = {'sighting_id': sighting_id}
        result = connect_to_mysql(cls.db_name).query_db(query, data)
        return result[0]['count'] if result else 0

    @classmethod
    def has_marked_as_believer(cls, data):
        query = "SELECT * FROM believers WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;"
        result = connect_to_mysql(cls.db_name).query_db(query, data)
        return len(result) > 0