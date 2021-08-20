#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 10:12:08 2021

@author: user
"""
import os
import sys
import subprocess
prStr1=['python','rs']
#subprocess.run("~/Desktop/tutoprial/stopWatch.py")
#subprocess.run(['python',prStr1])
#prStr1=['ls', '-l']
try:
    
    process = subprocess.Popen(prStr1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return_code = process.poll()
    out = out.decode(sys.stdin.encoding)
    err = err.decode(sys.stdin.encoding)
#    print(out, return_code)
    
#except:
    if return_code !=0:
#        print(err)
        e = subprocess.CalledProcessError(return_code, prStr1, output=out)
        e.stdout, e.stderr = out, err
        print("Call to microphonics script failed \n"+str(e))
        
except subprocess.CalledProcessError as e:
    print("Call to microphonics script failed \n"+str(e))        
# try:
#     p=subprocess.check_call(prStr1, shell=False,stdout=subprocess.PIPE, universal_newlines=True)

# #    print(p)

# except subprocess.CalledProcessError as e:
#     print("Call to microphonics script failed \n"+str(e))
    
   
#subprocess.CompletedProcess(['python','stopWatch.py'], returncode=0)

print('the code waited for the process to complete')