import streamlit as st
import random

def rock_paper_scissors():
    """
    가위바위보 게임을 실행하는 함수
    """
    st.header("✂️ 가위바위보 게임")
    
    # 게임 상태 초기화
    if 'player_score' not in st.session_state:
        st.session_state.player_score = 0
        st.session_state.computer_score = 0
        st.session_state.result = ""

    options = ["✌️", "✊", "🖐️"]
    computer_choice = random.choice(options)

    st.write("무엇을 내시겠어요?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✌️ (가위)"):
            player_choice = "✌️"
            play_game(player_choice, computer_choice)

    with col2:
        if st.button("✊ (바위)"):
            player_choice = "✊"
            play_game(player_choice, computer_choice)
            
    with col3:
        if st.button("🖐️ (보)"):
            player_choice = "🖐️"
            play_game(player_choice, computer_choice)

    st.subheader(f"플레이어: {st.session_state.player_score} vs 컴퓨터: {st.session_state.computer_score}")
    
    if st.session_state.result:
        st.info(st.session_state.result)

    if st.button("점수 초기화"):
        st.session_state.player_score = 0
        st.session_state.computer_score = 0
        st.session_state.result = "점수가 초기화되었습니다."
        st.rerun()

def play_game(player, computer):
    """
    가위바위보 게임의 승패를 결정하는 함수
    """
    result = ""
    if player == computer:
        result = f"컴퓨터도 {computer}를 냈습니다. 비겼네요! 🤝"
    elif (player == "✊" and computer == "✌️") or \
         (player == "🖐️" and computer == "✊") or \
         (player == "✌️" and computer == "🖐️"):
        result = f"컴퓨터는 {computer}를 냈습니다. 이겼습니다! 😄"
        st.session_state.player_score += 1
    else:
        result = f"컴퓨터는 {computer}를 냈습니다. 졌습니다... 😥"
        st.session_state.computer_score += 1
        
    st.session_state.result = result

# --- 앱 실행 ---
st.title("간단한 미니 게임")
rock_paper_scissors()