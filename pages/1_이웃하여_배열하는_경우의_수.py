import random
from math import factorial
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="순열 문제 풀이", layout="wide")
st.title("순열 문제 풀이 - 이웃하여 배열하는 경우의 수")

# --- [1] 세션 상태 초기화 ---
if "total_people" not in st.session_state or st.session_state.total_people == 0:
    st.session_state.total_people = random.randint(5, 8)  # 최대 8명 제한
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
    st.session_state.total_people = random.randint(5, 8)
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

# --- [4] 1.5단계: 형광펜 스타일이 적용된 시각화 ---
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

st.write("### 🪑 좌석 배치 미리보기 (형광펜 강조)")

seat_cols = st.columns(total)

for i, person in enumerate(people_list):
    with seat_cols[i]:
        if person in selected_neighbors:
            # 이웃 그룹: 안전한 인라인 스타일로 분홍색 형광펜 패딩 박스 구현 (에러 없음)
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="background-color: #FFE6EC; border: 1px dashed #FF3366; 
                                padding: 10px; border-radius: 5px; text-align: center;">
                        <span style="color: #FF3366; font-weight: bold; font-size: 16px;">💗 {person}</span><br>
                        <small style="color: #FF3366; font-weight: bold;">[이웃 그룹]</small>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            # 일반 사람: 연두색의 깔끔하고 차분한 박스 구현
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="background-color: #E6F9E6; padding: 10px; border-radius: 5px; text-align: center;">
                        <span style="color: #28A745; font-weight: bold; font-size: 16px;">👤 {person}</span><br>
                        <small style="color: #666;">일반</small>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

st.write("") 

if is_bundle_ready:
    st.success(f"💡 조건 확인 완료: 이웃 그룹(1묶음)과 나머지 일반 사람({total - adjacent}명)의 배열 관계를 생각해보세요.")
else:
    st.warning(f"⚠️ 정확히 {adjacent}명을 선택해야 그룹이 올바르게 생성됩니다.")


# --- [5] 🧮 풀이 보조 만능 계산기 팩 ---
st.markdown("")
with st.expander("🧮 풀이를 위한 보조 계산기 열기 (팩토리얼 / 곱셈)", expanded=False):
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        st.markdown("**ℹ️ 팩토리얼 계산기**")
        fact_input = st.text_input("n! 형식으로 입력 (예: 5!)", key="fact_calc_in")
        if fact_input:
            clean_fact = fact_input.replace(" ", "").lower()
            if clean_fact.endswith("!") and clean_fact[:-1].isdigit():
                n_val = int(clean_fact[:-1])
                st.success(f" 결과: {n_val}! = {factorial(n_val):,}")
            else:
                st.warning("올바른 형식으로 입력해 주세요. (예: 6!)")
                
    with calc_col2:
        st.markdown("**ℹ️ 곱셈 계산기**")
        mul_input = st.text_input("n x m 형식으로 입력 (예: 24 x 6)", key="mul_calc_in")
        if mul_input:
            clean_mul = mul_input.replace(" ", "").replace("×", "x").replace("*", "x").lower()
            if "x" in clean_mul:
                parts = clean_mul.split("x")
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    n1, n2 = int(parts[0]), int(parts[1])
                    st.success(f" 결과: {n1} × {n2} = {n1 * n2:,}")
                else:
                    st.warning("숫자 x 숫자 형식으로 입력해 주세요.")
            else:
                st.warning("올바른 형식으로 입력해 주세요. (예: 24 x 6)")


# --- [6] 2단계 UI: 외부 블록 배열하기 ---
st.markdown("---")
st.header("2단계: 전체 배열 경우의 수 구하기")
st.write("이웃한 사람들을 한 묶음으로 봤을 때 전체를 일렬로 배열하는 경우의 수를 구하세요.")

if not st.session_state.step2_correct:
    col_in1, col_in2 = st.columns(2)
    s2_expr = col_in1.text_input("2단계 식 입력 (예: 4!)", key="s2_expr_input")
    s2_val = col_in2.text_input("2단계 계산값 입력", key="s2_val_input")
    
    if st.button("2단계 정답 확인"):
        expr_ok = s2_expr.replace(" ", "").lower() == f"{block_count}!"
        val_ok = s2_val.replace(" ", "").replace(",", "") == str(step2_expected_value)
        if expr_ok and val_ok:
            st.session_state.step2_correct = True
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("오답입니다. 묶음의 총 개수를 고려하여 식과 결과값을 다시 확인하세요.")
else:
    st.success(f"✔️ 2단계 정답 통과: `{block_count}!` = {step2_expected_value:,}")

# --- [7] 3단계 UI: 묶음 내부 순서 정하기 ---
if st.session_state.step >= 3:
    st.markdown("---")
    st.header("3단계: 이웃한 묶음 내부의 경우의 수 구하기")
    st.write("이웃한 사람들끼리 자리를 바꾸는 경우의 수를 구하세요.")

    if not st.session_state.step3_correct:
        col_in1, col_in2 = st.columns(2)
        st3_expr = col_in1.text_input("3단계 식 입력 (예: 3!)", key="st3_expr_input")
        st3_val = col_in2.text_input("3단계 계산값 입력", key="st3_val_input")
        
        if st.button("3단계 정답 확인"):
            expr_ok = st3_expr.replace(" ", "").lower() == f"{adjacent}!"
            val_ok = st3_val.replace(" ", "").replace(",", "") == str(step3_expected_value)
            if expr_ok and val_ok:
                st.session_state.step3_correct = True
                st.session_state.step = 4
                st.rerun()
            else:
                st.error("오답입니다. 이웃한 그룹의 인원수를 기준으로 다시 입력하세요.")
    else:
        st.success(f"✔️ 3단계 정답 통과: `{adjacent}!` = {step3_expected_value:,}")

# --- [8] 4단계 UI: 최종 결합 ---
if st.session_state.step >= 4:
    st.markdown("---")
    st.header("4단계: 전체 경우의 수 구하기")
    st.write(f"외부 배열({step2_expected_value:,}가지)과 내부 배열({step3_expected_value:,}가지)의 조건을 결합하여 최종 정답을 구하세요.")

    if not st.session_state.final_correct:
        final_val = st.text_input("최종 정답 숫자로 입력", key="final_val_input")
        if st.button("최종 정답 제출"):
            if final_val.replace(" ", "").replace(",", "") == str(final_expected_value):
                st.session_state.final_correct = True
                st.rerun()
            else:
                st.error("오답입니다. 두 조건이 동시에 일어나는 경우이므로 알맞은 연산을 해보세요.")
    else:
        st.balloons()
        st.success(f"🎉 정답입니다! 최종 경우의 수: {step2_expected_value:,} × {step3_expected_value:,} = {final_expected_value:,} 가지")

st.markdown("---")
st.caption("*이 페이지는 이웃하여 배열하는 순열의 원리를 단계별로 탐색하도록 설계되었습니다.*")