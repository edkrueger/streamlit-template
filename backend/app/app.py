"""The App."""
import streamlit as st
import package  # pylint: disable=import-error

A = 1
B = 1

st.title("My first app")
st.write(f"{A} + {B} = {package.add(A, B)}")
