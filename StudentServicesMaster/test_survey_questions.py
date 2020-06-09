import ss_helpers
from ss_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger


@logTestName
def test_get_survey_questions():
        logger.info("GET /survey_questions?year=2021&editions=mco,mop - Positive Test")
        response = get('/survey_questions?year=2021&editions=mco,mop')

        responseTest(response.status, 200)

        print(response.body)
