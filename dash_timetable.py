import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def table(initial,day,hour,lecture):
    """Creates a dataframe with a default value of the
    initial variable, than fills the dataframe according
    to the list of triplets of day, hour and lecture."""

    df = pd.DataFrame(data=initial,columns=days,index=hours)
    lectures = zip(day,hour,lecture)
    for dd,hh,ll in lectures:
        df.loc[hh,dd] = ll
    return df

# assign a number to every lecture for the heatmap
lect_code = {'nnl':1,
             'qft':2,
             'jap':3,
             'qmo':4,
             'stats':5,
             'gs-nnl':1.1}
lect_Lname = {'nnl':'Nonlinear waves',
             'qft':'QFT',
             'jap':'Japanese',
             'qmo':'QM Optics',
             'stats':'Statistics',
             'gs-nnl':'GS - Nonlinear waves'}
lect_Hname = {'nnl':'Nonlinear waves',
             'qft':'Quantum Field Theory',
             'jap':'Japanese',
             'qmo':'Quantum Optics',
             'stats':'Applied Statistics',
             'gs-nnl':'Guided Study - Nonlinear waves'}

# range of the timetable
days = np.array(['Monday','Tuesday','Wednesday','Thursday',
        'Friday'])
hours = np.arange(9,19)

#############################################################

# input data for the timetable
# lecture days (I am aware of the clash)
lecture_days = np.array(['Monday','Thursday','Monday','Tuesday','Tuesday',
                'Tuesday','Wednesday','Thursday','Wednesday','Friday',
               'Thursday'])
lecture_hours = np.array([15,11,15,15,10,11,10,10,12,9,15])
lecture_vals = np.array([lect_code['nnl'],lect_code['nnl'],
                        lect_code['qft'],lect_code['qft'],
                        lect_code['jap'],lect_code['jap'],
                        lect_code['qmo'],lect_code['qmo'],
                        lect_code['stats'],lect_code['stats'],
                        lect_code['gs-nnl']])
# dataframe for displayed labels
"""lecture_name = np.array(['Nonlinear waves','Nonlinear waves','QFT','QFT','Japanese',
               'Japanese','QM Optics','QM Optics','Statistics','Statistics',
               'GS - Nonlinear waves'])"""
lecture_name = np.array([lect_Lname['nnl'],lect_Lname['nnl'],
                        lect_Lname['qft'],lect_Lname['qft'],
                        lect_Lname['jap'],lect_Lname['jap'],
                        lect_Lname['qmo'],lect_Lname['qmo'],
                        lect_Lname['stats'],lect_Lname['stats'],
                        lect_Lname['gs-nnl']])
# data for hovers
"""hover_name = np.array(['Nonlinear waves','Nonlinear waves','Quantum Field Theory',
              'Quantum Field Theory','Japanese','Japanese','Quantum Optics',
              'Quantum Optics','Applied Statistics','Applied Statistics',
              'Guided study - Nonlinear waves'])"""
hover_name = np.array([lect_Hname['nnl'],lect_Hname['nnl'],
                        lect_Hname['qft'],lect_Hname['qft'],
                        lect_Hname['jap'],lect_Hname['jap'],
                        lect_Hname['qmo'],lect_Hname['qmo'],
                        lect_Hname['stats'],lect_Hname['stats'],
                        lect_Hname['gs-nnl']])
lecture_theatre = np.array(['Physics West Library 125','Watson LT C','Aston Webb WG12',
                   'Aston Webb G33','Strahcona 113','Strahcona 113','Watson LT C',
                   'Physics West LT 117','Arts LT 2 (126)','Watson LT C',
                   'Law Board Room 220'])
lecture_weeks = np.array(['Spr 1-11','Spr 1-11','Spr 1-11','Spr 1-11','Spr 1-5,7-11',
                 'Spr 1-5,7-11','Spr 1-11','Spr 1-11','Spr 1-11','Spr 1-11',
                 'Spr 3,5,7,9,11'])

#############################################################

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(
        id='lecture-dropdown',
        options=[{'label':lect_Hname[i],'value':lect_code[i]} for i in lect_Hname.keys()],
        value=list(lect_code.values()),
        multi=True
        ),
    dcc.Graph(id='figure')
])

@app.callback(Output('figure','figure'),
             [Input('lecture-dropdown','value')])
def timetable_update(lects):
    lects = np.isin(lecture_vals,lects)
    # create numerical dataframe for heatmap and labels
    tt_numerical = table(0,lecture_days[lects],lecture_hours[lects],lecture_vals[lects])
    tt_labels = table('',lecture_days[lects],lecture_hours[lects],lecture_name[lects])

    # dataframe for hover labels
    hovers = [lecture + '<br>' + place + '<br>' + week for lecture,place,week in
              zip(hover_name[lects],lecture_theatre[lects],lecture_weeks[lects])]
    hover_labels = table('',lecture_days[lects],lecture_hours[lects],hovers)

    # custom colorscale
    colorscale=[[0.0, 'white'], [.2, 'green'],
                [.4, 'orange'], [.6, 'royalblue'],
                [.8, 'red'],[1.0, 'black']]

    # set up values for correct order
    x=tt_numerical.columns.tolist()
    y=(tt_numerical.index.tolist())[::-1]
    z = (tt_numerical.values.tolist())[::-1]
    text = (hover_labels.values.tolist())[::-1]
    annotation = (tt_labels.values.tolist())[::-1]

    # create annotated heatmap
    fig = ff.create_annotated_heatmap(x=x,
                                      y=y,
                                      z=z,
                                      text=text,
                                      hoverinfo='text',
                                      colorscale=colorscale,
                                      font_colors=['white'],
                                      annotation_text=annotation)
    # add title and reverse y-axis
    fig.layout.title = 'Spring Term Timetable'
    fig['layout']['yaxis']['autorange'] = "reversed"

    return fig

if __name__ == '__main__':
    app.run_server()
