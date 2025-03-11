# AI-Powered Code Mentor

## Overview
An agentic AI assistant built using Cohere and ChromaDB to help Python developers analyze code, detect issues, and receive real-time mentorship while maintaining conversation context.

## Features
- **File Monitoring System**: Detects and analyzes changes in Python files.
- **AI-Powered Code Analysis**: Uses Cohere AI for context-aware analysis, spotting inefficiencies and errors.
- **Memory Retrieval with ChromaDB**: Implements retrieval-augmented memory for conversation continuity.
- **Mentor-Like Responses**: Provides guidance without unnecessary rewrites.
- **Conversational Mode**: Enables interactive sessions for iterative code improvement.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/abaiml/ChatBot.git
   cd ChatBot
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables by creating a `.env` file:
   ```
   COHERE_API_KEY=your_api_key_here
   ```

## Usage
### Start Chatbot
Run the chatbot in interactive mode:
```
python chatbot.py
```

### Monitor Directory for Changes
Modify the `WATCH_DIRECTORY` variable in `monitor.py` to specify the directory you want to monitor. Then run:
```
python monitor.py
```

## Note
The file-watching mechanism in `monitor.py` is not efficient for handling a large number of files. Consider using the `watchdog` library for better performance:
```
pip install watchdog
```
Then, update `monitor.py` to use `watchdog` for more scalable file monitoring.

## License
This project is licensed under the MIT License.

