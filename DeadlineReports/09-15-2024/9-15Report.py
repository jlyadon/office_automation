import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import warnings

warnings.filterwarnings('ignore')

filepath = input('Enter the file path for the search results from XCM (You can also drag the file here): ')

deadmonum = '9' # The deadline month's number. By naming it, we won't have to go through and change it in multiple places every month.
deadmo = 'September'

now = dt.datetime.now()
today = str(now.day)
month = str(now.month)
hour = str(now.hour)
minute = ''
if now.minute < 10:
    minute = '0' + str(now.minute)
else:
    minute = str(now.minute)

results_df = pd.read_excel(filepath)

# Build a dataframe for the bar graph
rp_list = results_df['Responsible Party'].unique()
count_list = []
ecount_list = []

for rp in rp_list:
    count = results_df[results_df['Responsible Party'] == rp][results_df['Current Status'] != 'eFile-Awaiting Taxpayer Consent Form']['Client/Entity Name'].count()
    ecount = results_df[results_df['Responsible Party'] == rp][results_df['Current Status'] == 'eFile-Awaiting Taxpayer Consent Form']['Client/Entity Name'].count()
    count_list.append(count)
    ecount_list.append(ecount)

graph_df = pd.DataFrame()
graph_df['Responsible Party'] = rp_list
graph_df['Remaining, not "e-File Awaiting..."'] = count_list
graph_df['Remaining, "e-File Awaiting..."'] = ecount_list
graph_df = graph_df.sort_values('Remaining, not "e-File Awaiting..."')

# Plot it!
graph_df.plot.barh(stacked=True,
                   x='Responsible Party',
                   y=['Remaining, not "e-File Awaiting..."','Remaining, "e-File Awaiting..."'],
                   figsize=(7.5,15),
                   title= deadmonum + '/15 Returns Remaining as of ' + hour + ':' + minute + ', ' + today + ' ' + deadmo,
                   color=['black','gray'],
                   xlim=(0,70))

# Save it.
plt.savefig(f'H:\{deadmonum}-15Reports2024\BarChart_{month}-{today}_{hour}-{minute}.png',bbox_inches='tight')

# Now, let's get a report ready for publishing.

report_df = pd.DataFrame(pd.pivot_table(
    results_df,
    values='Client/Entity Name',
    index='Responsible Party',
    columns='Current Status',
    aggfunc='count'
))

report_df = report_df.fillna('0')
report_df = report_df.astype(int) # Tried to fillna with integer 0s. Don't know why it didn't work. Need it to be integers to do some math below.

report_df['Total'] = report_df.sum(axis=1) # Sum the rows for each RP's total
report_df['Total w/o eFile-Awaiting...'] = report_df['Total'] - report_df['eFile-Awaiting Taxpayer Consent Form']

# Add a totals row at the bottom:
report_df.loc['TOTALS'] = report_df.sum()

# Remove the zeroes to make it easier to read:
report_df = report_df.replace(0,'')

# Save it:
report_df.to_excel(f'H:\{deadmonum}-15Reports2024\Report_{now.month}-{now.day}_{now.hour}-{now.minute}.xlsx')

# You can record a macro to clean up the formatting in Excel.