import json
import os
from enum import Enum
from models import *

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
    ACTIVITY = "activity"
    DIET = "diet"


# --------- Account Access ---------
def create_firebase_account(email: str, password: str):
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
        u'activity': "",
        u'diet': []
    }
    db.collection(u'users').document(userUID).set(data)


def sign_in_with_email_and_password(email: str, password: str):
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


def get_user_info(UID: str):
    """
    Retrieves a user's document given a specific UID
    :param UID: users UID
    :return: dictionary response of user's document from firebase
    """
    user_doc_ref = db.collection(u'users').document(UID)
    user_doc = user_doc_ref.get()
    return user_doc.to_dict()


def set_user_info(UID: str, element: Enum, new_value: str):
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


# --------- User Goals ---------
def get_user_goals(UID: str):
    goal_doc = db.collection(u'users').document(UID).collection(u'savedGoals').get()
    goalList = []
    for item in goal_doc:
        goalList.append(item.to_dict())
    return goalList


def create_user_new_goal(UID: str, goal: Goal):
    goal_doc_ref = db.collection(u'users').document(UID).collection(u'savedGoals')
    goal_doc_ref.document(goal.goal_id).set(vars(goal))


def delete_user_goal(UID: str, goal_id: str):
    goal_doc_ref = db.collection(u'users').document(UID).collection(u'savedGoals')
    goal_doc_ref.document(goal_id).delete()


def update_user_goal(UID: str, goal: Goal):
    goal_doc_ref = db.collection(u'users').document(UID).collection(u'savedGoals')
    goal_doc_ref.document(goal.goal_id).set(vars(goal), merge=True)


# --------- Saved Meals ---------
def save_meal(UID: str, meal: Meal):
    """
    Saves a meal to a user's saved meals
    :param UID: user UID
    :param meal: meal to be saved
    :return:
    """
    db.collection(u'users').document(UID).collection(u'saved_meals').document(meal.meal_id).set(meal.to_json())


def remove_meal(UID: str, meal_id: str):
    """
    Remove a meal from a user's saved meals
    :param UID: user UID
    :param meal_id: ID of meal to be removed
    :return: None
    """
    db.collection(u'users').document(UID).collection(u'saved_meals').document(meal_id).delete()


def get_all_meals(UID: str):
    """
    Get all of a user's saved meals
    :param UID: user UID
    :return: stream
    """
    meals = []
    results = db.collection(u'users').document(UID).collection(u'saved_meals').stream()
    for result in results:
        meals.append(Meal.from_dict(result.to_dict()))

    return meals


# --------- Today's Meals ---------
def add_meal_todays_plan(UID: str, meal: Meal):
    """
    Adds a meal to today's plan
    :param UID: user UID
    :param meal: meal to be saved
    :return: None
    """
    db.collection(u'users').document(UID).collection(u'todays_plan').document(meal.meal_id).set(meal.to_json())


def remove_meal_todays_plan(UID: str, meal_id: str):
    """
    Remove a meal from today's plan
    :param UID: user UID
    :param meal_id: ID of meal to be removed
    :return: None
    """
    db.collection(u'users').document(UID).collection(u'todays_plan').document(meal_id).delete()


def get_all_meals_todays_plan(UID: str):
    """
    Get all of a user's saved meals in today's plan
    :param UID: user UID
    :return: stream
    """
    meals = []
    results = db.collection(u'users').document(UID).collection(u'todays_plan').stream()
    for result in results:
        meals.append(Meal.from_dict(result.to_dict()))

    return meals


# # ------------------- Create Account -------------------
# user_email = "riskgrant@gmail.com"
# user_password = "123456"
# # create_firebase_account(user_email, user_password)
#
# # ------------------- Signing in -------------------
# firebase_user = sign_in_with_email_and_password(user_email, user_password)
# # If there is no user this is returned: User sign in response: {'error': {'code': 400, 'message': 'EMAIL_NOT_FOUND',
# # 'errors': [{'message': 'EMAIL_NOT_FOUND', 'domain': 'global', 'reason': 'invalid'}]}}
# print(f"User sign in response: {firebase_user}")
# userUID = firebase_user['localId']
# print(f"User UID in database: {userUID}")
# user_document = get_user_info(userUID)
# print(f"Retrieving initial user document: {user_document}")
#
# # ------------------- Making Changes -------------------
# # new_email = "risk@gmail.com"
# # set_user_info(userUID, FirebaseEnum.EMAIL, new_email)
#
# new_name = "Grant Risk"
# set_user_info(userUID, FirebaseEnum.NAME, new_name)
#
# meals = get_all_meals_todays_plan(userUID)
# for meal in meals:
#     remove_meal_todays_plan(userUID, meal.meal_id)
#
# from models import Meal
#
# meal1 = Meal("burger", str(uuid.uuid4()), MealType.DINNER.value, "",
#              {"calories": 400, "protein": 20, "carbs": 250, "fat": 50}, [], [])
# meal2 = Meal("yogurt", str(uuid.uuid4()), MealType.BREAKFAST.value, "",
#              {"calories": 100, "protein": 5, "carbs": 90, "fat": 40}, [], [])
# meal3 = Meal("banana", str(uuid.uuid4()), MealType.BREAKFAST.value, "",
#              {"calories": 50, "protein": 2, "carbs": 90, "fat": 10}, [], [])
# meal4 = Meal("pizza", str(uuid.uuid4()), MealType.LUNCH.value, "",
#              {"calories": 300, "protein": 20, "carbs": 100, "fat": 70}, [], [])
# meal5 = Meal("hot dog", str(uuid.uuid4()), MealType.DINNER.value, "",
#              {"calories": 120, "protein": 14, "carbs": 75, "fat": 37}, [], [])
#
# add_meal_todays_plan(userUID, meal1)
# add_meal_todays_plan(userUID, meal2)
# add_meal_todays_plan(userUID, meal3)
# add_meal_todays_plan(userUID, meal4)
# add_meal_todays_plan(userUID, meal5)
#
# user_document = get_user_info(userUID)
# print(f"Retrieving modified user document: {user_document}")
#
# meals = get_all_meals_todays_plan(userUID)
# print(f"Retrieving meal one: {meals[0].meal_name}")
# print(f"Retrieving meal two: {meals[1].meal_name}")
