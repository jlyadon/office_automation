import requests
import pandas as pd
from datetime import datetime as dt
from xml.etree import ElementTree as ET
from config import userid, password
from bs4 import BeautifulSoup

base_url = 'https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML='

tracking_df = pd.read_csv('TrackingList.csv',dtype={'Client Nos.':str})

# Build a list of delivered packages based on API calls and save it to a file:
delivered_list = []
rn = dt.now()
filename = 'Output\deliveredlist' + rn.strftime('%Y%m%d_%H%M') + '.txt'
deliveredfile = open(filename, 'a')
deliveredfile.write(
    'Packages delivered as of ' + rn.strftime('%d %B %Y, %H:%M') + ':\n'
)
for num in tracking_df['Tracking Nos.']:
    response = requests.get(base_url + \
                        f'<TrackRequest USERID="{userid}" PASSWORD="{password}">\
                            <TrackID ID="{num}"></TrackID>\
                                </TrackRequest>')
    soup = BeautifulSoup(response.content, 'xml')
    # Three different phrases might indicate that the package has reached the recipient:
    condition1 = 'Your item was delivered' in str(response.content)
    condition2 = 'Your item has been delivered' in str(response.content)
    condition3 = 'Your item was picked up' in str(response.content)

    if condition1 | condition2 | condition3:
        delivered_list.append(num)
        spot = tracking_df[tracking_df['Tracking Nos.'] == num].index[0]
        # NOTE: the above line is written with the assumption that exactly one row is returned. If the condition returns more than one index for a tracking number, the first will go into the varible.
        deliveredfile.write(f'\n{tracking_df.iloc[spot,0]}, {tracking_df.iloc[spot,1]}, {tracking_df.iloc[spot,2]}')
        deliveredfile.write('\n\n' + soup.TrackSummary.text + '\n')

# Print a list of the delivered packages to the terminal:
if len(delivered_list) == 0:
    print('No new packages have been delivered.')
    deliveredfile.write('\nNo packages delivered since last report.')
else:
    print('The following ' + str(len(delivered_list)) + ' packages have been delivered:')
    [print(f'{id}') for id in delivered_list]

deliveredfile.close()

# With the file written, ask about removing the packages from the list:
if len(delivered_list) != 0:
    removedelivered = 'x'
    while removedelivered.lower() != 'y' and removedelivered.lower() != 'n':
        removedelivered = input('Would you like to remove them from the tracking list? (y/n) ')
        if removedelivered == 'y':
            for id in delivered_list:
                tracking_df.drop(tracking_df[tracking_df['Tracking Nos.'] == id].index[0], inplace=True)
                # NOTE: the above line is written with the assumption that exactly one row is returned. If the condition returns more than one index for a tracking number, only the first will be deleted.
            tracking_df.to_csv('Output\TrackingList' + rn.strftime('%Y%B%d_%H%M') + '.csv',index=False)
            tracking_df.to_csv('TrackingList.csv',index=False)
        elif removedelivered != 'y' and removedelivered != 'n':
            print('Please answer with the letter y for Yes or the letter n for No.')