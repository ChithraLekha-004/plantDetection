import tensorflow as tf
import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
from utilities import detect_from_image

st.set_page_config(layout="wide")
with open("resources/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def display_plant_info(detected_plants):
    if detected_plants == "Aloe vera":
        st.markdown("<p class='plant-info'>Aloe vera is a succulent plant species of the genus Aloe. It is widely distributed, and is considered an invasive species in many world regions. An evergreen perennial, it originates from the Arabian Peninsula, but also grows wild in tropical, semi-tropical, and arid climates around the world.</p>", unsafe_allow_html=True)
        st.markdown("<h4 class='detected-plant-use'>Medicinal uses: </h4>", unsafe_allow_html=True)
        st.markdown("""
            * <b class='medicinal-use-point'>Skin Care: </b>Aloe vera gel is perhaps most famous for its topical application in treating various skin conditions. It is used to soothe sunburns, minor burns, and cuts due to its cooling and anti-inflammatory properties. Aloe vera promotes wound healing by stimulating cell regeneration and reducing inflammation and pain.
            * <b class='medicinal-use-point'>Moisturizer: </b>Aloe vera gel is an excellent natural moisturizer for the skin. It hydrates the skin without leaving it greasy, making it suitable for all skin types, including oily and acne-prone skin.
            * <b class='medicinal-use-point'>Wound Healing: </b>Aloe vera accelerates the healing process of wounds, including minor cuts, scrapes, and abrasions. It forms a protective barrier over the wound, keeping it moist and preventing infection.
            * <b class='medicinal-use-point'>Burn Relief: </b>Aloe vera gel is commonly used to soothe sunburns and other types of burns. Its cooling effect provides immediate relief from pain and helps to reduce redness and inflammation.
            * <b class='medicinal-use-point'>Acne Treatment: </b>Aloe vera gel has antibacterial and anti-inflammatory properties that make it effective in treating acne. It helps reduce acne inflammation, soothe irritated skin, and prevent further breakouts.
        """, unsafe_allow_html=True
        )
    elif detected_plants == "Tulasi":
        st.markdown("<p class='plant-info'>Ocimum tenuiflorum, commonly known as holy basil or tulsi, is an aromatic perennial plant in the family Lamiaceae.It is native to tropical and subtropical regions of Australia, Malesia, Asia, and the western Pacific.It is widely cultivated throughout the Southeast Asian tropics. This plant has escaped from cultivation and has naturalized in many tropical regions of the Americas. It is an agricultural and environmental weed.</p>", unsafe_allow_html=True)
        st.markdown("<h4 class='detected-plant-use'>Medicinal uses: </h4>", unsafe_allow_html=True)
        st.markdown("""
            * <b class='medicinal-use-point'>Immune System Support: </b>Tulsi is rich in antioxidants and other bioactive compounds that help boost the immune system, making the body more resilient to infections and diseases.
            * <b class='medicinal-use-point'>Respiratory Health: </b>Tulsi is known for its anti-inflammatory and antimicrobial properties, which can help relieve symptoms of respiratory conditions such as asthma, bronchitis, and coughs. It is often used in herbal remedies for respiratory health.
            * <b class='medicinal-use-point'>Stress Relief: </b>Tulsi is considered an adaptogen, meaning it helps the body adapt to stress and promotes mental clarity and relaxation. Consuming tulsi tea or extract may help reduce stress and anxiety levels.
            * <b class='medicinal-use-point'>Digestive Health: </b>Tulsi has carminative properties, which means it can help alleviate digestive issues like bloating, gas, and indigestion. It also promotes healthy gut bacteria and may aid in the treatment of stomach ulcers.
            * <b class='medicinal-use-point'>Cardiovascular Health: </b>Tulsi may help lower cholesterol levels and regulate blood pressure, thus reducing the risk of heart disease and stroke. It also improves blood circulation and supports overall cardiovascular health.
        """, unsafe_allow_html=True
        )
    elif detected_plants == "Pepper":
        st.markdown("<p class='plant-info'>Pepper is a flowering vine in the family Piperaceae, cultivated for its fruit, which is usually dried and used as a spice and seasoning. The fruit is a drupe which is about 5 mm in diameter, dark red, and contains a stone which encloses a single pepper seed.</p>", unsafe_allow_html=True)
        st.markdown("<h4 class='detected-plant-use'>Medicinal uses: </h4>", unsafe_allow_html=True)
        st.markdown("""
            * <b class='medicinal-use-point'>Digestive Aid: </b>Pepper contain piperine, a compound that has been shown to stimulate the production of digestive enzymes, aiding in the digestion process. It can help alleviate digestive discomfort, bloating, and gas.
            * <b class='medicinal-use-point'>Antioxidant: </b>Pepper contains antioxidants that help neutralize harmful free radicals in the body, reducing oxidative stress and lowering the risk of chronic diseases such as cancer, cardiovascular disease, and neurodegenerative disorders.
            * <b class='medicinal-use-point'>Weight Management: </b>Piperine in black pepper has been studied for its potential to aid in weight management. It may help inhibit the formation of new fat cells and increase metabolism, promoting weight loss when combined with a healthy diet and exercise.
            * <b class='medicinal-use-point'>Pain Relief: </b>Topical application of pepper extracts or essential oil may provide relief from muscle pain, joint pain, and headaches due to its warming and analgesic properties.
            * <b class='medicinal-use-point'>Oral Health: </b>The antibacterial properties of pepper may also benefit oral health by helping to prevent the growth of bacteria in the mouth, reducing the risk of cavities and gum disease.
        """, unsafe_allow_html=True
        )


def main_content():
    uploaded_image = st.file_uploader("Chooose an image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        st.subheader("Uploaded Image")
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        detected_plants = None
        with st.spinner("Processing..."):
            detected_plants = detect_from_image(uploaded_image)

        if len(detected_plants) != 0:
            st.subheader("Output Image")
            st.image("output.png", caption="Outputimage", use_column_width=True)

            for detected_plant in detected_plants:
                st.markdown(f"<p class='detected-plant'>{detected_plant}</p>", unsafe_allow_html=True)
                display_plant_info(detected_plant)
                st.divider()

# page_bg_img ="""
#     <style>
#         [data-testid="stAppViewContainer"]{
#             background-image: url("https://images.unsplash.com/photo-1476842634003-7dcca8f832de?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
#             background-size: cover;
#         }
#     </style>
# """
# st.markdown(page_bg_img,unsafe_allow_html=True)
st.title("Nature Scan: Medicinal Herbs Identification System")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authentication_choice = None

if 'authentication_status' not in st.session_state:
    st.session_state.authentication_status = None

if st.session_state["authentication_status"] is True:
    with st.sidebar:
        st.write(f'Logged in as: <span class="login-info"><i><b>{st.session_state["name"]}</b></i></span>', unsafe_allow_html=True)
        authenticator.logout(location='sidebar', key='logout_button')
    main_content()
else:
    auth_selectbox_placeholder = st.sidebar.empty()
    authentication_choice = auth_selectbox_placeholder.selectbox(
        'Choose: ',
        ('Login', 'Register')
    )

    if authentication_choice == 'Register':
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)
    elif authentication_choice == 'Login':
        authenticator.login('main')
        if st.session_state["authentication_status"] is True:
            with st.sidebar:
                st.write(f'Logged in as: <span class="login-info"><i><b>{st.session_state["name"]}</b></i></span>', unsafe_allow_html=True)
                authenticator.logout(location='sidebar', key='logout_button')
            main_content()
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')
    else:
        st.warning("Please choose Register or Login")

    if st.session_state["authentication_status"] is not None:
            auth_selectbox_placeholder.empty()