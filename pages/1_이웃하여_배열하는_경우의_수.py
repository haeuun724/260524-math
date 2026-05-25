import random
from math import factorial
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PAGE_TITLE = "순열 문제 풀이 - 이웃하여 배열하는 경우의 수"
st.set_page_config(page_title=PAGE_TITLE, layout="wide")

st.title(PAGE_TITLE)

# 한글 폰트 깨짐 방지 설정
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# --- [1] Session State 초기화 섹션 ---
if "total_people" not in st.session_state:
    st.session_state.total_people = 0
    st.session_state.adjacent_count = 0
    st.session_state.step = 2
    st.session_state.step2_correct = False
    st.session_state.step3_correct = False
    st.session_state.final_correct = False
    st.session_state.step2_expr = ""
    st.session_state.step2_value = 0
    st.session_state.step3_expr = ""
    st.session_state.step3_value = 0
    st.session_state.final_value = 0

def reset_problem():
    total = random.randint(5, 8)  # 직접 묶어보기에 가장 적절한 인원 수(5~8명)
    adjacent = random.randint(2, total - 2)  # 이웃 인원은 최소 2명, 전체보다 적게
    st.session_state.total_people = total
    st.session_state.adjacent_count = adjacent
    st.session_state.step = 2
    st.session_state.step2_correct = False
    st.session_state.step3_correct = False
    st.session_state.final_correct = False
    st.session_state.step2_expr = ""
    st.session_state.step2_value = 0
    st.session_state.step3_expr = ""
    st.session_state.step3_value = 0
    st.session_state.final_value = 0

if st.button("🔄 새로운 문제 생성 (조건 무작위 변경)"):
    reset_problem()
    st.rerun()

if st.session_state.total_people == 0:
    reset_problem()

# 주요 변수 재할당
total = st.session_state.total_people
adjacent = st.session_state.adjacent_count
block_count = total - adjacent + 1

step2_expected_value = factorial(block_count)
step3_expected_value = factorial(adjacent)
final_expected_value = step2_expected_value * step3_expected_value


# --- [2] 헬퍼 함수 정의 섹션 ---
def normalize_factorial_input(value: str) -> str:
    return value.replace(" ", "").replace("\t", "").lower()

def check_factorial_expression(value: str, expected_n: int) -> bool:
    normalized = normalize_factorial_input(value)
    if not normalized.endswith("!"): 
        return False
    number_part = normalized[:-1]
    if not number_part.isdigit(): 
        return False
    return int(number_part) == expected_n

def parse_factorial_input(value: str):
    normalized = normalize_factorial_input(value)
    if normalized.endswith("!"):
        number_part = normalized[:-1]
        if number_part.isdigit(): 
            return int(number_part)
    if normalized.isdigit(): 
        return int(normalized)
    return None

def parse_product_input(value: str):
    normalized = normalize_factorial_input(value).replace("x", "*").replace("×", "*")
    parts = normalized.split("*")
    if len(parts) != 2: 
        return None
    if parts[0].isdigit() and parts[1].isdigit(): 
        return int(parts[0]), int(parts[1])
    return None


# --- [3] 1단계: 문제 설정 UI ---
st.header("1단계: 문제 설정")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="총 인원 수 (N)", value=f"{total} 명")
with col2:
    st.metric(label="이웃할 인원 수 (K)", value=f"{adjacent} 명")
st.info(f"문제: {total}명의 사람을 일렬로 앉힐 때, 특정한 {adjacent}명이 서로 이웃하게 앉는 경우의 수를 구하세요.")


# --- [4] 1.5단계: 직접 묶어보는 탐색 섹션 (형광펜 시각화) ---
st.markdown("---")
st.subheader("🕵️‍♂️ 1.5단계 [아이디어 탐색]: 이웃할 사람들을 직접 묶어봅시다!")
st.markdown(f"아래 선택창에서 이웃하게 만들고 싶은 사람을 딱 **{adjacent}명**만 선택해 보세요.")

# 학생들이 클릭해서 선택할 수 있는 사람 명단 (P1, P2, P3...)
people_list = [f"P{i}" for i in range(1, total + 1)]

selected_neighbors = st.multiselect(
    "이웃으로 묶을 사람을 선택하세요:",
    options=people_list,
    default=people_list[:adjacent], # 초기에 자동으로 앞인원 선택 유도
    max_selections=adjacent
)

# 실시간 주머니 형성 시각화 (Matplotlib)
fig, ax = plt.subplots(figsize=(max(6, total * 1.2), 2))
current_x = 0
box_width = 0.8
gap = 0.3

selected_indices = [people_list.index(p) for p in selected_neighbors]
is_bundle_ready = len(selected_neighbors) == adjacent

if is_bundle_ready:
    min_idx = min(selected_indices)
    max_idx = max(selected_indices)
    
    # 연분홍색 형광펜 주머니 영역 그리기
    bundle_start_x = min_idx * (box_width + gap) - 0.1
    bundle_width = (max_idx - min_idx + 1) * box_width + (max_idx - min_idx) * gap + 0.2
    
    rect_bundle = patches.Rectangle(
        (bundle_start_x, 0.1), bundle_width, 0.8,
        linewidth=2.5, edgecolor='#ff3366', facecolor='#ffe6ec', linestyle='--'
    )
    ax.add_patch(rect_bundle)
    ax.text(bundle_start_x + bundle_width/2, 0.95, "이웃 묶음 (하나의 큰 덩어리!)", 
            color='#ff3366', ha='center', fontweight='bold', fontsize=11)

# 개별 사람 상자 배치
for i, person in enumerate(people_list):
    if person in selected_neighbors:
        facecolor = '#ff99bb'  # 이웃은 분홍색 형광펜 효과
        edgecolor = '#ff3366'
    else:
        facecolor = '#ccffcc'  # 일반 사람은 연두색
        edgecolor = 'black'
        
    rect = patches.Rectangle((current_x, 0.2), box_width, 0.6, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(current_x + box_width/2, 0.5, person, ha='center', va='center', fontsize=12, fontweight='bold')
    current_x += box_width + gap

ax.set_xlim(-0.5, current_x)
ax.set_ylim(0, 1.2)
ax.axis('off')
st.pyplot(fig)
plt.close(fig)

if is_bundle_ready:
    st.success(f"💡 주머니 완성! 이제 {selected_neighbors}번 사람들은 하나로 묶여 함께 움직입니다.")
    st.markdown(f"**🤔 생각해보기:** 이 분홍색 주머니를 **'커다란 1명'**이라고 생각한다면, 일렬로 배열해야 할 덩어리는 총 몇 개로 보이나요?")
    st.markdown(f"➡️ 묶음 주머니(1개) + 남은 일반 사람({total - adjacent}명) = 총 **{block_count}개**의 덩어리!")
else:
    st.warning(f"⚠️ 인원 명단에서 정확히 **{adjacent}명**을 선택해야 주머니가 올바르게 형성됩니다.")

st.markdown("---")

# [보조 계산기 툴팩 - 기존 기능 유지]
with st.expander("🧮 풀이에 필요한 계산기 열기 (팩토리얼 / 곱셈)", expanded=False):
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        with st.form("factorial_calculator", clear_on_submit=False):
            calc_input = st.text_input("팩토리얼 계산기 (예: 5!)", value="")
            if st.form_submit_button("계산하기"):
                parsed_n = parse_factorial_input(calc_input)
                if parsed_n is not None: st.success(f"{parsed_n}! = {factorial(parsed_n)}")
    with col_c2:
        with st.form("product_calculator", clear_on_submit=False):
            product_input = st.text_input("곱셈 계산기 (예: 24x6)", value="")
            if st.form_submit_button("계산하기"):
                parsed_p = parse_product_input(product_input)
                if parsed_p is not None: st.success(f"{parsed_p[0]} × {parsed_p[1]} = {parsed_p[0] * parsed_p[1]}")


# --- [5] 2단계 UI: 외부 블록 배열하기 ---
st.header("2단계: 묶음을 하나의 블록으로 보고 배열하기")
st.write(f"형광펜 주머니를 포함하여 총 **{block_count}개**의 덩어리를 일렬로 배열하는 경우의 수를 구하세요.")

if not st.session_state.step2_correct:
    with st.form("step2_form"):
        col_in1, col_in2 = st.columns(2)
        step2_expr = col_in1.text_input("2단계 식 입력 (n!)", value=st.session_state.step2_expr)
        step2_value = col_in2.number_input("2단계 계산값 입력", min_value=0, step=1, value=int(st.session_state.step2_value))
        if st.form_submit_button("제출"):
            st.session_state.step2_expr, st.session_state.step2_value = step2_expr, step2_value
            if check_factorial_expression(step2_expr, block_count) and step2_value == step2_expected_value:
                st.session_state.step2_correct, st.session_state.step = True, 3
                st.rerun()
            else: 
                st.error("오답입니다. 덩어리 개수를 세어 식(n!)과 계산값을 다시 확인하세요.")
else:
    st.success(f"✔️ 2단계 정답 패스: `{block_count}!` = {step2_expected_value}")


# --- [6] 3단계 UI: 묶음 내부 순서 정하기 ---
if st.session_state.step >= 3:
    st.markdown("---")
    st.header("3단계: 이웃하는 이들끼리 순서 변경하기")
    st.write(f"이제 분홍색 형광펜 주머니 내부를 봅시다. 주머니 속의 **{adjacent}명**이 안에서 자리를 바꾸는 경우의 수를 구하세요.")

    if not st.session_state.step3_correct:
        with st.form("step3_form"):
            col_in1, col_in2 = st.columns(2)
            step3_expr = col_in1.text_input("3단계 식 입력 (n!)", value=st.session_state.step3_expr)
            step3_value = col_in2.number_input("3단계 계산값 입력", min_value=0, step=1, value=int(st.session_state.step3_value))
            if st.form_submit_button("제출"):
                st.session_state.step3_expr, st.session_state.step3_value = step3_expr, step3_value
                if check_factorial_expression(step3_expr, adjacent) and step3_value == step3_expected_value:
                    st.session_state.step3_correct, st.session_state.step = True, 4
                    st.rerun()
                else: 
                    st.error("오답입니다. 주머니 속 인원수를 기준으로 식과 계산값을 확인하세요.")
    else:
        st.success(f"✔️ 3단계 정답 패스: `{adjacent}!` = {step3_expected_value}")


# --- [7] 4단계 UI: 최종 결합 ---
if st.session_state.step >= 4:
    st.markdown("---")
    st.header("4단계: 전체 경우의 수 구하기")
    st.write("외부 덩어리를 배열하는 각 경우마다 내부 배열이 동시에 발생하므로, 두 단계의 값을 곱하여 최종 정답을 구하세요.")

    if not st.session_state.final_correct:
        with st.form("final_form"):
            final_value = st.number_input(f"최종 정답 입력 ({step2_expected_value} × {step3_expected_value})", min_value=0, step=1, value=int(st.session_state.final_value))
            if st.form_submit_button("최종 제출"):
                st.session_state.final_value = final_value
                if final_value == final_expected_value:
                    st.session_state.final_correct = True
                    st.rerun()
                else: 
                    st.error("오답입니다. 곱셈 연산 결과를 다시 계산해 보세요.")
    else:
        st.balloons()
        st.success(f"🎉 모든 단계를 완료했습니다! 최종 정답: {step2_expected_value} × {step3_expected_value} = {final_expected_value} 가지")

st.markdown("---")
st.caption("*이 페이지는 이웃하여 배열하는 순열의 원리를 단계별로 탐색하도록 설계되었습니다.*")