import streamlit as st
import qrcode
import io
import json
import os
import base64

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
        "caterer_name": "",
        "address": "",
        "phone": "",
        "quote": "",
        "image_base64": "",
        "menu": {}
    }

stored_data = load_data()

# ================================
# SESSION STATE
# ================================
if "menu" not in st.session_state:
    st.session_state.menu = stored_data.get("menu", {})

# ================================
# VIEW MODE
# ================================
view_mode = st.query_params.get("view", "admin")

# ================================
# COMMON DATA
# ================================
base_url = stored_data.get("base_url", "")
caterer_name = stored_data.get("caterer_name", "")
address = stored_data.get("address", "")
phone = stored_data.get("phone", "")
quote = stored_data.get("quote", "")
image_base64 = stored_data.get("image_base64", "")

# ================================
# ADMIN PANEL
# ================================
if view_mode == "admin":
    st.sidebar.title("🛠 Admin Panel")

    # Base URL
    st.sidebar.subheader("🌐 App Configuration")
    base_url = st.sidebar.text_input(
        "App Base URL (example: http://172.20.10.4:8501)",
        value=base_url
    )

    # Image Upload
    st.sidebar.subheader("📸 Bride & Groom Image")
    uploaded_image = st.sidebar.file_uploader(
        "Upload Image (jpg / png)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:
        image_base64 = base64.b64encode(uploaded_image.getvalue()).decode("utf-8")
        st.sidebar.success("Image uploaded")

    # 4. SAVE ALL CHANGES BUTTON
    if st.sidebar.button("💾 Save All Changes"):
        save_data({
            "base_url": base_url,
            "caterer_name": caterer_name,
            "address": address,
            "phone": phone,
            "quote": quote,
            "image_base64": image_base64, # Saved directly in JSON
            "menu": st.session_state.menu
        })
        st.sidebar.success("All data saved successfully!")
        st.rerun()

    # Caterer Details
    st.sidebar.subheader("🍽 Caterer Details")
    caterer_name = st.sidebar.text_input("Name", value=caterer_name)
    address = st.sidebar.text_input("Address", value=address)
    phone = st.sidebar.text_input("Phone", value=phone)
    quote = st.sidebar.text_area("Wedding Quote", value=quote)

    # Menu Management
    st.sidebar.subheader("📋 Menu Management")
    category = st.sidebar.text_input("Menu Category")
    item = st.sidebar.text_input("Menu Item")

    if st.sidebar.button("➕ Add Item & Save"):
        if category and item:
            st.session_state.menu.setdefault(category, []).append(item)

            save_data({
                "base_url": base_url,
                "caterer_name": caterer_name,
                "address": address,
                "phone": phone,
                "quote": quote,
                "image_base64": image_base64,
                "menu": st.session_state.menu
            })

            st.sidebar.success("Saved successfully")
            st.rerun()
        else:
            st.sidebar.error("Category and item required")

    # QR Code
    st.sidebar.subheader("🔳 QR Code")
    if base_url:
        guest_url = base_url.rstrip("/") + "/?view=guest"
        qr = qrcode.make(guest_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")

        st.sidebar.image(buf.getvalue())
        st.sidebar.download_button(
            "⬇ Download QR",
            buf.getvalue(),
            "wedding_menu_qr.png",
            "image/png"
        )
    else:
        st.sidebar.warning("Enter Base URL to generate QR")

    # ================================
    # ADMIN PREVIEW - Show menu preview in admin mode
    # ================================
    st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#4f82a0;'>📱 Menu Preview</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

    # Image (fixed syntax)
    if image_base64:
        image_bytes = base64.b64decode(image_base64)
        st.markdown("<div class='hero-img'>", unsafe_allow_html=True)
        st.image(image_bytes, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    # Quote
    if quote:
        st.markdown(
            f"<div class='quote'>{quote}</div>",
            unsafe_allow_html=True
        )

    # ================================
    # GUEST MENU POSTER VIEW
    # ================================
    st.markdown("<div class='menu-poster'>", unsafe_allow_html=True)

    st.markdown("<div class='poster-title'>WEDDING MENU</div>", unsafe_allow_html=True)

    if st.session_state.menu:
        for cat, items in st.session_state.menu.items():
            st.markdown(f"<div class='poster-category'>{cat.upper()}</div>", unsafe_allow_html=True)
            st.markdown("<div class='poster-divider'></div>", unsafe_allow_html=True)

            for food in items:
                st.markdown(f"<div class='poster-item'>{food}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Caterer Card
    if caterer_name:
        st.markdown(f"""
        <div class="caterer-card">
            <h3>🍽 Caterer Details</h3>
            <p><b>Name:</b> {caterer_name}</p>
            <p><b>Address:</b> {address}</p>
            <p><b>Phone:</b> {phone}</p>
        </div>
        """, unsafe_allow_html=True)

# ================================
# GUEST VIEW - Only display when ?view=guest
# ================================
elif view_mode == "guest":
    # Image (fixed syntax)
    if image_base64:
        image_bytes = base64.b64decode(image_base64)
        st.markdown("<div class='hero-img'>", unsafe_allow_html=True)
        st.image(image_bytes, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    # Quote
    if quote:
        st.markdown(
            f"<div class='quote'>{quote}</div>",
            unsafe_allow_html=True
        )

    # ================================
    # GUEST MENU POSTER VIEW
    # ================================
    st.markdown("<div class='menu-poster'>", unsafe_allow_html=True)

    st.markdown("<div class='poster-title'>WEDDING MENU</div>", unsafe_allow_html=True)

    if st.session_state.menu:
        for cat, items in st.session_state.menu.items():
            st.markdown(f"<div class='poster-category'>{cat.upper()}</div>", unsafe_allow_html=True)
            st.markdown("<div class='poster-divider'></div>", unsafe_allow_html=True)

            for food in items:
                st.markdown(f"<div class='poster-item'>{food}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Caterer Card
    if caterer_name:
        st.markdown(f"""
        <div class="caterer-card">
            <h3>🍽 Caterer Details</h3>
            <p><b>Name:</b> {caterer_name}</p>
            <p><b>Address:</b> {address}</p>
            <p><b>Phone:</b> {phone}</p>
        </div>
        """, unsafe_allow_html=True)




