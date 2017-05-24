#!/usr/bin/env python
#coding:utf-8
def dict_max_value(dict):
    key=max(dict.items(), key=lambda x: x[1])
    return key


def if_list(lists):
    if isinstance(lists,list):
        value=",".join(lists)
    else:
        value=lists

    return value


def if_has_key(dict,key):
    if key in dict:
        value=if_list(dict[key])
    else:
        value="NA"

    return value


def get_sideeffect(compdict, drug_side_effect, whole_similarity, outputdir):
    compounds_list_normal=list(compdict)
    compounds_list_lower=[key.lower() for key in compdict]
    side_effect_comp=list(set(list(set(compounds_list_normal).intersection(set(list(drug_side_effect))))+list(set(compounds_list_lower).intersection(set(list(drug_side_effect))))))
    side_effect_file_path=outputdir
    side_effect_filename="%s/side_effect_table.txt" % (side_effect_file_path)
    side_effect_table=open(side_effect_filename,"w")
    title_list=["BGC","side effect_bgc","drug compounds","similarity","side effect_drug"]
    side_effect_table.writelines("%s\t" % item for item in title_list)
    side_effect_table.write("\n")
    for index in side_effect_comp:
        _bgc=index+" biosynthetic gene cluster"
        if index in whole_similarity:
            _dict_smi= whole_similarity[index]
            _max_drug_comp=dict_max_value(_dict_smi)[0]
            _max_smi=dict_max_value(_dict_smi)[1]
            _side_effect_bgc=drug_side_effect[index]
            _side_effect_drug=if_has_key(drug_side_effect,_max_drug_comp)
            side_effect_table.write("%s\t%s\t%s\t%s\t%s\n" % (_bgc,_side_effect_bgc,_max_drug_comp,
                                                             _max_smi,_side_effect_drug))
        else:
            _side_effect_bgc="NA"
            _max_drug_comp=index
            _max_smi="NA"
            _side_effect_drug=drug_side_effect[index]
            side_effect_table.write("%s\t%s\t%s\t%s\t%s\n" % (_bgc,_side_effect_bgc,_max_drug_comp,
                                                 _max_smi,_side_effect_drug))

    side_effect_table.close()

