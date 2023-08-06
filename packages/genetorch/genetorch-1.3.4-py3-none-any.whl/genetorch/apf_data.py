import os
import sys


def model(gene):
    lst = os.listdir(os.path.join(os.getcwd(),"genetorch\\apf"))
    if gene+'.apf' in lst:
        return os.path.join(os.getcwd(), "genetorch\\apf\\{}.apf".format(gene))
    else:
        print("file not exist, please refer to https://alphafold.com/",file=sys.stderr)
