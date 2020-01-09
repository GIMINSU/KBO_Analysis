from __future__ import division

import numpy as np
from scipy import optimize, signal
import pandas as pd
from pandas_datareader.data import DataReader
import statsmodels.api as sm
from statsmodels.tools.numdiff import approx_fprime, approx_fprime_cs
from IPython.display import display
import matplotlib.pyplot as plt
# import seaborn as sn
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

from numpy.testing import assert_allclose

# Set some pretty-printing options
np.set_printoptions(precision=3, suppress=True, linewidth=120)
pd.set_option('float_format', lambda x: '%.3g' % x, )

# Save the names of the equations, variables, and parameters
equation_names = [
    'static FOC', 'euler equation', 'production',
    'aggregate resource constraint', 'capital accumulation',
    'labor-leisure', 'technology shock transition'
]
variable_names = [
    'output', 'consumption', 'investment',
    'labor', 'leisure', 'capital', 'technology'
]
parameter_names = [
    'discount rate', 'marginal disutility of labor',
    'depreciation rate', 'capital share',
    'technology shock persistence',
    'technology shock standard deviation',
]

# Save some symbolic forms for pretty-printing
variable_symbols = [
    r"y", r"c", r"i", r"n", r"l", r"k", r"z",
]
contemporaneous_variable_symbols = [
    r"$%s_t$" % symbol for symbol in variable_symbols
]
lead_variable_symbols = [
    r"$%s_{t+1}$" % symbol for symbol in variable_symbols
]

parameter_symbols = [
    r"$\beta$", r"$\psi$", r"$\delta$", r"$\alpha$", r"$\rho$", r"$\sigma^2$"
]


class RBC1(object):
    def __init__(self, params=None):
        # Model dimensions
        self.k_params = 6
        self.k_variables = 7

        # Initialize parameters
        if params is not None:
            self.update(params)

    def update(self, params):
        # Save deep parameters
        self.discount_rate = params[0]
        self.disutility_labor = params[1]
        self.depreciation_rate = params[2]
        self.capital_share = params[3]
        self.technology_shock_persistence = params[4]
        self.technology_shock_std = params[5]

    def eval_logged(self, log_lead, log_contemporaneous):
        (log_lead_output, log_lead_consumption, log_lead_investment,
         log_lead_labor, log_lead_leisure, log_lead_capital,
         log_lead_technology_shock) = log_lead

        (log_output, log_consumption, log_investment, log_labor,
         log_leisure, log_capital, log_technology_shock) = log_contemporaneous

        return np.r_[
            self.log_static_foc(
                log_lead_consumption, log_lead_labor,
                log_lead_capital, log_lead_technology_shock
            ),
            self.log_euler_equation(
                log_lead_consumption, log_lead_labor,
                log_lead_capital, log_lead_technology_shock,
                log_consumption
            ),
            self.log_production(
                log_lead_output, log_lead_labor, log_lead_capital,
                log_lead_technology_shock
            ),
            self.log_aggregate_resource_constraint(
                log_lead_output, log_lead_consumption,
                log_lead_investment
            ),
            self.log_capital_accumulation(
                log_lead_capital, log_investment, log_capital
            ),
            self.log_labor_leisure_constraint(
                log_lead_labor, log_lead_leisure
            ),
            self.log_technology_shock_transition(
                log_lead_technology_shock, log_technology_shock
            )
        ]

    def log_static_foc(self, log_lead_consumption, log_lead_labor,
                       log_lead_capital, log_lead_technology_shock):
        return (
                np.log(self.disutility_labor) +
                log_lead_consumption -
                np.log(1 - self.capital_share) -
                log_lead_technology_shock -
                self.capital_share * (log_lead_capital - log_lead_labor)
        )

    def log_euler_equation(self, log_lead_consumption, log_lead_labor,
                           log_lead_capital, log_lead_technology_shock,
                           log_consumption):
        return (
                -log_consumption -
                np.log(self.discount_rate) +
                log_lead_consumption -
                np.log(
                    (self.capital_share *
                     np.exp(log_lead_technology_shock) *
                     np.exp((1 - self.capital_share) * log_lead_labor) /
                     np.exp((1 - self.capital_share) * log_lead_capital)) +
                    (1 - self.depreciation_rate)
                )
        )

    def log_production(self, log_lead_output, log_lead_labor, log_lead_capital,
                       log_lead_technology_shock):
        return (
                log_lead_output -
                log_lead_technology_shock -
                self.capital_share * log_lead_capital -
                (1 - self.capital_share) * log_lead_labor
        )

    def log_aggregate_resource_constraint(self, log_lead_output, log_lead_consumption,
                                          log_lead_investment):
        return (
                log_lead_output -
                np.log(np.exp(log_lead_consumption) + np.exp(log_lead_investment))
        )

    def log_capital_accumulation(self, log_lead_capital, log_investment, log_capital):
        return (
                log_lead_capital -
                np.log(np.exp(log_investment) + (1 - self.depreciation_rate) * np.exp(log_capital))
        )

    def log_labor_leisure_constraint(self, log_lead_labor, log_lead_leisure):
        return (
            -np.log(np.exp(log_lead_labor) + np.exp(log_lead_leisure))
        )

    def log_technology_shock_transition(self, log_lead_technology_shock, log_technology_shock):
        return (
                log_lead_technology_shock -
                self.technology_shock_persistence * log_technology_shock
        )

# Setup fixed parameters
parameters = pd.DataFrame({
    'name': parameter_names,
    'value': [0.95, 3, 0.025, 0.36, 0.85, 0.04]
})
print(parameters.T)
