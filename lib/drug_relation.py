#!/usr/bin/env python
#coding:utf-8
def dict_max_value(dict):
    key=max(dict.items(), key=lambda x: x[1])
    return key

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


def if_list(lists):
    if isinstance(lists,list):
        value=",".join(lists)
    else:
        value=lists

    return value


def classify_dict(dict):
    new_dict={}
    key_list=["increased","decreased","may increase","may decrease"]
    insert_key(new_dict,key_list,inserts="list")
    if dict == {} :
        pass
    else:
        for item in dict:
            string=dict[item]
            if "increased" in string:
                new_dict["increased"].append(item)
            elif "decreased" in string:
                new_dict["decreased"].append(item)
            elif "may increase" in string:
                new_dict["may increase"].append(item)
            elif "may decrease" in string:
                new_dict["may decrease"].append(item)
            else:
                pass

    return new_dict


def if_has_list(lists):
    if lists == []:
        item="NA"
    else:
        item=if_list(lists)

    return item


def get_smidrug(compdict, whole_similarity, drug_infor, outputdir):
    compounds_list_normal=list(compdict)
    compounds_list_lower=[key.lower() for key in compdict]

    ## sort compounds if in the similarity table
    similarity_compounds= list(whole_similarity)
    compounds_list_sorted=list(set(list(set(compounds_list_normal).intersection(set(similarity_compounds)))+list(set(compounds_list_lower).intersection(set(similarity_compounds)))))

    # similarity_compounds_expr=whole_similarity["expression"].keys()
    # compounds_list_sorted_expr=list(set(list(set(compounds_list_normal).intersection(set(similarity_compounds_expr)))+list(set(compounds_list_lower).intersection(set(similarity_compounds_expr)))))


    ##get drug smi table(数值中含有[])

    drug_file_path=outputdir
    smi_drug_filename="%s/similar_drug_table.txt" % (drug_file_path)
    smi_drug_table=open(smi_drug_filename,"w")
    drug_list= whole_similarity['TP-1161']
    smi_drug_table.writelines("%s\t" % item for item in drug_list)
    smi_drug_table.write("\n")

    for index in compounds_list_sorted:
        _bgc=index+" biosynthetic gene cluster"
        smi_drug_table.write("%s\t" % _bgc)
        smi_drug_table.writelines("%s\t" %  whole_similarity[index][item] for item in drug_list)
        smi_drug_table.write("\n")

    smi_drug_table.close()


    ## get drug information table (取最大相似值的药物)

    drug_infor_file_path=outputdir
    drug_infor_filename="%s/drug_infor_table.txt" % (drug_infor_file_path)
    drug_infor_table=open(drug_infor_filename,"w")
    title_list=["bgc","drug compounds","smilarity","drug","indication","increased","decreased",'may increase','may decrease']
    drug_infor_table.writelines("%s\t" % item for item in title_list)
    drug_infor_table.write("\n")
    max_drug=[]

    for index in compounds_list_sorted:
        _bgc=index+" biosynthetic gene cluster"
        _dict_smi= whole_similarity[index]
        _max_drug_comp=dict_max_value(_dict_smi)[0]
        max_drug.append(_max_drug_comp)
        _max_smi=dict_max_value(_dict_smi)[1]
        _drug_product=if_has_list(drug_infor[_max_drug_comp]["products"])
        _drug_indication=if_has_list(drug_infor[_max_drug_comp]["indication"])
        _interaction_dict=classify_dict(drug_infor[_max_drug_comp]["drug-interactions"])
        _increased=if_has_list(_interaction_dict["increased"])
        _decreased=if_has_list(_interaction_dict["decreased"])
        _may_increase=if_has_list(_interaction_dict["may increase"])
        _may_decrease=if_has_list(_interaction_dict["may decrease"])
        drug_infor_table.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                               % (_bgc,_max_drug_comp,_max_smi,_drug_product,_drug_indication,
                                  _increased,_decreased,_may_increase,_may_decrease))


    drug_infor_table.close()
    return max_drug

