# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
  @ Time     : 2019/7/9 下午2:00
  @ Author   : Vodka
  @ File     : extractTriple .py
  @ Software : PyCharm
"""
import json

path = open('../data/dataset/person.json')
fr = json.load(path,encoding='utf-8')
path.close()

fw = open('../data/dataset/triple.nt','w')
for item in fr:
    j = json.dumps(item,encoding='utf-8',ensure_ascii=False)
    print j
    fw.write("<http://>")

