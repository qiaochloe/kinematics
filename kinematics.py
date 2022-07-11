from sympy import *
import copy
import matplotlib.pyplot as plt
import numpy as np

name_dict = {
    "deltax": "Change in position: ",
    "v0": "Initial velocity: ",
    "v": "Final velocity: ",
    "a": "Acceleration: ",
    "t": "Time: ",
}

# Accept user input
var_dict = {}
for key in name_dict:
    var_dict[key] = input(name_dict[key])

# Change input into floats or key names
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


for var in var_dict:
    if isfloat(var_dict[var]):
        var_dict[var] = float(var_dict[var])
    else:
        var_dict[var] = f"{var}"

# List of values to solve for
missing = [key for key in var_dict if type(var_dict[key]) == str]

# Establish SymPy Symbols
deltax, v, v0, a, t = symbols("deltax v v0 a t")

# Keys are the missing variables in each kinematics equation
equation_dict = {
    "deltax": -v + v0 + a * t,
    "v0": -deltax + v * t - 0.5 * a * t**2,
    "v": -deltax + v0 * t + 0.5 * a * t**2,
    "a": -deltax + 0.5 * (v0 + v) * t,
    "t": -(v**2) + v0**2 + 2 * a * deltax,
}


def islist(value):
    try:
        value[1]
        return True
    except TypeError:
        return False
    except IndexError:
        return False


def solver(dict_name, var_name):
    global equation_dict
    if var_name != "deltax":
        expr = equation_dict["deltax"]
    else:
        expr = equation_dict["v0"]
    dict_name[var_name] = solve(expr.subs(dict_name), var_name)[0]
    return dict_name


# Kinematics equation solver
if len(missing) == 0:
    print("You don't need me.")
elif 0 < len(missing) < 3:
    if len(missing) == 2:
        expr = equation_dict[missing[0]]
        var_dict[missing[1]] = solve(expr.subs(var_dict), missing[1])
        if islist(var_dict["t"]):
            solution_one_dict = copy.deepcopy(var_dict)
            solution_two_dict = copy.deepcopy(var_dict)
            solution_one_dict["t"] = var_dict["t"][0]
            solution_two_dict["t"] = var_dict["t"][1]

            solver(solution_one_dict, missing[0])
            solver(solution_two_dict, missing[0])

            print("Solution One")
            for var in missing:
                print(f"{name_dict[var]}{round(solution_one_dict[var], 3)}")
            print("Solution Two")
            for var in missing:
                print(f"{name_dict[var]}{round(solution_two_dict[var], 3)}")
        else:
            var_dict[missing[1]] = var_dict[missing[1]][0]
            solver(var_dict, missing[0])
            print("Only Solution")
            for var in missing:  # make code more attactive again
                print(f"{name_dict[var]}{round(var_dict[var], 3)}")
    else:
        solver(var_dict, missing[0])
        print("Only Solution")
        for var in missing:
            print(f"{name_dict[var]}{round(var_dict[var], 3)}")
else:
    print("No solution.")

# make plots handle multiple solutions - create a function?

tvals = np.linspace(0, float(var_dict["t"]), 100)  # make all dictionary values floats
avals = np.full(tvals.shape, var_dict["a"])
vvals = var_dict["v0"] + var_dict["a"] * tvals
xvals = var_dict["v0"] * tvals + 1 / 2 * var_dict["a"] * tvals**2

plt.plot(tvals, avals, label="Acceleration (m/s^2)")
plt.plot(tvals, vvals, label="Velocity (m/s)")
plt.plot(tvals, xvals, label="Position (m)")

plt.title("Position, Velocity, Acceleration")
plt.xlabel("Time (s)")
plt.grid(alpha=0.4, linestyle="--")  # opacity of .4
plt.legend()

plt.show()
