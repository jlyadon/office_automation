This will depend on how the tracking API works, but here's the plan:

import pandas as pd
import requests
will probably need to import datetime as well

# Load in info from the tracking CSV

tracking_df = pd.read_csv('TrackingList.csv')

# Send the numbers to the API

-- Will have to read documentation to see how this works--

# Save the response in a usable format (JSON)

response = requests.get(...)

# Make a list of packages delivered

Find the tracking number in the JSON
if {delivery status} == {delivered}:
    delivered_list.append({tracking number})

print('The following packages have been delivered:')
if delivered_list = []:
    print('None.')
else
    [print(f'{id}n/') for each id in delivered_list]

# If desired, save a file (highly recommended)

savelist = x
while savelist != 'y' and savelist != 'n':
    savelist = input(Would you like to save a list of them? (y/n)')
    If savelist == 'y':
        filename = f'deliveredlist{today's date}.txt'
        deliveredfile = open(f'deliveredlist{today's date}.txt', 'a')
        deliveredfile.write(
            f'Packages delivered as of {current date and time}:'
        )
        for id in delivered_list:
            delivered_file.write(f'n/{id}')
    elif savelist != 'y' and savelist != 'n':
        print('Please answer with the letter y for Yes or the letter n for No.')

# Remove delivered packages from the list

Input('Would you like to remove them from the tracking list? (y/n)')
If yes:
    for id in delivered_list:
        tracking_df.loc(id,'Tracking Nos.')
        Delete that row
