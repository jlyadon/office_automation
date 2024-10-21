import pandas as pd
from datetime import datetime as dt
from datetime import timedelta

filename = input('What is the name of the file? It must be in your downloads folder in your H drive. ')

AP_df = pd.read_excel(f'H:\Downloads\{filename}')
Pickup_df = AP_df[['Client/Entity Name','Task Type','Number','Last Move Date','Responsible Party']]

today = dt.today()
one_week = timedelta(days=7)
two_weeks = timedelta(days=14)

Pickup_df['DateObject'] = pd.to_datetime(Pickup_df['Last Move Date'])

two_weeks_df = Pickup_df[Pickup_df['DateObject'] <= (today - two_weeks)]

one_week_df = Pickup_df[Pickup_df['DateObject'] <= (today - one_week)]
one_week_df = Pickup_df[Pickup_df['DateObject'] > (today - two_weeks)]

two_weeks_df[['Client/Entity Name','Task Type','Number','Last Move Date','Responsible Party']]\
    .to_csv('Output\TwoWeeksList_' + dt.strftime(dt.now(),'%y_%m_%d-%H_%M') +'.csv',index=False)
one_week_df[['Client/Entity Name','Task Type','Number','Last Move Date','Responsible Party']]\
    .to_csv('Output\OneWeekList_' + dt.strftime(dt.now(),'%y_%m_%d-%H_%M') +'.csv',index=False)