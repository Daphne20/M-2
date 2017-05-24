#!/usr/bin/env python
# coding:utf-8
import json
import numpy as np


def calculate_rpkm(inputfile,outputfile):
    sum_read_list=[float(line.strip().split("\t")[2]) for line in inputfile]
    sum_read=np.sum(sum_read_list)
    for line in inputfile:
        _mapped_read= float(line.strip().split("\t")[2])
        _bgc_len=float(line.strip().split("\t")[1])
        _rpkm=_mapped_read/(_bgc_len/1000 * sum_read/1000000)
        outputfile.write("%s\t%s\n" % (line.strip("\n"),_rpkm))


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


def split_id(dict,sort_dict):
    read_id=[id.split("|")[0] for id in dict]
    insert_key(sort_dict,read_id,inserts="list")
    for index in range(len(dict)):
        _read_id=list(dict)[index]
        _read_map=dict[_read_id]
        _id=_read_id.split("|")[0]
        sort_dict[_id]=_read_map

    return sort_dict


def save_json(mydict,filename):
    with open(filename, 'w') as f:
        json.dump(mydict, f)


def sort_shotgun(files,outputdir):
    file_reads=open(files,"r").readlines()
    file_rpkm_name=outputdir+"/rpkm.txt"
    file_rpkm=open(file_rpkm_name,"w")
    calculate_rpkm(file_reads,file_rpkm)
    file_rpkm.close()

    ## sort the mapped file(cut off 0.9)
    file_reads=open(file_rpkm_name,"r").readlines()[:-1]
    mapped_read={}
    read_rpkm=[float(line.strip().split("\t")[4]) for line in file_reads]
    cutoff=np.percentile(read_rpkm,90)
    for line in file_reads:
        _read_id=line.strip().split("\t")[0]
        _read_rpkm=float(line.strip().split("\t")[4])
        if _read_rpkm > cutoff :
            mapped_read[_read_id]=_read_rpkm

    mapped_read_sort={}
    mapped_read_sort=split_id(mapped_read,mapped_read_sort)
    filename=outputdir+"/test_mapped.json"
    # save_json(mapped_read_sort, filename)
    return  mapped_read_sort


def open_json(dict,filename):
    with open(filename, 'r') as f:
        dict = json.load(f)
    return dict


def modify_genus(file_line):
    taxonomy=file_line.strip().split("\t")[0]
    taxonomy=taxonomy.split(";")[-1]
    taxonomy=taxonomy.split("__")
    if taxonomy[0] == "g":
        _taxonomy=taxonomy[1]
    else:
        _taxonomy=taxonomy[0]

    return _taxonomy


def search_dict(value,dict):
    key_id = [i for i in dict if dict[i]["organism"] == value]
    return key_id


def sort_rna(files,outputdir,reference):
    reference_filename = reference
    taxa_file = open(files,"r").readlines()
    reference_json = reference_filename
    # reference_json = open_json(reference_json,reference_filename)
    taxa_sort_filename = outputdir+"/taxa.txt"
    taxa_sort = open(taxa_sort_filename,"w")
    taxa_json={}
    for line in taxa_file[2:]:
        _value=line.strip().split("\t")[1]
        _taxonomy=modify_genus(line)
        _id=search_dict(_taxonomy,reference_json)
        if _id==[]:
            pass
        else:
            for index in _id:
                taxa_sort.write("%s\t%s\n" %
                                (index,_value))
                taxa_json[index]=float(_value)

    taxa_sort.close()
    return taxa_json


