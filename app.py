import streamlit as st
from datetime import datetime
from vega_datasets import data
from PIL import Image

from utils import db

COMMENT_TEMPLATE_MD = """{} - {}
> {}"""


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


st.set_page_config(layout="wide", page_icon="", page_title="Top 10 Activities/Places in NJ")
st.title("Best Places and Activites in New Jersey")
st.markdown("""
 - New Jersey is filled with amazing places, but here are the top 10 activities and places within the Garden State! 
 - Feel free to discuss (or debate) in the comment below and explore!
 - Created as a part of the Coding NJ TSA 2022 Challenge
 - Made by @sriramelango: https://github.com/sriramelango 
 """)
conn = db.connect()
comments = db.collect(conn)




st.subheader("Six Flags Great Adventure/Hurricane Harbor")
image = Image.open('images/sixflags.jpeg')
st.image(image, caption = "Six Flags Great Adventure Rollercoaster")
st.info("""Six Flags Great Adventure and Hurricane Harbor is a park in Jackson, New Jersey! It includes a Wild Safari to top it off! It is filled with rollercoasters, restaurants, and is all around a great family experience!
More information can be found here: https://www.sixflags.com/greatadventure
""")















with st.expander("💬 Open comments"):

    # Show comments

    st.write("**Comments:**")

    for index, entry in enumerate(comments.itertuples()):
        st.markdown(COMMENT_TEMPLATE_MD.format(entry.name, entry.date, entry.comment))

        is_last = index == len(comments) - 1
        is_new = "just_posted" in st.session_state and is_last
        if is_new:
            st.success("☝️ Your comment was successfully posted.")

    space(2)

    # Insert comment

    st.write("**Add your own comment:**")
    form = st.form("comment")
    name = form.text_input("Name")
    comment = form.text_area("Comment")
    submit = form.form_submit_button("Add comment")

    if submit:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        db.insert(conn, [[name, comment, date]])
        if "just_posted" not in st.session_state:
            st.session_state["just_posted"] = True
        st.experimental_rerun()
