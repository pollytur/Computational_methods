import pandas as pd
from statistics import mean
from dif_eq import my_derivate


def ordinary_euler(x_0, y_0, h_0, X=None, n=None):
    d = {'x': [x_0], 'y': [y_0], 'f': [my_derivate(x_0, y_0)], 'fh': [my_derivate(x_0, y_0) * h_0],
         'method': 'ordinary_euler'}
    df = pd.DataFrame(data=d)
    if n is None:
        n = round((X - x_0) / h_0)
    for i in range(n):
        x_cur = df.iloc[i][0] + h_0
        y_cur = df.iloc[i, 1] + df.iloc[i, 3]
        f_cur = my_derivate(x_cur, y_cur)
        fh_cur = f_cur * h_0
        d2 = {'x': [x_cur],
              'y': [y_cur],
              'f': [f_cur],
              'fh': [fh_cur],
              'method': 'ordinary_euler'
              }
        df2 = pd.DataFrame(data=d2)
        df = df.append(df2, ignore_index=True)
        # print(df)
    df.drop('fh', axis=1, inplace=True)
    df.drop('f', axis=1, inplace=True)
    return df


# only y rows
def r_squared_error(origin, calculated):
    y_mean = mean(calculated)
    ss_tot = 0
    ss_res = 0
    for i in range(len(origin)):
        ss_tot = ss_tot + (calculated[i] - y_mean) ** 2
        ss_res = ss_res + (calculated[i] - origin[i]) ** 2
    return 1 - ss_res / ss_tot


def errors(y_exact, y_num, method):
    err = pd.DataFrame({'n': [0], 'global': [0], 'local': [0], 'method': method})
    for i in range(1, len(y_exact)):
        gl = y_num.iloc[i][0] - y_exact.iloc[i][0]
        loc = gl - err.iloc[i - 1][1]
        d = {'n': [i], 'global': [gl], 'local': [loc],
             'method': method}
        d = pd.DataFrame(data=d)
        err = err.append(d)
    # print(err)
    return err


def enhanced_euler(x_0, y_0, h_0, X=None, n=None):
    x_cur = x_0 + h_0 / 2
    f = my_derivate(x_0, y_0)
    y_cur = y_0 + f * h_0 / 2
    f_cur = my_derivate(x_cur, y_cur)
    d = {'x': [x_0],  # 0
         'y': [y_0],  # 1
         'x+(h/2)': x_cur,  # 2
         'f': [f],  # 3
         'y+(h/2)*f(x, y)': [y_cur],  # 4
         'f(x+h/2, y+(h/2)*f(x, y))': [f_cur],  # 5
         'delta y': [f_cur * h_0],
         'method': 'enhanced_euler'}  # 6
    df = pd.DataFrame(data=d)
    if n is None:
        n = round((X - x_0) / h_0)
    for i in range(n):
        x_cur = df.iloc[i, 0] + h_0
        y_cur = df.iloc[i, 1] + df.iloc[i, 6]
        x_1_cur = x_cur + h_0 / 2
        f = my_derivate(x_cur, y_cur)
        y_1_cur = y_cur + f * h_0 / 2
        f_cur = my_derivate(x_1_cur, y_1_cur)

        d2 = {'x': [x_cur],  # 0
              'y': [y_cur],  # 1
              'x+(h/2)': [x_1_cur],  # 2
              'f': [f],  # 3
              'y+(h/2)*f(x, y)': [y_1_cur],  # 4
              'f(x+h/2, y+(h/2)*f(x, y))': [f_cur],  # 5
              'delta y': [f_cur * h_0],
              'method': 'enhanced_euler'}
        df2 = pd.DataFrame(data=d2)
        df = df.append(df2, ignore_index=True)
        # print(df)
    df.drop('x+(h/2)', axis=1, inplace=True)
    df.drop('f', axis=1, inplace=True)
    df.drop('y+(h/2)*f(x, y)', axis=1, inplace=True)
    df.drop('f(x+h/2, y+(h/2)*f(x, y))', axis=1, inplace=True)
    df.drop('delta y', axis=1, inplace=True)
    return df


def runge_kutta(x_0, y_0, h_0, X=None, n=None):
    k_1 = my_derivate(x_0, y_0)
    k_2 = my_derivate(x_0 + h_0 / 2, y_0 + h_0 * k_1 / 2)
    k_3 = my_derivate(x_0 + h_0 / 2, y_0 + h_0 * k_2 / 2)
    k_4 = my_derivate(x_0 + h_0, y_0 + h_0 * k_3)
    d_y = (k_1 + k_4 + 2 * (k_2 + k_3)) * h_0 / 6
    d = {'x': [x_0], 'y': [y_0], 'k_1': [k_1], 'k_2': [k_2], 'k_3': [k_3], 'k_4': [k_4], 'delta y': [d_y],
         'method': 'runge_kutta'}
    df = pd.DataFrame(data=d)
    if n is None:
        n = round((X - x_0) / h_0)
    for i in range(n):
        x_cur = df.iloc[i][0] + h_0
        y_cur = df.iloc[i][1] + df.iloc[i][6]
        k_1 = my_derivate(x_cur, y_cur)
        k_2 = my_derivate(x_cur + h_0 / 2, y_cur + h_0 * k_1 / 2)
        k_3 = my_derivate(x_cur + h_0 / 2, y_cur + h_0 * k_2 / 2)
        k_4 = my_derivate(x_cur + h_0, y_cur + h_0 * k_3)
        d_y = (k_1 + k_4 + 2 * (k_2 + k_3)) * h_0 / 6
        d2 = {'x': [x_cur], 'y': [y_cur], 'k_1': [k_1], 'k_2': [k_2], 'k_3': [k_3], 'k_4': [k_4], 'delta y': [d_y],
              'method': 'runge_kutta'}
        df2 = pd.DataFrame(data=d2)
        df = df.append(df2, ignore_index=True)

        # print(df)

    df.drop('k_1', axis=1, inplace=True)
    df.drop('k_2', axis=1, inplace=True)
    df.drop('k_3', axis=1, inplace=True)
    df.drop('k_4', axis=1, inplace=True)
    df.drop('delta y', axis=1, inplace=True)

    # print(df)

    return df

# if __name__ == '__main__':
#     runge_kutta(0, 1, 0.1, 1)
