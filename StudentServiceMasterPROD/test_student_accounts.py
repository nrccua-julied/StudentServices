import ss_helpers
from ss_helpers import get, post, put, patch, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
#import requests
import datetime
TS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
newuemailname = "nrccua.signup+" + TS + "@gmail.com"


############verify the creation of a user################
@logTestName
def test_post_student_accounts():
    logger.info("POST /student_accounts - Positive Test")

    payload = {
        "survey_year": 2020,
        "is_approved": False,
        "is_active_login": False,
        "email": newuemailname,
        "password": "password",
        "first_name": "f_name",
        "last_name": "lname",
        "date_of_birth": "07-07-2002"
    }

    response = post('/student_accounts', payload)
    print(response.body)
    responseTest(response.status, 201)

    global student_key
    global user_id
    student_key = response.body['student_key']
    user_id = response.body['user_id']
    print(student_key)



############verify the creation of a user################
@logTestName
def test_post_student_accounts_error():
    logger.info("POST /student_accounts - Positive Test")

    payload = {
        "survey_year": 2020,
        "is_approved": False,
        "is_active_login": False,
        "email": "nrccua.signup+999@gmail.com",
        "password": "password",
        "first_name": "f_name",
        "last_name": "a",
        "date_of_birth": "07-07-2002"
    }

    response = post('/student_accounts', payload)
    print(response.body)
    responseTest(response.status, 400)



###############verify user is returned based on email and password###################
@logTestName
def test_post_student_accounts_filter():
    logger.info("POST /student_accounts/filter - Positive Test")

    payload = {
      "email": newuemailname,
      "password": "password"
    }
    response = post('/student_accounts/filter', payload)
    print(response.body)
    responseTest(response.status, 200)

############verify the creation of a user wth is_active_login and is_approved = true################
@logTestName
def test_patch_student_accounts():
    logger.info("PATCH /student_accounts - Positive Test")

    payload = {
    "email": newuemailname,
    "password": "password",
    "old_password_format": False,
    "is_approved": True,
    "is_active_login": True,
    "last_activity_date": "2020-04-21T20:44:41.748Z"
    }
    response = patch('/student_accounts?user_id='+user_id, payload)
    print(response.body)
    responseTest(response.status, 200)

############verify the error message for creation of a duplicate user with is_active_login and is_approved = true################
@logTestName
def test_post_student_accounts3():
    logger.info("POST /student_accounts - Positive Test")

    payload = {
        "survey_year": 2020,
        "is_approved": False,
        "is_active_login": False,
        "email": newuemailname,
        "password": "password",
        "first_name": "f_name",
        "last_name": "lname",
        "date_of_birth": "07-07-2002"
    }
    response = post('/student_accounts', payload)
    print(response.body)
    responseTest(response.status, 409)

