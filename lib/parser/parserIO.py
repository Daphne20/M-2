#!/usr/bin/env python
#coding:utf-8
import sys
import json


class ConfigParser(object):
    def __init__(self):
        self.__configs = {}
        self.__preset = {"mapping":{"Bowtie2_path":None,"Bowtie2_index":None,
                                  "Samtools_path":None},
                         "database":{"Structuredir":None,"Expressiondir":None,"Drugdir":None,
                                  "Antibioticdir":None,"Sideeffectdir":None,"Immunedir":None,
                                  "shotgun_reference":None,"rna_reference":None}}

    def __open_json(self,filename):
        with open(filename, 'r') as f:
            dict = json.load(f)
        return dict

    def __table_list(self,filename):
        file=open(filename,"r").readlines()
        comp_list=[line.strip() for line in file]
        return comp_list

    def load_parser(self,configfile="config.txt"):
        _file=[i.strip() for i in open(configfile)]
        self.__configs["mapping"]={}
        self.__configs["database"]={}
        runtype=["mapping","database"]
        for _line in _file:
            if ":" in _line[:50]:
                _key = _line.split(":")[0]
                _value = _line.split(":")[1]
                for _type in runtype:
                    if _key in self.__preset[_type]:
                            self.__configs[_type][_key] = _value
                Configs = self.__configs
        for _type in runtype:
            for _key,_val in Configs[_type].items():
                if _val is None:
                    Configs[_type].pop(_key)

        database_path = Configs["database"]
        for key in database_path:
            if key != "Antibioticdir":
                _filepath=database_path[key]
                database_path[key]=self.__open_json(_filepath)
            else:
                _filepath=database_path[key]
                database_path[key]=self.__table_list(_filepath)

        Configs["database"] = database_path
        return Configs