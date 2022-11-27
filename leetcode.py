#!/usr/bin/env python

import requests
import json
from question import Question


class Leetcode:
    def __init__(self):
        self._url = 'https://leetcode.cn/graphql/'
        self._headers = {'content-type': 'application/json'}

    def question_of_today(self):
        request_body = '{"operationName":"questionOfToday", "query": "query questionOfToday {todayRecord {question { questionFrontendId questionTitleSlug } } }" }'
        response = requests.post(url=self._url,
                                 headers=self._headers,
                                 data=request_body)
        response_dict = json.loads(response.content)
        title_slug = response_dict['data']['todayRecord'][0]['question'][
            'questionTitleSlug']
        return Question(title_slug)

    def question_of_frontend_id(self, frontend_id):
        request_body = f'{{"query":" query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {{ problemsetQuestionList( categorySlug: $categorySlug limit: $limit skip: $skip filters: $filters ) {{ hasMore total questions {{ acRate difficulty freqBar frontendQuestionId isFavor paidOnly solutionNum status title titleCn titleSlug topicTags {{ name nameTranslated id slug }} extra {{ hasVideoSolution topCompanyTags {{ imgUrl slug numSubscribed }} }} }} }}}} ","variables":{{"categorySlug":"","skip":0,"limit":1,"filters":{{"searchKeywords":"{frontend_id}"}}}}}}'
        response = requests.post(url=self._url,
                                 headers=self._headers,
                                 data=request_body)
        response_dict = json.loads(response.content)
        questions = response_dict['data']['problemsetQuestionList'][
            'questions']
        if len(questions) == 0:
            print('Empty questions')
            exit(-1)
        title_slug = questions[0]['titleSlug']
        return Question(title_slug)

