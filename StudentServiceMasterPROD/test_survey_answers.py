import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import requests
import datetime

Authentication_ID = '53276DD6-6865-4CCD-B9BF-7D8E10BDCF92'


@logTestName
def test_survey_answers():
    logger.info("POST /survey_answers/filter - Positive Test")
#    responseTest(type(TOKEN), str)

    head = {
        'Content-Type': 'application/json',
        'x-api-key': ss_helpers.environ,
    }

    creds = {
      "student_keys": [
        1004523128,
        966365098
          ],
          "editions": [
            "mco",
            "mop"
          ],
          "year": 2020
}
    response = requests.post(ss_helpers.envUrl +
                             '/survey_answers/filter', headers=head, json=creds)
    for _ in range(3):
        if response.status_code != 504:
            break
        response = requests.post(
            ss_helpers.envUrl + '/users', headers=head, json=creds)
    print("Survey Answers: Expected Response Code is 200, Actual Response Code is", response.status_code)
    assert response.status_code == 200