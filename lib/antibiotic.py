#!/usr/bin/env python
#coding:utf-8
def get_antibiotic(max_drug,antibioticdir,outputdir):
    antibiotic_file_path=outputdir
    antibiotic_filename="%s/antibiotic_table.txt" % (antibiotic_file_path)
    antibiotic_table=open(antibiotic_filename,"w")
    title_list=["antibiotic"]
    antibiotic_table.writelines("%s\t" % item for item in title_list)
    antibiotic_table.write("\n")
    if max_drug in antibioticdir:
        antibiotic_table.writelines("%s\t" % max_drug)
        antibiotic_table.write("\n")

    antibiotic_table.close()