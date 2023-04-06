from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def dashboard():
    app = Dash(__name__)

    colors = {
        'background': '#ADD8E6',
        'text': '#111111'
    }

    # 'Unique Users', 'User Type', 'Cycles'
    user_cycle_df = pd.read_csv('user_cycle.csv')
    # 'Equipment', 'Unique Users'
    unique_user_equipment_df = pd.read_csv('unique_user_equipment.csv').sort_values(by="Unique Users", ascending=False)
    # 'Equipment', 'Non Unique Users'
    non_unique_user_equipment_df = pd.read_csv('non_unique_user_equipment.csv').sort_values(by="Users", ascending=False)
    # 'Equipment', 'Cycles', 'Check Out Times'
    equipment_cycle_df = pd.read_csv('equipment_cycle.csv').sort_values(by="Equipment", ascending=False)

    # creating a dictionary because the equipment usertype dataframe isn't in the correct format
    equipment_usertype_dict = {'Equipment': [], 'User Type': [], 'Count': []}
    for i in range(len(unique_user_equipment_df['Equipment'])):
        user_list = unique_user_equipment_df["Unique Users"][i].split(', ')
        for j in user_list:

            if user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Staff':
                equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Staff')
                equipment_usertype_dict['Count'].append(1)

            elif user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Student':
                equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Student')
                equipment_usertype_dict['Count'].append(1)

            elif user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Contractor':
                equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Contractor')
                equipment_usertype_dict['Count'].append(1)

            elif user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Academia':
                equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Academia')
                equipment_usertype_dict['Count'].append(1)

            elif user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Faculty':
                equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Faculty')
                equipment_usertype_dict['Count'].append(1)

            else:
                equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Other')
                equipment_usertype_dict['Count'].append(1)

    # creating a dictionary because the non-unique equipment usertype dataframe isn't in the correct format
    non_unique_equipment_usertype_dict = {'Equipment': [], 'User Type': [], 'Count': []}
    for i in range(len(non_unique_user_equipment_df['Equipment'])):
        user_list = non_unique_user_equipment_df["Users"][i].split(', ')
        for j in user_list:

            if user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Staff':
                non_unique_equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                non_unique_equipment_usertype_dict['User Type'].append('Staff')
                non_unique_equipment_usertype_dict['Count'].append(1)

            elif user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Student':
                non_unique_equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                non_unique_equipment_usertype_dict['User Type'].append('Student')
                non_unique_equipment_usertype_dict['Count'].append(1)

            elif user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Faculty':
                non_unique_equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                non_unique_equipment_usertype_dict['User Type'].append('Faculty')
                non_unique_equipment_usertype_dict['Count'].append(1)

            else:
                non_unique_equipment_usertype_dict['Equipment'].append(unique_user_equipment_df["Equipment"][i])
                non_unique_equipment_usertype_dict['User Type'].append('Other')
                non_unique_equipment_usertype_dict['Count'].append(1)

    # turning the dictionary back into a dataframe and then sorting it (for top 5 and least 5)
    equipment_usertype_df = pd.DataFrame(data=equipment_usertype_dict)
    dfg_top = equipment_usertype_df.groupby(['Equipment']).size().to_frame().sort_values([0], ascending=False).head(
        5).reset_index()
    dfg_bottom = equipment_usertype_df.groupby(['Equipment']).size().to_frame().sort_values([0], ascending=True).head(
        5).reset_index()
    final_top_df = equipment_usertype_df.merge(dfg_top)
    final_bottom_df = equipment_usertype_df.merge(dfg_bottom).sort_values(by=0).reset_index()

    # turning the dictionary back into a dataframe and then sorting it (for non-unique use equipment)
    non_unique_equipment_usertype_df = pd.DataFrame(data=non_unique_equipment_usertype_dict)
    dfg = non_unique_equipment_usertype_df.groupby(['Equipment']).size().to_frame().sort_values(
        [0], ascending=False).reset_index()
    non_unique_final_df = non_unique_equipment_usertype_df.merge(dfg)

    # creating a dictionary for daily timeline because the equipment cycle dataframe isn't in the correct format
    equipment_cycle_dict = {'Time': [], 'Cycles': [], 'Equipment': []}
    for i in range(len(equipment_cycle_df['Equipment'])):
        check_out_time_list = equipment_cycle_df['Check Out Times'][i].split(', ')
        for j in check_out_time_list:
            try:
                index = equipment_cycle_dict['Time'].index(j, len(equipment_cycle_dict['Time']) - 1)
                if equipment_cycle_dict['Equipment'][index] != equipment_cycle_df['Equipment'][i]:
                    equipment_cycle_dict['Time'].append(j)
                    count = 0
                    for k in range(int(equipment_cycle_df['Cycles'][i])):
                        if check_out_time_list[k] == j:
                            count += 1
                    equipment_cycle_dict['Cycles'].append(count)
                    equipment_cycle_dict['Equipment'].append(equipment_cycle_df['Equipment'][i])
            except ValueError:
                equipment_cycle_dict['Time'].append(j)
                count = 0
                for k in range(int(equipment_cycle_df['Cycles'][i])):
                    test = check_out_time_list[k]
                    if test == j:
                        count += 1
                equipment_cycle_dict['Cycles'].append(count)
                equipment_cycle_dict['Equipment'].append(equipment_cycle_df['Equipment'][i])

    time_list = []
    for i in range(len(equipment_cycle_df['Equipment'])):
        check_out_time_list = equipment_cycle_df['Check Out Times'][i].split(', ')
        # check_out_list = ['01/09/2021', '01/09/2021', '01/09/2021', ...]
        for check_out_time in check_out_time_list:
            if check_out_time not in time_list:
                if len(time_list) == 0:
                    time_list.append(check_out_time)
                else:
                    added = False
                    for j in range(len(time_list) - 1, -1, -1):
                        if pd.to_datetime(time_list[j], dayfirst=True, format="%d/%m/%Y").isoformat()[0:10] \
                                < pd.to_datetime(check_out_time, dayfirst=True, format="%d/%m/%Y").isoformat()[0:10]:
                            time_list.insert(j + 1, check_out_time)
                            added = True
                            break

                    if not added:
                        time_list.insert(0, check_out_time)

    # finds the index of the date in the list
    # index = equipment_cycle_dict['Time'].index(pd.to_datetime(j, dayfirst=True, format="%d/%m/%Y").isoformat()[0:10],
    #                                          len(equipment_cycle_dict['Time']) - 1)

    # if equipment_cycle_dict['Equipment'][index] != equipment_cycle_df['Equipment'][i]:
    #    equipment_cycle_dict['Time'].append(pd.to_datetime(j, dayfirst=True, format="%d/%m/%Y").isoformat()[0:10])
    #    count = 0
    #    for k in range(int(equipment_cycle_df['Cycles'][i])):
    #        if check_out_time_list[k] == j:
    #            count += 1
    #    equipment_cycle_dict['Cycles'].append(count)
    #    equipment_cycle_dict['Equipment'].append(equipment_cycle_df['Equipment'][i])

    # for i in range(len(equipment_cycle_dict['Time'])):
    #   equipment_cycle_dict['Time'][i] = pd.to_datetime(equipment_cycle_dict['Time'][i], format="%Y-%m-%d").strftime(
    #      "%d/%m/%Y")

    # creating a dictionary for monthly timeline because the equipment cycle dataframe isn't in the correct format
    equipment_cycle_dict2 = {'Time': [], 'Cycles': [], 'Equipment': []}
    for i in range(len(equipment_cycle_df['Equipment'])):
        check_out_time_list = equipment_cycle_df['Check Out Times'][i].split(', ')
        for j in check_out_time_list:
            try:
                index = equipment_cycle_dict2['Time'].index(j[3:10], len(equipment_cycle_dict2['Time']) - 1)
                if equipment_cycle_dict2['Equipment'][index] != equipment_cycle_df['Equipment'][i]:
                    equipment_cycle_dict2['Time'].append(j[3:10])
                    count = 0
                    for k in range(int(equipment_cycle_df['Cycles'][i])):
                        if check_out_time_list[k] == j[3:10]:
                            count += 1
                    equipment_cycle_dict2['Cycles'].append(count)
                    equipment_cycle_dict2['Equipment'].append(equipment_cycle_df['Equipment'][i])
            except ValueError:
                equipment_cycle_dict2['Time'].append(j[3:10])
                count = 0
                for k in range(int(equipment_cycle_df['Cycles'][i])):
                    test = check_out_time_list[k][3:10]
                    if test == j[3:10]:
                        count += 1
                equipment_cycle_dict2['Cycles'].append(count)
                equipment_cycle_dict2['Equipment'].append(equipment_cycle_df['Equipment'][i])

    # creating the graphs from the dataframes
    fig_pie_total = user_cycle_df.groupby('User Type').sum()
    fig_pie = px.pie(user_cycle_df, "User Type", "Cycles")
    fig_pie.update_layout(title_text='Total Cycles: ' + str(fig_pie_total['Cycles'].sum()))

    # top 5 bar graph
    fig_top_5_bar_total = final_top_df.groupby('Equipment').sum()
    fig_top_5_bar = px.histogram(final_top_df, x="Equipment", y='Count', color='User Type',
                                 color_discrete_map={
                                     'Student': px.colors.qualitative.Plotly[1],
                                     'Staff': px.colors.qualitative.Plotly[0],
                                     'Other': px.colors.qualitative.Plotly[3],
                                     'Faculty': px.colors.qualitative.Plotly[2],
                                     'Academia': px.colors.qualitative.Plotly[4],
                                     'Contractor': px.colors.qualitative.Plotly[5]})
    # label for total number of cycles
    fig_top_5_bar.add_trace(go.Scatter(x=fig_top_5_bar_total.index, y=fig_top_5_bar_total['Count'],
                                       text=fig_top_5_bar_total['Count'], mode='text',
                                       textposition='top center', textfont=dict(size=14), showlegend=False))
    fig_top_5_bar.update_xaxes(categoryorder='total descending')

    # least 5 bar graph
    fig_least_5_bar_total = final_bottom_df.groupby('Equipment').sum()
    print(fig_least_5_bar_total)
    fig_least_5_bar = px.histogram(final_bottom_df, x="Equipment", y='Count', color='User Type',
                                   color_discrete_map={'Student': px.colors.qualitative.Plotly[1],
                                                       'Staff': px.colors.qualitative.Plotly[0],
                                                       'Faculty': px.colors.qualitative.Plotly[2],
                                                       'Other': px.colors.qualitative.Plotly[3],
                                                       'Academia': px.colors.qualitative.Plotly[4],
                                                       'Contractor': px.colors.qualitative.Plotly[5]})
    # label for total number of cycles
    fig_least_5_bar.update_xaxes(categoryorder='total ascending')
    fig_least_5_bar.add_trace(go.Scatter(x=fig_least_5_bar_total.index, y=fig_least_5_bar_total['Count'],
                                         text=fig_least_5_bar_total['Count'], mode='text',
                                         textposition='top center', textfont=dict(size=14), showlegend=False))

    # non-unique equipment bar graph
    non_unique_equipment_bar_total = non_unique_final_df.groupby('Equipment').sum()
    fig_non_unique_equipment_bar = px.histogram(non_unique_final_df, x="Equipment", y='Count', color='User Type',
                                                color_discrete_map={'Student': px.colors.qualitative.Plotly[1],
                                                                    'Staff': px.colors.qualitative.Plotly[0],
                                                                    'Other': px.colors.qualitative.Plotly[3],
                                                                    'Faculty': px.colors.qualitative.Plotly[2],
                                                                    'Academia': px.colors.qualitative.Plotly[4],
                                                                    'Contractor': px.colors.qualitative.Plotly[5]})
    # label for total number of cycles
    fig_non_unique_equipment_bar.add_trace(go.Scatter(x=non_unique_equipment_bar_total.index,
                                                      y=non_unique_equipment_bar_total['Count'],
                                                      text=non_unique_equipment_bar_total['Count'], mode='text',
                                                      textposition='top center', textfont=dict(size=14),
                                                      showlegend=False))
    fig_non_unique_equipment_bar.update_xaxes(categoryorder='total descending')

    # daily timeline graph
    fig_daily_timeline_df = pd.DataFrame(equipment_cycle_dict)
    fig_daily_timeline_total = fig_daily_timeline_df.groupby('Time').sum()
    fig_time_cycle = px.bar(equipment_cycle_dict, x='Time', y='Cycles', color='Equipment',
                            color_discrete_sequence=px.colors.qualitative.Bold)
    # label for total number of cycles
    fig_time_cycle.add_trace(go.Scatter(x=fig_daily_timeline_total.index, y=fig_daily_timeline_total['Cycles'],
                                        text=fig_daily_timeline_total['Cycles'], mode='text',
                                        textposition='top center', textfont=dict(size=11),
                                        showlegend=False))
    fig_time_cycle.update_xaxes(categoryorder='array', categoryarray=time_list)

    # monthly timeline graph
    fig_monthly_timeline_df = pd.DataFrame(equipment_cycle_dict2)
    fig_monthly_timeline_total = fig_monthly_timeline_df.groupby('Time').sum()
    fig_time_cycle2 = px.histogram(equipment_cycle_dict2, x='Time', y='Cycles', color='Equipment',
                                   color_discrete_sequence=px.colors.qualitative.Bold)
    # label for total number of cycles
    fig_time_cycle2.add_trace(go.Scatter(x=fig_monthly_timeline_total.index, y=fig_monthly_timeline_total['Cycles'],
                                         text=fig_monthly_timeline_total['Cycles'], mode='text',
                                         textposition='top center', textfont=dict(size=14),
                                         showlegend=False))

    # graph layouts
    fig_pie.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    fig_top_5_bar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    fig_least_5_bar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    fig_non_unique_equipment_bar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    fig_time_cycle.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    fig_time_cycle2.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    # webpage layout
    app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children='Loaning Dashboard',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(children='User Type Pie Chart', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='pie-graph',
            figure=fig_pie
        ),

        html.Div(children='5 Most Used Equipment', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='top-5-graph',
            figure=fig_top_5_bar),

        html.Div(children='5 Least Used Equipment', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='least-5-graph',
            figure=fig_least_5_bar),

        html.Div(children='Used Equipment by non-unique Users', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='non_unique_equipment_bar',
            figure=fig_non_unique_equipment_bar),

        html.Div(children='Daily Equipment Timeline', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='-cycle-timeline-graph',
            figure=fig_time_cycle),

        html.Div(children='Monthly Equipment Timeline', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='monthly-timeline-graph',
            figure=fig_time_cycle2)

    ])

    app.run(debug=True)


if __name__ == "__main__":
    dashboard()
