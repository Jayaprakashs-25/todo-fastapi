import subprocess
import streamlit as st

st.title("FastAPI Backend Running")
subprocess.Popen(["uvicorn", "todo_fastapi:app", "--host", "0.0.0.0", "--port", "8000"])
st.success("FastAPI server Started")
