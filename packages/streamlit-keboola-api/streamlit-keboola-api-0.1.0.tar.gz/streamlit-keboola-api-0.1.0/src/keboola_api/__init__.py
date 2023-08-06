from pathlib import Path
from pickletools import uint4
from tkinter.tix import StdButtonBox
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components
from kbcstorage.client import Client


def upload(url,key,table_name,bucket_id,file_path,primary_key):
    with st.spinner("uploading..."):
        client = Client(url, key)
        try:
            return client.tables.create(name=table_name,
                                bucket_id=bucket_id,
                                file_path=file_path,
                                primary_key=primary_key) + " successfully created!!"
        except Exception as e:
            return str(e)   

def list_buckets(keboola_URL,keboola_key):
    with st.spinner("Getting Buckets..."):
        client = Client(keboola_URL, keboola_key)
        try:
            return client.buckets.list()
        except Exception as e:
            return str(e)  

def list_tables(keboola_URL,keboola_key):
    with st.spinner("Getting Tables..."):
        client = Client(keboola_URL, keboola_key)
        try:
            return client.tables.list()
        except Exception as e:
            return str(e)  

frontend_dir = (Path(__file__).parent / "frontend").absolute()

_component_func = components.declare_component(
	"keboola_api", path=str(frontend_dir)
)


def keboola_table_list(
    keboola_URL: str,
    keboola_key:str,
    key: str,
    label:Optional[str] = None,
):

    component_value = _component_func(label=label,default="",key=key)  
    if st.session_state.get(key) is not None:
        if st.session_state.get('_'+key)!=st.session_state[key]:
            st.session_state['_'+key]=component_value
            ret= list_tables(keboola_URL,keboola_key)
            st.session_state['__'+key]=ret
            return ret
        return st.session_state['__'+key]
    return ""

def keboola_bucket_list(
    keboola_URL: str,
    keboola_key:str,
    key: str,
    label:Optional[str] = None,
):

    component_value = _component_func(label=label,default="",key=key)  
    if st.session_state.get(key) is not None:
        if st.session_state.get('_'+key)!=st.session_state[key]:
            st.session_state['_'+key]=component_value
            ret= list_buckets(keboola_URL,keboola_key)
            st.session_state['__'+key]=ret
            return ret
        return st.session_state['__'+key]
    return ""

def keboola_upload(
    keboola_URL: str,
    keboola_key:str,
    keboola_table_name:str,
    keboola_bucket_id:str,
    keboola_file_path:str,
    keboola_primary_key:list,
    key: str,
    action: Optional[str] = "UPLOAD",
    label:Optional[str] = None,
):
    if label is None:
        label=action 
    component_value = _component_func(label=label,default="",key=key)  
    if st.session_state.get(key) is not None:
        if st.session_state.get('_'+key)!=st.session_state[key]:
            st.session_state['_'+key]=component_value
            ret= upload(keboola_URL,keboola_key,keboola_table_name,keboola_bucket_id,keboola_file_path,keboola_primary_key)
            st.session_state['__'+key]=ret
            return ret
        return st.session_state['__'+key]
    return ""


