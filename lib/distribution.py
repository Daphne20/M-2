#!/usr/bin/env python
#coding:utf-8

## rscript need to update
import subprocess


def sh(args):
    return subprocess.call(args,shell=True)


def dict_to_table(inputdict,outputfilename):
    outputfile=open(outputfilename,"w")
    for index in inputdict.keys():
        _col_name=index
        _col_read=inputdict[_col_name]
        outputfile.write("%s\t%s\n"
                         % (_col_name,_col_read))

    outputfile.close()


def insert_key(dict, keys, inserts="dict"):
    if inserts == "dict":
        for key in keys:
            dict[key] = {}
    elif inserts == "list":
        for key in keys:
            dict[key] = []
    elif inserts == "float":
        for key in keys:
            dict[key] = 0.0
    else:
        pass


def get_table(Softpath, mapped_read_sort, reference_json, outputdir):
    id_dict={}
    bacteria_dict={}
    bgc_dict={}
    compounds_dict={}
    bacteria_dict_key=list(set([reference_json[id_index]["organism"] for id_index in mapped_read_sort.keys()]))
    bgc_dict_key=list(set([reference_json[id_index]["description"] for id_index in mapped_read_sort.keys()]))
    compounds_dict_key=list(set([reference_json[id_index]["description"][:-26] for id_index in mapped_read_sort.keys()]))

    insert_key(bacteria_dict,bacteria_dict_key,inserts="float")
    insert_key(bgc_dict,bgc_dict_key,inserts="float")
    insert_key(compounds_dict,compounds_dict_key,inserts="float")


    for id_index in mapped_read_sort.keys():
        _organism=reference_json[id_index]["organism"]
        _read_count=mapped_read_sort[id_index]
        _bgc_description=reference_json[id_index]["description"]
        _compounds=reference_json[id_index]["description"][:-26]
        bacteria_dict[_organism]=bacteria_dict[_organism]+_read_count
        bgc_dict[_bgc_description]=bgc_dict[_bgc_description]+_read_count
        compounds_dict[_compounds]=compounds_dict[_compounds]+_read_count
        id_dict[id_index]=_read_count


    distribution_file_path=outputdir
    bacteria_table_filename="%s/bacteria_table.txt" % (distribution_file_path)
    bgc_table_filename="%s/bgc_table.txt" % (distribution_file_path)
    compounds_table_filename="%s/compounds_table.txt" % (distribution_file_path)
    id_table_filename="%s/id_table.txt" % (distribution_file_path)


    dict_to_table(bacteria_dict,bacteria_table_filename)
    dict_to_table(bgc_dict,bgc_table_filename)
    dict_to_table(compounds_dict,compounds_table_filename)
    dict_to_table(id_dict,id_table_filename)

    sh("Rscript {}/rscript/individual_distribution.R {} {} {} {} {}&>>distribution.log"\
       .format(Softpath, id_table_filename, bacteria_table_filename,  bgc_table_filename, compounds_table_filename, outputdir))

    return compounds_dict









