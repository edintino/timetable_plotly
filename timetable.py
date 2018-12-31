import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

# range of the timetable
days = ['Monday','Tuesday','Wednesday','Thursday',
        'Friday']
hours = np.arange(9,19)

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
lect_code = {'nonlinear':1,
             'qft':2,
             'jap':3,
             'qmo':4,
             'stats':5}

# input data for lectures (I am aware of the clash)
lecture_days = ['Monday','Thursday','Monday','Tuesday','Tuesday',
                'Tuesday','Wednesday','Thursday','Wednesday','Friday',
               'Thursday']
lecture_hours = [15,11,15,15,10,11,10,10,12,9,15]
lecture_vals = [lect_code['nonlinear'],lect_code['nonlinear'],
               lect_code['qft'],lect_code['qft'],
               lect_code['jap'],lect_code['jap'],
               lect_code['qmo'],lect_code['qmo'],
               lect_code['stats'],lect_code['stats'],
               lect_code['nonlinear']]
# create numerical dataframe for heatmap
tt_numerical = table(0,lecture_days,lecture_hours,lecture_vals)

# dataframe for displayed labels
lecture_name = ['Nonlinear waves','Nonlinear waves','QFT','QFT','Japanese',
               'Japanese','QM Optics','QM Optics','Statistics','Statistics',
               'GS - Nonlinear waves']
tt_labels = table('',lecture_days,lecture_hours,lecture_name)

# dataframe for hover labels
hover_name = ['Nonlinear waves','Nonlinear waves','Quantum Field Theory',
              'Quantum Field Theory','Japanese','Japanese','Quantum Optics',
              'Quantum Optics','Applied Statistics','Applied Statistics',
              'Guided study - Nonlinear waves']
lecture_theatre = ['Physics West Library 125','Watson LT C','Aston Webb WG12',
                   'Aston Webb G33','Strahcona 113','Strahcona 113','Watson LT C',
                   'Physics West LT 117','Arts LT 2 (126)','Watson LT C',
                   'Law Board Room 220']
lecture_weeks = ['Spr 1-11','Spr 1-11','Spr 1-11','Spr 1-11','Spr 1-5,7-11',
                 'Spr 1-5,7-11','Spr 1-11','Spr 1-11','Spr 1-11','Spr 1-11',
                 'Spr 3,5,7,9,11']
hovers = [lecture + '<br>' + place + '<br>' + week for lecture,place,week in
          zip(hover_name,lecture_theatre,lecture_weeks)]
hover_labels = table('',lecture_days,lecture_hours,hovers)

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

pyo.plot(fig,filename='schedule.html')
