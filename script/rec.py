from pylab import *
from matplotlib import rc
import os.path as path
import sys
from scipy.optimize import curve_fit
from pandas import read_excel as read
from sympy import symbols,limit
rc('text', usetex=True)
rc('text.latex', preamble=[r'\usepackage[russian]{babel}',
                         r'\usepackage{amsmath}',
                        r'\usepackage{amssymb}'])


rc('font', family='serif')
grad = path.abspath('..\\data\\grad.xlsx')
def func(x,a,b,c,d):
	return a*x**4+b*x**3+c*x**2+d*x
df=read(grad, sheet_name='1')
x=array(df['x'])
y=array(df['y'])



popt, pcov = curve_fit(func,y,x)
a,b,c,d=popt
EDS2T = lambda x: a*x**4+b*x**3+c*x**2+d*x

rec = path.abspath('..'+'\\data\\rec.xlsx')
df=read(rec, sheet_name='1')


et=linspace(0,10,1000)
Et = array(df['ЭДС']) #mВ
T = EDS2T(Et)
# plot(T, Et)
# show()


figure('Измерение ширины запрещенной зоны')
Ik1 = df['I1'] #mA
Ik2 = df['I2'] #mA
Ik = (Ik1+Ik2)/2 #mA 
Iob = df['Iобр'] #mA
Et = array(df['ЭДС']) 
Re = 10 #Ohm
a = 4 #width
d = 1.4 # thickness
l = 7  #len between 1&2

room_t = 28
k_b = 8.62 *10**(-5) ## eV/K
d_T = 5 # temp error

#Calculating
T=T+ 273.15 #to kelvin 
print(T)
weights = np.ones(T.shape)
weights[0:3] = 0

Ik = (Ik1+Ik2)/2
Rob =  Ik*Re / Iob 
ro = (a*d / l) * Rob
sigma = 1/ro
k_T = 1000/T
ln_sigma = log(sigma)

eps_lns = np.ones(T.shape) * 0.02
d_lns = eps_lns * ln_sigma


n = (ln_sigma[0]-ln_sigma[2])/(log(T[0]/T[2]))
print('n = ',n)

# approx
pp = np.polyfit(k_T,log(sigma),1, w = weights)
print('tan(theta) = ',pp[0])
print('ln(sigma)(0) = ',pp[1])
Wg = -pp[0]*2*k_b*1000
print('Wg = ', Wg,' эВ')
pf = np.poly1d(pp)


# plot(10**3/T[weights>0],log(sigma[weights>0]),'o')
plot(10**3/T,log(sigma),'o',color='crimson')
xlabel(r'$\frac{10^3}{T}, \frac{10^3}{K}$',fontsize=16)
ylabel(r'$\ln{\sigma}, a.u.$ ',fontsize=16)
grid(which='major', linestyle='-')
grid(which='minor', linestyle=':')
minorticks_on()
savefig(path.abspath('..'+'\\fig\\lns.pdf'))
show()

x=10**3/T[weights>0]
x=linspace(x[0],x[-1],100)
plot(x,pf(x),label='интерполяция',color='darkblue')
plot(10**3/T[weights>0],log(sigma[weights>0]),'o',label='эксперимент',color='crimson')
xlabel(r'$\frac{10^3}{T}, \frac{10^3}{K}$',fontsize=16)
ylabel(r'$\ln{\sigma}, a.u.$ ',fontsize=16)
grid(which='major', linestyle='-')
grid(which='minor', linestyle=':')
minorticks_on()
legend()
savefig(path.abspath('..'+'\\fig\\lns1.pdf'))
show()