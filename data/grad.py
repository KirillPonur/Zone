from pylab import *
from matplotlib import rc
import os.path as path
import sys
from scipy import interpolate
from pandas import read_excel as read
rc('text', usetex=True)
rc('text.latex', preamble=[r'\usepackage[russian]{babel}',
                         r'\usepackage{amsmath}',
                        r'\usepackage{amssymb}',
                        r'\usepackage{mathrsfs}',
                        r'\usepackage{gensymb}'])


rc('font', family='serif')

rec = path.abspath('grad.xlsx')

df=read(rec, sheet_name='1')
figure('Градуировочный график')
x=array(df['x'])
y=array(df['y'])
g = polyfit(x,y,4)
print(g)
t=linspace(x[0],x[-1],1000)
f=poly1d(g)
plot(t,f(t),color='darkblue')

xlabel(r'$T_{\text{спая}}, ^{\circ}C$', fontsize=16)
ylabel(r'$\mathscr{E}_{\text{термо}}$, мВ',fontsize=16)
grid(which='major', linestyle='-')
grid(which='minor', linestyle=':')
minorticks_on()
savefig(path.abspath('..'+'\\img\\grad.pdf'))


show()

