#!/usr/bin/env python

import requests
import json


class Question:
    def __init__(self, title):
        self._title = title
        response = requests.post(url='https://leetcode.cn/graphql/',
                                 headers={'content-type': 'application/json'},
                                 data=self._request_body())
        #  print(str(response.content, encoding='utf8'))
        response_dict = json.loads(response.content)
        question = response_dict['data']['question']
        self._id = question['questionFrontendId']
        for code_snippet in question['codeSnippets']:
            if code_snippet['lang'] == 'C++':
                self._cpp_solution = code_snippet['code']
        meta_dict = json.loads(question['metaData'])
        self._func_name = meta_dict['name']
        self._param_names = [i['name'] for i in meta_dict['params']]
        self._param_types = [i['type'] for i in meta_dict['params']]
        self._testcases = [i.split() for i in eval(question['jsonExampleTestcases'])]

    def _request_body(self):
        return f'{{"operationName":"questionData","variables":{{"titleSlug":"{self._title}"}},"query":"query questionData($titleSlug: String) {{ question(titleSlug: $titleSlug) {{ questionId questionFrontendId categoryTitle boundTopicId title titleSlug content translatedTitle translatedContent isPaidOnly difficulty likes dislikes isLiked similarQuestions contributors {{ username profileUrl avatarUrl __typename }} langToValidPlayground topicTags {{ name slug translatedName __typename }} companyTagStats codeSnippets {{ lang langSlug code __typename }} stats hints solution {{ id canSeeDetail __typename }} status sampleTestCase metaData judgerAvailable judgeType mysqlSchemas enableRunCode envInfo book {{ id bookName pressName source shortDescription fullDescription bookImgUrl pressImgUrl productUrl __typename }} isSubscribed isDailyQuestion dailyRecordStatus editorType ugcQuestionId style exampleTestcases jsonExampleTestcases __typename }}}}"}}'

    def id(self):
        return self._id

    def cpp_solution(self):
        return self._cpp_solution

    def func_name(self):
        return self._func_name

    def param_names(self):
        return self._param_names

    def cpp_param_types(self):
        return [Question._to_cpp_param_name(i) for i in self._param_types]

    def testcases(self):
        return self._testcases

    def _to_cpp_param_name(param_name):
        if param_name not in Question.cpp_param_type_map:
            print('Unkown param type')
            exit(-1)
        return Question.cpp_param_type_map[param_name]

    cpp_param_type_map = {
        'string': 'std::string',
        'string[]': 'std::vector<std::string>',
        'integer': 'int',
        'integer[]': 'std::vector<int>',
        'integer[][]': 'std::vector<std::vector<int>>',
    }