# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
  @ Time     : 2019/7/9 下午2:00
  @ Author   : Vodka
  @ File     : extractTriple .py
  @ Software : PyCharm
"""
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


# 生成 人物 的三元组
path = open('../data/dataset/person.json')
fr = json.load(path,encoding='utf-8')
path.close()

fw = open('../data/dataset/triple_person.nt','w')
for item in fr:
    iri = "<http://ke.course/rtk#"+str(item[u'姓名'])+'> '
    fw.write(iri + '<http://ke.course/rtk#姓名>   ' + "\"" + item[u'姓名'] + "\"    .\n")
    fw.write(iri + '<http://www.w3.org/2000/01/rdf-schema#lable>   ' + "\"" + item[u'姓名'] + "\"    .\n")
    fw.write(iri + '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#人物>   .\n')

    base_property = [u'姓名',u'拼音',u'性别',u'是否虚构',u'字',u'现代籍贯',u'介绍']
    for _index,property_name in enumerate(item):

        # 基本属性：姓名、拼音、性别、是否虚构、字、现代籍贯、介绍
        if (property_name in base_property) and (item[property_name] != 'None'):
            if property_name == u'姓名':
                continue
            fw.write(iri + '<http://ke.course/rtk#' + str(property_name) + ">   \"" + item[property_name] + "\"   .\n")

        # 基本属性：出生死亡年份  "？ - 196"
        if property_name == u'生卒' and item[property_name] != 'None' and item[property_name] != '？ - ？':
            years = str(item[property_name]).replace(' ','').split('-')
            if years[0] != u'？':
                fw.write(iri + '<http://ke.course/rtk#出生年份>   \"' + years[0] + "\"^^<http://www.w3.org/2001/XMLSchema#date>   .\n")
            if years[1] != u'？':
                fw.write(iri + '<http://ke.course/rtk#死亡年份>   \"' + years[1] + "\"^^<http://www.w3.org/2001/XMLSchema#date>   .\n")

        # 对象属性：效忠势力、古代籍贯
        if property_name == u'效忠势力' and item[property_name] != 'None':
            fw.write(iri + '<http://ke.course/rtk#效忠势力>   <http://ke.course/rtk#' + item[property_name] + ">   .\n")
        if property_name == u'古代籍贯' and item[property_name] != 'None':
            fw.write(iri + '<http://ke.course/rtk#古代籍贯>   <http://ke.course/rtk#' + item[property_name] + ">   .\n")


    # 潜在属性：别名
    pattern = re.compile(u'‘([\u4e00-\u9fa5]+)‘')
    if pattern.findall(item[u'介绍']) != [] :
        if item[u'姓名'] not in [u'刘宏[汉灵帝]',u'苗泽',u'杨琦',u'臧旻',u'张机',u'蔡琰',u'曹芳',u'曹休',u'曹植',u'郭女王',u'刘馥',u'夏侯恩',u'夏侯令女',u'徐庶',u'荀彧',u'关银屏',u'黄月英',u'诸葛瞻',u'丁奉',u'鲁肃',u'陆景',u'华雄',u'李儒',u'张尚[西晋]']:
            fw.write(iri + '<http://ke.course/rtk#别名>   \"' + pattern.findall(item[u'介绍'])[0] + "\"   .\n")


    # 潜在属性：父母兄弟姐妹子女配偶
    # 父母
    pattern = re.compile(item[u'姓名'][0] + u'([\u4e00-\u9fa5]+)之([子女]+)')
    if pattern.findall(item[u'介绍']) != [] and len(pattern.findall(item[u'介绍'])[0][0]) < 4 and item[u'姓名'][0]+pattern.findall(item[u'介绍'])[0][0]!=item[u'姓名']:
        # print item[u'姓名'] + '   ' + item[u'姓名'][0] + pattern.findall(item[u'介绍'])[-1]
        fw.write(iri + '<http://ke.course/rtk#父母>   <http://ke.course/rtk#' + item[u'姓名'][0] + pattern.findall(item[u'介绍'])[0][0] + ">   .\n")
    # 子女
    pattern = re.compile(item[u'姓名'][0] + u'([\u4e00-\u9fa5]+)之([父母]+)')
    if pattern.findall(item[u'介绍']) != [] and len(pattern.findall(item[u'介绍'])[0][0]) < 4 and item[u'姓名'][0]+pattern.findall(item[u'介绍'])[0][0]!=item[u'姓名']:
        if item[u'姓名'] == u'曹腾':
            fw.write(iri + '<http://ke.course/rtk#子女>   <http://ke.course/rtk#曹嵩>   .\n')
            continue
        # print item[u'姓名'] + '   ' + item[u'姓名'][0] + pattern.findall(item[u'介绍'])[-1]
        fw.write(iri + '<http://ke.course/rtk#子女>   <http://ke.course/rtk#' + item[u'姓名'][0] + pattern.findall(item[u'介绍'])[0][0] + ">   .\n")
    # 兄弟
    pattern = re.compile(item[u'姓名'][0] + u'([\u4e00-\u9fa5]+)之([兄弟]+)')
    if pattern.findall(item[u'介绍']) != [] and len(pattern.findall(item[u'介绍'])[0][0]) < 4 and item[u'姓名'][0] + pattern.findall(item[u'介绍'])[0][0] != item[u'姓名']:
        # print item[u'姓名'] + '   ' + item[u'姓名'][0] + pattern.findall(item[u'介绍'])[-1]
        fw.write(iri + '<http://ke.course/rtk#兄弟>   <http://ke.course/rtk#' + item[u'姓名'][0] + pattern.findall(item[u'介绍'])[0][0] + ">   .\n")


fw.close()


# 生成 事件 的三元组
path = open('../data/dataset/event.json')
fr = json.load(path,encoding='utf-8')
path.close()

fw = open('../data/dataset/triple_event.nt','w')
for item in fr:
    iri = "<http://ke.course/rtk#"+str(item[u'事件名'])+'> '
    fw.write(iri + '<http://ke.course/rtk#事件名>   ' + "\"" + item[u'事件名'] + "\"    .\n")
    fw.write(iri + '<http://www.w3.org/2000/01/rdf-schema#lable>   ' + "\"" + item[u'事件名'] + "\"    .\n")
    fw.write(iri + '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#事件>   .\n')

    base_property = [u'事件名',u'提示',u'历史',u'时间',u'简述']
    for _index,property_name in enumerate(item):

        # 基本属性：事件名、提示、历史、发生时间、介绍
        if (property_name in base_property) and (item[property_name] != 'None'):
            if property_name == u'事件名':
                continue
            if property_name == u'时间':
                fw.write(iri + '<http://ke.course/rtk#发生时间>   \"' + str(item[property_name]).replace('年','') + "\"^^<http://www.w3.org/2001/XMLSchema#date>   .\n")
            elif property_name == u'简述':
                fw.write(iri + '<http://ke.course/rtk#介绍>   \"' + item[property_name] + "\"   .\n")
            else:
                fw.write(iri + '<http://ke.course/rtk#' + str(property_name) + ">   \"" + item[property_name] + "\"   .\n")

        # 对象属性：事件地点、对应章节、涉及人物
        if property_name == u'地点' and item[property_name] != 'None':
            fw.write(iri + '<http://ke.course/rtk#事件地点>   <http://ke.course/rtk#' + item[property_name] + ">   .\n")
        if property_name == u'章节' and item[property_name] != 'None':
            fw.write(iri + '<http://ke.course/rtk#对应章节>   <http://ke.course/rtk#' + item[property_name] + ">   .\n")
        if property_name == u'涉及人物' and item[property_name] != 'None':
            for name in item[property_name]:
                fw.write(iri + '<http://ke.course/rtk#涉及人物>   <http://ke.course/rtk#' + name + ">   .\n")
fw.close()


# 生成 地点 的三元组
path = open('../data/dataset/person.json')
fr = json.load(path,encoding='utf-8')
path.close()
visited_place = {}
fw = open('../data/dataset/triple_place.nt','w')
# 州郡
for item in fr:
    zhou_pattern = re.compile(u'([\u4e00-\u9fa5]+)州')
    jun_pattern = re.compile(u'([\u4e00-\u9fa5]+)郡')
    if zhou_pattern.findall(item[u'古代籍贯']) != [] and visited_place.has_key(zhou_pattern.findall(item[u'古代籍贯'])[0] + u'州') == False:
        name_zhou = zhou_pattern.findall(item[u'古代籍贯'])[0] + u'州'
        iri = "<http://ke.course/rtk#" + name_zhou + '> '
        fw.write(iri + '<http://ke.course/rtk#地名>   ' + "\"" + name_zhou + "\"    .\n")
        fw.write(iri + '<http://www.w3.org/2000/01/rdf-schema#lable>   ' + "\"" + name_zhou + "\"    .\n")
        fw.write(iri + '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#州>   .\n')
        visited_place[name_zhou] = 1
    if jun_pattern.findall(item[u'古代籍贯']) != [] and visited_place.has_key(jun_pattern.findall(item[u'古代籍贯'])[0] + u'郡') == False:
        name_jun = jun_pattern.findall(item[u'古代籍贯'])[0] + u'郡'
        iri = "<http://ke.course/rtk#" + name_jun + '> '
        fw.write(iri + '<http://ke.course/rtk#地名>   ' + "\"" + name_jun + "\"    .\n")
        fw.write(iri + '<http://www.w3.org/2000/01/rdf-schema#lable>   ' + "\"" + name_jun + "\"    .\n")
        fw.write(iri + '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#郡>   .\n')
        visited_place[name_jun] = 1
# 普通地点
for item in fr:
    if item[u'古代籍贯'] != 'None' and visited_place.has_key(item[u'古代籍贯']) == False:
        visited_place[item[u'古代籍贯']] = 1
        # 基本属性：地名、现代地名、行政级别
        iri = "<http://ke.course/rtk#"+str(item[u'古代籍贯'])+'> '
        fw.write(iri + '<http://ke.course/rtk#地名>   ' + "\"" + item[u'古代籍贯'] + "\"    .\n")
        fw.write(iri + '<http://www.w3.org/2000/01/rdf-schema#lable>   ' + "\"" + item[u'古代籍贯'] + "\"    .\n")
        fw.write(iri + '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#地点>   .\n')
        fw.write(iri + '<http://ke.course/rtk#现代地名>   \"' + str(item[u'现代籍贯']) + '\"   .\n')
        if u'郡' in item[u'古代籍贯'] and item[u'古代籍贯'][-1]!=u'郡':
            fw.write(iri + '<http://ke.course/rtk#行政级别>   \"县\"   .\n')
        elif u'郡' in item[u'古代籍贯']:
            fw.write(iri + '<http://ke.course/rtk#行政级别>   \"郡\"   .\n')
        elif u'州' in item[u'古代籍贯'] and item[u'古代籍贯'][-1]!=u'州':
            fw.write(iri + '<http://ke.course/rtk#行政级别>   \"郡\"   .\n')
        elif u'州' in item[u'古代籍贯']:
            fw.write(iri + '<http://ke.course/rtk#行政级别>   \"州\"   .\n')
        else:
            fw.write(iri + '<http://ke.course/rtk#行政级别>   \"县\"   .\n')
        # 对象属性：所属州、所属郡
        zhou_pattern = re.compile(u'([\u4e00-\u9fa5]+)州')
        jun_pattern = re.compile(u'([\u4e00-\u9fa5]+)郡')
        if zhou_pattern.findall(item[u'古代籍贯']) != []:
            fw.write(iri + '<http://ke.course/rtk#所属州>   <http://ke.course/rtk#' + zhou_pattern.findall(item[u'古代籍贯'])[0] + u'州' + '>  .\n')
        if jun_pattern.findall(item[u'古代籍贯']) != [] :
            fw.write(iri + '<http://ke.course/rtk#所属郡>   <http://ke.course/rtk#' + jun_pattern.findall(item[u'古代籍贯'])[0] + u'郡' + '>  .\n')

fw.close()

# 生成 势力 的三元组
fw = open('../data/dataset/triple_power.nt','w')
fw.write('<http://ke.course/rtk#东汉>    <http://ke.course/rtk#势力名称>   "东汉"  .\n')
fw.write('<http://ke.course/rtk#东汉>    <http://www.w3.org/2000/01/rdf-schema#lable>   "东汉"  .\n')
fw.write('<http://ke.course/rtk#东汉>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')
fw.write('<http://ke.course/rtk#东汉>    <http://ke.course/rtk#建立时间>   "25"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')
fw.write('<http://ke.course/rtk#东汉>    <http://ke.course/rtk#灭亡时间>   "220"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')

fw.write('<http://ke.course/rtk#魏>    <http://ke.course/rtk#势力名称>   "魏"  .\n')
fw.write('<http://ke.course/rtk#魏>    <http://www.w3.org/2000/01/rdf-schema#lable>   "魏"  .\n')
fw.write('<http://ke.course/rtk#魏>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')
fw.write('<http://ke.course/rtk#魏>    <http://ke.course/rtk#建立时间>   "213"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')
fw.write('<http://ke.course/rtk#魏>    <http://ke.course/rtk#灭亡时间>   "266"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')

fw.write('<http://ke.course/rtk#蜀>    <http://ke.course/rtk#势力名称>   "蜀"  .\n')
fw.write('<http://ke.course/rtk#蜀>    <http://www.w3.org/2000/01/rdf-schema#lable>   "蜀"  .\n')
fw.write('<http://ke.course/rtk#蜀>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')
fw.write('<http://ke.course/rtk#蜀>    <http://ke.course/rtk#建立时间>   "221"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')
fw.write('<http://ke.course/rtk#蜀>    <http://ke.course/rtk#灭亡时间>   "263"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')

fw.write('<http://ke.course/rtk#吴>    <http://ke.course/rtk#势力名称>   "吴"  .\n')
fw.write('<http://ke.course/rtk#吴>    <http://www.w3.org/2000/01/rdf-schema#lable>   "吴"  .\n')
fw.write('<http://ke.course/rtk#吴>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')
fw.write('<http://ke.course/rtk#吴>    <http://ke.course/rtk#建立时间>   "229"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')
fw.write('<http://ke.course/rtk#吴>    <http://ke.course/rtk#灭亡时间>   "280"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')

fw.write('<http://ke.course/rtk#西晋>    <http://ke.course/rtk#势力名称>   "西晋"  .\n')
fw.write('<http://ke.course/rtk#西晋>    <http://www.w3.org/2000/01/rdf-schema#lable>   "西晋"  .\n')
fw.write('<http://ke.course/rtk#西晋>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')
fw.write('<http://ke.course/rtk#西晋>    <http://ke.course/rtk#建立时间>   "266"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')
fw.write('<http://ke.course/rtk#西晋>    <http://ke.course/rtk#灭亡时间>   "316"^^<http://www.w3.org/2001/XMLSchema#date>  .\n')

fw.write('<http://ke.course/rtk#袁绍[势力]>    <http://ke.course/rtk#势力名称>   "袁绍[势力]"  .\n')
fw.write('<http://ke.course/rtk#袁绍[势力]>    <http://www.w3.org/2000/01/rdf-schema#lable>   "袁绍[势力]"  .\n')
fw.write('<http://ke.course/rtk#袁绍[势力]>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')

fw.write('<http://ke.course/rtk#袁术[势力]>    <http://ke.course/rtk#势力名称>   "袁术[势力]"  .\n')
fw.write('<http://ke.course/rtk#袁术[势力]>    <http://www.w3.org/2000/01/rdf-schema#lable>   "袁术[势力]"  .\n')
fw.write('<http://ke.course/rtk#袁术[势力]>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')

fw.write('<http://ke.course/rtk#刘表[势力]>    <http://ke.course/rtk#势力名称>   "刘表[势力]"  .\n')
fw.write('<http://ke.course/rtk#刘表[势力]>    <http://www.w3.org/2000/01/rdf-schema#lable>   "刘表[势力]"  .\n')
fw.write('<http://ke.course/rtk#刘表[势力]>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')

fw.write('<http://ke.course/rtk#起义军>    <http://ke.course/rtk#势力名称>   "起义军"  .\n')
fw.write('<http://ke.course/rtk#起义军>    <http://www.w3.org/2000/01/rdf-schema#lable>   "起义军"  .\n')
fw.write('<http://ke.course/rtk#起义军>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')

fw.write('<http://ke.course/rtk#董卓[势力]>    <http://ke.course/rtk#势力名称>   "董卓[势力]"  .\n')
fw.write('<http://ke.course/rtk#董卓[势力]>    <http://www.w3.org/2000/01/rdf-schema#lable>   "董卓[势力]"  .\n')
fw.write('<http://ke.course/rtk#董卓[势力]>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')

fw.write('<http://ke.course/rtk#刘璋[势力]>    <http://ke.course/rtk#势力名称>   "刘璋[势力]"  .\n')
fw.write('<http://ke.course/rtk#刘璋[势力]>    <http://www.w3.org/2000/01/rdf-schema#lable>   "刘璋[势力]"  .\n')
fw.write('<http://ke.course/rtk#刘璋[势力]>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')

fw.write('<http://ke.course/rtk#少数民族>    <http://ke.course/rtk#势力名称>   "少数民族"  .\n')
fw.write('<http://ke.course/rtk#少数民族>    <http://www.w3.org/2000/01/rdf-schema#lable>   "少数民族"  .\n')
fw.write('<http://ke.course/rtk#少数民族>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')

fw.write('<http://ke.course/rtk#在野>    <http://ke.course/rtk#势力名称>   "在野"  .\n')
fw.write('<http://ke.course/rtk#在野>    <http://www.w3.org/2000/01/rdf-schema#lable>   "在野"  .\n')
fw.write('<http://ke.course/rtk#在野>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')

fw.write('<http://ke.course/rtk#其他>    <http://ke.course/rtk#势力名称>   "其他"  .\n')
fw.write('<http://ke.course/rtk#其他>    <http://www.w3.org/2000/01/rdf-schema#lable>   "其他"  .\n')
fw.write('<http://ke.course/rtk#其他>    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#势力>  .\n')

fw.close()


# 生成 官职 三元组
fw = open('../data/dataset/triple_office.nt','w')
offices = ['后军校尉','大将军','侍郎','中常侍','司徒','宦官','郡丞','刺史','太守','车骑将军','县令','长史','武威将军','侍中','太医令','太傅','部将','仆射','征西将军','谋士','都尉','太尉','司隶校尉','镇东将军','太常卿','主簿','议郎','辅国将军','副将','武卫将军','中郎将','龙骧将军','平北将军','黄门侍郎','扬威将军','骠骑将军']
for office in offices:
    iri = "<http://ke.course/rtk#" + office + '> '
    fw.write(iri + '<http://ke.course/rtk#官职名称>   ' + "\"" + office + "\"    .\n")
    fw.write(iri + '<http://www.w3.org/2000/01/rdf-schema#lable>   ' + "\"" + office + "\"    .\n")
    fw.write(iri + '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#官职>   .\n')
fw.close()


# 生成 章节 三元组
fr = open('../data/dataset/chapter.txt','r')
fw = open('../data/dataset/triple_chapter.nt','w')
cnt = 1
for line in fr.readlines():
    s = line.split(' ')
    iri = "<http://ke.course/rtk#" + s[1] + "_" +s[2].replace('\n','').replace('\r','') + '> '
    fw.write(iri + '<http://ke.course/rtk#章节编号>   ' + "\"" + str(cnt) + "\"^^<http://www.w3.org/2001/XMLSchema#>    .\n")
    fw.write(iri + '<http://ke.course/rtk#章节标题>   ' + "\"" + s[1] + "_" +s[2].replace('\n','').replace('\r','') + "\"    .\n")
    fw.write(iri + '<http://www.w3.org/2000/01/rdf-schema#lable>   ' + "\"" + s[1] + "_" +s[2].replace('\n','').replace('\r','') + "\"    .\n")
    fw.write(iri + '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>   <http://ke.course/rtk#章节>   .\n')
    cnt += 1
fw.close()
fr.close()

# TODO：补全三元组
# 对象属性：击败、致死
# 对象属性：主公、主要将领
# 对象属性：参战势力、胜利势力、失败势力、参战人物、死亡人物