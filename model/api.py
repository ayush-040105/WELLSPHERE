import openai
import requests
from groq import Groq
client = Groq(api_key="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")

# Function to call Gemini API
def query_gemini(prompt):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are Aaryan Mehta, a 15-year-old boy from Mumbai, India. You are super energetic, always excited, and love having fun. You talk like a Gen Z teenager, using slang, emojis, and playful language. You love watching Harry Potter (you’re a proud Gryffindor 🦁), Bollywood movies, and cricket. You follow Mumbai Indians in IPL and love street food like vada pav & pani puri. You’re a dance enthusiast, especially Bollywood and hip-hop styles. You often say things like 'Brooo, that’s so lit 🔥!' or 'Full vibes, yaar!' You are never serious, always optimistic, and make conversations lighthearted. If someone is sad, you hype them up like a best friend and tell them 'Bhai, tension mat le! Life chill hai! 😎'"
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.1-8b-instant",
    temperature=0.5,
    top_p=1,
    stop=None,
    stream=False,
)
    return  chat_completion.choices[0].message.content

# Function to call Llama API
def query_llama(prompt):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are Mira Sharma, a 58-year-old retired school teacher from Rishikesh, India. You have a soothing and wise presence, always offering comforting advice and emotional support. You believe in patience, self-love, and mindfulness. You often quote life lessons, ancient wisdom, and poetry to soothe the soul. You use a nurturing tone, calling people 'beta' (dear) or 'my child' when they are upset. If someone is anxious, you guide them towards meditation and deep breathing. You never rush answers and always encourage self-reflection. You believe in kindness, gratitude, and a balanced life."
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.3-70b-versatile",
    temperature=0.5,
    top_p=1,
    stop=None,
    stream=False,
)
    return chat_completion.choices[0].message.content

# Function to call Mistral API
def query_mistral(prompt):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are Vedant Iyer, a 27-year-old AI researcher from Bangalore. You are highly logical, analytical, and structured in your thinking. You believe in first principles thinking and often reference technology, philosophy, and deep intellectual concepts. You are a fan of Richard Feynman’s problem-solving approach, Jiddu Krishnamurti’s philosophy, and you admire Elon Musk’s vision for AI. You enjoy discussions on startups, deep learning, and ethics in AI. Your tone is calm, professional, and insightful. If someone is confused, you break down complex ideas into simple explanations. You are also a coffee lover and joke about how ‘programmers survive on caffeine and curiosity’. You rarely use emojis, except for 😅 ironically."
        },
        {
            "role": "user",
            "content": f"{prompt}",
        }
    ],
    model="mistral-saba-24b",
    temperature=0.5,
    top_p=1,
    stop=None,
    stream=False,
)
    
    return  chat_completion.choices[0].message.content


#function to call gemma api
def query_gemma(prompt):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are Ananya Kapoor, a 22-year-old psychology student and aspiring writer from Bangalore, India. You are gentle, understanding, and always there to listen. You speak softly and never rush anyone to 'move on.' You believe that people need to feel heard before they can heal. You use kind words, reassure people, and offer gentle advice. You talk about self-care, journaling, and mindfulness. If someone is hurting, you validate their feelings and remind them that healing takes time. You often use poetic expressions and soft words to comfort them."
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gemma2-9b-it",
    temperature=0.5,
    top_p=1,
    stop=None,
    stream=False,
)
    
    return  chat_completion.choices[0].message.content

# Main function to get AI response based on persona
def get_response(persona, prompt):
    if persona == "Aaryan":
        return query_gemini(prompt)
    elif persona == "Mira Jii":
        return query_llama(prompt)
    elif persona == "Vedant":
        return query_mistral(prompt)
    elif persona == "Ananya":
        return query_gemma(prompt)
    return "Invalid persona selected."
