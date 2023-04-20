
from flask import flash
import re

from app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.sightings = []


    @classmethod
    def add_user(cls, data):

            query = """
                INSERT INTO 
                
                    users 
                    (first_name, last_name, email, password)
                    
                VALUES 
                    (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
            """

            result = connectToMySQL('python_exam').query_db(query, data)

            return result


    @classmethod
    def get_by_email(cls, email):
        
        query = """
                    SELECT 
                        * 
                    FROM 
                        users 
                    WHERE 
                        email = %(email)s
                        ;
                """
        
        result = connectToMySQL("python_exam").query_db( query, {'email': email})
        
        
        return cls(result[0]) if result else None
    

    @classmethod
    def get_user(cls, id):

            query = """
                SELECT 
                * 
                FROM
                    users
                WHERE
                    id = %(id)s
            """

            result = connectToMySQL('python_exam').query_db(query, {'id': id})

            return cls(result[0])
        
    @classmethod
    def get_all_users(cls, data):

            query = """
                SELECT 
                * 
                FROM
                    users
                    (id, first_name, last_name, email)
                    
                VALUES 
                    (%(id)s,%(first_name)s, %(last_name)s, %(email)s);
            """

            result = connectToMySQL('python_exam').query_db(query, data)

            return result
        
    @staticmethod
    def validate_registration(user):
        is_valid = True

        if len(user['first_name']) < 3:
            flash("Enter a first name", "register")
            is_valid = False

        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters","register")
            is_valid = False
            
        if User.get_by_email(user['email']):
            flash("Email already taken", "register")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter valid Email Address", "register")
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False

        if user['password'] != user['password_conf']:
            flash("Passwords need to match","register")
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True


        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter valid Email Address", "login")
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "login")
            is_valid = False

        return is_valid