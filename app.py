# IMPORT DEPENDANCIES
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# FUNCTIONS
def take_input():
    st.title('Physics Lab Line of Best Fit Calculation, Error Analysis and Plotting')
    num_points = st.text_input('Enter the number of data points observed: ', placeholder='2')

    x_values_input = st.text_input('Enter X values separated by spaces: ', placeholder='1 2')
    y_values_input = st.text_input('Enter Y values separated by spaces: ', placeholder='3 5')

    return num_points, x_values_input, y_values_input

def convert_input_to_df(num_points, x_values_input, y_values_input):
    # Split the input values by spaces and convert to a list of strings
    x_values = x_values_input.split()
    y_values = y_values_input.split()
    # Convert the lists of strings to lists of floats
    x_values = [float(x) for x in x_values]
    y_values = [float(y) for y in y_values]
    # Also convert number of data points from a string to int
    num_points = int(num_points)

    data = {
        'S. No.': list(range(1, num_points + 1)),
        'X': x_values,
        'Y': y_values
    }
    df = pd.DataFrame(data)
    df.set_index('S. No.', inplace=True)
    return df

def best_fit_line(df):
    x_bar = df['X'].mean()
    y_bar = df['Y'].mean()

    df['(x_i - x_bar) * yi'] = (df['X'] - x_bar) * df['Y']
    df['(x_i - x_bar)^2'] = (df['X'] - x_bar) ** 2

    m = df['(x_i - x_bar) * yi'].sum() / df['(x_i - x_bar)^2'].sum()
    c = y_bar - m * x_bar

    st.subheader('The required data for the line of best fit is: ')
    st.write('x_bar = ', x_bar)
    st.write('y_bar = ', y_bar)
    st.write('m = ', m)
    st.write('c = ', c, '\n\n')
    st.write(df)
    return {'x_bar': x_bar, 'y_bar': y_bar, 'm': m, 'c': c, 'df': df}

def find_errors(df, x_bar, m, c):
    df['(S_i)^2'] = (df['Y'] - m * df['X'] - c) ** 2
    N = len(df)
    D = df['(x_i - x_bar)^2'].sum() 

    delta_m = df['(S_i)^2'].sum() / (D * (N-2))
    delta_m = delta_m ** 0.5

    delta_c = df['(S_i)^2'].sum() * ( (1/N) + ((x_bar ** 2) / D) )
    delta_c /= (N - 2)
    delta_c = delta_c ** 0.5

    st.subheader('The required data for the error analysis part is: ')
    st.write('N = ', N)
    st.write('D = ', D)
    st.write('delta_m = ', delta_m)
    st.write('delta_c = ', delta_c, '\n\n')
    st.write(df)
    return df

def plot_graph(df, m, c):
    st.subheader('Plot and see the figure so that you can get an idea of the scale to choose for the graph')

    scatter = go.Scatter(x=df['X'], y=df['Y'], mode='markers',  name='Data Points', marker=dict(color='red'))
    best_fit_line = go.Scatter(x=df['X'], y=m * df['X'] + c, mode='lines', name='Best-Fit Line', line=dict(color='blue'))

    layout = go.Layout(
        title = {'text': 'Scatter Plot with Best-Fit Line','x': 0.35, 'y': 0.95, 'font': {'size': 19, 'color': 'black', 'family': 'Arial-Bold'}},

        # axis-label, label-style, tick-label-styles (numbers along the axis) are the arguments of the dictionary being passed
        xaxis = dict(title='X', titlefont=dict(size=17, color='black', family='Arial-Bold'), tickfont=dict(size=14, color='black')), 
        yaxis = dict(title='Y', titlefont=dict(size=17, color='black', family='Arial-Bold'), tickfont=dict(size=14, color='black')),

        autosize=False ,
        width = 1000, height=800, margin=dict(l=100, r=50, b=100, t=100, pad=5), # can change width or height according to the plot you want to make
        paper_bgcolor = 'LightSteelBlue',
        plot_bgcolor ='white' # To prevent the plot from changing with Streamlit's dark mode
    )
    fig = go.Figure(data=[scatter, best_fit_line], layout=layout)
    st.plotly_chart(fig)


# APP:
num_points, x_values_input, y_values_input = take_input()
if st.button('Submit'):
    df = convert_input_to_df(num_points, x_values_input, y_values_input)

    line_data = best_fit_line(df)
    x_bar, y_bar, m, c, df = (line_data['x_bar'], line_data['y_bar'], line_data['m'], line_data['c'], line_data['df'])
    
    find_errors(df, x_bar, m, c)

    plot_graph(df, m, c)
