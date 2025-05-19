# app.py

import streamlit as st
import streamlit.components.v1 as components

# ← 이 블록이 다른 st.* 호출보다 언제나 먼저 와야 합니다.
st.set_page_config(
    page_title="Nasdaq 100 Market Map",
    layout="wide"
)

st.title("📈 Nasdaq 100 Market Map")

# TradingView Stock Heatmap 위젯 HTML
heatmap_widget = """
<!-- TradingView Stock Heatmap Widget BEGIN -->
<div class="tradingview-widget-container">
  <div id="tv-heatmap"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
    new TradingView.StockHeatmap("tv-heatmap", {
      "width": "100%",
      "height": 600,
      "index": "US100",
      "locale": "kr",
      "colorTheme": "light"
    });
  </script>
</div>
<!-- TradingView Stock Heatmap Widget END -->
"""
components.html(heatmap_widget, height=650)
