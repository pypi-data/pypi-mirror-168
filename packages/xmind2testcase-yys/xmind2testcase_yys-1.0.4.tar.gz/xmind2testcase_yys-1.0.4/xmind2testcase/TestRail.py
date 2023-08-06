#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import logging
import os
from xmind2testcase.utils import get_xmind_testcase_list, get_absolute_path
import re
import pandas as pd
"""
Convert XMind fie to TestRail testcase csv file 

"""


def xmind_to_testrail_csv_file(xmind_file):
    """Convert XMind file to a testrail xlsx file"""
    xmind_file = get_absolute_path(xmind_file)   # 获取xmind的绝对路径
    logging.info('Start converting XMind file(%s) to testrail file...', xmind_file)   # 打印日志信息
    testcases = get_xmind_testcase_list(xmind_file)   # 获取testcase
    # print(testcases)
    fileheader = ["用例名称", "所属产品", "所属模块", "用例等级", "用例类型", "前提条件", "用例步骤", "预期结果"]   # csv表格标题
    testrail_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        testrail_testcase_rows.append(row)

    testrail_file = xmind_file[:-6] + '.xlsx'
    if os.path.exists(testrail_file):
        os.remove(testrail_file)
        # logging.info('The testrail csv file already exists, return it directly: %s', testrail_file)
        # return testrail_file
        df = pd.DataFrame(data=testrail_testcase_rows, columns=fileheader)  # 构造数据
        df.to_excel(testrail_file, index=False)  # 写入文件，设置不需要索引
        logging.info('Convert XMind file(%s) to a testrail xlsx file(%s) successfully!', xmind_file, testrail_file)

    return testrail_file
# def xmind_to_testrail_csv_file(xmind_file):
#     """Convert XMind file to a testrail csv file"""
#     xmind_file = get_absolute_path(xmind_file)   # 获取xmind的绝对路径
#     logging.info('Start converting XMind file(%s) to testrail file...', xmind_file)   # 打印日志信息
#     testcases = get_xmind_testcase_list(xmind_file)   # 获取testcase
#     # print(testcases)
#     # fileheader = ["Section", "Title", "优先级", "版本", "前置条件", "测试步骤", "预期结果"]   # csv表格标题
#     fileheader = ["用例名称", "所属模块", "用例等级", "前提条件", "用例步骤", "预期结果"]   # csv表格标题
#     testrail_testcase_rows = [fileheader]
#     for testcase in testcases:
#         row = gen_a_testcase_row(testcase)
#         testrail_testcase_rows.append(row)
#
#     testrail_file = xmind_file[:-6] + '.csv'
#     if os.path.exists(testrail_file):
#         os.remove(testrail_file)
#         # logging.info('The testrail csv file already exists, return it directly: %s', testrail_file)
#         # return testrail_file
#
#     with open(testrail_file, 'w', encoding='utf8', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerows(testrail_testcase_rows)
#         logging.info('Convert XMind file(%s) to a testrail csv file(%s) successfully!', xmind_file, testrail_file)
#
#     return testrail_file
def xmind_to_testrail_xlsx_file(xmind_file):
    """Convert XMind file to a testrail xlsx file"""
    xmind_file = get_absolute_path(xmind_file)   # 获取xmind的绝对路径
    logging.info('Start converting XMind file(%s) to testrail file...', xmind_file)   # 打印日志信息
    testcases = get_xmind_testcase_list(xmind_file)   # 获取testcase
    # print(testcases)
    fileheader = ["用例名称", "所属产品", "所属模块", "用例等级", "用例类型", "前提条件", "用例步骤", "预期结果"]   # csv表格标题
    testrail_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        testrail_testcase_rows.append(row)

    testrail_file = xmind_file[:-6] + '.xlsx'
    if os.path.exists(testrail_file):
        os.remove(testrail_file)
        # logging.info('The testrail csv file already exists, return it directly: %s', testrail_file)
        # return testrail_file
        df = pd.DataFrame(data=testrail_testcase_rows, columns=fileheader)  # 构造数据
        df.to_excel(testrail_file, index=False)  # 写入文件，设置不需要索引
        logging.info('Convert XMind file(%s) to a testrail xlsx file(%s) successfully!', xmind_file, testrail_file)
    return testrail_file




def gen_a_testcase_row(testcase_dict):
    case_title_list = testcase_dict['name'].split()   # 用例title
    case_title = case_title_list[-1]
    del(case_title_list[-1])
    case_section = '/' + gen_case_section(testcase_dict['suite'])  # 获取Section
    # print("case_title：" + case_title)
    # print(case_title_list)
    for i in case_title_list:
        case_section = case_section + '/'+i

    # print("case_section:" + case_section)

    case_precontion = testcase_dict['preconditions']   # 前置条件
    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])   # 测试步骤和预期结果
    # case_keyword = ''
    case_priority = gen_case_priority(testcase_dict['importance'])  # 优先级
    case_type = gen_case_type(testcase_dict['execution_type'])  # 用例类型
    # print("case_type:" + case_type)
    case_version = testcase_dict['version']
    case_product = testcase_dict['product']
    # print(testcase_dict)
    # case_apply_phase = '迭代测试'
    row = [case_title, case_product, case_section,  case_priority, case_type, case_precontion, case_step, case_expected_result]
    return row


def gen_case_section(section_name):
    if section_name:
        section_name = section_name.replace('（', '(')
        section_name = section_name.replace('）', ')')
    else:
        section_name = '/'
    return section_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    case_expected_result = ''

    for step_dict in steps:
        actions_num = re.compile(r'\d+[、.]').findall(step_dict['actions'])
        expectedresults_num = re.compile(r'\d+[、.]').findall(step_dict['expectedresults'])
        if actions_num == []:
            case_step += str(step_dict['step_number']) + '、' + step_dict['actions'].replace('\n', '').strip() + '\n'
        else:
            case_step += step_dict['actions'].replace('\n', '').strip() + '\n'
        if expectedresults_num == []:
            case_expected_result += str(step_dict['step_number']) + '.0、 ' + \
                                    step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
                if step_dict.get('expectedresults', '') else ''
        else:
            case_expected_result += step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
                if step_dict.get('expectedresults', '') else ''

    return case_step, case_expected_result


def gen_case_priority(priority):
    mapping = {1: 'L0', 2: 'L1', 3: 'L2', 4: 'L3'}
    if priority in mapping.keys():
        return mapping[priority]
    else:
        return 'L2'


def gen_case_type(case_type):
    #“是否实现自动化” 1为否，2为是
    mapping = {1: '功能', 2: '性能', 3: '可靠性', 4: '安全', 5: '兼容性', 6: '用户体验', 7: '可运维'}
    if case_type in mapping.keys():
        return mapping[case_type]
    else:
        return '功能'


if __name__ == '__main__':
    # xmind_file = '../docs/testrail_testcase_template.xmind'
    xmind_file = 'C:/Users/YYS/Desktop/草帽云V1.5.0测试用例.xmind'
    # get_xmind_testcase_list(xmind_file)
    testrail_csv_file = xmind_to_testrail_xlsx_file(xmind_file)
    # print('Conver the xmind file to a testrail csv file succssfully: %s', testrail_csv_file)