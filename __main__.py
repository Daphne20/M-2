#!/usr/bin/env python
# coding:utf-8
"""
Licensed Materials - Property of Tongji University
(C) Copyright Tongji University LifeBio Dept. 2017, 2017 All Rights Reserved
--------------------------------------------------------------------------------------
File Name   :  __main__.py
Description : m2 pipeline
Author: Han Zhao


Change activity:
v1.0.1
Add antibiotic function

"""
import subprocess
import json
import sys
import argparse
from lib.parser.parserIO import ConfigParser
from lib.bowtie2 import bowtie2_run
from lib.samtools import samtools_run
from lib.qiime import qiime_run
from lib.filesort import sort_shotgun,sort_rna
from lib.distribution import get_table
from lib.drug_relation import get_smidrug
from lib.side_effect import get_sideeffect
from lib.immune import get_immmune
from lib.antibiotic import get_antibiotic

def sh(args):
    return subprocess.call(args,shell=True)


## for test
def save_json(mydict,filename):
    with open(filename, 'w') as f:
        json.dump(mydict, f)


def shotgun_mapping_main(Bowtie2_path, Bowtie2_index, files, outputdir, Samtools_path):
    outprefix = files.split("/")[-1]
    outprefix = outprefix.split(".")[0]
    bowtie2_run(Bowtie2_path, Bowtie2_index, files, outputdir, outprefix)
    filename=outputdir+"/"+outprefix+".sam"
    samtools_run(Samtools_path, filename, outputdir, outprefix)
    outputfile="{0}/result_mapped.txt" .format(outputdir)
    return outputfile


def rna_mapping_main(files, mapfile, outputdir):
    outprefix = files.split("/")[-1]
    outprefix = outprefix.split(".")[0]
    qiime_run(files, mapfile, outputdir, outprefix)
    outputfile="{0}/cdhit_picked_otus/taxa_summary/otu_table_L6.txt" .format(outputdir)
    return outputfile


def shotgun_sort_main(Bowtie2_path, Bowtie2_index, Samtools_path, outputdir, files):
    result=shotgun_mapping_main(Bowtie2_path, Bowtie2_index, files, outputdir, Samtools_path)
    # result="{0}result_mapped.txt" .format(outputdir)
    mapdict=sort_shotgun(result, outputdir)
    return mapdict


def rna_sort_main(files, mapfile, outputdir, reference):
    result=rna_mapping_main(files, mapfile, outputdir)
    ##for test
    # result="{0}cdhit_picked_otus/taxa_summary/otu_table_L6.txt" .format(outputdir)
    ##
    mapdict=sort_rna(result, outputdir, reference)
    return mapdict


def open_json(filename):
    with open(filename, 'r') as f:
        dict = json.load(f)
    return dict


def main(testfile, outputdir, args, mapfile, config_file="/home/tuser/myproject/m2/lib/db/config.txt"):  
    Softpath=config_file[:-18]
    Config=ConfigParser()
    Config=Config.load_parser(config_file)
    map_config=Config["mapping"]
    database_config=Config["database"]
# Bowtie2_path, Bowtie2_index, Samtools_path, outputdir, files
    if args.shotgun:
        map_dict=shotgun_sort_main(files=testfile,outputdir=outputdir, **map_config)
        reference_json=database_config["shotgun_reference"]
    elif args.rna:
    # else:
        map_dict=rna_sort_main(testfile,mapfile, outputdir, database_config["rna_reference"])
        reference_json=database_config["rna_reference"]
    else:
        print ("error in data type!")
        sys.exit(1)

    compound_dict=get_table(Softpath, map_dict, reference_json, outputdir)
    ### for test
    # test_name=outputdir+"test_comp_dict.json"
    # compound_dict=open_json(test_name)
    ###
    max_drugcomp=get_smidrug(compound_dict, database_config["Structuredir"], database_config["Drugdir"], outputdir)
    get_immmune(max_drugcomp, database_config["Immunedir"], outputdir)
    get_sideeffect(compound_dict, database_config["Sideeffectdir"], database_config["Structuredir"], outputdir)
    get_antibiotic(max_drugcomp,database_config["Antibioticdir"], outputdir)



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--shotgun", action="store_true", help="input file is shotgun type")
    parser.add_argument("-r", "--rna", action="store_true", help="input file is 16s rRNA type")
    parser.add_argument("-f", "--file", help="input file")
    parser.add_argument("-m", "--mapfile", help="16s rRNA file type must have mapfile for mapping")
    parser.add_argument("-o", "--output", help="output path")
    args = parser.parse_args()
    file=args.file
    mapfile=args.mapfile
    outputdir=args.output

    sh("cd {0}" .format(outputdir))
    main(file, outputdir, args, mapfile)
    output_mapping=outputdir+"/mapping"
    output_database=outputdir+"/database"
    ouput_picture=outputdir+"/picture"
    sh("mkdir {0} {1} {2}" .format(output_mapping, output_database, ouput_picture))
    sh("mv *.txt {0}" .format(output_database))
    sh("mv *.pdf {0}" .format(ouput_picture))
    sh("mv *.bam *.sam *.bai {0}" .format(output_mapping))



