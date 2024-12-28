import os.path

import streamlit as st
from openai import OpenAI

import gspread
from google.oauth2.service_account import Credentials

# Google Sheets API scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DOCUMENT_ID = "1mEYGtIpS7uHGcQeJgp2tpaDAYlLakeBLFfRLFrr3YqE"

# Path to your service account JSON file
CREDENTIALS_FILE = os.path.abspath(".streamlit/token.json")
creds = None

if not os.path.exists(CREDENTIALS_FILE):
    st.error(f"Missing Google API Credential file!")

# Connect to Google Sheets
def connect_google_sheet(document_id):
    # Authenticate using service account
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    workbook = client.open_by_key(document_id)
    return workbook

document = connect_google_sheet(DOCUMENT_ID)
worksheet = document.worksheet("Menu")
records = worksheet.get_all_records()
promt_menu = '\n'.join(map(lambda r: " - " + r.get("Items") + ", " + str(r.get("Price")), records))

# Title and Description
st.title("🍛 Indian Cuisine Chatbot")
st.write(
    "Welcome to the Indian Cuisine Chatbot! This chatbot helps you explore an Indian menu, take orders, and answer questions."
)

if not st.secrets.OPEN_API_KEY:
    st.info("OpenAI API key not available!", icon="🗝️")
else:
    # Create OpenAI client
    try:
        client = OpenAI(api_key=st.secrets.OPEN_API_KEY)

        # Initialize session state for chat messages
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "system",
                    "content": f"""
You are an experienced Indian cuisine specialist,You will suggest menu, educate the customers and provide automated service to collect orders for an Indian restaurant.
You first greet the customer, then start chatting with the customer.
and the take the order, 
and then asks if it's a pickup or delivery. 
You wait to collect the entire order, then summarize it and check for a final time if the customer wants to add anything else. 
If it's a delivery, you ask for an address. 
Finally you collect the payment.
Make sure to clarify all options, extras and sizes to uniquely identify the item from the menu.
You respond in a short, very conversational friendly style. 
The menu includes:
{promt_menu}
"""
            }
        ]
    
        # Function to handle chat interaction
        def get_completion_from_messages(messages, model="gpt-4o", temperature=1):
            try:
                response = client.chat.completions.create(
                    model=model, messages=messages, temperature=temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                st.error(f"Error fetching response: {e}")
                return "Sorry, something went wrong."

        # Now that the system context has been set, request the dynamic welcome message
        prompt = "Generate a dynamic and engaging welcome message for a chatbot about Indian cuisine. Mention that users can explore the menu, place orders, and ask questions. And don't forget to add Namaste🙏."
        try:
            # # Generate the welcome message using OpenAI and extract the generated message
            # welcome_message = get_completion_from_messages(
            #     messages=[{"role": "system", "content": prompt}],
            #     model="gpt-4o",
            #     temperature=1
            # )

            # TODO: Apply the logic to generate dynamic message. For now use hardcoded message
            welcome_message="""Namaste! 🙏 Welcome to the delightful world of Indian cuisine, where every flavor tells a story and each dish is a celebration of culture and tradition. Our chatbot is here to guide you through a culinary journey like no other. Feel free to explore our diverse menu, brimming with authentic Indian dishes that cater to every palate. Whether you're in the mood for something spicy, tangy, or sweet, we've got you covered!

Ready to place an order? It's just a click away! If you have any questions about ingredients, dietary preferences, or spice levels, don't hesitate to ask. We're here to make your experience as enjoyable and informative as possible. Dive in and let the flavors of India enchant you! 🍛🥘🇮🇳"""

            st.write(welcome_message)
        
        except Exception as e:
            st.error(f"Error generating welcome message: {e}")

    except Exception as e:
        st.error(f"Error initializing OpenAI client: {e}")

# Display chat history
for message in st.session_state.messages:
    if message["role"]!="system":
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
        st.session_state.messages, model="gpt-4o", temperature=1
    )

    # Append and display AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
