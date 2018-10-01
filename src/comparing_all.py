#!/usr/bin/env python3
# encoding: utf-8

'''
    bbo

Usage:
    bbo.py <n> <more_arg> <norm_file> <trace> <threshold> <vec_out> <swf_file>... [-h]

Options:
    <n>            budget
    <swf_file>     an input file
    <more_arg>     extra cli ocs arguments
    <trace>        name of the current trace
    <threshold>    threshold value
    <vec_out>      output vector
    <norm_file>    normalizer file
    -h --help      show this help message and exit.
'''


from docopt import docopt
import pybrain
from subprocess import check_output
import subprocess
import os
import time
import pandas as pd
import csv
import numpy as np
import math
import pybrain.optimization as opt
import sys



"""" list  of used functions"""
def v2s(v):
	return(','.join([str(e) for e in v]))

def makev(x,norm,a,b):
	return("%s:%s:%s" %(v2s(x[a:b]),v2s(norm[0][a:b]),v2s(norm[1][a:b])))



def simulate(f,x):

    if(len(x)<6):
        x=[x[0],x[1],x[2],0.0,0.0,0.0]
    s=["ocs","mixed",f,"--alpha=%s" %makev(x,norm,0,len(x)),"--threshold="+threshold]+more_arg
    s=" ".join(s)
    p=subprocess.Popen(s,stdout=subprocess.PIPE,shell=True)
    if p.poll() is None:
        p.wait()
    obj=float(p.stdout.read())
    return obj


def simulate_max(f,x):
    if(len(x)<6):
        x=[x[0],x[1],x[2],0.0,0.0,0.0]
    s=["ocs","mixed",f,"--alpha=%s" %makev(x,norm,0,len(x)),"--threshold="+threshold,'--backfill=spf','--stat=maxbsld']
    s=" ".join(s)
    p=subprocess.Popen(s,stdout=subprocess.PIPE,shell=True)
    if p.poll() is None:
        p.wait()
    obj=float(p.stdout.read())
    return obj


def objf(x):
    if(len(x)<6):
        x=[x[0],x[1],x[2],0.0,0.0,0.0]
    s=["ocs","mixed",file,"--alpha=%s" %makev(x,norm,0,len(x)),"--threshold="+threshold]+more_arg
    s=" ".join(s)
    p=subprocess.Popen(s,stdout=subprocess.PIPE,shell=True)
    if p.poll() is None:
        p.wait()
        obj=float(p.stdout.read())
    scaling_term=a=10**(len(str(int(obj)))-1)# scaling term to give penalty the same size of the objective
    penalty=np.sum(np.abs(x)) + 1/np.sum(np.abs(x))# the penalty term to stop the values from converging to 0
    return (obj + penalty*scaling_term)



def getperf(f,x):
    if(len(x)<6):
        x=[x[0],x[1],x[2],0.0,0.0,0.0]
    s=["ocs","mixed",f,"--alpha=%s" %makev(x,norm,0,len(x)),"--threshold="+threshold]+more_arg
    return(" ".join(s))
def objf_batch(x):
    if(len(x)<6):
        x=[x[0],x[1],x[2],0.0,0.0,0.0]
    processes = [subprocess.Popen(getperf(f,x),stdout=subprocess.PIPE,shell=True) for f in args["<swf_file>"]]
    for p in processes:
        if p.poll() is None:
            p.wait()
    objs = [float(x.stdout.read()) for x in processes]
    sum_objs=sum(objs)
    scaling_term=a=10**(len(str(int(sum_objs)))-1)# scaling term to give penalty the same size of the objective
    penalty=np.sum(np.abs(x)) + 1/np.sum(np.abs(x))# the penalty term to stop the values from converging to 0
    return(sum_objs + penalty*scaling_term)

def objf_batch_training(x):
    processes = [subprocess.Popen(getperf(f,x),stdout=subprocess.PIPE,shell=True) for f in f_training]
    for p in processes:
        if p.poll() is None:
            p.wait()
    objs = [float(x.stdout.read()) for x in processes]
    sum_objs=sum(objs)
    scaling_term=a=10**(len(str(int(sum_objs)))-1)# scaling term to give penalty the same size of the objective
    penalty=np.sum(np.abs(x)) + 1/np.sum(np.abs(x))# the penalty term to stop the values from converging to 0
    return(sum_objs + penalty*scaling_term)


def v_one(i,m):
    x = [0 for e in range(6)]
    x[i]=m
    return(x)

def get_pure_policy_list():
	v=[]
	for i in range(6):
		policy_vector_short=v_one(i,1)
		policy_vector_long=v_one(i,-1)
		v.append(policy_vector_long)
		v.append(policy_vector_short)
	return v
def learn_xnes(x0=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])):
	try:
		
		l=opt.XNES(objf,x0)
		l.minimize = True
		l.mustMinimize = True
		l.verbose = False
		l.maxLearningSteps=int(args["<n>"])
		l.batchSize=25
		r=l.learn()
		return r
	except:
		print("errrrrrrrrrrror single learning")


	
def learn_xnes_batch(x0=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])):

	l=opt.XNES(objf_batch,x0)
	l.minimize = True
	l.mustMinimize = True
	l.verbose = False
	l.maxLearningSteps=int(args["<n>"])
	l.batchSize=25
	r=l.learn()
	return r
def learn_xnes_batch_training(x0=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])):


	l=opt.XNES(objf_batch_training,x0)
	l.minimize = True
	l.mustMinimize = True
	l.verbose = True
	l.maxLearningSteps=int(args["<n>"])
	l.batchSize=25
	r=l.learn()
	return r

def divide_training_testing():
    f_training=[]
    f_testing=[]
    training_size=100
    for f in args["<swf_file>"]:
        if(training_size>0):
            f_training.append(f)
            training_size-=1
        else:
            f_testing.append(f)
    return f_training,f_testing


def save_progress(l=[],file_name="logs/place_holder.csv",mode='a'):
	with open(file_name, mode) as file_temp:
		writer = csv.writer(file_temp)
		writer.writerows(l)


def execute_single_weeks(pol=None,name="Unamed"):
    grand_list=[]
    for f in args["<swf_file>"]:
        id_string=f.split(".")
        li=[id_string[1] ,id_string[3],name,simulate(f,pol),simulate_max(f,pol)]
        grand_list.append(li)
    save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="a")


# Main
if __name__ == '__main__':
    args = docopt(__doc__, version='1.0.0rc2')
    with open(args["<norm_file>"]) as f:
        norm = [[float(e) for e in l.split(",")]  for l in f]
    with open(args["<more_arg>"]) as f:
        more_arg = [l.strip() for l in f]
    

    threshold= args["<threshold>"].strip()
    trace=args["<trace>"].strip()
    #sys.exit('stopping execution')


    policy_translation_dict={'-100000': 'lqf','0-10000': 'lpf','00-1000': 'lcfs','000-100': 'lexp','0000-10': 'lrf','00000-1': 'laf','000001': 'saf','000010': 'srf','000100': 'sexp','001000': 'fcfs','010000': 'spf','100000': 'sqf'}
    simulate_pure=True
    learning_dynamic_clairvoyant_6=True
    learning_offline_clairvoyant_6=True
    learning_offline_6=True
    succsesive_learning_6=True
    learning_dynamic_clairvoyant_3=True
    learning_offline_clairvoyant_3=True
    learning_offline_3=True
    succsesive_learning_3=True

    pure_policy_list=get_pure_policy_list()
    grand_list=[]
    grand_list.append(["id","trace","policy","avg","max"])
    save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="w")
    save_progress(l=[["id","trace","vector"]],file_name="logs/learned_vectors.csv",mode="w")

	#performance of pure policies
    if(simulate_pure):
        print("simulating the 12 pure policies")
        for pol in pure_policy_list:
            policy_name=policy_translation_dict[''.join(str(nb) for nb in pol)]
            execute_single_weeks(pol=pol,name=policy_name)

#learning using a vector of 6

    if(learning_dynamic_clairvoyant_6):
        print("learning dynamic clairvoyant of 6 featues")
        grand_list=[]
        learned_vector_list=[]
        learned_vector_list_next=[]
        for file in args["<swf_file>"]:
            r=learn_xnes()

            id_string=file.split(".")
            l=[id_string[1] ,id_string[3], "xnes_dynamic_clairvoyant_6" , simulate(file,r[0]) , simulate_max(file,r[0])]
            grand_list.append(l)
            learned_vector_list_next.append([file,r[0]])
            save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="a")
            save_progress(l=[[id_string[1] ,id_string[3],";".join(str(nb) for nb in r[0])]],file_name="logs/learned_vectors.csv",mode="a")
            grand_list=[]

    if (learning_offline_clairvoyant_6):
        print("learning offline clairvoyant for 6 features")
        r=learn_xnes_batch()
        execute_single_weeks(pol=r[0],name="learning_offline_clairvoyant_6")
        save_progress(l=[["learning_offline_clairvoyant_6",trace,";".join(str(nb) for nb in r[0])]],file_name="logs/learned_vectors.csv",mode="a")

    if(learning_offline_6):
        print("learning offline for 6 features")
        size=len(args["<swf_file>"])
        f_training=args["<swf_file>"][:int(size/2)]
        f_testing=args["<swf_file>"][int(size/2):]
        r=learn_xnes_batch_training()
        execute_single_weeks(pol=r[0],name="learning_offline_6") 
        save_progress(l=[["learning_offline_6",trace,";".join(str(nb) for nb in r[0])]],file_name="logs/learned_vectors.csv",mode="a")
    
    if(succsesive_learning_6):
        print("testing each learned vector on the next week: 6 features")
        i=0
        files=args["<swf_file>"][1:len(args["<swf_file>"])+1]
        grand_list=[]
        for file in files:
            week_name=learned_vector_list_next[i][0]

            vector=learned_vector_list_next[i][1]

            id_string=file.split(".")    
            l=[id_string[1] ,id_string[3] , "past_week_6" , simulate(file,vector) ,simulate_max(file,vector)]
            grand_list.append(l)
            
            save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="a")
            grand_list=[]
            i+=1
    if(learning_dynamic_clairvoyant_3):
        print("learning dynamic clairvoyant of 6 featues")
        grand_list=[]
        learned_vector_list=[]
        learned_vector_list_next=[]
        for file in args["<swf_file>"]:
            r=learn_xnes(x0=np.array([0.0,0.0,0.0]))

            id_string=file.split(".")
            l=[id_string[1] ,id_string[3], "xnes_dynamic_clairvoyant_3" , simulate(file,r[0]) , simulate_max(file,r[0])]
            grand_list.append(l)
            learned_vector_list_next.append([file,r[0]])
            save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="a")
            save_progress(l=[[id_string[1] ,id_string[3],";".join(str(nb) for nb in r[0])]],file_name="logs/learned_vectors.csv",mode="a")
            grand_list=[]

    if (learning_offline_clairvoyant_3):
        print("learning offline clairvoyant for 6 features")
        r=learn_xnes_batch(x0=np.array([0.0,0.0,0.0]))
        execute_single_weeks(pol=r[0],name="learning_offline_clairvoyant_3")
        save_progress(l=[["learning_offline_clairvoyant_3",trace,";".join(str(nb) for nb in r[0])]],file_name="logs/learned_vectors.csv",mode="a")

    if(learning_offline_3):
        print("learning offline for 6 features")
        size=len(args["<swf_file>"])
        f_training=args["<swf_file>"][:int(size/2)]
        f_testing=args["<swf_file>"][int(size/2):]
        r=learn_xnes_batch_training(x0=np.array([0.0,0.0,0.0]))
        execute_single_weeks(pol=r[0],name="learning_offline_3") 
        save_progress(l=[["learning_offline_3",trace,";".join(str(nb) for nb in r[0])]],file_name="logs/learned_vectors.csv",mode="a")
    
    if(succsesive_learning_3):
        print("testing each learned vector on the next week: 6 features")
        i=0
        files=args["<swf_file>"][1:len(args["<swf_file>"])+1]
        grand_list=[]
        for file in files:
            week_name=learned_vector_list_next[i][0]

            vector=learned_vector_list_next[i][1]

            id_string=file.split(".")    
            l=[id_string[1] ,id_string[3] , "past_week_3" , simulate(file,vector) ,simulate_max(file,vector)]
            grand_list.append(l)
            
            save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="a")
            grand_list=[]
            i+=1

