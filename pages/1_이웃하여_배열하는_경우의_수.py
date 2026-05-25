import random
from math import factorial
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="순열 문제 풀이", layout="wide")
st.title("순열 문제 풀이 - 이웃하여 배열하는 경우의 수")

# --- [1] 세션 상태 초기화 ---
if "total_people" not in st.session_state or st.session_state.total_people == 0:
    st.session_state.total_people = random.randint(5, 7)  # 5~7명 무작위 설정
    st.session_state.adjacent_count = random.randint(2, st.session_state.total_people - 2) # 이웃할 인원
    st.session_state.step = 2
    st.session_state.step2_correct = False
    st.session_state.step3_correct = False
    st.session_state.final_correct = False

total = st.session_state.total_people
adjacent = st.session_state.adjacent_count
block_count = total - adjacent + 1

step2_expected_value = factorial(block_count)
step3_expected_value = factorial(adjacent)
final_expected_value = step2_expected_value * step3_expected_value

# --- [2] 문제 재설정 함수 ---
def reset_problem():
    st.session_state.total_people = random.randint(5, 7)
    st.session_state.adjacent_count = random.randint(2, st.session_state.total_people - 2)
    st.session_state.step = 2
    st.session_state.step2_correct = False
    st.session_state.step3_correct = False
    st.session_state.final_correct = False
    st.rerun()

if st.button("🔄 새로운 문제 생성"):
    reset_problem()

# --- [3] 1단계: 문제 설정 표시 ---
st.header("1단계: 문제 설정")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="총 인원 수 (N)", value=f"{total} 명")
with col2:
    st.metric(label="이웃할 인원 수 (K)", value=f"{adjacent} 명")
st.info(f"문제: {total}명의 사람을 일렬로 앉힐 때, 특정한 {adjacent}명이 서로 이웃하게 앉는 경우의 수를 구하세요.")

# --- [4] 1.5단계: 텍스트 및 스타일 기반 형광펜 주머니 시각화 ---
st.markdown("---")
st.subheader("🕵️‍♂️ 1.5단계 [아이디어 탐색]: 이웃할 사람들을 직접 묶어봅시다!")
st.write(f"아래 명단에서 이웃하게 만들고 싶은 사람을 딱 **{adjacent}명**만 선택해 보세요.")

people_list = [f"사람 {i}" for i in range(1, total + 1)]
selected_neighbors = st.multiselect(
    "이웃으로 묶을 사람 선택:",
    options=people_list,
    default=people_list[:adjacent],
    max_selections=adjacent
)

is_bundle_ready = len(selected_neighbors) == adjacent

# HTML/CSS를 이용한 에러 없는 깔끔한 형광펜 주머니 시각화
st.write("### 🪑 좌석 배치 미리보기")
visual_cols = st.columns(total)

for i, person in enumerate(people_list):
    with visual_cols[i]:
        if person in selected_neighbors:
            # 이웃은 눈에 띄는 핑크색 형광펜 스타일 박스로 감싸기
            st.markdown(
                f"""
                <div style="background-color: #FFE6EC; border: 2px dashed #FF3366; 
                            padding: 15px; border-radius: 10px; text-align: center;">
                    <span style="color: #FF3366; font-weight: bold; font-size: 16px;">💗 {person}</span><br>
                    <small style="color: #FF3366;">(이웃 그룹)</small>
                </div>
                """, 
                unsafe_html=True
            )
        else:
            # 일반 사람은 편안한 초록색 박스
            st.markdown(
                f"""
                <div style="background-color: #E6F9E6; border: 1px solid #28A745; 
                            padding: 15px; border-radius: 10px; text-align: center; margin-top: 10px;">
                    <span style="color: #28A745; font-weight: bold; font-size: 16px;">👤 {person}</span><br>
                    <small style="color: #666;">(일반)</small>
                </div>
                """, 
                unsafe_html=True
            )

st.write("") # 공백 추가

if is_bundle_ready:
    st.success(f"💡 주머니 완성! 분홍색 점선 주머니(1개) + 나머지 일반 사람({total - adjacent}명) = 총 {block_count}개의 덩어리가 됩니다.")
else:
    st.warning(f"⚠️ 정확히 {adjacent}명을 선택해야 형광펜 주머니가 올바르게 묶입니다.")

# --- [5] 2단계 UI: 외부 블록 배열하기 ---
st.markdown("---")
st.header("2단계: 묶음을 하나의 블록으로 보고 배열하기")
st.write(f"분홍색 주머니를 포함하여 총 **{block_count}개**의 덩어리를 일렬로 배열하는 경우의 수를 구하세요.")

if not st.session_state.step2_correct:
    col_in1, col_in2 = st.columns(2)
    s2_expr = col_in1.text_input("2단계 식 입력 (예: 4!)", key="s2_expr_input")
    s2_val = col_in2.number_input("2단계 계산값 입력", min_value=0, step=1, key="s2_val_input")
    
    if st.button("2단계 정답 확인"):
        expr_ok = s2_expr.replace(" ", "").lower() == f"{block_count}!"
        val_ok = s2_val == step2_expected_value
        if expr_ok and val_ok:
            st.session_state.step2_correct = True
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("오답입니다. 덩어리 개수를 세어 식(n!)과 값을 다시 확인하세요.")
else:
    st.success(f"✔️ 2단계 정답 통과: `{block_count}!` = {step2_expected_value}")

# --- [6] 3단계 UI: 묶음 내부 순서 정하기 ---
if st.session_state.step >= 3:
    st.markdown("---")
    st.header("3단계: 이웃하는 이들끼리 순서 변경하기")
    st.write(f"분홍색 주머니 내부의 **{adjacent}명**이 안에서 자리를 바꾸는 경우의 수를 구하세요.")

    if not st.session_state.step3_correct:
        col_in1, col_in2 = st.columns(2)
        st3_expr = col_in1.text_input("3단계 식 입력 (예: 3!)", key="st3_expr_input")
        st3_val = col_in2.number_input("3단계 계산값 입력", min_value=0, step=1, key="st3_val_input")
        
        if st.button("3단계 정답 확인"):
            expr_ok = st3_expr.replace(" ", "").lower() == f"{adjacent}!"
            val_ok = st3_val == step3_expected_value
            if expr_ok and val_ok:
                st.session_state.step3_correct = True
                st.session_state.step = 4
                st.rerun()
            else:
                st.error("오답입니다. 주머니 안의 인원수를 기준으로 다시 입력하세요.")
    else:
        st.success(f"✔️ 3단계 정답 통과: `{adjacent}!` = {step3_expected_value}")

# --- [7] 4단계 UI: 최종 결합 ---
if st.session_state.step >= 4:
    st.markdown("---")
    st.header("4단계: 전체 경우의 수 구하기")
    st.write(f"외부 배열({step2_expected_value}가지)과 내부 배열({step3_expected_value}가지)을 곱해 최종 정답을 구하세요.")

    if not st.session_state.final_correct:
        final_val = st.number_input("최종 정답 숫자로 입력", min_value=0, step=1, key="final_val_input")
        if st.button("최종 정답 제출"):
            if final_val == final_expected_value:
                st.session_state.final_correct = True
                st.rerun()
            else:
                st.error("오답입니다. 곱셈 계산을 다시 해보세요.")
    else:
        st.balloons()
        st.success(f"🎉 정답입니다! 최종 경우의 수: {step2_expected_value} × {step3_expected_value} = {final_expected_value} 가지")

st.markdown("---")
st.caption("*이 페이지는 이웃하여 배열하는 순열의 원리를 단계별로 탐색하도록 설계되었습니다.*")