import streamlit as st
from models.api import get_response
import random

# Streamlit App Configuration
st.set_page_config(
    page_title="AI Persona Chatbot", 
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .stApp {
            background-color: rgb(235, 235, 235);
        }
        .sidebar .sidebar-content {
            background-color: #2c3e50;
            color: white;
        }
        .stRadio > div {
            flex-direction: column;
            gap: 10px;
        }
        .stRadio > div > label {
            padding: 15px;
            border-radius: 10px;
            transition: all 0.3s;
            background-color: #34495e;
            color: white !important;
        }
        .stRadio > div > label:hover {
            background-color: #3d566e;
            transform: translateX(5px);
        }
        [data-testid=stRadio] > div > div > label > div:first-child {
            font-weight: bold;
            font-size: 16px;
        }
        /*.chat-container {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            height: 65vh;
            overflow-y: auto;
        }*/
        .user-message {
            background-color: rgb(150, 80, 255);
            padding: 12px 15px;
            border-radius: 18px 18px 0 18px;
            margin: 8px 0;
            max-width: 80%;
            margin-left: auto;
        }
        .bot-message {
            background-color: white;
            padding: 12px 15px;
            border-radius: 18px 18px 18px 0;
            margin: 8px 0;
            max-width: 80%;
            color: black;
        }
        .stTextInput > div > div > input {
            border-radius: 20px !important;
            padding: 12px !important;
        }
        .stButton > button {
            border-radius: 20px !important;
            padding: 10px 25px !important;
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold !important;
            border: none !important;
        }
        .persona-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        .persona-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #4CAF50;
        }
        .typing-indicator {
            display: inline-block;
            padding: 10px;
        }
        .typing-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #888;
            margin: 0 2px;
            animation: typingAnimation 1.4s infinite ease-in-out;
        }
            
        /* Text input box styling */
        .stTextInput>div>div>input {
            background-color: #f0f2f6;  /* Light gray background */
            color: Black;              /* font color */
            //border: 1px solid #dfe1e5; /* Light border */
            border-radius: 10px;       /* Rounded corners */
            padding: 12px 15px;        /* Inner spacing */
        }
        
        /* Change font color when typing */
        .stTextInput>div>div>input::placeholder {
            color: black;            /* Gray placeholder text */
        }
        
        /* Focus state styling */
        .stTextInput>div>div>input:focus {
            background-color: #ffffff;  /* White background when focused */
            //border-color: #4CAF50;     /* Green border when focused */
            //box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }
            
        
        .typing-dot:nth-child(1) { animation-delay: 0s; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typingAnimation {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-5px); }
        }
    </style>
""", unsafe_allow_html=True)

# Persona avatars and descriptions
personas = {
    "Aaryan": {
        "avatar": "🤹",
        "description": "Energetic, funny, and lighthearted like a Gen Z buddy 🔥",
        "color": "#3498db"
    },
    "Mira Jii": {
        "avatar": "👵",
        "description": "Wise, spiritual, and comforting like a grandmother",
        "color": "#e74c3c"
    },
    "Vedant": {
        "avatar": "👨‍💻",
        "description": "Analytical, intellectual, and structured like a philosopher-researcher 🧠",
        "color": "#2ecc71"
    },
    "Ananya": {
        "avatar": "🧑‍🤝‍🧑",
        "description": "Gentle, supportive, and soft-spoken like a best friend 🌸",
        "color": "#9b59b6"
    }
}

# Sidebar for persona selection
with st.sidebar:
    st.markdown("<h1 style='color: white;'>Persona Selector</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ecf0f1;'>Choose who you'd like to chat with:</p>", unsafe_allow_html=True)
    
    persona = st.radio(
        "Choose a Persona:",
        options=list(personas.keys()),
        format_func=lambda x: f"{personas[x]['avatar']} {x}",
        label_visibility="collapsed"
    )
    
    st.markdown(f"""
        <div style='margin-top: 30px; padding: 15px; background-color: {personas[persona]['color']}20; border-radius: 10px; border-left: 4px solid {personas[persona]['color']};'>
            <h3 style='color: {personas[persona]['color']}; margin-bottom: 5px;'>{personas[persona]['avatar']} About {persona}</h3>
            <p style='color: #7f8c8d;'>{personas[persona]['description']}</p>
        </div>
    """, unsafe_allow_html=True)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header with persona info
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.markdown(f"<div style='font-size: 40px;'>{personas[persona]['avatar']}</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<h1 style='margin-bottom: 5px; color: black'>Chat with {persona}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: black; margin-top: 0;'>{personas[persona]['description']}</p>", unsafe_allow_html=True)

# Chat container
with st.container():
    chat_container = st.empty()
    
    with chat_container.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        
        for msg in st.session_state.chat_history:
            if msg["sender"] == "user":
                st.markdown(f"<div class='user-message'> {msg['message']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-message'> {msg['message']}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Chat input at bottom
input_col, button_col = st.columns([0.85, 0.15])
with input_col:
    prompt = st.text_input(
        "Type your message...", 
        key="input",
        label_visibility="collapsed",
        placeholder=f"Message {persona}..."
    )
with button_col:
    send_button = st.button("Send", use_container_width=True)

if send_button and prompt:
    # Add user message to chat
    st.session_state.chat_history.append({"sender": "user", "message": prompt})
    
    # Show typing indicator
    with chat_container.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        
        for msg in st.session_state.chat_history[:-1]:  # All messages except the new one
            if msg["sender"] == "user":
                st.markdown(f"<div class='user-message'><strong>You:</strong> {msg['message']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-message'><strong>{persona}:</strong> {msg['message']}</div>", unsafe_allow_html=True)
        
        # Show user's new message
        st.markdown(f"<div class='user-message'><strong>You:</strong> {prompt}</div>", unsafe_allow_html=True)
        
        # Typing indicator
        st.markdown("""
            <div class='bot-message'>
                <strong>{persona}:</strong> 
                <div class='typing-indicator'>
                    <span class='typing-dot'></span>
                    <span class='typing-dot'></span>
                    <span class='typing-dot'></span>
                </div>
            </div>
        """.format(persona=persona), unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Get bot response (simulate delay for realism)
    with st.spinner(""):
        response = get_response(persona, prompt)
    
    # Add bot response to chat
    st.session_state.chat_history.append({"sender": "bot", "message": response})
    st.rerun()