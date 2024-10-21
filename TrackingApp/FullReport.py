import requests
import pandas as pd
from datetime import datetime as dt
from config import userid, password
from bs4 import BeautifulSoup

# Initialize some stuff:
base_url = 'https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML='
tracking_df = pd.read_csv('TrackingList.csv',dtype={'Client Nos.':str})
track_list = list(tracking_df['Tracking Nos.'])
delivered_list = []
rn = dt.now() # rn for 'right now'
filename = 'Output\comprehensivelist' + rn.strftime('%Y%m%d_%H%M') + '.txt'
comprehensivefile = open(filename,'a')
comprehensivefile.write('\n\nALL PACKAGES LIST FOR ' + dt.strftime(rn,'%d %B %Y %H:%M') + ':\n\n')

# We'll use these to split it up into groups of 35 or fewer for USPS's API:
length = len(track_list)
fullbatches = int(length/35) # int() always rounds down

# Make the call for each list, write the file, and build the list:
for i in range(fullbatches + 1):

    # Slice our tracking list down to 35 or fewer, per the rules of the USPS tracking API:
    if i == fullbatches + 1: # This if will trigger the last time through the loop, when we have fewer than 35 packages remaining.
        batch_list = track_list[35*fullbatches : length]
    else:
        batch_list = track_list[35*i : 35*(i+1)]

    # Build a call URL for the batch list:
    call_url = base_url + f'<TrackRequest USERID="{userid}" PASSWORD="{password}">'
    for number in batch_list:
        call_url += f'<TrackID ID="{number}"></TrackID>'
    call_url += '</TrackRequest>'

    # Make the API call for the current batch and save the response:    
    response = requests.get(call_url)
    soup = BeautifulSoup(response.content, 'xml')
    
    # Interpret the xml to make a list of delivered packages for the current batch
    for number in pd.Series(batch_list).drop_duplicates(): # only do the unique tracking numbers because the possibility of multiple packages with the same number is taken care of on lines 53 & 54
        summary = soup.find('TrackInfo', ID=number).find('TrackSummary')

        if summary != None: # Not every package gets a summary, i.e. 'label created, not yet in system.' Every delivered package will get one, though.

            # Three different phrases might indicate that the package has reached the recipient:
            condition1 = 'Your item was delivered' in summary.text
            condition2 = 'Your item has been delivered' in summary.text
            condition3 = 'Your item was picked up' in summary.text

            if condition1 | condition2 | condition3:
                delivered_list.append(number)
                spots = tracking_df[tracking_df['Tracking Nos.'] == number].index
                for spot in spots: # Usually, there will only be one spot in spots. Occassionally, we will have multiple client numbers associated with one tracking number. Hence, the list
                    comprehensivefile.write(
                        f'{tracking_df.iloc[spot,0]}, {tracking_df.iloc[spot,1]}, {tracking_df.iloc[spot,2]}\n'
                    )
                    comprehensivefile.write(f'{summary.text}\n\n')


# Print a list of the delivered packages to the terminal:
if len(delivered_list) == 0:
    print('No new packages have been delivered.')
    comprehensivefile.write('\nNo packages delivered since last report.')
else:
    print('The following ' + str(len(delivered_list)) + ' packages have been delivered:')
    [print(f'{id}') for id in delivered_list]
    
comprehensivefile.close()

# With the file written, ask about removing the packages from the list:
if len(delivered_list) != 0:
    removedelivered = 'x'
    while removedelivered.lower() != 'y' and removedelivered.lower() != 'n':
        removedelivered = input('Would you like to remove them from the tracking list? (y/n) ')
        if removedelivered == 'y':
            for id in delivered_list:
                spots = tracking_df[tracking_df['Tracking Nos.'] == id].index
                for spot in spots:
                    tracking_df.drop(spot, inplace=True) # In most cases, there will only be one spot in spots.
            tracking_df.to_csv('Output\TrackingList' + rn.strftime('%Y%B%d_%H%M') + '.csv',index=False)
            tracking_df.to_csv('TrackingList.csv',index=False)
        elif removedelivered != 'y' and removedelivered != 'n':
            print('Please answer with the letter y for Yes or the letter n for No.')