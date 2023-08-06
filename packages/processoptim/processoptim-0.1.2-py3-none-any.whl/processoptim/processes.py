# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 23:12:25 2022

@author: HEDI
"""

import CoolProp.CoolProp as CP
from numpy import zeros, array, ones, pi,concatenate,cumsum
from prettytable import PrettyTable
from .thermo_properties import water,tomato_paste
import json
import os
from scipy.optimize import fsolve
from numpy import pi
from .__disp__ import _set_color, _set_decimals
from .__colors__ import __colors__
from tabulate import tabulate

class _schema_obj:
    def __init__(self, dict_):
            self.__dict__.update(dict_)
_schema = json.loads(json.dumps(json.loads(open (os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "process_schema.json"), "r").read()),), object_hook=_schema_obj,)

class __processclass__():
    def __init__(self):
        # set default attributes of the process
        for k,v in self.schema.design_variables.__dict__.items():
            setattr(self,k,v.default)
        for k,v in self.schema.process_specifications.__dict__.items():
            setattr(self,k,v.default)
    @property
    def type(self):
        return type(self).__name__
    @property
    def schema(self):
        return getattr(_schema,self.type)
    def __repr__(self):
        str_=_set_color(self.type,__colors__.bcyan)
        str_+="\n"
        for field in ["process_specifications", "design_variables"]:
            str_+=_set_color(field,__colors__.byellow)
            str_+="\n"
            data=[]
            for k,v in getattr(self.schema,field).__dict__.items():
                data.append([v.label,getattr(self,k),v.unit])
            str_+=tabulate(data,numalign="left", stralign="left",headers=["Property","Value","Unit"])
            str_+="\n"
        
        return str_
    
        # set result schema
class __falling_film_evaporator_res__:
    def __init__(self,schema):
        for k,v in schema.__dict__.items():
            setattr(self,k,v.default)
    
class falling_film_evaporator(__processclass__):
    def __init__(self, **args):
        self.auto_calcul=False
        super().__init__()
        # update n_effects
        if "n_effects" in args.keys():
            self.n_effects = args["n_effects"]
            del args["n_effects"]
        # update args
        for k,v in args.items():
            if k in self.schema.design_variables.__dict__.keys() or k in self.schema.process_specifications.__dict__.keys():
                setattr(self,k,v)
        setattr(self,"res",__falling_film_evaporator_res__(self.schema.res))
            
        self.calcul()
        self.auto_calcul=True

       

        
        
        
        
    def calcul(self):
        for k,v in self.schema.res.__dict__.items():
            if isinstance(v.default,list):
                setattr(self.res,k,zeros(self.n_effects+v.len))
        self.res.x[0]=self.feed_concentration
        self.res.x[-1]=self.target_concentration
        self.res.L[0]=self.feed_flowrate
        self.res.T[0]=self.steam_temperature
        self.res.dm = self.res.L[0]*self.res.x[0] # dry matter
        if self.res.x[-1] != 0:
            self.res.L[-1] = self.res.dm/self.res.x[-1]
        self.res.mevap = self.res.L[0]-self.res.L[-1] #evaporation rate
        self.res.V[0:] = self.res.mevap/self.n_effects
        for j in range(1, self.n_effects):
            self.res.L[j] = self.res.L[j-1]-self.res.V[j]
            self.res.x[j] = self.res.dm/self.res.L[j]
            
        
            
        self.res.p[0]=water.pv_T(self.res.T[0])/1e5
        for i in range(self.n_effects):
            self.res.rho_L[i]=tomato_paste.rho(self.res.x[i])
            S_liq=pi*pow(self.tube_diameter[i],2)/4
            e_film = .5
            S_liq-=pi*pow(self.tube_diameter[i]-2*e_film*1e-3,2)/4
            #S_liq=.5*pi*pow(self.tube_diameter[i],2)/4
            self.res.u[i] = self.res.L[i]/S_liq/self.res.rho_L[i]/self.n_tubes[i]
            self.res.A[i]=pi*self.n_tubes[i]*self.tube_diameter[i]*self.tube_length[i]
            self.res.T[i+1]=self.solve_T(i)
            self.res.bep[i]=tomato_paste.BPE(T=self.res.T[i+1],x=self.res.x[i+1])
            self.liquid_flow(self.res.T[i+1],
                        self.res.T[i],
                        self.res.x[i],
                        self.tube_diameter[i],
                        self.tube_length[i],
                        self.n_tubes[i],
                        self.res.u[i],i)
            self.res.p[i+1]=water.pv_T(self.res.T[i+1])/1e5
            self.res.ts[i]=self.tube_length[i]/self.res.u[i]
            
    def solve_T(self,effect):
        Thot = self.res.T[effect]
        if effect:
            Thot-=self.res.bep[effect-1]
        Q=water.Lv_T(Thot)*self.res.V[effect]
        def err_(T):
            hg = self.liquid_flow(T[0], Thot, self.res.x[effect],
                                  self.tube_diameter[effect],
                                  self.tube_length[effect],
                                  self.n_tubes[effect],
                                  self.res.u[effect])
            return abs(Q-hg*self.res.A[effect]*(Thot-T[0]))
        opt = fsolve(err_,[Thot])
        return opt[0]
        
        
    
    def liquid_flow(self,T,Tw,x,d,L,N,u,effect=None):
          rho=tomato_paste.rho(x)
          mu=tomato_paste.mu(x,T,u,d)
          muw=tomato_paste.mu(x,Tw,u,d)
          lambda_=tomato_paste.Lambda(x, T)
          Cp=tomato_paste.Cp(x)*1000
          Re=rho*d*u/mu
          Pr=Cp*mu/lambda_
          # correction factor
          phi = mu/muw
          if Re<2100: # laminar flow
              Nu=1.86*pow(d*Re*Pr/L,1/3)*pow(phi,.14)
              f=16/Re
          else:#turbulent flow
              f=.08*pow(Re,-.25)
              Nu=.023*(1+pow(d/L,.7))*pow(Re,.8)*pow(Pr,1/3)*pow(phi,.14)    
          h=Nu*lambda_/d
          hs = 10 # steam side heat transfer coeff kW/m2/K
          hf = 10 # fouling heat transfer coeff kW/m2/K
          hw = 5  # wall heat transfer coeff kW/m2/K
          # overall heat transfer coeff
          hg=1/(1/h+1/hs+1/hw+1/hf)
          if not effect is None:
              self.res.hg[effect]=hg
              self.res.rho_L[effect]=rho
              self.res.Cp_L[effect]=Cp
              self.res.mu_L[effect]=mu
              self.res.lambda_L[effect]=lambda_
              self.res.Re_L[effect]=Re
              self.res.Pr_L[effect]=Pr
              self.res.Nu_L[effect]=Nu
              f=1
              #self.res.f_L[effect]=f
              DP = 2*f *(L/d)*rho*u**2
              #F=u*N*pi*d*d/4
              F=self.res.L[effect]/rho
              E = F*DP
              self.res.DP_L[effect]=DP/1e5
              self.res.F[effect]=F
              self.res.E[effect] = E/1000
          else:
              return hg
          
            
        
    def __setattr__(self, key, value):
        if key in ["res","auto_calcul"]:
            super(__processclass__, self).__setattr__(key, value)
        else:
            if key=="n_effects":
                if hasattr(self,"n_effects"):
                    if value!=self.n_effects:
                        super(__processclass__, self).__setattr__(key, value)
                        #update all arrays
                        for k,v in self.__dict__.items():
                            if isinstance(v,list):
                                while len(v) > self.n_effects:
                                    v.pop(-1)
                                while len(v) < self.n_effects:
                                    v.append(v[-1])
                else:
                    super(__processclass__, self).__setattr__(key, value)
            else:
                default=None
                if key in self.schema.design_variables.__dict__.keys():
                    default = getattr(self.schema.design_variables,key).default
                elif key in self.schema.process_specifications.__dict__.keys():
                    default = getattr(self.schema.process_specifications,key).default
                if default and isinstance(default,list):
                    if isinstance(value,list):
                        #adjust array
                        while len(value)>self.n_effects:
                            value.pop(-1)
                        while len(value)<self.n_effects:
                            value.append(value[-1])
                        super(__processclass__, self).__setattr__(key, value)
                    else:
                        super(__processclass__, self).__setattr__(key, [value]*self.n_effects)
                elif default:
                    super(__processclass__, self).__setattr__(key, value)
                
            if self.auto_calcul:
                self.calcul()
    def __repr__(self):
        str_ = super().__repr__()
        str_+="\n"
        str_+=_set_color("results",__colors__.byellow)
        str_+="\n"
        data=[]
        for k,v in self.schema.res.__dict__.items():
            color = __colors__.color_off
            if hasattr(v,"color"):
                color = getattr(__colors__,v.color)
            if isinstance(v.default,list):
                v_ = list(map(lambda x:float(_set_decimals(x, str(v.decimals))),getattr(self.res,k)))
            else:
                v_=_set_decimals(getattr(self.res,k), str(v.decimals))
            if isinstance(v.label,list):
                data.append([_set_color(v.label[0],color),_set_color(str(v_[0]),color),_set_color(v.unit,color)])
                data.append([_set_color(v.label[1],color),_set_color(str(v_[1:]),color),_set_color(v.unit,color)])
            else:
                data.append([_set_color(v.label,color),_set_color(str(v_),color),_set_color(v.unit,color)])
        str_+=tabulate(data,numalign="left", stralign="left",headers=["Property","Value","Unit"])
        str_+="\n"
        return str_
    @property
    def hist_T(self):
        t=0
        import matplotlib.pyplot as plt
        for i in range(self.n_effects):
            ts=[]
            T=[]
            ts.append(t)
            ts.append(t+self.res.ts[i])
            t+=self.res.ts[i]
            T.append(self.res.T[i+1])
            T.append(self.res.T[i+1])
            plt.plot(ts,T,"-s",label="effect_{}".format(i+1))
        plt.legend()
        plt.grid()
        plt.ylabel("Temperature °C")
        plt.xlabel("residence time s")
    def lycopene(self,effect=None,plt=False,y0=1,tab=False):
        if effect:
            t,y = tomato_paste.lycopene(T=self.res.T[effect+1],
                                         x=self.res.x[effect+1],
                                         ts=self.res.ts[effect],
                                         y0=y0)
        else:
            y0_=y0
            t=[]
            y=[]
            for effect in range(self.n_effects):
                t1,y1 = tomato_paste.lycopene(T=self.res.T[effect+1],
                                             x=self.res.x[effect+1],
                                             ts=self.res.ts[effect],
                                             y0=y0_)
                if len(t)>0:
                    t1=t1+t[-1]
                y0_=y1[-1]
                t=concatenate((t,t1))
                y=concatenate((y,y1))
        if plt:
            import matplotlib.pyplot as plt
            plt.plot(t,y*100)
            plt.xlabel("time s")
            plt.ylabel("lycopene %")      
        if tab:
            data=[]
            for i,t1 in enumerate(t):
                data.append([t1,_set_decimals(y[i], "2")])
            print(tabulate(data,numalign="left", stralign="left",headers=["time s","lycopene kg/kg",]))
        if not plt and not tab:
            return t,y
                
        

        