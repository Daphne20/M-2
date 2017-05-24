#!/usr/bin/env python
# coding:utf-8
import subprocess


def sh(args):
    return subprocess.call(args,shell=True)


def bowtie2_run(bowtie2_path, bowtie2_index, files, outputdir, outprefix):
    sh("{0} -p 4 --local -x {1} -U {2} -N 1 -S {3}/{4}.sam"\
           .format(bowtie2_path, bowtie2_index, files, outputdir,outprefix))


