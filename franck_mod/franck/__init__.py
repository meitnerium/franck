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



def converg_analyse(files,label,show=[1,1,1,1,1,1]):
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
    print("alpha,beta,gamma in "+files[i]+" = "+str(angle(v2,v3)/math.pi*180.)+","+str(angle(v1,v3)/math.pi*180.)+","+str(angle(v1,v2)/math.pi*180.))


  fig1, ax1 = plt.subplots()
  x=np.arange(1,len(files)+1,1)
  if show[0]==1:
    ax1.plot(x,a,label="a")
  if show[1]==1:
    ax1.plot(x,b,label="b")
  if show[2]==1:
    ax1.plot(x,c,label="c")
  plt.xlabel("Mesh grid size")
  plt.ylabel(r"Vector length (bohr)")
  #plt.legend(loc=11)
  if show[3] == 1 or show[4] == 1 or show[5] == 1:
    ax2 = ax1.twinx()
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10),
          fancybox=True, shadow=True, ncol=5)
  if show[3]==1:
    ax2.plot(x,alpha,'b--',label=r"$\alpha$")
  else if show[3]==-1:
    ax2.plot(x,180.-alpha,label=r"$\alpha$")
  if show[4]==1:
    ax2.plot(x,beta,'--',color="orange",label=r"$\beta$")
  else if show[4]==-1:
    ax2.plot(x,180.-beta,label=r"$\beta$")
  if show[5]==1:
    ax2.plot(x,gamma,'g--',label=r"$\gamma$")
  else if show[5]==-1:
    ax2.plot(x,180.-gamma,label=r"$\gamma$")
  ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.20),
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

def getfreq(dmout):
    freq=[]
    intens=[]
    print("analysing "+str(dmout))
    lines=open(dmout).readlines()
    for i in range(len(lines)):
        if 'IR activities are in (D/A)^2/amu units' in lines[i]:
            j=3
            while 'DYNMAT' not in lines[i+j+1]:  
                #print(str(lines[i+j].split()))
                #print("freq")
                #print(str(lines[i+j].split()[1])+" "+str(lines[i+j].split()[3]))
                freq.append(np.float(lines[i+j].split()[1]))
                #print("intens")
                #print(lines[i+j].split()[3])
                intens.append(np.float(lines[i+j].split()[3]))
                j=j+1
            break

    return freq,intens
















def lorentz(r, x, x0):
    """
    :param r: mid-height witdh of the lorentz function
    :param x: x-value for the evaluation
    :param x0: abscice of the maximum of the lorentz function
    :return: Amplitude of the Lorentz at the x value
    """
    under=(r/2)**2+(x-x0)**2
    l=r/(2*np.pi)*1/under
    return(l)


def normalize(vec):
    output=vec/np.max(vec)
    return output


def freqanharmscan(output,freqanharm,intensanharm,Nvibs):
    f=open(output)
    for line in f:
        #print(line)
        #print(' Cite this work as:')
        #wait = input("PRESS ENTER TO CONTINUE.")
        if line[0:19] == ' Cite this work as:':
            print("it's here")
            line = next(f)
            print(line)
            if line[0:28] == ' Gaussian 09, Revision C.01,':
                GAUSSMAIN = '09'
                GAUSSREV = 'c.01'
                print('Version = '+GAUSSMAIN+GAUSSREV)
            if line[0:28] == ' Gaussian 16, Revision A.03,':
                GAUSSMAIN = '16'
                GAUSSREV = 'a.03'
                print('Version = '+GAUSSMAIN+GAUSSREV)
            if line[0:28] == ' Gaussian 16, Revision B.01,':
                GAUSSMAIN = '16'
                GAUSSREV = 'b.01'
                print('Version = '+GAUSSMAIN+GAUSSREV)
            if line[0:28] == ' Gaussian 09, Revision E.01,':
                GAUSSMAIN = '09'
                GAUSSREV = 'e.01'
                print('Version = '+GAUSSMAIN+GAUSSREV)
            #wait = input("PRESS ENTER TO CONTINUE.")

        # For FREQ=Anharm, extract anharmonicity frequency
        #print(line)
        if line[14:46] == "Anharmonic Infrared Spectroscopy":
            #print("test")
            #Nvibs = len(vibfreqs)
            print('Nvibs = ' + str(Nvibs))
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)

            #freqanharm=np.zeros(Nvibs,"d")
            for i in range(Nvibs):
                #print('i='+str(i))
                line = next(f)
                #print('freqanharm = '+line[33:44]+ "intensanharm = "+line[63:79])
                if GAUSSMAIN == '16':
                    freqanharm[i]=line[37:46]
                else:
                    freqanharm[i] = line[33:44]
                    #print('freqanharm')
                    #print(freqanharm[i])
                #print(line[62:76])
                if (line[62:76] == '************\n'):
                    intensanharm[i]=line[46:59]
                else:
                    intensanharm[i]=line[63:79]


def mkspectra(freqx,vibfreqs,iract,r):
    """
    mkspectra create a IR spectra with lorentz function correlated to vibrationnal frequency value with iract amplitude
    :param freqx: frequence vector used to create the spectra
    :param vibfreqs: theoritical vibrationnal frequency
    :param amp: Ir activities of each vibrationnal frequency
    :return: Absorbance for each freqx value
    """
    spectra=np.zeros(len(freqx))
    for i in range(len(freqx)):
        spectra[i]=0

        for j in range(len(vibfreqs)):
            #TODO calculate correctly the amplitude (amp[i])
            spectra[i]=spectra[i]+lorentz(r,freqx[i],vibfreqs[j])*iract[j]

    return spectra



def freqanharmscan2(output,freqanharm,intensanharm,Nvibs):
    f=open(output)
    for line in f:
        #print(line)
        #print(' Cite this work as:')
        #wait = input("PRESS ENTER TO CONTINUE.")
        if line[0:19] == ' Cite this work as:':
            print("it's here")
            line = next(f)
            print(line)
            if line[0:28] == ' Gaussian 09, Revision C.01,':
                GAUSSMAIN='09'
                GAUSSREV='c.01'
                print('Version = '+GAUSSMAIN+GAUSSREV)
            if line[0:28] == ' Gaussian 16, Revision A.03,':
                GAUSSMAIN='16'
                GAUSSREV='a.03'
                print('Version = '+GAUSSMAIN+GAUSSREV)
            if line[0:28] == ' Gaussian 16, Revision B.01,':
                GAUSSMAIN='16'
                GAUSSREV='b.01'
                print('Version = '+GAUSSMAIN+GAUSSREV)
            if line[0:28] == ' Gaussian 09, Revision E.01,':
                GAUSSMAIN='09'
                GAUSSREV='e.01'
                print('Version = '+GAUSSMAIN+GAUSSREV)
            #wait = input("PRESS ENTER TO CONTINUE.")

        # For FREQ=Anharm, extract anharmonicity frequency
        #print(line)
        if line[14:46] == "Anharmonic Infrared Spectroscopy":
            print("testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest")
            #Nvibs = len(vibfreqs)
            print('Nvibs = ' + str(Nvibs))
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)

            #freqanharm=np.zeros(Nvibs,"d")
            for i in range(Nvibs):
                #print('i='+str(i))
                line = next(f)
                #print('freqanharm = '+line[33:44]+ "intensanharm = "+line[63:79])
                #GAUSSMAIN='16'
                if GAUSSMAIN == '16':
                    freqanharm[i]=line[37:47]

                else:
                    freqanharm[i] = line[33:44]
                if (line[62:76] == '************\n'):
                    intensanharm[i]=line[46:59]
                else:
                    intensanharm[i]=line[63:79]
                #print("Fondamental freqanharm " +str(i)+ " = "+str(freqanharm[i])+" Intense = "+str(intensanharm[i]))
            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            for j in range(Nvibs):
                line = next(f)
                print(line[37:47])
                freqanharm[i+j+1] = line[37:47]
                if (line[62:76] == '************\n'):
                    intensanharm[i+j+1]=line[46:59]
                else:
                    intensanharm[i+j+1]=line[63:79]
                #print("Overtone freqanharm " +str(i+j+1)+ " = "+str(freqanharm[i+j+1])+" Intense = "+str(intensanharm[i+j+1]))
            line = next(f)
            print(line)
            line = next(f)
            line = next(f)
            line = next(f)
            for k in range(int(Nvibs*(Nvibs-1)/2)):
                line = next(f)
                print("line[37:47] = "+line[37:47])
                freqanharm[i+j+k+2] = line[37:47]
                if (line[62:76] == '************\n'):
                    intensanharm[i+j+k+2]=line[46:59]
                else:
                    intensanharm[i+j+k+2]=line[63:79]

                #print("Combination freqanharm " +str(i+j+k+2)+ " = "+str(freqanharm[i+j+k+2])+" Intense = "+str(intensanharm[i+j+k+2]))
            # calculate the number of  Combination Bands

            line = next(f)
            line = next(f)
            line = next(f)
            line = next(f)
            ntest=0
            print("Nvibs = "+str(Nvibs))
            #input("Press any key")
#            for i in range(58):
#                if i != 0:
#                    ntest=ntest+(i-1)
#                    #print(str(i)+" * "+str(i-1))
#                    #input("Press any key")
#            print(ntest)
#            for k in range(ntest):
#                line = next(f)
#                print("line[37:46] = "+line[37:47])
#                tmpfreqanharm = line[37:47]
#                if (line[62:76] == '************\n'):
#                    tmpintensanharm=line[46:59]
#                else:
#                    tmpintensanharm=line[63:79]
#               if k==0:
#                    print(line)
#                    print("first one : ")
#                    print(tmpfreqanharm)
#                    print(tmpintensanharm)
#                    input("Press any key")
#            print("lastone")
#            print(tmpfreqanharm)
#            print(tmpintensanharm)
#            input("Press any key")














#font = {'size'   : 12}

#matplotlib.rc('font', **font)

#from jcamp import JCAMP_reader
#jcamp_dict = JCAMP_reader("NaClO4.H2O/B6000524-IR.jdx")
#x=np.array(jcamp_dict['x'])
#xcm=1/(x*10**(-4))
#if jcamp_dict['yunits'] == 'TRANSMITTANCE':
#            print('Unit is TRANSMITTANCE, changing to absorbance')
#            y = np.array(-np.log(jcamp_dict['y']))
#else:
#            print('Unit is '+jcamp_dict['yunits']+', keeping it')
#            y = np.array(jcamp_dict['y'])
#ynorm=normalize(y)
#plt.plot(xcm,ynorm,'black',label="Experimental")

#from cclib.parser import ccopen


#fileg='GAUSSIAN/B3LYP/aug-cc-pvdz/freq.log'
#logfile=ccopen(fileg)
#data=logfile.parse()
#gspectra=normalize(mkspectra(freq,data.vibfreqs,data.vibirs,10))
#plt.plot(freq,gspectra,'green',label="Single molecule")
#plt.plot(freq,gspectra,'green',label="Single molecule (harm)")

#anharmfile='GAUSSIAN/B3LYP/aug-cc-pvdz/anharm.log'
#freqanharm=np.zeros(int(2*len(data.vibfreqs)+len(data.vibfreqs)*(len(data.vibfreqs)-1)/2))
#intensanharmtmp=np.zeros(int(2*len(data.vibfreqs)+len(data.vibfreqs)*(len(data.vibfreqs)-1)/2))
#intensanharm=np.zeros(int(2*len(data.vibfreqs)+len(data.vibfreqs)*(len(data.vibfreqs)-1)/2))
#freqanharmscan2(anharmfile,freqanharm,intensanharmtmp,len(data.vibfreqs))

#freqanharm = np.zeros(len(data.vibfreqs))
#intensanharmtmp = np.zeros(len(data.vibfreqs))
#intensanharm = np.zeros(len(data.vibfreqs))
#freqanharmscan('GAUSSIAN_DIMER/B3LYP/aug-cc-pvdz/anharm.log',freqanharm,intensanharmtmp,len(data.vibfreqs)) #To be modified with frescan
#sort = np.argsort(freqanharm)
#freqanharm=np.sort(freqanharm)
#for k in range(len(intensanharmtmp)):
#        intensanharm[k]=intensanharmtmp[sort[k]]

#sort=np.argsort(freqanharm)
#freqanharm=np.sort(freqanharm)

#for k in range(len(intensanharmtmp)):
    #    ws['D'+str(k+2)] = freqanharm[k]
#    intensanharm[k]=intensanharmtmp[sort[k]]
    #print(str(k)+" "+str(freqanharm[k])+" "+str(intensanharm[k]))
#print("Len viharm = "+str(data.vibfreqs)+" Len anharm = "+str(len(freqanharm)))

#anharmspectra=normalize(mkspectra(freq,freqanharm,intensanharm,10))
#plt.plot(freq,anharmspectra,'r',label="Single molecule (anharm)")




#data=np.genfromtxt('exp/FOX7.1.dpt')

#Y=normalize(data[:,1])
#plt.plot(data[:,0],Y,'black',label="Experimental")

#f=open("spectra.txt",'w')
#for i in range(len(freq)):
#  f.write(str(freq[i])+" "+str(gspectra[i])+"\n")
#
#plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=14)
#plt.ylabel('Normalized absorbance',fontsize=14)
#plt.subplots_adjust(bottom=0.2)
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#majorLocator = MultipleLocator(500)
#majorFormatter = FormatStrFormatter('%d')
#minorLocator = MultipleLocator(100)
#plt.legend()

#plt.axis([40,4000,0,1.05])

#plt.savefig("spectra.png")
#plt.show()


#fileg='/backup/QCDB/516900/GAUSSIAN/B3LYP/6-311plusplusG_3dfvirg3pd_/freq.log'
#logfile=ccopen(fileg)
#data=logfile.parse()
#gspectra=normalize(mkspectra(freq,data.vibfreqs,data.vibirs,10))
#plt.plot(freq,gspectra,'g',label="Predicted gas phase")
#f=open("spectra.txt",'w')
#for i in range(len(freq)):
#  f.write(str(freq[i])+" "+str(gspectra[i])+"\n")
#
#plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=14)
#plt.ylabel('Normalized absorbance',fontsize=14)
#plt.subplots_adjust(bottom=0.2)
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter
#
#majorLocator = MultipleLocator(500)
#majorFormatter = FormatStrFormatter('%d')
#minorLocator = MultipleLocator(100)



#ax.xaxis.set_major_locator(majorLocator)
#ax.xaxis.set_major_formatter(majorFormatter)
#plt.axis([600,3200,0,1.1])
# for the minor ticks, use no labels; default NullFormatter
#ax.xaxis.set_minor_locator(minorLocator)
#im = plt.imread('1706.png')
#newax = fig.add_axes([0.25, 0.3, 0.4, 0.4], anchor='NE')
#newax.imshow(im)
#newax.axis('off')
#ax.annotate("", xy=(1190, 0.5), xytext=(1260, 0.3), arrowprops=dict(arrowstyle="->"))
#im2 = plt.imread('ch2_waving.png')
#newax2 = fig.add_axes([-0.06, 0.45, 0.4, 0.4], anchor='NE')
#newax2.imshow(im2)
#newax2.axis('off')
#freqanharm = np.zeros(len(data.vibfreqs))
#intensanharmtmp = np.zeros(len(data.vibfreqs))
#intensanharm = np.zeros(len(data.vibfreqs))
#freqanharmscan('/backup/QCDB/516900/GAUSSIAN/B3LYP/6-311plusplusG_3dfvirg3pd_/anharm.log',freqanharm,intensanharmtmp,len(data.vibfreqs)) #To be modified with frescan
#sort = np.argsort(freqanharm)
#freqanharm=np.sort(freqanharm)
#for k in range(len(intensanharmtmp)):
#        intensanharm[k]=intensanharmtmp[sort[k]]

#anharmspectra=normalize(mkspectra(freq,freqanharm,intensanharm,10))
#plt.plot(freq,anharmspectra,'r',label="Predicted anharmonic gas phase")
#ax.annotate("", xy=(1850, 0.5), xytext=(1710, 0.3), arrowprops=dict(arrowstyle="->"))
#plt.legend()
#plt.savefig('KClO4.png')
#plt.show()
#plt.close()


































if __name__ == "__main__":
    #getlastgeom('C:/Users/fdion/Documents/Francois/Python/ir_vib/test/536770/5_5_5/scf.out',"test.in")
    #files=["1_1_1/scf.out","2_2_2/scf.out","3_3_3/scf.out","4_4_4/scf.out","5_5_5/scf.out","6_6_6/scf.out","7_7_7/scf.out","8_8_8/scf.out"]
    #labels=["1_1_1/scf.out","2_2_2/scf.out","3_3_3/scf.out","4_4_4/scf.out","5_5_5/scf.out","6_6_6/scf.out","7_7_7/scf.out","8_8_8/scf.out"]
    #converg_analyse(files,labels,[1,1,1,1,1,1])
    freq,intens = getfreq('exemples/dm.out')
    x=np.arange(40,3500,1)
    spectra=normalize(mkspectra(x,freq,intens,10))
    import matplotlib.pyplot as plt
    fig1, ax = plt.subplots()
    plt.plot(x,spectra,label='solid state prediction')
    plt.xlabel(r'Wavenumber ($cm^{-1}$)',fontsize=14)
    plt.ylabel('Normalized absorbance',fontsize=14)
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter
    majorLocator = MultipleLocator(500)
    minorLocator = MultipleLocator(100)
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_minor_locator(minorLocator)
    majorFormatter = FormatStrFormatter('%d')
    ax.xaxis.set_major_formatter(majorFormatter)
    plt.legend()
    plt.show()
