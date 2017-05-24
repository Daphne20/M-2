#!/usr/bin/env python
#coding:utf-8
def get_immmune(max_drug, immunedir, outputdir):
    immune_file_path=outputdir
    immune_filename="%s/immune_table.txt" % (immune_file_path)
    immune_table=open(immune_filename,"w")
    title_list=["drug", "transition", "cell", "tissue", "p_value", "fdr"]
    immune_table.writelines("%s\t" % item for item in title_list)
    immune_table.write("\n")
    for index in max_drug:
        if index in immunedir:
            _transition=immunedir[index]["transition"]
            _cell=immunedir[index]["cell"]
            _tissue=immunedir[index]["tissue"]
            _value=immunedir[index]["p_value"]
            _fdr=immunedir[index]["fdr"]
            immune_table.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (index, _transition, _cell, _tissue,
                                                         _value, _fdr))

    immune_table.close()
