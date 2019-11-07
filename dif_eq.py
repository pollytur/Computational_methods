import math
import pandas as pd


def find_coef_for_exact_solutions(x_0, y_0):
    return y_0 / (x_0 * x_0 * math.exp(-3 / x_0))


# note x!=0
def count_funct(x, c=0):
    return c * x * x * math.exp(-3. / x)


def my_func(x_0, y_0, h_0, X=None, n=None):
    c = find_coef_for_exact_solutions(x_0=x_0, y_0=y_0)
    d = {'x': [x_0], 'y': [y_0], 'method': 'exact'}
    df = pd.DataFrame(data=d)
    if n is None:
        n = round((X - x_0) / h_0)
    for i in range(n):
        d = {'x': [df.iloc[i][0] + h_0], 'y': [count_funct(x=df.iloc[i][0], c=c)], 'method': 'exact'}
        d = pd.DataFrame(data=d)
        df = df.append(d)
        # print(df)
    return df


def my_derivate(x, y):
    return (3 * y + 2 * x * y) / (x * x)
