#!/usr/bin/env python

import requests
import json
from question import Question
import jinja2
import shutil
import os


def GetQuestionOfToday():
    response = requests.post(
        url='https://leetcode.cn/graphql/',
        headers={'content-type': 'application/json'},
        data=
        '{"operationName":"questionOfToday", "query": "query questionOfToday {todayRecord {question { questionFrontendId questionTitleSlug } } }" }'
    )
    response_dict = json.loads(response.content)
    title = response_dict['data']['todayRecord'][0]['question'][
        'questionTitleSlug']
    qst = Question(title)
    return qst


def Main():
    qst = GetQuestionOfToday()
    qst_dir = qst.id()
    os.makedirs(qst_dir, exist_ok=True)
    shutil.copy('template/cpp/Makefile', qst_dir)
    shutil.copy('template/cpp/serialize.h', qst_dir)

    # main.cpp
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./template/'))
    main_temp = env.get_template('cpp/main.cpp.template')
    main_text = main_temp.render(func_name=qst.func_name(),
                            param_types=qst.cpp_param_types(),
                            param_names=qst.param_names())
    with open(os.path.join(qst_dir, 'main.cpp'), 'w') as main_file:
        main_file.write(main_text)

    # solution.h
    solution_temp = env.get_template('cpp/solution.h.template')
    solution_text = solution_temp.render(code=qst.cpp_solution())
    with open(os.path.join(qst_dir, 'solution.h'), 'w') as solution_file:
        solution_file.write(solution_text)

    # testcases
    with open(os.path.join(qst_dir, 'testcases'), 'w') as testcases_file:
        for testcase in qst.testcases():
            testcases_file.writelines([i + '\n' for i in testcase])


if __name__ == '__main__':
    Main()
