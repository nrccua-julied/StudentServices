import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import requests
import datetime

@logTestName
def test_get_esurvey():
        logger.info("GET /esurvey/in_class_survey/{document_name} - Positive Test")
        response = get('/esurvey/in_class_survey/ACTFL')

        responseTest(response.status, 200)

        print(response.body)
        responseTest(response.body['document_name'], 'ACTFL')