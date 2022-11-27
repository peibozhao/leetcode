#!/usr/bin/env python

import requests
import json
from leetcode import Leetcode
import jinja2
import shutil
import os
import argparse


def Main():
    leetcode = Leetcode()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--frontend-id', type=str)
    args = arg_parser.parse_args()

    if not args.frontend_id is None:
        qst = leetcode.question_of_frontend_id(args.frontend_id)
    else:
        qst = leetcode.question_of_today()
    qst_dir = qst.fronted_id()
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
