import numpy as np
import warnings
import matplotlib.pyplot as plt

x= np.loadtxt('pump1.txt',usecols=0,skiprows=3)
y= np.loadtxt('pump1.txt',usecols=1,skiprows=3)
e= np.loadtxt('pump1.txt',usecols=2,skiprows=3)
z=np.polyfit(x,y,3)
g=np.polyfit(x,e,3)
print("z= {}".format(z))
print("g= {}".format(g))
p=np.poly1d(z)
h=np.poly1d(g)
print('h= {}'.format(h))
print("p= {}".format(p))
with warnings.catch_warnings():
    warnings.simplefilter('ignore', np.RankWarning)
    p30 = np.poly1d(np.polyfit(x, e, 50))
xp=np.linspace(15,45,100)

fig, ax1 =plt.subplots()
ax1.plot(x,y,'wo',mec='k')
ax1.plot(xp,p(xp),'--',color='k')
ax1.set_ylim(5,75)
ax1.set_ylabel('Head(ft)')
ax1.set_xlabel('Flow Rate (gpm)')
ax2=ax1.twinx()
ax2.set_ylabel('Efficiency (%)')
ax2.plot(x,e,'^',color='w',mec='k')
ax2.plot(xp,h(xp),':',color='k')
ax2.set_ylim(5,59)
#plt.plot(x,y,'wo',mec='k')
#plt.plot(xp,p(xp),'--',color='k')
#plt.plot(x,e,'^',color='k')
#plt.ylim(0,75)

plt.show()