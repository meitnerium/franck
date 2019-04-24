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



def converg_analyse(files,label):
  #from ase.io.formats import iread
  #import ase
  import math
  import matplotlib.pyplot as plt
  #test=iread(filename='scf.out', format='espresso-out')
  #print(test)
  #ase.io.read_es
  import numpy as np
  print("range = "+str(len(files)))
  dens=[]
  alpha=[]
  beta=[]
  gamma=[]
  a=[]
  b=[]
  c=[]
  for i in range(len(files)):
    file=files[i]
    dens1,v1,v2,v3=getvec(file)
    dens.append(np.float(dens1))


    alpha.append(angle(v2,v3)/math.pi*180.)
    beta.append(angle(v1,v3)/math.pi*180.)
    gamma.append(angle(v1,v2)/math.pi*180.)
    a.append(length(v1))
    b.append(length(v2))
    c.append(length(v3))
    print("a,b,c in "+files[i]+" = "+str(length(v1))+","+str(length(v2))+","+str(length(v3)))


  fig1, ax1 = plt.subplots()
  x=np.arange(1,len(files)+1,1)
  ax1.plot(x,a,label="a")
  ax1.plot(x,b,label="b")
  ax1.plot(x,c,label="c")
  plt.xlabel("Mesh grid size")
  plt.ylabel(r"Vector length (bohr)")
  #plt.legend(loc=11)
  ax2 = ax1.twinx()
  ax2.plot(x,alpha,'b--',label=r"$\alpha$")
  ax2.plot(x,beta,'--',color="orange",label=r"$\beta$")
  ax2.plot(x,gamma,'g--',label=r"$\gamma$")
  ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.20),
          fancybox=True, shadow=True, ncol=5)
  ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10),
          fancybox=True, shadow=True, ncol=5)
  plt.xticks(x)
  plt.ylabel(r"Angle (${}^o$)")
  plt.subplots_adjust(top=0.85, right=0.85)
  plt.savefig("convergvec.png")
  #plt.axis([1,3,4.4,8.3])
  plt.show()
  plt.close()

  #fig=plt.figure(figsize=[8,6])

  fig1, ax1 = plt.subplots()
  ax1.plot(x,dens)
  plt.xlabel("Mesh grid size")
  plt.ylabel(r"Density ($g . cm^{-3}$)")
  #plt.legend(loc=11)
  #ax2.plot(x,gamma,'g--',label=r"$\gamma$")
  #ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.20),
  #          fancybox=True, shadow=True, ncol=5)
  plt.xticks(x)
  plt.subplots_adjust(top=0.85, right=0.85)
  plt.savefig("convergdens.png")
  #plt.axis([1,3,4.4,8.3])
  plt.show()
  plt.close()



def getlastgrom(file):
    lines=open(file).readlines()
    for i in range(len(lines)):
        if lines[i][0:23] == 'Begin final coordinates':
            for j in range(50):
                print(lines[i+j])

def getvec(file):
    import re
    import numpy as np
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
    import math
    return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
    import math
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
    files=["1_1_1/scf.out","2_2_2/scf.out","3_3_3/scf.out","4_4_4/scf.out","5_5_5/scf.out","6_6_6/scf.out","7_7_7/scf.out","8_8_8/scf.out"]
    labels=["1_1_1/scf.out","2_2_2/scf.out","3_3_3/scf.out","4_4_4/scf.out","5_5_5/scf.out","6_6_6/scf.out","7_7_7/scf.out","8_8_8/scf.out"]
    converg_analyse(files,labels)
