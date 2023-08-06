import numpy as np
import math
import pandas as pd
from sklearn.linear_model import LogisticRegression
from scipy.stats import truncnorm
import matplotlib.pyplot as plt

def intervention(Xa, rho, rho_bar=0.2, l = 0.8):
    # Xa is Xa_e(0))
    # rho is rho_e-1(Xs_e(0), Xa_e(0))

    g1 = (((Xa-10) + 0.5*(Xa-10+np.sqrt(1+(Xa-10)**2)))*(1-rho) + ((Xa-10) - 0.5*(Xa-10+np.sqrt(1+(Xa-10)**2)))*rho)
    g2 = ((Xa) + 0.5*(Xa+np.sqrt(1+(Xa)**2)))*(1-rho**2) + ((Xa) - 0.5*(Xa+np.sqrt(1+(Xa)**2)))*(rho**2)
    g3 = 0.5*((3-2*rho)*Xa+(1-2*rho)*(np.sqrt(1+(Xa)**2)))
    g4 = (1-(rho_bar**l))*g2 + (rho_bar**l)*Xa
    noise = np.random.normal(0, 1, 1)
    return g1+10 + noise

size = 100

# epoch 0

rho_0 = 0.3
action0 = 0

# epoch 1
pat_e1= np.hstack([np.ones((size, 1)), np.random.normal(10, 1, size=(size,2))]) # 1, Xs, Xa
Xa_pre = pat_e1[:, 2]           
Xa_post = intervention(Xa_pre, rho_0)
f_e = 1/(1+ np.exp(pat_e1[:, 0]-pat_e1[:, 1]-Xa_post))

print("Xa", Xa_pre)
print("Xa post", Xa_post)
print("fe", f_e)
#Y_1 = np.random.binomial(1, 0.2, (size, 1)) # 
#pat_e1 = np.hstack([Y_1, np.reshape(pat_e0[:, 1], (size, 1)), np.reshape(Xa, (size, 1))])
#df = 





df = pd.DataFrame(data={'Xs': pat_e1[:, 1], 'Xa': pat_e1[:, 2]})
df = df.assign(rho = rho_0, Xa_post = Xa_post)
df = (df.assign(risk= lambda x: pd.cut(df['rho'], 
                                              bins=[0, 0.25, 0.5, 1],
                                              labels=["L", "M", "H"])))
                                            
quartile_post_90 = np.percentile(df.Xa_post + df.Xs, 90)
print("quartile_post_90", quartile_post_90)
quartile_pre = np.percentile(df.Xa + df.Xs, [10, 50, 90])


print("quartile", quartile_pre)
Y_array = np.zeros(size)
print("Y_array", Y_array)
def set_outcome(Y, df):
    
    for i in range(len(Y_array)):
        if (df.Xa_post[i] + df.Xs[i]) > quartile_post_90:
            Y[i] = 1
        elif df.risk[i] == "H":
            Y[i] = 1

        else: Y[i] = Y[i]
    return Y    
Y_array1 = set_outcome(Y_array, df)
df = df.assign(Y = set_outcome(Y_array, df))
print("df", df)  


def outcome(data, rho, Xa_post): # data is pat_e1
    df = pd.DataFrame(data={'Xs': data[:, 1], 'Xa': data[:, 2]})
    df = df.assign(rho = rho, Xa_post = Xa_post)
    df = (df.assign(risk= lambda x: pd.cut(df['rho'], 
                                                bins=[0, 0.25, 0.5, 1],
                                                labels=["L", "M", "H"])))
                                                
    quartile_post_90 = np.percentile(df.Xa_post + df.Xs, 90)
    Y_array = np.zeros(size)
        
    for i in range(len(Y_array)):
        if (df.Xa_post[i] + df.Xs[i])  > quartile_post_90 - np.random.normal(0, 0.5, 1):
            Y_array[i] = 1
        elif df.risk[i] == "H":
            Y_array[i] = 1
        elif df.risk[i] == "M" and ((df.Xa_post[i] - df.Xa[i] < np.mean(df.Xa_post[i] - df.Xa[i]) + np.random.normal(0, 0.5, 1))):
            Y_array[i] = 1
        else: Y_array[i] = Y_array[i]  
    
    return Y_array

print(outcome(pat_e1, rho_0, Xa_post))


'''
plots
'''
rho_ = [0, 0.25, 0.5, 0.75, 1]
dataset_normal= np.hstack([np.ones((size, 1)), np.random.normal(10, 1, size=(size,2))]) #shape (size, 3), (1, Xs, Xa)


pre = np.sort(dataset_normal[:, 2])
g_e = intervention(pre, rho_[3])  

plt.plot(pre, intervention(pre, rho_[0]), label = "0")
plt.plot(pre, intervention(pre, rho_[1]), label = "0.25")
plt.plot(pre, intervention(pre, rho_[2]), label = "0.5")
plt.plot(pre, intervention(pre, rho_[3]), label = "0.75")
plt.plot(pre, intervention(pre, rho_[4]), label = "1")
plt.xlabel('Xa pre-intervention')
plt.ylabel('Xa post-intervention')

plt.legend(title = "rho")
plt.show()