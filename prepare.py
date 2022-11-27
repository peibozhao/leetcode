#!/usr/bin/env python

import requests
import json
from leetcode import Leetcode
import jinja2
import shutil
import os
import argparse


def Main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--frontend-id', type=str)
    args = arg_parser.parse_args()

    leetcode = Leetcode()
    if not args.frontend_id is None:
        qst = leetcode.question_of_frontend_id(args.frontend_id)
    else:
        qst = leetcode.question_of_today()

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./template/'))
    # Create question file
    qst_dir = qst.fronted_id()
    os.makedirs(qst_dir, exist_ok=True)
    # testcases
    with open(os.path.join(qst_dir, 'testcases'), 'w') as testcases_file:
        for testcase in qst.testcases():
            testcases_file.writelines([i + '\n' for i in testcase])
    # question.md
    qst_temp = env.get_template('question.md.template')
    qst_text = qst_temp.render(en_title=qst.en_title(),
                               en_content=qst.en_content(),
                               zh_title=qst.zh_title(),
                               zh_content=qst.zh_content())
    with open(os.path.join(qst_dir, 'question.md'), 'w') as qst_file:
        qst_file.write(qst_text)

    # Craete cpp file
    cpp_dir = os.path.join(qst_dir, 'cpp')
    os.makedirs(cpp_dir, exist_ok=True)
    shutil.copy('template/cpp/Makefile', cpp_dir)
    shutil.copy('template/cpp/serialize.h', cpp_dir)
    # main.cpp
    main_temp = env.get_template('cpp/main.cpp.template')
    main_text = main_temp.render(func_name=qst.func_name(),
                                 param_types=qst.cpp_param_types(),
                                 param_names=qst.param_names())
    with open(os.path.join(cpp_dir, 'main.cpp'), 'w') as main_file:
        main_file.write(main_text)
    # solution.h
    solution_temp = env.get_template('cpp/solution.h.template')
    solution_text = solution_temp.render(code=qst.cpp_solution())
    with open(os.path.join(cpp_dir, 'solution.h'), 'w') as solution_file:
        solution_file.write(solution_text)


if __name__ == '__main__':
    Main()
