import pandas as pd
list3 = []
for i in range(46):
    if i % 5 == 0 and i % 3 == 0:
        list3.append('Fizzbuzz')
    elif i % 5 == 0:
        list3.append('Buzz')
    elif i % 3 == 0:
        list3.append('Fizz')
    else:
        list3.append('')
frame3_df = pd.DataFrame(list3,columns=['Fizzbuzz value'])
frame3_df.to_csv('FizzbuzzSheet.csv',index=True)