# Music Controller 
*A collaborative music room application with Spotify integration*

## Table of Contents  
- [Overview](#overview)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  
- [Usage](#usage)  

---

## Overview  
Music Controller is a web application that allows users to create and join music rooms where they can collaboratively control the playback of songs. The host can play or pause the music, and guests can vote to skip songs. The application integrates with **Spotify's Web API** for seamless music streaming and playback control.

## Features  
✅ **Create and Join Rooms** – Users can create rooms with custom settings or join existing ones.  
✅ **Collaborative Playback Control** – Guests can vote to skip songs, and the host can play/pause the music.  
✅ **Spotify Integration** – Fetches and controls music playback using Spotify’s API.  
✅ **Real-time Updates** – Ensures all participants see changes instantly.  

## Tech Stack  
- **Backend:** Django, Django REST Framework  
- **Frontend:** React  
- **Authentication:** Spotify OAuth 2.0  

## Installation  

### Backend Setup (Django)  
1. Clone the repository:  
   ```sh
   git clone https://github.com/your-username/music-controller.git
   cd music-controller
   ```
2. Set up a virtual environment:  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```
4. Run migrations and start the server:  
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend Setup (React)  
1. Navigate to the frontend directory:  
   ```sh
   cd frontend
   ```
2. Install dependencies:  
   ```sh
   npm install
   ```
3. Start the React development server:  
   ```sh
   npm run dev
   ```

## Usage  
1. Open `http://localhost:8000` in your browser.  
2. Authenticate with your Spotify account.  
3. Create a music room or join an existing one.  
4. Control playback collaboratively with others in the room.  
