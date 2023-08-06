# ------------------------- MINUIT PART ----------------
#  pip3 install iminout  numba_stats numpy
from iminuit import cost, Minuit
import iminuit
from numba_stats import norm, uniform # faster replacements for scipy.stats functions
import numpy as np
from scipy.integrate import quad

# from termcolor import colored
from console import fg, fx

import json
import datetime as dt

#-----------------------------------------------
def gauss(x, area,channel,sigma):
    #if area<0:      return 0.
    #if sigma<0:    return 0.
    return area*np.exp(-((x-channel)**2/(2*sigma**2)))


def print_errors(m2, chi2dof):
    WID =65
    print("_"*WID)
    print(" name              value     error       error%   remark")
    print("_"*WID)
    for key in m2.parameters:
        if len(key)==1:
            continue

        err = m2.errors[key]
        val = m2.values[key]
        if val<0:val=-val

        if val==0:
            errval = 0
        else:
            errval = 100*err/val

        if chi2dof>1:
            err = err * np.sqrt(chi2dof)

        print(f"| {key:7} | {val:11.2f} | {err:9.2f}  |  {errval:6.1f}% |", end="")
        if key=="area":
            print(f" {100/np.sqrt(val):5.2f}%  (sqrt)|")
        elif key=="fwhm":
            print(f" {100*m2.values['fwhm']/m2.values['channel']:5.2f}%  (reso)|")
        else:
            print(f"               |")


    print("_"*WID)
    if chi2dof>1: print(f"i... errors WERE scaled up  {np.sqrt(chi2dof):.1f}x     for chi2={chi2dof:.1f} !")


#
# I need to go to chebyshev
#


#------------------------------------------------------------------------
def main(x,y,dy, polorder = None):
    print("__________________________________________________ model entered")


    global bin1 # trick for better convergence
    bin1 = x[0]



    # --++++++++++++++++++++++++++++------------chi2
    def model_chi2(x,   a,b, area,channel,fwhm):
        global bin1
        #f = a* x + b
        penalty = 1

        # area =a*sigma*sqrt(2*pi)
        sigma = fwhm/2.355
        height = area/sigma/np.sqrt(np.pi*2)

        signal = gauss(x, height, channel ,sigma)
        bg =  np.polynomial.Chebyshev( [a,b] )(x-bin1)

        f = signal + bg
        #if (sigma<0) or (fwhm<0) or (area<0):
        #    f = signal

        return f





    # ---- for histograms, use cx...
    print(".............iminuit.............>")
    c2 = cost.LeastSquares(x, y, dy, model_chi2)

    bgest = (y[0]+y[-1])/2 * len(x)
    bgest = y.min() * len(x)
    areaest = sum(y)-bgest
    eneest = x[y.argmax()]



    m2 = Minuit(c2,
                area = areaest,
                channel = eneest,
                fwhm = 5,
                a=1, b=1  )

    print_errors(m2, 0) # my nice table BEFORE

    # m2.limits["a", "b", "c"] = (0, None)

    m2.migrad()       # DO MINIMIZATION <<<<<<<<<<
    #m2.minos()
    print(m2.errors) # error view
    print(m2.values) # value view

    print(m2.fmin)   #NICE table
    print("--- parameters in the table are not exact the values -----")
    print(m2.params) # NICE table

    # -------------------- it is important to keep same x vector:
    #                      chebyshev  parametrization uses  -x[0] !
    yf = model_chi2( x,
                     m2.values['a'],
                     m2.values['b'],
                     m2.values['area'],
                     m2.values['channel'],
                     m2.values['fwhm']
    )

    #-------------------- this part serves to provide y(x) points
    #                     for various scenarios to PLOT IT later
    #                     not much used..... i think
    def sig(x):
        return model_chi2(x, 0,
                          0,
                         m2.values['area'],
                         m2.values['channel'],
                         m2.values['fwhm'] )
    def sigbg_h(x):
        return model_chi2(x, m2.values['a'],
                          m2.values['b'],
                         m2.values['area']+m2.errors['area'],
                         m2.values['channel'],
                         m2.values['fwhm'] )
    def sigbg_l(x):
        return model_chi2(x, m2.values['a'],
                          m2.values['b'],
                         m2.values['area']-m2.errors['area'],
                         m2.values['channel'],
                         m2.values['fwhm'] )


    def sigbg(x):
        return model_chi2(x, m2.values['a'],
                          m2.values['b'],
                         m2.values['area'],
                         m2.values['channel'],
                         m2.values['fwhm'] )


    def bg(x):
        return model_chi2(x,m2.values['a'],
                          m2.values['b'],
                         0,
                         m2.values['channel'],
                         m2.values['fwhm'] )

    yf_bg = bg(x)
    yf_sig = sig(x)
    yf_l   = sigbg_l(x)
    yf_h   = sigbg_h(x)

    i1 = x[0]-0.5
    i2 = x[-1]+0.5
    sigarea = quad( sig    ,i1, i2 )


    print(f"i... integral BG  [ {i1}, {i2} ] :", quad( bg     ,i1, i2 ) )
    print(f"i... integral SIG [ {i1}, {i2} ] :", sigarea )
    print(f"i... integral TOT [ {i1}, {i2} ] :", quad( sigbg  ,i1, i2 )  )


    NOError = sigarea[0]>0

    print(f"i...     :  fit      =  {m2.values['area']} " )
    print(f"i...     :      integ=  {sigarea[0]} " )
    print(f"i... diff:  fit-integ=  {m2.values['area'] - sigarea[0]} " )

    print(f"i... Chebyshev parameters are not real! they are for shifted X")
    # ------------ TIME TO transfer Chi^2 to errors ---------------


    chi2dof=m2.fval/(len(x) - m2.nfit)
    if False:
        print("   FCN =",m2.fval)
        print(" points=",len(x))
        print("   par = ",m2.nfit)
        print("  Chi2 = ", chi2dof)

    print_errors(m2, chi2dof) # my nice table at end
    print()
    print(f"i... FIT IS valid ... {m2.valid} ")
    print(f" ... and accurate ... {m2.accurate}")
    print(f" ... and all ok   ... {NOError}")


    ok = True
    if not(m2.valid):
        print( f"{fg.red}X... ____________FIT SEEMS NOT  VALID___________{fg.default}" )
        ok = False
    if  not(m2.accurate):
        print( f"{fg.yellow}X... ____________          NOT ACCURATE_________{fg.default}" )
    if not NOError:
        print( f"{fg.red}X... ____________SOME ERROR IN FIT     _________{fg.default}")
        ok = False
    if m2.values['area'] + sigarea[0]<=0:
        print( f"{fg.red}X... ____________empirically : error   _________{fg.default}")
        ok = False
    if ok:
        print( f"{fg.green}i...    fit seems OK to me {fg.default}" )


    print("_________________________________________________")

    # ----- super return"
    res = {}

    res['ok'] = ok

    res['yf'] = yf
    res['yf_l'] = yf_l
    res['yf_h'] = yf_h

    res['chi2dof'] = chi2dof

    res['valid'] = m2.valid
    res['accurate'] = m2.accurate
    res['noerror'] = NOError
    #------------ the last one is OR ALL
    if not(m2.valid) or not(m2.accurate) or not(NOError):
        res['noerror'] = False

    res['x']       = x
    res['y']       = y

    res['range']    = ( x[0], x[-1] )


    res['area']    = m2.values['area']
    err            = m2.errors['area']
    if chi2dof>1:
            err = err * np.sqrt(chi2dof)
    res['darea']   = err



    res['channel'] = m2.values['channel']
    err            = m2.errors['channel']
    if chi2dof>1:
            err = err * np.sqrt(chi2dof)
    res['dchannel']   = err



    res['fwhm']    = m2.values['fwhm']
    err            = m2.errors['fwhm']
    if chi2dof>1:
            err = err * np.sqrt(chi2dof)
    res['dfwhm']   = err


    # empirical eerror
    if m2.values['area'] + sigarea[0]>0:
        res['diff_fit_int_proc'] = 100*abs(m2.values['area'] - sigarea[0])/(m2.values['area'] + sigarea[0])/2
    else:
        res['diff_fit_int_proc'] = 0

    # --------dump-----without np arrays
    dum = {}
    dum['timemark'] = dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    for i in res.keys():
        if not (type(res[i]) == np.ndarray):
            dum[i] = res[i]
    with open(".gpol1.results", "a") as f:
        json.dump( dum , f , indent=4 )
        f.write("\n")

    return res
    # return (yf,yf_l,yf_h)
