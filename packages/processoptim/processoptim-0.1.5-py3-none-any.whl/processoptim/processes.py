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
def __load_shema():
    return json.loads(json.dumps(json.loads(open (os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 "process_schema.json"), "r").read()),), object_hook=_schema_obj,)
_schema = __load_shema()




def update(process_schema):
    obj = json.loads(open (os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "process_schema.json"), "r").read())
    def check_obj(obj_val):
        for k in ["var","res"]:
            if not k in obj_val.keys():
                obj_val[k]={}

        for k1,v1 in {"unit":"","label":"","decimals":4,"default":0}.items():
            for k in ["var","res"]:
                for k2,v2 in obj_val[k].items():
                    if not k1 in v2.keys():
                        obj_val[k][k2][k1]=v1
        return obj_val

    for k,v in process_schema.items():
            print(k)
            obj[k]=check_obj(v)

    with open (os.path.join(os.path.dirname(os.path.abspath(__file__)),
               "process_schema.json"), "w") as f:
        json.dump(obj, f)  
    import importlib
    import sys
    importlib.reload(sys.modules[__name__])



class __processclass__():
    def __init__(self,**args):
        self.auto_calcul=False
        # set default attributes of the process
        for k,v in self.schema.var.__dict__.items():
            setattr(self,k,v.default)
        setattr(self,"res",__resclass__(self.schema.res))
        # update args
        for k,v in args.items():
            if k in self.schema.var.__dict__.keys():
                setattr(self,k,v)

    @property
    def type(self):
        return type(self).__name__
    @property
    def schema(self):
        return getattr(_schema,self.type)
    def __repr__(self):
        str_=_set_color(self.type,__colors__.bcyan)
        str_+="\n"
        str_+=_set_color("process specifications",__colors__.byellow)
        str_+="\n"
        data=[]
        for k,v in self.schema.var.__dict__.items():
            data.append([v.label,getattr(self,k),v.unit])
        str_+=tabulate(data,numalign="left", stralign="left",headers=["Property","Value","Unit"])
        str_+="\n"
        str_+=self.res.__repr__()
        return str_
    def calcul(self):
        pass
    def __setattr__(self, key, value):
        super(__processclass__, self).__setattr__(key, value)
        if self.auto_calcul:
            self.calcul()
    
        # set result schema
class __resclass__:
    def __init__(self,schema):
        self.schema=schema
        for k,v in schema.__dict__.items():
            setattr(self,k,v.default)
    def __repr__(self):
        str_=_set_color("results",__colors__.byellow)
        str_+="\n"
        data=[]
        for k,v in self.schema.__dict__.items():
            color = __colors__.color_off
            if hasattr(v,"color"):
                color = getattr(__colors__,v.color)
            if isinstance(v.default,list):
                v_ = list(map(lambda x:float(_set_decimals(x, str(v.decimals))),getattr(self,k)))
            else:
                v_=_set_decimals(getattr(self,k), str(v.decimals))
            if isinstance(v.label,list):
                d=[]
                for i,v_1 in enumerate(v_):
                    if i<len(v.label)-1:
                        data.append([_set_color(v.label[i],color),_set_color(str(v_1),color),_set_color(v.unit,color)])
                    else:
                        d.append(v_1)
                if d:
                    data.append([_set_color(v.label[-1],color),_set_color(str(d),color),_set_color(v.unit,color)])
            else:
                data.append([_set_color(v.label,color),_set_color(str(v_),color),_set_color(v.unit,color)])
        str_+=tabulate(data,numalign="left", stralign="left",headers=["Property","Value","Unit"])
        return str_
    
class falling_film_evaporator(__processclass__):
    def __init__(self, **args):
        super().__init__()
        # update n_effects
        if "n_effects" in args.keys():
            self.n_effects = args["n_effects"]
            del args["n_effects"]
        # update args
        for k,v in args.items():
            if k in self.schema.var.__dict__.keys():
                setattr(self,k,v)
        self.calcul()
        self.auto_calcul=True     
        
    def calcul(self):
        for k,v in self.schema.res.__dict__.items():
            if isinstance(v.default,list):
                setattr(self.res,k,zeros(eval(v.len)))
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
                auto_calcul = self.auto_calcul
                self.auto_calcul=False
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
                    if key in self.schema.var.__dict__.keys():
                        default = getattr(self.schema.var,key).default
    
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
                self.auto_calcul=auto_calcul
                if auto_calcul:
                    self.calcul()
                
    def __repr__(self):
        str_ = super().__repr__()
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
                
class shell_tube_heat_exchanger(__processclass__):
    def __init__(self,**args):
        super().__init__(**args)
        self.auto_calcul=True
        self.calcul()
    def calcul(self):
        x = self.feed_concentration
        T = [self.feed_temperature, self.target_temperature]
        d = self.tube_diameter
        L = self.tube_length
        m = self.feed_flowrate
        N = self.n_tubes
        n = self.n_passes
        rho = tomato_paste.rho(x)
        u = n*m/rho/N*4/pi/d/d
        DP=n*(4*L/d+2.5)*rho*u*u/2
        E = DP*m/rho
        H=[tomato_paste.H(x, T[0]),tomato_paste.H(x, T[1])]
        Q=m*(H[1]-H[0])
        ts = n*L/u
        self.res.u = u
        self.res.DP=DP/1e5
        self.res.E=E/1000
        self.res.Q = Q
        self.res.ts = ts
    def lycopene(self,plt=False,y0=1,tab=False):
        from numpy import polyfit,polyval
        T = [self.feed_temperature, self.target_temperature]
        t = [0, self.res.ts]
        p = polyfit(t, T, 1)
        def T_func(t):
            return polyval(p,t)
        
        t,y = tomato_paste.lycopene(T=T_func,
                                     x= self.feed_concentration,
                                     ts=self.res.ts,
                                     y0=y0)
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
        
        
        
            
        
        
    
        

        