import pandas as pd

def get_songs_by_emotion(emotion):
    df = pd.read_csv("songs.csv")
    df.columns = df.columns.str.strip()  # Clean column headers
    df['emotion'] = df['emotion'].str.lower().str.strip()
    df['language'] = df['language'].str.lower().str.strip()
    
    emotion = emotion.lower().strip()
    songs = []

    filtered_df = df[df['emotion'] == emotion]

    for _, row in filtered_df.iterrows():
        if pd.notna(row['youtubelink']):
            songs.append({
                "Emotion": emotion,
                "Language": row['language'],
                "Song": row['song'],
                "Link": row['youtubelink'],
                "Platform": "YouTube"
            })
        if pd.notna(row['spotifylink']):
            songs.append({
                "Emotion": emotion,
                "Language": row['language'],
                "Song": row['song'],
                "Link": row['spotifylink'],
                "Platform": "Spotify"
            })

    return songs
