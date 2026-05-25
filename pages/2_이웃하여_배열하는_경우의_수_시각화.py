if st.session_state.step >= 4:
    st.markdown("---")
    st.header("4단계: 전체 경우의 수 구하기 및 결과 탐색")
    st.markdown("💡 **아이디어 종합:** 덩어리를 배열하는 각 경우마다(2단계), 묶음 내부의 배열(3단계)이 동시에 일어납니다. 따라서 두 값을 **곱해야** 합니다.")

    if not st.session_state.final_correct:
        with st.form("final_form"):
            final_value = st.number_input(f"최종 정답 ({step2_expected_value} × {step3_expected_value})", min_value=0, step=1, value=int(st.session_state.final_value))
            if st.form_submit_button("최종 제출"):
                st.session_state.final_value = final_value
                if final_value == final_expected_value:
                    st.session_state.final_correct = True
                    st.rerun()
                else: 
                    st.error("오답입니다. 곱셈 결과를 다시 계산해 보세요.")
    else:
        st.balloons()
        st.success(f"🎉 축하합니다! 최종 정답입니다: **{final_expected_value:,}** 가지")

        st.markdown("---")
        st.subheader("🕵️‍♂️ 결과 탐색 도구: 실제 배치를 확인해봅시다")
        st.write(f"우리가 구한 {final_expected_value:,}가지의 경우 중 궁금한 배치의 순서를 선택하여 시각적으로 확인해 보세요.")

        # 슬라이더로 몇 번째 경우가 궁금한지 입력받는 부분
        selected_nth = st.slider(
            "확인하고 싶은 배치 번호를 선택하세요:", 
            1, final_expected_value, 
            value=random.randint(1, final_expected_value)
        )
        
        # 입력받은 번호를 바탕으로 순열 역산 (Lehmer code 기반 복원)
        k_zero_based = selected_nth - 1
        block_k = k_zero_based // step3_expected_value
        internal_k = k_zero_based % step3_expected_value

        current_block_order = get_nth_permutation(block_count, block_k)
        current_internal_order = get_nth_permutation(adjacent, internal_k)

        # 시각화 출력
        fig = plot_single_arrangement(total, adjacent, current_block_order, current_internal_order, selected_nth)
        st.pyplot(fig)
        
        st.caption(f"그림 설명: 'I'는 이웃해야 할 내부 멤버(빨간 점선 주머니 안), 'P'는 나머지 일반 멤버입니다. 슬라이더를 움직이면 다른 배치 형태를 볼 수 있습니다.")

st.markdown("---")
st.caption("*이 페이지는 이웃하여 배열하는 순열의 원리를 단계별로 학습하도록 설계되었습니다.*")