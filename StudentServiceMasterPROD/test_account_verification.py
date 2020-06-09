import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import pyodbc
import datetime
TS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
newuemailname = "nrccua.signup+" + TS + "@gmail.com"



############creation of a user for testing below################
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
    global auth_id
    student_key = response.body['student_key']
    user_id = response.body['user_id']
    auth_id = response.body['authentication_id']
    print(student_key)

#########Uses the AuthenticationID from above to test API call Get AuthenticationID - verify 200 response###########
@logTestName
def test_account_verification():
    logger.info("GET /account_verification/?authentication_id={Authentication_ID} - Positive Test")

    response = get('/account_verification/?authentication_id=' +auth_id)

    responseTest(response.status, 200)

    print (response.body)


##########Post to approve user creation above######################
@logTestName
def test_account_verification_create_account():
    logger.info("POST /account_verification/create_account?authentication_id={Authentication_ID} - Positive Test")

    payload = {
        "password": "password",
        "is_approved": True,
        "is_active_login": True
    }

    response = post('/account_verification/create_account/?authentication_id=' + auth_id, payload)

    responseTest(response.status, 201)

    print(response.body)




##########Post to Activate the user found in the query above######################
@logTestName
def test_account_verification_validate():
    logger.info("POST /account_verification/validate?authentication_id={Authentication_ID} - Positive Test")


    payload = {
       "date_of_birth": "07-07-2002"
    }

    response = post('/account_verification/validate?authentication_id='+ auth_id, payload)

    responseTest(response.status, 200)

    print (response.body)



@logTestName
def test_account_verification_is_auto_login():
    logger.info("GET /account_verification/is_auto_login?authentication_id={Authentication_ID} - Positive Test")

    response = get('/account_verification/is_auto_login?authentication_id='+ auth_id)

    responseTest(response.status, 200)

    print (response.body)
    responseTest(response.body['is_auto_login'], True)



##########Delete the user's email found in the query above######################
@logTestName
def test_delete_account_verification_email():
    logger.info("DELETE /account_verification?authentication_id={Authentication_ID} - Positive Test")
    head = {
        'Content-Type': 'application/json',
        'x-api-key': ss_helpers.environ,
        }

    response = delete('/account_verification?authentication_id=' + auth_id)

    responseTest(response.status, 200)

    print(response.body)



#########Uses the AuthenticationID from above to test API call Get AuthenticationID - verify 200 response###########
@logTestName
def test_account_verification_error():
    logger.info("GET /account_verification/?authentication_id={Authentication_ID} - Positive Test")

    response = get('/account_verification/?authentication_id=' + auth_id)

    responseTest(response.status, 404)
    responseTest(response.body['error_code'], "ACCOUNT_NOT_FOUND")
    print(response.body)