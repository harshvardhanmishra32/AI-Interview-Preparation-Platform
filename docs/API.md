# PREPAI Backend API Documentation

All request payloads and response bodies utilize standard JSON encoding unless specified.

## Base URL
`http://localhost:8000/api`

## Authentication
Protected endpoints require a JWT bearer token passed inside the `Authorization` header:
`Authorization: Bearer <your-access-token>`

---

## 🔑 Authentication Endpoints

### 1. Register Account
* **Method:** `POST`
* **Path:** `/auth/register`
* **Auth Required:** No
* **Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "education": "B.Tech Computer Science",
  "target_role": "Software Engineer"
}
```
* **Success Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "education": "B.Tech Computer Science",
  "target_role": "Software Engineer",
  "created_at": "2026-06-23T10:00:00Z"
}
```

### 2. User Login
* **Method:** `POST`
* **Path:** `/auth/login`
* **Auth Required:** No
* **Request Body (Form URL-Encoded):**
  * `username`: Candidate Email (e.g. `john@example.com`)
  * `password`: Password string
* **Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer"
}
```

---

## 📄 Resume Endpoints

### 1. Upload PDF Resume
* **Method:** `POST`
* **Path:** `/resume/upload-resume`
* **Auth Required:** Yes
* **Request Body:** Multipart Form Data with a `file` field containing the PDF resume.
* **Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "skills": ["Python", "FastAPI", "Docker", "SQL"],
  "projects": ["Web Chat App using Websockets"],
  "certifications": ["AWS Solutions Architect"],
  "experience": ["Software Intern at TechCorp"],
  "education_details": ["B.S. in Computer Science"],
  "summary": "Motivated software engineer...",
  "strengths": ["Strong coding fundamentals", "Hands-on projects"],
  "missing_skills": ["Kubernetes", "CI/CD Pipelines"],
  "suggestions": ["Include metrics in your project descriptions."],
  "uploaded_at": "2026-06-23T10:05:00Z"
}
```

---

## 🎯 Mock Interview Endpoints

### 1. Generate Interview Questions
* **Method:** `POST`
* **Path:** `/interview/generate-questions`
* **Auth Required:** Yes
* **Request Body:**
```json
{
  "interview_type": "technical",
  "difficulty": "medium",
  "question_count": 5,
  "company": "Google"
}
```
* **Success Response (200 OK):**
```json
{
  "id": 1,
  "company": "Google",
  "role": "Software Engineer",
  "interview_type": "technical",
  "difficulty": "medium",
  "status": "in_progress",
  "created_at": "2026-06-23T10:10:00Z",
  "questions": [
    {
      "id": 1,
      "question_text": "Explain how hashing works in hash maps and how collisions are resolved.",
      "difficulty": "medium",
      "topic": "Data Structures",
      "expected_concepts": ["hash function", "hash table", "chaining", "open addressing"]
    }
  ]
}
```

---

## 📊 Analytics Endpoints

### 1. Retrieve Dashboard Summary
* **Method:** `GET`
* **Path:** `/analytics/dashboard`
* **Auth Required:** Yes
* **Success Response (200 OK):**
```json
{
  "total_interviews": 3,
  "average_score": 7.4,
  "strongest_topics": ["Data Structures", "Algorithms"],
  "weakest_topics": ["System Design"],
  "recent_sessions": [
    {
      "id": 1,
      "company": "Google",
      "role": "Software Engineer",
      "interview_type": "technical",
      "difficulty": "medium",
      "created_at": "2026-06-23 10:10",
      "question_count": 5,
      "completed_count": 5,
      "average_score": 7.8
    }
  ],
  "score_trend": [
    {
      "date": "2026-06-23",
      "average_score": 7.8
    }
  ]
}
```
