import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import requests
import datetime

@logTestName
def test_get_college_matching():
        logger.info("GET /college_matching/trigger - Positive Test")

        payload = {
            "student_key": 966365098
        }

        response = post('/college_matching/trigger', payload)

        responseTest(response.status, 202)
