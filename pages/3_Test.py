import streamlit as st
import uuid
from streamlit_ace import st_ace

print("Begin")
print(f"val1 session={st.session_state.get('val1')}")
print(f"val2 session={st.session_state.get('val2')}")


def on_change():
    print("Changed")
    print(f"val1={val1}")
    print(f"val2={val2}")
    print(f"val1 session={st.session_state.get('val1')}")
    print(f"val2 session={st.session_state.get('val2')}")
    st.write("Changed")

def on_click():
    print("Clicked")
    st.write("Clicked")

st.write(st.session_state)

st.write(str(uuid.uuid4()))

val1 = st_ace(language='sql', theme='twilight', key='val1')

st.write(str(uuid.uuid4()))

st.write(val1)

st.write(str(uuid.uuid4()))

val2 = st.text_input("Box 2", key='val2', on_change=on_change)

st.write(str(uuid.uuid4()))

st.write(val2)

st.write(str(uuid.uuid4()))

x = st.button("Click me", key='save', on_click=on_click)

st.write(str(uuid.uuid4()))

st.write(x)

st.write(str(uuid.uuid4()))
