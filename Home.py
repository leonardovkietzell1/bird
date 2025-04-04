import streamlit as st

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] ul {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

PAGES = {
    "Home": None,
    "The Birder AI": "pages/Birds.py",
    "Team": "pages/Team.py"
}

for page_name, file_path in PAGES.items():
    if file_path:
        st.sidebar.page_link(file_path, label=page_name)
    else:
        st.sidebar.write(f"### {page_name}")
col1,col2,col3=st.columns(3)
with col2:
    st.image("data/logo.png", width=200)

st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:35px; text-align:left; ">Welcome to <b>The Birder</b> -- Your Intelligent Online Ornithologist</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:15px; text-align:left; ">You are now able to access the most incredible information about birds</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; "><b>The Birder</b> is a cutting-edge, AI-driven bird companion that will make sure you get the best experience in the ornithology sector. The Birder will guide you through this incredible world letting you know the best curiosities of every bird, along with whre to find it and how to get there. This experience includes the best flight and hotel recommendations to make it the easiest possible for you to make your dream come true. You are one step away to achieve real happiness!</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; font-weight:bold;">But why The Birder?</p>', unsafe_allow_html=True)
st.markdown("""
- **Bird Information** – In this tab you will find the most interesting and precise information of any bird you want, just by uploading the image of the bird you want to know more about. You will also be able to ask any intricate question you might think of and The Birder will answer you as best as it knows.
- **Flights** – Once you know where this particular bird is usually located, your companion will recommend the three best flight options for you to get to live the experience with your own eyes.
- **Hotels** – The last thing you need to live the full experience is a good hotel to stay in and enjoy the best days of your life. The Birder will help you choose the best staying places you can think of to have a good rest after a long day of spotting your favourite birds.
- **Team** – In here you can have an inside look at our incredible and hard-working team that made all this possible.
""")
st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left;font-weight:bold;">What are you waiting for?</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; ">Start your experience here!</p>', unsafe_allow_html=True)
website_url = "https://machinelearning2-j2lvfnphayyg9eqsgeapp2p.streamlit.app/Birds"
if st.button("LET'S GO!"):
    st.markdown(f'<meta http-equiv="refresh" content="0; URL={website_url}">', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)

cola,colb,colc=st.columns(3)
with cola:
    st.image("data/bird5.jpg", width=205)
    st.image("data/bird4.jpg", width=205)
    st.image("data/bird7.jpg", width=205)
with colb:
    st.image("data/bird2.jpg", width=205)
    st.image("data/bird1.jpg", width=205)
    st.image("data/bird8.jpg", width=205)
with colc:
    st.image("data/bird3.jpg", width=205)
    st.image("data/bird6.jpg", width=205)
    st.image("data/bird9.jpg", width=205)