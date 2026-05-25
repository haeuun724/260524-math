import random
from math import factorial
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 페이지 설정
st.set_page_config(page_title="순열 문제 풀이", layout="wide")
st.title("순열 문제 풀이 - 이웃하여 배열하는 경우의 수")

# --- [1] 세션 상태 초기화 ---
if "total_people" not in st.session_state or st.session_state.total_people == 0:
    st.session_state.total_people = random.randint(5, 7)  # 5~7명 무작위
    st.session_state.adjacent_count = random.randint(2, st.session_state.total_people - 2) # 이웃 인원
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

# --- [4] 1.5단계: 형광펜 주머니 시각화 및 조작 탐색 ---
st.markdown("---")
st.subheader("🕵️‍♂️ 1.5단계 [아이디어 탐색]: 이웃할 사람들을 직접 묶어봅시다!")
st.write(f"아래 명단에서 이웃하게 만들고 싶은 사람을 딱 **{adjacent}명**만 선택해 보세요.")

people_list = [f"P{i}" for i in range(1, total + 1)]
selected_neighbors = st.multiselect(
    "이웃으로 묶을 사람 선택:",
    options=people_list,
    default=people_list[:adjacent],
    max_selections=adjacent
)

# Matplotlib를 이용한 실시간 형광펜 주머니 렌더링
fig, ax = plt.subplots(figsize=(max(5, total * 1.0), 1.8))
box_width = 0.8
gap = 0.3
current_x = 0

selected_indices = [people_list.index(p) for p in selected_neighbors]
is_bundle_ready = len(selected_neighbors) == adjacent

if is_bundle_ready:
    min_idx = min(selected_indices)
    max_idx = max(selected_indices)
    bundle_start_x = min_idx * (box_width + gap) - 0.1
    bundle_width = (max_idx - min_idx + 1) * box_width + (max_idx - min_idx) * gap + 0.2
    
    # 연분홍색 형광펜 주머니 칠하기
    rect_bundle = patches.Rectangle(
        (bundle_start_x, 0.1), bundle_width, 0.8,
        linewidth=2, edgecolor='#ff3366', facecolor='#ffe6ec', linestyle='--'
    )
    ax.add_patch(rect_bundle)

for i, person in enumerate(people_list):
    if person in selected_neighbors:
        facecolor, edgecolor = '#ff99bb', '#ff3366'  # 이웃 (핑크)
    else:
        facecolor, edgecolor = '#ccffcc', 'black'    # 일반 (연두)
        
    rect = patches.Rectangle((current_x, 0.2), box_width, 0.6, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(current_x + box_width/2, 0.5, person, ha='center', va='center', fontsize=11, fontweight='bold')
    current_x += box_width + gap

ax.set_xlim(-0.5, current_x)
ax.set_ylim(0, 1.2)
ax.axis('off')
st.pyplot(fig)
plt.close(fig) # 에러 방지용 그래프 메모리 해제

if is_bundle_ready:
    st.success(f"💡 주머니 완성! 주머니(1개) + 남은 인원({total - adjacent}명) = 총 {block_count}개의 덩어리가 됩니다.")
else:
    st.warning(f"⚠️ 정확히 {adjacent}명을 선택해야 형광펜 주머니가 올바르게 묶입니다.")

# --- [5] 2단계 UI: 외부 블록 배열하기 ---
st.markdown("---")
st.header("2단계: 묶음을 하나의 블록으로 보고 배열하기")
st.write(f"형광펜 주머니를 포함하여 총 **{block_count}개**의 덩어리를 일렬로 배열하는 경우의 수를 구하세요.")

if not st.session_state.step2_correct:
    col_in1, col_in2 = st.columns(2)
    s2_expr = col_in1.text_input("2단계 식 입력 (예: 4!)", key="s2_expr_input")
    s2_val = col_in2.number_input("2단계 계산값 입력", min_value=0, step=1, key="s2_val_input")
    
    if st.button("2단계 정답 확인"):
        # 입력 양식 검증
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
    st.write(f"형광펜 주머니 내부의 **{adjacent}명**이 안에서 자리를 바꾸는 경우의 수를 구하세요.")

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