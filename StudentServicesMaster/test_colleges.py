import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import requests
import datetime

Authentication_ID = '53276DD6-6865-4CCD-B9BF-7D8E10BDCF92'

@logTestName
def test_post_colleges_filter():
    logger.info("POST /colleges/filter - Positive Test")

    payload = {
    "mcocids": [
        342,
        306,
        308
        ]
    }
    response = post('/colleges/filter', payload)
    print(response)
    responseTest(response.status, 200)

@logTestName
def test_get_colleges_mcocid():
        logger.info("GET /colleges - Positive Test")
        response = get('/colleges/1466')

        responseTest(response.status, 200)

        print(response.body)

        responseTest(response.body['mcocid'], 1466)

@logTestName
def test_get_colleges_offset_limit_search():
        logger.info("GET /colleges - Positive Test")
        response = get('/colleges?offset=0&limit=10&search=texas')

        responseTest(response.status, 200)

        print(response.body)

