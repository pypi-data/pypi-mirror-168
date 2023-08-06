import pandas as pd
import datetime
import math
import numpy as np

from dash import Dash, dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

from .components import *

class Signals:
    # Settings
    chart_bg = '#1f2c56'

    def __new__(self, filename, output_folder, start_date, end_date, para_dict, generate_filepath, settings):

        chart_bg = self.chart_bg
        components = Components()
        empty_line_chart = components.empty_line_chart()
        radioitems_div = components.generate_radioitems(para_dict)
        period = settings['histogram_period']
        stat_ = ['---', '---', '---', '---', '---']

        app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO], suppress_callback_exceptions=True)

        app.layout = html.Div([

            html.Div(style={'height': '10px', }),

            html.Div(
                dbc.Row([

                    # Left Column
                    dbc.Col(html.Div([
                        html.Div(style={'height': '10px', }),

                        html.Div(id='radioitems_container',children=radioitems_div),

                    ],style={'padding':'0px','border-radius':'5px',
                             'padding-left':'50px','height': '704px',
                             'background-color':'rgba(0, 0, 0, 0)'})
                        ,style={'padding':'0',}, width=3),


                    # Right Column
                    dbc.Col(html.Div([

                        html.Div(style={'height': '5px', }),

                        html.Div(id='stat_area',
                                 children=components.update_stat_div(period, stat_, stat_, stat_),
                                 style={'padding': '5px 25px', 'border-radius': '5px', 'font-size': '13px',
                                        'padding-left': '40px', 'padding-right': '80px', 'text-align': 'center',
                                        'background-color': chart_bg}),

                        html.Div(style={'height': '5px', }),

                        html.Div([html.Div(html.Img(),style={'height':'5px'}),
                                  html.Div(id='chart_area',
                                           children=dcc.Graph(id='line_chart', figure=empty_line_chart)),

                                 ],style={'padding':'5px','border-radius':'5px',
                                          'padding-right': '25px',
                                          'background-color':chart_bg}),

                        html.Div(style={'height': '5px', }),

                        html.Div(id='hist_area', children=html.Div(),
                                 style={'padding': '5px', 'border-radius': '5px',
                                        'height': '323px',
                                         'padding-left': '50px', 'padding-right': '0px',
                                         'background-color': chart_bg}),

                    ]), style={'padding':'0','padding-left':'5px'}, width=9),
                ])
            ),

        ], style={'width':'1200px','margin':'auto','padding':'0px','color':'white'})

        @app.callback(
            Output('stat_area', 'children'),
            Output('line_chart', 'figure'),
            Output('hist_area', 'children'),
            State('stat_area', 'children'),
            State('line_chart', 'figure'),
            State('hist_area', 'children'),
            Input({'type': 'para_radioitems', 'index': ALL}, 'value'),
        )
        def display_output(stat_area, line_chart, hist_area, para_radioitems):

            if None in para_radioitems:
                return stat_area, line_chart, hist_area

            save_path = generate_filepath(
                py_filename=filename,
                output_folder=output_folder,
                start_date=start_date,
                end_date=end_date,
                para_dict=para_dict,
                para_combination=para_radioitems)

            df = pd.read_csv(save_path)

            # Close Chart
            df_chart = df.copy()

            open_col = []
            for i, row in df_chart.iterrows():
                if row['logic'] == 'trade_logic':
                    open_col.append(row['close'])
                else:
                    open_col.append(None)

            df_chart['open_signal'] = open_col

            fig_line = go.Figure()
            fig_line.update_xaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
            fig_line.update_yaxes(showline=True, zeroline=False, linecolor='white', gridcolor='rgba(0, 0, 0, 0)')
            fig_line.add_trace(go.Scatter(mode='lines', hoverinfo='skip',
                                          x=df_chart['date'], y=df_chart['close'],
                                          line=dict(color='#00FFFF', width=1), name='Close'), )
            fig_line.update_layout(plot_bgcolor=self.chart_bg, paper_bgcolor=self.chart_bg, height=340,
                                   margin=dict(l=85, r=80, t=35, b=0),
                                   font={"color": "white", 'size': 9}, yaxis={'title': 'Close'},
                                   xaxis={'title': ''})
            fig_line.add_trace(go.Scatter(mode='markers',
                                          x=df_chart['date'], y=df_chart['open_signal'],
                                          marker=dict(color='rgba(0, 0, 0, 0)', size=8,
                                                      line=dict(color='yellow', width=1.5)), name='Signal'), )
            line_chart = fig_line


            # Histograms
            ## First column of the 5 charts
            title_list = [dbc.Col(width=1)]
            pct_list = [dbc.Col(html.Div('pct_change', style={'font-size': '12px', 'margin-top': '60px',
                                                              'margin-left': '40px',
                                                              'transform': 'rotate(-90deg)'}), width=1)]
            rise_list = [dbc.Col(html.Div('max_rise', style={'font-size': '12px', 'margin-top': '55px',
                                                              'margin-left': '40px',
                                                              'transform': 'rotate(-90deg)'}), width=1)]
            fall_list = [dbc.Col(html.Div('max_fall', style={'font-size': '12px', 'margin-top': '55px',
                                                              'margin-left': '40px',
                                                              'transform': 'rotate(-90deg)'}), width=1)]
            pct_mean = []
            rise_mean = []
            fall_mean = []

            for p in period:
                title_list.append(dbc.Col(f'{p} Days',style={'font-size': '12px', 'padding-left':'20px',
                                                             'text-align': 'center'},width=2))
                fig_pct, fig_rise, fig_fall = components.generate_histogram(df, p, 'signal')
                pct_list.append( dbc.Col(dcc.Graph(figure=fig_pct,config={'displayModeBar': False})
                                         ,style={'padding':'0'},width=2))
                rise_list.append(dbc.Col(dcc.Graph(figure=fig_rise,config={'displayModeBar': False})
                                         ,style={'padding': '0'}, width=2))
                fall_list.append(dbc.Col(dcc.Graph(figure=fig_fall,config={'displayModeBar': False})
                                         ,style={'padding': '0'}, width=2))

                stat_pct, stat_rise, stat_fall = components.generate_df_stat(df, p)
                pct_mean.append(stat_pct)
                rise_mean.append(stat_rise)
                fall_mean.append(stat_fall)


            title_list = html.Div(dbc.Row(title_list))
            pct_list = html.Div(dbc.Row(pct_list))
            rise_list = html.Div(dbc.Row(rise_list))
            fall_list = html.Div(dbc.Row(fall_list))

            hist_area = [html.Div(style={'height': '15px', }),
                         title_list,
                         html.Div(style={'height': '5px', }),
                         pct_list,
                         html.Div(style={'height': '5px', }),
                         rise_list, fall_list,
                         html.Div(style={'height': '15px', })]

            hist_style = {'padding': '5px', 'border-radius': '5px',
                          'padding-left': '50px','padding-right': '40px',
                          'background-color': chart_bg}


            stat_area = components.update_stat_div(period, pct_mean, rise_mean, fall_mean)



            return stat_area, line_chart, hist_area


        return app