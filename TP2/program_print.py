import sys
import os

file_name = "output.vm"

def begin():
    f = open(file_name, "w")

def clean():
    os.remove(file_name)

def begin_instrs():
    f = open(file_name, "a")
    f.write("start\n")
    f.close

def end_instrs():
    f = open(file_name, "a")
    f.write("stop\n")
    f.close

def varDecl(value):
    f = open(file_name, "a")
    f.write("\tpushi " + str(value) + "\n")
    f.close

def atrib(offset):
    f = open(file_name, "a")
    f.write("\tstoreg " + str(offset) + "\n")
    f.close

def pushVar(offset):
    f = open(file_name, "a")
    f.write("\tpushg " + str(offset) + "\n")
    f.close

def pushNum(value):
    f = open(file_name, "a")
    f.write("\tpushi " + str(value) + "\n")
    f.close

def operation(op):
    f = open(file_name, "a")
    if op == '+':
        f.write("\tadd\n")
    elif op == '-':
        f.write("\tsub\n")
    elif op == '*':
        f.write("\tmul\n")
    elif op == '/':
        f.write("\tdiv\n")
    f.close

def read():
    f = open(file_name, "a")
    f.write("\tread\n")
    f.write("\tatoi\n")
    f.close

def write_num(number):
    f = open(file_name, "a")
    f.write("\tpushi " + str(number) + "\n")
    f.write("\twritei\n")
    f.close

def write_var(offset):
    f = open(file_name, "a")
    f.write("\tpushg " + str(offset) + "\n")
    f.write("\twritei\n")
    f.close

def write_str(string):
    f = open(file_name, "a")
    f.write("\tpushs " + string + "\n")
    f.write("\twrites\n")
    f.close