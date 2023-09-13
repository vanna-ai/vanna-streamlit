import os
import streamlit as st
import vanna as vn
from dotenv import load_dotenv


@st.cache_resource(ttl=3600)
def setup_connexion():
    if "vanna_api_key" in st.secrets and "gcp_project_id" in st.secrets:
        vn.set_api_key(st.secrets.get("vanna_api_key"))
        vn.set_model("thelook")
        vn.connect_to_bigquery(
            project_id=st.secrets.get("gcp_project_id"),
        )

    else:
        load_dotenv()
        vn.set_api_key(os.environ.get("VANNA_API_KEY"))
        vn.set_model("thelook")
        vn.connect_to_bigquery(
            project_id=os.environ.get("GCP_PROJECT_ID"),
        )


def setup_session_state():
    st.session_state["my_question"] = None
