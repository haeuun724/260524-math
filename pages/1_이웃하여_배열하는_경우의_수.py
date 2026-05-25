import random
from math import factorial

import streamlit as st

PAGE_TITLE = "순열 문제 풀이 - 이웃하여 배열하는 경우의 수"

st.title(PAGE_TITLE)

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
    total = random.randint(5, 20)
    adjacent = random.randint(1, total)
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


if st.button("재설정"):
    reset_problem()

if st.session_state.total_people == 0:
    reset_problem()


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


def render_arrangement_diagram(total: int, adjacent: int):
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
    except ImportError:
        return None

    block_count = total - adjacent + 1
    other_count = block_count - 1
    other_labels = [f"P{i+1}" for i in range(other_count)]
    labels = other_labels + ["이웃 그룹"] if other_labels else ["이웃 그룹"]

    fig, axes = plt.subplots(2, 1, figsize=(max(6, block_count * 0.9), 4))

    def draw_boxes(ax, labels, title):
        box_width = 1.0
        box_height = 0.8
        for index, label in enumerate(labels):
            color = "salmon" if label == "이웃 그룹" else "skyblue"
            rect = Rectangle((index * box_width, 0), box_width, box_height, facecolor=color, edgecolor="black")
            ax.add_patch(rect)
            ax.text(index * box_width + box_width / 2, box_height / 2, label, ha="center", va="center", fontsize=10)
        ax.set_xlim(0, len(labels) * box_width)
        ax.set_ylim(0, box_height)
        ax.axis("off")
        ax.set_title(title, fontsize=10, pad=10)

    draw_boxes(axes[0], labels, "블록 단위 배열 예시")
    internal_labels = [str(i + 1) for i in range(adjacent)]
    draw_boxes(axes[1], internal_labels, "이웃 그룹 내부 순서 예시")
    plt.tight_layout()
    return fig


total = st.session_state.total_people
adjacent = st.session_state.adjacent_count
block_count = total - adjacent + 1
step2_expected_expr = f"{block_count}!"
step2_expected_value = factorial(block_count)
step3_expected_expr = f"{adjacent}!"
step3_expected_value = factorial(adjacent)
final_expected_value = step2_expected_value * step3_expected_value

st.header("1단계: 문제 설정")
st.markdown("- 문제의 인원수와 이웃 인원수를 랜덤으로 설정합니다.")
st.info(
    f"**총 인원 수:** {total}명\n\n**이웃하게 앉을 인원 수:** {adjacent}명"
)

st.markdown("---")

st.subheader("*팩토리얼 계산기*")
st.write("필요한 경우에 사용하세요.")
with st.form("factorial_calculator", clear_on_submit=False):
    calc_input = st.text_input(
        "계산기 입력: n! 형식으로 입력하세요",
        value="",
        help="예: 7!",
    )
    calc_submit = st.form_submit_button("계산하기")

    if calc_submit:
        parsed_n = parse_factorial_input(calc_input)
        if parsed_n is None:
            st.error("입력 형식이 올바르지 않습니다. n! 형식으로 입력해주세요.")
        else:
            calc_value = factorial(parsed_n)
            st.success(f"{parsed_n}! = {calc_value}")
            st.write(f"입력한 표현식: `{parsed_n}!`")

st.markdown("---")

st.subheader("*계산기*")
st.write("필요한 경우에 사용하세요.")
with st.form("product_calculator", clear_on_submit=False):
    product_input = st.text_input(
        "계산기 입력: nxm 형식으로 입력하세요",
        value="",
        help="예: 3x4",
    )
    product_submit = st.form_submit_button("계산하기")

    if product_submit:
        parsed_product = parse_product_input(product_input)
        if parsed_product is None:
            st.error("입력 형식이 올바르지 않습니다. nxm 형식으로 입력해주세요.")
        else:
            a, b = parsed_product
            st.success(f"{a} × {b} = {a * b}")
            st.write(f"입력한 표현식: `{a}x{b}`")

st.markdown("---")

st.header("2단계: 묶음을 하나의 블록으로 보고 배열하기")
st.write(
    "이웃하는 사람들을 하나의 묶음으로 생각하고, 전체를 일렬로 배열하는 경우의 수를 구하세요."
)

if not st.session_state.step2_correct:
    with st.form("step2_form"):
        step2_expr = st.text_input(
            "2단계 (표현): n! 형식으로 입력하세요",
            value=st.session_state.step2_expr,
        )
        step2_value = st.number_input(
            "2단계 (계산값): n!을 계산한 값을 숫자로 입력하세요",
            min_value=0,
            step=1,
            value=int(st.session_state.step2_value),
        )
        submit_step2 = st.form_submit_button("제출")

        if submit_step2:
            st.session_state.step2_expr = step2_expr
            st.session_state.step2_value = step2_value
            expr_ok = check_factorial_expression(step2_expr, block_count)
            value_ok = step2_value == step2_expected_value
            if expr_ok and value_ok:
                st.session_state.step2_correct = True
                st.session_state.step = 3
                st.success("정답입니다! 이제 3단계로 이동하세요.")
            else:
                st.error(
                    "오답입니다. n! 형식과 계산값을 다시 확인하고 다시 제출해 주세요."
                )
else:
    st.success(
        f"정답을 맞혔습니다. 2단계 정답: `{step2_expected_expr}` = {step2_expected_value}"
    )

if st.session_state.step >= 3:
    st.markdown("---")
    st.header("3단계: 이웃하는 이들끼리 순서 변경하기")
    st.write(
        "이웃한 사람들끼리 서로의 순서를 바꿔 앉을 경우의 수를 구하세요."
    )

    if not st.session_state.step3_correct:
        with st.form("step3_form"):
            step3_expr = st.text_input(
                "3단계 (표현): n! 형식으로 입력하세요",
                value=st.session_state.step3_expr,
            )
            step3_value = st.number_input(
                "3단계 (계산값): n!을 계산한 값을 숫자로 입력하세요",
                min_value=0,
                step=1,
                value=int(st.session_state.step3_value),
            )
            submit_step3 = st.form_submit_button("제출")

            if submit_step3:
                st.session_state.step3_expr = step3_expr
                st.session_state.step3_value = step3_value
                expr_ok = check_factorial_expression(step3_expr, adjacent)
                value_ok = step3_value == step3_expected_value
                if expr_ok and value_ok:
                    st.session_state.step3_correct = True
                    st.session_state.step = 4
                    st.success("정답입니다! 이제 최종 단계로 이동하세요.")
                else:
                    st.error(
                        "오답입니다. n! 형식과 계산값을 다시 확인하고 다시 제출해 주세요."
                    )
    else:
        st.success(
            f"정답을 맞혔습니다. 3단계 정답: `{step3_expected_expr}` = {step3_expected_value}"
        )

if st.session_state.step >= 4:
    st.markdown("---")
    st.header("4단계: 전체 경우의 수 구하기")
    st.write(
        "2단계에서 구한 경우와 3단계에서 구한 경우를 곱한 값을 최종 정답으로 입력하세요."
    )

    if not st.session_state.final_correct:
        with st.form("final_form"):
            final_value = st.number_input(
                "최종 정답: 숫자로만 입력하세요",
                min_value=0,
                step=1,
                value=int(st.session_state.final_value),
            )
            submit_final = st.form_submit_button("제출")

            if submit_final:
                st.session_state.final_value = final_value
                if final_value == final_expected_value:
                    st.session_state.final_correct = True
                    st.success("정답입니다! 모든 단계를 완료했습니다.")
                else:
                    st.error("오답입니다. 다시 계산해서 입력해 주세요.")
    else:
        st.success(
            f"최종 정답입니다: {step2_expected_value} × {step3_expected_value} = {final_expected_value}"
        )
        diagram = render_arrangement_diagram(total, adjacent)
        if diagram is not None:
            st.pyplot(diagram)

st.markdown("---")
st.caption(
    "*이 페이지는 단계별로 이웃하여 배열하는 경우의 수를 학습하도록 설계되었습니다.*"
) st.subheader("🕵️‍♂️ 결과 탐색 도구: 실제 배치를 확인해봅시다")
st.write(f"우리가 구한 {final_expected_value:,}가지의 경우 중 하나를 선택해서 시각적으로 확인해 보세요.")

# --- 핵심 대안: 슬라이더를 통해 몇 번째 경우가 궁금한지 입력받는 부분 ---
selected_nth = st.slider("확인하고 싶은 배치 번호를 선택하세요:", 
                        1, final_expected_value, 
                        value=random.randint(1, final_expected_value))

# ... (중략: 선택한 번호의 배치 상태를 수학적으로 계산하는 로직) ...

# --- 입력한 번호에 맞는 '단 하나의 배치'를 시각화하여 보여주는 부분 ---
fig = plot_single_arrangement(total, adjacent, current_block_order, current_internal_order, selected_nth)
st.pyplot(fig)
