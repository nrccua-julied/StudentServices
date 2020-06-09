import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import requests
import datetime

@logTestName
def test_get_campaign_validate_student_pin():
        logger.info("GET /campaign/student/validate/{pin} - Positive Test")
        response = get('/campaign/student/validate/R3GF9Q')

        responseTest(response.status, 200)

        print(response.body)
        responseTest(response.body['student_key'], 966365098)

@logTestName
def test_get_campaign_student_pin():
    logger.info("GET /campaign/student/{pin} - Positive Test")
    response = get('/campaign/student/R3GF9Q')

    responseTest(response.status, 200)

    print(response.body)
    responseTest(response.body['student_key'], 966365098)

@logTestName
def test_get_campaign_campaignname():
    logger.info("GET /campaign/{campaign_name} - Positive Test")
    response = get('/campaign/Culinary-Institute-of-America')

    responseTest(response.status, 200)

    print(response.body)
    responseTest(response.body['campaign_name'], "Culinary-Institute-of-America")

@logTestName
def test_post_campaign_mcocid():
    logger.info("POST /campaign/{mcocid} - Positive Test")

    payload = {
      "campaign_student": {
        "pin": "R3GF9Q",
        "student_key": 966365098,
        "entity_type": "High School Student",
        "first_name": "Julie",
        "last_name": "Admittedly",
        "email_address": "julie.dixon@admittedly.org",
        "street_address": "2500 Salorn Way",
        "city": "Round Rock",
        "state": "TX",
        "zip": "78681",
        "home_phone": "",
        "cell_phone": "5125551111",
        "gender": "F",
        "graduation_year": 2021,
        "high_school_id": "HS017909",
        "sat_score": "1598",
        "act_score": "36",
        "gpa": "A+",
        "majors": "string"
      },
      "extra_questions": {
        "form_title": "Culinary Institute of America",
        "form_key": 11,
        "ccode": 0,
        "rcode": 0,
        "question_answers": [
          {
            "question_alias": "User Defined Option 1",
            "answer_label": "Bachelor's in Food Business Management (Culinary Arts)"
          }
        ]
      }
    }



    response = post('/campaign/1732', payload)

    responseTest(response.status, 200)

    print(response.body)
