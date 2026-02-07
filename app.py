# import streamlit as st
# import qrcode
# import io
# import json
# import os
# import base64

# # ================================
# # PAGE CONFIG
# # ================================
# st.set_page_config(
#     page_title="Wedding QR Menu",
#     page_icon="🍽️",
#     layout="centered"
# )

# # ================================
# # LOAD CSS
# # ================================
# def load_css():
#     try:
#         with open("assets/css/style.css") as f:
#             st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#     except FileNotFoundError:
#         pass

# load_css()

# # ================================
# # DATA FILE
# # ================================
# DATA_FILE = "data/menu.json"

# def save_data(data):
#     os.makedirs("data", exist_ok=True)
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4)

# def load_data():
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     return {
#         "base_url": "",
#         "bride_name": "",
#         "groom_name": "",
#         "caterer_name": "",
#         "address": "",
#         "phone": "",
#         "quote": "",
#         "image_base64": "",
#         "menu": {}
#     }

# data = load_data()

# # ================================
# # SESSION STATE
# # ================================
# if "menu" not in st.session_state:
#     st.session_state.menu = data.get("menu", {})

# # ================================
# # VIEW MODE
# # ================================
# view_mode = st.query_params.get("view", "admin")

# # ================================
# # COMMON DATA
# # ================================
# base_url = data.get("base_url", "")
# bride_name = data.get("bride_name", "")
# groom_name = data.get("groom_name", "")
# caterer_name = data.get("caterer_name", "")
# address = data.get("address", "")
# phone = data.get("phone", "")
# quote = data.get("quote", "")
# image_base64 = data.get("image_base64", "")

# # ================================
# # ADMIN PANEL
# # ================================
# if view_mode == "admin":
#     st.sidebar.title("🛠 Admin Panel")

#     st.sidebar.subheader("🌐 App Configuration")
#     base_url = st.sidebar.text_input("App Base URL", value=base_url)

#     st.sidebar.subheader("📸 Bride & Groom Image")
#     uploaded_image = st.sidebar.file_uploader(
#         "Upload Image (jpg / png)",
#         type=["jpg", "jpeg", "png"]
#     )
#     if uploaded_image:
#         image_base64 = base64.b64encode(uploaded_image.getvalue()).decode("utf-8")
#         st.sidebar.success("Image uploaded")

#     st.sidebar.subheader("💍 Couple Details")
#     bride_name = st.sidebar.text_input("Bride Name", value=bride_name)
#     groom_name = st.sidebar.text_input("Groom Name", value=groom_name)

#     st.sidebar.subheader("🍽 Caterer Details")
#     caterer_name = st.sidebar.text_input("Caterer Name", value=caterer_name)
#     address = st.sidebar.text_input("Address", value=address)
#     phone = st.sidebar.text_input("Phone", value=phone)
#     quote = st.sidebar.text_area("Wedding Quote", value=quote)

#     st.sidebar.subheader("📋 Menu Management")
#     category = st.sidebar.text_input("Menu Category")
#     item = st.sidebar.text_input("Menu Item")

#     if st.sidebar.button("➕ Add Item"):
#         if category and item:
#             st.session_state.menu.setdefault(category, []).append(item)
#             st.sidebar.success("Item added")
#         else:
#             st.sidebar.error("Both fields required")

#     if st.sidebar.button("💾 Save All Changes"):
#         save_data({
#             "base_url": base_url,
#             "bride_name": bride_name,
#             "groom_name": groom_name,
#             "caterer_name": caterer_name,
#             "address": address,
#             "phone": phone,
#             "quote": quote,
#             "image_base64": image_base64,
#             "menu": st.session_state.menu
#         })
#         st.sidebar.success("Saved successfully")
#         st.rerun()

#     st.sidebar.subheader("🔳 QR Code")
#     if base_url:
#         qr_url = base_url.rstrip("/") + "/?view=guest"
#         qr = qrcode.make(qr_url)
#         buf = io.BytesIO()
#         qr.save(buf, format="PNG")
#         st.sidebar.image(buf.getvalue())
#         st.sidebar.download_button("⬇ Download QR", buf.getvalue(), "wedding_menu_qr.png", "image/png")



# # ================================
# # GUEST / PREVIEW VIEW
# # ================================

# # Hero Image
# if image_base64:
#     st.markdown("<div class='hero-img'>", unsafe_allow_html=True)
#     st.image(base64.b64decode(image_base64), width="stretch")
#     st.markdown("</div>", unsafe_allow_html=True)

# # Quote
# if quote:
#     st.markdown(f"<div class='quote'>{quote}</div>", unsafe_allow_html=True)

# # Title Box
# st.markdown(f"""
# <div class="menu-title-box">
#     <span>WEDDING MENU</span>
#     <div class="menu-couple">{bride_name} &amp; {groom_name}</div>
# </div>
# """, unsafe_allow_html=True)

# # --- FIXED SECTION START ---
# # We removed the <div class='menu-poster'> wrapper to get rid of the extra box
# for cat, items in st.session_state.menu.items():
#     st.markdown(f"<div class='poster-category'>{cat.upper()}</div>", unsafe_allow_html=True)
#     st.markdown("<div class='poster-divider'></div>", unsafe_allow_html=True)
#     for food in items:
#         st.markdown(f"<div class='poster-item'>{food}</div>", unsafe_allow_html=True)
# # --- FIXED SECTION END ---

# # Caterer Card
# if caterer_name:
#     st.markdown(f"""
#     <div class="caterer-card">
#         <h3>🍽 Caterer Details</h3>
#         <p><b>Name:</b> {caterer_name}</p>
#         <p><b>Address:</b> {address}</p>
#         <p><b>Phone:</b> {phone}</p>
#     </div>
#     """, unsafe_allow_html=True)



import streamlit as st
import qrcode
import io
import json
import os
import base64
from PIL import Image   # ✅ needed for image optimization

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Wedding QR Menu",
    page_icon="🍽️",
    layout="centered"
)

# ================================
# LOAD CSS
# ================================
def load_css():
    try:
        with open("assets/css/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# ================================
# DATA FILE
# ================================
DATA_FILE = "data/menu.json"

def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "base_url": "",
        "bride_name": "",
        "groom_name": "",
        "caterer_name": "",
        "address": "",
        "phone": "",
        "quote": "",
        "image_base64": "",
        "menu": {}
    }

data = load_data()

# ================================
# SESSION STATE
# ================================
if "menu" not in st.session_state:
    st.session_state.menu = data.get("menu", {})

# ================================
# VIEW MODE
# ================================
view_mode = st.query_params.get("view", "admin")

# ================================
# COMMON DATA
# ================================
base_url = data.get("base_url", "")
bride_name = data.get("bride_name", "")
groom_name = data.get("groom_name", "")
caterer_name = data.get("caterer_name", "")
address = data.get("address", "")
phone = data.get("phone", "")
quote = data.get("quote", "")
image_base64 = data.get("image_base64", "")

# ================================
# ADMIN PANEL
# ================================
if view_mode == "admin":
    st.sidebar.title("🛠 Admin Panel")

    st.sidebar.subheader("🌐 App Configuration")
    base_url = st.sidebar.text_input("App Base URL", value=base_url)

    # -------- IMAGE UPLOAD (OPTIMIZED) --------
    st.sidebar.subheader("📸 Bride & Groom Image")
    uploaded_image = st.sidebar.file_uploader(
        "Upload Image (jpg / png)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:
        img = Image.open(uploaded_image).convert("RGB")
        img.thumbnail((900, 900))               # ✅ critical for mobile
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=80)
        image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        st.sidebar.success("Image uploaded (optimized)")

    # -------- DETAILS --------
    st.sidebar.subheader("💍 Couple Details")
    bride_name = st.sidebar.text_input("Bride Name", value=bride_name)
    groom_name = st.sidebar.text_input("Groom Name", value=groom_name)

    st.sidebar.subheader("🍽 Caterer Details")
    caterer_name = st.sidebar.text_input("Caterer Name", value=caterer_name)
    address = st.sidebar.text_input("Address", value=address)
    phone = st.sidebar.text_input("Phone", value=phone)
    quote = st.sidebar.text_area("Wedding Quote", value=quote)

    # -------- MENU --------
    st.sidebar.subheader("📋 Menu Management")
    category = st.sidebar.text_input("Menu Category")
    item = st.sidebar.text_input("Menu Item")

    if st.sidebar.button("➕ Add Item"):
        if category and item:
            st.session_state.menu.setdefault(category, []).append(item)
            st.sidebar.success("Item added")
        else:
            st.sidebar.error("Both fields required")

    if st.sidebar.button("💾 Save All Changes"):
        save_data({
            "base_url": base_url,
            "bride_name": bride_name,
            "groom_name": groom_name,
            "caterer_name": caterer_name,
            "address": address,
            "phone": phone,
            "quote": quote,
            "image_base64": image_base64,
            "menu": st.session_state.menu
        })
        st.sidebar.success("Saved successfully")
        st.rerun()

    # -------- QR --------
    st.sidebar.subheader("🔳 QR Code")
    if base_url:
        qr_url = base_url.rstrip("/") + "/?view=guest"
        qr = qrcode.make(qr_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        st.sidebar.image(buf.getvalue())
        st.sidebar.download_button(
            "⬇ Download QR",
            buf.getvalue(),
            "wedding_menu_qr.png",
            "image/png"
        )

# ================================
# GUEST / PREVIEW VIEW
# ================================

# -------- IMAGE (NO HTML WRAPPER → MOBILE SAFE) --------
if image_base64:
    st.image(base64.b64decode(image_base64), width="stretch")

# -------- QUOTE --------
if quote:
    st.markdown(f"<div class='quote'>{quote}</div>", unsafe_allow_html=True)

# -------- TITLE BOX (GUARDED) --------
if bride_name or groom_name:
    st.markdown(f"""
    <div class="menu-title-box">
        <span class="menu-title-text">WEDDING MENU</span>
        <div class="menu-couple">{bride_name} &amp; {groom_name}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="menu-title-box">
        <span class="menu-title-text">WEDDING MENU</span>
    </div>
    """, unsafe_allow_html=True)

# -------- MENU (NO EXTRA WRAPPERS) --------
for cat, items in st.session_state.menu.items():
    st.markdown(f"<div class='poster-category'>{cat.upper()}</div>", unsafe_allow_html=True)
    st.markdown("<div class='poster-divider'></div>", unsafe_allow_html=True)
    for food in items:
        st.markdown(f"<div class='poster-item'>{food}</div>", unsafe_allow_html=True)

# # -------- CATERER DETAILS (CARD STYLE, SAFE) --------
# if caterer_name:
#     with st.container(border=True):
#         st.markdown("### 🍽 Caterer Details")
#         st.write(f"**Name:** {caterer_name}")

#         if address:
#             st.write(f"**Address:** {address}")

#         if phone:
#             st.write(f"**Phone:** {phone}")

# -------- CATERER DETAILS (MOBILE-SAFE) --------
if caterer_name:
    st.markdown("### 🍽 Caterer Details")
    st.write(f"**Name:** {caterer_name}")

    if address:
        st.write(f"**Address:** {address}")

    if phone:
        st.write(f"**Phone:** {phone}")


