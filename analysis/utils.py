import plotly.express as px
import numpy as np

def preprocess_data(df):
    """
    some quick and dirty data preprocessing
    """
    df['trialtime'] = df['timestamp'].sub( df.groupby('trial_number')['timestamp'].transform('first'))/1_000_000_000
    df['delta_ts'] = df['trialtime'] - df['trialtime'].shift(1)
    df = df.dropna()
    df.loc[:,'animal_lab_heading'] = np.unwrap(df.loc[:,'animal_lab_heading'] )
    df['animal_rotation'] = (df['animal_lab_heading'] - df['animal_lab_heading'].shift(1)) / df['delta_ts']
    df['animal_velocity'] = np.sqrt((df['integrated_lab_x'] - df['integrated_lab_x'].shift(1))**2
        + (df['integrated_lab_y'] - df['integrated_lab_y'].shift(1))**2)  * df['delta_ts'] * 10000  * 4.5
    df['animal_straight'] = df['d_lab_y'] *4.5 / df['delta_ts']
    df = df.dropna()
    df['animal_velocity_15'] = df['animal_velocity'].rolling(15, min_periods=1, center=True).mean()
    df['animal_velocity_50'] = df['animal_velocity'].rolling(50, min_periods=1, center=True).mean()
    df['animal_straight_15'] = df['animal_straight'].rolling(15, min_periods=1, center=True).mean()
    df['animal_rotation_15'] = df['animal_rotation'].rolling(15, min_periods=1, center=True).mean()
    return df



def plot_rotation_per_trial(df):
    fig = px.line(df
        , x='trialtime'
        , y='animal_rotation_15'
        , facet_col='trial_number'
        , facet_col_wrap=4
        , labels = {
            'trialtime': 'Trial time (s)'
          , 'animal_rotation_15': 'rotation (rad/s)'
          , 'trial_number': 'Trial'
        }
        , title="Animal rotation per trial"
        , color='direction'
        , width=1200
        , height=800)
    return fig

def plot_velocity_per_trial(df):
    fig = px.line(df
        , x='trialtime'
        , y='animal_velocity_15'
        , facet_col='trial_number'
        , facet_col_wrap=4
        , labels = {
            'trialtime': 'Trial time (s)'
          , 'animal_velocity_15': 'v (mm/s)'
          , 'trial_number': 'Trial'
        }
        , color_discrete_sequence=["#CCCC00"]
        , title="Animal velocity per Trial"
        , width=1200
        , height=800)
    fig.update_yaxes(range=[0,50])
    return fig

def plot_foward_movement_per_trial(df):
    fig = px.line(df
        , x='trialtime'
        , y='animal_straight_15'
        , facet_col='trial_number'
        , facet_col_wrap=4
        , labels = {
            'trialtime': 'Trial time (s)'
          , 'animal_straight_15': 'v_f (mm/s)'
          , 'trial_number': 'Trial'
        }
        , color_discrete_sequence=["#CC00CC"]
        , title="Forward movement per Trial"
        , width=1200
        , height=800)
    return fig

def plot_rotation_per_grating_group(df):
    df['trial_speed_deg_abs'] = df['trial_speed_deg'].abs()
    df['plot_group'] = df.groupby(['bar_deg', 'trial_speed_deg_abs'])['trial_number'].ngroup()

    fig = px.line(df
        , x='trialtime'
        , y='animal_rotation_15'
        , facet_col='plot_group'
        , facet_col_wrap=3
        , labels = {
            'trialtime': 'Trial time (s)'
          , 'animal_rotation_15': 'rotation (rad/s)'
          , 'trial_number': 'Trial'
        }
        , title="Animal rotation per grating group"
        , color='direction'
        , width=1200
        , height=800
        , line_group='trial_number')
    titles = ['22.5° bars @ 4Hz', '22.5° bars @ 8Hz', '22.5° bars @ 16Hz', '45° bars @ 4Hz', '45° bars @ 8Hz', '45° bars @ 16Hz']
    fig.for_each_annotation(lambda a: a.update(text=titles[int(a.text.split("=")[-1])]))
    return fig

def plot_velocity_per_grating_group(df):
    df['trial_speed_deg_abs'] = df['trial_speed_deg'].abs()
    df['plot_group'] = df.groupby(['bar_deg', 'trial_speed_deg_abs'])['trial_number'].ngroup()

    fig = px.line(df
        , x='trialtime'
        , y='animal_velocity_15'
        , facet_col='plot_group'
        , facet_col_wrap=3
        , labels = {
            'trialtime': 'Trial time (s)'
          , 'animal_velocity_15': 'v (mm/s)'
          , 'trial_number': 'Trial'
        }
        , title="Animal rotation per grating group"
        , color='direction'
        , width=1200
        , height=800
        , line_group='trial_number')
    titles = ['22.5° bars @ 4Hz', '22.5° bars @ 8Hz', '22.5° bars @ 16Hz', '45° bars @ 4Hz', '45° bars @ 8Hz', '45° bars @ 16Hz']
    fig.for_each_annotation(lambda a: a.update(text=titles[int(a.text.split("=")[-1])]))
    fig.update_yaxes(range=[0,80])
    return fig

def _add_multiples(lst):
    lst = np.append(lst, np.array(lst) + 48)
    lst = np.append(lst, np.array(lst) + 2*48)
    lst = np.append(lst, np.array(lst) + 3*48)
    return lst

def plot_rotation_per_smallfield_group(df):
    df['trial_speed_deg_abs'] = df['trial_speed_deg'].abs()

    grp1 = [i for i in range(1,7)]
    grp1 = _add_multiples(grp1)

    grp2 = [i for i in range(7,13)]
    grp2 = _add_multiples(grp2)
    grp3 = [i for i in range(13,19)]
    grp3 = _add_multiples(grp3)
    grp4 = [i for i in range(19,25)]
    grp4 = _add_multiples(grp4)
    
    grp5 = [i for i in range(25,31)]
    grp5 = _add_multiples(grp5)
    grp6 = [i for i in range(31,37)]
    grp6 = _add_multiples(grp6)
    grp7 = [i for i in range(37,43)]
    grp7 = _add_multiples(grp7)
    grp8 = [i for i in range(43,49)]
    grp8 = _add_multiples(grp8)


    df.loc[df['trial_number'].isin(grp1), 'plot_group'] = 1
    df.loc[df['trial_number'].isin(grp2), 'plot_group'] = 2
    df.loc[df['trial_number'].isin(grp3), 'plot_group'] = 3
    df.loc[df['trial_number'].isin(grp4), 'plot_group'] = 4

    df.loc[df['trial_number'].isin(grp5), 'plot_group'] = 5
    df.loc[df['trial_number'].isin(grp6), 'plot_group'] = 6
    df.loc[df['trial_number'].isin(grp7), 'plot_group'] = 7
    df.loc[df['trial_number'].isin(grp8), 'plot_group'] = 8

    fig = px.line(df
        , x='trialtime'
        , y='animal_rotation_15'
        , facet_col='plot_group'
        , facet_col_wrap=4
        , labels = {
            'trialtime': 'Trial time (s)'
          , 'animal_rotation_15': 'rotation (rad/s)'
          , 'trial_number': 'Trial'
        }
        , title="Animal rotation per grating group"
        , color='direction'
        , width=1200
        , height=800
        , line_group='trial_number')
    titles = ['bars @ 2Hz', 'bars @ 3Hz', 'bars @ 4Hz', 'bars @ 8Hz', 'object @ 2Hz', 'object @ 3Hz', 'object @ 4Hz', 'object @ 8Hz',]
    fig.for_each_annotation(lambda a: a.update(text=titles[round(float(a.text.split("=")[-1]))-1]))
    fig.update_xaxes(matches=None)
    return fig

def plot_velocity_per_smallfield_group(df):
    df['trial_speed_deg_abs'] = df['trial_speed_deg'].abs()

    grp1 = [i for i in range(1,7)]
    grp1 = _add_multiples(grp1)

    grp2 = [i for i in range(7,13)]
    grp2 = _add_multiples(grp2)
    grp3 = [i for i in range(13,19)]
    grp3 = _add_multiples(grp3)
    grp4 = [i for i in range(19,25)]
    grp4 = _add_multiples(grp4)
    
    grp5 = [i for i in range(25,31)]
    grp5 = _add_multiples(grp5)
    grp6 = [i for i in range(31,37)]
    grp6 = _add_multiples(grp6)
    grp7 = [i for i in range(37,43)]
    grp7 = _add_multiples(grp7)
    grp8 = [i for i in range(43,49)]
    grp8 = _add_multiples(grp8)


    df.loc[df['trial_number'].isin(grp1), 'plot_group'] = 1
    df.loc[df['trial_number'].isin(grp2), 'plot_group'] = 2
    df.loc[df['trial_number'].isin(grp3), 'plot_group'] = 3
    df.loc[df['trial_number'].isin(grp4), 'plot_group'] = 4

    df.loc[df['trial_number'].isin(grp5), 'plot_group'] = 5
    df.loc[df['trial_number'].isin(grp6), 'plot_group'] = 6
    df.loc[df['trial_number'].isin(grp7), 'plot_group'] = 7
    df.loc[df['trial_number'].isin(grp8), 'plot_group'] = 8

    fig = px.line(df
        , x='trialtime'
        , y='animal_velocity_50'
        , facet_col='plot_group'
        , facet_col_wrap=4
        , labels = {
            'trialtime': 'Trial time (s)'
          , 'animal_velocity_15': 'v (mm/s)'
          , 'trial_number': 'Trial'
        }
        , title="Animal velocity per grating group"
        , color='direction'
        , width=1200
        , height=800
        , line_group='trial_number')
    titles = ['bars @ 2Hz', 'bars @ 3Hz', 'bars @ 4Hz', 'bars @ 8Hz', 'object @ 2Hz', 'object @ 3Hz', 'object @ 4Hz', 'object @ 8Hz',]
    fig.for_each_annotation(lambda a: a.update(text=titles[round(float(a.text.split("=")[-1]))-1]))
    fig.update_xaxes(matches=None)
    fig.update_yaxes(range=[0,80])
    return fig