import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv(r'C:\Users\europ\Documents\Github_clone\boilerplate-medical-data-visualizer\medical_examination.csv')
# 2
df['BMI'] = df['weight']/(df['height']/100)**2
df['overweight'] = (df['BMI']>25).astype(int)
# 3
df['cholesterol'] = df['cholesterol'].apply(lambda x:0 if x ==1 else 1)
df['gluc'] = df['gluc'].apply(lambda x:0 if x ==1 else 1)
# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    # 6
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    # 7
    catplot = sns.catplot(x='variable', y='total', hue='value', col='cardio', kind='bar', data=df_cat)
    # 8
    fig = catplot.fig
    # 9
    fig.savefig('catplot.png')
    return fig

# 10
def draw_heat_map():
    # 11
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &  
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]
    if 'BMI' in df_heat.columns:
        df_heat = df_heat.drop(columns=['BMI'])
    # 12
    corr = df_heat.corr()
    # 13
    mask = np.triu(corr)
    # 14
    fig, ax = plt.subplots(figsize=(10,8))
    # 15
    sns.heatmap(corr, annot=True, mask=mask, square=True, fmt='.1f', ax=ax, cmap='RdBu')
    # 16
    fig.savefig('heatmap.png')
    return fig
