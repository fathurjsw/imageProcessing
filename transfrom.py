import os
import numpy as np 
 
def transform(pos):
# This function is used to find the corners of the object and the dimensions of the object
    pts=[]
    n=len(pos)
    for i in range(n):
        pts.append(list(pos[i][0]))
       
    sums={}
    diffs={}
    tl=tr=bl=br=0
    for i in pts:
        x=i[0]
        y=i[1]
        sum=x+y
        diff=y-x
        sums[sum]=i
        diffs[diff]=i
    sums=sorted(sums.items())
    diffs=sorted(diffs.items())
    n=len(sums)
    rect=[sums[0][1],diffs[0][1],diffs[n-1][1],sums[n-1][1]]
    #      top-left   top-right   bottom-left   bottom-right
   
    h1=np.sqrt((rect[0][0]-rect[2][0])**2 + (rect[0][1]-rect[2][1])**2)     #height of left side
    h2=np.sqrt((rect[1][0]-rect[3][0])**2 + (rect[1][1]-rect[3][1])**2)     #height of right side
    h=max(h1,h2)
   
    w1=np.sqrt((rect[0][0]-rect[1][0])**2 + (rect[0][1]-rect[1][1])**2)     #width of upper side
    w2=np.sqrt((rect[2][0]-rect[3][0])**2 + (rect[2][1]-rect[3][1])**2)     #width of lower side
    w=max(w1,w2)
   
    return int(w),int(h),rect