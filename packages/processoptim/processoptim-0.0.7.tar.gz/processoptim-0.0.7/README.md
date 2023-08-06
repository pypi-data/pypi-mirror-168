# Food Process Design
`processoptim` is a Python library for food process design.
## Installation
WaterOptim runs under Python 3.6+. To install it with [pip](https://pip.pypa.io/en/stable/), run the following:
`pip install processoptim`
To upgrade it with [pip](https://pip.pypa.io/en/stable/), run the following:
`pip install --upgrade processoptim`
## Basic usage
    from processoptim.properties.__properties__ import tomato_sauce
    ts = tomato_sauce()
    print("density 6% dry matter",ts.rho(0.6),"kg/m3")
    print("enthalpy 6% dry matter at 60°C",ts.H(0.6,60),"kJ/kg")
    #Tomato paste concentration
    from processoptim.opu.__evapo__ import evapo
    # n : number of effects
    # x0 : initial concentration
    # xt : target concentration
    # L0 : feed flowrate kg/s
    # Ts : steam temperature °C
    # S : heat transfer area of each effect m2
    # h : Overall heat transfer coeff of each effect W/m2/K
    # liq : product to concente, inherit from tomato_sauce class
    # N : number of tubes in each effect
    # d : tube diameter m
    # u : velocity in tubes m/s
    # l : tube length m
    x0 = 0.06
    evapo(n=3,x0=.06,xt=.32,L0=5,Ts=120,S=80,h=2,liq=ts,N=100,d=2.5e-2,u=2,l=5)
