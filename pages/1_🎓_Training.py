import streamlit as st
from streamlit_ace import st_ace
import snowflake.connector
import vanna as vn

def save():
    training_question = st.session_state.get('training_question')
    if training_question is not None and training_question != '':
        vn.store_sql(question=training_question, sql=sql)
        st.success(f"Saved '{training_question}' as '{st.session_state.get('sql','')[0:100]}'")
        st.session_state['training_question'] = ''
        st.session_state['sql'] = ''

@st.cache_data()
def get_data(sql):
    df = vn.get_results(cs, st.secrets['snowflake_default_database'], sql)
    return df

@st.cache_data()
def get_question(sql):
    return vn.generate_question(sql)

st.set_page_config(layout="wide")

st.sidebar.header("Training")
st.markdown("# Training")

st.header("SQL")
sql = st_ace(value=st.session_state.get('sql', ''), language='sql', theme='twilight', key='sql')

if not sql or sql == '':
    st.stop()

# Try to run the SQL
conn = snowflake.connector.connect(
        user=st.secrets['snowflake_user'],
        password=st.secrets['snowflake_password'],
        account=st.secrets['snowflake_account'],
        database=st.secrets['snowflake_default_database'],
    )

cs = conn.cursor()

with st.spinner('Running SQL...'):
    df = get_data(sql)

if df is None:
    st.error('Table error')
elif isinstance(df, str):
    st.error(df)
else:
    st.text('First 100 rows of data')
    st.dataframe(df.head(100))

    with st.spinner('Generating Question...'):
        question = get_question(sql)

        st.header("AI-Generated Question based on the SQL")
        st.write(question)

    st.text_input("Question", question, key='training_question')
    st.button("Save", on_click=save)
