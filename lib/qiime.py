#!/usr/bin/env python
# coding:utf-8
import subprocess


def sh(args):
    return subprocess.call(args,shell=True)


def qiime_run(files, mapfile, outputdir, outputprefix):
    sh("source activate qiime1")
    sh("convert_fastaqual_fastq.py -c fastq_to_fastaqual -f {0} -o {1}/fastaqual" \
           .format(files, outputdir))
    sh("split_libraries.py -m {0} -f {1}/fastaqual/*.fna -q {1}/fastaqual/*.qual -s 15 -o {1}/{2}.lib -k -a 6 -r -b 10 -M 5 -e 0" \
           .format(mapfile,outputdir,outputprefix))
    sh("pick_de_novo_otus.py -i {0}/{1}.lib/seqs.fna -o {0}/cdhit_picked_otus" \
           .format(outputdir, outputprefix))
    sh("summarize_taxa_through_plots.py -i {0}/cdhit_picked_otus/otu_table.biom -o {0}/cdhit_picked_otus/taxa_summary -m {1}" \
           .format(outputdir, mapfile))




