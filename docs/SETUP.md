# Setup and Installation Guide

Follow these steps to configure, install dependencies, and run the AI Interview Preparation Assistant locally.

## Prerequisites
* Python 3.10 or higher
* Pip (Python package installer)
* Git

---

## 🚀 Step 1: Clone the Repository
Clone the project folder and navigate to the directory:
```bash
git clone <repository-url>
cd ai-interview-preparation-assistant
```

---

## 🐍 Step 2: Set Up Virtual Environment

### On Mac / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

---

## 📦 Step 3: Install Dependencies
Install all package packages in the activated environment:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Step 4: Environment Configurations
Create a copy of `.env.example` as `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in the values:
* **`GEMINI_API_KEY`**: Obtain your API Key from [Google AI Studio](https://aistudio.google.com/).
* **`SECRET_KEY`**: Provide a random secret hash string for secure JWT token encryption.
* **`DATABASE_URL`**: Keep default `sqlite:///./interview_assistant.db` for local SQLite storage.

---

## ▶️ Step 5: Run the FastAPI Backend
Start the FastAPI server utilizing `uvicorn`:
```bash
cd backend
python main.py
```
The API server will launch at `http://localhost:8000`. You can inspect interactive OpenAPI docs at `http://localhost:8000/docs`.

---

## 🎨 Step 6: Run the Streamlit Frontend
In a new terminal window (with the virtual environment activated), start Streamlit:
```bash
cd frontend
streamlit run app.py
```
The frontend UI will automatically open in your default browser at `http://localhost:8501`.

---

## 🧪 Step 7: Run Unit Tests
To verify implementation logic with `pytest`, run:
```bash
pytest tests/ -v
```
This will create a temporary test database, execute all tests, and clean up test artifacts on completion.
