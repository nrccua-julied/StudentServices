import ss_helpers
from ss_helpers import get, post, patch, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import requests


@logTestName
def test_getstudents():
    logger.info("GET /students/{student_key} - Positive Test")

    response = get('/students/966365098')

    responseTest(response.status, 200)

    print (response.body)

@logTestName
def test_getstudents_colleges():
    logger.info("GET /students/{student_key}/colleges - Positive Test")

    response = get('/students/966365098/colleges')

    responseTest(response.status, 200)

    print(response.body)

@logTestName
def test_getstudents_surveyanswers():
    logger.info("GET /students/{student_key}/survey_answers?year=2019&editions=mco,mop - Positive Test")

    response = get('/students/966365098/survey_answers?year=2019&editions=mco,mop')

    responseTest(response.status, 200)

    print (response.body)


@logTestName
def test_poststudents():
    logger.info("POST /students/filter - Positive Test")

    payload = {
      "student_keys": [
        1004523128,
        966365098
          ]
    }
    response = post('/students/filter', payload)
    print(response)
    responseTest(response.status, 200)



@logTestName
def test_patch_students_surveyanswers():
    logger.info("PATCH /students/<student_key>/survey_answers?year=2019&editions=mco,mop - Positive Test")

    payload = {
        "PARENTCOL": [
            "PARCOLNO"
        ],
        "HSPREP": [
            "ADVPLACE",
            "VOTECH",
            "GENRLPREP",
            "GIFTEDPROG",
            "INTLBACCAL"
        ],
        "PROFESSION": [
            "DESIGN",
            "ARCHITECTURE",
            "ENGINEERING"
        ],
        "INTEREST": [
            "BAND"
        ],
        "MBRANCH": [
            "AIRFORCE"
        ],
        "MPLANINFO": [
            "ENLISTHS"
        ],
        "RACE": [
            "NATIVEAM",
            "BLACKRACE",
            "LATINORACE",
            "WHITERACE"
        ],
        "DECSTATE": [
            "DECSTATETX",
            "DECSTATEWA"
        ],
        "ACTSCORE": [
            "36"
        ],
        "SATSCORE": [
            "1598"
        ],
        "GPA": [
            "GRADEAPLUS"
        ],
        "HHLDRLGN": [
            "HHRLNOTKNO"
        ],
        "GRADYEAR": [
            "HSGRAD2021"
        ],
        "MINDSET": [
            "EXPLORATIONMEANING"
        ]
    }


    response = patch('/students/966365098/survey_answers?year=2021&editions=mco,mop', payload)
    responseTest(response.status, 200)

    print (response.body)

