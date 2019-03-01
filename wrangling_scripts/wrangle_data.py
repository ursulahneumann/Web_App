import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def cleandata(dataset, keepcolumns = ['Country', '1980', '2008'], value_variables = ['1980', '2008']):
    """Clean Gapminder cholesterol and BMI data for a visualizaiton dashboard

    Keeps data range of dates in keep_columns variable and data for the top 10 economies
    Reorients the columns into a year, country and value
    Saves the results to a csv file

    Args:
        dataset (str): name of the csv data file

    Returns:
        None

    """
    df = pd.read_csv(dataset)

    # Keep only the columns of interest (years and country name)
    df = df[keepcolumns]

    top10country = ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada']
    df = df[df['Country'].isin(top10country)]

    # melt year columns  and convert year to date time
    df_melt = df.melt(id_vars='Country', value_vars = value_variables)
    df_melt.columns = ['country','year', 'variable']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

    # output clean csv file
    return df_melt


def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    df_chol = cleandata('data/female_cholesterol.csv')
    df_BMI = cleandata('data/female_BMI.csv')

    # first chart plots cholesterol levels from 1980 to 2008 in top 10 economies
    # as a line chart
    graph_one = []
    df_chol.columns = ['country','year','cholesterol']
    countrylist = df_chol.country.unique().tolist()

    for country in countrylist:
      x_val = df_chol[df_chol['country'] == country].year.tolist()
      y_val =  df_chol[df_chol['country'] == country].cholesterol.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_one = dict(title = 'Cholesterol Levels Over Time',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Total Cholesterol (mmol/L)'),
                )

# second chart plots BMI from 1980 to 2008 in a line chart
    graph_two = []
    df_BMI.columns = ['country','year','BMI']
    #df_BMI.sort_values('BMI', ascending=False, inplace=True)
    countrylist = df_BMI.country.unique().tolist()

    for country in countrylist:
      x_val = df_BMI[df_BMI['country'] == country].year.tolist()
      y_val =  df_BMI[df_BMI['country'] == country].BMI.tolist()
      graph_two.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_two = dict(title = 'BMI Levels Over Time',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'BMI (kg/m^2)'),
                )


# third chart plots cholesterol vs BMI as a scatterplot
    graph_three = []
    df_BMI.columns = ['country','year','BMI']
    #df_BMI.sort_values('BMI', ascending=False, inplace=True)
    countrylist = df_BMI.country.unique().tolist()

    for country in countrylist:
      x_val = df_BMI[df_BMI['country'] == country].BMI.tolist()
      y_val =  df_chol[df_chol['country'] == country].cholesterol.tolist()
      graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'markers',
          name = country
          )
      )

    layout_three = dict(title = 'Cholesterol vs BMI Levels',
                xaxis = dict(title = 'Cholesterol (mmol/dL)'),
                yaxis = dict(title = 'BMI (kg/m^2)'),
                )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))

    return figures
