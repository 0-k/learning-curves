import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np

path = '../data/experience_curve_PV.csv'

data = pd.read_csv(path, sep=';', decimal=',', usecols=[0,1,2])

def func(x, a, b):
    return a*x+b

def power_func(x, a, b):
    return a * x**b

def exp_func(x, a, b):
    return a* np.exp(-b*x)

def lin_func(x, a, b):
    return a + b*x

def plot_log_log():
    opt = (optimize.curve_fit(power_func, data.Cumulative_Shipments * 10 ** 6, data.ASP_in_2018USD))
    opt_result = (opt[0])
    range = np.logspace(np.log10(min(data.Cumulative_Shipments*10**6)), np.log10(max(data.Cumulative_Shipments*10**6)), 100)
    fig, ax = plt.subplots()
    plt.rc('font', family='serif')
    ax.loglog(range, power_func(range, opt_result[0], opt_result[1]), color='#9e9e9e', linewidth=1, linestyle='--')
    ax.loglog(data.Cumulative_Shipments*10**6, data.ASP_in_2018USD, color='black')
    ax.grid(color='#e5e5e5')

    label_x_1976 = 0.32*1e6
    label_y_1976 = 70.12
    label_x_1997 = 716.17*1e6
    label_y_1997 =  6.177516
    label_x_2018 = max(data.Cumulative_Shipments*10**6)
    label_y_2018 = min(data.ASP_in_2018USD)

    ax.set_xlabel('Solar PV Cumulative Installed Capacity [W]')
    ax.set_ylabel('Solar PV Module Cost [\$2018/W]')
    ax.annotate('2018', xy=(label_x_2018, label_y_2018), xytext=(5e10, label_y_2018-0.02),
                arrowprops=dict(facecolor='grey', shrink=0.08, headwidth=1, width=1))
    ax.annotate('1997', xy=(label_x_1997, label_y_1997), xytext=(3e9, label_y_1997+0.18),
                arrowprops=dict(facecolor='grey', shrink=0.10, headwidth=1, width=1))
    ax.annotate('1976', xy=(label_x_1976, label_y_1976), xytext=(1.3e6, label_y_1976+2),
                arrowprops=dict(facecolor='grey', shrink=0.10, headwidth=1, width=1))
    plt.savefig('../graphs/learning_curve_PV.png')
    plt.show()


def plot_log():
    opt = (optimize.curve_fit(lin_func, data.Year, np.log(data.ASP_in_2018USD)))
    opt_result = (opt[0])
    plt.rc('font', family='serif')
    fig, ax = plt.subplots()
    ax.set_xlabel('Year')
    ax.set_ylabel('Solar PV Module Cost [\$2018/W]')
    ax.grid(color='#e5e5e5')
    range_time = range(1, 2018-1979+2)
    range_time_10 = range(1, 2018-2009+2)
    fitted_values = []
    for year in range_time:
        fitted_values.append(32.457 * np.exp(-0.0957*year))
    fitted_values_10 = []
    for year in range_time_10:
        fitted_values_10.append(2.4837 * np.exp(-0.1932*year))
    ax.semilogy(data.Year[3:], data.ASP_in_2018USD[3:], color='black', label='Module cost')
    ax.semilogy(data.Year[3:], fitted_values, color='#9e9e9e', linewidth=1, linestyle='--', label='Exponential fit (last 40 years)')
    ax.semilogy(data.Year[-10:], fitted_values_10, color='#9e9e9e', linewidth=1, linestyle='-.', label='Exponential fit (last 10 years)')

    plt.legend()
    plt.savefig('../graphs/exponential_curve_PV.png')
    plt.show()


if __name__ == '__main__':
    plot_log_log()
    plot_log()