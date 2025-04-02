# Music database organized by mood categories
# This serves as a simple in-memory database of music recommendations
# Updated with trending and new songs as of 2025

mood_to_songs = {
    'happy': [
        {'title': 'Happy', 'artist': 'Pharrell Williams', 'album': 'G I R L'},
        {'title': 'Uptown Funk', 'artist': 'Mark Ronson ft. Bruno Mars', 'album': 'Uptown Special'},
        {'title': "Can't Stop the Feeling!", 'artist': 'Justin Timberlake', 'album': 'Trolls (Original Motion Picture Soundtrack)'},
        {'title': 'Good as Hell', 'artist': 'Lizzo', 'album': 'Cuz I Love You'},
        {'title': 'Walking on Sunshine', 'artist': 'Katrina and The Waves', 'album': 'Walking on Sunshine'},
        {'title': 'Shake It Off', 'artist': 'Taylor Swift', 'album': '1989'},
        # New trending songs
        {'title': 'Dance The Night', 'artist': 'Dua Lipa', 'album': 'Barbie: The Album', 'trending': True},
        {'title': 'Butter', 'artist': 'BTS', 'album': 'Butter', 'trending': True},
        {'title': 'As It Was', 'artist': 'Harry Styles', 'album': "Harry's House", 'trending': True}
    ],
    'sad': [
        {'title': 'Someone Like You', 'artist': 'Adele', 'album': '21'},
        {'title': 'Hurt', 'artist': 'Johnny Cash', 'album': 'American IV: The Man Comes Around'},
        {'title': 'Fix You', 'artist': 'Coldplay', 'album': 'X&Y'},
        {'title': 'All I Want', 'artist': 'Kodaline', 'album': 'In a Perfect World'},
        {'title': 'Skinny Love', 'artist': 'Bon Iver', 'album': 'For Emma, Forever Ago'},
        {'title': 'Hello', 'artist': 'Adele', 'album': '25'},
        # New trending songs
        {'title': 'Drivers License', 'artist': 'Olivia Rodrigo', 'album': 'SOUR', 'trending': True},
        {'title': 'Easy On Me', 'artist': 'Adele', 'album': '30', 'trending': True},
        {'title': 'Happier Than Ever', 'artist': 'Billie Eilish', 'album': 'Happier Than Ever', 'trending': True}
    ],
    'relaxed': [
        {'title': 'Weightless', 'artist': 'Marconi Union', 'album': 'Weightless'},
        {'title': 'Pure Shores', 'artist': 'All Saints', 'album': 'Saints & Sinners'},
        {'title': 'Watermark', 'artist': 'Enya', 'album': 'Watermark'},
        {'title': 'Gymnopédie No.1', 'artist': 'Erik Satie', 'album': 'Gymnopédies'},
        {'title': 'Porcelain', 'artist': 'Moby', 'album': 'Play'},
        {'title': 'Clair de Lune', 'artist': 'Claude Debussy', 'album': 'Suite bergamasque'},
        # New trending songs
        {'title': 'Calm Down', 'artist': 'Rema & Selena Gomez', 'album': 'Rave & Roses', 'trending': True},
        {'title': 'Flowers', 'artist': 'Miley Cyrus', 'album': 'Endless Summer Vacation', 'trending': True},
        {'title': 'Daylight', 'artist': 'Taylor Swift', 'album': 'Lover', 'trending': True}
    ],
    'energetic': [
        {'title': 'Eye of the Tiger', 'artist': 'Survivor', 'album': 'Eye of the Tiger'},
        {'title': 'Stronger', 'artist': 'Kanye West', 'album': 'Graduation'},
        {'title': 'Power', 'artist': 'Kanye West', 'album': 'My Beautiful Dark Twisted Fantasy'},
        {'title': 'Till I Collapse', 'artist': 'Eminem ft. Nate Dogg', 'album': 'The Eminem Show'},
        {'title': 'Thunderstruck', 'artist': 'AC/DC', 'album': 'The Razors Edge'},
        {'title': 'Lose Yourself', 'artist': 'Eminem', 'album': '8 Mile Soundtrack'},
        # New trending songs
        {'title': 'STAY', 'artist': 'The Kid LAROI & Justin Bieber', 'album': 'F*CK LOVE 3: OVER YOU', 'trending': True},
        {'title': 'Levitating', 'artist': 'Dua Lipa', 'album': 'Future Nostalgia', 'trending': True},
        {'title': 'Unstoppable', 'artist': 'Sia', 'album': 'This Is Acting', 'trending': True}
    ],
    'angry': [
        {'title': 'Break Stuff', 'artist': 'Limp Bizkit', 'album': 'Significant Other'},
        {'title': 'Killing In The Name', 'artist': 'Rage Against The Machine', 'album': 'Rage Against The Machine'},
        {'title': 'Given Up', 'artist': 'Linkin Park', 'album': 'Minutes to Midnight'},
        {'title': 'The Way I Am', 'artist': 'Eminem', 'album': 'The Marshall Mathers LP'},
        {'title': 'Platypus (I Hate You)', 'artist': 'Green Day', 'album': 'Nimrod'},
        {'title': 'I Hate Everything About You', 'artist': 'Three Days Grace', 'album': 'Three Days Grace'},
        # New trending songs
        {'title': 'good 4 u', 'artist': 'Olivia Rodrigo', 'album': 'SOUR', 'trending': True},
        {'title': 'MONTERO (Call Me By Your Name)', 'artist': 'Lil Nas X', 'album': 'MONTERO', 'trending': True},
        {'title': 'Kill Bill', 'artist': 'SZA', 'album': 'SOS', 'trending': True}
    ],
    'romantic': [
        {'title': 'All of Me', 'artist': 'John Legend', 'album': 'Love in the Future'},
        {'title': 'Perfect', 'artist': 'Ed Sheeran', 'album': '÷ (Divide)'},
        {'title': 'Thinking Out Loud', 'artist': 'Ed Sheeran', 'album': 'x (Multiply)'},
        {'title': 'At Last', 'artist': 'Etta James', 'album': 'At Last!'},
        {'title': 'Lovesong', 'artist': 'The Cure', 'album': 'Disintegration'},
        {'title': 'Make You Feel My Love', 'artist': 'Adele', 'album': '19'},
        # New trending songs
        {'title': 'Die With A Smile', 'artist': 'Bruno Mars & Lady Gaga', 'album': 'Single', 'trending': True},
        {'title': 'Lover', 'artist': 'Taylor Swift', 'album': 'Lover', 'trending': True},
        {'title': 'Anyone', 'artist': 'Justin Bieber', 'album': 'Justice', 'trending': True}
    ],
    'anxious': [
        {'title': 'Breathe Me', 'artist': 'Sia', 'album': 'Colour the Small One'},
        {'title': 'Fix You', 'artist': 'Coldplay', 'album': 'X&Y'},
        {'title': 'Everybody Hurts', 'artist': 'R.E.M.', 'album': 'Automatic for the People'},
        {'title': 'Unsteady', 'artist': 'X Ambassadors', 'album': 'VHS'},
        {'title': 'Breathe (2 AM)', 'artist': 'Anna Nalick', 'album': 'Wreck of the Day'},
        {'title': 'I Need Some Sleep', 'artist': 'Eels', 'album': 'Shrek 2: Motion Picture Soundtrack'},
        # New trending songs
        {'title': 'Hold On', 'artist': 'Justin Bieber', 'album': 'Justice', 'trending': True},
        {'title': 'Everything I Wanted', 'artist': 'Billie Eilish', 'album': 'Everything I Wanted', 'trending': True},
        {'title': 'Panic Attack', 'artist': 'Elohim', 'album': 'Elohim', 'trending': True}
    ],
    'nostalgic': [
        {'title': 'In My Life', 'artist': 'The Beatles', 'album': 'Rubber Soul'},
        {'title': '1979', 'artist': 'The Smashing Pumpkins', 'album': 'Mellon Collie and the Infinite Sadness'},
        {'title': 'Vienna', 'artist': 'Billy Joel', 'album': 'The Stranger'},
        {'title': 'Landslide', 'artist': 'Fleetwood Mac', 'album': 'Fleetwood Mac'},
        {'title': 'Good Riddance (Time of Your Life)', 'artist': 'Green Day', 'album': 'Nimrod'},
        {'title': 'Memories', 'artist': 'Maroon 5', 'album': 'Memories'},
        # New trending songs
        {'title': 'Anti-Hero', 'artist': 'Taylor Swift', 'album': 'Midnights', 'trending': True},
        {'title': 'Heat Waves', 'artist': 'Glass Animals', 'album': 'Dreamland', 'trending': True},
        {'title': 'Last Last', 'artist': 'Burna Boy', 'album': 'Love, Damini', 'trending': True}
    ],
    'focused': [
        {'title': 'Experience', 'artist': 'Ludovico Einaudi', 'album': 'In a Time Lapse'},
        {'title': 'Nuvole Bianche', 'artist': 'Ludovico Einaudi', 'album': 'Una Mattina'},
        {'title': 'Time', 'artist': 'Hans Zimmer', 'album': 'Inception (Music from the Motion Picture)'},
        {'title': 'Divenire', 'artist': 'Ludovico Einaudi', 'album': 'Divenire'},
        {'title': 'Strobe', 'artist': 'deadmau5', 'album': 'For Lack of a Better Name'},
        {'title': 'Avril 14th', 'artist': 'Aphex Twin', 'album': 'Drukqs'},
        # New trending songs
        {'title': 'Deep Focus', 'artist': 'Brian Eno', 'album': 'Ambient 1: Music for Airports', 'trending': True},
        {'title': 'Concentration', 'artist': 'KAMAUU', 'album': 'A Gorgeous Fortune', 'trending': True},
        {'title': 'Study Beats', 'artist': 'Lo-Fi Beats', 'album': 'Chill Study Session', 'trending': True}
    ],
    'sleepy': [
        {'title': 'Moonlight Sonata', 'artist': 'Ludwig van Beethoven', 'album': 'Beethoven: Piano Sonatas'},
        {'title': 'Claire de Lune', 'artist': 'Claude Debussy', 'album': 'Debussy: Suite Bergamasque'},
        {'title': 'Comptine d\'un autre été', 'artist': 'Yann Tiersen', 'album': 'Amélie: Original Soundtrack'},
        {'title': 'Dreams', 'artist': 'Fleetwood Mac', 'album': 'Rumours'},
        {'title': 'Holocene', 'artist': 'Bon Iver', 'album': 'Bon Iver'},
        {'title': 'Saturn', 'artist': 'Sleeping At Last', 'album': 'Atlas: Space'},
        # New trending songs
        {'title': 'Dreamland', 'artist': 'Glass Animals', 'album': 'Dreamland', 'trending': True},
        {'title': 'Sleep On The Floor', 'artist': 'The Lumineers', 'album': 'Cleopatra', 'trending': True},
        {'title': 'Deep Sleep Drone', 'artist': 'Sleeping Music', 'album': 'Sleep Sounds', 'trending': True}
    ]
}
