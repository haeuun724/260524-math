import random
from math import factorial
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PAGE_TITLE = "이웃하는 순열 - 모든 경우의 수 즉시 탐색"
st.set_page_config(page_title=PAGE_TITLE, layout="wide")

st.title("🕵️‍♂️ 이웃하는 순열: 무작위 조건 및 모든 배치 탐색")
st.markdown("""
[새로운 문제 생성] 버튼을 누르면 5명 이내의 무작위 조건이 설정됩니다.
조건에 맞는 **모든 배치 형태(경우의 수 전체)**가 아래에 즉시 시각화됩니다. 
빨간색 형광펜 주머니가 어떻게 묶여서 이동하는지 관찰해 보세요!
""")

# --- 1. Session State 초기화 (무작위 상태 저장) ---
if "rand_total" not in st.session_state:
    st.session_state.rand_total = 4
    st.session_state.rand_adjacent = 2

def generate_random_condition():
    # 총 인원 3~5명 사이 무작위
    total = random.randint(3, 5)
    # 이웃할 인원수 2~4명 사이 (단, 총 인원보다는 작거나 같게)
    max_adj = min(4, total)
    adjacent = random.randint(2, max_adj)
    
    st.session_state.rand_total = total
    st.session_state.rand_adjacent = adjacent

# --- 2. 컨트롤러 버튼 ---
if st.button("🔄 새로운 문제 생성 (조건 무작위 변경)"):
    generate_random_condition()
    st.rerun()

# 현재 적용된 무작위 값 가져오기
total = st.session_state.rand_total
adjacent = st.session_state.rand_adjacent
block_count = total - adjacent + 1
case_count = factorial(block_count) * factorial(adjacent)

# 화면 상단에 현재 무작위 문제 상황 브리핑
st.subheader("📌 오늘의 무작위 탐색 조건")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="총 인원 수 (N)", value=f"{total} 명")
with col2:
    st.metric(label="이웃할 인원 수 (K)", value=f"{adjacent} 명")
with col3:
    st.metric(label="총 경우의 수", value=f"{case_count} 가지")

st.info(f"👉 **수학적 공식 원리:** 외부 덩어리 배열 단계 `{block_count}! ({factorial(block_count)}가지)` × 묶음 내부 배열 단계 `{adjacent}! ({factorial(adjacent)}가지)` = **{case_count}가지**")

st.markdown("---")

# --- 3. 순열 생성 알고리즘 ---
def get_all_permutations(items):
    if len(items) == 0:
        return [[]]
    result = []
    for i in range(len(items)):
        current = items[i]
        remaining = items[:i] + items[i+1:]
        for p in get_all_permutations(remaining):
            result.append([current] + p)
    return result

blocks = list(range(1, block_count + 1))
all_block_perms = get_all_permutations(blocks)
all_internal_perms = get_all_permutations(list(range(1, adjacent + 1)))

# --- 4. 형광펜 효과가 적용된 미니 배치도 그리기 ---
def draw_highlighted_arrangement(block_order, internal_order, idx):
    # 인원수에 맞게 가로 크기 동적 조절
    fig, ax = plt.subplots(figsize=(total * 0.7, 0.9))
    
    current_x = 0
    box_width = 0.45
    gap = 0.12
    
    for block_id in block_order:
        if block_id == 1:  # 1번 블록이 '이웃 그룹 묶음'인 경우 (형광펜 하이라이트 적용)
            # 형광펜으로 크게 감싼 주머니 (연한 핑크색 배경 + 빨간 점선 테두리)
            bundle_width = adjacent * box_width + (adjacent - 1) * 0.03 + 0.08
            rect_bundle = patches.Rectangle(
                (current_x - 0.04, 0.08), bundle_width, 0.84, 
                linewidth=2, edgecolor='#ff3366', facecolor='#ffe6ec', linestyle='--'
            )
            ax.add_patch(rect_bundle)
            
            # 주머니 내부 멤버들 그리기
            internal_x = current_x
            for internal_id in internal_order:
                rect = patches.Rectangle((internal_x, 0.18), box_width, 0.6, facecolor='#ff99bb', edgecolor='black')
                ax.add_patch(rect)
                ax.text(internal_x + box_width/2, 0.48, f"I{internal_id}", ha='center', va='center', fontsize=9, fontweight='bold', color='black')
                internal_x += box_width + 0.03
            current_x += bundle_width + gap
        else:  # 일반 사람일 때 (연한 초록색)
            rect = patches.Rectangle((current_x, 0.18), box_width, 0.6, facecolor='#ccffcc', edgecolor='black')
            ax.add_patch(rect)
            ax.text(current_x + box_width/2, 0.48, f"P{block_id-1}", ha='center', va='center', fontsize=9, fontweight='bold', color='black')
            current_x += box_width + gap
            
    ax.set_xlim(-0.2, current_x)
    ax.set_ylim(0, 1.1)
    ax.axis('off')
    ax.set_title(f"Case {idx}", fontsize=10, pad=4, fontweight='bold')
    return fig

# --- 5. 바둑판(Grid) 형태로 모든 배치 즉시 출력 ---
st.subheader(f"📊 가능한 {case_count}가지 배치 형태 전체 목록")

# 한 줄에 3개씩 배치되도록 설정
cols_per_row = 3
cols = st.columns(cols_per_row)

case_idx = 1
for block_perm in all_block_perms:
    for internal_perm in all_internal_perms:
        col_to_use = cols[(case_idx - 1) % cols_per_row]
        
        with col_to_use:
            fig = draw_highlighted_arrangement(block_perm, internal_perm, case_idx)
            st.pyplot(fig)
            plt.close(fig)  # 메모리 과부하 방지
            
        case_idx += 1

st.markdown("---")
st.markdown("""
### 👩‍🏫 수업 실연 활용 코칭 가이드
교수님 앞에서 스크린을 조작하며 이렇게 발문해 보세요.

1. **"여러분, [🔄 새로운 문제 생성] 버튼을 누르니 이번엔 총 4명 중 3명이 이웃하는 상황이 되었네요."**
2. **"아래 펼쳐진 Case들을 보세요. 핑크색 형광펜 주머니 보이시나요? 어떤 배치를 보더라도 이 핑크색 주머니는 찢어지지 않고 한 덩어리로 움직입니다."**
3. **"Case 1, 2, 3을 연달아 보면 일반 사람 P1의 위치는 똑같은데, 형광펜 주머니 안에서 I1, I2, I3의 순서만 슉슉 바뀌고 있죠? 이게 바로 우리가 배운 '내부 배열의 수'가 전체 틀마다 곱해지는 원리입니다!"**
""")