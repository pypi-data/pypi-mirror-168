import os
import itertools
import multiprocessing as mp

from .equity_curves import *
from .signals import *

def generate_filepath(py_filename, output_folder, start_date, end_date, para_dict, para_combination):
    start_date_str = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime("%Y%m%d")
    end_date_str = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime("%Y%m%d")
    save_name = f'file={py_filename}&date={start_date_str}{end_date_str}'

    for i, key in enumerate(para_dict):
        para = para_combination[i]
        if key == 'code':
            if str(para).isdigit():
                para = str(para).zfill(5)

        if isinstance(para, float):
            if para.is_integer():
                para = int(para)

        save_name += f'{key}={str(para)}&'

    filepath = os.path.join(output_folder, f'{save_name[:-1]}.csv')

    return filepath


def mp_cal_performance(tuple_data):
    save_path    = tuple_data[0]
    start_date   = tuple_data[1]
    end_date     = tuple_data[2]
    manager_list = tuple_data[3]
    ii           = tuple_data[4]

    result = cal_performance(save_path, start_date, end_date)
    manager_list.append((ii,result))


def get_result_df(py_filename, output_folder, start_date, end_date, para_dict):

    para_key_list = list(para_dict)
    para_list = list(para_dict.values())
    result_df = pd.DataFrame(list(itertools.product(*para_list)), columns=para_key_list)

    manager_list = mp.Manager().list()

    cal_performance_list = []
    for ii in range(len(result_df)):
        save_path = generate_filepath(py_filename, output_folder, start_date, end_date, para_dict, result_df.iloc[ii])
        cal_performance_list.append((save_path, start_date, end_date, manager_list, ii))

    pool = mp.Pool(processes=32)
    pool.map(mp_cal_performance, cal_performance_list)
    pool.close()

    for result_tuple in manager_list:
        ii       = result_tuple[0]
        sub_dict = result_tuple[1]
        for key, value in sub_dict.items():
            if key not in result_df.columns:
                result_df[key] = np.NaN
            result_df.at[ii,key] = value

    return result_df


def plot_equity_curves(py_filename, output_folder, start_date, end_date, para_dict, result_df, subchart_settings):

    app = equity_curves.Plot(py_filename, output_folder, start_date, end_date, para_dict, result_df, generate_filepath, subchart_settings)

    return app


def plot_signal_analysis(py_filename, output_folder, start_date, end_date, para_dict, signal_settings):

    app = signals.Signals(py_filename, output_folder, start_date, end_date, para_dict, generate_filepath, signal_settings)

    return app


def cal_performance(save_path, start_date, end_date):
    result_dict = {}

    start_date_year = datetime.datetime.strptime(start_date, '%Y-%m-%d').year
    end_date_year = datetime.datetime.strptime(end_date, '%Y-%m-%d').year
    year_list = list(range(start_date_year, end_date_year + 1))
    for y in year_list: result_dict[str(y)] = []

    df = pd.read_csv(save_path)

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    net_profit = df.loc[df.index[-1], 'net_profit']
    mdd_dollar = df.loc[df.index[-1], 'mdd_dollar']
    mdd_pct = df.loc[df.index[-1], 'mdd_pct']

    signal = df['action'].value_counts()
    df2 = df[df['action'].notnull()].reset_index(drop=True)

    holding_period_day = (df.loc[df.index[-1], 'date'] - df.loc[df.index[0], 'date']).days

    num_of_trade = signal['open'] if 'open' in signal else 0
    num_of_loss = len(df2[df2['realized_pnl'] < 0])
    num_of_win = num_of_trade - num_of_loss

    if num_of_trade > 0:
        win_rate = round(100 * num_of_win / num_of_trade, 2)
        loss_rate = round(100 * num_of_loss / num_of_trade, 2)
    else:
        win_rate = 0
        loss_rate = 0

    initial_capital = df.loc[df.index[0], 'equity_value']
    equity_value_pct_series = df['equity_value'].pct_change()
    equity_value_pct_series = equity_value_pct_series.dropna()

    return_on_capital = net_profit / initial_capital
    annualized_return = (1 + return_on_capital) ** (365 / holding_period_day) - 1
    annualized_std = equity_value_pct_series.std() * math.sqrt(365)

    if annualized_std > 0:
        annualized_sr = annualized_return / annualized_std
    else:
        annualized_sr = 0

    return_on_capital = round(100 * return_on_capital, 2)
    annualized_return = round(100 * annualized_return, 2)
    annualized_std = round(100 * annualized_std, 2)
    annualized_sr = round(annualized_sr, 2)

    bah_return = df.loc[df.index[-1], 'close'] / df.loc[df.index[0], 'close'] - 1
    bah_annualized_return = (1 + bah_return) ** (365 / holding_period_day) - 1
    bah_annualized_std = df['pct_change'].std() * math.sqrt(365)

    if bah_annualized_std > 0:
        bah_annualized_sr = bah_annualized_return / bah_annualized_std
    else:
        bah_annualized_sr = 0

    bah_return = round(100 * bah_return, 2)
    bah_annualized_return = round(100 * bah_annualized_return, 2)
    bah_annualized_std = round(100 * bah_annualized_std, 2)
    bah_annualized_sr = round(bah_annualized_sr, 2)

    df['bah_equity_curve'] = df['close'] * initial_capital // df.loc[df.index[0], 'close']
    df['bah_dd_dollar'] = df['bah_equity_curve'].expanding().max() - df['bah_equity_curve']
    df['bah_dd_pct'] = df['bah_dd_dollar'] / df['bah_equity_curve'].expanding().max()

    bah_mdd_dollar = df['bah_dd_dollar'].max()
    bah_mdd_pct = df['bah_dd_pct'].max()
    bah_mdd_pct = 100 * bah_mdd_pct

    total_commission = df['commission'].sum()

    result_dict['net_profit_to_mdd'] = 0
    result_dict['net_profit'] = net_profit
    result_dict['mdd_dollar'] = mdd_dollar
    result_dict['mdd_pct'] = mdd_pct
    result_dict['num_of_trade'] = num_of_trade
    result_dict['win_rate'] = win_rate
    result_dict['loss_rate'] = loss_rate

    result_dict['holding_period_day'] = holding_period_day
    result_dict['return_on_capital'] = return_on_capital
    result_dict['annualized_return'] = annualized_return
    result_dict['annualized_std'] = annualized_std
    result_dict['annualized_sr'] = annualized_sr

    result_dict['bah_return'] = bah_return
    result_dict['bah_annualized_return'] = bah_annualized_return
    result_dict['bah_annualized_std'] = bah_annualized_std
    result_dict['bah_annualized_sr'] = bah_annualized_sr
    result_dict['bah_mdd_dollar'] = bah_mdd_dollar
    result_dict['bah_mdd_pct'] = bah_mdd_pct

    result_dict['total_commission'] = total_commission

    if mdd_dollar == 0:
        result_dict['net_profit_to_mdd'] = np.inf
    else:
        result_dict['net_profit_to_mdd'] = net_profit / mdd_dollar

    df3 = df[df['action'] == 'open']
    df3 = df3.set_index('date')
    current_year = datetime.datetime.now().year
    signal_year_count = df3.groupby(lambda x: x.year).size()

    signal_year_std = np.std(signal_year_count)
    signal_year_mean = np.mean(signal_year_count)
    cov = round(signal_year_std / signal_year_mean, 3)

    result_dict['cov'] = cov

    for y in year_list:
        try:
            result_dict[str(y)] = signal_year_count[y]
        except:
            result_dict[str(y)] = 0

    result_dict['return_to_bah'] = return_on_capital / bah_return

    return result_dict