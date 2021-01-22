import copy


##
# @brief percent_to_radius - count percent value to radians
#
# @params
#     data - data to be filtered                                  (pandas.DataFrame)
#     column_name - name of column which should be counted        (pandas.DataFrame.column.name)
#
# @return
#     pandas.Dataframe - counted dataframe                        (pandas.DataFrame)
#
def percent_to_radius(data, column_name):
    data['Radius'] = round((data[column_name] / 100) * 360, 2)
    return data


##
# @brief dataframe_to_radius - count data frame to radians
#
# @params
#     data - data to be filtered                                  (pandas.DataFrame)
#     column_idx - index of column which should be counted        (pandas.DataFrame.column.name)
#
# @return
#     pandas.Dataframe - counted dataframe                        (pandas.DataFrame)
#
def dataframe_to_radius(data, column_idx):
    ret_data = copy.deepcopy(data)
    ret_data['Percent'] = round((data[data.columns[column_idx]] / data[data.columns[column_idx]].sum()) * 100, 2)
    return percent_to_radius(ret_data, 'Percent')


##
# @brief filter_negative_numbers - function to filter and remove negative numbers from dataframe
#
# @params
#     data - data to be filtered                                  (pandas.DataFrame)
#     column_idx- index of column which should be filtered        (pandas.DataFrame.column.name)
#
# @return
#     pandas.Dataframe - filtered dataframe                       (pandas.DataFrame)
#
def filter_negative_numbers(data, column_idx):
    filtered = data[data.columns[column_idx]] > 0
    return data[filtered]
