import streamlit as st
import sqlite3
import openai

# Get OpenAI API key from environment variable
openai.api_key = "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"


# Function to fetch files associated with the user
def fetch_files(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT filename FROM files WHERE user_id=?", (user_id,))
    files = c.fetchall()
    conn.close()
    return [file[0] for file in files]


# Function to fetch file content
def fetch_file_content(user_id, filename):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT file_content FROM files WHERE user_id=? AND filename=?", (user_id, filename))
    file_content = c.fetchone()
    conn.close()
    return file_content[0] if file_content else None


# Main function to run Streamlit app
def main():
    st.title("OpenAI Response Demo")

    # Input user ID
    user_id = st.text_input("Enter your user ID:")

    # Fetch files associated with the user
    files = fetch_files(user_id)

    # Select a file
    selected_file = st.selectbox("Select a file:", files)

    # Button to request response from OpenAI
    if st.button("Get Response"):
        if selected_file:
            # Fetch file content
            file_content = fetch_file_content(user_id, selected_file)
            if file_content:
                try:
                    # Call OpenAI API with file content
                    response = openai.Completion.create(
                        engine="gpt-3.5-turbo-instruct",
                        prompt=file_content,
                        temperature=0.7,
                        max_tokens=50,
                        n=1,
                        stop=None
                    )
                    # Display response
                    st.write("Response:", response.choices[0].text.strip())
                except Exception as e:
                    st.error("Error occurred while fetching response from OpenAI API: {}".format(e))
            else:
                st.write("Error: File content not found.")
        else:
            st.write("No file selected.")


if __name__ == "__main__":
    main()
