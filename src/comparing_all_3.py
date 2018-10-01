#!/usr/bin/env python3
# encoding: utf-8

'''
    bbo

Usage:
    bbo.py <n> <more_arg> <norm_file> <vec_out> <swf_file>... [-h]

Options:
    <n>            budget
    <swf_file>     an input file
    <more_arg>     extra cli ocs arguments
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
import csv



"""" list  of used functions"""
def v2s(v):
	return(','.join([str(e) for e in v]))

def makev(x,norm,a,b):
	return("%s:%s:%s" %(v2s(x[a:b]),v2s(norm[0][a:b]),v2s(norm[1][a:b])))



def simulate(f,x):
    x=[x[0],x[1],x[2],0.0,0.0,0.0]
    s=["ocs","mixed",f,"--alpha=%s" %makev(x,norm,0,len(x)),"--threshold=604800"]+more_arg
    s=" ".join(s)
    p=subprocess.Popen(s,stdout=subprocess.PIPE,shell=True)
    if p.poll() is None:
        p.wait()
    obj=float(p.stdout.read())
    return obj


def simulate_max(f,x):
    x=[x[0],x[1],x[2],0.0,0.0,0.0]
    s=["ocs","mixed",f,"--alpha=%s" %makev(x,norm,0,len(x)),"--threshold=604800",'--backfill=spf','--stat=maxbsld']
    s=" ".join(s)
    p=subprocess.Popen(s,stdout=subprocess.PIPE,shell=True)
    if p.poll() is None:
        p.wait()
    obj=float(p.stdout.read())
    return obj


def objf(x):
    x=[x[0],x[1],x[2],0.0,0.0,0.0]
    s=["ocs","mixed",file,"--alpha=%s" %makev(x,norm,0,len(x)),"--threshold=604800"]+more_arg
    s=" ".join(s)
    p=subprocess.Popen(s,stdout=subprocess.PIPE,shell=True)
    if p.poll() is None:
        p.wait()
        obj=float(p.stdout.read())
    scaling_term=a=10**(len(str(int(obj)))-1)# scaling term to give penalty the same size of the objective
    penalty=np.sum(np.abs(x)) + 1/np.sum(np.abs(x))# the penalty term to stop the values from converging to 0
    return (obj + penalty*scaling_term)



def getperf(f,x):
    x=[x[0],x[1],x[2],0.0,0.0,0.0]
    s=["ocs","mixed",f,"--alpha=%s" %makev(x,norm,0,len(x)),"--threshold=604800"]+more_arg
    return(" ".join(s))
def objf_batch(x):
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
    x=[x[0],x[1],x[2],0.0,0.0,0.0]
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
def learn_xnes():
    x0=np.array([0.0,0.0,0.0])
    l=opt.XNES(objf,x0)
    l.minimize = True
    l.mustMinimize = True
    l.verbose = False
    l.maxLearningSteps=int(args["<n>"])
    l.batchSize=25
    r=l.learn()
    return r


	
def learn_xnes_batch():
    x0=np.array([0.0,0.0,0.0])
    l=opt.XNES(objf_batch,x0)
    l.minimize = True
    l.mustMinimize = True
    l.verbose = False
    l.maxLearningSteps=int(args["<n>"])
    l.batchSize=25
    r=l.learn()
    return r
def learn_xnes_batch_training():

	x0=np.array([0.0, 0.0, 0.0])
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
        li=[f[-25:],name,simulate(f,pol),simulate_max(f,pol)]
        grand_list.append(li)
    save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="a")


# Main
if __name__ == '__main__':
    args = docopt(__doc__, version='1.0.0rc2')
    with open(args["<norm_file>"]) as f:
        norm = [[float(e) for e in l.split(",")] for l in f]
    with open(args["<more_arg>"]) as f:
        more_arg = [l.strip() for l in f]
    policy_translation_dict={'-100000': 'lqf','0-10000': 'lpf','00-1000': 'lcfs','000-100': 'lexp','0000-10': 'lrf','00000-1': 'laf','000001': 'saf','000010': 'srf','000100': 'sexp','001000': 'fcfs','010000': 'spf','100000': 'sqf'}
    simulate_pure=True
    learning_dynamic_clairvoyant=False
    learning_offline_clairvoyant=False
    learning_offline=True
    learning_offline_stats=False
    testing_premade_vectors=False
    succsesive_learning=False
    pure_policy_list=get_pure_policy_list()
    grand_list=[]
    grand_list.append(["id","policy","avg","max"])
    save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="w")
	#performance of pure policies
    if(simulate_pure):
        print("simulating the 12 pure policies")
        for pol in pure_policy_list:
            print(pol)
            policy_name=policy_translation_dict[''.join(str(nb) for nb in pol)]
            execute_single_weeks(pol=pol,name=policy_name)

    if(learning_dynamic_clairvoyant):

        print("learning dynamic clairvoyant")
        grand_list=[]
        learned_vector_list=[]
        learned_vector_list_next=[]
        for file in args["<swf_file>"]:
            print("file:::::::::::::::::::::::::::::::::::::::",file)
            print("learning",file)
            r=learn_xnes()
            l=[file[-25:] , "xnes_dynamic_clairvoyant" , simulate(file,r[0]) , simulate_max(file,r[0])]
            print(l)
            grand_list.append(l)
            learned_vector_list.append([file,",".join(str(nb) for nb in r[0])])
            learned_vector_list_next.append([file,r[0]])
            save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="a")
            save_progress(l=learned_vector_list,file_name="logs/learned_vectors.csv",mode="a")
            grand_list=[]
            learned_vector_list=[]

    if (learning_offline_clairvoyant):
        print("learning offline clairvoyant")
        r=learn_xnes_batch()
        print("learned vector: ",r)
        name_learned="learning offline clairvoyant:"+",".join(str(nb) for nb in r[0])
        execute_single_weeks(pol=r[0],name="learning_offline_clairvoyant")
        save_progress(l=[["learning_offline_clairvoyant",",".join(str(nb) for nb in r[0])]],file_name="logs/learned_vectors.csv",mode="a")

    if(learning_offline):
        print("learning offline")
        #f_training,f_testing=divide_training_testing()
        size=len(args["<swf_file>"])
        f_training=args["<swf_file>"][:int(size/2)]
        f_testing=args["<swf_file>"][int(size/2):]
        print("training size: ",len(f_training))
        print("testing size: ",len(f_testing))
        r=learn_xnes_batch_training()
        print("learned vector: ",r)
        name_learned="learning offline:"+",".join(str(nb) for nb in r[0])
        execute_single_weeks(pol=r[0],name="learning_offline") 
        save_progress(l=[["learning_offline",",".join(str(nb) for nb in r[0])]],file_name="logs/learned_vectors.csv",mode="a")

    if(learning_offline_stats):
        print("learning offline many times")
        #f_training,f_testing=divide_training_testing()
        size=len(args["<swf_file>"])
        f_training=args["<swf_file>"][:int(size/2)]
        f_testing=args["<swf_file>"][int(size/2):]
                    
        print("training size: ",len(f_training))
        print("testing size: ",len(f_testing))

        for i in range(10):
            r=learn_xnes_batch_training()
            print("learned vector: ",r)
            save_progress(l=[["learning_offline_"+str(i),",".join(str(nb) for nb in r[0])]],file_name="logs/learned_vectors.csv",mode="a") 
            name_learned="learning offline:"+",".join(str(nb) for nb in r[0])
            execute_single_weeks(pol=r[0],name="learning_offline_"+str(i)) 
              
    
    if(succsesive_learning):
        print("testing each learned vector on the next week")
        # with open('logs/learned_vectors.csv') as f:#load all vectors:
        #     lines=f.readlines()
        i=0
        #we should skip the file and start reading form the second
        files=args["<swf_file>"][1:len(args["<swf_file>"])+1]
        grand_list=[]
        for file in files:
            # list_temp=lines[i].split(',')
            # print("list_temp 2: ",list_temp[1:])
            # vector= [float(e) for e in list_temp[1:]]
            # print("the vector is ",vector)
            week_name=learned_vector_list_next[i][0]

            vector=learned_vector_list_next[i][1]

            
            print("\n")#dispaly on terminal
            print("file: ",file[-25:] )
            print("learned from :",week_name)
            print("vector: ",vector)
            print("\n")
            
            
            l=[file[-25:]  , "past_week" , simulate(file,vector) ,simulate_max(file,vector)]
            grand_list.append(l)
            
            save_progress(l=grand_list,file_name="logs/policies_performace.csv",mode="a")
            grand_list=[]
            i+=1
            #test the vector
            #save the results

    if (testing_premade_vectors):
        print("testing premade vectors")
        premade_vector=[-0.19087185738,0.288745675215,-0.0941328562606,-0.152673629639,-0.114548550635,0.158445820014]
        execute_single_weeks(pol=premade_vector,name="batch_3_months") 		

