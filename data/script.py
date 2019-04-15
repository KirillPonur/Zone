import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.backends.backend_pdf import PdfPages
import os.path as path
plt.rc('text', usetex = True)
plt.rc('font', size=13, family = 'serif')
# plt.rc('text.latex',unicode=True)
plt.rc('legend', fontsize=14)
plt.rc('text.latex', preamble=r'\usepackage[russian]{babel}')

data = np.loadtxt(path.abspath('..\\data\\data.tsv'))
size = data.shape
Et, T, Iob, Ik1, Ik2 = [],[],[],[],[]

def get_dT(U):
    return -0.02 * U**4 + 0.42 * U**3 - 3.556 * U**2 + 39.46*U 
# Re = 10 #Ohm
# a = 20  #width
# d = 4  #thickness
# l = 7  #len between 1&2

Re = 10 #Ohm
a = 4  #width
d = 1.4  #thickness
l = 7  #len between 1&2

room_t = 28
k_b = 8.62 *10**(-5) ## eV/K
d_T = 5 # temp error
#Note, that the temperature is added with room temp of 28 degs C!
# print('Shape:',size)
for i in range(0,size[0]):
    Et.append(data[i][0])
    T.append(data[i][1])
    Iob.append(data[i][2])
    Ik1.append(data[i][3])
    Ik2.append(data[i][4])


T = np.array(T)
weights = np.ones(T.shape)
weights[0:4] = 0
# print(weights)
Et = np.array(Et)
Iob = np.array(Iob)
Ik1 = np.array(Ik1)
Ik2 = np.array(Ik2)
# Tt = get_dT(Et) + room_t + 273.15
# print(Tt)

#calcs
T = T + 273.15 #to kelvin 
Ik = (Ik1+Ik2)/2
Rob =  Ik*Re / Iob 
ro = (a*d / l) * Rob
sigma = 1/ro
k_T = 1000/T
ln_sigma = np.log(sigma)

print(ln_sigma)
print(T)
# err_10 = [2.5,2.5,2.5,2.5,2.5,0.1,0.1,0.1,0.1,0.1,]
# err_Iob = 0.1 / Iob # err,%
# err_Ik = err_10 / Ik
# print(err_Iob) 
# print(err_Ik)
eps_lns = np.ones(T.shape) * 0.02
d_lns = eps_lns * ln_sigma


n = (ln_sigma[0]-ln_sigma[1])/(np.log(T[0]/T[1]))
print('n = ',n)

#approx
pp = np.polyfit(k_T,ln_sigma,1, w = weights)
print('tan(theta) = ',pp[0])
print('ln(sigma)(0) = ',pp[1])
Wg = -pp[0]*2*k_b*1000
print('Wg = ', Wg,' эВ')
pf = np.poly1d(pp)

Tt = np.array([300,250,200,150,100,50])
A = (6*10**(-5))**n
sigma_T = A*Tt**n
# plt.errorbar(k_T[0:3],ln_sigma[0:3],yerr = d_lns[0:3],capsize =2,linestyle = '',color = 'black')
plt.plot(k_T,ln_sigma,'o-',color = 'magenta')
# plt.plot(1000/Tt,np.log(sigma_T),'ko-')
# plt.plot(np.log(T),n*np.log(6*10**(-5)*T))
# plt.grid(which = 'both')
plt.xlabel('$10^3 \cdot T^{-1},10^3\cdot K^{-1}$')
# plt.xlabel('$\ln T$')
plt.ylabel('$ln ~\sigma$')
plt.grid(which='major', linestyle='-')
plt.grid(which='minor', linestyle='-',color = 'lightgrey')
plt.minorticks_on()
plt.plot(k_T[weights>0],pf(k_T)[weights>0],'k--',lw =1)
# plt.savefig('graphs/lns3.png',dpi=500)

plt.show()