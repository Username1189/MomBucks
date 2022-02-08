import streamlit as st

from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData

import socket
import pandas as pd
from datetime import datetime


def done(mombucks, num, total, subadd, reason):
    if st.button("Done"):
        if subadd:
            st.session_state.add = False
        else:
            st.session_state.sub = False
        mombucks.seek(0)
        mombucks.truncate(0)
        mombucks.write(f"{int(total) + int(num)}")
        file = pd.read_csv("Tracker.csv")

        now = datetime.now().strftime("%H:%M:%S")
        data = {"DateTime": str(now), "For": str(reason), "Num": int(num)}
        file = file.append(data, ignore_index=True)
        file.to_csv("Tracker.csv", index=False)
        raise RerunException(RerunData())


def add(mombucks, nummombucks, reason):
    st.session_state.add = True
    mombucksadded = st.number_input("Number of Mom Bucks To Add: ", 0)
    done(mombucks, mombucksadded, nummombucks, True, reason)


def sub(mombucks, nummombucks, reason):
    st.session_state.sub = True
    mombucksadded = st.number_input("Number of Mom Bucks To Subtract: ", 0)
    done(mombucks, -mombucksadded, nummombucks, False, reason)


def run():
    if st.text_input("Password: ") != "1234":
        return
    mombucks = open("MomBucksTraker", "r+")
    nummombucks = mombucks.read()
    st.subheader("Sanjay has MomBucks: " + str(nummombucks))
    st.subheader(f"Which is equal to {int(nummombucks) / 10} rupees")
    if 'sub' not in st.session_state: st.session_state.sub = False
    if 'add' not in st.session_state: st.session_state.add = False
    if socket.gethostname() == "pybox":
        if st.button("Add") or st.session_state.add:
            reason = st.text_input("Reason: ")
            add(mombucks, nummombucks, reason)
        if st.button("Subtract") or st.session_state.sub:
            reason = st.text_input("Reason: ")
            sub(mombucks, nummombucks, reason)
