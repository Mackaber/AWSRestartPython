import streamlit as st

st.header("My first app")
st.write("Hello everyone!")

# Input 
name = st.text_input("Enter your name")
submit_clicked = st.button("Submit")

if submit_clicked:
    st.write(f"Hola {name}")