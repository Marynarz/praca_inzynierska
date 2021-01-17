import math


def percent_to_radius(data, column_name):
    data['Radius'] = (data[column_name] / 100) * 360
    return data


def dataframe_to_radius(data, column_name):
    data['Percent'] = (data[column_name] / data[column_name].sum()) * 100
    return data


##
# @brief filter_negative_numbers - function to filter and remove negative numbers from dataframe
#
# @params
#     data - data to be filtered                                  (pandas.DataFrame)
#     column_name - name of column whichc should be filtered      (pandas.DataFrame.column.name)
#
# @return
#     pandas.Dataframe - filtered dataframe                       (pandas.DataFrame)
#
def filter_negative_numbers(data, column_name):
    filtered = data[column_name] > 0
    return data[filtered]
