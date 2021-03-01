import math #For pow and sqrt
import sys
import matplotlib.pyplot as plt
from random import shuffle, uniform
import threading as th
import numpy as np
import time
import os
import numpy as np
from bitstring import Bits

X=[]
no_th=10
look_distance=4   #0.8
kernel_bandwidth=2
no_iter=5
circles=[]
ind=0


def ReadOutput():
	f=open("out.txt",'r')
	line= f.read()
	f.close()
	return(line[0:-1])
def add(a_int,b_int):
	a_int=int(a_int*1024)
	b_int=int(b_int*1024)
	a=np.binary_repr(a_int, width=64)
	b=np.binary_repr(b_int, width=64)
	cmd="./adder +a="+a+" +b="+str(b)+" > out.txt"
	os.system(cmd)
	sum=ReadOutput()
	#print(sum)
	sum=Bits(bin=sum)
	return(round((sum.int/1024),3))

def multiplier(a_int,b_int):
	a_int=int(a_int*1024)
	b_int=int(b_int*1024)
	if(a_int<0 and b_int<0):
		a=-a_int
		b=-b_int
		cmd="./multiplier +a="+str(a)+" +b="+str(b)+" > out.txt"
		os.system(cmd)
		prod=ReadOutput()
		prod=int(prod)
	elif(a_int<0 and b_int>0):
		a=-a_int
		b=b_int
		cmd="./multiplier +a="+str(a)+" +b="+str(b)+" > out.txt"
		os.system(cmd)
		prod=ReadOutput()
		prod=-1*int(prod)
	elif(a_int>0 and b_int<0):
		a=a_int
		b=-b_int
		cmd="./multiplier +a="+str(a)+" +b="+str(b)+" > out.txt"
		os.system(cmd)
		prod=ReadOutput()
		prod=-1*int(prod)
	else:
		a=a_int
		b=b_int
		cmd="./multiplier +a="+str(a)+" +b="+str(b)+" > out.txt"
		os.system(cmd)
		prod=ReadOutput()
		prod=int(prod)
	return(round((prod/(1024*1024)),3))



def ReadData(fileName):
    #Read the file, splitting by lines
    f = open(fileName,'r');
    liness = f.read().splitlines();
    f.close();

    items = [];

    for i in range(0,len(liness)):
        line = liness[i].split(',');
        itemFeatures = [];

        for j in range(len(line)):
            v = float(line[j]); #Convert feature value to float
            itemFeatures.append(v); #Add feature value to dict

        items.append(itemFeatures);

    shuffle(items);
    return items;


def euclid_distance(x,y):
	S = 0; #The sum of the squared differences of the elements
	for i in range(len(x)):
        # diff=x[i]-y[i]
		diff=add(x[i],-y[i])
        # S+=diff*diff
		S=add(S,multiplier(diff,diff))
	#print("S = ",S)
	ret=math.sqrt(S)
    #print("euuci"+str(ret))
	return ret; #The square root of the sum

def neighbourhood_points(X, x_centroid, distance):
    eligible_X = []
    for x in X:
        distance_between = euclid_distance(x, x_centroid)
        # print('Evaluating: [%s vs %s] yield dist=%.2f' % (x, x_centroid, distance_between))
        if distance_between <= distance:
            eligible_X.append(x)
    return eligible_X

def gaussian_kernel(distance, bandwidth):
	div=(distance / bandwidth)
    # div_sq=div*div
	div_sq=multiplier(div,div)
	# val = (1/(bandwidth*math.sqrt(2*math.pi))) * np.exp(-0.5*div_sq)
	m1=multiplier(2,math.pi)
	m2=multiplier(-0.5,div_sq)
	m3=multiplier(bandwidth,math.sqrt(m1))
	val = multiplier((1/m3),np.exp(m2))
	return val

def runner(X,x,i):
    ### Step 1. For each datapoint x E X, find the neighbouring points N(x) of x.
	neighbours = neighbourhood_points(X, x, look_distance)

    ### Step 2. For each datapoint x E X, calculate the mean shift m(x).
	numerator = [0]*len(x)
	denominator = 0
	for neighbour in neighbours:
		distance = euclid_distance(neighbour, x)
		weight = gaussian_kernel(distance, kernel_bandwidth)
		for j in range(len(x)):
			# numerator[j] += (weight * neighbour[j])
			numerator[j]=add(numerator[j],multiplier(weight,neighbour[j]))
		denominator = add(denominator,weight)            ########
		# denominator+=weight

	new_x=[0]*len(x)
	for j in range(len(x)):
		new_x[j] = numerator[j] / denominator
        ### Step 3. For each datapoint x E X, update x <- m(x).
	X[i] = new_x

	print(new_x)


def meanShift(original_X):

    X = np.copy(original_X)
    past_X = [[0,0]]*len(X)
    print("l = "+str(len(X)))
    for it in range(no_iter):
        for i in range(0,len(X)):       #for i, x in enumerate(X):
            print("i = "+str(i))
            runner(X,X[i],i)
            circle=plt.Circle((X[i][0],X[i][1]),radius=look_distance,fill=False,color='b')
            plt.gcf().gca().add_artist(circle)
            circles.append(circle)
            plt.pause(0.0001)

        for c in circles:
            c.remove()
            plt.pause(0.0001)
        circles.clear()

        past_X=np.copy(X)
    unique=[]
    color=["red","blue","green","purple","yellow","orange","pink","cyan","black","magenta","goldenrod","teal","plum"]
    for i in range(len(X)):
        flag=0
        for j in range(len(unique)):
            if(euclid_distance(X[i],unique[j]) < 0.1 ):
                flag=1
                break
        if(flag==0):
            unique.append(X[i])
    print(unique)
    for i in range(len(X)):
        for j in range(len(unique)):
            if(euclid_distance(X[i],unique[j]) < 0.1):
                ind=j
        plt.scatter(original_X[i][0],original_X[i][1],c=color[ind],alpha=0.5,s=10)
        plt.pause(0.0001)




def CutToTwoFeatures(items,indexA,indexB):
    n = len(items);
    X = [];
    for i in range(n):
        item = items[i];
        newItem = [item[indexA],item[indexB]];
        X.append(newItem);
    return X;

def main():

    items = ReadData('data1.txt')
    items = CutToTwoFeatures(items,0,1)
    print(items)
    for item in items:
        plt.scatter(item[0],item[1],c="gray",alpha=0.5,s=10)
        plt.pause(0.00001)

    meanShift(items)
    plt.show();

if __name__ == "__main__":
    main();
