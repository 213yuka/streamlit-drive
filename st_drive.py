import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

yuhi = 'src/yuhi02.csv'
yakei = 'src/yakei02.csv'
kaisui = 'src/kaisui02.csv'

@st.cache
def load_data(file):
    df_load = pd.read_csv(file,encoding='shift-jis')
    # 経度緯度をmapで認識できるように修正
    df1 = df_load.rename(columns={'北緯': 'lat','東経':'lon'})
    # 所在地を都道府県と市区町村に分割
    df2 = pd.concat([df1,df1['所在地'].str.extract('(?P<都道府県>...??[都道府県])(?P<市区町村>.*)', expand=True)], axis=1).drop('所在地', axis=1)
    return df2

def main():
    st.title('日本のドライブで寄れそうなスポット')
    block_list = ['夕陽', '夜景', '海水']
    control_features = st.sidebar.selectbox('何を楽しみたい？',block_list)
    st.header(f'{control_features}100選')
    if control_features == '夕陽':
        visualize(yuhi)
    elif control_features == '夜景':
        visualize(yakei)
    elif control_features == '海水':
        visualize(kaisui)

def visualize(file):
    df = load_data(file)
    st.dataframe(df[['名称','都道府県','市区町村']])
    if st.sidebar.checkbox('mapを表示'):
        st.subheader('map')
        st.map(df)
    if st.sidebar.checkbox('都道府県ごとのグラフを表示'):
        st.subheader('都道府県ごとのグラフ')
        selected_prefectures = st.multiselect('都道府県を選択',df['都道府県'].unique().tolist(),['北海道','秋田県','青森県','富山県'])
        n = [(df['都道府県'] == prefecture).sum() for prefecture in selected_prefectures]
        # 棒グラフで表示
        sns.set(font="IPAexGothic") 
        sns.set_style('whitegrid')
        sns.set_palette('gray')
        x = np.array(selected_prefectures)
        y = np.array(n)
        x_position = np.arange(len(x))
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(x_position, y, tick_label=x)
        ax.set_xlabel('都道府県')
        ax.set_ylabel('数')
        st.pyplot(fig)

if __name__ == "__main__":
    main()