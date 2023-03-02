import pandas as pd
import streamlit as st
import altair as alt

############## DASH ##########################
st.set_page_config(page_title="DashCopy",layout="wide",page_icon="sport-car.ico")

st.write("""
# Car Rental
""")

############## DATASET #######################
@st.cache(allow_output_mutation=True)
def load_data(url):
    return pd.read_csv(url, decimal=',')

df = load_data('https://docs.google.com/spreadsheets/d/e/2PACX-1vRhWHgSDJxbYiwZh0VPgNBuPP5Jgujsa-uRY6QGbCeVhe7uN8c0Lxw8UHzs3ULslsTkCubXTkfo8K4O/pub?gid=1427198076&single=true&output=csv')
df_params = load_data('https://docs.google.com/spreadsheets/d/e/2PACX-1vRhWHgSDJxbYiwZh0VPgNBuPP5Jgujsa-uRY6QGbCeVhe7uN8c0Lxw8UHzs3ULslsTkCubXTkfo8K4O/pub?gid=720793826&single=true&output=csv')

# df['ANOMES'] = df['ANOMES'].map(int)

############## INFOS #######################
df_gas = df[df['NOME']=='gás']

col1, col2 = st.columns(2)
profit = df['VALOR'].sum()
breakeven = (df['VALOR'].sum() / df['ANOMES'].nunique()).round(2)
gas_profit = df_gas['VALOR'].sum().round(2) + (df['ANOMES'].nunique() * 200)
profitability_today = (((df['VALOR'].sum().round(2) - 17500 - df_params['Quitação'].sum() + df_params['Venda'].sum()) / 17500) / df['ANOMES'].nunique()).round(4) * 100
profitability_breakeven = ((((df_params['Venda'].sum() - ((48-(breakeven + df['ANOMES'].nunique())) * 619.78)) / 17500)) / (df['ANOMES'].nunique() + breakeven)).round(4) * 100
new_profitability_breakeven = (((df_params['Venda'].sum() + ((breakeven-(48-df['ANOMES'].nunique()))*619,78)) / 17500) - 1) / (breakeven+df['ANOMES'].nunique())

col1.metric(label="Profit", value=profit)
col1.metric(label="Month Profit", value=(profit / df['ANOMES'].nunique()).round(2))
col1.metric(label="% Breakeven", value=(df['VALOR'].sum() / 17500).round(4)*100)
col1.metric(label="Breakeven", value=((17500 - df['VALOR'].sum()) / breakeven).round())

col2.metric(label="Gas Profit", value=gas_profit)
col2.metric(label="Gas Breakeven", value=(abs(gas_profit) / 200).round())
col2.metric(label="% Profitability Today", value=profitability_today)
col2.metric(label="% Profitability Breakeven", value=new_profitability_breakeven)

############# GRAPHS #########################
st.write("""
 Month Profit
""")

profit = alt.Chart(df).mark_line(color='blue').encode(
    x=alt.X(field='ANOMES'),
    y=alt.Y(field='VALOR', aggregate='sum'),
)

text = profit.mark_text(
    align='left',
    baseline='middle',
    dx=3,
    color='white'
).encode(
    text=alt.Y(field='VALOR', aggregate='sum')
)

st.altair_chart(profit.interactive() + text, use_container_width=True)

df_maintenance = df[df['TIPO'] == 'manutenção']
df_maintenance['VALOR'] = abs(df_maintenance['VALOR'])
st.write("""
 Maintenance
""")

maintenance = alt.Chart(df_maintenance).mark_line(color='blue').encode(
    x=alt.X(field='NOME'),
    y=alt.Y(field='VALOR', aggregate='sum'),
)

text = maintenance.mark_text(
    align='left',
    baseline='middle',
    dx=3,
    color='white'
).encode(
    text=alt.Y(field='VALOR', aggregate='sum')
)

st.altair_chart(maintenance.interactive() + text, use_container_width=True)