from typing import List
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("static/resources/buffed-9aca2-firebase-adminsdk-ugcpz-3315b655ca.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


class FirebaseConnector:
    """
    Provides an interface to fetch data stored from Firebase.
    """

    def __init__(self, account_info: str, name: str, password: str, email: str, weight: int, height: int):
        """
        Creates an instance of a User object
        :param account_info: user's email
        """
        self.account_info = account_info
        self.name = name
        self.password = password
        self.email = email
        self.weight = weight
        self.height = height


    def get_account_info(self, document) -> str:
        """
        This function returns a string of the users information with every values individual keys.
        :param document: the document of the user
        :return: the users information in string format
        """

        doc_ref = db.collection(u'users').document(document)
        doc = doc_ref.get()
        account_info = doc.to_dict()
        return account_info

    def get_name(self, document):
        """
        This function returns the name for a given user.
        :param document: the document of the user
        :return: the name for the user in string format
        """

        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        user_name = user_doc.to_dict().get('name')
        return user_name

    def get_email(self, document):
        """
        This function returns the email for a given user.
        :param document: the document of the user
        :return: the email for the user in string format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        email = user_doc.to_dict().get('email')
        return email

    def get_weight(self, document):
        """
        This function returns the weight for a given user.
        :param document: the document of the user
        :return: the weight for the user in int format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        weight = user_doc.to_dict().get('weight')
        return weight

    def get_height(self, document):
        """
        This function returns the height for a given user.
        :param document: the document for a given user
        :return: the height for the user in int format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        height = user_doc.to_dict().get('height')
        return height

    def get_activity(self, document):
        """
        This function returns the activity level for a given user.
        :param document: the document for a given user
        :return: the activity level for the user in string format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        activity = user_doc.to_dict().get('activity')
        return activity

    def get_current_goal(self, document):
        """
        This function returns the current goal for a given user.
        :param document: the document for a given user
        :return: the current goal for the user in string format
        """
        user_doc_ref = db.collection(u'users').document(document)
        user_doc = user_doc_ref.get()
        current_goal = user_doc.to_dict().get('current_goal')
        return current_goal

    def get_ingredients(self, document):
        """
        This function pulls all the ingredients down from a given user's document.
        :param document: the document for a given user
        :return: a list of every ingredient a user likes
        """
        pass