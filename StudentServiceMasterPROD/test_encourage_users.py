import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import requests
import pyodbc
import datetime
TS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
newuname = "Enc" + TS
newuemailname = "enc" + TS + "@nrccua.org"



@logTestName
def test_post_encourage_user():
    logger.info("POST /encourage_users - Positive Test")

    head = {
        'Content-Type': 'application/json',
        'x-api-key': ss_helpers.environ,
    }

    creds = {
        "first_name": "Encourage",
        "last_name": newuname,
        "address_1": "555 Sunny Street ",
        "address_2": "Address 2",
        "city": "Austin",
        "state": "TX",
        "zip": "78681",
        "cell_phone": 5125551212,
        "fax_phone": 5125551234
}

    response = requests.post(ss_helpers.envUrl +'/encourage_users', headers=head, json=creds)
    print(response)
    print("Create Encourage User: Expected Response Code is 201, Actual Response Code is", response.status_code)
    assert response.status_code == 201
    global MentorEntityKey
    MentorEntityKey = response.json()['entity_key']
    print (MentorEntityKey)
    MentorEntityKey = str(MentorEntityKey)




##################Create a MyOptions User##########################
@logTestName
def test_user_account_signup():
    logger.info("POST mo_environment_url/v2/user_accounts/signup - Positive Test")

    head = {
        'Content-Type': 'application/json'
    }

    creds = {
      "email": newuemailname,
      "password": "password",
      "first_name": "Julietest",
       "last_name": "DixonTesting",
      "date_of_birth": "2003-03-16T00:00:00.000Z",
      "terms": 1
    }

    response = requests.post('https://development-api2.myoptions.org/v2/user_accounts/signup', headers=head, json=creds)


    assert response.status_code == 201
    print(response)
    global StudentEntityKey
    global strStudentEntityKey
    StudentEntityKey = response.json()['student_key']
    print (StudentEntityKey)
    StudentEntityKey = int(StudentEntityKey)
    strStudentEntityKey = str(StudentEntityKey)
##################Login to MyOptions to get the Bearer Token##########################
@logTestName
def test_user_account_login():
    logger.info("POST mo_environment_url/v2/user_accounts/login - Positive Test")

    head = {
        'Content-Type': 'application/json'
    }

    creds = {
    "email": "julie.dixon@admittedly.org",
    "password": "password"
    }

    response = requests.post('https://development-api2.myoptions.org/v2/user_accounts/login', headers=head, json=creds)


    assert response.status_code == 200
    print(response)
    global BEARERTOKEN
    BEARERTOKEN = response.json()['bearer_token']
    print (BEARERTOKEN)



##################Create data for MyOptions User##########################
@logTestName
def test_put_users_id():
    logger.info("PUT users/id - Positive Test")

    head = {
        'Content-Type': 'application/json',
        'Authorization': 'bearer '+BEARERTOKEN
    }

    creds = {
    "profile": {
        "graduation_year": "2021",
        "zip_code": "78681",
        "state": "TX",
        "city": "Round Rock",
        "is_valid_address": False,
        "phone": 5125551111,
        "high_school_id": "HS017909",
        "high_school": "Round Rock High School",
        "parent_one_email": "flname@test.com",
        "parent_one_first_name": "fname",
        "parent_one_last_name": "lname",
        "parent_two_first_name": "ftest",
        "parent_two_last_name": "ltest",
        "is_survey_complete": "true",
        "is_onboarding_complete": "true",
        "college_start_year": "2021",
        "zipcode": "78682",
        "user_type": "high-school",
        "country": "United States of America",
        "high_school_country": "usa"
    },
    "update_increment": 6
}


    response = requests.put('https://development-api2.myoptions.org/v2/users/'+strStudentEntityKey, headers=head, json=creds)


    assert response.status_code == 200
    print(response)



@logTestName
def test_post_encourage_user_relationship():

        head = {
            'Content-Type': 'application/json',
            'x-api-key': ss_helpers.environ,
        }

        creds = {
        "relationship_type_key": 8,
        "entity_key": StudentEntityKey
        }

        response = requests.post(ss_helpers.envUrl +
                                 '/encourage_users/'+MentorEntityKey+'/relationships', headers=head, json=creds)
        print(response)
        print("Create Encourage User Relationship: Expected Response Code is 201, Actual Response Code is", response.status_code)
        assert response.status_code == 201



@logTestName
def test_get_encourage_user():
    logger.info("GET /encourage_users/{entitykey} - Positive Test")

    response = get('/encourage_users/'+MentorEntityKey)

    responseTest(response.status, 200)

    print (response.body)



@logTestName
def test_get_encourage_user_relationship_studentkeys():
    logger.info("GET /encourage_users/{entitykey}/student_keys - Positive Test")

    response = get('/encourage_users/'+MentorEntityKey+'/student_keys?relationship_type_keys=8,9&limit=10&offset=0&graduation_years=2020,2021')

    responseTest(response.status, 200)

    print (response.body)

@logTestName
def test_get_encourage_user_relationship_student_search():
    logger.info("GET /encourage_users/{entitykey}/student_search - Positive Test")

    response = get('/encourage_users/'+MentorEntityKey+'/students_search?relationship_type_keys=8,9&graduation_years=2020,2021,2022&search=a&limit=10&offset=0')

    responseTest(response.status, 200)

    print (response.body)

@logTestName
def test_delete_encourage_user_relationship():
    logger.info(
        "GET /encourage_users/<entity_key>/relationships/<entity_key>?relationship_type_keys=8,9 - Positive Test")

    response = delete('/encourage_users/' + MentorEntityKey + '/relationships/' + strStudentEntityKey)

    responseTest(response.status, 204)

    print(response.body)

@logTestName
def test_get_encourage_user_relationship():
    logger.info("GET /encourage_users/{entitykey}/relationships - Positive Test")

    response = get('/encourage_users/' + MentorEntityKey + '/relationships')

    responseTest(response.status, 200)

    print(response.body)



@logTestName
def test_put_encourage_user():
    logger.info("PUT /encourage_users/{entitykey}- Positive Test")

    head = {
        'Content-Type': 'application/json',
        'x-api-key': ss_helpers.environ,
    }

    creds = {
        "first_name": "EncourageAgain",
        "last_name": newuname,
        "address_1": "555 Sunny Street",
        "address_2": "Address 2",
        "city": "Round Rock",
        "state": "TX",
        "zip": "78681",
        "cell_phone": 5125551212,
        "fax_phone": 5125551234
    }

    response = requests.put(ss_helpers.envUrl + '/encourage_users/'+MentorEntityKey, headers=head,
                            json=creds)
    print(response)



@logTestName
def test_post_encourage_user_relationship_two():

    head = {
        'Content-Type': 'application/json',
        'x-api-key': ss_helpers.environ,
    }

    creds = {
    "relationship_type_key": 8,
    "entity_key": StudentEntityKey
    }

    response = requests.post(ss_helpers.envUrl +
                             '/encourage_users/'+MentorEntityKey+'/relationships', headers=head, json=creds)
    print(response)
    print("Create Encourage User Relationship: Expected Response Code is 201, Actual Response Code is", response.status_code)
    assert response.status_code == 201

@logTestName
def test_post_encourage_user_relationship_three():
    head = {
        'Content-Type': 'application/json',
        'x-api-key': ss_helpers.environ,
    }

    creds = {
        "relationship_type_key": 9,
        "entity_key": StudentEntityKey
    }

    response = requests.post(ss_helpers.envUrl +
                             '/encourage_users/' + MentorEntityKey + '/relationships', headers=head, json=creds)
    print(response)
    print("Create Encourage User Relationship: Expected Response Code is 201, Actual Response Code is",
          response.status_code)
    assert response.status_code == 201






