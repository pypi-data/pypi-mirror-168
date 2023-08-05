import pandas as pd
import datetime
import math

from dash import dcc, html    ## pip install dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go



class Components:
    chart_bg = '#1f2c56'

    sort_method_dropdown = html.Div(
        dbc.Select(id='sort_method',
                   placeholder="Select Sorting Method",
                   options=[{'label': 'Top 20 Net Profit', 'value': 'Top 20 Net Profit'},
                            {'label': 'Top 20 Net Profit to MDD', 'value': 'Top 20 Net Profit to MDD'}, ],
                   style={'border-radius': '5px', 'font-size': '12px', }),
        style={'padding-left': '12.5px', 'width': '230px'})

    subchart_dropdown = html.Div(
        dbc.Select(id='subchart_dropdown',
                   placeholder="Select Sorting Method",
                   options=[{'label': 'Top 20 Net Profit', 'value': 'Top 20 Net Profit'},
                            {'label': 'Top 20 Net Profit to MDD', 'value': 'Top 20 Net Profit to MDD'}, ],
                   style={'border-radius': '5px', 'font-size': '12px', }),
        style={'padding-left': '12.5px', 'width': '230px'})

    filter_dropdown = html.Div(id='filter_dropdown',
                               children=dbc.Select(id='filter_name',
                                                   placeholder="Select Filter",
                                                   options=[
                                                       {'label': 'Exclude Stock', 'value': 'exclude'},
                                                       {'label': 'Return to BaH Ratio >', 'value': 'return_to_bah>'},
                                                       {'label': 'Return to BaH Ratio <', 'value': 'return_to_bah<'},
                                                       {'label': 'Sharp Ratio >', 'value': 'annualized_sr>'},
                                                       {'label': 'Sharp Ratio <', 'value': 'annualized_sr<'},
                                                       {'label': 'MDD Percentage >', 'value': 'mdd_pct>'},
                                                       {'label': 'MDD Percentage <', 'value': 'mdd_pct<'},
                                                       {'label': 'Trade Count >', 'value': 'num_of_trade>'},
                                                       {'label': 'Trade Count <', 'value': 'num_of_trade<'},
                                                       {'label': 'COV >', 'value': 'cov>'},
                                                       {'label': 'COV <', 'value': 'cov<'},
                                                       {'label': 'Win Rate >', 'value': 'win_rate>'},
                                                       {'label': 'Win Rate <', 'value': 'win_rate<'},
                                                   ],
                                                   style={'border-radius': '5px', 'font-size': '12px'}),
                               style={'padding-left': '15px', 'width': '170px'})

    filter_dropdown_disabled = html.Div(id='filter_dropdown',
                                        children=dbc.Select(id='filter_name', disabled=True,
                                                            placeholder="Select Filter",
                                                            style={'border-radius': '5px', 'font-size': '12px',
                                                                   'backgroundColor': 'Gray'}),
                                        style={'padding-left': '15px', 'width': '170px'})

    filter_input = dbc.Input(id='filter_input', value=None, size="md", type='text',
                             style={'width': '50px', 'margin-right': '5px', 'border-radius': '3px',
                                      'padding': '6px 5px', 'font-size': '12px', })

    filter_input_disabled = dbc.Input(id='filter_input', value=None, size="md", disabled=True,
                                      style={'width': '50px', 'margin-right': '5px', 'border-radius': '3px',
                                               'padding': '6px 5px', 'font-size': '12px', 'backgroundColor': 'Gray'})

    add_button_style = {'margin-left': '50px', 'width': '140px', 'backgroundColor': 'blue',
                        'border-radius': '5px', 'text-align': 'center', 'cursor': 'pointer'}

    add_button_style_disabled = {'margin-left': '50px', 'width': '140px', 'color': 'Silver', 'backgroundColor': 'Gray',
                                 'border-radius': '5px', 'text-align': 'center'}


    def empty_line_chart(self):
        chart_bg = self.chart_bg
        fig_line = px.line()
        fig_line.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, margin=dict(l=85, r=60, t=30, b=40),
                               height=340, font={"color": chart_bg})
        fig_line.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor=chart_bg)
        fig_line.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor=chart_bg)

        return fig_line


    def update_checkbox_div(self, para_dict, result_df):
        # find the unique values from result_df according to the key from para_dict
        checkbox_values = {}
        for key in para_dict:
            if not key == 'code':
                unique_values = list(dict.fromkeys(result_df[key].tolist()))
                try:
                    unique_values.sort()
                except:
                    pass
                checkbox_values[key] = unique_values

        checkbox_div = []
        for i, para_name in enumerate (para_dict):
            if not para_name == 'code':
                _options = checkbox_values[para_name]
                if _options == [False, True]:
                    _checklist = dcc.Checklist([str(tf) for tf in _options], [str(tf) for tf in _options], inline=True,
                                               id={'type': 'para-checklist', 'index': i},
                                               labelStyle={'font-size': '11px'},
                                               inputStyle={'margin-left': '10px', 'margin-right': '3px'})
                else:
                    _checklist = dcc.Checklist(_options, _options, inline=True,
                                               id={'type': 'para-checklist', 'index': i},
                                               labelStyle={'font-size': '11px'},
                                               inputStyle={'margin-left': '10px', 'margin-right': '3px'})
                row = html.Div(
                    dbc.Row([
                        html.Div(para_name),
                        html.Div(style={'height': '5px'}),
                        html.Div(_checklist),
                        html.Div(style={'height': '5px'}),
                    ]), style={'padding': '0px 20px', 'font-size': '11px'})

                checkbox_div.append(row)

        return checkbox_div


    def update_performance_matrix(self, start_date,end_date,df,para_dict):
        per_col1 = []
        per_col2 = []
        per_col_1_1 = []
        per_col_1_2 = []
        per_col_2_1 = []
        per_col_2_2 = []

        keys = ['num_of_trade', 'net_profit', 'net_profit_to_mdd','total_commission',
                'mdd_dollar', 'mdd_pct', 'return_on_capital', 'annualized_return', 'annualized_std', 'annualized_sr',
                'return_to_bah', 'win_rate', 'cov',
                'bah_mdd_dollar', 'bah_mdd_pct', 'bah_return', 'bah_annualized_return', 'bah_annualized_std',
                'bah_annualized_sr']

        try:
            df['net_profit'] = "{:,}".format(int(round(df['net_profit'], 0)))
            df['net_profit_to_mdd'] = round(df['net_profit_to_mdd'], 2)
            df['total_commission'] = "{:,}".format(int(round(df['total_commission'] , 0)))

            df['mdd_dollar'] = "{:,}".format(int(round(df['mdd_dollar'], 0)))
            df['mdd_pct'] = "{:.0%}".format(df['mdd_pct'] / 100)
            df['return_on_capital'] = "{:.0%}".format(df['return_on_capital'] / 100)
            df['annualized_return'] = "{:.0%}".format(df['annualized_return'] / 100)

            df['cov'] = round(df['cov'], 2)
            df['win_rate'] = "{:.0%}".format(df['win_rate'] / 100)
            df['return_to_bah'] = round(df['return_to_bah'], 2)

            df['bah_mdd_dollar'] = "{:,}".format(int(round(df['bah_mdd_dollar'], 0)))
            df['bah_mdd_pct'] = "{:.0%}".format(df['bah_mdd_pct'] / 100)
            df['bah_return'] = "{:.0%}".format(df['bah_return'] / 100)
            df['bah_annualized_return'] = "{:.0%}".format(df['bah_annualized_return'] / 100)
        except Exception as e:
            # print(e)
            pass

        per_col_1_1.append(html.Div('Number of Trade'))
        per_col_1_1.append(html.Div('Net Profit'))
        per_col_1_1.append(html.Div('Net Profit to MDD'))
        per_col_1_1.append(html.Div('Total Commission'))
        per_col_1_1.append(html.Div(html.Img()))
        per_col_1_1.append(html.Div('MDD Dollar'))
        per_col_1_1.append(html.Div('MDD Percentage'))
        per_col_1_1.append(html.Div('Return on Capital'))
        per_col_1_1.append(html.Div('Annualized Return'))
        per_col_1_1.append(html.Div('Annualized Std'))
        per_col_1_1.append(html.Div('Annualized Sharp Ratio'))

        for i in range(4):
            per_col_1_2.append(html.Div(df[keys[i]], style={'text-align': 'center'}))
        per_col_1_2.append(html.Div(html.Img()))
        for i in range(4, 10):
            per_col_1_2.append(html.Div(df[keys[i]], style={'text-align': 'center'}))

        per_col_2_1.append(html.Div('Return to BaH Ratio'))
        per_col_2_1.append(html.Div('Win Rate'))
        per_col_2_1.append(html.Div('COV'))
        per_col_2_1.append(html.Div(html.Img()))
        per_col_2_1.append(html.Div(html.Img()))
        per_col_2_1.append(html.Div('BaH MDD Dollar'))
        per_col_2_1.append(html.Div('BaH MDD Percentage'))
        per_col_2_1.append(html.Div('BaH Return'))
        per_col_2_1.append(html.Div('BaH Annualized Return'))
        per_col_2_1.append(html.Div('BaH Annualized Std'))
        per_col_2_1.append(html.Div('BaH Annualized Sharp Ratio'))

        for i in range(10, 13):
            per_col_2_2.append(html.Div(str(df[keys[i]]), style={'text-align': 'center'}))
        per_col_2_2.append(html.Div(html.Img()))
        per_col_2_2.append(html.Div(html.Img()))
        for i in range(13, 19):
            per_col_2_2.append(html.Div(str(df[keys[i]]), style={'text-align': 'center'}))

        per_col1.append(dbc.Row([dbc.Col(html.Div(per_col_1_1), width=9),
                                 dbc.Col(per_col_1_2, style={'padding': '0'}, width=3)]))
        per_col2.append(dbc.Row([dbc.Col(html.Div(per_col_2_1), width=9),
                                 dbc.Col(per_col_2_2, style={'padding': '0'}, width=3)]))

        start_date_year = datetime.datetime.strptime(start_date, '%Y-%m-%d').year
        end_date_year = datetime.datetime.strptime(end_date, '%Y-%m-%d').year
        year_list = list(range(start_date_year, end_date_year))

        year_col1 = []
        year_col2 = []

        if len(year_list) < 11:
            for i in range(len(year_list)):
                year_col1.append(dbc.Row([dbc.Col(year_list[i], style={'padding-left': '20px'}, width=3),
                                          dbc.Col(df[str(year_list[i])], style={'text-align': 'center'}
                                                  , width=3)], style={'font-size': '11px'}))

        title = []
        for key in para_dict:
            title_div = []
            title_div.append(html.Div(key, style={'margin-right': '5px', 'display': 'inline'}))
            title_div.append(html.Div(':', style={'margin-right': '5px', 'display': 'inline'}))
            title_div.append(html.Div(str(df[key]) + ' ', style={'margin-right': '10px', 'display': 'inline'}))
            title.append(html.Span(title_div))

        matrix_div = html.Div([
            html.Div(style={'height': '5px', }),
            dbc.Row(html.Div(title), style={'padding-left': '10px', 'font-size': '14px'}),
            html.Div(style={'height': '5px', }),
            dbc.Row([
                dbc.Col(html.Div(children=per_col1), style={'font-size': '11px'}, width=4),

                dbc.Col(html.Div(children=per_col2), style={'font-size': '11px'}, width=4),

                dbc.Col([html.Div('Year Signal Count', style={'font-size': '12px'}),
                         html.Div(children=year_col1)], style={'padding-left': '30px'}, width=4),

            ], style={'padding': '10px'})
        ])

        return matrix_div


    filter_options = {
            'num_of_trade':'Trade Count',
            'annualized_sr': 'Sharp Ratio',
            'mdd_pct':'MDD Percentage',
            'cov':'COV',
            'win_rate':'Win Rate',
            'return_to_bah': 'Return to BnH Ratio',
            'exclude': 'Exclude',
        }
    def update_filter_div(self, filter_list):
        filter_button = []
        for i, element in enumerate(filter_list):
            # element = filter_list[i]
            filter_full = []
            filter_full.append(html.Div(self. filter_options[element[0]], style={'margin-right': '15px', 'display': 'inline'}))
            filter_full.append(html.Div(element[1], style={'margin-right': '15px', 'display': 'inline'}))
            filter_full.append(html.Div(element[2], style={'margin-right': '15px', 'display': 'inline'}))
            filter_button.append(dbc.Row([
                dbc.Col(html.Div(filter_full,
                                 style={'font-size': '12px', 'padding': '0px', 'margin': '0px'}), width=10),
                dbc.Col(html.Div(children=html.Div('✗', style={'padding': '0px', 'margin': '0px'}),
                                 id='button_' + str(i), n_clicks=i,
                                 style={'font-size': '12px', 'backgroundColor': 'rgba(0, 0, 0, 0)',
                                        'border': '0px black solid', 'padding': '0px', 'padding-bottom': '10px',
                                        'margin': '0px', 'width': '5px', 'cursor': 'pointer'}), width=2)
            ]))

        for i in range(len(filter_list), 10):
            filter_button.append(html.Div(id='button_' + str(i), n_clicks=i))

        return filter_button


    def sort_method_df(self, sort_method, result_df):
        if sort_method == 'Top 20 Net Profit':
            df_sorted = result_df.sort_values(by='net_profit', ascending=False).head(20).copy()
        elif sort_method == 'Top 20 Net Profit to MDD':
            df_sorted = result_df.sort_values(by='net_profit_to_mdd', ascending=False).head(20).copy()
        else:
            df_sorted = result_df.copy()

        df_sorted = df_sorted.reset_index(drop=True)

        line_colour = []
        for c in range(len(df_sorted)):
            profile = c % 6
            degree = (c // 6) / math.ceil(len(df_sorted) / 6)
            line_colour.append(self.assign_colour(profile, degree))
        df_sorted['line_colour'] = line_colour

        return df_sorted


    def assign_colour(self, profile, degree):
        if profile == 0:    rgb = (0, int(252 - 252 * degree), 252)
        elif profile == 1:  rgb = (int(252 - 252 * degree), 252, 0)
        elif profile == 2:  rgb = (252, 0, int(252 - 252 * degree))
        elif profile == 3:  rgb = (0, 252, int(252 * degree))
        elif profile == 4:  rgb = (252, int(252 * degree), 0)
        elif profile == 5:  rgb = (int(252 * degree), 0, 252)
        return 'rgb' + str(rgb)


    def generate_chart_1(self, graph_df, para_key_list, generate_filepath, filename, output_folder, start_date, end_date,
                   para_dict):
        fig_line = px.line()
        fig_line.update_xaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
        fig_line.update_yaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
        fig_line.update_layout(plot_bgcolor=self.chart_bg, paper_bgcolor=self.chart_bg, height=340,
                               margin=dict(l=85, r=25, t=10, b=0),
                               showlegend=False,
                               font={"color": "white", 'size': 10.5}, yaxis={'title': 'Equity'},
                               xaxis={'title': ''}
                               )

        for i in graph_df.index:
            para_values = []
            hovertemplate = "%{x}<br>"
            for key in para_key_list:
                para_values.append(graph_df.iloc[i][key])
                hovertemplate = hovertemplate + \
                                key + " : " + str(graph_df.iloc[i][key]) + "<br>"
            hovertemplate = hovertemplate + "<br>"
            hovertemplate = hovertemplate + "Return to BaH Ratio : " + str(
                round(graph_df.iloc[i]['return_to_bah'], 2)) + "<br>"
            hovertemplate = hovertemplate + "Net Profit to MDD: " + str(
                round(graph_df.iloc[i]['net_profit_to_mdd'], 2)) + "<br>"
            hovertemplate = hovertemplate + "Sharp Ratio : " + str(graph_df.iloc[i]['annualized_sr']) + "<br>"
            hovertemplate = hovertemplate + "MDD Percentage : " + "{:.0%}".format(
                graph_df.iloc[i]['mdd_pct'] / 100) + "<br>"
            hovertemplate = hovertemplate + "Trade Count : " + str(graph_df.iloc[i]['num_of_trade']) + "<br>"
            hovertemplate = hovertemplate + "COV : " + str(round(graph_df.iloc[i]['cov'], 2)) + "<br>"
            hovertemplate = hovertemplate + "Win Rate : " + "{:.0%}".format(
                graph_df.iloc[i]['win_rate'] / 100) + "<br>"
            hovertemplate = hovertemplate + "<br>"

            save_path = generate_filepath(filename, output_folder, start_date, end_date, para_dict, para_values)
            line_colour = graph_df.loc[i].line_colour

            df = pd.read_csv(save_path)
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

            hovertemplate = hovertemplate + "Equity : %{y:,.0f}"

            fig_line.add_trace(go.Scatter(mode='lines', hovertemplate=hovertemplate,
                                          x=df['date'], y=df['equity_value'],
                                          line=dict(color=line_colour, width=1.5), name=''), )
        return fig_line


    def prepare_df_chart(self, df):     # Chart Data for Chart 2
        df_chart = pd.DataFrame()
        df_chart['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df_chart['close'] = df['close']
        df_chart['bah'] = df['close'] * (100000 / df_chart.iloc[0].close)
        df_chart['equity_value'] = df['equity_value']
        df_chart['action'] = df['action']
        df_chart['volume'] = df['volume']
        df_chart['sma'] = df['sma']

        _open = []
        _stop_loss = []
        _close_logic = []
        _profit_target = []

        for i in range(len(list(df['action']))):
            element = list(df['action'])[i]
            if element == 'open':
                _open.append(df_chart.iloc[i].bah)
                _stop_loss.append(None)
                _close_logic.append(None)
                _profit_target.append(None)
            elif element == 'stop_loss':
                _open.append(None)
                _stop_loss.append(df_chart.iloc[i].bah)
                _close_logic.append(None)
                _profit_target.append(None)
            elif element == 'close_logic':
                _open.append(None)
                _stop_loss.append(None)
                _close_logic.append(df_chart.iloc[i].bah)
                _profit_target.append(None)
            elif element == 'profit_target':
                _open.append(None)
                _stop_loss.append(None)
                _close_logic.append(None)
                _profit_target.append(df_chart.iloc[i].bah)
            else:
                _open.append(None)
                _stop_loss.append(None)
                _close_logic.append(None)
                _profit_target.append(None)

        df_chart['open'] = _open
        df_chart['stop_loss'] = _stop_loss
        df_chart['close_logic'] = _close_logic
        df_chart['profit_target'] = _profit_target

        return df_chart


    def generate_chart_2(self,df_chart,line_colour):
        df_signal = df_chart.copy()
        df_signal = df_signal.dropna(subset=['action'])
        df_signal = df_signal.reset_index()
        signal_open_date = []
        signal_open_close = []
        signal_close_date = []
        signal_close_close = []
        signal_close_reason = []


        for i, row in df_signal.iterrows():
            if row['action'] == 'open':
                signal_open_date.append(df_signal.iloc[i]['date'])
                signal_open_close.append(df_signal.iloc[i]['close'])
                signal_close_date.append(df_signal.iloc[i + 1]['date'])
                signal_close_close.append(df_signal.iloc[i + 1]['close'])
                signal_close_reason.append(df_signal.iloc[i + 1]['action'])
            else:
                signal_open_date.append(df_signal.iloc[i - 1]['date'])
                signal_open_close.append(df_signal.iloc[i - 1]['close'])
                signal_close_date.append(df_signal.iloc[i]['date'])
                signal_close_close.append(df_signal.iloc[i]['close'])
                signal_close_reason.append(df_signal.iloc[i]['action'])

        df_signal['signal_open_date'] = signal_open_date
        df_signal['signal_open_close'] = signal_open_close
        df_signal['signal_close_date'] = signal_close_date
        df_signal['signal_close_close'] = signal_close_close
        df_signal['close_reason'] = signal_close_reason
        df_signal = df_signal.set_index('date')

        open_date = []
        open_close = []
        close_date = []
        close_close = []
        close_reason = []
        for i, row in df_chart.iterrows():
            try:
                open_date.append(df_signal.loc[row['date']].signal_open_date.strftime("%Y-%m-%d"))
            except:
                open_date.append(None)
            try:
                open_close.append(df_signal.loc[row['date']].signal_open_close)
            except:
                open_close.append(None)
            try:
                close_date.append(df_signal.loc[row['date']].signal_close_date.strftime("%Y-%m-%d"))
            except:
                close_date.append(None)
            try:
                close_close.append(df_signal.loc[row['date']].signal_close_close)
            except:
                close_close.append(None)
            try:
                close_reason.append(df_signal.loc[row['date']].close_reason)
            except:
                close_reason.append(None)

        df_signal_final = pd.DataFrame()
        df_signal_final['open_date'] = open_date
        df_signal_final['open_close'] = open_close
        df_signal_final['close_date'] = close_date
        df_signal_final['close_close'] = close_close
        df_signal_final['close_reason'] = close_reason
        df_signal_final['pctchange'] = ((df_signal_final['close_close'] - df_signal_final['open_close']) /
                                        df_signal_final['open_close']) * 100
        df_signal_final.open_close = df_signal_final.open_close.round(2)
        df_signal_final.close_close = df_signal_final.close_close.round(2)
        df_signal_final.pctchange = df_signal_final.pctchange.round(2)

        hover_template = "<br>".join([
            "Close Reason: %{customdata[4]}",
            "Open Date: %{customdata[0]}",
            "Close Date: %{customdata[2]}",
            "Open Close: %{customdata[1]}",
            "Close Close: %{customdata[3]}",
            "Pct Change: %{customdata[5]}%",
        ])


        fig_line = px.line(df_chart, x='date', y="equity_value")
        fig_line.update_traces(line_color='rgba(0, 0, 0, 0)')
        fig_line.update_xaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
        fig_line.update_yaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
        fig_line.add_trace(go.Scatter(mode='lines', hoverinfo='skip',
                                      x=df_chart['date'], y=df_chart['equity_value'],
                                      line=dict(color=line_colour, width=1), name='Strategy Equity'), )
        fig_line.add_trace(go.Scatter(mode='lines', hoverinfo='skip',
                                      x=df_chart['date'], y=df_chart['bah'],
                                      line=dict(color='#00FFFF', width=1), name='BnH Equity'), )
        fig_line.update_layout(plot_bgcolor=self.chart_bg, paper_bgcolor=self.chart_bg, height=220,
                               margin=dict(l=85, r=25, t=25, b=0),
                               font={"color": "white", 'size': 9}, yaxis={'title': 'Equity'},
                               xaxis={'title': ''}
                               )
        fig_line.add_trace(go.Scatter(mode='markers', customdata=df_signal_final, hovertemplate=hover_template,
                                      x=df_chart['date'], y=df_chart['open'], visible='legendonly',
                                      marker=dict(color='rgba(0, 0, 0, 0)', size=8,
                                                  line=dict(color='yellow', width=1.5)), name='open'), )
        fig_line.add_trace(go.Scatter(mode='markers', customdata=df_signal_final, hovertemplate=hover_template,
                                      x=df_chart['date'], y=df_chart['close_logic'], visible='legendonly',
                                      marker=dict(color='rgba(0, 0, 0, 0)', size=8,
                                                  line=dict(color='green', width=1.5)), name='close_logic'), )
        fig_line.add_trace(go.Scatter(mode='markers', customdata=df_signal_final, hovertemplate=hover_template,
                                      x=df_chart['date'], y=df_chart['profit_target'], visible='legendonly',
                                      marker=dict(color='rgba(0, 0, 0, 0)', size=8,
                                                  line=dict(color='red', width=1.5)), name='profit_target'), )
        fig_line.add_trace(go.Scatter(mode='markers', customdata=df_signal_final, hovertemplate=hover_template,
                                      x=df_chart['date'], y=df_chart['stop_loss'], visible='legendonly',
                                      marker=dict(color='rgba(0, 0, 0, 0)', size=8,
                                                  line=dict(color='blue', width=1.5)), name='stop_loss'), )

        fig_line.update_layout(xaxis_range=[df_chart.iloc[0].date, df_chart.iloc[-1].date])

        return fig_line



    def generate_subchart(self,df_chart, element, line_type, line_color):
        if line_type == 'bar':
            fig = go.Figure(
                data=[
                    go.Bar(hoverinfo='skip', x=df_chart['date'], y=df_chart[element], showlegend=True,
                           marker_color=line_color, marker_line_color=line_color, name=element),
                ])
            fig.update_layout(width=683)
        else:
            fig = go.Figure(data=[
                go.Scatter(mode='lines', hoverinfo='skip', x=df_chart['date'], y=df_chart[element], showlegend=True,
                           line=dict(color=line_color, width=1.5), name=element), ] )
            fig.update_layout(width=670)
        fig.update_layout(plot_bgcolor='#1f2c56', paper_bgcolor='#1f2c56', height=60,
                          margin=dict(l=85, r=50, t=5, b=20),
                          font={"color": "white",'size': 9}, yaxis={'fixedrange': True}, xaxis={'fixedrange': True},
                          bargap=0, )
        fig.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#1f2c56', )
        fig.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#626567', mirror=True)

        return fig


    def generate_histogram(self, df, period):
        chart_bg = self.chart_bg
        col_pct = 'pct_change_' + str(period)
        col_rise = 'max_rise_' + str(period)
        col_fall = 'max_fall_' + str(period)
        df_his = df.copy()
        df_his[col_pct] = df_his['close'].pct_change(period)
        df_his[col_pct] = df_his[col_pct].shift(-1 * period)
        df_his[col_pct] = df_his[col_pct] * 100
        df_his[col_pct] = df_his[col_pct].map(lambda x: round(x, 2))
        df_his = df_his[df_his['action'] == 'open']

        df_his[col_rise] = (df_his['high'].rolling(period).max().shift(-1 * (period)) / df_his['close']) - 1
        df_his[col_fall] = (df_his['low'].rolling(period).min().shift(-1 * (period)) / df_his['close']) - 1

        df_his[col_rise] = df_his[col_rise] * 100
        df_his[col_fall] = df_his[col_fall] * 100

        df_his[col_rise] = df_his[col_rise].map(lambda x: round(x, 2))
        df_his[col_fall] = df_his[col_fall].map(lambda x: round(x, 2))

        df_his = df_his[['date'] + [col_pct, col_rise, col_fall]]

        margin = dict(l=5, r=5, t=5, b=5)
        h = 85
        w = 120
        f = {"color": "white", 'size': 8}

        fig_pct = go.Figure()
        fig_pct.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, height=h, width=w, margin=margin,
                              font=f, bargap=0.1)
        fig_pct.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#1f2c56', )
        fig_pct.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#626567', )
        fig_pct.add_trace(go.Histogram(x=df_his[col_pct], marker_color='Cyan'))

        fig_rise = go.Figure()
        fig_rise.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, height=h, width=w, margin=margin,
                               font=f, bargap=0.1)
        fig_rise.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#1f2c56', )
        fig_rise.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#626567', )
        fig_rise.add_trace(go.Histogram(x=df_his[col_rise], marker_color='Yellow'))

        fig_fall = go.Figure()
        fig_fall.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg, height=h, width=w, margin=margin,
                               font=f, bargap=0.1)
        fig_fall.update_xaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#1f2c56', )
        fig_fall.update_yaxes(showline=True, zeroline=False, linecolor='#979A9A', gridcolor='#626567', )
        fig_fall.add_trace(go.Histogram(x=df_his[col_fall], marker_color='Fuchsia'))

        return fig_pct, fig_rise, fig_fall

