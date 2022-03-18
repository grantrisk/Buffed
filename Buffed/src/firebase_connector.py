import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

cred = credentials.Certificate("static/resources/buffed-9aca2-firebase-adminsdk-ugcpz-3315b655ca.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


class FB_connector(object):
    """
    Provides an interface to fetch data stored from Firebase.
    """

    def __init__(self, name: str, password: str, email: str, weight: int, height: int, birth: str, gender: str,
                 current_goal: str):
        """
        Creates an instance of a User object
        :param account_info: user's email
        """

        self.name = name
        self.password = password
        self.email = email
        self.weight = weight
        self.height = height
        self.birth = birth
        self.gender = gender
        self.current_goal = current_goal

    def register(self, email, pw):
        """

        :param email:
        :param pw:
        :return:
        """
        auth.create_user(email=email, password=pw)

    def get_account_info(self, document) -> str:
        """
        This method returns a string of the users information with every values individual keys.
        :param document: the document of the user
        :return: the users information in string format
        """

        doc_ref = db.collection(u'users').document(document)
        doc = doc_ref.get()
        account_info = doc.to_dict()
        return account_info

    def get_name(self, document):
        """
        This method returns the name for a given user.
        :param document: the document of the user
        :return: the name for the user in string format
        """

        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        user_name = user_doc.to_dict().get('name')
        return user_name

    def get_email(self, document):
        """
        This method returns the email for a given user.
        :param document: the document of the user
        :return: the email for the user in string format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        email = user_doc.to_dict().get('email')
        return email

    def get_weight(self, document):
        """
        This method returns the weight for a given user.
        :param document: the document of the user
        :return: the weight for the user in int format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        weight = user_doc.to_dict().get('weight')
        return weight

    def get_height(self, document):
        """
        This method returns the height for a given user.
        :param document: the document for a given user
        :return: the height for the user in int format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        height = user_doc.to_dict().get('height')
        return height

    def get_activity(self, document):
        """
        This method returns the activity level for a given user.
        :param document: the document for a given user
        :return: the activity level for the user in string format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        activity = user_doc.to_dict().get('activity')
        return activity

    def get_current_goal(self, document):
        """
        This method returns the current goal for a given user.
        :param document: the document for a given user
        :return: the current goal for the user in string format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        current_goal = user_doc.to_dict().get('current_goal')
        return current_goal

    def get_birthdate(self, document):
        """
        This method returns the birthdate for a given user.
        :param document: the document for a given user
        :return: the birthdate for the user in string format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        current_goal = user_doc.to_dict().get('birthdate')
        return current_goal

    def get_gender(self, document):
        """
        This method returns the gender for a given user.
        :param document: the document for a given user
        :return: the gender for the user in string format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        current_goal = user_doc.to_dict().get('gender')
        return current_goal

    def get_ingredients(self, document):
        """
        This method pulls all the ingredients down from the ingredient collection in a given user's document.
        :param document: the document for a given user
        :return: a list of every ingredient a user likes
        """
        pass

    def change_name(self, document, user_name):
        """
        The method updates the name key in the users document in the firebase.
        :param document:
        :param user_name:
        :return: nothing
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc_ref.update({u'name': user_name})

    def change_email(self, document, user_email):
        """
        This method updates the email key in the users document in the firebase.
        :param document:
        :param user_email:
        :return: nothing
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc_ref.update({u'name': user_email})

    def change_weight(self, document, user_weight):
        """
        This method updates the users weight key in the users document in firebase.
        :param document:
        :param user_weight:
        :return: nothing
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc_ref.update({u'name': user_weight})

    def change_height(self, document, user_height):
        """
        This method updates the users height key in the users document in firebase.
        :param document:
        :param user_height:
        :return: nothing
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc_ref.update({u'name': user_height})

    def change_activity(self, document, user_activity):
        """
        This method updates the users activity key in the users document in firebase.
        :param document:
        :param user_activity:
        :return: nothing
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc_ref.update({u'name': user_activity})

    def change_gender(self, document, user_gender):
        """
        This method updates the users gender key in the users document in firebase.
        :param document:
        :param user_gender:
        :return: nothing
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc_ref.update({u'name': user_gender})

    def change_current_goal(self, document, user_goal):
        """
        This method updates the users current goal in the users document in firebase.
        :param document:
        :param user_goal:
        :return: nothing
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc_ref.update({u'name': user_goal})

    def add_ingredient(self, document):
        """
        This method adds an ingredient into a users ingredient collection.
        :param document:
        :return:
        """
        # user_doc_ref = db.collection(u'users').document(document)
        pass

    def add_goal(self, document, user_goals):
        """
        This method adds a goal into a users goal collection.
        :param document:
        :param user_goals:
        :return:
        """
        pass

    # Change this to add the User object
    def set_person(self, user_name, user_pw, user_email, user_weight, user_height, user_birth, user_gender, user_goal):
        """
        This method adds a User object to the Firebase firestore.
        :param user_goal:
        :param user_gender:
        :param user_name:
        :param user_pw:
        :param user_email:
        :param user_weight:
        :param user_height:
        :param user_birth:
        :return:
        """
        user = FB_connector(name=user_name, password=user_pw, email=user_email, weight=user_weight,
                    height=user_height, birth=user_birth, gender=user_gender, current_goal=user_goal)

        # Set a reference to the user document so we can get the id of the document and add the goal/ingredients
        # collections to it.  Firebase add and set are essentially the same.  See doc for explanation.
        doc_ref = db.collection(u'users').document()
        doc_ref.set(user.to_dict())

        return user

    def __str__(self):
        """
        This method returns the user object back in string format.
        :return:
        """
        return "name: %s password: %s email: %s weight: %s height %s birthdate: %s gender: %s current_goal: %s" % \
               (self.name, self.password, self.email, self.weight, self.height, self.birth, self.gender,
                self.current_goal)

    def to_dict(self):
        """
        This method maps out the user object to add into the users collection.
        :return: person
        """
        person = {
            u'name': self.name,
            u'password': self.password,
            u'email': self.email,
            u'weight': self.weight,
            u'height': self.height,
            u'birth': self.birth,
            u'gender': self.gender,
            u'current_goal': self.current_goal
        }

        return person
