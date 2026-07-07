import streamlit as st
import requests

st.set_page_config(page_title="Smart Document Q&A", page_icon="📄")

st.title("📄 Smart Document Q&A")

API_URL = "http://127.0.0.1:8000"

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

        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )

        if response.status_code == 200:
            st.success(f"'{uploaded_file.name}' uploaded successfully!")
        else:
            st.error("Upload failed")
            
st.divider()

st.subheader("Ask a Question")

query = st.text_input("Enter your question")

if st.button("Get Answer"):

    if query.strip() == "":
        st.warning("Please enter a question.")

    else:
        response = requests.post(
            f"{API_URL}/query",
            json={"query": query}
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Answer")

            st.write(result["answer"])

            # Show page numbers if your API returns them
            if "pages" in result:
                st.info(f"Pages: {result['pages']}")

            # Show sources if your API returns them
            elif "sources" in result:
                st.subheader("Sources")

                for source in result["sources"]:
                    st.write(f"**Page:** {source['page']}")
                    if "distance" in source:
                        st.write(f"Distance: {source['distance']}")
                    if "text" in source:
                        st.write(source["text"])
                    st.divider()

        else:
            st.error("Failed to get answer.")