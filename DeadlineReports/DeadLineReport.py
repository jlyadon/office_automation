import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import warnings

warnings.filterwarnings('ignore')

filepath = input('Filepath? ')

# The drag-and-drop feature for copying filepaths has some characters at the beginning and end.
if (filepath[0:3] == "& '") & (filepath[-1] == "'"):
    filepath = filepath[3:-1]

# The deadline month's name and number.
deadmo = input('Deadline month (name)? ')
deadmonum = str(input("Deadline month's number? "))
deadday = str(input("Deadline day's number? "))

# If it's a single-digit month, this line will kick in:
if len(deadmonum) == 1:
    deadmonum = '0' + deadmonum

now = dt.datetime.now()
today = str(now.day)
if len(today) == 1:
    today = '0' + today # Using 03 instead of 3 will keep the files in order by name so that Report_10-13... doesn't get put before Report_10-2...

if now.month < 10:
    month = '0' + str(now.month)
else:
    month = str(now.month)

hour = str(now.hour)
if len(hour) == 1:
    hour = '0' + hour # Again, using 08 instead of 8 for keeping files in order

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
xlims = (0,70)
if deadmonum == '10':
    xlims = (0,70) # I'll come back and adjust this as the month goes on and stop at 70 or something so people can see progress

graph_df.plot.barh(stacked=True,
                   x='Responsible Party',
                   y=['Remaining, not "e-File Awaiting..."','Remaining, "e-File Awaiting..."'],
                   figsize=(7.5,15),
                   title= deadmonum + '/' + deadday + ' Returns Remaining as of ' + hour + ':' + minute + ', ' + month + '/' + today,
                   color=['black','gray'],
                   xlim=xlims)

# An annotation for the October reports
if deadmonum == '10':
    plt.annotate('These numbers do not include 1041\ntasks.',
                 ((xlims[1] - 35),1.5))

# Save it.
plt.savefig(f'.\{deadmonum}-{deadday}-2024\BarChart_{month}-{today}_{hour}-{minute}.png',bbox_inches='tight')

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
report_df.to_excel(f'.\{deadmonum}-{deadday}-2024\Report_{month}-{today}_{hour}-{minute}.xlsx')

# I've got a macro to clean up the formatting in Excel.