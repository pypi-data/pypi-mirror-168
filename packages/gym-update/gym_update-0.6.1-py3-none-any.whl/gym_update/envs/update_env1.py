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

'''
modified version. here we want to see:
- modified g function--> g_ = (1-\bar(rho)^l)g() + \bar(rho)^l Xa
- l exponent in 0,1
- \bar(rho) overall risk (hence not just individual risk for the intervention)
- 
'''

## 

#Gym environment - continuous

class UpdateEnv(gym.Env):
  def __init__(self):
    self.size = 2000     

    #set range for action space
    self.high_th = np.array([2, 2, 2])
   
    #set ACTION SPACE
    self.action_space = spaces.Box(
            low = np.float32(-self.high_th),
            high = np.float32(self.high_th))
    
    #set range for obs space    
    self.min_Xas=np.array([0, 0])
    self.max_Xas=np.array([math.inf, math.inf])
    
    #set OBSERVATION SPACE
    #it is made of values for f with shape (size, )
    self.observation_space = spaces.Box(low=0, high=1, shape=(self.size,), dtype=np.float32)
    #self.observation_space = spaces.Box(low=np.float32(self.min_Xas), high=np.float32(self.max_Xas))
        
    #set an initial state
    self.state=None 
    # self.seed()
    
    #self.init_actions = [0.1, 0.1, 0.1] 
 
  def intervention(self, Xa, rho):
    # Xa is Xa_e(0))
    # rho is rho_e-1(Xs_e(0), Xa_e(0))
    g = ((Xa) + 0.5*(Xa+np.sqrt(1+(Xa)**2)))*(1-rho) + ((Xa) - 0.5*(Xa+np.sqrt(1+(Xa)**2)))*rho
    return g
    
#take an action with the environment
  def step(self, action):
    
    done = False    
    #-----------------------------------------------------------------------------------
    # e=e, t=0
    # observe new patients (Xs_e(0), Xa_e(0))
    pat_e0= np.hstack([np.ones((self.size, 1)), truncnorm.rvs(a=0, b= math.inf,size=(self.size,2))]) #shape (size, 3), (1, Xs, Xa)
    
    # compute rho_0(Xs_e(0), Xa_e(0)) - we're using covariates at e and thetas at e-1
    # well thetas are actually actions
    rho_0 = (1/(1+np.exp(-(np.matmul(pat_e0, action))))) #prob of Y=1. # (sizex3) x (3x1) = (size, 1)
    
    # decide an intervention, use rho_0, Xa_1(0)
    g_e = self.intervention(pat_e0[:, 2], rho_0)
    
    #-----------------------------------------------------------------------------------
    # e=1, t=1
    #update Xa_1(0) to Xa_1(1) with intervention
    Xa = g_e # size
    # predict f_1 = E[Y_1|X_1(1)] 
    f_e = 1/(1+ np.exp(-pat_e0[:, 1]-Xa))
    
    # observe Y_1(1)
    # this doesn't make sense (it doesn't depend on X) and is not needed
    Y_1 = np.random.binomial(1, 0.2, (self.size, 1)) # 
    pat_e1 = np.hstack([Y_1, np.reshape(pat_e0[:, 1], (self.size, 1)), np.reshape(Xa, (self.size, 1))]) #shape (size, 3), (Y, Xs, Xa)                
    
    
    # decide on \rho_e. we'll use actions produced by NN when feeding the input values (self.patients) returned by this function             
    #-----------------------------------------------------------------------------------
    # no actions, uses variables without intervention. use pat_e0, Y_e
    # Y_1 not good
    pat_noA =  np.hstack([Y_1, pat_e0[:, 1:3]])  
    model_noA = LogisticRegression().fit(pat_noA[:, 1:3], np.ravel(pat_noA[:, 0].astype(int)))                        
    thetas_noA = np.array([model_noA.intercept_[0], model_noA.coef_[0,0] , model_noA.coef_[0,1]]) #thetas_n[0]: intercept; thetas_n[1]: coef for Xs, thetas_n[2] coef for Xa
    rho_noA = (1/(1+np.exp(-(np.matmul(pat_e0, thetas_noA[:, None])))))  #prob of Y=1 # (sizex3) x (3x1) = (size, 1)  
    f_noA = 1/(1+ np.exp(-pat_e0[:, 1]-pat_e0[:, 2]))
                            
    #-----------------------------------------------------------------------------------                        
    # we return:
    # - f_1 = E[Y_1|X_1(1)]                      
    # - rho_naive, that is E[Y_1|X_1(0)]                                               
    
    self.patients = pat_e1[:, 1:3]
    #model performance should worsen, hence risk increase. we can stop when increase in risk exceeds 0.3
    ## add a count, so that to see a fix (e.g. 20) a number of transitions in the traj  

    if np.mean(rho_0) >= 0.3:
      done = True
    else:
      done = False 
     
    info = {"patients": self.patients, "patients_noA": pat_noA[:, 1:3], "rew_noA": rho_noA, "risk_noA": f_noA}     
    return f_e, rho_0, done, info
    
    
#reset state and horizon    
  def reset(self, seed = None, return_info: bool = False, options: Optional[dict] = None,):  

    # not used but seems to be required by gym.core
    self.seed = seed
    self.return_info = return_info
    self.options = options     

    # e=0, t=0
    # observe self.patients (from reset function, self.patients) (Xs(0), Xa(0))
    self.patients = truncnorm.rvs(a=0, b= math.inf,size=(self.size,2)) #shape (size, 2), 1st columns is Xs, second is Xa                        
    
    #-----------------------------------------------------------------------------------
    #e=0, t=1    
    # observe same patients (Xs(1), Xa(1))=(Xs(0), Xa(0))
    # predict f_0 = E[Y_0|X_0]                      
    f_0 = 1/(1+ np.exp(-self.patients[:, 0]-self.patients[:, 1]))                      

    # observe Y(1)    
    Y_0 = np.random.binomial(1, 0.2, (self.size, 1))
    pat_01 = np.hstack([Y_0, self.patients]) # Y, Xs, Xa
    
    # decide on \rho_0, which will be retained to the next epoch
    model_rho = LogisticRegression().fit(pat_01[:, 1:3], np.ravel(pat_01[:, 0].astype(int)))                        
    thetas_0 = np.array([model_rho.intercept_[0], model_rho.coef_[0,0] , model_rho.coef_[0,1]]) #thetas_n[0]: intercept; thetas_n[1]: coef for Xs, thetas_n[2] coef for Xa
    patients_model = np.hstack([np.ones((self.size, 1)), self.patients])
    rho_0 = (1/(1+np.exp(-(np.matmul(patients_model, thetas_0[:, None])))))  #prob of Y=1 # (sizex3) x (3x1) = (size, 1)  
      
    
    # i don't really think there's need for initial actions any longer
    # f_0 and rho_0 are the same at e=0 
    # info = {"f": f_0, "rho": rho_0, "theta": thetas_0}
    return f_0, rho_0, thetas_0
    
    #info, self.seed, self.return_info, self.options                                                      
    
