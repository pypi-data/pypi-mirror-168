'''
Created on 2022年8月22日

@author: 86139
'''
from  pipetool.runner import seg_generator

seq = seg_generator('中环人们的男的女的调度的的的的的阿斯顿发发斯蒂芬八十多分',5,3)

for s in seq:
    print(s)