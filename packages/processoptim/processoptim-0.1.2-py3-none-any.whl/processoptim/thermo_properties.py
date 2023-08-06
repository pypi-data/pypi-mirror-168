# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 06:28:38 2022

@author: HEDI
"""

from numpy import exp
import CoolProp.CoolProp as CP
__R__ = 8.314 #J/mol/K

class __water__:
    def pv_T(self,T):
        return CP.PropsSI('P','T',T+273,'Q',1,"water")
    def rho(self,T):
        return CP.PropsSI('D','T',T+273,'Q',0,"water")
    def Cp(self,T):
        return CP.PropsSI("C",'T',T+273,'Q',0,"water")/1000
    def H(self,T):
        return CP.PropsSI("H",'T',T+273,'Q',0,"water")/1000
    def Lv_p(self,p):
        return (CP.PropsSI("H",'P',p*1e5,'Q',1,"water")-CP.PropsSI("H",'P',p*1e5,'Q',0,"water"))/1000
    def Lv_T(self,T):
        return (CP.PropsSI("H",'T',T+273.15,'Q',1,"water")-CP.PropsSI("H",'T',T+273.15,'Q',0,"water"))/1000
    def mu(self,T):
        return CP.PropsSI("V",'T',T+273,'Q',0,"water")
    def Lambda(self,T):
        return CP.PropsSI("L",'T',T+273,'Q',0,"water")
    
class __tomato_paste__:
    def rho(self,x):
        """
        Parameters
        x : mass fraction of dry matter [0-1]
        Returns
        density [kg/m3]
        """
        return 1/(x/1600+(1-x)/1000)
    def Cp(self,x):
        """
        Parameters
        x :mass fraction of dry matter [0-1]
        Returns
        specific heat [kJ/kg/K]
        """
        return x*.5 + 4.18*(1-x)
    def Lambda(self, x, T):
        """
        Parameters
        x : mass fraction of dry matter [0-1]
        T :temperature [degC]
        Returns
        thermal conductivity [W/m/K]
        """
        T+=273.15
        Es = 5*1000 # kJ/mol
        Ew = .17*1000 # kJ/mol
        Tr = 60+273.15 # K
        return x*.22*exp(-Es/__R__*(1/T-1/Tr))+(1-x)*.68*exp(-Ew/__R__*(1/T-1/Tr))
    def mu(self,x,T,u,d):
        """
        Parameters
        x : mass fraction of dry matter [0-1]
        T : temperature [degC]
        u : velocity [m/s]
        d :  characteristic length [m]
        Returns
        -Apparent viscosity [Pa.s]
        """
        T+=273.15
        k0 = 1.27
        B=.15
        E=15.8*1000
        n0=.403
        b=.0028
        T0=25+273
        k = k0*exp(B*x)*exp(E/__R__*(1/T-1/T0))
        n = n0-b*x
        #k=1.84*pow(x*100,2.54)/(100-x*100)
        return k*pow(8*u/d,n-1)
    def H(self,x,T):
        """
        Parameters
        x : mass fraction of dry matter [0-1]
        T : temperature [degC]
        Returns
        enthalpy [kJ/kg]
        """
        return self.Cp(x)*T
    def BPE(self,**args):
            T=args["T"]
            x=args["x"]
            Lv = water.Lv_T(T)
            T += 273.15
            return 8.314*T*T*x/Lv/.018/1000
    def lycopene(self,**args):
            from scipy.integrate import solve_ivp
            from numpy import arange
            T=args["T"]
            x=args["x"]
            ts=args["ts"]
            y0 = args["y0"]
            if y0 is None:
                y0=1
            T+=273
            t_eval = arange(0, ts, 1)
            def sys_diff(t,y):
                if x>=.55:
                    return -.121238*exp(.0188*x)*exp(-2317/T)*y*60
                else:
                    return -.27527*exp(.0024*x)*exp(-2317/T)*y*60
            
            sol = solve_ivp(sys_diff, [0, ts], [y0], t_eval=t_eval)
            return sol.t, sol.y[0]
            
water =__water__()       
tomato_paste = __tomato_paste__()