#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 10:12:08 2021

@author: user
"""
import os
import subprocess
prStr1=['python','Testy2.py']
#subprocess.run("~/Desktop/tutoprial/stopWatch.py")
#subprocess.run(['python',prStr1])
#prStr1=['ls', '-l']

# process = subprocess.Popen(prStr1, stdout=subprocess.PIPE)
# while True:
#     output = process.stdout.readline().decode()
#     if output == '' and process.poll() is not None:
#         break
#     if output !='':
#         print(output)
try:
    p=subprocess.check_call(prStr1, shell=False,stdout=subprocess.PIPE, universal_newlines=True)

    print(p)

except subprocess.CalledProcessError as e:
    print("Call to microphonics script failed \n"+str(e))
    
   
#subprocess.CompletedProcess(['python','stopWatch.py'], returncode=0)

print('the code waited for the process to complete')