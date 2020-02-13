import sac as s
import time
import numpy as np
import matplotlib.pyplot as plt
from config import Config as cf

#time
start_time = time.time()
#number of comparisons
n = 10

prw_fun_list = []
lf_fun_list = []
prw_last_iter_list = []
lf_last_iter_list = []
true_global = 0

for i in range(0,n):
    results = s.sac()
    prs_fun = results['pure_random_search'].fun
    lf_fun = results['levy_flight'].fun
    prw_fun_list.append(prs_fun)
    lf_fun_list.append(lf_fun)
    
    prw_last_iter = results['pure_random_search'].iter_to_best[-2]
    lf_last_iter = results['levy_flight'].iter_to_best[-2]
    prw_last_iter_list.append(prw_last_iter)
    lf_last_iter_list.append(lf_last_iter)

def iqr(values_list):
    values_list = np.sort(values_list)
    smaller_half = values_list[:int(np.floor(len(values_list)/2))]
    higher_half  = values_list[int(np.ceil(len(values_list)/2)):]
    # first quartile
    q1 = np.mean(smaller_half)
    #third quartile
    q3 = np.mean(higher_half)
    return q3-q1

def mad(value_list,axis=None):
    return np.mean(np.abs(value_list - np.mean(value_list, axis)), axis)

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

fig1, ax1 = plt.subplots()
ax1.set_title('fun')
all_t=[prw_fun_list,lf_fun_list]
ax1.boxplot(all_t)
#plt.savefig('IQR_fun',dpi=600)
plt.show()

fig2, ax2 = plt.subplots()
ax2.set_title('iter')
all_t1=[prw_last_iter_list,lf_last_iter_list]
ax2.boxplot(all_t1)
#plt.savefig('IQR_iter',dpi=600)
plt.show()
       
print('number of iterations: ',n)
print('true global fun: ',cf.get_global_min())

print('Pure Random Search:')   
print('  mean fun                 : ',truncate(np.mean(prw_fun_list),4))
print('  mean best iter           : ',truncate(np.mean(prw_last_iter_list),4))
print('  Statistic range W_fun    : ',truncate(max(prw_fun_list)-min(prw_fun_list),4))
print('  Statistic range W_iter   : ',truncate(max(prw_last_iter_list)-min(prw_last_iter_list),4))
print('  IQR fun                  : ',truncate(iqr(prw_fun_list),4))
print('  IQR best iter            : ',truncate(iqr(prw_last_iter_list),4))
print('  avg abs deviation fun    : ',truncate(mad(prw_fun_list),4))
print('  avg abs deviation iter   : ',truncate(mad(prw_last_iter_list),4))

print('Levy-Flight:') 
print('  mean fun                 : ',truncate(np.mean(lf_fun_list),4))
print('  mean best iter           : ',truncate(np.mean(lf_last_iter_list),4))
print('  Statistic range W_fun    : ',truncate(max(lf_fun_list)-min(lf_fun_list),4))
print('  Statistic range W_iter   : ',truncate(max(lf_last_iter_list)-min(lf_last_iter_list),4))
print('  IQR fun                  : ',truncate(iqr(lf_fun_list),4))
print('  IQR best iter            : ',truncate(iqr(lf_last_iter_list),4))
print('  avg abs deviation fun    : ',truncate(mad(lf_fun_list),4))
print('  avg abs deviation iter   : ',truncate(mad(lf_last_iter_list),4))

print("--- %s seconds ---" % truncate((time.time() - start_time),4))  
print('--- mean %s seconds ---' % truncate((time.time() - start_time)/n,4))
    