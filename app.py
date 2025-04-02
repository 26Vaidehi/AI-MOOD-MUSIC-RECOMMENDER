import os
import logging
import json
import re
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from music_data import mood_to_songs

# Import database and models
from models import db, ChatHistory, MoodStatistics, MoodHistory

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define mood keywords to identify user's mood
mood_keywords = {
    'happy': ['happy', 'cheerful', 'joy', 'joyful', 'excited', 'good', 'great', 'fantastic', 'wonderful', 'positive', 'upbeat'],
    'sad': ['sad', 'depressed', 'unhappy', 'down', 'blue', 'gloomy', 'heartbroken', 'melancholy', 'upset', 'negative'],
    'angry': ['angry', 'mad', 'frustrated', 'irritated', 'annoyed', 'furious', 'rage', 'outraged'],
    'relaxed': ['relaxed', 'calm', 'peaceful', 'chill', 'tranquil', 'serene', 'zen', 'mellow', 'soothing'],
    'romantic': ['romantic', 'love', 'loving', 'passionate', 'affectionate', 'dreamy', 'sentimental'],
    'energetic': ['energetic', 'pumped', 'hyper', 'motivated', 'dynamic', 'lively', 'enthusiastic', 'active', 'workout'],
    'anxious': ['anxious', 'stressed', 'nervous', 'worried', 'tense', 'uneasy', 'panic', 'restless'],
    'nostalgic': ['nostalgic', 'memory', 'reminiscent', 'reflective', 'thoughtful', 'sentimental'],
    'focused': ['focused', 'productive', 'concentration', 'study', 'work', 'determined', 'concentrate'],
    'sleepy': ['sleepy', 'tired', 'drowsy', 'exhausted', 'sleep', 'bedtime', 'dreamy', 'night']
}

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback_secret_key")

# Configure the database
# Check different possible database URL environment variables
database_url = os.environ.get("DATABASE_URL")

# Convert postgres:// to postgresql:// if needed (Railway PostgreSQL format fix)
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    
    # Initialize mood statistics if they don't exist
    for mood in mood_keywords.keys():
        existing = MoodStatistics.query.filter_by(mood=mood).first()
        if not existing:
            db.session.add(MoodStatistics(mood=mood, count=0))
    db.session.commit()

# Mood-specific emojis for responses
mood_emojis = {
    'happy': '😊',
    'sad': '😢',
    'angry': '😠',
    'relaxed': '😌',
    'romantic': '❤️',
    'energetic': '⚡',
    'anxious': '😰',
    'nostalgic': '🕰️',
    'focused': '🧠',
    'sleepy': '😴'
}

# Colors for mood chart
mood_colors = {
    'happy': '#ffcc00',      # Yellow
    'sad': '#3498db',        # Blue
    'angry': '#e74c3c',      # Red
    'relaxed': '#2ecc71',    # Green
    'romantic': '#e84393',   # Pink
    'energetic': '#f39c12',  # Orange 
    'anxious': '#9b59b6',    # Purple
    'nostalgic': '#7f8c8d',  # Grey
    'focused': '#1abc9c',    # Teal
    'sleepy': '#34495e'      # Dark blue
}

# Mood-specific conversation starters
mood_conversations = {
    'happy': [
        "That's a great mood to be in! Let's find some upbeat tunes to keep that positive energy going!",
        "Awesome! Happy vibes call for happy music. Check these out:",
        "I love matching happy moods with energetic music! Here's what I recommend:"
    ],
    'sad': [
        "I understand feeling down sometimes. Music can be a great comfort. Here are some songs that might resonate:",
        "When you're feeling blue, the right music can help you process those emotions. Try these:",
        "Sometimes sad songs can actually make us feel better when we're down. See if these help:"
    ],
    'angry': [
        "Sounds like you need to release some frustration! These tracks might help:",
        "Music can be a great outlet for anger. Let these powerful songs help you express those feelings:",
        "When you're feeling angry, sometimes the right song can help you channel that energy. Try these:"
    ],
    'relaxed': [
        "A relaxed mood deserves some smooth, calming tunes. Check these out:",
        "Perfect time for some chill music to maintain that peaceful state. Here are my picks:",
        "Relaxation and good music go hand in hand. These songs should complement your mood:"
    ],
    'romantic': [
        "Feeling the love? These romantic tracks might be perfect for your mood:",
        "Romance and music are perfect partners. Here are some songs to match your feelings:",
        "When love is in the air, these songs can enhance the mood:"
    ],
    'energetic': [
        "That energetic spirit deserves some high-tempo music! Try these motivating tracks:",
        "When you're feeling pumped up, these songs will keep that energy flowing:",
        "Your energetic mood calls for some powerful beats! Check these out:"
    ],
    'anxious': [
        "I know anxiety can be challenging. These soothing tracks might help calm your mind:",
        "When you're feeling anxious, gentle music can help ground you. Give these a try:",
        "Music has a wonderful way of easing anxiety. These songs are selected to help you relax:"
    ],
    'nostalgic': [
        "Nostalgia is such a special feeling. These songs might enhance those reflective moments:",
        "Taking a trip down memory lane? These tracks make perfect companions for nostalgia:",
        "Nostalgic moods call for songs that touch the soul. Here are some recommendations:"
    ],
    'focused': [
        "Need to stay concentrated? These tracks are perfect for maintaining focus:",
        "When you're in work mode, the right music can boost productivity. Try these:",
        "For a focused mind, instrumental pieces often work best. Check out these recommendations:"
    ],
    'sleepy': [
        "Feeling tired? These gentle songs might help you drift off to dreamland:",
        "When sleep is calling, these soothing melodies can help you answer:",
        "These calm, peaceful tracks are perfect for winding down when you're feeling sleepy:"
    ]
}

# Define chatbot responses
greetings = [
    "Hello! How are you feeling today? 🎵", 
    "Hi there! What kind of mood are you in? I'd love to suggest some music! 🎧", 
    "Hey! How's your mood right now? I can recommend the perfect soundtrack! 🎼", 
    "Welcome to Mood Music! How's your day going? Let me find your perfect playlist! 🎹"
]

follow_ups = [
    "Would you like more recommendations? I have plenty more songs that match your mood! 🎵",
    "How do you like these suggestions? I can find different styles if you prefer! 🎧",
    "Would you like different songs for this mood? Or maybe try a new mood? 🎼",
    "Do these match what you're looking for? I'd be happy to refine my recommendations! 🎹"
]

fun_facts = [
    "Did you know music can reduce stress by up to 65%? 🧠",
    "Fun fact: Listening to music releases dopamine, the 'feel good' chemical in your brain! 💫",
    "Interesting tidbit: The 'Mozart Effect' suggests that listening to Mozart temporarily boosts spatial reasoning! 🎻",
    "Music fact: Songs with 60-80 BPM can help synchronize with your heartbeat and induce relaxation! ❤️",
    "Did you know? The longest recorded pop song is over 13 hours long! ⏱️"
]

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/stats')
def mood_stats():
    """Get mood statistics."""
    try:
        stats = MoodStatistics.query.all()
        mood_data = {stat.mood: stat.count for stat in stats}
        total = sum(mood_data.values())
        
        # Calculate percentages
        if total > 0:
            percentages = {mood: round((count / total) * 100, 1) for mood, count in mood_data.items()}
        else:
            percentages = {mood: 0 for mood in mood_data.keys()}
            
        result = {
            'total_interactions': total,
            'mood_counts': mood_data,
            'mood_percentages': percentages
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': "Could not retrieve mood statistics."})

@app.route('/history')
def chat_history():
    """Get chat history."""
    try:
        limit = request.args.get('limit', default=50, type=int)
        history = ChatHistory.query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
        
        result = []
        for entry in history:
            result.append({
                'id': entry.id,
                'user_message': entry.user_message,
                'bot_response': entry.bot_response,
                'detected_mood': entry.detected_mood,
                'created_at': entry.created_at.isoformat()
            })
            
        return jsonify({'history': result, 'count': len(result)})
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        return jsonify({'error': "Could not retrieve chat history."})
        
@app.route('/mood-history')
def mood_history():
    """Get mood history data for chart visualization."""
    try:
        # Get mood history data
        history = MoodHistory.query.order_by(MoodHistory.recorded_at.asc()).all()
        
        # Initialize data structure for chart.js
        moods = list(mood_keywords.keys())
        labels = []
        datasets = {}
        
        # Create a dataset for each mood
        for mood in moods:
            datasets[mood] = {
                'label': mood.capitalize(),
                'data': [],
                'fill': False,
                'borderColor': get_color_for_mood(mood),
                'tension': 0.1
            }
        
        # Group by date
        date_mood_counts = {}
        for entry in history:
            # Format date as YYYY-MM-DD
            date_str = entry.recorded_at.strftime('%Y-%m-%d')
            mood = entry.mood
            
            if date_str not in date_mood_counts:
                date_mood_counts[date_str] = {mood: 1 for mood in moods}
            
            if mood in date_mood_counts[date_str]:
                date_mood_counts[date_str][mood] += 1
        
        # Sort dates and add to datasets
        sorted_dates = sorted(date_mood_counts.keys())
        labels = sorted_dates
        
        for date in sorted_dates:
            for mood in moods:
                count = date_mood_counts[date].get(mood, 0)
                datasets[mood]['data'].append(count)
        
        # Convert datasets dictionary to list for chart.js
        datasets_list = [datasets[mood] for mood in moods]
        
        result = {
            'labels': labels,
            'datasets': datasets_list
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting mood history: {str(e)}")
        return jsonify({'error': "Could not retrieve mood history data."})

@app.route('/chat', methods=['POST'])
def chat():
    """Process the user's message and return a response."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        logger.debug(f"Received message: {user_message}")
        
        # Default response and mood
        bot_response = None
        identified_mood = None
        
        # Check for greetings or initial messages
        if any(greeting in user_message for greeting in ['hi', 'hello', 'hey', 'greetings']):
            bot_response = random.choice(greetings) + " " + random.choice(fun_facts)
            result = {'response': bot_response}
        
        # Check for goodbye messages
        elif any(bye in user_message for bye in ['bye', 'goodbye', 'see you', 'exit']):
            bot_response = 'Goodbye! 👋 Come back anytime for more music recommendations! Remember, the right song can transform any mood! 🎵'
            result = {'response': bot_response}
        
        # Check for help or commands 
        elif any(help_term in user_message for help_term in ['help', 'what can you do', 'commands', 'features']):
            help_text = (
                "I'm your music mood assistant! Here's what I can do:\n\n"
                "🎵 Recommend songs based on your mood\n"
                "🧠 Share interesting music facts\n"
                "🔍 Help you find songs on YouTube\n"
                "🎧 Simulate playing music previews\n\n"
                "Just tell me how you're feeling (happy, sad, energetic, etc.) or click one of the mood buttons below!"
            )
            bot_response = help_text
            result = {'response': bot_response}
        
        # Check for random mood request
        elif any(random_term in user_message for random_term in ['random mood', 'surprise me', 'any mood', 'pick for me']):
            identified_mood = random.choice(list(mood_keywords.keys()))
            mood_emoji = mood_emojis.get(identified_mood, '')
            response = f"Let's try a {identified_mood} mood! {mood_emoji} "
            songs = get_songs_for_mood(identified_mood)
            songs_text = format_song_recommendations(songs)
            bot_response = f"{response}\n\n{random.choice(mood_conversations[identified_mood])}\n\n{songs_text}\n\n{random.choice(follow_ups)}"
            result = {'response': bot_response, 'mood': identified_mood}
            
            # Update mood statistics and history for random mood
            with app.app_context():
                # Update statistics counter
                mood_stat = MoodStatistics.query.filter_by(mood=identified_mood).first()
                if mood_stat:
                    mood_stat.count += 1
                
                # Add to mood history for charting
                mood_history_entry = MoodHistory(mood=identified_mood)
                db.session.add(mood_history_entry)
                
                db.session.commit()
        
        else:
            # Determine user's mood from the message
            identified_mood = identify_mood(user_message)
            
            if identified_mood:
                # Get songs for the identified mood
                songs = get_songs_for_mood(identified_mood)
                
                if songs:
                    # Format the song recommendations
                    songs_text = format_song_recommendations(songs)
                    
                    # Get mood emoji
                    mood_emoji = mood_emojis.get(identified_mood, '')
                    
                    # Craft response with more personality
                    mood_response = random.choice(mood_conversations[identified_mood])
                    
                    # Maybe add a fun fact (30% chance)
                    fun_fact = ""
                    if random.random() < 0.3:
                        fun_fact = f"\n\n{random.choice(fun_facts)}"
                    
                    bot_response = f"{mood_emoji} {mood_response}\n\n{songs_text}{fun_fact}\n\n{random.choice(follow_ups)}"
                    result = {'response': bot_response, 'mood': identified_mood}
                    
                    # Update mood statistics and history
                    with app.app_context():
                        # Update statistics counter
                        mood_stat = MoodStatistics.query.filter_by(mood=identified_mood).first()
                        if mood_stat:
                            mood_stat.count += 1
                        
                        # Add to mood history for charting
                        mood_history_entry = MoodHistory(mood=identified_mood)
                        db.session.add(mood_history_entry)
                        
                        db.session.commit()
                else:
                    bot_response = "I'm sorry, I couldn't find any songs for that mood at the moment. Could you try describing your mood differently? Or try one of the mood buttons below! 🎵"
                    result = {'response': bot_response}
            else:
                bot_response = "I'm not sure I understand your mood. Could you describe how you're feeling more clearly? For example, 'I'm feeling happy' or 'I'm in a relaxed mood'. Or simply click one of the mood buttons below! 🎼"
                result = {'response': bot_response}
        
        # Save chat history to database
        if bot_response:
            with app.app_context():
                chat_entry = ChatHistory(
                    user_message=user_message,
                    bot_response=bot_response,
                    detected_mood=identified_mood
                )
                db.session.add(chat_entry)
                db.session.commit()
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        return jsonify({'response': "Sorry, I encountered an error. Please try again. 🎵"})

def identify_mood(message):
    """Identify the mood from the user's message."""
    for mood, keywords in mood_keywords.items():
        # Check if any keyword for this mood is in the message
        if any(re.search(r'\b' + keyword + r'\b', message) for keyword in keywords):
            return mood
    return None

def get_songs_for_mood(mood):
    """Get songs for the identified mood."""
    songs = mood_to_songs.get(mood, [])
    # Shuffle the songs to provide variety
    if songs:
        random.shuffle(songs)
    return songs

def format_song_recommendations(songs):
    """Format the song recommendations with emojis and style."""
    result = ""
    music_icons = ["🎵", "🎶", "🎸", "🎹", "🎷", "🎻", "🥁", "🎤"]
    
    for i, song in enumerate(songs[:3], 1):  # Limit to 3 recommendations
        icon = random.choice(music_icons)
        title = song['title']
        artist = song['artist']
        album = song['album']
        
        # YouTube search link
        youtube_search = f"https://www.youtube.com/results?search_query={title.replace(' ', '+')}+{artist.replace(' ', '+')}"
        
        # Check if there's a trending flag
        trending_badge = "🔥 Trending" if song.get('trending', False) else ""
        
        # Format the recommendation with the link
        result += f"{i}. {icon} \"{title}\" by {artist} ({album}) {trending_badge}\n"
        result += f"   <a href='{youtube_search}' target='_blank' class='song-link'>▶️ Listen on YouTube</a>\n"
    
    return result

def get_color_for_mood(mood):
    """Get the color for a specific mood for the chart."""
    return mood_colors.get(mood, '#6c757d')  # Default to gray if mood not found

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
