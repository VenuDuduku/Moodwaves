import streamlit as st
from PIL import Image
from predict_emotion import predict_emotion
from emotion_to_song import get_songs_by_emotion

st.set_page_config(page_title="MoodWaves - Emotion-Based Song Recommender", layout="centered")

st.title("🎵 MoodWaves")
st.markdown("Upload or capture your face image to detect emotion and get personalized song suggestions.")

# --- Emotion Mode Toggle ---
mode = st.radio("🎛️ Select Emotion Input Mode:", ["Auto Detect from Image", "Manual Selection"])

manual_emotion = None
if mode == "Manual Selection":
    manual_emotion = st.selectbox("🎭 Choose Emotion:", ["Happy", "Sad", "Angry", "Neutral", "Surprised"])

# --- Input Method Selection (only in Auto mode) ---
image = None
if mode == "Auto Detect from Image":
    input_method = st.radio("Select Input Method:", ["📤 Upload Image", "📸 Use Webcam"])

    if input_method == "📤 Upload Image":
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")

    elif input_method == "📸 Use Webcam":
        captured_image = st.camera_input("Capture a photo")
        if captured_image:
            image = Image.open(captured_image)
            st.image(image, caption="Captured Image")

# --- Language Filter ---
language_choice = st.selectbox("🌐 Preferred Language:", 
                               options=["All", "Telugu", "Hindi", "English", "Malayalam"])

# --- Emotion message utilities ---
def get_emotion_message(emotion):
    emotion = emotion.lower()
    messages = {
        "happy": "😊 You look joyful! Let’s play something upbeat 🎶",
        "sad": "😢 Feeling low? Here’s something soothing for you 🎵",
        "angry": "😠 You seem angry. Try these intense tracks 🔥",
        "neutral": "😐 Neutral vibe. Let’s keep it mellow 🎧",
        "surprised": "😲 Surprise in the air! Try something exciting 🎉"
    }
    return messages.get(emotion, "🎧 Let’s find music that fits your mood!")

def get_emotion_punctuation(emotion):
    return {
        "happy": "!",
        "sad": "...",
        "angry": "!!",
        "relaxed": "~",
        "neutral": ".",
        "surprised": "?!"
    }.get(emotion.lower(), ".")

# --- Final Emotion Determination ---
emotion = None

if mode == "Manual Selection" and manual_emotion:
    emotion = manual_emotion.lower()
    st.session_state['predicted_emotion'] = emotion

elif mode == "Auto Detect from Image" and image:
    if ('predicted_emotion' not in st.session_state or
        st.session_state.get('last_image') != image):

        emotion = predict_emotion(image)
        st.session_state.predicted_emotion = emotion
        st.session_state.last_image = image
    else:
        emotion = st.session_state.predicted_emotion

# --- Emotion Message Display ---
if emotion:
    # Construct full message
    punctuation = get_emotion_punctuation(emotion)
    emotion_display = f"🎭 Emotion: {emotion.capitalize()}{punctuation}"
    message_display = get_emotion_message(emotion)

    # Emotion-based background color
    emotion_colors = {
        "happy": "#fff8dc",      # light yellow
        "sad": "#f0f8ff",        # alice blue
        "angry": "#ffe4e1",      # misty rose
        "neutral": "#f5f5f5",    # light gray
        "surprised": "#fafad2"   # pale gold
    }
    bg_color = emotion_colors.get(emotion.lower(), "#f0f0f0")

    # Highlighted message block with better text color
    st.markdown(
        f"""
        <div style='
            background-color: {bg_color}; 
            padding: 12px 16px; 
            border-radius: 12px; 
            font-size: 18px; 
            font-weight: 500; 
            color: #222222; 
            line-height: 1.6;
        '>
            <b>{emotion_display}</b> {message_display}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Song Recommendations ---
    songs = get_songs_by_emotion(emotion)

    if language_choice != "All":
        songs = [s for s in songs if s['Language'].lower() == language_choice.lower()]

    if songs:
        st.markdown("### 🎶 Recommended Songs:")

        # Group songs by name and collect links
        grouped = {}
        for song in songs:
            name = song.get("Song", "Unknown")
            platform = song.get("Platform", "").lower()
            link = song.get("Link", "#")

            if name not in grouped:
                grouped[name] = {"youtube": "", "spotify": ""}

            if "youtube" in platform:
                grouped[name]["youtube"] = link
            elif "spotify" in platform:
                grouped[name]["spotify"] = link

        # Display each song in a row with logos
        for name, links in grouped.items():
            yt_icon = f'<a href="{links["youtube"]}" target="_blank"><img src="https://cdn-icons-png.flaticon.com/24/1384/1384060.png" alt="YouTube" style="vertical-align:middle; margin-right:10px;"></a>' if links["youtube"] else ""
            sp_icon = f'<a href="{links["spotify"]}" target="_blank"><img src="https://cdn-icons-png.flaticon.com/24/2111/2111624.png" alt="Spotify" style="vertical-align:middle;"></a>' if links["spotify"] else ""

            st.markdown(
                f'<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">'
                f'<span style="font-size:17px;">🎼 <b>{name}</b></span>'
                f'<span>{yt_icon}{sp_icon}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.warning(f"No songs found for **{emotion}** in **{language_choice}**.")
