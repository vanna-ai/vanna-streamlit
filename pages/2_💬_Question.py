import vanna as vn
import snowflake.connector
import streamlit as st
import time
from streamlit_ace import st_ace

st.set_page_config(layout="wide")

st.write(st.session_state)

vn.api_key = st.secrets['vanna_api_key']
vn.set_org(st.secrets['org'])

# st.sidebar.title('Organization')

st.image('https://ask.vanna.ai/static/img/vanna_with_text_transparent.png', width=300)
st.write('[Vanna.AI](https://vanna.ai) is a natural language interface to data. Ask questions in natural language and get answers in seconds.')

if st.session_state.get('mark_correct', False):
    st.success('Thanks for marking the question as correct!')
    st.session_state['mark_correct'] = False
    st.stop()

my_question = st.text_input('Question', value=st.session_state.get('my_question', ''), help='Enter a question in natural language')

last_run = st.session_state.get('last_run', None)

if my_question == '' or my_question is None:
    st.info('Enter a question or try one of the examples below')
    if st.button("Who are the top 10 customers by Sales?"):
        my_question = "Who are the top 10 customers by Sales?"
    elif st.button("Who are the top 5 customers by Sales?"):
        my_question = "Who are the top 5 customers by Sales?"

if my_question == '' or my_question is None:
    st.stop()

sql_tab, table_tab, plotly_tab, vanna_tab = st.tabs([':game_die: SQL', ':table_tennis_paddle_and_ball: Table', ':snake: Plotly Code', ':bulb: Vanna Code'])

with vanna_tab:
    st.text('Import Vanna')
    st.code('import vanna as vn', language='python')
    st.text('Generate SQL')
    st.code(f"my_question='{my_question}'\nsql = vn.generate_sql(question=my_question)")
    st.text('Run SQL')
    st.code(f"df = vn.get_results(cs, my_db, sql)")
    st.text('Generate Plotly Code')
    st.code(f"plotly_code = vn.generate_plotly_code(question=my_question, sql=sql, df=df)")
    st.text('Run Chart')
    st.code(f"fig = vn.get_plotly_figure(plotly_code=plotly_code, df=df)")

if my_question == '' or my_question is None:
    pass
elif st.session_state.get('my_question') != my_question and last_run is not None and time.time() - last_run < 20:
    st.error('Wait 20 seconds before trying again')
else:
    same_question_as_before = st.session_state.get('my_question') == my_question

    if not same_question_as_before:
        st.session_state['my_question'] = my_question
        st.session_state['last_run'] = time.time()

        with st.spinner('Generating SQL...'):
            sql = vn.generate_sql(question=my_question)
            st.session_state['sql'] = sql
    else:
        sql = st.session_state.get('sql')

    if not sql:
        with sql_tab:
            st.error('SQL error')
    else:
        with sql_tab:
            # st.code(sql, language='sql', line_numbers=True)
            updated_sql = st_ace(sql, language='sql', theme='twilight')

            print("updated_sql", updated_sql)
            if updated_sql != sql:
                print("updated_sql != sql")
                st.session_state['sql'] = updated_sql
                sql = updated_sql
        # with table_tab:
            # st.header('Table')

        with st.spinner('Running SQL...'):
            conn = snowflake.connector.connect(
                    user=st.secrets['snowflake_user'],
                    password=st.secrets['snowflake_password'],
                    account=st.secrets['snowflake_account'],
                    database=st.secrets['snowflake_default_database'],
                )

            cs = conn.cursor()

            df = vn.get_results(cs, st.secrets['snowflake_default_database'], sql)

        if df is None:
            st.error('Table error')
        elif isinstance(df, str):
            st.error(df)
        else:
            with table_tab:
                st.text('First 100 rows of data')
                st.dataframe(df.head(100))

            # with plotly_tab:
            #     st.header('Plotly Code')                

            with st.spinner('Generating Plotly Code...'):
                plotly_code = vn.generate_plotly_code(question=my_question, sql=sql, df=df)

            if not plotly_code:
                with plotly_tab:
                    st.error('Plotly Code error')
            else:
                with plotly_tab:
                    st.code(plotly_code, language='python')

                st.header('Chart')
                with st.spinner('Running Chart...'):
                    fig = vn.get_plotly_figure(plotly_code=plotly_code, df=df)
                    
                if fig is None:
                    st.error('Chart error')
                else:
                    st.plotly_chart(fig)

                    def mark_correct():
                        st.session_state['mark_correct'] = True

                    st.button('Mark as correct', on_click=mark_correct)

