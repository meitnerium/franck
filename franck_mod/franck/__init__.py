import math
import re
import numpy as np

def getlastgeom(file,outfile):
    f=open(outfile,'w')
    lines=open(file).readlines()
    for i in range(len(lines)):
        if lines[i][0:23] == 'Begin final coordinates':
            j=4
            while("End final coordinates" not in lines[i+j]):
                print(lines[i+j])
                f.write(lines[i+j])
                j=j+1




def getvec(file):
    lines=open(file).readlines()
    dens=""
    for i in range(len(lines)):
        if lines[i][0:23] == 'Begin final coordinates':
            print("0:"+lines[i])
            print("1:"+lines[i+1])
            print("2:"+lines[i+2])
            m = re.match(r'.* density = (.*) g', lines[i+2])
            print(m)
            dens=m.group(1)
            print("3:"+lines[i+3])
            print("4:"+lines[i+4])
            print("5:"+lines[i+5])
            v1=np.fromstring(lines[i+5],sep=' ')
            print(str(i)+":"+lines[i+6])
            v2=np.fromstring(lines[i+6],sep=' ')
            print(str(i)+":"+lines[i+7])
            v3=np.fromstring(lines[i+7],sep=' ')
    return dens,v1,v2,v3
#print("test")
#print(a[0])

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def get_final_dens(file):
   f = open(file)
   lines=f.readlines()
   for i in range(len(lines)):
      if 'Begin final coordinates' in lines[i]:
         #m = re.match(r'new unit-cell volume = (.*) a.u.^3', lines[i+1])
         m = re.match(r'.*new unit-cell volume = (.*) a', lines[i+1])
         print(m)
         print(m.group(1))

   return m.group(1)


if __name__ == "__main__":
    getlastgeom('C:/Users/fdion/Documents/Francois/Python/ir_vib/test/536770/5_5_5/scf.out',"test.in")
