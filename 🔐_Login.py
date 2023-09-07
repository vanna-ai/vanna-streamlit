import vanna as vn
import snowflake.connector
import streamlit as st
import time
from streamlit_ace import st_ace
import model

st.markdown("""
| GitHub | PyPI | Colab | Documentation |
| ------ | ---- | ----- | ------------- |
| [![GitHub](https://img.shields.io/badge/GitHub-vanna--py-blue?logo=github)](https://github.com/vanna-ai/vanna-py) | [![PyPI](https://img.shields.io/pypi/v/vanna?logo=pypi)](https://pypi.org/project/vanna/) | [![Colab](https://img.shields.io/badge/Colab-vanna--py-blue?logo=google-colab)](https://colab.research.google.com/github/vanna-ai/vanna-py/blob/main/notebooks/vn-starter.ipynb) | [![Documentation](https://img.shields.io/badge/Documentation-vanna--py-blue?logo=read-the-docs)](https://docs.vanna.ai) |
""")

if st.session_state.get('api_key', None) is None:
    st.write('Login Required')

    st.text_input('Email', key='email')

    if st.session_state.get('email', None) is not None and st.session_state['email'] != '':
        if st.session_state.get('code', None) is not None and st.session_state['code'] != '':
            with st.spinner('Logging in...'):
                time.sleep(3)
                st.session_state['api_key'] = '1234'
                st.success('Logged in!')
                st.experimental_rerun()
        else:
            st.info('Code emailed to: ' + st.session_state['email'] + ". Check your spam folder if you don't see it.")
            st.text_input('Code', key='code')

            st.stop()
    else:
        st.stop()

st.write(st.session_state)

st.markdown("""
* [Training](/Training)
""")