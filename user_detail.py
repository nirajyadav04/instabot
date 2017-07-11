# Class to store user details

class User:
    def __init__(self,name,id):
        self.name = name
        self.id = id

# Class to store recent media of all users


class Recent_Media:
    def __init__(self, name, media_id, media_type ,media_link ,media_likes):
        self.name = name
        self.media_id = media_id
        self.media_type = media_type
        self.media_link = media_link
        self.media_likes = media_likes


# List to store multiple object of class User

user_list = []

# List to store recent media

media_list = []