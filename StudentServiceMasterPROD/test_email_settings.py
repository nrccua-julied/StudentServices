import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import pyodbc
import requests
import datetime
TS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
newuname = "SS" + TS
newuemailname = "nrccua.signup+" + TS + "@nrccua.org"



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
    global EntityKey
    EntityKey = response.json()['student_key']

@ logTestName
def test_getstudents():
    logger.info("GET /students/{student_key} - Positive Test")

    response = get('/students/'+EntityKey)

    responseTest(response.status, 200)

    print(response.body)
    global Authentication_ID
    Authentication_ID = response.body['authentication_id']


#########Uses the AuthenticationID from above to test API call - verify 200 response###########
@logTestName
def test_email_settings_authentication_id():
    logger.info("GET /email_settings?authentication_id={Authentication_ID} - Positive Test")

    response = get('/email_settings?authentication_id=' + Authentication_ID)

    responseTest(response.status, 200)

    print(response.body)

#########Uses the AuthenticationID from above to test API call - update email StudentCommunications to False ###########
@logTestName
def test_email_update_settings_authentication_id():
    logger.info("PUT /email_settings?authentication_id={entity_type - Positive Test")

    payload = {
        "StudentCommunications": 0,
        "Partner": 1,
        "Features": 1,
        "Opinion": 1,
        "Scholarship": 1,
        "CollegeOffers": 1,
        "MarketingServices": 1,
        "AOSNotifications": 1,
        "EmailActive": 1
    }

    response = put('/email_settings?authentication_id=' + Authentication_ID, payload)
    print(response)
    responseTest(response.status, 200)


#########Uses the AuthenticationID from above -verifies email is False ###########
@logTestName
def test_email_settings_authentication_id_check1():
    logger.info("GET /email_settings?authentication_id={Authentication_ID} - Positive Test")

    response = get('/email_settings?authentication_id=' + Authentication_ID)

    responseTest(response.status, 200)
    responseTest(response.body['StudentCommunications'], False)
    responseTest(response.body['EmailActive'], True)
    print(response.body)

#########Uses the AuthenticationID from above to test API call - updates ALL emails to False ###########
@logTestName
def test_email_updateALL_settings_authentication_id():
    logger.info("PUT /email_settings?authentication_id={entity_type - Positive Test")

    payload = {
        "StudentCommunications": 0,
        "Partner": 0,
        "Features": 0,
        "Opinion": 1,
        "Scholarship": 1,
        "CollegeOffers": 1,
        "MarketingServices": 1,
        "AOSNotifications": 1,
        "EmailActive": 0
    }

    response = put('/email_settings?authentication_id=' + Authentication_ID, payload)
    responseTest(response.status, 200)
    print(response)

    #########Uses the AuthenticationID from above -verifies ALL email is False ###########
@logTestName
def test_email_settings_authentication_id_check2():
        logger.info("GET /email_settings?authentication_id={Authentication_ID} - Positive Test")

        response = get('/email_settings?authentication_id=' + Authentication_ID)

        responseTest(response.status, 200)
        responseTest(response.body['StudentCommunications'], False)
        responseTest(response.body['EmailActive'], False)
        print(response.body)

###Verify that after setting and email to false an error appears if trying to set it to true
@logTestName
def test_email_error_settings_authentication_id():
    logger.info("PUT /email_settings?authentication_id={entity_type - Negative Test")

    payload = {
        "StudentCommunications": 0,
        "Partner": 0,
        "Features": 0,
        "Opinion": 1,
        "Scholarship": 1,
        "CollegeOffers": 1,
        "MarketingServices": 1,
        "AOSNotifications": 1,
        "EmailActive": 1
    }

    response = put('/email_settings?authentication_id=' + Authentication_ID, payload)
    responseTest(response.status, 501)
    print(response)

#########Get users with emailtype = 3##############
@logTestName
def test_email_settings_entitytype():
    logger.info("GET /email_settings/options?entity_type_key={entity_type - Positive Test")

    # EntityType 3 is a High school student
    response = get('/email_settings/options?entity_type_key=3')

    responseTest(response.status, 200)

    print(response.body)



@logTestName
def test_post_emailsettings_collegeoptout():
    logger.info("POST /email_settings/college_opt_out - Positive Test")

    payload = {
	"authentication_id": Authentication_ID,
	"mcocid": 10064
}

    response = post('/email_settings/college_opt_out', payload)
    print(response)
    responseTest(response.status, 200)

