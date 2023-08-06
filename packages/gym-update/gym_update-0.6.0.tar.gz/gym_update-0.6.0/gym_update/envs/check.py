import numpy as np
import math
from sklearn.linear_model import LogisticRegression
from scipy.stats import truncnorm

size = 2000
patients = truncnorm.rvs(a=0, b= math.inf, loc = 4, scale = 1, size=(size,2)) #shape (size, 2), 1st columns is Xs, second is Xa 
Xa = patients[:, 1]  
print(np.quantile(Xa, (0.25, 0.5, 0.75)) , "min" ,  np.min(Xa), "max", np.max(Xa), np.mean(Xa), np.std(Xa))                
rho = [0, 0.25, 0.5, 0.75, 1]
#g = ((Xa) + 0.5*(Xa+np.sqrt(1+(Xa)**2)))*(1-rho) + ((Xa) - 0.5*(Xa+np.sqrt(1+(Xa)**2)))*rho
