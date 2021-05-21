import sys

file_name = "output.vm"

def begin():
    f = open(file_name, "w")

def begin_instrs():
    f = open(file_name, "a")
    f.write("start\n")
    f.close

def end_instrs():
    f = open(file_name, "a")
    f.write("stop\n")
    f.close

def var(value):
    f = open(file_name, "a")
    f.write("\tpushi " + value + "\n")
    f.close

def atrib(offset, value):
    f = open(file_name, "a")
    f.write("\tpushi " + value + "\n")
    f.write("\tstoreg " + offset + "\n")
    f.close
