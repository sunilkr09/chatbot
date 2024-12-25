import streamlit as st
from openai import OpenAI

# Title and Description
st.title("🍛 Indian Cuisine Chatbot")
st.write(
    "Welcome to the Indian Cuisine Chatbot! This chatbot helps you explore an Indian menu, take orders, and answer questions. "
    "Provide your OpenAI API key below to start interacting."
)

# Ask user for OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create OpenAI client
    try:
        client = OpenAI(api_key=openai_api_key)
        st.success("API key successfully loaded.")
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {e}")
    
    # Initialize session state for chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """
You are an experienced Indian cuisine specialist. Suggest menu items, educate customers, and provide an automated service to collect orders for an Indian restaurant. 
Here is the menu:
Butter Chicken: $14.99, Paneer Tikka: $11.99, Chole Bhature: $10.99, Biryani: $12.99, Masala Dosa: $9.99.
(Additional menu items are included in the chatbot logic.)
""",
            }
        ]

    # Function to handle chat interaction
    def get_completion_from_messages(messages, model="gpt-4", temperature=1):
        try:
            response = client.chat.completions.create(
                model=model, messages=messages, temperature=temperature
            )
            return response['choices'][0]['message']['content']  # Corrected access to message content
        except Exception as e:
            st.error(f"Error fetching response: {e}")
            return "Sorry, something went wrong."

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input field
    if prompt := st.chat_input("Ask me about Indian cuisine or place an order!"):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        response = get_completion_from_messages(
            st.session_state.messages, model="gpt-4", temperature=1
        )

        # Append and display AI response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
