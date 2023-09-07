import streamlit as st
import vanna as vn
import os
import time


# Vanna Setup
vn.set_api_key(st.secrets.get('vanna_api_key'))
vn.set_model('thelook')
vn.connect_to_bigquery(
    project_id=st.secrets.get('gcp_project_id'),
)


# FUNCTIONS
@st.cache_data
def generate_questions_cached():
    return vn.generate_questions()

@st.cache_data
def generate_sql_cached(question: str):
    return vn.generate_sql(question=question)

@st.cache_data
def run_sql_cached(sql: str):
    return vn.run_sql(sql=sql)

@st.cache_data
def generate_plotly_code_cached(question, sql, df):
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code

@st.cache_data
def generate_plot_cached(code, df):
    return vn.get_plotly_figure(plotly_code=code, df=df)

@st.cache_data
def generate_followup_cached(question, df):
    return vn.generate_followup_questions(question=question, df=df)


st.sidebar.title('Output Settings')
st.sidebar.checkbox('Show SQL', value=True, key='show_sql')
st.sidebar.checkbox('Show Table', value=True, key='show_table')
st.sidebar.checkbox('Show Plotly Code', value=False, key='show_plotly_code')
st.sidebar.checkbox('Show Chart', value=False, key='show_chart')
st.sidebar.checkbox('Show Follow-up Questions', value=True, key='show_followup')

st.title('Vanna AI')
st.sidebar.write(st.session_state)

assistant_message_suggested = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
if assistant_message_suggested.button("Click to show suggested questions"):
    questions = generate_questions_cached()
    for question in questions:
        time.sleep(0.05)
        assistant_message_suggested.write(question)

my_question = st.chat_input("Ask me a question about your data")
if my_question:
    user_message = st.chat_message("user")
    user_message.write(f"{my_question}")

    sql = generate_sql_cached(question=my_question)

    with st.spinner('Generating SQL...'):
        sql = vn.generate_sql(question=my_question)

    if sql:
        if st.session_state.get('show_sql', True):
            assistant_message_sql = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
            assistant_message_sql.code(sql, language='sql', line_numbers=True)

        with st.spinner('Running Query...'):
            df = run_sql_cached(sql=sql)

        if df is not None:
            if st.session_state.get('show_table', True):
                assistant_message_table = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
                if len(df) > 10:
                    assistant_message_table.text('First 10 rows of data')
                    assistant_message_table.dataframe(df.head(10))
                else:
                    assistant_message_table.dataframe(df)

            code = generate_plotly_code_cached(question=my_question, sql=sql, df=df)

            if st.session_state.get('show_plotly_code', False):
                assistant_message_plotly_code = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
                assistant_message_plotly_code.code(code, language='python', line_numbers=True)                

            if st.session_state.get('show_chart', True):
                fig = generate_plot_cached(code=code, df=df)
                assistant_message_chart = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
                if fig is not None:
                    assistant_message_chart.plotly_chart(fig)
                else:
                    assistant_message_chart.error("I couldn't generate a chart")

            if st.session_state.get('show_followup', True):
                assistant_message_followup = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
                followup_questions = generate_followup_cached(question=my_question, df=df)

                if len(followup_questions) > 0:
                    assistant_message_followup.text('Here are some possible follow-up questions')
                    # Print the first 5 follow-up questions
                    for question in followup_questions[:5]:
                        time.sleep(0.05)
                        assistant_message_followup.write(question)

    else:
        assistant_message_error = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
        assistant_message_error.error("I wasn't able to generate SQL for that question")
