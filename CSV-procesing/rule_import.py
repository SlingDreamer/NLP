import csv
import json
import os
from argparse import ArgumentParser as ArgParser

import pymongo
from bson import ObjectId

mongoHost = "127.0.0.1"
mongoPort = 27017


class MongoImport:
    def __init__(self, host, port):

        client = pymongo.MongoClient(host=host, port=port)

        self.db = client['resource-service']
        self.conceptMap = {}
        self.attributeMap = {}
        self.relationMap = {}

    def __init__(self, url):
        client = pymongo.MongoClient(url)
        self.db = client['resource-service']
        self.conceptMap = {}
        self.attributeMap = {}
        self.relationMap = {}

    def import_concept(self):
        self.db.Concept.drop()
        list = os.listdir("./rs-data")
        for file in list:
            if file.startswith("concept_") and file.endswith(".csv"):
                concept_strs = file.split("_")
                concept = {"concept": concept_strs[1].lower(), "conceptName": concept_strs[2]}
                result = self.db.Concept.insert(concept)
                self.conceptMap[concept_strs[3].replace(".csv", "")] = result

    def import_attribute(self):
        self.db.Attribute.drop()
        list = os.listdir("./rs-data")
        for file in list:
            if file.startswith("attribute"):
                with open("./rs-data/" + file, "r", encoding="UTF-8") as f:
                    i = 0
                    reader = csv.reader(f)
                    for row in reader:
                        i = i + 1
                        if i == 1:
                            continue
                        attribute = {
                            "attributeName": row[0],
                            "attributeEnglishAlias": str(row[1]).lower(),
                            "attributeType": row[6],
                            "attributeStatus": "ACTIVE",
                            "isSupportMultiValue": row[3]
                        }
                        result = self.db.Attribute.insert(attribute)
                        self.attributeMap[row[5]] = result

    def import_relation(self):
        self.db.ConceptRelation.drop()
        list = os.listdir("./rs-data")
        for file in list:
            if file.startswith("concept_") and file.endswith(".csv"):
                with open("./rs-data/" + file, "r", encoding="UTF-8") as f:
                    reader = csv.reader(f)
                    i = 0
                    for row in reader:
                        i = i + 1
                        if i == 1:
                            continue
                        try:
                            if (row[6] == "CONCEPT"):
                                relatedObjectId = str(self.conceptMap[row[8]])
                            else:
                                relatedObjectId = str(self.attributeMap[row[8]])

                            rules = []
                            # has topic rules
                            if len(row) > 9:
                                rule_strs = row[9].split('\n')
                                j = 1
                                for rule_str in rule_strs:
                                    rule = {
                                        "ruleId": ObjectId(),
                                        "ruleName": row[1] + "_topic_" + str(j),
                                        "ruleExpression": rule_str,
                                        "ruleType": "TOPIC"
                                    }
                                    j = j + 1
                                    rules.append(rule)
                            # has core answer rules
                            if len(row) > 10:
                                rule_str = row[10]
                                rule_str = str.replace(rule_str, "“", "\"")
                                rule_str = str.replace(rule_str, "”", "\"")
                                try:
                                    rule_jsons = json.loads(rule_str)
                                except Exception as ex:
                                    rule_jsons = []

                                j = 1
                                for rule_json in rule_jsons:
                                    rule = {
                                        "ruleId": ObjectId(),
                                        "ruleName": row[1] + "_reply_core_" + str(j),
                                        "ruleExpression": rule_json["value"],
                                        "ruleType": "REPLY_CORE",
                                        "weight": rule_json["weight"]
                                    }
                                    j = j + 1
                                    rules.append(rule)

                            # has multi answer rules
                            if len(row) > 11:
                                rule_str = row[11]
                                rule_str = str.replace(rule_str, "“", "\"")
                                rule_str = str.replace(rule_str, "”", "\"")
                                try:
                                    rule_jsons = json.loads(rule_str)
                                except Exception as ex:
                                    rule_jsons = []
                                j = 1
                                for rule_json in rule_jsons:
                                    rule = {
                                        "ruleId": ObjectId(),
                                        "ruleName": row[1] + "_reply_multi_" + str(j),
                                        "ruleExpression": rule_json["value"],
                                        "ruleType": "REPLY_MULTI",
                                        "weight": rule_json["weight"]
                                    }
                                    j = j + 1
                                    rules.append(rule)

                            relation = {
                                "relationName": row[1],
                                "primaryObjectType": row[2],
                                "primaryObjectName": row[3],
                                "primaryObjectId": ObjectId(str(self.conceptMap[row[4]])),
                                "relatedObjectName": row[5],
                                "relatedObjectType": row[6],
                                "relatedObjectId": ObjectId(relatedObjectId),
                                "rules": rules
                            }
                            result = self.db.ConceptRelation.insert(relation)
                        except Exception as e:
                            print(e)
                            print(row)


if __name__ == '__main__':
    argParser = ArgParser()
    argParser.add_argument("-m", "--host", type=str, help="Mongodb host")
    argParser.add_argument("-p", "--port", type=int, help="Mongodb port")
    argParser.add_argument("-u", "--user", type=str, help="Mongodb username")
    argParser.add_argument("-s", "--password", type=str, help="Mongodb password")
    argParser.add_argument("-l", "--url", type=str, help="Mongodb url")
    args = argParser.parse_args()
    if args.url:
        mongoImport = MongoImport(url=args.url)
    elif args.host and args.port:
        mongoImport = MongoImport(host=args.host, port=args.port)

    mongoImport.import_concept()
    mongoImport.import_attribute()
    mongoImport.import_relation()
