import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import pyodbc

##########Queries the DB to get a user's AuthenticationID to use in the Get AuthenticationID API Call##########
@logTestName
def test_db_authenticationid():
    global Authentication_ID
    global x

    print(ss_helpers.dbserv)
    mydb = pyodbc.connect('Driver={SQL Server};'
                          'Server='+ss_helpers.dbserv+';'
                          'DB=mco;'
                          'user=' + ss_helpers.dbuname +';'
                          'pwd='+ss_helpers.dbpword+';')
    mycursor = mydb.cursor()

##########Getting a user's AuthenticationID################
    mycursor.execute("SELECT * FROM MCO.Api.StudentProfile WHERE EmailAddress = 'julie.dixon@admittedly.org'")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    Authentication_ID = (x[3])
    print (Authentication_ID)
    return Authentication_ID


#########Uses the AuthenticationID from above to test API call Get AuthenticationID - verify 200 response###########
@logTestName
def test_account_verification():
    logger.info("GET /account_verification/?authentication_id={Authentication_ID} - Positive Test")

    response = get('/account_verification/?authentication_id='+ Authentication_ID)

    responseTest(response.status, 200)

    print (response.body)

#########DEB query to get Authentication ID of user to be created in the POST below###########
@logTestName
def test_db_account_verification_create_account():
    global Authentication_ID
    mydb = pyodbc.connect('Driver={SQL Server};'
                            'Server=' + ss_helpers.dbserv + ';'
                            'DB=mco;'
                            'user=' + ss_helpers.dbuname + ';'
                             'pwd=' + ss_helpers.dbpword + ';')
    mycursor = mydb.cursor()

    ##########Getting a user with an isautologin = 0 #########################################3
    mycursor.execute("SELECT TOP 1 eu.AuthenticationID\
                            FROM MCO.Core.EntityUser eu\
                            INNER JOIN MCO.Core.Entity en WITH (NOLOCK) ON eu.EntityKey = en.EntityKey AND en.EntityTypeKey = 3\
                            INNER JOIN MCO.Core.EntityEmail AS em WITH (NOLOCK) ON eu.EntityKey = em.EntityKey\
                            INNER JOIN MCO.Core.Email AS ee WITH (NOLOCK) ON em.EmailKey = ee.EmailKey\
                            where eu.UserID is NULL\
                            order by eu.entitykey desc")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    Authentication_ID = (x[0])
    print(Authentication_ID)

    return Authentication_ID


##########Post to create the user found in the query above######################
@logTestName
def test_account_verification_create_account():
    logger.info("POST /account_verification/create_account?authentication_id={Authentication_ID} - Positive Test")

    payload = {
        "password": "password",
        "is_approved": True,
        "is_active_login": True
    }

    response = post('/account_verification/create_account/?authentication_id=' + Authentication_ID, payload)

    responseTest(response.status, 201)

    print(response.body)




##########Queries the DB to get a user's authenticationid, birthday, and zip whose IsAutoLogin = 0###########
##########The birthday and zip will be used to activate the user###############
@logTestName
def test_db_authenticationid_zip_birth():
    global Authentication_ID
    global Bday
    global Zip
    mydb = pyodbc.connect('Driver={SQL Server};'
                          'Server='+ss_helpers.dbserv+';'
                          'DB=mco;'
                          'user=' + ss_helpers.dbuname + ';'
                           'pwd=' + ss_helpers.dbpword + ';')
    mycursor = mydb.cursor()

##########Getting a user with an isautologin = 0 and the zip and birth to use in the API call below#############
##########If the user has a userid then HasAccount = true otherwise false################
    mycursor.execute("SELECT top 10 cp.entitykey, ce.AuthenticationID, cp.birthdate, ca.zip, ce.isautologin, ce.userid \
        FROM MCO.core.person cp \
        join MCO.core.entityuser ce on cp.entitykey = ce.entitykey \
        join MCO.Core.EntityAddress cea on cp.entitykey = cea.entitykey \
        join MCO.Core.AddressDomestic ca on cea.AddressKey = ca.addresskey \
        join MCO.Core.EntityEmail ee on ce.entitykey = ee.entitykey\
        join MCO.Core.email em on ee.emailkey = em.emailkey\
        where ce.IsAutoLogin = 0 and ca.zip is Not Null and cp.birthdate is Not Null and ce.userid is Not Null \
        order by ce.entitykey desc")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    Authentication_ID = (x[1])
    print (Authentication_ID)

    Bday = (x[2])
    print (Bday)

    Zip = (x[3])
    print (Zip)

    return Authentication_ID
    return Bday
    return Zip


##########Post to Activate the user found in the query above######################
@logTestName
def test_account_verification_validate():
    logger.info("POST /account_verification/validate?authentication_id={Authentication_ID} - Positive Test")


    payload = {
        "zip": Zip,
        "date_of_birth": Bday
    }

    response = post('/account_verification/validate?authentication_id='+ Authentication_ID, payload)

    responseTest(response.status, 200)

    print (response.body)

##########Verifying the user's isautologin is updated to 1####################333
    mydb = pyodbc.connect('Driver={SQL Server};'
                          'Server='+ss_helpers.dbserv+';'
                          'DB=mco;'
                          'user=' + ss_helpers.dbuname + ';'
                          'pwd=' + ss_helpers.dbpword + ';')
    mycursor = mydb.cursor()

    mycursor.execute("select * from MCO.Core.entityuser where authenticationid=?", (Authentication_ID))

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    responseTest(x[3], True)

@logTestName
def test_account_verification_is_auto_login():
    logger.info("GET /account_verification/is_auto_login?authentication_id={Authentication_ID} - Positive Test")

    response = get('/account_verification/is_auto_login?authentication_id='+ Authentication_ID)

    responseTest(response.status, 200)

    print (response.body)
    responseTest(response.body['is_auto_login'], True)


##########Post to Update the password of the user found in the query above######################
##@logTestName
##def test_change_password():
##    logger.info("POST /account_verification/change_password/?authentication_id={Authentication_ID} - Positive Test")
##    head = {
##        'Content-Type': 'application/json',
##        'x-api-key': ss_helpers.environ,
##    }

##    payload = {
##    "password": "password"
##    }

##    response = post('/account_verification/change_password/?authentication_id='+ Authentication_ID, payload)
##    responseTest(response.status, 200)
##    print (response.body)


##########Delete the user's email found in the query above######################
@logTestName
def test_delete_account_verification_email():
    logger.info("DELETE /account_verification?authentication_id={Authentication_ID} - Positive Test")
    head = {
        'Content-Type': 'application/json',
        'x-api-key': ss_helpers.environ,
        }

    response = delete('/account_verification?authentication_id=' + Authentication_ID)

    responseTest(response.status, 200)

    print(response.body)


##########Verifying the user's email is deleted####################333
    mydb = pyodbc.connect('Driver={SQL Server};'
                          'Server='+ss_helpers.dbserv+';'
                          'DB=mco;'
                          'user=' + ss_helpers.dbuname + ';'
                          'pwd=' + ss_helpers.dbpword + ';')
    mycursor = mydb.cursor()

    mycursor.execute("select StudentProfile.AuthenticationID, StudentProfile.EmailAddress from MCO.Api.StudentProfile where authenticationid=?", (Authentication_ID))

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    assert x[1] == None

#########Uses the AuthenticationID from above to test API call Get AuthenticationID - verify 200 response###########
@logTestName
def test_account_verification_error():
    logger.info("GET /account_verification/?authentication_id={Authentication_ID} - Positive Test")

    response = get('/account_verification/?authentication_id=' + Authentication_ID)

    responseTest(response.status, 404)
    responseTest(response.body['error_code'], "ACCOUNT_NOT_FOUND")
    print(response.body)