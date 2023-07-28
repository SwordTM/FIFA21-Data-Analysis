import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

raw_data = pd.read_csv("fifa21_raw_data.csv")
raw_data.columns

# Leading Questions in the cleaning phase
# 1. Do the height and weight columns have the appropriate data types?
# 2. Can you seperate the joined column into year, month and day?
# 3. Can you clean and transform the value, wage and release clause columns into columns of integers?
# 4. How can you remove the newline characters from the hits column?
# 5. Should you seperate the Team & contract column into seperate columns?

# --- Q1 --- #
raw_data['Height']
raw_data['Weight']

# Changing from imperial to metric
df = pd.DataFrame()
df['Feet'], df['Inches'] = raw_data['Height'].str.split("'", 1).str
df['Inches'] = pd.to_numeric(df['Inches'].str.replace('"', ''))
df['Feet'] = pd.to_numeric(df['Feet'])

raw_data['Height'] = round((df['Feet'] * 30.48) + (df['Inches'] * 2.54), 2)

raw_data['Weight'] = pd.to_numeric(raw_data['Weight'].str.replace('lbs',''))
raw_data['Weight'] = round(raw_data['Weight'] * 0.453592, 2)

print(raw_data[['Height', 'Weight']])

# --- Q2 --- #
months_day = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}
raw_data['Joined'], raw_data['Joined Year'] = raw_data['Joined'].str.split(",", 1).str
raw_data['Joined Month'] = raw_data['Joined'].str[:3].map(months_day)
raw_data['Joined Day'] = raw_data['Joined'].str[4:].astype(int)
raw_data.drop('Joined', axis=1, inplace=True)

# --- Q3 --- #
edit_data = raw_data[['Value','Wage','Release Clause']]

def removeSigns(data):
    value =  data.replace('€','')
    multi = 1
    if data[-1] == 'K':
        multi = 1000
    elif data[-1] == 'M':
        multi = 1000000
    real_value = value[:-1] if value.endswith(('K', 'M')) else value[:]
    return int(float(real_value) * multi)

raw_data[['Value','Wage','Release Clause']] = edit_data.applymap(removeSigns)

# --- Q4 --- #
# Identify the values that have a K at the end
kValues = raw_data['Hits'].loc[raw_data['Hits'].astype(str).str.contains('K')]
kValues = kValues.index

# Strip the K
raw_data['Hits'].iloc[kValues] = raw_data['Hits'].iloc[kValues].astype(str).str.strip('K')

# Strip the \n from all
raw_data['Hits'] = pd.to_numeric(raw_data['Hits'].astype(str).str.strip('\n'))

# Multipy by 1000 for the values that were more than 1000
raw_data['Hits'].iloc[kValues] = raw_data['Hits'].iloc[kValues] * 1000

# --- Q5 --- #
edited_data = raw_data.copy()
edited_data['Team & Contract'].iloc[99]
edited_data['Contract'].iloc[18970]
edited_data['Team'].iloc[99]

# Strip the left then the right newline characters
edited_data['Team & Contract'] = edited_data['Team & Contract'].astype(str).str.lstrip('\n')
edited_data['Team & Contract'] = edited_data['Team & Contract'].astype(str).str.rstrip('\n')

# Split the Team and Contract lenght into seperate columns
teams, contract = edited_data['Team & Contract'].astype(str).str.split('\n')
edited_data['Team'] = edited_data['Team & Contract'].astype(str).str.slice_replace(start=-11, repl='').str.rstrip('\n')
edited_data['Contract'] = edited_data['Team & Contract'].astype(str).str.slice(start=-11)
edited_data['Contract Start'] = edited_data['Contract'].astype(str).str.split().str[0]
edited_data['Contract End'] = edited_data['Contract'].astype(str).str.split().str[2]