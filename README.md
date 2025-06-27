# Task Prioritization AI App

A web application that leverages Google Vertex AI (Gemini) to intelligently prioritize your tasks based on urgency, importance, effort, and context (like company OKRs). Built with FastAPI for the backend and a simple HTML frontend, and fully containerized with Docker.

---

## Features
- **AI-powered task prioritization** using Google Vertex AI (Gemini)
- **REST API** for programmatic access
- **User-friendly web frontend** for easy task entry and results viewing
- **Dockerized** for easy deployment anywhere

---

## File Overview

- **agent_prioritazion.py**: Main FastAPI backend. Handles API requests, serves the frontend, and communicates with Vertex AI.
- **frontend.html**: Simple HTML/JS frontend for user interaction.
- **requirements.txt**: Python dependencies.
- **Dockerfile**: Containerizes the app for deployment.

---

## Setup Instructions

### 1. Google Cloud Setup
- Enable the **Vertex AI API** in your Google Cloud project.
- Create a **Service Account** with Vertex AI permissions and download the JSON key, or use `gcloud auth application-default login` to generate `application_default_credentials.json`.
- Note the path to your credentials file (e.g., `C:/Users/yourname/AppData/Roaming/gcloud/application_default_credentials.json`).

### 2. Clone the Repository
```bash
# Clone this repo and cd into it
cd /path/to/task_prioritization
```

### 3. Local Development

#### a. Install Python dependencies
```bash
pip install -r requirements.txt
```

#### b. Set Google Credentials
**Windows PowerShell:**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\yourname\AppData\Roaming\gcloud\application_default_credentials.json"
```
**Command Prompt:**
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\yourname\AppData\Roaming\gcloud\application_default_credentials.json
```

#### c. Set Vertex AI Project and Location
Create a `.env` file in the project root with:
```
VERTEX_PROJECT_ID=your-gcp-project-id
VERTEX_LOCATION=us-central1
```

#### d. Run the app
```bash
python agent_prioritazion.py
```

Visit [http://localhost:8000/](http://localhost:8000/) in your browser.

---

### 4. Docker Deployment

#### a. Build the Docker image
```bash
docker build -t task-prioritization-app .
```

#### b. Run the container
```bash
docker run -p 8000:8000 \
  -e VERTEX_PROJECT_ID=your-gcp-project-id \
  -e VERTEX_LOCATION=us-central1 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/application_default_credentials.json \
  -v C:/Users/yourname/AppData/Roaming/gcloud/application_default_credentials.json:/app/application_default_credentials.json \
  task-prioritization-app
```

---

## API Usage Example

**POST /prioritize**
```json
{
  "tasks": [
    "Finish the Q2 sales report by tomorrow",
    "Book a flight for the conference in Austin next month"
  ],
  "context": "Q2 Company OKRs: Launch Project Phoenix, Achieve 15% sales growth"
}
```
**Response:**
```json
{
  "prioritized_tasks": [
    {
      "task_description": "Finish the Q2 sales report by tomorrow",
      "priority_level": "Critical",
      "estimated_effort": "High",
      "reasoning": "Deadline is imminent and it's crucial for company OKRs."
    },
    ...
  ]
}
```

---

## Troubleshooting
- **Authentication errors:** Ensure your `GOOGLE_APPLICATION_CREDENTIALS` env variable is set and the file is accessible in the container or local environment.
- **Vertex AI errors:** Make sure the API is enabled and your service account has the right permissions.
- **Port conflicts:** Change the exposed port in the Dockerfile and run command if 8000 is in use.

---

## Credits
- Built with [FastAPI](https://fastapi.tiangolo.com/), [Google Vertex AI](https://cloud.google.com/vertex-ai), and [Docker](https://www.docker.com/).
- Supported by Google For Developers
- Google Cloud credits are provided for this project
- #VertexAISprint
---
