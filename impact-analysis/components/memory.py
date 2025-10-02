
import streamlit as st

def get_value(key):
    if key not in st.session_state:
        st.session_state[key] = None
    return st.session_state[key]

def get_array(key):
    if key not in st.session_state:
        st.session_state[key] = []
    return st.session_state[key]

def get_object(key):
    if key not in st.session_state:
        st.session_state[key] = {}
    return st.session_state[key]

def get_json(key):
    if key not in st.session_state:
        st.session_state[key] = None
    return st.session_state[key]

def set_json(key, value):
    if key not in st.session_state:
        st.session_state[key] = {}
    st.session_state[key] = value

def set(key, value):
    st.session_state[key] = value

def set_array(key, value):
    if key not in st.session_state:
        st.session_state[key] = []
    st.session_state[key].append(value)

def set_object(key, value):
    if key not in st.session_state:
        st.session_state[key] = {}
    st.session_state[key].update(value)

def clear(key):
    if key in st.session_state:
        del st.session_state[key]

def clear_array(key):
    if key in st.session_state:
        st.session_state[key] = []

def clear_object(key):
    if key in st.session_state:
        st.session_state[key] = {}

def clear_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def clear_all_except(exceptions):
    for key in list(st.session_state.keys()):
        if key not in exceptions:
            del st.session_state[key]


