import streamlit as st
import requests

st.set_page_config(page_title="Smart Document Q&A")

st.title("Smart Document Q&A")

API_URL = "http://127.0.0.1:8000"

# -----------------------------
# Session State
# -----------------------------
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Upload Section
# -----------------------------
input_method = st.radio(
    "Choose Input Method",
    [
        "Upload PDF",
        "Paste Text"
    ]
)

# -------- Upload PDF --------
if input_method == "Upload PDF":

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button("Upload Document"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            with st.spinner("Uploading and processing PDF..."):

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files
                )

            if response.status_code == 200:

                st.session_state.uploaded = True

                st.success(f"{uploaded_file.name} uploaded successfully!")

            else:
                try:
                    st.error(response.json()["error"])
                except:
                    st.error("Upload failed")

# -------- Paste Text --------
else:

    pasted_text = st.text_area(
        "Paste your text here",
        height=250
    )

    if st.button("Process Text"):

        if not pasted_text.strip():
            st.warning("Please enter some text.")
            st.stop()

        with st.spinner("Processing text..."):
            response = requests.post(
            f"{API_URL}/paste-text",
            json={"text": pasted_text}
            )

        if response.status_code == 200:

            st.session_state.uploaded = True

            st.success("Text processed successfully!")

        else:
            try:
                st.error(response.json()["error"])
            except:
                st.error("Processing failed")

st.divider()

# -----------------------------
# Chat Section
# -----------------------------
if st.session_state.uploaded:

    st.subheader("Chat with your Document")

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input("Ask a question about your document")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):

            response = requests.post(
                f"{API_URL}/query",
                json={
                    "query": prompt
                }
            )

        if response.status_code == 200:

            result = response.json()

            answer = result["answer"]

            with st.chat_message("assistant"):

                st.markdown(answer)

                if "pages" in result:
                    st.caption(f"Pages: {result['pages']}")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        else:

            st.error("Failed to get answer.")

else:

    st.info("Please upload a PDF or paste text first.")