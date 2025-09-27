import streamlit as st
from PIL import Image
from utils.compare import compare_with_ocr

st.title("📊 Dashboard Screenshot Comparator")
st.write("Upload two screenshots of the same dashboard, and I’ll highlight where the numbers/text have changed.")

# File uploaders
uploaded_file1 = st.file_uploader("Upload *before* screenshot", type=["png", "jpg", "jpeg"])
uploaded_file2 = st.file_uploader("Upload *after* screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file1 and uploaded_file2:
    img1 = Image.open(uploaded_file1).convert("RGB")
    img2 = Image.open(uploaded_file2).convert("RGB")

    st.subheader("Uploaded Images")
    col1, col2 = st.columns(2)
    with col1:
        st.image(img1, caption="Before", use_container_width=True)
    with col2:
        st.image(img2, caption="After", use_container_width=True)

    if st.button("🔍 Compare Screenshots"):
        result_img = compare_with_ocr(img1, img2)
        st.subheader("Differences Highlighted")
        st.image(result_img, caption="Changed areas highlighted", use_container_width=True)

        # Option to download the result
        output_path = "output/ocr_highlighted.png"
        Image.fromarray(result_img).save(output_path)
        with open(output_path, "rb") as f:
            st.download_button("⬇️ Download result", f, file_name="ocr_highlighted.png")
