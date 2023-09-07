import streamlit as st

# st.sidebar.header("Settings")
# st.markdown("# Settings")

if st.session_state.get('api_key', None) is None:
    st.markdown("[Login](/login)")
    st.stop()

genre = st.radio(
    "Choose a dataset to use",
    ('Comedy', 'Drama', 'Documentary'))