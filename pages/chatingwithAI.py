import streamlit as st
from openai import OpenAI # openai v1.x.x 이상

# 1. API 키 로드 및 OpenAI 클라이언트 초기화
try:
    client = OpenAI(api_key=st.secrets["openai"]["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"OpenAI API 키를 로드하는 중 오류가 발생했습니다: {e}")
    st.info("'.streamlit/secrets.toml' 파일에 OPENAI_API_KEY를 설정했는지 확인하세요.")
    st.stop()

# 2. 앱 제목 설정
st.title("💬 멀티턴 챗봇")
st.caption("🚀 Streamlit과 OpenAI로 만든 챗봇입니다.")

# 3. 대화 내용 저장을 위한 session_state 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "당신은 사용자에게 도움이 되는 친절한 AI 어시스턴트입니다."}]

# 4. 이전 대화 내용 표시
for msg in st.session_state.messages:
    if msg["role"] != "system": # 시스템 메시지는 화면에 직접 표시하지 않음
        st.chat_message(msg["role"]).write(msg["content"])

# 5. 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자의 메시지를 대화 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # OpenAI API 호출 (예외 처리 포함)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # 또는 사용 가능한 다른 모델 (예: "gpt-4")
            messages=st.session_state.messages
        )
        # AI의 응답을 대화 기록에 추가
        assistant_response = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.chat_message("assistant").write(assistant_response)

    except Exception as e:
        st.error(f"OpenAI API 호출 중 오류가 발생했습니다: {e}")
        # 실패한 경우, 사용자 메시지를 롤백하거나 사용자에게 알림
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            st.session_state.messages.pop() # 마지막 사용자 메시지 제거 (선택적)

        st.warning("죄송합니다. 답변을 생성하는 데 문제가 발생했습니다. 잠시 후 다시 시도해 주세요.")

# (선택 사항) 디버깅을 위해 session_state 내용 표시
# with st.expander("대화 기록 보기 (디버깅용)"):
# st.json(st.session_state.messages)