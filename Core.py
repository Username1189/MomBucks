import streamlit as st

from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData

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


def add(reason):
    with open("MomBucksTraker", "r+") as mombucks:
        nummombucks = mombucks.read()
        st.session_state.add = True
        mombucksadded = st.number_input("Number of Mom Bucks To Add: ", 0)
        done(mombucks, mombucksadded, nummombucks, True, reason)


def sub(reason):
    with open("MomBucksTraker", "r+") as mombucks:
        nummombucks = mombucks.read()
        st.session_state.sub = True
        mombucksadded = st.number_input("Number of Mom Bucks To Subtract: ", 0)
        done(mombucks, -mombucksadded, nummombucks, False, reason)


def log():
    st.table(pd.read_csv("Tracker.csv").to_dict())
    st.write("Total Lines: " + str(pd.read_csv("Tracker.csv").size))


def run():
    if st.text_input("Password: ") != "123456": return

    with open("MomBucksTraker", "r+") as mombucks:
        nummombucks = mombucks.read()

        if st.button("Log"):
            log()
            if not st.button("Back"): return
        st.subheader("Sanjay has MomBucks: " + str(nummombucks))
        st.subheader(f"Which is equal to {int(nummombucks) / 10} rupees")

        if 'sub' not in st.session_state: st.session_state.sub = False
        if 'add' not in st.session_state: st.session_state.add = False
        if st.button("Add") or st.session_state.add:
            reason = st.text_input("Reason: ")
            add(reason)
        if st.button("Subtract") or st.session_state.sub:
            reason = st.text_input("Reason: ")
            sub(reason)
