import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import requests
import datetime

@logTestName
def test_get_high_schools_searchcriteria():
    logger.info("GET /high_schools - Positive Test")
    response = get('/high_schools?search=a%20%26%20m&limit=100&offset=0')

    responseTest(response.status, 200)

    print(response.body)


@logTestName
def test_get_high_schools_hs_id():
    logger.info("GET /high_schools{hs_id} - Positive Test")
    response = get('/high_schools/HS017655')

    responseTest(response.status, 200)

    print(response.body)

