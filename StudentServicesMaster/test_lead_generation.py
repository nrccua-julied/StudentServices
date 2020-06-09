import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import requests


@logTestName
def test_get_lead_generation_mcocid():
    logger.info("GET /lead_generation/{mcocid} - Positive Test")

    response = get('/lead_generation/10692')

    responseTest(response.status, 200)

    print(response.body)

@logTestName
def test_get_lead_generation_student():
    logger.info("GET /lead_generation/student/{authentication_id} - Positive Test")

    response = get('/lead_generation/student/53276DD6-6865-4CCD-B9BF-7D8E10BDCF92')

    responseTest(response.status, 200)

    print(response.body)


@logTestName
def test_post_lead_generation_student():
    logger.info("POST /lead_generation/{mcocid} - Positive Test")


    payload = {
    "lead_generation_student": {
    "authentication_id": "684E13BB-D632-4AE7-8A5C-EF4238DA3108",
    "student_key": 1007377831,
    "entity_type": "High School Student",
    "first_name": "Trey",
    "last_name": "Vassell",
    "email_address": "Trey.Vassell@admittedly.org",
    "street_address": "2500 Salorn Way",
    "city": "Round Rock",
    "state": "TX",
    "zip": "78681",
    "home_phone": "",
    "cell_phone": "5125551111",
    "gender": "M",
    "graduation_year": 2020,
    "high_school_id": "HS017909",
    "date_of_birth": "1990-07-22T00:00:00",
    "sat_score": "1598",
    "act_score": "36",
    "gpa": "A+",
    "majors": "17,26"

    },
  "extra_questions": {
    "form_title": "string",
    "form_key": 91,
    "ccode": 0,
    "rcode": 0,
    "question_answers": [
      {
        "question_alias": "College/Organization Interest Free Text",
        "answer_label": "This is a test"
      }
    ]
  }
}

    response = post('/lead_generation/10692', payload)


    responseTest(response.status, 200)

    print(response.body)
