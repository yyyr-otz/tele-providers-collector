import os
import wget
import json
import math
import string
import random
import jdatetime
import re
import urllib.parse
# 定义去重函数

def remove_duplicate_lines(file_path):
    lines = set()
    with open(file_path, 'r') as file:
        for line in file:
            lines.add(line)
    lines = list(lines)
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)
    return True
    
# 对待测节点去重 
if remove_duplicate_lines("./collected-proxies/row-url/all.txt"):
    print("待测节点./collected-proxies/row-url/all.txt"+"去重完成")
        
# 待测节点分割
with open("./collected-proxies/row-url/all.txt", "r") as file:
    file = file.readlines()
    num_part = 3
    start = 0
    num_lines = len(file)
    part_size = ( num_lines // num_part ) + 1
    end = part_size
    for i in range(num_part):
        part_name = "./collected-proxies/row-url/all_" + str(i+1)
        with open(part_name, 'w') as part_f:
            part_f.write(''.join(file[start:end]))
        start = start + part_size
        end = end + part_size
    print(os.listdir("./collected-proxies/row-url/"))
# xray配置分割
with open("./collected-proxies/xray-json/actives_all.txt", "r") as file:
    file = file.readlines()
    num_part = 3
    start = 0
    num_lines = len(file)
    part_size = ( num_lines // num_part ) + 1
    end = part_size
    for i in range(num_part):
        part_name = "./collected-proxies/xray-json/actives_now_" + str(i+1)
        with open(part_name, 'w') as part_f:
            part_f.write(''.join(file[start:end]))
        start = start + part_size
        end = end + part_size
    print(os.listdir("./collected-proxies/xray-json/"))
# 活跃节点分割
with open("./collected-proxies/row-url/actives.txt", "r") as file:
    file = file.readlines()
    num_part = 3
    start = 0
    num_lines = len(file)
    part_size = ( num_lines // num_part ) + 1
    end = part_size
    for i in range(num_part):
        part_name = "./collected-proxies/row-url/actives_now_" + str(i+1)
        with open(part_name, 'w') as part_f:
            part_f.write(''.join(file[start:end]))
        start = start + part_size
        end = end + part_size
    print(os.listdir("./collected-proxies/row-url/"))

