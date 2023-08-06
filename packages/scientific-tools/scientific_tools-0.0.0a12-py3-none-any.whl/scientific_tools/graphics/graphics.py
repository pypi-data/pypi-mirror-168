"""This module trace function graph"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def trace_2D(function, min_variable, max_variable, values_number, args_before_variable=[], args_after_variable=[], color="blue", linestyle ="-", title="", label_x="", label_y="", **kwargs) :
    """Trace the 2D graphic of the function "function"
    
    function is a function with at least one argument
    args_before_variable is the list of positional arguments before the variable argument's position
    args_after_variable is the list of positional arguments after the variable argument's position
    The value of the variable argument varies from min_variable to max_variable by taking values_number values
    linestyle is the line style (cf Matplotlib docs for futher information)
    color is the line color
    title is the graph title
    label_x and label_y are texts to put on the axes
    You can add after keywords arguments for the function "function"
    """
    variable_list = np.linspace(min_variable, max_variable, values_number)
    results_list = []
    for variable in variable_list :
        results_list.append(function(*args_before_variable, variable, *args_after_variable, **kwargs))
    
    #displaying
    plt.plot(variable_list, results_list, color=color, linestyle=linestyle)
    plt.title(title)
    plt.xlabel(label_x)
    plt.ylabel(label_y)

def trace_3D(function, min_x, max_x, values_x, min_y, max_y, values_y, args_before_variables=[], args_between_variables=[], args_after_variables=[], x_before_y = True, colormap=cm.RdYlGn, title="", label_x ="", label_y="", label_z="", **kwargs) :
    """Trace the 3D graphic of the function "function"
    
    function is a function with at least two arguments
    args_before_variable is the list of positional arguments before the first variable argument's position
    args_between_variables is the list of positional arguments between positions of the first and the second variable
    args_after_variables is the list of positional arguments after the second variable argument's position
    x_before_x is true if x variable is the first variable (in the function arguments order)
    The value of the "x" variable varies from min_x to max_x by taking values_x values
    Idem for "y" variable
    colormap is the colormap used for displaying
    title is the graph title
    label_x, label_y and label_z are texts to put on the axes
    You can add after keywords arguments for the function "function"
    """
    line = np.linspace(min_x, max_x, values_x)
    array_x = np.array([line for i in range(values_y) ], dtype=float)
    #crée la matrice des valeurs de N
    column = np.linspace(min_y, max_y, values_y)
    array_y = np.array([[column[j]]*values_x for j in range(values_y)], dtype=float)
    #génère la matrice des valeurs de M
    results = []#a array like object with values of function
    for i in range(values_y) :
        ligne_resultats = []
        for j in range(values_x) :
            variable1 = array_x[i][j]
            variable2 = array_y[i][j]
            if x_before_y is False :
                variable1, variable2 = variable2, variable1
            ligne_resultats.append(function(*args_before_variables, variable1, *args_between_variables, variable2, *args_after_variables, **kwargs))
        results.append(ligne_resultats)
    array_z = np.array(results, dtype=float)

    linewidth = (max_x - min_x+ max_y - min_y)/20#to trace around 10 lines 

    #displaying
    ax = plt.axes(projection='3d')#affichage en 3D
    ax.plot_surface(array_x, array_y, array_z, cmap=colormap, linewidth=linewidth)#linewidth : distance between two lines
    ax.set_title(title)
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.set_zlabel(label_z)
