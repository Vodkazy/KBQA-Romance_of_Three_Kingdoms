# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
  @ Time     : 2019/7/9 下午2:00
  @ Author   : Vodka
  @ File     : extractTriple .py
  @ Software : PyCharm
"""
import json
import sys;
reload(sys);
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

        # 对象属性:效忠势力、古代籍贯
        if property_name == u'效忠势力' and item[property_name] != 'None':
            fw.write(iri + '<http://ke.course/rtk#效忠势力>   <http://ke.course/rtk#' + item[property_name] + ">   .\n")
        if property_name == u'古代籍贯' and item[property_name] != 'None':
            fw.write(iri + '<http://ke.course/rtk#古代籍贯>   <http://ke.course/rtk#' + item[property_name] + ">   .\n")
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

        # 对象属性:事件地点、对应章节、涉及人物
        if property_name == u'地点' and item[property_name] != 'None':
            fw.write(iri + '<http://ke.course/rtk#事件地点>   <http://ke.course/rtk#' + item[property_name] + ">   .\n")
        if property_name == u'章节' and item[property_name] != 'None':
            fw.write(iri + '<http://ke.course/rtk#对应章节>   <http://ke.course/rtk#' + item[property_name] + ">   .\n")
        if property_name == u'涉及人物' and item[property_name] != 'None':
            for name in item[property_name]:
                fw.write(iri + '<http://ke.course/rtk#涉及人物>   <http://ke.course/rtk#' + name + ">   .\n")
fw.close()
