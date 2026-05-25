import streamlit as st

st.title("순열을 통한 문제 풀이")

st.subheader("1. 순열이란?")
st.write("- 서로 다른 n개에서 r(0<r<=n)개를 택하여 일렬로 나열하는 것은 n개에서 r개를 택하는 순열")
st.write("- nPr = n(n-1) x ... x (n-r+1)")

st.subheader("2. 계승이란?")
st.write("- nPn = n(n-1) x ... x 2 x 1, 1부터 n까지의 자연수를 차례로 곱한 것 = n의 계승 = n!")
st.write("- nP0 = 1")
st.write("- 0! = 1")
st.write("- nPr = n! / (n-r)! (단, 0<=r<=n)")
