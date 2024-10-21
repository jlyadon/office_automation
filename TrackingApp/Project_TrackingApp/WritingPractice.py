import pandas as pd
from datetime import datetime
from time import ctime
from time import strftime

track_df = pd.read_csv('TrackingList2.csv',index_col=0)

filename = f'newfile{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'
text = open(filename,'a')

text.write(f'This line was written {datetime.now().strftime("%m/%d/%Y, %H:%M")}\n')

for i in range(10):
    text.write(f'{track_df.iloc[i,0]}\n')
    text.write(f'   Client: {track_df.iloc[i,1]}\n')

text.close()