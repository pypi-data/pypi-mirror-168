#packages environment
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import pandas.testing as tm
import math
from sklearn.linear_model import LogisticRegression
from scipy.stats import truncnorm
from typing import Optional


## 

#Gym environment - continuous

class DocEnv(gym.Env):
  def __init__(self):
    self.size = 2000         
   
    #set ACTION SPACE
    #set range for action space
    self.high_th = np.array([2, 2, 2])
    self.action_space = spaces.Box(
            low = np.float32(-self.high_th),
            high = np.float32(self.high_th))
    
    #set OBSERVATION SPACE
    #it is made of values for f with shape (size, )
    self.observation_space = spaces.Box(low=0, high=1, shape=(self.size,), dtype=np.float32)
        
    self.state=None 
 
  def intervention(self, Xa, rho, rho_bar=0.25, l = 0.8):
    # Xa is Xa_e(0))
    # rho is rho_e-1(Xs_e(0), Xa_e(0))

    g1 = ((Xa) + 0.5*(Xa+np.sqrt(1+(Xa)**2)))*(1-rho) + ((Xa) - 0.5*(Xa+np.sqrt(1+(Xa)**2)))*rho
    g2 = ((Xa) + 0.5*(Xa+np.sqrt(1+(Xa)**2)))*(1-rho**2) + ((Xa) - 0.5*(Xa+np.sqrt(1+(Xa)**2)))*(rho**2)
    g3 = 0.5*((3-2*rho)*Xa+(1-2*rho)*(np.sqrt(1+(Xa)**2)))
    g4 = (1-(rho_bar**l))*g2 + (rho_bar**l)*Xa
    noise = np.random.normal(0, 1, 1)
    return g1 + noise

  def set_outcome(self, data, rho, Xa_post): # data is pat_e1
    df = pd.DataFrame(data={'Xs': data[:, 1], 'Xa': data[:, 2]})
    df = df.assign(rho = rho, Xa_post = Xa_post)
    df = (df.assign(risk= lambda x: pd.cut(df['rho'], 
                                                bins=[0, 0.25, 0.5, 1],
                                                labels=["L", "M", "H"])))
                                                
    quartile_post_90 = np.percentile(df.Xa_post + df.Xs, 90)
    Y_array = np.zeros(self.size)
        
    for i in range(len(Y_array)):
        if (df.Xa_post[i] + df.Xs[i])  > quartile_post_90 - np.random.normal(0, 0.5, 1):
            Y_array[i] = 1
        elif df.risk[i] == "H":
            Y_array[i] = 1
        elif df.risk[i] == "M" and ((df.Xa_post[i] - df.Xa[i] < np.mean(df.Xa_post[i] - df.Xa[i]) + np.random.normal(0, 0.5, 1))):
            Y_array[i] = 1
        else: Y_array[i] = Y_array[i]  
    
    return Y_array

#take an action with the environment
  def step(self, action, rho_0):
    
    done = False    
    #-----------------------------------------------------------------------------------
    '''e=e, t=0
    observe new patients (Xs_e(0), Xa_e(0))'''
    pat_e0= np.hstack([np.ones((self.size, 1)), np.random.normal(10, 1, size=(self.size,2))]) #shape (size, 3), (1, Xs, Xa)

    '''compute rho_0(Xs_e(0), Xa_e(0)) - we're using covariates at e and thetas at e-1
    well thetas are actually actions'''
    rho_0bar = np.mean(rho_0)
    # decide an intervention, use rho_0, Xa_1(0)
    g_e = self.intervention(pat_e0[:, 2], rho_0, rho_0bar)
    
    #-----------------------------------------------------------------------------------
    '''e=1, t=1
    update Xa_1(0) to Xa_1(1) with intervention'''
    Xa_post = g_e # size
    # predict f_1 = E[Y_1|X_1(1)] 
    f_e = 1/(1+ np.exp(-pat_e0[:, 1]-Xa_post))
    
    # observe Y_1(1)

    Y_1 = self.set_outcome(pat_e1, rho_0, Xa_post) 
    pat_e1 = np.hstack([Y_1, np.reshape(pat_e0[:, 1], (self.size, 1)), np.reshape(Xa_post, (self.size, 1))]) #shape (size, 3), (Y, Xs, Xa)                
    
    
    ''' decide on \rho_e. we'll use actions produced by NN when feeding the input values (self.patients) returned by this function   
    '''
    rho_1 = (1/(1+np.exp(-(np.matmul(pat_e1, action)))))          
    #-----------------------------------------------------------------------------------
    '''no actions, uses variables without intervention. use pat_e0, Y_e
    Y_1 not good'''
    pat_noA =  np.hstack([Y_1, pat_e0[:, 1:3]])  
    model_noA = LogisticRegression().fit(pat_noA[:, 1:3], np.ravel(pat_noA[:, 0].astype(int)))                        
    coef_noA = np.array([model_noA.intercept_[0], model_noA.coef_[0,0] , model_noA.coef_[0,1]]) #thetas_n[0]: intercept; thetas_n[1]: coef for Xs, thetas_n[2] coef for Xa
    rho_noA = (1/(1+np.exp(-(np.matmul(pat_e0, coef_noA[:, None])))))  #prob of Y=1 # (sizex3) x (3x1) = (size, 1)  
    f_noA = 1/(1+ np.exp(-pat_e0[:, 1]-pat_e0[:, 2]))
                            
    #-----------------------------------------------------------------------------------                        
    '''
    log reg to get rho without actions but using coefficients from log reg

    '''
    model_LogReg = LogisticRegression().fit(pat_e1[:, 1:3], np.ravel(pat_e1[:, 0].astype(int)))      
    coef_LogReg = np.array([model_LogReg.intercept_[0], model_LogReg.coef_[0,0] , model_LogReg.coef_[0,1]])  
    rho_LogReg = (1/(1+np.exp(-(np.matmul(pat_e1, coef_LogReg[:, None]))))) 
    
    '''we return:
    - f_1 = E[Y_1|X_1(1)]                      
    - rho_naive, that is E[Y_1|X_1(0)] '''                                              
    
    self.patients = pat_e1[:, 1:3] # intervened df
    #model performance should worsen, hence risk increase. we can stop when increase in risk exceeds 0.3
    ## add a count, so that to see a fix (e.g. 20) a number of transitions in the traj  

    if np.mean(rho_1) >= 0.4:
      done = True
    else:
      done = False 
    


    info = {"patients": self.patients, "patients_noA": pat_noA[:, 1:3], "rho_noA": rho_noA, "f_noA": f_noA, "rho_LogReg": rho_LogReg }     
    return f_e, rho_1, done, info
    
    
#reset state and horizon    
  def reset(self, seed = None, return_info: bool = False, options: Optional[dict] = None,):  

    # not used but seems to be required by gym.core
    self.seed = seed
    self.return_info = return_info
    self.options = options     

    ''' e=0, t=0
    observe self.patients (from reset function, self.patients) (Xs(0), Xa(0))'''
    pat_e0= np.hstack([np.ones((self.size, 1)), np.random.normal(10, 1, size=(self.size,2))]) #shape (size, 3), (1, Xs, Xa)               
    
    #-----------------------------------------------------------------------------------
    '''e=0, t=1    
    observe same patients (Xs(1), Xa(1))=(Xs(0), Xa(0))
    predict f_0 = E[Y_0|X_0]'''                      
    f_0 = 1/(1+ np.exp(-self.patients[:, 0]-self.patients[:, 1]))                      

    '''observe Y(1) '''   
    Y_0 = np.random.binomial(1, 0.2, (self.size, 1))
    pat_01 = np.hstack([Y_0, self.patients]) # Y, Xs, Xa
    
    '''decide on \rho_0, which will be retained to the next epoch '''   
    rho_0 = np.repeat(0.3, self.size) #prob of Y=1. # (sizex3) x (3x1) = (size, 1)



    # f_0 and rho_0 are the same at e=0 
    # info = {"f": f_0, "rho": rho_0, "theta": thetas_0}
    return f_0, rho_0
    
    #info, self.seed, self.return_info, self.options                                                      
    
