import numpy as np
import tqdm as tq

from .sol_ode import sol_ode
from .delay import delay

def PID_controller(model, var0, t, param, ylimit, w, y0 = 0, PID = [0,0,0], Tt = 0, x_index = -1, y_index = -1):

    """
    Create a PID controller to adjust the parameter of input ode function,
    calculate the dataframe using the adjusted parameter.

    Args:
    
        model (callable(y,t,...)): The function computes the derivative of y at t.
        var0 (array): Initial condition on var.
        t (array): A sequence of time points for which to solve for y. The initial
                    value point should be the first element of this sequence.
        param (array, optional): Input parameters to model function           
        ylimit (array, optional): Upper and lower setpoint for control element.
                    
        w (float or int, optional): The w value of the measured element function.      
        y0 (int, optional): Parameter of the PID controller. Defaults to 0.
        PID (array, optional): Parameter of the PID controller. Defaults to 0.
        Tt (float, optional): Specified dead time point.
        
        x_index (int, optional): Index of the measured element in var0.
        y_index (int, optional): Index of control element in param.

    Returns:
        results: The solved variables using adjusted control element.
        y_final: The log of the adjusted control element.
        e: The log of error signal
    """

#    warnings.filterwarnings("ignore")


    # create the y value list with initial value.
    y = y0
    y_final = np.zeros(len(t)-1)
    x = np.zeros(len(t)-1)
    e_final = np.zeros(len(t)-1)
    e = w
    KP, KI, KD = PID

    # empty dataframe for saving results
    results = list(range(len(t)-1))

    #  store the value calculated from last time.
    for i in tq.tqdm(range(len(t)-1),position=0,leave=True):
        
        y_final[i] = y
        param[y_index] = y

        #   get the solved results and get the new kla
        df = sol_ode(model, var0, t[i:i+2], param)

        # save the solved results, drop the duplicated value with the same time index,
        # only keeping the last one.
        
        results[i] = np.transpose(df)[-1]
        var0 = np.transpose(df)[-1]
        x[i] = df[x_index][-1]
        
        if Tt != 0:
            x_delay = delay(t, x, Tt, value = 0)

        else:
            x_delay = x

        e_temp = w - x_delay[i]
        # D component
        D = KD * (e - e_temp) / (t[i+1]-t[i])
        # P component
        e = e_temp
        e_final[i] = e_temp
        P = KP * e
        # I component
        I = KI* e*(t[i+1]-t[1])
        
        y = y0 + P + I + D
        y = max(min(y, ylimit[1]), ylimit[0])
        
    return np.transpose(results), y_final, e