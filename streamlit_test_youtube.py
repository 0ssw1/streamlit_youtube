import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

st.header("유튜브 크롤러")
url = st.text_input("주소를 입력하세요")
#https://www.youtube.com/watch?v=2JinL6G7EhM
button = st.button("확인")

if button:
    if "v=" in url:
        video_id = url.split("v=")[1]
    else:
        video_id = url.split("youtu.be/")[1]
    result = YouTubeTranscriptApi.get_transcript(video_id,languages=["ko"])

    context = ""
    for text in result:
        context = context + text["text"] + " " 

    template_text = """
        반드시 입력문에 있는 내용을 3줄로 요약해주세요. 아래 출력예시와 비슷하게 3개의 bullet point로 문장을 정리하면 됩니다.

        # 예시
        ·금요일 미세먼지 '매우 나쁨'예상: 내몽골 발원 황사, 북서풍으로 유입
        ·황사위기경보 발령: 수도권, 강원, 충남, 경북에 관심 요청, 외출 자제 권고
        ·대기질 악화 예상: 30일까지 전국적으로 미세 먼지 '나쁨'수준 지속 예상

        # 입력문
        -{prompt}

        """

    template1 = PromptTemplate.from_template(template_text)

    llm = ChatOpenAI(temperature=0.7, max_tokens=1000, model_name='gpt-3.5-turbo', openai_api_key=st.secrets['OPENAI_API_KEY'])
    result = (
        template1
        | llm
        | StrOutputParser()
    )
    result = result.invoke({"prompt": context})

    st.write(result)
    