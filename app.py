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


# Page Setup
st.set_page_config(layout="centered", page_icon="", page_title="T10 of New Jersey!")
st.title("Best Places & Activites in NJ")
st.markdown("""
 - New Jersey is filled with amazing places, but here are the top 10 activities and places within the Garden State! 
 - Feel free to discuss (or debate) in the comment below and explore!
 - Created as a part of the Coding NJ TSA 2022 Challenge
 - Made by @sriramelango: https://github.com/sriramelango 
 """)
conn = db.connect()
comments = db.collect(conn)



# Places and Activites
st.subheader("Six Flags Great Adventure/Hurricane Harbor")
image = Image.open('images/sixflags.jpeg')
st.image(image, caption = "Six Flags Great Adventure Rollercoaster")
st.info("""Six Flags Great Adventure and Hurricane Harbor is a park in Jackson, New Jersey! It includes a Wild Safari to top it off! It is filled with rollercoasters, restaurants, and is all around a great family experience!

More information can be found here: https://www.sixflags.com/greatadventure
""")


st.subheader("Atlantic City & Boardwalk")
image = Image.open('images/atlanticcity.jpeg')
st.image(image, caption = "Night at Atlantic City and the Boardwalk")
st.info("""Atlantic City is a New Jersey City situated on the Atlantic Coast with beautiful sandy beaches. Many casinos and other night activities are prevalent here, and one of the best boardwalks in the world also lies in this city.

More information can be found here: https://www.atlanticcitynj.com/
""")


st.subheader("Ellis Island")
image = Image.open('images/ellis.jpeg')
st.image(image, caption = "Historic Image of Ellis Island")
st.info("""Ellis Island is ingrained within the greater context of American history, and is the beginning place of millions of American stories. It was once one of the busiest and largest immigration processing centers in the entire world and continues to remain influential today. 

More information can be found here: https://en.wikipedia.org/wiki/Ellis_Island
""")


st.subheader("Adventure Aquarium")
image = Image.open('images/aquarium.webp')
st.image(image, caption = "School Children and Hippos")
st.info("""The Adventure Aquarium, situated on the Camden riverfront, and with a view looking into the skyscrapers of Philidelphia, is an amazing joy to visit. Filled with sharks and marine creatures of all sorts, you are guaranteed to be in awe. With exhibits all around and a learning experience for everyone, the Adventure Aquarium is truly awesome.

More information can be found here: https://www.adventureaquarium.com/
""")


st.subheader("Liberty Science Center")
image = Image.open('images/science.jpeg')
st.image(image, caption = "Liberty Science Center + Planetarium")
st.info("""The Liberty Science Center is truly a sight to behold! At one point, it was the largest planetarium in the entire Western hemisphere! There are a variety of activities here, as well as fun events for the entire family! 

More information can be found here: https://en.wikipedia.org/wiki/Liberty_Science_Center
""")

st.subheader("Newark Museum of Art")
image = Image.open('images/newark.jpeg')
st.image(image, caption = "Newark Museum of Art - Streetview")
st.info("""The Newark Museum of Art holds one of the largest collections of art in the entire nation! It has pieces stretching nearly all continents, with some pieces from the ancient world! Their Tibetan exhibits are known to be one of the best in the world!

More information can be found here: https://en.wikipedia.org/wiki/The_Newark_Museum_of_Art
""")

st.subheader("Garden State Discovery Museum")
image = Image.open('images/discovery.jpeg')
st.image(image, caption = "Garden State Discovery Museum Exhibit")
st.info("""The Garden State Discovery Museum can be found in Cherry Hill, where there are a ton of fun exhibits that children can learn from and play on. It is known for its hands-on activities and exhibits!

More information can be found here: https://www.discoverymuseum.com/
""")

st.subheader("Princeton University")
image = Image.open('images/princeton.jpeg')
st.image(image, caption = "Princeton University")
st.info("""Princeton is one of the most prestigious universities in the entire world, once home to scientists such as Albert Einstein, and alumni include Jeff Bezos and Michelle Obama!

More information can be found here: https://www.princeton.edu/
""")

st.subheader("Battleship New Jersey Museum & Memorial")
image = Image.open('images/ship.jpeg')
st.image(image, caption = "Battleship New Jersey")
st.info("""Battleship New Jersey is the longest battleship ever built, and is a tourist spot for military enthusiasts and historians! It was used in several wars, such as in WW2 and the Vietnam War!

More information can be found here: https://www.battleshipnewjersey.org/
""")

st.subheader("Liberty State Park")
image = Image.open('images/park.jpeg')
st.image(image, caption = "Liberty State Park")
st.info("""The Liberty State Park is home to breathtaking views and walkways, as well as several influential memorials commemorating the lives lost in the Holocaust and 9/11.

More information can be found here: https://nj.gov/dep/parksandforests/parks/libertystatepark.html
""")
space(2)


# Comment Section
with st.expander("💬 Open comments"):

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