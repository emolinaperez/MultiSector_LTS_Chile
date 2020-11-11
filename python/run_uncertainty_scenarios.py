'''
Centro de Energia, Facultad de Ciencias Fisicas y Matematicas, U.de Chile
Octubre 2020
Rutina para crear escenarios de incertidumbre a partir de rango maximo y minimo
'''
import os, os.path

#Parameters in the code
N=139 #number of partitions of the LHS

# Se extraen las direcciones de las distintas carpetas de la implementacion
dir_main = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dir_ref = os.path.join(dir_main,"ref")

plot_par='fuel_price_fuel oil' #name of parameter to plot
csv_to_read=os.path.join(dir_ref,"parameter_ranges_max-min.csv") #name of the input csv file with ranges for uncertainty parameters
csv_to_save=os.path.join(dir_ref,"parameter_ranges_max-min_output.csv") #name of the output csv file for the samples in the uncertainty ranges

#-----------------------o-----------------------------------------------------

from timeit import default_timer as timer
start = timer()
from random import uniform
from random import random
from random import choices
import random
import numpy as np
import matplotlib.pyplot as plt 
import math
import csv
#-----------------------o-----------------------------------------------------
#Reading input csv file with uncertainty ranges

data=[]
with open(csv_to_read) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count=line_count+1
        data.append(row)
columns=len(row)
rows=len(data)
T=columns-3
t=range(0,T)
N_par=int((rows-1)/2)
sector=[]
par=[]
years=np.zeros(T)
max_x=np.zeros((N_par,T))
min_x=np.zeros((N_par,T))
for k in range(0,N_par):
    sector.append(data[2*k+1][0])
    par.append(data[2*k+1][1])
    for i in range(0,T):
        years[i]=data[0][i+3]
        max_x[k][i]=data[2*k+1][i+3]
        min_x[k][i]=data[2*k+2][i+3]

#-----------------------o-----------------------------------------------------
#Generate the LHS sampling in the uncertainty ranges
#We assume the variables are X ~ Uniform(a,b)

P_b=np.zeros((N_par,N,T)) #max value for the intervals for each sampling
P_a=np.zeros((N_par,N,T)) #max value for the intervals for each sampling
LHS=np.zeros((N_par,N,T)) #sampling of the LHS in those ranges defined by P_a and P_b
z=np.zeros((N_par,N,T))
for h in range(0,N_par):
    for j in t:
        for i in range(0,N):
            P_a[h,i,j]=min_x[h,j]+(max_x[h,j]-min_x[h,j])/N*i
            P_b[h,i,j]=min_x[h,j]+(max_x[h,j]-min_x[h,j])/N*(i+1)
row_range=list(range(1,N+1))
column_range=list(range(1,N+1))

for h in range(0,N_par):
    w=list((row_range))
    y=list((row_range))
    for k in range(0,N):
        y[k]=random.choice(w)
#    print('y[',k,']=',y[k])
        c=int(y[k]-1)
        a=P_a[h,c,t]
        b=P_b[h,c,t]
        LHS[h,k,t]=uniform(a,b)
        w.remove(y[k])
        #for j in t:
            #z[h,k,j]=(LHS[h,k,j]-P_a[h,c,j])/(P_b[h,c,j]-P_a[h,c,j])


#-----------------------o-----------------------------------------------------
#Generate plot for parameter "plot_var" defined at the top of the code.
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 8
fig_size[1] = 4
plt.rcParams["figure.figsize"] = fig_size
            
for i in range(0, N):
   plt.plot(years[t],LHS[par.index(plot_par),i,t],label='Sample '+str(i+1))
   plt.plot(years[t],P_a[par.index(plot_par),i,t],'k--',linewidth=0.5)#label='Banda inf'+str(i+1))
   plt.plot(years[t],P_b[par.index(plot_par),i,t],'k--',linewidth=0.5)#label='Banda sup'+str(i+1))

if N<=30:
    plt.legend(loc="right")
   
plt.title('Random sampling with LHS for '+str(T)+' variables and '+str(N)+' intervals per variable')
plt.ylabel('Values for the variables')
plt.xlabel('year')
plt.grid()
plt.xticks(np.arange(years[0],years[len(years)-1],step=1))

#ax = plt.subplot(111)
#ax.legend(bbox_to_anchor=(1, 1))
#-----------------------o-----------------------------------------------------
#Generate output csv file
A=np.zeros((N*T,N_par))
for i in range(0,N):
    for j in range(0,T):
        for h in range(0,N_par):
            A[j+T*i,h]=LHS[h,i,j]

B=[]
C=np.zeros((N*T,2))
C_0=[]
C_0.append('master_id')
C_0.append('year')
for h in range(0,N_par):
    C_0.append(par[h])

for i in range(0,N):
    for j in range(0,T):
        C[T*i+j,0]=int(i)
        C[T*i+j,1]=int(years[j])
 
output = open(csv_to_save, 'w',newline='')
writer = csv.writer(output)
writer.writerow(C_0)
for u in range(0,N*T):
    B.append(C[u,0])
    B.append(C[u,1])
    for h in range(0,N_par):

        B.append(A[u,h])
    writer.writerow(B)
    B=[]
output.close()
#---

end = timer()
a=math.trunc((end-start)/60)
print('La ejecución tardó',a,'minutos para T=',T,'y N=',N)
