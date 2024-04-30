import tensorflow as tf
import streamlit as st

from utilities import detect_from_image, detect_from_webcam


st.title("Plant Detection")


add_select_box = st.empty()
with st.sidebar:
    st.sidebar.title('Medicinal Plant Detection')
    add_select_box = st.sidebar.selectbox(
        "Choose mode: ",
        (None, "Image Upload", "Webcam")
    )

if add_select_box == "Image Upload":
    uploaded_image = st.file_uploader("Chooose an image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        st.subheader("Uploaded Image")
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        with st.spinner("Processing..."):
            detect_from_image(uploaded_image)

        st.subheader("Output Image")
        st.image("output.png", caption="Outputimage", use_column_width=True)

elif add_select_box == "Webcam":
    st.write("In progress")

else:
    st.write("Choose a mode in the sidebar.")