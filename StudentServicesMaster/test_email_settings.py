import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import pyodbc
import requests


##########Queries the DB to get a user's AuthenticationID to use in the Get AuthenticationID API Call##########
@logTestName
def test_db_authenticationid():
    global Authentication_ID

    mydb = pyodbc.connect('Driver={SQL Server};'
                          'Server='+ss_helpers.dbserv+';'
                          'DB=mco;'
                          'user=' + ss_helpers.dbuname + ';'
                          'pwd=' + ss_helpers.dbpword + ';')
    mycursor = mydb.cursor()

    ##########Getting a user's AuthenticationID################
    mycursor.execute("SELECT * FROM MCO.Api.StudentProfile WHERE EmailAddress = 'julie.dixon@admittedly.org'")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    Authentication_ID = (x[3])
    print(Authentication_ID)
    return Authentication_ID

    mycursor.execute("delete FROM mco.Core.CommunicationSuppress WHERE EntityKey = 966365098")

    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
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


##########Queries the DB to fix the user's email ##########
@logTestName
def test_db_reset():
    global Authentication_ID

    mydb = pyodbc.connect('Driver={SQL Server};'
                          'Server='+ss_helpers.dbserv+';'
                          'DB=mco;'
                          'user=' + ss_helpers.dbuname + ';'
                          'pwd=' + ss_helpers.dbpword + ';')
    mycursor = mydb.cursor()


##########Fixes the users email################
    mycursor.execute("delete FROM mco.Core.CommunicationSuppress WHERE EntityKey = 966365098")

    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")

    mycursor.execute("INSERT INTO mco.Core.Subscription\
           ([CreatedBy],[CreatedDate],[CreatedCase],[EntityKey],[PublicationKey],[SubscriptionDate])\
            VALUES\
           ('webuser','2019-01-09 09:33:30.157','0','966365098','1','2019-01-09 09:34:00'),\
		    ('webuser','2019-01-09 09:33:30.157','0','966365098','2','2019-01-09 09:34:00'),\
		    ('webuser','2019-01-09 09:33:30.157','0','966365098','3','2019-01-09 09:34:00'),\
		    ('webuser','2019-01-09 09:33:30.157','0','966365098','4','2019-01-09 09:34:00'),\
		    ('webuser','2019-01-09 09:33:30.157','0','966365098','5','2019-01-09 09:34:00'),\
		    ('webuser','2019-01-09 09:33:30.157','0','966365098','6','2019-01-09 09:34:00'),\
		    ('webuser','2019-01-09 09:33:30.157','0','966365098','7','2019-01-09 09:34:00'),\
		    ('webuser','2019-01-09 09:33:30.157','0','966365098','9','2019-01-09 09:34:00')")

    mydb.commit()

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

