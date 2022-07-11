from sympy import *
import copy
import matplotlib.pyplot as plt
import numpy as np

# TODO: make functions return instead of print?

# Prompt dictionary
name_dict = {
    "deltax": "Change in position: ",
    "v0": "Initial velocity: ",
    "v": "Final velocity: ",
    "a": "Acceleration: ",
    "t": "Time: ",
}

# Establish SymPy Symbols
deltax, v, v0, a, t = symbols("deltax v v0 a t")

# Keys are the missing variables in each kinematics expression
# expressions equal 0
equation_dict = {
    "deltax": -v + v0 + a * t,
    "v0": -deltax + v * t - 0.5 * a * t**2,
    "v": -deltax + v0 * t + 0.5 * a * t**2,
    "a": -deltax + 0.5 * (v0 + v) * t,
    "t": -(v**2) + v0**2 + 2 * a * deltax,
}


def get_user_input():
    # Accept user input
    var_dict = {}
    for key in name_dict:
        var_dict[key] = input(name_dict[key])

    # Change input into floats or key names
    for var in var_dict:
        if isfloat(var_dict[var]):
            var_dict[var] = float(var_dict[var])
        else:
            var_dict[var] = f"{var}"

    check_variables(var_dict)
    return var_dict


def equation_solver(var_dict):
    # Check variables:
    missing = get_missing(var_dict)

    # Kinematics equation solver
    if len(missing) == 0:
        check_variables(var_dict)
        print("You don't need me.")

    elif len(missing) == 2:
        solve_two_var(var_dict)

    elif len(missing) == 1:
        solve_one_var(var_dict)

    else:
        print("No solution.")


def solve_two_var(var_dict):
    missing = get_missing(var_dict)

    # solve for t if it is missing; else solve randomly
    if "t" in missing:
        var_one = "t"
        var_two = missing[0] if missing[0] != "t" else missing[1]
    else:
        var_one = missing[0]
        var_two = missing[1]

    expr = equation_dict[var_two]
    var_dict[var_one] = solve_equation(expr, var_dict, var_one)

    # handle multiple t solutions
    if islist(var_dict["t"]):
        print("Solution One:")
        solution_one_dict = copy.deepcopy(var_dict)
        solution_one_dict["t"] = var_dict["t"][0]
        print_missing(solution_one_dict, missing)
        solve_one_var(solution_one_dict)

        print("Solution Two:")
        solution_two_dict = copy.deepcopy(var_dict)
        solution_two_dict["t"] = var_dict["t"][1]
        print_missing(solution_two_dict, missing)
        solve_one_var(solution_two_dict)

    else:
        print("Only Solution:")
        print_missing(var_dict, missing)
        solve_one_var(var_dict)


def solve_one_var(var_dict):
    missing = get_missing(var_dict)
    var = missing[0]
    var_dict[var] = evaluate_variable(var_dict, var)
    print_missing(var_dict, missing)


def evaluate_variable(dict_name, var_name):
    if var_name != "deltax":
        expr = equation_dict["deltax"]
    else:
        expr = equation_dict["v0"]

    value = solve(expr.subs(dict_name), var_name)
    return value


def solve_equation(expr, var_dict, var_name=None):
    if var_name is None:
        return expr.subs(var_dict)  # substitutes in all variables and evaluates
    return solve(expr.subs(var_dict), var_name)  # solves for var_name


def print_missing(var_dict, missing):
    check_variables(var_dict)
    for var in missing:
        if str(var_dict[var]) != f"{var}":  # check missing value was solved for
            if isinstance(
                var_dict[var], list
            ):  # check if missing value is in list form
                var_dict[var] = float(
                    var_dict[var][0]
                )  # turn first value in list into float
            var_dict[var] = round(float(var_dict[var]), 3)
            print(f"{name_dict[var]}{var_dict[var]}")


def check_variables(var_dict):
    for key in equation_dict:
        expr = equation_dict[key]
        value = solve_equation(expr, var_dict)

        if isfloat(value):
            assert float(value) == 0, "These variable inputs are not possible."


def get_missing(var_dict):
    # List of values to solve for
    missing = [key for key in var_dict if type(var_dict[key]) == str]
    return missing


def isfloat(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError) as error:
        return False


def islist(value):
    try:
        value[1]
        return True
    except (TypeError, IndexError) as error:
        return False


def plot_kinematics_variables(var_dict):
    tvals = np.linspace(
        0, float(var_dict["t"]), 100
    )  # make all dictionary values floats
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


def main():
    # var_dict = get_user_input()
    var_dict = {"deltax": 0, "v0": 1, "v": "v", "a": -2, "t": "t"}
    equation_solver(var_dict)
    print(var_dict)
    # plot_kinematics_variables(var_dict)


if __name__ == "__main__":
    main()
