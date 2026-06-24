"""Service layer for mock interview orchestrations, question generation, and answer submissions."""
from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session
from app.models.interview import InterviewSession, Question, Answer
from app.models.resume import Resume
from app.models.user import User
from app.schemas.interview import QuestionGenerateRequest
from app.services.ai_service import ai_service
from app.services.analytics_service import AnalyticsService

class InterviewService:
    @staticmethod
    def create_session(db: Session, user_id: int, request: QuestionGenerateRequest) -> InterviewSession:
        """Create new interview session, generate questions via Gemini, and store in database."""
        # 1. Fetch user to identify target role
        user = db.query(User).filter(User.id == user_id).first()
        target_role = user.target_role if (user and user.target_role) else "Software Engineer"
        
        # 2. Fetch user resume to feed into prompt context
        resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        
        # Structure resume context or use placeholder
        resume_context = {
            "skills": resume.skills if (resume and resume.skills) else ["Core Engineering", "Problem Solving"],
            "projects": resume.projects if (resume and resume.projects) else ["Classroom Projects"],
            "summary": resume.summary if (resume and resume.summary) else "Candidate seeking roles.",
            "experience": resume.experience if (resume and resume.experience) else [],
            "target_role": target_role
        }
        
        # 3. Generate tailored questions from AI Service
        raw_questions = ai_service.generate_questions(
            resume_data=resume_context,
            interview_type=request.interview_type,
            difficulty=request.difficulty,
            count=request.question_count,
            company=request.company
        )
        
        # 4. Create database records
        session = InterviewSession(
            user_id=user_id,
            company=request.company,
            role=target_role,
            interview_type=request.interview_type,
            difficulty=request.difficulty,
            status="in_progress"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # Add generated questions to database
        for q in raw_questions:
            db_q = Question(
                session_id=session.id,
                question_text=q.get("question_text", "Explain your experience."),
                difficulty=request.difficulty,
                topic=q.get("topic", "General"),
                expected_concepts=q.get("expected_concepts", [])
            )
            db.add(db_q)
            
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_session(db: Session, session_id: int, user_id: int) -> InterviewSession | None:
        """Fetch specific interview session detail for the user."""
        return db.query(InterviewSession).filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == user_id
        ).first()

    @staticmethod
    def get_user_sessions(db: Session, user_id: int) -> list[InterviewSession]:
        """Fetch all interview sessions conducted by the user."""
        return db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id
        ).order_by(InterviewSession.created_at.desc()).all()

    @staticmethod
    def submit_answer(db: Session, user_id: int, question_id: int, answer_text: str) -> Answer:
        """Submit answer, evaluate through Gemini, save details, and update session completion."""
        # 1. Fetch Question details
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise ValueError("Question not found.")
            
        # Verify ownership
        session = db.query(InterviewSession).filter(
            InterviewSession.id == question.session_id,
            InterviewSession.user_id == user_id
        ).first()
        if not session:
            raise ValueError("Unauthorized to submit answer for this session question.")
            
        # Check if already answered
        existing_answer = db.query(Answer).filter(Answer.question_id == question_id).first()
        
        # 2. Check if skipped, otherwise grade answer with Gemini
        if answer_text.strip() == "[Skipped]":
            evaluation = {
                "score": 0.0,
                "technical_accuracy": "Question was skipped by candidate.",
                "communication_quality": "Question was skipped by candidate.",
                "depth_of_understanding": "Question was skipped by candidate.",
                "clarity": "Question was skipped by candidate.",
                "industry_relevance": "Question was skipped by candidate.",
                "missing_concepts": question.expected_concepts or [],
                "suggestions": ["Ensure you attempt all questions to test technical proficiency."],
                "ideal_answer": "Model answer not generated for skipped question."
            }
        else:
            evaluation = ai_service.evaluate_answer(
                question=question.question_text,
                answer=answer_text,
                topic=question.topic
            )
        
        # 3. Save evaluation structure
        if existing_answer:
            db_answer = existing_answer
            db_answer.answer_text = answer_text
            db_answer.score = evaluation.get("score", 5.0)
            db_answer.feedback = json.dumps(evaluation)  # Store full JSON payload inside feedback, or extract
            db_answer.missing_concepts = evaluation.get("missing_concepts", [])
            db_answer.suggestions = evaluation.get("suggestions", [])
            db_answer.ideal_answer = evaluation.get("ideal_answer", "")
            db_answer.evaluated_at = datetime.now(timezone.utc)
        else:
            db_answer = Answer(
                question_id=question_id,
                answer_text=answer_text,
                score=evaluation.get("score", 5.0),
                feedback=json.dumps(evaluation),
                missing_concepts=evaluation.get("missing_concepts", []),
                suggestions=evaluation.get("suggestions", []),
                ideal_answer=evaluation.get("ideal_answer", ""),
                evaluated_at=datetime.now(timezone.utc)
            )
            db.add(db_answer)
            
        db.commit()
        db.refresh(db_answer)
        
        # 4. Check if session completed (if all questions have answers)
        questions = db.query(Question).filter(Question.session_id == session.id).all()
        q_ids = [q.id for q in questions]
        
        answers_count = db.query(Answer).filter(Answer.question_id.in_(q_ids)).count()
        if answers_count >= len(questions):
            session.status = "completed"
            db.commit()
            
        # 5. Recalculate user analytics dashboard metrics asynchronously/inline
        AnalyticsService.update_user_analytics(db, user_id)
        
        return db_answer
