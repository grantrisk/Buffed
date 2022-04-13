import json
import os
from enum import Enum

import firebase_admin
import requests
from firebase_admin import credentials, firestore, auth

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

cred = credentials.Certificate("static/resources/buffed-9aca2-firebase-adminsdk-ugcpz-0d366e7b2c.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


class FirebaseEnum(Enum):
    BIRTH = "birth"
    CURRENT_GOAL = "current_goal"
    EMAIL = 'email'
    GENDER = "gender"
    HEIGHT = "height"
    NAME = "name"
    WEIGHT = "weight"
    MEALS = "meals"


class FirebaseConnector:
    def create_firebase_account(self, email: str, password: str):
        """
        Creates a user account with the given email and password
        :param email: user email
        :param password: user password
        :return: none
        """
        user = firebase_admin.auth.create_user(email=email, password=password)
        userUID = user.uid
        data = {
            u'birth': "",
            u'current_goal': "",
            u'email': email,
            u'gender': "",
            u'height': "",
            u'name': "",
            u'weight': "",
            u'meals': [],
        }
        db.collection(u'users').document(userUID).set(data)

    def sign_in_with_email_and_password(self, email: str, password: str):
        """
        Signs in a user account with the given email and password
        :param email: user email
        :param password: user password
        :return: dictionary response of user object from firebase
        """
        payload = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": "true"
        })
        r = requests.post(rest_api_url,
                          params={"key": FIREBASE_WEB_API_KEY},
                          data=payload)
        return r.json()

    def get_user_info(self, UID: str):
        """
        Retrieves a user's document given a specific UID
        :param UID: users UID
        :return: dictionary response of user's document from firebase
        """
        user_doc_ref = db.collection(u'users').document(UID)
        user_doc = user_doc_ref.get()
        return user_doc.to_dict()

    def set_user_info(self, UID: str, element: Enum, new_value: str):
        """
        Updates a user's information given a specific point in user document
        :param UID: user UID
        :param element: FirebaseEnum enum
        :param new_value: new value being stored in user document
        :return: None
        """
        doc_ref = db.collection(u'users').document(UID)
        field_updates = {element.value: new_value}
        doc_ref.update(field_updates)


# fb_connector = FirebaseConnector()
# # ------------------- Create Account -------------------
# user_email = "riskgranttt@gmail.com"
# user_password = "123456"
# # fb_connector.create_firebase_account(user_email, user_password)
#
# # ------------------- Signing in -------------------
# firebase_user = fb_connector.sign_in_with_email_and_password(user_email, user_password)
# # If there is no user this is returned: User sign in response: {'error': {'code': 400, 'message': 'EMAIL_NOT_FOUND',
# # 'errors': [{'message': 'EMAIL_NOT_FOUND', 'domain': 'global', 'reason': 'invalid'}]}}
# print(f"User sign in response: {firebase_user}")
# userUID = firebase_user['localId']
# print(f"User UID in database: {userUID}")
# user_document = fb_connector.get_user_info(userUID)
# print(f"Retrieving initial user document: {user_document}")
#
# # ------------------- Making Changes -------------------
# new_email = "risk@gmail.com"
# fb_connector.set_user_info(userUID, FirebaseEnum.EMAIL, new_email)
#
# new_name = "Grant"
# fb_connector.set_user_info(userUID, FirebaseEnum.NAME, new_name)
#
# from models import *
#
# meal1 = Meal("burger", MealType.DINNER.value, "", {"calories": 400, "protein": 20, "carbs": 250, "fat": 50}, [], [], [])
# meal2 = Meal("pizza", MealType.DINNER.value, "", {"calories": 500, "protein": 50, "carbs": 300, "fat": 90}, [], [], [])
# meal3 = Meal("sandwich", MealType.LUNCH.value, "", {"calories": 200, "protein": 20, "carbs": 250, "fat": 50}, [], [], [])
# meal4 = Meal("yogurt", MealType.BREAKFAST.value, "", {"calories": 100, "protein": 5, "carbs": 90, "fat": 40}, [], [], [])
# meal1 = vars(meal1)
# meal2 = vars(meal2)
# meal3 = vars(meal3)
# meal4 = vars(meal4)
# new_meals = [meal1, meal2, meal3, meal4]
# fb_connector.set_user_info(userUID, FirebaseEnum.MEALS, new_meals)
#
# user_document = fb_connector.get_user_info(userUID)
# print(f"Retrieving modified user document: {user_document}")
#
# first_meal = user_document['meals'][0]
# print(f"Retrieving meal 1: {first_meal}")
# print(f"Retrieving meal 1 calories: {first_meal['nutrients']['calories']}")
