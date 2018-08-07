import os
import csv
import json

from bson import ObjectId

# list = os.listdir("./rs-data")
# print(list)
# for file in list:
#     if file.startswith("concept_") and file.endswith(".csv"):
#         concept_connect = file.split("_")
#         print(concept_connect)
#         concept = {"concept":concept_connect[1].lower(),"conceptName":concept_connect[2]}
#         print(concept)
#     # concept_strs = file.split("_")
#     # concept = {"concept": concept_strs[1].lower(), "conceptName": concept_strs[2]}



# list = os.listdir("./rs-data")
# for file in list:
#    if file.startswith("attribute"):
#         with open("./rs-data/" + file, "r", encoding="UTF-8") as f:
#               i = 0
#               reader = csv.reader(f)
#               # for s in f.readlines():
#               #      print(s)
#               for row in reader:
#                     i = i + 1
#                     print(row[0])
#                     if i == 1:
#                        continue
#                     attribute = {
#                         "attributeName": row[0],
#                         "attributeEnglishAlias": str(row[1]).lower(),
#                         "attributeType": row[6],
#                         "attributeStatus": "ACTIVE",
#                         "isSupportMultiValue": row[3]
#                     }
#                     # result = self.db.Attribute.insert(attribute)
#                     # self.attributeMap[row[5]] = result

# s=ObjectId("5b67f54954afe07a6d1bf75c")
# print(s)
#
# rule_str = "双色球无群无群二“是是是”说说的发生实打实地方"
# rule_str = str.replace(rule_str, "“", "\"")
# rule_str = str.replace(rule_str, "”", "\"")
# print(rule_str)
#
s=["22",22121,'212']
for i in s:
    print(i)

a=str(s)
print(a)
print(type(a))
print(a[2])