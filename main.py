import os
from app import app
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Check if DATABASE_URL is set
    if not os.environ.get("DATABASE_URL"):
        # For local development without DATABASE_URL environment variable
        logger.warning("DATABASE_URL not found in environment. Using SQLite as fallback.")
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mood_music.db"
    
    # Print configuration for debugging
    logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Run the app
    app.run(host="0.0.0.0", port=5000, debug=True)
