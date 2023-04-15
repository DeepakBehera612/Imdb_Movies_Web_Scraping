import json
import pandas as pd

f = open('demo.json')
  

data = json.load(f)
  

for i in data['employee_details']:
    
    df = pd.DataFrame(i, index=[0])
    
    
    # print(df.groupby(['department_id', 'balance']))

    df['Sum'] = df['balance'].sum()
    print(df)

f.close()