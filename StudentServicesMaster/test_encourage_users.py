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


@logTestName
def test_post_encourage_user_relationship():
    global StudentEntityKey
    mydb = pyodbc.connect('Driver={SQL Server};'
                              'Server='+ss_helpers.dbserv+';'
                              'DB=mco;'
                              'user=' + ss_helpers.dbuname + ';'
                                                             'pwd=' + ss_helpers.dbpword + ';')
    mycursor = mydb.cursor()

    ##########Getting a user's AuthenticationID################
    mycursor.execute("SELECT top 10 cp.entitykey, ca.zip, cp.birthdate, ce.IsAutoLogin, ce.userid, em.emailkey\
        FROM MCO.Core.person cp\
        join MCO.Core.entityuser ce on cp.entitykey = ce.entitykey\
        join MCO.Core.EntityAddress cea on cp.entitykey = cea.entitykey\
        join MCO.Core.AddressDomestic ca on cea.AddressKey = ca.addresskey\
        join MCO.Core.EntityEmail ee on ce.entitykey = ee.entitykey\
        join MCO.Core.Email em on ee.emailkey = em.emailkey\
        where ce.IsAutoLogin = 1 and ca.zip is Not Null and cp.birthdate is Not Null and ce.userid is Not Null \
        order by ce.entitykey desc")

    myresult = mycursor.fetchall()
    print (myresult)

## need a loop to post all the mentor/student relationships from the students I grabbed from the db above
    i = 0
    for row in myresult:
        StudentEntityKey = (row[i])
        print (StudentEntityKey)
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


        StudentEntityKey = str(StudentEntityKey)


@logTestName
def test_get_encourage_user():
    logger.info("GET /encourage_users/{entitykey} - Positive Test")

    response = get('/encourage_users/'+MentorEntityKey)

    responseTest(response.status, 200)

    print (response.body)

@logTestName
def test_delete_encourage_user_relationship():
    logger.info("GET /encourage_users/<entity_key>/relationships/<entity_key>?relationship_type_keys=8,9 - Positive Test")


    response = delete('/encourage_users/'+MentorEntityKey+'/relationships/'+StudentEntityKey)

    responseTest(response.status, 204)

    print (response.body)



@logTestName
def test_get_encourage_user_relationship():
    logger.info("GET /encourage_users/{entitykey}/relationships - Positive Test")

    response = get('/encourage_users/'+MentorEntityKey+'/relationships')

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





