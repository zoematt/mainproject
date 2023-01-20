from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Song:
    db = "main_project"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.img = data['img']
        self.video = data['video']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO songs (name, description, img, video, user_id) VALUES(%(name)s,%(description)s,%(img)s,%(video)s, %(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM songs JOIN users ON users.id = songs.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        list = []
        for i in results:
            r = Song(i)
            u = {
                'id': i['users.id'], 
                'first_name': i['first_name'], 
                'last_name': i['last_name'], 
                'email': i['email'], 
                'password': i['password'], 
                'created_at' : i['users.created_at'],
                'updated_at' : i['users.updated_at']
                }
            User(u)
            r.user = u
            list.append(r)
        print("list")
        print(list)
        return list

    @classmethod
    def get_by_id(cls,data):
        query= "SELECT * FROM songs JOIN users ON users.id = songs.user_id where songs.id= %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        print("creating song")
        r = cls(results[0])
        u = {
            'id': results[0]['users.id'], 
            'first_name': results[0]['first_name'], 
            'last_name': results[0]['last_name'], 
            'email': results[0]['email'], 
            'password': results[0]['password'], 
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at']
            }
        User(u)
        r.user = u
        print(r)
        return r


    @staticmethod
    def is_valid(song_dict):
        valid = True
        flash_string = " field is required and must be at least 3 characters."
        if len(song_dict["name"]) < 3:
            flash("Name " + flash_string)
            valid = False
        if len(song_dict["description"]) < 3:
            flash("Description " + flash_string)
            valid = False
        if len(song_dict["img"]) < 3:
            flash("Img " + flash_string)
            valid = False
        if len(song_dict["video"]) < 3:
            flash("Video" + flash_string)
            valid = False

        return valid

    @classmethod
    def update_song(cls, song_dict):

        # Update the data in the database.
        query = """UPDATE songs
                    SET name = %(name)s, description = %(description)s, img = %(img)s, video = %(video)s
                    WHERE id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query,song_dict)
        return result

    @classmethod
    def delete_song_by_id(cls, song_id):

        data = {"id": song_id}
        query = "DELETE from songs WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query,data)
        return song_id




    