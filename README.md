# Video Recording and Processing Web Application

## Overview

This is a Django-based web application that allows users to record and process videos through a RESTful API. The application is designed to receive video data in chunks, process it, and make the recorded video available for retrieval. It also extracts and saves the audio from the recorded videos.

## Features

- Start a recording session and generate a unique session ID.
- Receive and store video data chunks sent by the frontend intermittently.
- Handle the final video chunk with a flag indicating the end of the recording.
- Process and save recorded data, including audio extraction.
- Retrieve and serve recorded video data.
- Swagger documentation for the API.

## Getting Started

These instructions will help you set up and run the project on your local development machine.

### Prerequisites

- Python 3.x
- Django
- [Add other prerequisites here]

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/breezeconcept/HNGx_Task5.git

2.  Navigate to the project directory:

    ```bash
    cd HNGx_Task5

3.  Create and activate a virtual environment:

    ```bash
    python -m venv venv

    source venv/bin/activate  # On Windows, use: venv\Scripts\activate

4.  Install project dependencies:

    ```bash
    pip install -r requirements.txt

5.  Run migrations to set up the database:

    ```bash
    python manage.py migrate

6.  Start the Django development server:

    ```bash
    python manage.py runserver

7.  Access the Swagger documentation at http://localhost:8000/swagger/ to explore the API endpoints.


## Usage

### API Endpoints

.   /api/start-recording/: Start a new recording session and generate a unique session ID.

.   /api/receive-video-chunk/: Receive and store video data chunks sent by the frontend intermittently.

.   /api/finalize-recording/: Handle the final video chunk with a flag indicating the end of the recording. Process and save recorded data.

.   /api/get-recorded-data/<str:session_id>/: Retrieve and serve recorded video data for a specific session ID.


## Recording Workflow

1.  Start a recording session by making a POST request to /api/start-recording/. The response will include a session ID.

2.  As the user records, send video data chunks to /api/receive-video-chunk/ intermittently, including the session ID and the video chunk.

3.  To finalize the recording, make a POST request to /api/finalize-recording/ with the last video chunk and set is_final to true.

4.  The recorded data will be processed and saved.
Retrieve the recorded data by making a GET request to /api/get-recorded-data/<session_id>/.


## Configuration

.   You can adjust various settings in the Django project's settings file (settings.py).

.   Customize the storage location for recorded data and extracted audio in the models.py and utils.py files.


## Dependencies

.   Django: Web framework.

.   Django REST framework: Toolkit for building Web APIs.

.   moviepy: Python library for video editing.


## Author

.   Arinze Peter


## License
This project i
s licensed under the MIT License - see the LICENSE.md file for details.