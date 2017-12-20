import requests
import json
from time import sleep
from sgizmo import *
import pandas as pd

_HTTP = "https://restapi"
_SITE = "surveygizmo.com"
DOMAIN = 'ca'
VERSION = '5'
PARAMS = {"resultsperpage": 500,
          "page": 1}


def _get_data(url, attempts=10, wait_sec=3):

    attempt_count = 0
    for i in range(0, attempts):
        try:
            attempt_count += 1
            output = requests.get(url)
            if output.ok:
                output = output.json()
                return output
        except KeyboardInterrupt:
            pass
        except requests.exceptions.RequestException as e:
            if attempt_count >= attempts:
                print("All attempts failed")
                return
            print(e, "\nTrying again in", wait_sec, "second(s)...")
            sleep(wait_sec)


def _multi_get_data(url, api_token, obj_id='', subobj1=''):

    params = PARAMS
    output_list = []
    output = _get_data(url)
    if output["total_pages"] == 1:
        return output
    else:
        output_list.append(output)
        for i in range(2, output["total_pages"] + 1):
            params["page"] = i
            url = make_url(api_token, obj_id=obj_id, subobj1=subobj1, params=params)
            output = _get_data(url)
            output_list.append(output)
    return output_list


def get_survey_list(api_token):

    url = make_url(api_token)
    data = _get_data(url)
    surveys = data["data"]
    df = pd.DataFrame(surveys)
    return df


def get_survey(api_token, survey_id):

    url = make_url(api_token, obj_id=survey_id)
    data = _get_data(url)
    survey = data["data"]
    return survey


def get_questions(api_token, survey_id):

    url = make_url(api_token, obj_id=survey_id, subobj1="surveyquestion")
    data = _get_data(url)
    questions = data["data"]
    return questions


def get_question_option(api_token, survey_id, question_id):

    url = make_url(api_token, obj_id=survey_id, subobj1='surveyquestion',
                   subobj1_id=question_id, subobj2='surveyoption')
    data = _get_data(url)
    option = data["data"]
    if len(option) > 0:
        for opt in option:
            opt["question_id"] = question_id
    return option


def get_all_survey_options(api_token, survey_id):

    questions = get_questions(api_token, survey_id)
    options = []
    for question in questions:
        qid = question["id"]
        option = get_question_option(api_token, survey_id, qid)
        if len(option) > 0:
            options.append(option)
    return options


def get_survey_responses(api_token, survey_id):

    url = make_url(api_token, obj_id=survey_id, subobj1='surveyresponse')
    data = _multi_get_data(url, api_token=api_token, obj_id=survey_id, subobj1='surveyresponse')
    return data


def make_url(api_token, domain=DOMAIN, version=VERSION, obj='survey',
             obj_id='', subobj1 = '', subobj1_id='', subobj2='', subobj2_id='', params=PARAMS):

    base_url = _HTTP + domain + '.' + _SITE + '/v' + version + '/'
    if api_token[0] == '?':
        api_token = api_token[1:]

    endpoints = ''

    if obj:
        endpoints = endpoints + str(obj)

        if obj_id:
            endpoints = endpoints + '/' + str(obj_id)

            if subobj1:
                endpoints = endpoints + '/' + str(subobj1)

                if subobj1_id:
                    endpoints = endpoints + '/' + str(subobj1_id)

                    if subobj2:
                        endpoints = endpoints + '/' + str(subobj2)

                        if subobj2_id:
                            endpoints = endpoints + '/' + str(subobj2_id)
    else:
        print("No endpoints. Returning None")
        return None

    url = base_url + endpoints + '/?'

    url = url + api_token

    params_list = []
    for key in params.keys():
        s = str(key) + '=' + str(params[key])
        params_list.append(s)
    param_str = '&'.join(params_list)
    param_str = '&' + param_str
    print("Parameters", param_str)

    url = url + param_str
    print("URL:", url)

    return url
