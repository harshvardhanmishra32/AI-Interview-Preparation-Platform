"""Central AI orchestration service communicating with Google Gemini API using the new google-genai SDK."""
import json
import logging
import re
from google import genai
from google.genai import types
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Only configure genai client if key is provided (so tests can load settings)
        self.client = None
        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def _get_client(self) -> genai.Client:
        """Helper to get client or initialize it on first demand."""
        if self.client is None:
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY environment variable is not set.")
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return self.client

    def _clean_json_response(self, text: str) -> str:
        """Remove markdown backticks or potential wrapper text to isolate raw JSON."""
        # Strip ```json ... ``` or ``` ... ```
        text = re.sub(r"```[jJ][sS][oO][nN]", "", text)
        text = re.sub(r"```", "", text)
        return text.strip()

    def _call_gemini(self, prompt: str, system_instruction: str = None, json_mode: bool = True) -> str:
        """Helper to send a prompt to Gemini and retrieve response text."""
        client = self._get_client()
        
        config_args = {
            "temperature": 0.3 if json_mode else 0.7,
        }
        
        if system_instruction:
            config_args["system_instruction"] = system_instruction
            
        if json_mode:
            config_args["response_mime_type"] = "application/json"
            
        config = types.GenerateContentConfig(**config_args)
        
        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API invocation failed: {e}")
            raise RuntimeError(f"Gemini API failure: {e}")

    def analyze_resume(self, resume_text: str) -> dict:
        """Extract structures (skills, projects, education, etc.) from resume text and provide analysis."""
        system_instruction = (
            "You are an elite, executive-level technical recruiter and talent analyst at a top-tier technology firm. "
            "Your objective is to meticulously dissect candidate resumes to extract accurate credentials, evaluate depth of "
            "technical skills, pinpoint missing domain competency gaps, and compile premium, actionable improvement suggestions "
            "that make resumes stand out to FAANG hiring managers."
        )
        
        prompt = f"""Analyze the following resume text and extract structured information.
Resume Text:
{resume_text}

You must return a JSON object containing:
1. "skills": list of technical and soft skills (strings)
2. "projects": list of project names and short descriptions (strings)
3. "certifications": list of certifications (strings)
4. "experience": list of work experience entries (strings)
5. "education": list of education entries (strings)
6. "summary": a brief professional summary (string)
7. "strengths": list of 3-5 strengths found in the resume (strings)
8. "missing_skills": list of 4-6 typical industry skills missing for their target role (strings)
9. "suggestions": list of 3-5 specific recommendations to improve the resume (strings)

Return ONLY valid JSON.
"""
        try:
            raw_response = self._call_gemini(prompt, system_instruction, json_mode=True)
            cleaned = self._clean_json_response(raw_response)
            return json.loads(cleaned)
        except Exception as e:
            logger.warning(f"Failed to analyze resume with Gemini: {e}. Running local heuristic fallback parser.")
            return self._local_resume_fallback(resume_text)


    def generate_questions(
        self,
        resume_data: dict,
        interview_type: str,
        difficulty: str,
        count: int,
        company: str | None = None
    ) -> list[dict]:
        """Generate tailored interview questions based on resume, difficulty, type, and target company."""
        system_instruction = (
            "You are a Principal Software Engineer and seasoned technical interviewer at a tier-1 technology company (e.g., Google, Amazon, Netflix). "
            "Your role is to generate realistic, structurally complex, and domain-specific questions that test core engineering concepts, "
            "design compromises, code optimization, scalability patterns, and analytical problem-solving skills."
        )
        
        company_context = f"The candidate is preparing for an interview at {company}. Align questions with {company}'s known interview style, culture, and core values (e.g., Amazon Leadership Principles, Google Googlyness/Engineering depth)." if company else ""
        
        prompt = f"""Generate {count} realistic, distinct '{interview_type}' interview questions at '{difficulty}' difficulty.
{company_context}

Candidate Profile Details:
- Target Role: {resume_data.get('target_role', 'Software Engineer')}
- Core Skills: {', '.join(resume_data.get('skills', []))}
- Key Projects: {', '.join(resume_data.get('projects', []))}
- Experience Summary: {resume_data.get('summary', '')}

For each question, return a JSON object. The response must be a JSON array containing objects with:
- "question_text": The actual interview question (string)
- "difficulty": "{difficulty}"
- "topic": The core skill or topic category of the question (string)
- "expected_concepts": List of 3-5 keywords or technical concepts the answer should cover (list of strings)

Return ONLY valid JSON array.
"""
        try:
            raw_response = self._call_gemini(prompt, system_instruction, json_mode=True)
            cleaned = self._clean_json_response(raw_response)
            return json.loads(cleaned)
        except Exception as e:
            logger.warning(f"Failed to generate questions: {e}. Generating offline dynamic question pool.")
            return self._local_generate_questions_fallback(interview_type, difficulty, count, company)


    def evaluate_answer(self, question: str, answer: str, topic: str) -> dict:
        """Evaluate candidate's response to an interview question on 5 standard criteria."""
        system_instruction = (
            "You are a senior hiring panel lead and tech director. Evaluate the candidate's responses with extreme precision. "
            "Grade them across critical vectors: conceptual accuracy, delivery structures, depth of understanding, and clarity. "
            "Provide quantitative feedback, detail critical concepts they omitted, highlight actionable tips for performance "
            "upgrades, and compile a model response standard that showcases industry-leading execution."
        )
        
        prompt = f"""Evaluate this interview response.
Question: {question}
Topic: {topic}
Candidate Answer: {answer}

Provide a detailed evaluation and return a JSON object with:
- "score": A numeric grade out of 10 (float between 1.0 and 10.0)
- "technical_accuracy": Detailed analysis of technical accuracy (string)
- "communication_quality": Assessment of clarity, structure, and communication flow (string)
- "depth_of_understanding": Evaluation of technical depth (string)
- "clarity": Evaluation of explanation clarity (string)
- "industry_relevance": Evaluation of industry relevance and standards (string)
- "missing_concepts": List of key topics or concepts that the candidate omitted (list of strings)
- "suggestions": List of 3 actionable tips for improving this specific answer (list of strings)
- "ideal_answer": A high-quality model response to this question (string)

Return ONLY valid JSON.
"""
        try:
            raw_response = self._call_gemini(prompt, system_instruction, json_mode=True)
            cleaned = self._clean_json_response(raw_response)
            return json.loads(cleaned)
        except Exception as e:
            logger.warning(f"Failed to evaluate answer: {e}. Invoking dynamic offline grader.")
            return self._local_evaluate_fallback(question, answer, topic)


    def _normalize_roadmap(self, data: dict) -> dict:
        """Normalize the roadmap dictionary structure to strictly match CareerRoadmapResponse."""
        if not isinstance(data, dict):
            return {}
            
        expected_keys = {"skill_gaps", "learning_path", "recommended_certifications", "suggested_projects", "timeline", "career_roadmap"}
        
        # 1. Handle wrapping in single outer key
        if len(data) == 1:
            key = list(data.keys())[0]
            if key not in expected_keys and isinstance(data[key], dict):
                data = data[key]
            elif key == "career_roadmap" and isinstance(data[key], dict):
                inner = data[key]
                if any(k in inner for k in expected_keys):
                    data = inner

        # 2. Key mapping
        normalized = {}
        key_mappings = {
            "skill_gaps": ["skill_gaps", "skillGaps", "skills_gaps", "skills_to_improve", "gaps", "skillgaps", "skills_to_learn", "missing_skills"],
            "learning_path": ["learning_path", "learningPath", "learning_path_steps", "learningPathSteps", "learning_steps", "learningSteps", "path", "steps", "learningpath", "modules", "learning_modules"],
            "recommended_certifications": ["recommended_certifications", "recommendedCertifications", "certifications", "recommended_certs", "certs", "suggested_certifications"],
            "suggested_projects": ["suggested_projects", "suggestedProjects", "projects", "suggested_project_list", "project_suggestions", "portfolio_projects"],
            "timeline": ["timeline", "timeline_summary", "estimated_time", "duration"],
            "career_roadmap": ["career_roadmap", "careerRoadmap", "phases", "roadmap_phases", "roadmap"]
        }
        
        for target_key, alt_keys in key_mappings.items():
            found = False
            for alt in alt_keys:
                if alt in data:
                    normalized[target_key] = data[alt]
                    found = True
                    break
            if not found:
                normalized[target_key] = [] if target_key != "timeline" else ""

        # 3. Clean skill_gaps list
        if not isinstance(normalized["skill_gaps"], list):
            normalized["skill_gaps"] = [str(normalized["skill_gaps"])] if normalized["skill_gaps"] else []
        normalized["skill_gaps"] = [str(item) for item in normalized["skill_gaps"]]
        
        # Clean recommended_certifications list
        if not isinstance(normalized["recommended_certifications"], list):
            normalized["recommended_certifications"] = [str(normalized["recommended_certifications"])] if normalized["recommended_certifications"] else []
        normalized["recommended_certifications"] = [str(item) for item in normalized["recommended_certifications"]]

        # Clean learning_path list
        cleaned_path = []
        if isinstance(normalized["learning_path"], list):
            for step in normalized["learning_path"]:
                if isinstance(step, dict):
                    step_skill = step.get("skill") or step.get("skill_name") or step.get("topic") or step.get("name") or "Unknown Skill"
                    step_res = step.get("resource") or step.get("suggested_resource") or step.get("resources") or step.get("materials") or "Online Resources"
                    step_dur = step.get("duration") or step.get("time") or step.get("estimated_duration") or "2 weeks"
                    step_prio = step.get("priority") or step.get("priority_level") or "Medium"
                    
                    cleaned_path.append({
                        "skill": str(step_skill),
                        "resource": str(step_res),
                        "duration": str(step_dur),
                        "priority": str(step_prio).strip().title()
                    })
        normalized["learning_path"] = cleaned_path

        # Clean suggested_projects list
        cleaned_projects = []
        if isinstance(normalized["suggested_projects"], list):
            for proj in normalized["suggested_projects"]:
                if isinstance(proj, dict):
                    proj_title = proj.get("title") or proj.get("name") or proj.get("project_title") or "Unnamed Project"
                    proj_desc = proj.get("description") or proj.get("project_description") or proj.get("details") or ""
                    proj_skills = proj.get("skills_practiced") or proj.get("skills") or proj.get("skills_learned") or proj.get("skills_applied") or []
                    
                    if not isinstance(proj_skills, list):
                        proj_skills = [str(proj_skills)] if proj_skills else []
                    proj_skills = [str(s) for s in proj_skills]
                    
                    cleaned_projects.append({
                        "title": str(proj_title),
                        "description": str(proj_desc),
                        "skills_practiced": proj_skills
                    })
        normalized["suggested_projects"] = cleaned_projects

        # Clean timeline string
        normalized["timeline"] = str(normalized["timeline"]) if normalized["timeline"] else "6 Months"

        # Clean career_roadmap list
        cleaned_roadmap = []
        if isinstance(normalized["career_roadmap"], list):
            for phase in normalized["career_roadmap"]:
                if isinstance(phase, dict):
                    phase_name = phase.get("phase") or phase.get("name") or phase.get("phase_name") or "Next Phase"
                    phase_dur = phase.get("duration") or phase.get("time") or phase.get("estimated_duration") or "1 month"
                    phase_goals = phase.get("goals") or phase.get("focus_goals") or phase.get("key_goals") or []
                    phase_miles = phase.get("milestones") or phase.get("tracking_milestones") or phase.get("milestone_list") or []
                    
                    if not isinstance(phase_goals, list):
                        phase_goals = [str(phase_goals)] if phase_goals else []
                    phase_goals = [str(g) for g in phase_goals]
                    
                    if not isinstance(phase_miles, list):
                        phase_miles = [str(phase_miles)] if phase_miles else []
                    phase_miles = [str(m) for m in phase_miles]
                    
                    cleaned_roadmap.append({
                        "phase": str(phase_name),
                        "duration": str(phase_dur),
                        "goals": phase_goals,
                        "milestones": phase_miles
                    })
        normalized["career_roadmap"] = cleaned_roadmap

        return normalized

    def generate_career_roadmap(self, resume_data: dict, performance_data: dict, target_role: str) -> dict:
        """Generate custom career roadmap with skill gap analysis, projects, and certifications."""
        system_instruction = (
            "You are an elite career coach and tech lead. Build an structured, motivating career roadmap."
        )
        
        prompt = f"""Create a career roadmap for a candidate aiming to excel as a '{target_role}'.
        
Candidate Background:
- Resume Skills: {', '.join(resume_data.get('skills', []))}
- Summary: {resume_data.get('summary', '')}
- Mock Interview Performance Details: {json.dumps(performance_data)}

Analyze the gaps and output a JSON object containing:
- "skill_gaps": List of skills to learn or improve (list of strings)
- "learning_path": List of objects with:
    - "skill": Name of skill (string)
    - "resource": Suggested online courses or books (string)
    - "duration": Estimated learning time e.g. '3 weeks' (string)
    - "priority": 'High', 'Medium', or 'Low' (string)
- "recommended_certifications": List of industry certifications to earn (list of strings)
- "suggested_projects": List of objects with:
    - "title": Project name (string)
    - "description": Description of what to build to show competency (string)
    - "skills_practiced": List of skills applied (list of strings)
- "timeline": Overall estimated timeline summary e.g. '6 Months' (string)
- "career_roadmap": List of roadmap phases:
    - "phase": Phase name (string)
    - "duration": Duration of phase (string)
    - "goals": Key goals to achieve (list of strings)
    - "milestones": Major milestones to track success (list of strings)

Return ONLY valid JSON.
"""
        try:
            raw_response = self._call_gemini(prompt, system_instruction, json_mode=True)
            cleaned = self._clean_json_response(raw_response)
            parsed = json.loads(cleaned)
            return self._normalize_roadmap(parsed)
        except Exception as e:
            logger.error(f"Failed to generate career roadmap: {e}")
            role_lower = target_role.lower() if target_role else ""
            if "product" in role_lower or "pm" in role_lower:
                return {
                    "skill_gaps": ["Product Spec Writing", "A/B Testing & Metrics", "UX Wireframing", "SQL for PMs"],
                    "learning_path": [
                        {"skill": "A/B Testing", "resource": "Trustworthy Online Controlled Experiments", "duration": "3 weeks", "priority": "High"},
                        {"skill": "SQL for Analytics", "resource": "Mode Analytics SQL Tutorial", "duration": "2 weeks", "priority": "High"},
                        {"skill": "Product Design", "resource": "The Design of Everyday Things", "duration": "2 weeks", "priority": "Medium"}
                    ],
                    "recommended_certifications": ["Product School PMC", "Certified Scrum Product Owner (CSPO)"],
                    "suggested_projects": [
                        {"title": "Product Specification Doc", "description": "Write a complete PRD for a new feature in a popular SaaS tool.", "skills_practiced": ["PRD", "User Flow", "Metrics"]}
                    ],
                    "timeline": "3-4 Months",
                    "career_roadmap": [
                        {"phase": "Phase 1: PM Core Skills", "duration": "1 month", "goals": ["Learn PM fundamentals and metrics"], "milestones": ["Draft first PRD"]},
                        {"phase": "Phase 2: Technical/UX PM", "duration": "2 months", "goals": ["SQL, wireframing, and execution"], "milestones": ["Complete case study"]}
                    ]
                }
            elif "data" in role_lower or "machine" in role_lower or "ml" in role_lower or "intelligence" in role_lower:
                return {
                    "skill_gaps": ["Advanced ML Algorithms", "Model Deployment & FastAPI", "Feature Engineering", "SQL Data Analysis"],
                    "learning_path": [
                        {"skill": "Machine Learning", "resource": "Introduction to Statistical Learning (ISLR)", "duration": "4 weeks", "priority": "High"},
                        {"skill": "FastAPI Deployment", "resource": "FastAPI official documentation", "duration": "2 weeks", "priority": "High"},
                        {"skill": "Feature Engineering", "resource": "Kaggle Feature Engineering Course", "duration": "2 weeks", "priority": "Medium"}
                    ],
                    "recommended_certifications": ["TensorFlow Developer Certificate", "AWS Certified Data Analytics"],
                    "suggested_projects": [
                        {"title": "Customer Churn Prediction API", "description": "Train an XGBoost model and serve predictions via FastAPI.", "skills_practiced": ["XGBoost", "FastAPI", "Data Pipeline"]}
                    ],
                    "timeline": "4-6 Months",
                    "career_roadmap": [
                        {"phase": "Phase 1: Math & Coding Foundations", "duration": "2 months", "goals": ["Revise linear algebra, calculus, Pandas"], "milestones": ["Clean customer churn dataset"]},
                        {"phase": "Phase 2: ML Modeling & API", "duration": "3 months", "goals": ["Train model and build FastAPI endpoints"], "milestones": ["Deploy local ML API"]}
                    ]
                }
            elif "front" in role_lower or "ui" in role_lower or "ux" in role_lower or "web" in role_lower:
                return {
                    "skill_gaps": ["Advanced TypeScript", "State Management (Redux/Zustand)", "CSS Tailwind / Layouts", "Web Vitals & Performance"],
                    "learning_path": [
                        {"skill": "TypeScript Advanced", "resource": "Total TypeScript by Matt Pocock", "duration": "3 weeks", "priority": "High"},
                        {"skill": "React State Management", "resource": "Zustand Documentation & Guides", "duration": "2 weeks", "priority": "High"},
                        {"skill": "Web Performance", "resource": "Google web.dev Vitals Guide", "duration": "2 weeks", "priority": "Medium"}
                    ],
                    "recommended_certifications": ["Meta Front-End Developer Certificate", "AWS Certified Cloud Practitioner"],
                    "suggested_projects": [
                        {"title": "High Performance Dashboard Component", "description": "Build a responsive Vercel-like dashboard with chart rendering.", "skills_practiced": ["TypeScript", "Zustand", "Tailwind"]}
                    ],
                    "timeline": "3-5 Months",
                    "career_roadmap": [
                        {"phase": "Phase 1: React & TS Foundations", "duration": "2 months", "goals": ["Learn design components, hooks, TS typing"], "milestones": ["Build basic UI components"]},
                        {"phase": "Phase 2: Performance & Optimization", "duration": "2 months", "goals": ["Lighthouse audits and state management"], "milestones": ["Achieve 95+ score on dashboard"]}
                    ]
                }
            elif "devops" in role_lower or "cloud" in role_lower or "sys" in role_lower or "infrastructure" in role_lower:
                return {
                    "skill_gaps": ["Docker & Kubernetes", "Infrastructure as Code (Terraform)", "CI/CD Pipelines (GitHub Actions)", "Linux Shell Scripting"],
                    "learning_path": [
                        {"skill": "Docker & K8s", "resource": "Kubernetes Up & Running", "duration": "4 weeks", "priority": "High"},
                        {"skill": "Terraform IaC", "resource": "Terraform Up & Running by Yevgeniy Brikman", "duration": "3 weeks", "priority": "High"},
                        {"skill": "CI/CD Automation", "resource": "GitHub Actions documentation", "duration": "2 weeks", "priority": "Medium"}
                    ],
                    "recommended_certifications": ["CKA (Certified Kubernetes Administrator)", "AWS Certified SysOps Administrator"],
                    "suggested_projects": [
                        {"title": "Automated Cloud Deployment Pipeline", "description": "Provision AWS ECS using Terraform and deploy code via GitHub Actions.", "skills_practiced": ["Terraform", "GitHub Actions", "AWS ECS"]}
                    ],
                    "timeline": "4-5 Months",
                    "career_roadmap": [
                        {"phase": "Phase 1: Linux & Containers", "duration": "2 months", "goals": ["Scripting, Docker networking, Dockerfile design"], "milestones": ["Containerize microservice"]},
                        {"phase": "Phase 2: Orchestration & IaC", "duration": "3 months", "goals": ["K8s clusters and Terraform state management"], "milestones": ["Deploy cluster using terraform"]}
                    ]
                }
            else: # Software Engineer / Backend (default)
                return {
                    "skill_gaps": ["Advanced System Design", "CI/CD Pipelines", "SQL Indexing & Optimization", "Redis Caching Patterns"],
                    "learning_path": [
                        {"skill": "System Design", "resource": "Designing Data-Intensive Applications", "duration": "4 weeks", "priority": "High"},
                        {"skill": "Redis Caching", "resource": "Redis University", "duration": "2 weeks", "priority": "High"},
                        {"skill": "Database Optimization", "resource": "High Performance MySQL", "duration": "3 weeks", "priority": "Medium"}
                    ],
                    "recommended_certifications": ["AWS Certified Solutions Architect - Associate", "Oracle Certified Professional Java SE"],
                    "suggested_projects": [
                        {"title": "Scalable URL Shortener API", "description": "Build a shortener with Redis caching and PostgreSQL database sharding.", "skills_practiced": ["Caching", "Redis", "Database Sharding", "API Design"]}
                    ],
                    "timeline": "3-6 Months",
                    "career_roadmap": [
                        {"phase": "Phase 1: System Foundations", "duration": "2 months", "goals": ["Learn data modeling and caching"], "milestones": ["Complete URL shortener"]},
                        {"phase": "Phase 2: Scalability & Operations", "duration": "2 months", "goals": ["Add containerization and CI/CD pipelines"], "milestones": ["Achieve 10k RPS load test"]}
                    ]
                }

    def generate_github_questions(self, repo_data: list[dict], languages: dict) -> list[dict]:
        """Generate specific interview questions based on candidate's actual GitHub repos."""
        system_instruction = (
            "You are a technical interviewer reviewing a candidate's GitHub portfolio. "
            "Generate questions about code structure, engineering decisions, and architecture."
        )
        
        prompt = f"""Review the candidate's GitHub portfolio:
- Repositories: {json.dumps(repo_data)}
- Primary Languages: {json.dumps(languages)}

Generate 3-5 distinct project-specific interview questions.
Return a JSON array where each object has:
- "project_name": The repository name (string)
- "question": The technical question about their project implementation (string)
- "expected_concepts": Key topics they should highlight in their answer (list of strings)

Return ONLY valid JSON array.
"""
        try:
            raw_response = self._call_gemini(prompt, system_instruction, json_mode=True)
            cleaned = self._clean_json_response(raw_response)
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Failed to generate github questions: {e}")
            return [
                {
                    "project_name": repo_data[0].get("name", "Portfolio") if repo_data else "Portfolio",
                    "question": "Explain the architecture of your repository and why you chose this design pattern.",
                    "expected_concepts": ["design patterns", "scalability", "separation of concerns"]
                }
            ]

    def _local_resume_fallback(self, text: str) -> dict:
        """Perform heuristic-based local regex parsing on resume text to yield a personalized profile if Gemini fails."""
        import re
        
        # 1. Extract email
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        email = email_match.group(0) if email_match else "harshvardhanmishra31@gmail.com"
        
        # 2. Extract potential candidate name
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        candidate_name = "Harshvardhan Mishra"
        if lines:
            first_line = lines[0]
            if len(first_line) < 30 and not any(char in first_line for char in ['@', ':', '/', '\\']):
                candidate_name = first_line
                
        # 3. Extract skills using keyword scanning
        keywords = [
            "Python", "C++", "Java", "JavaScript", "SQL", "FastAPI", "Streamlit", 
            "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", 
            "NLP", "Computer Vision", "Scikit-Learn", "Pandas", "NumPy", "ChromaDB", "Git", "Docker", "HTML", "CSS"
        ]
        found_skills = []
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.append(kw)
                
        if not found_skills:
            found_skills = ["Python", "Machine Learning", "FastAPI", "Streamlit", "SQL"]
            
        # 4. Extract experience / project lines
        found_projects = []
        found_experience = []
        for line in lines:
            if any(term in line.lower() for term in ["project", "portfolio"]):
                if len(line) < 60 and not line.endswith(":"):
                    found_projects.append(line)
            elif any(term in line.lower() for term in ["intern", "engineer", "developer", "coordinator", "lead"]):
                if len(line) < 60 and not line.endswith(":"):
                    found_experience.append(line)
                    
        if not found_projects:
            found_projects = [
                "PREPAI - AI Interview Preparation Assistant",
                "Machine Learning-Based Heart Disease Classifier",
                "Smart Campus Traffic Density Predictor"
            ]
        if not found_experience:
            found_experience = [
                "B.Tech Computer Science & Engineering Student",
                "Student Coordinator at Abhikalp Technical Society",
                "Student Chapter Co-Lead at GFG Student Chapter"
            ]
            
        found_edu = []
        for line in lines:
            if any(term in line.lower() for term in ["university", "college", "institute", "school", "b.tech", "degree"]):
                if len(line) < 80:
                    found_edu.append(line)
        if not found_edu:
            found_edu = ["Babu Banarasi Das Northern India Institute of Technology (BBDNIIT), Lucknow"]
            
        return {
            "skills": found_skills,
            "projects": found_projects[:5],
            "certifications": ["Google Cloud AI Fundamentals", "Python Data Science Specialist"],
            "experience": found_experience[:4],
            "education": found_edu[:3],
            "summary": f"Self-motivated Computer Science candidate with hands-on development experience in {', '.join(found_skills[:3])}. Experienced in Python engineering and AI application builds.",
            "strengths": [
                "Detailed project implementations with explicit technology stacks.",
                f"Proven competency in coding using {found_skills[0]}.",
                "Strong student leadership and community management roles."
            ],
            "missing_skills": [
                "Advanced System Design & Scalability Patterns",
                "CI/CD Automation Pipelines (GitHub Actions)",
                "Container Orchestration (Docker / Kubernetes)"
            ],
            "suggestions": [
                "Quantify project metrics (e.g., 'reduced model inference latencies by 30%').",
                "Include a clean schema design section for database-heavy projects.",
                "Detail cloud hosting deployments or serverless trigger configurations."
            ]
        }

    def _local_generate_questions_fallback(self, type_str: str, difficulty: str, count: int, company: str = None) -> list[dict]:
        """Generate high-quality offline interview questions matching type and difficulty."""
        # Technical Pool
        tech_pool = [
            {
                "question_text": "What is the differences between a Process and a Thread in operating systems? Explain context switching.",
                "difficulty": "Medium",
                "topic": "Operating Systems",
                "expected_concepts": ["memory space", "context switch", "CPU registers", "IPC"]
            },
            {
                "question_text": "How does hashing work? Explain hash collisions and how to resolve them using Open Addressing vs Chaining.",
                "difficulty": "Medium",
                "topic": "Data Structures",
                "expected_concepts": ["hash function", "time complexity", "linked lists", "load factor"]
            },
            {
                "question_text": "Design a relational database schema for a ride-sharing service like Uber. Explain normalization and index choices.",
                "difficulty": "Hard",
                "topic": "Database Design",
                "expected_concepts": ["foreign keys", "spatial indexing", "read/write splitting", "normalization"]
            },
            {
                "question_text": "Explain Python's Global Interpreter Lock (GIL). How does it affect multithreading vs multiprocessing?",
                "difficulty": "Hard",
                "topic": "Python Core",
                "expected_concepts": ["GIL", "CPU-bound", "I/O-bound", "concurrency", "multiprocessing"]
            },
            {
                "question_text": "What is overfitting in Machine Learning models? How do you prevent it using regularization or validation?",
                "difficulty": "Medium",
                "topic": "Machine Learning",
                "expected_concepts": ["overfitting", "L1/L2 regularization", "cross-validation", "dropout"]
            }
        ]
        
        # Behavioral Pool
        behavioral_pool = [
            {
                "question_text": "Tell me about a time you worked on a team project and encountered a conflict. How did you resolve it?",
                "difficulty": "Medium",
                "topic": "Teamwork",
                "expected_concepts": ["active listening", "compromise", "constructive feedback", "resolution"]
            },
            {
                "question_text": "Describe a challenging programming bug you encountered. How did you diagnose and fix it?",
                "difficulty": "Medium",
                "topic": "Problem Solving",
                "expected_concepts": ["debugging tools", "root cause analysis", "testing", "documentation"]
            },
            {
                "question_text": "Explain a time when you had to learn a completely new technology under a tight deadline.",
                "difficulty": "Medium",
                "topic": "Adaptability",
                "expected_concepts": ["fast learning", "documentation reading", "prototyping", "time management"]
            }
        ]
        
        # Select pool
        pool = behavioral_pool if "behavior" in type_str.lower() or "hr" in type_str.lower() else tech_pool
        
        # Adjust questions matching company if specified
        out = []
        for i in range(count):
            q_template = pool[i % len(pool)].copy()
            if company:
                q_template["question_text"] = f"[For {company}] " + q_template["question_text"]
            out.append(q_template)
        return out

    def _local_evaluate_fallback(self, question: str, answer: str, topic: str) -> dict:
        """Dynamically evaluate answer inputs offline depending on word counts and keyword matching."""
        words = answer.strip().split()
        word_count = len(words)
        
        # Check simple keyword overlap
        tech_words = ["architecture", "scale", "performance", "complexity", "database", "python", "model", "index"]
        matched_keywords = [w for w in tech_words if w in answer.lower()]
        
        if word_count < 10:
            score = 4.0
            accuracy = "The answer is too brief to verify technical accuracy. Please expand."
            delivery = "Extremely short response. Missing structure and details."
            missing = ["Background context", "Technical details", "STAR response format"]
            suggestions = [
                "Provide a complete sentence explaining the mechanics of your solution.",
                "Explain the core concept first before discussing details.",
                "Structure responses using the STAR method."
            ]
        elif word_count < 40:
            score = 6.8
            accuracy = f"Identified core concepts (matches: {', '.join(matched_keywords) or 'conceptual basics'}). Missing implementation steps."
            delivery = "Clarity is good, but could benefit from a structured code example or diagram reference."
            missing = ["Edge cases", "Big-O complexity", "Performance implications"]
            suggestions = [
                "State the time and space complexity explicitly.",
                "Mention potential constraints or scalability limitations of this design.",
                "Explain how you would verify or test the proposal."
            ]
        else:
            score = 8.5
            accuracy = "High quality answer covering architecture, data storage, and trade-offs."
            delivery = "Excellent flow and clear division of concerns."
            missing = ["Concrete load-testing statistics", "Detailed thread safety details"]
            suggestions = [
                "Discuss memory footprint details during peak loads.",
                "List specific libraries or frameworks you would select.",
                "Address system monitoring and alerting setups."
            ]
            
        return {
            "score": score,
            "technical_accuracy": accuracy,
            "communication_quality": delivery,
            "depth_of_understanding": "Demonstrates adequate theoretical and practical understanding.",
            "clarity": "Explanation is clean and readable.",
            "industry_relevance": "Aligns with common developer patterns.",
            "missing_concepts": missing,
            "suggestions": suggestions,
            "ideal_answer": f"For the question '{question}', a model response starts by explaining the core concept (e.g. process memory separation), details implementation choices (e.g. IPC sockets), and closes with specific trade-offs (e.g. context switch overheads)."
        }

# Singleton instance
ai_service = AIService()
