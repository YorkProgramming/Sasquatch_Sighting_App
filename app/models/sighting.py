from app.config.mysqlconnection import connectToMySQL
from flask import flash, request

from app.models.login import User


class Sighting:
    
    def __init__(self, data):
        self.id = data["id"]
        self.location = data["location"]
        self.describe_sighting = data["describe_sighting"]
        self.num_of_squatch = data["num_of_squatch"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None
        
    @classmethod
    def add_sighting(cls, data):

            query = """
                INSERT INTO 
                
                    sightings 
                    (location, describe_sighting, num_of_squatch, user_id)
                    
                VALUES 
                    (%(location)s, %(describe_sighting)s, %(num_of_squatch)s, %(user_id)s);
            """

            result = connectToMySQL('python_exam').query_db(query, data)

            return result

    @classmethod
    def get_a_sighting(cls, data):

        query = """
            SELECT 
                *
            FROM
                sightings
            JOIN
                users
            ON 
                sightings.user_id = users.id
            WHERE
                sightings.id = %(id)s
        """

        result = connectToMySQL('python_exam').query_db(query, data)
        sighting = cls(result[0])

        row = result[0]
        sighting_user_info = {
            'id': row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at'],
        }
        
        author = User(sighting_user_info)
        
        sighting.creator = author
        
        print("#1", query)
        
        
        
        return sighting


    @classmethod
    def get_all_sightings(cls): 
        
        query = """
                SELECT 
                    *
                FROM
                    sightings
                JOIN
                    users
                ON
                    sightings.user_id = users.id
            """

        result = connectToMySQL('python_exam').query_db(query)
        
        sightings = []
        for row in result:
            one_sighting = cls(row)
            
            sighting_user_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            
            author = User(sighting_user_info)
            
            one_sighting.creator = author
            
            sightings.append(one_sighting)
            print("this is the result", result)
        return sightings
    
    @classmethod
    def get_a_sighting_to_update(cls, data): 
        
        query = """
                SELECT 
                    *
                FROM
                    sightings
                WHERE
                    id = %(id)s
            """

        result = connectToMySQL('python_exam').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update_sighting(cls, data):

        query = """
            UPDATE 
                sightings 
            SET 
                location = %(location)s,
                describe_sighting = %(describe_sighting)s,
                num_of_squatch = %(num_of_squatch)s
            WHERE 
                user_id = %(user_id)s;
        """

        return connectToMySQL('python_exam').query_db(query, data)
    
    @classmethod
    def delete_sighting(cls, id):

        query  = """
            DELETE FROM 
            
                sightings 
                
            WHERE 
                id = %(id)s;
        """
        
        return connectToMySQL('python_exam').query_db(query, {'id': id})
    
    
    @staticmethod
    def validate_new_sighting(sighting):
        is_valid = True

        if len(sighting['location']) < 3:
            flash("Enter a Location", "New Sighting")
            is_valid = False

        if len(sighting['describe_sighting']) < 4:
            flash("Please Describe Your Encounter", "New Sighting")
            is_valid = False
            
        if len(sighting['num_of_squatch']) == 0:
            flash("Please Tell us How Many You Saw", "New Sighting")
            is_valid = False
            
        sighting_date = request.form.get("created_at")
        if sighting_date is None:
            flash("Please Choose an option", "New Sighting")
            is_valid = False
            
        return is_valid