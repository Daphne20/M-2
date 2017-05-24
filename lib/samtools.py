#!/usr/bin/env python
# coding:utf-8
import subprocess


def sh(args):
    return subprocess.call(args,shell=True)


def samtools_run(samtools_path, files, outputdir, outprefix):
    sh("{0} view -hbS {1} -o {2}/{3}.bam"\
           .format(samtools_path, files, outputdir, outprefix))

    sh("{0} sort {1}/{2}.bam {2}.sorted"\
           .format(samtools_path, outputdir, outprefix))

    sh("{0} view -b -F 0x04 -q 1 -o {1}/{2}_filter.bam {1}/{2}.sorted.bam"\
           .format(samtools_path, outputdir, outprefix))

    sh("{0} index {1}/{2}_filter.bam "\
           .format(samtools_path, outputdir, outprefix))

    sh("{0} idxstats {1}/{2}_filter.bam > {1}/result_mapped.txt"\
           .format(samtools_path, outputdir, outprefix))

