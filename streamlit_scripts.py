import streamlit as st
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta


# from preprocessing_window import in_out_df, my_katalk_df
# from preprocessing_mac import in_out_df, my_katalk_df
in_out_df = pd.read_csv("preprocessed_data/" +  "in_out_2023-09-14-00-31-16.csv")
my_katalk_df = pd.read_csv("preprocessed_data/" +  "kakao_msg_2023-09-14-00-31-16.csv")

st.text('전체 채팅 분포')
total_groupby_df = my_katalk_df.groupby(['year_month_day', 'user_class'])['year_month_day'].size().reset_index(name='user_class_day_count')
total_pivot_df = total_groupby_df.pivot(index='year_month_day',columns='user_class',values='user_class_day_count').reset_index()
total_chart_df = total_pivot_df.fillna(0)
total_chart_df_columns = total_chart_df.columns.to_list()
total_chart_df_columns.remove('year_month_day')
st.area_chart(
    total_chart_df,
    x='year_month_day',
    y= total_chart_df_columns
)

st.text('요일 별 채팅 분포')
weekday_groupby_df = my_katalk_df.groupby(['hour', 'weekday'])['hour'].size().reset_index(name='weekday_hour_count')
weekday_pivot_df = weekday_groupby_df.pivot(index='hour',columns='weekday',values='weekday_hour_count').reset_index()
weekday_chart_df = weekday_pivot_df.fillna(0)
weekday_chart_df_columns = weekday_chart_df.columns.to_list()
weekday_chart_df_columns.remove('hour')
st.area_chart(
        weekday_chart_df,
        x='hour',
        y= weekday_chart_df_columns)


day = my_katalk_df.year_month_day.unique()
day_sorted = sorted(day, reverse = True)
# 시작 날짜와 종료 날짜 설정
start_date = st.selectbox(
    '어떤 날짜의 현황을 볼래?',
    (day_sorted))
start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
new_date_obj = start_date_obj + timedelta(days=1)
end_date = new_date_obj.strftime('%Y-%m-%d')

# 날짜 범위를 적용하여 데이터 프레임 필터링
def filer_df_by_date(df, start_date, end_date):
    return df[(df['date_time'] >= start_date) & (df['date_time'] <= end_date)]

in_out_df_today = filer_df_by_date(in_out_df, start_date, end_date)
my_katalk_df_today = filer_df_by_date(my_katalk_df, start_date, end_date)
weekday_today = my_katalk_df_today.weekday.unique()

st.header(f"{start_date} {weekday_today[0]}의 :blue[로마드] 오픈 채팅 현황")
if st.button('로마드 :red[2주 챌린지] 현황 바로가기!(PC ver.'):
    webbrowser.open_new_tab("https://roalnamchallenge1.streamlit.app")



st.subheader('오늘 하루의 채팅 분포')
groupby_df = my_katalk_df_today.groupby(['hour', 'user_class'])['hour'].size().reset_index(name='user_class_hour_count')
pivot_df = groupby_df.pivot(index='hour',columns='user_class',values='user_class_hour_count').reset_index()
chart_df = pivot_df.fillna(0)
chart_df_columns = chart_df.columns.to_list()
chart_df_columns.remove('hour')
st.area_chart(
    chart_df,
    x='hour',
    y= chart_df_columns
)

st.text('오늘의 채팅 내용')
st.dataframe(my_katalk_df_today[['date_time','user_name', 'user_class', 'text']])


heavy_talker = my_katalk_df_today.user_name.value_counts().to_frame()
st.subheader('🌟오늘 최고의 참여자🌟')
st.dataframe(heavy_talker)


st.subheader('오늘의 가입자👏')
st.dataframe(in_out_df_today[in_out_df_today.in_out == 'IN'][['date_time', 'user_name', 'user_class', 'in_out']])

st.subheader('오늘의 탈퇴자💧')
st.dataframe(in_out_df_today[in_out_df_today.in_out == 'OUT'][['date_time', 'user_name', 'user_class', 'in_out']])


st.text('이름 재설정 안내가 필요해요!')
st.dataframe(my_katalk_df_today[my_katalk_df_today.user_class == 'Not defined'][['user_name', 'text']])
