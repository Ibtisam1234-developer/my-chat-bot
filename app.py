import google.generativeai as generativeai
import streamlit as st
import base64
import speech_recognition as sr

# Configure the API key
generativeai.configure(api_key='AIzaSyB-ozmy3iQAWbD-htE3ojrVb9avVrDWGLw')

# Function to set background image
def set_background(image_file):
    with open(image_file, "rb") as file:
        base64_str = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stApp"] {{
            background-image: url("data:image/jpg;base64,{base64_str}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background("image.png")

# Initialize model
model = generativeai.GenerativeModel('gemini-1.5-flash')

# Function to capture voice input
def take_command() -> str:
    """Listen for audio input and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

        try:
            st.info("🧠 Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            return query
        except sr.UnknownValueError:
            return "Could not understand, please try again."
        except sr.RequestError:
            return "Speech recognition service error."
        except Exception:
            return "An error occurred during speech recognition."

def main():
    st.title('Chat with Ibtisam AI')

    # Initialize chat history
    messages = st.session_state.setdefault("messages", [])

    # Display previous messages
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input handling
    prompt = None

    # Voice input button
    if st.button("🎤 Speak"):
        prompt = take_command()
        st.success(f"Recognized: {prompt}")  # Display recognized text

    # Text input box
    if not prompt:
        prompt = st.chat_input("What would you like to ask?")

    # Process input if available
    if prompt:
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = model.generate_content(prompt).text
            messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
