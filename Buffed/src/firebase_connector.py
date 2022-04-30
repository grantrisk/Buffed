import json
import os
from models import *

import firebase_admin
import requests
from firebase_admin import credentials, firestore, auth

from models import Meal

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


def delete_user(uid: str):
    auth.delete_user(uid)


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


def get_user_active_goal(UID: str):
    goalList = get_user_goals(UID)
    for goal in goalList:
        if goal['is_active']:
            return goal


def set_active_goal_to_false(UID: str):
    active_goal = get_user_active_goal(UID)
    old_goal = Goal(active_goal['goal_id'],
                    active_goal['goal_name'], False,
                    active_goal['calories'],
                    active_goal['macro_nutrients'],
                    active_goal['number_of_meals'],
                    active_goal['desired_weight'])
    update_user_goal(UID, old_goal)


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


def update_meal(UID: str, meal: Meal):
    """
    Updates a meal saved to a user
    :param UID: user UID
    :param meal: meal to be updated
    :return: None
    """
    db.collection(u'users').document(UID).collection(u'saved_meals').document(meal.meal_id).set(vars(meal))


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
def initialize_todays_plan(UID: str):
    """
    Initializes a blank list of meals into users information
    :param UID: user UID
    :return: None
    """
    doc_ref = db.collection(u'users').document(UID)
    field_updates = {'todays_plan': []}
    doc_ref.update(field_updates)

def add_meal_todays_plan(UID: str, meal: Meal):
    """
    Adds a meal to today's plan
    :param UID: user UID
    :param meal: meal to be saved
    :return: None
    """
    meals_list = get_all_meals_todays_plan(UID)
    meals_list.append(meal)
    meal_dict_list = []
    for meal in meals_list:
        meal_dict_list.append(vars(meal))

    doc_ref = db.collection(u'users').document(UID)
    field_updates = {'todays_plan': meal_dict_list}
    doc_ref.update(field_updates)


def remove_meal_todays_plan(UID: str, meal_id: str, meal_type_section: str):
    """
    Remove a meal from today's plan
    :param UID: user UID
    :param meal_id: ID of meal to be removed
    :param meal_type_section: type of meal (breakfast, lunch, etc.)
    :return: None
    """
    meals_list = get_all_meals_todays_plan(UID)
    meal_dict_list = []
    meal_removed = False
    for meal in meals_list:
        meal_dict = vars(meal)
        if not meal_removed and meal_id == meal.meal_id and meal_type_section == meal.meal_type_section:
            meal_removed = True
            continue
        meal_dict_list.append(meal_dict)

    doc_ref = db.collection(u'users').document(UID)
    field_updates = {'todays_plan': meal_dict_list}
    doc_ref.update(field_updates)


def remove_all_meals_todays_plan(UID: str):
    """
    Remove all the meals from today's plan
    :param UID: user UID
    :return: None
    """
    meal_dict_list = []
    doc_ref = db.collection(u'users').document(UID)
    field_updates = {'todays_plan': meal_dict_list}
    doc_ref.update(field_updates)

def get_all_meals_todays_plan(UID: str):
    """
    Get all of a user's saved meals in today's plan
    :param UID: user UID
    :return: list of Meal Objects
    """
    user_dict = db.collection(u'users').document(UID).get().to_dict()
    meal_list = user_dict['todays_plan']
    meals = []
    for meal in meal_list:
        meals.append(Meal.from_dict(meal))
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
# # new_name = "Grant Risk"
# # set_user_info(userUID, FirebaseEnum.NAME, new_name)
#
# from models import Meal
#
# meal1 = Meal("burger", "recipe_0b30b0c29576079a12998d386a42d019", MealType.DINNER.value, "",
#              {"calories": 400, "protein": 20, "carbs": 250, "fat": 50}, [], [])
#
# # add_meal_todays_plan(userUID, meal1)
# remove_meal_todays_plan(userUID, meal1.meal_id)
#
# user_document = get_user_info(userUID)
# print(f"Retrieving modified user document: {user_document}")
