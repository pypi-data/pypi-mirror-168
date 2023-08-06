from numpy import log, sqrt, exp, NaN, pi
from scipy import stats
import pandas as pd
import sys
from datetime import datetime as dt
from datetime import date as dte
from datetime import timedelta
import plotly.express as px


def bsm_vega(S0, K, T, r, sigma):

    d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T / (sigma * sqrt(T)))
    vega = S0 * stats.norm.pdf(d1, 0.0, 1.0) * sqrt(T)

    return vega


def bsm_call_value(S0, K, T, r, sigma):

    
    d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = (log(S0 / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    
    value = (S0 * stats.norm.cdf(d1, 0.0, 1.0) - K * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))
    # stats.norm.cdf --> cumulative distribution function
    # for normal distribution
    return value


def bsm_call_imp_vol(S0, K, T, C0, r, it = 1000):
    
    sigma_est = 0.15
    
    for i in range(it):
        sigma_est -= ((bsm_call_value(S0, K, T, r, sigma_est) - C0) / bsm_vega(S0, K, T, r, sigma_est))
        
    return sigma_est


def bsm_call_theta(S0, T, sigma, K, r):
    
    
    d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = (log(S0 / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    
    theta = -((S0 * stats.norm.pdf(d1, 0.0, 1.0) * sigma) \
    / (2 * sqrt(T))) - r * K * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0)
    
    return theta / 365


def model_theta(spot_price, exp_date, value_date, premium, strike, risk_free,
                instrument = ""):
    
    value_date = (datetime.strptime(value_date, "%d-%m-%Y"))
    exp_date = datetime.strptime(exp_date, "%d-%m-%Y")
    days_to_exp = ((exp_date) - (value_date)).days
    iv = bsm_call_imp_vol(spot_price, strike, days_to_exp / 365, premium, risk_free)
    theta_starting = bsm_call_theta(spot_price, days_to_exp / 365, iv, strike, risk_free)
    intrinsic = max(spot_price - strike, 0)
    extrinsic = premium - intrinsic
    
    theta_list = []
    option_premiums = []
    days_list = []
    dates_list = []
    intrinsic_list = []
    extrinsic_list = []
    
    for days in range(days_to_exp, -1, -1):
        
        if days != 0:
            theta = bsm_call_theta(spot_price, days/365, iv, strike, risk_free)
        else:
            theta = -(extrinsic_list[-1] )
        
        if len(option_premiums) != 0:
            option_new_premium = option_premiums[-1] + theta
        else:
            option_new_premium = premium + theta
        
        
        
        value_date = value_date + timedelta(days = 1)
        
        intrinsic = max(spot_price - strike, 0)
        extrinsic = option_new_premium - intrinsic
        
        intrinsic_list.append(intrinsic)
        extrinsic_list.append(extrinsic)
        option_premiums.append(option_new_premium)
        days_list.append(days)
        dates_list.append(value_date)
        theta_list.append(theta)
        
    
    result_df = pd.DataFrame({"Date" : dates_list, "Premium" : option_premiums, "Days to exp" : days_list,
                              "Theta" : theta_list, "Intrinsic" : intrinsic_list, "Extrinsic" : extrinsic_list,
                              "Instrument": [instrument for i in range(len(theta_list))]})
    
    result_df["Cumulative Theta Decay"] = round(result_df["Theta"].cumsum(), 2)
    
    price_chart_name = instrument + " Price Decay"
    theta_chart_name = instrument + " Theta Decay"
    cumsum_theta_chart_name = instrument + " Cumulative Theta Decay"
    
    price_chart = px.line(result_df, x="Date", y="Premium", title=price_chart_name)
    price_chart.show()
    
    theta_chart = px.line(result_df, x="Date", y="Theta", title=theta_chart_name)
    theta_chart.show()
    
    cumsum_theta_chart_name = px.line(result_df, x="Date", y="Cumulative Theta Decay", title=cumsum_theta_chart_name)
    cumsum_theta_chart_name.show()
    
    return result_df





