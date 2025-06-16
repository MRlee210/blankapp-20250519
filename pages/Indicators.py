import streamlit as st
import pandas as pd
import pandas_datareader.data as pdr
import yfinance as yf
from datetime import datetime, timedelta

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="경제 지표 검색기",
    page_icon="💹",
    layout="wide"
)

# yfinance가 pandas_datareader를 오버라이드하도록 설정
# yf.pdr_override()

# --- 앱 메인 ---
st.title("💹 경제 지표 검색기")
st.caption("선택한 주요 경제 지표의 최근 5년간 추이를 확인합니다.")

# 지표 선택 옵션
options = {
    '환율 (USD/KRW)': 'KRW=X',
    '미국 기준금리': 'DFF', # Federal Funds Effective Rate
    '미국 실업률': 'UNRATE',
    '미국 소비자물가지수 (CPI)': 'CPIAUCNS'
}
selected_option_label = st.selectbox(
    "확인하고 싶은 경제 지표를 선택하세요:",
    options.keys()
)

# 데이터 조회 기간 설정 (오늘로부터 5년 전)
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)
selected_ticker = options[selected_option_label]

# 데이터 로딩 상태 표시
with st.spinner('데이터를 불러오는 중입니다... 잠시만 기다려주세요.'):
    try:
        # 선택한 지표에 따라 데이터 소스 분기
        if selected_option_label == '환율 (USD/KRW)':
            # Yahoo Finance에서 환율 데이터 불러오기
            data = yf.download(selected_ticker, start=start_date, end=end_date)
            chart_data = data['Close']
            st.subheader(f"📊 {selected_option_label} 변화 (최근 5년)")
            st.info("원/달러 환율(종가 기준)의 변화를 나타냅니다.")

        else:
            # FRED에서 경제 지표 데이터 불러오기
            data = pdr.get_data_fred(selected_ticker, start=start_date, end=end_date)
            chart_data = data[selected_ticker]
            st.subheader(f"📊 {selected_option_label} 변화 (최근 5년)")

            if selected_option_label == '미국 기준금리':
                st.info("미국 연방준비은행의 유효 연방기금금리(Effective Federal Funds Rate)를 나타냅니다.")
            elif selected_option_label == '미국 실업률':
                st.info("미국의 계절 조정 실업률(%)을 나타냅니다.")
            elif selected_option_label == '미국 소비자물가지수 (CPI)':
                st.info("미국 도시 소비자를 대상으로 한 소비자물가지수(1982-84=100)를 나타냅니다.")

        # 차트 출력
        if chart_data.empty:
            st.warning("해당 기간의 데이터를 불러올 수 없습니다.")
        else:
            st.line_chart(chart_data)

            # 원본 데이터 테이블 출력
            st.write("---")
            st.subheader("📝 원본 데이터 보기")
            display_df = chart_data.to_frame(name=selected_option_label).sort_index(ascending=False)
            st.dataframe(display_df, use_container_width=True)

            # 데이터 출처 명시
            source = "Yahoo Finance" if selected_option_label == '환율 (USD/KRW)' else "FRED (Federal Reserve Economic Data)"
            st.caption(f"데이터 출처: {source}")

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        st.warning("네트워크 연결을 확인하거나 잠시 후 다시 시도해 주세요.")