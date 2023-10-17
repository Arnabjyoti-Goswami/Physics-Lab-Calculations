# IMPORT DEPENDANCIES
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# FUNCTIONS
def take_input():
    st.title('Physics Lab Line of Best Fit Calculation, Error Analysis and Plotting')
    st.subheader('Enter your observed data: ')
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
        'x': x_values,
        'y': y_values
    }
    df = pd.DataFrame(data)
    df.set_index('S. No.', inplace=True)
    return df

def best_fit_line(df):
    x_bar = df['x'].mean()
    y_bar = df['y'].mean()

    df['(xᵢ - x̄)yᵢ'] = (df['x'] - x_bar) * df['y']
    df['(xᵢ - x̄)²'] = (df['x'] - x_bar) ** 2

    m = df['(xᵢ - x̄)yᵢ'].sum() / df['(xᵢ - x̄)²'].sum()
    c = y_bar - m * x_bar

    st.subheader('The required data for the line of best fit is: ')
    st.latex(r'\bar{x} = \textcolor{lightgreen}{' + str(x_bar) + '}')
    st.latex(r'\bar{y} = \textcolor{lightgreen}{' + str(y_bar) + '}')
    st.latex(r'm = \frac{\sum{(x_i-\bar{x})y_i}}{\sum{{(x_i-\bar{x})}^2}} = \textcolor{lightgreen}{' + str(m) + '}')
    st.latex(r'c = \bar{y} - m\bar{x} = \textcolor{lightgreen}{' + str(c) + '}')

    display_html_df(df)

    return {'x_bar': x_bar, 'y_bar': y_bar, 'm': m, 'c': c, 'df': df}

def find_errors(df, x_bar, m, c):
    df['Sᵢ²'] = (df['y'] - m * df['x'] - c) ** 2
    N = len(df)
    D = df['(xᵢ - x̄)²'].sum() 

    delta_m = df['Sᵢ²'].sum() / (D * (N-2))
    delta_m = delta_m ** 0.5

    delta_c = df['Sᵢ²'].sum() * ( (1/N) + ((x_bar ** 2) / D) )
    delta_c /= (N - 2)
    delta_c = delta_c ** 0.5

    st.subheader('The required data for the error analysis part is: ')
    st.latex(r'N = \textcolor{lightgreen}{' + str(N) + '}')
    st.latex(r'D = \textcolor{lightgreen}{' + str(D) + '}')
    st.latex(r'\Delta m \approx \sqrt{\frac{\sum{S_i^2}}{D(N-2)}} = \textcolor{lightgreen}{' + str(delta_m) + '}')
    st.latex(r'\Delta c \approx \sqrt{\left(\frac1N + \frac{\bar{x}^2}D\right)\frac{\sum{S_i^2}}{(N-2)}} = \textcolor{lightgreen}{' + str(delta_c) + '}')
    
    display_html_df(df)

    return df


def display_html_df(dataframe):
    # Get the index name
    index_name = dataframe.index.name if dataframe.index.name else 'Index'

    # Begin the HTML table
    html_table = '<table style="text-align: center; margin: 0 auto;">'

    # Add the table header with bold column headings, including the index name
    html_table += '<thead>'
    html_table += '<tr>'
    html_table += f'<th style="font-weight: bold;">{index_name}</th>'
    for column in dataframe.columns:
        html_table += f'<th style="font-weight: bold;">{column}</th>'
    html_table += '</tr>'
    html_table += '</thead>'

    # Add the table body with centered elements, including the index
    html_table += '<tbody>'
    for index, row in dataframe.iterrows():
        html_table += '<tr>'
        html_table += f'<td>{index}</td>'
        for value in row:
            html_table += f'<td>{value}</td>'
        html_table += '</tr>'
    html_table += '</tbody>'

    # Close the HTML table
    html_table += '</table>'

    # Display the HTML table in the Streamlit app
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown("") # Add a space of 1 line after the html table

def plot_graph(df, m, c):
    st.subheader('Plot and see the figure so that you can get an idea of the scale to choose for the graph')

    scatter = go.Scatter(x=df['x'], y=df['y'], mode='markers',  name='Data Points', marker=dict(color='red'))
    best_fit_line = go.Scatter(x=df['x'], y=m * df['x'] + c, mode='lines', name='Best-Fit Line', line=dict(color='blue'))

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
