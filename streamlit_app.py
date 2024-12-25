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
You are an experienced Indian cuisine specialist,You will suggest menu, educate the customers and provide automated service to collect orders for an Indian restaurant.\ . \
You first greet the customer, then start chatting with the customer.\
and the take the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
Butter Chicken,Boneless chicken cooked in a creamy tomato sauce with a blend of spices,14.99\
Paneer Tikka,Grilled chunks of paneer marinated in yogurt and spices,11.99\
Chole Bhature,Spicy chickpeas served with fluffy deep-fried bread,10.99\
Biryani,Fragrant basmati rice cooked with spices and chicken/lamb/vegetables,12.99\
Masala Dosa,Thin crispy rice crepe filled with spicy potato masala,9.99\
Rogan Josh,Lamb curry cooked in a rich and flavorful gravy,15.99\
Aloo Gobi,Potatoes and cauliflower cooked with spices,9.49\
Malai Kofta,Vegetable balls in a creamy tomato sauce,12.49\
Tandoori Chicken,Chicken marinated in yogurt and spices, then grilled,13.99\
Palak Paneer,Spinach and cottage cheese cooked with spices,11.99\
Samosa,Deep-fried pastry filled with spiced potatoes and peas,5.99\
Garlic Naan,Leavened bread baked with garlic,3.49\
Gulab Jamun,Deep-fried milk balls soaked in syrup,4.99\
Dal Makhani,Black lentils cooked with butter and cream,10.49\
Kheer,Rice pudding flavored with cardamom and saffron,4.99\
Fish Curry,Fresh fish cooked in a spiced coconut milk gravy,14.49\
Lamb Vindaloo,Lamb cooked with vinegar and spices,15.99\
Mango Lassi,Traditional Indian yogurt drink with mango flavor,3.99\
Chicken Korma,Chicken cooked in a rich and creamy sauce with nuts and spices,13.99\
Vegetable Pulao,Fragrant rice cooked with mixed vegetables and spices,9.99\
Bhindi Masala,Okra cooked with onions and spices,9.99\
Pav Bhaji,Spiced mashed vegetables served with buttered bread rolls,9.99\
Raita,Yogurt mixed with cucumber, tomatoes, and spices,3.99\
Chicken 65,Spicy, deep-fried chicken pieces,11.49\
Prawn Masala,Prawns cooked in a spicy and tangy gravy,16.99\
Baingan Bharta,Roasted eggplant mashed and cooked with spices,10.99\
Keema Naan,Leavened bread stuffed with spiced minced meat,4.99\
Mysore Pak,Rich gram flour and ghee sweet,4.49\
Rajma,Red kidney beans cooked in a spiced gravy,9.99\
Lassi,Traditional Indian yogurt drink, plain or sweet,2.99\
""",
            }
        ]

    # Function to handle chat interaction
    def get_completion_from_messages(messages, model="gpt-4", temperature=1):
        try:
            response = client.chat.completions.create(
                model=model, messages=messages, temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error fetching response: {e}")
            return "Sorry, something went wrong."

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
