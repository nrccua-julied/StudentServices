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
        1004523153,
        1004523150,
        1004523149,
        1004523148,
        1004523145,
        1004523144,
        1004523143,
        1004523141,
        1004523142,
        1004523140,
        1004523139,
        1004523135,
        1004523134,
        1004523133,
        1004523129,
        1004523130,
        1004523131,
        1004523132,
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

