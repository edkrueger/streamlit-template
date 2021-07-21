"""The App."""
import streamlit as st
from resc.resc import add  # pylint: disable=import-error

A = 1
B = 1

st.title("My first app")
st.write(f"{A} + {B} = {add(A, B)}")
