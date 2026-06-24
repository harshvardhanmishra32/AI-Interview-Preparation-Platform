"""Service layer for computing user performance analytics and populating dashboard metrics."""
from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.interview import InterviewSession, Question, Answer
from app.models.analytics import Analytics

class AnalyticsService:
    @staticmethod
    def get_dashboard_data(db: Session, user_id: int) -> dict:
        """Fetch dashboard metrics, recent sessions, and score trends."""
        # 1. Total Completed Interview count
        total_interviews = db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id,
            InterviewSession.status == "completed"
        ).count()
        
        # 2. Average Score across all answered questions
        sessions = db.query(InterviewSession.id).filter(InterviewSession.user_id == user_id).all()
        session_ids = [s[0] for s in sessions]
        
        avg_score = 0.0
        if session_ids:
            questions = db.query(Question.id).filter(Question.session_id.in_(session_ids)).all()
            q_ids = [q[0] for q in questions]
            if q_ids:
                score_query = db.query(func.avg(Answer.score)).filter(Answer.question_id.in_(q_ids)).scalar()
                avg_score = round(score_query, 2) if score_query else 0.0
                
        # 3. Retrieve analytics record for strongest/weakest topics
        analytics_record = db.query(Analytics).filter(Analytics.user_id == user_id).first()
        strongest = analytics_record.strongest_topics if (analytics_record and analytics_record.strongest_topics) else []
        weakest = analytics_record.weakest_topics if (analytics_record and analytics_record.weakest_topics) else []
        
        # 4. Fetch recent sessions
        recent_db_sessions = db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id
        ).order_by(InterviewSession.created_at.desc()).limit(5).all()
        
        recent_sessions = []
        for s in recent_db_sessions:
            q_list = db.query(Question.id).filter(Question.session_id == s.id).all()
            qs_ids = [q[0] for q in q_list]
            
            completed_count = 0
            sess_avg_score = None
            if qs_ids:
                completed_count = db.query(Answer).filter(Answer.question_id.in_(qs_ids)).count()
                sess_avg = db.query(func.avg(Answer.score)).filter(Answer.question_id.in_(qs_ids)).scalar()
                sess_avg_score = round(sess_avg, 2) if sess_avg else None
                
            recent_sessions.append({
                "id": s.id,
                "company": s.company,
                "role": s.role,
                "interview_type": s.interview_type,
                "difficulty": s.difficulty,
                "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
                "question_count": len(q_list),
                "completed_count": completed_count,
                "average_score": sess_avg_score
            })
            
        # 5. Score trend (grouped by session date)
        score_trend = []
        trend_sessions = db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id
        ).order_by(InterviewSession.created_at.asc()).all()
        
        for ts in trend_sessions:
            t_qs = db.query(Question.id).filter(Question.session_id == ts.id).all()
            t_qs_ids = [q[0] for q in t_qs]
            if t_qs_ids:
                ts_avg = db.query(func.avg(Answer.score)).filter(Answer.question_id.in_(t_qs_ids)).scalar()
                if ts_avg:
                    score_trend.append({
                        "date": ts.created_at.strftime("%Y-%m-%d"),
                        "average_score": round(ts_avg, 2)
                    })
                    
        return {
            "total_interviews": total_interviews,
            "average_score": avg_score,
            "strongest_topics": strongest,
            "weakest_topics": weakest,
            "recent_sessions": recent_sessions,
            "score_trend": score_trend
        }

    @staticmethod
    def get_detailed_analytics(db: Session, user_id: int) -> dict:
        """Calculate detailed statistics including topic performance and weekly averages."""
        sessions = db.query(InterviewSession.id).filter(InterviewSession.user_id == user_id).all()
        session_ids = [s[0] for s in sessions]
        
        topic_performance = []
        weekly_progress = []
        skill_growth = []
        
        if not session_ids:
            return {
                "topic_performance": [],
                "weekly_progress": [],
                "skill_growth": []
            }
            
        # 1. Group by Topic
        topic_results = db.query(
            Question.topic,
            func.avg(Answer.score),
            func.count(Answer.id)
        ).join(Answer, Answer.question_id == Question.id).filter(
            Question.session_id.in_(session_ids)
        ).group_by(Question.topic).all()
        
        for topic, avg, count in topic_results:
            topic_performance.append({
                "topic": topic,
                "average_score": round(avg, 2) if avg else 0.0,
                "question_count": count
            })
            
        # Sort topic performance
        topic_performance.sort(key=lambda x: x["average_score"], reverse=True)
        
        # 2. Weekly progress (aggregate scores by calendar week)
        # For simplicity in SQLite, group by date, then bucket weekly in python
        days_results = db.query(
            InterviewSession.id,
            InterviewSession.created_at,
            Question.topic,
            Answer.score
        ).join(Question, Question.session_id == InterviewSession.id).join(
            Answer, Answer.question_id == Question.id
        ).filter(
            InterviewSession.user_id == user_id
        ).all()
        
        week_buckets = {}
        for session_id, created_at, topic, score in days_results:
            if score is None:
                continue
            # Calculate start of week (Monday)
            start_of_week = created_at - timedelta(days=created_at.weekday())
            week_str = start_of_week.strftime("%Y-%m-%d")
            
            if week_str not in week_buckets:
                week_buckets[week_str] = {"sum": 0.0, "count": 0, "session_ids": set()}
                
            week_buckets[week_str]["sum"] += score
            week_buckets[week_str]["count"] += 1
            week_buckets[week_str]["session_ids"].add(session_id)
            
        for week_str, bucket in sorted(week_buckets.items()):
            weekly_progress.append({
                "week": week_str,
                "average_score": round(bucket["sum"] / bucket["count"], 2),
                "interview_count": len(bucket["session_ids"])
            })
            
        # 3. Skill growth per topic over time
        # Track weekly performance improvement per topic
        skill_growth_buckets = {}
        for session_id, created_at, topic_name, score in days_results:
            if score is None:
                continue
            if not topic_name:
                continue
            start_of_week = created_at - timedelta(days=created_at.weekday())
            week_str = start_of_week.strftime("%Y-%m-%d")
            
            key = (week_str, topic_name)
            if key not in skill_growth_buckets:
                skill_growth_buckets[key] = {"sum": 0.0, "count": 0}
            skill_growth_buckets[key]["sum"] += score
            skill_growth_buckets[key]["count"] += 1
            
        for (week_str, topic_name), val in sorted(skill_growth_buckets.items()):
            skill_growth.append({
                "week": week_str,
                "topic": topic_name,
                "average_score": round(val["sum"] / val["count"], 2)
            })
            
        return {
            "topic_performance": topic_performance,
            "weekly_progress": weekly_progress,
            "skill_growth": skill_growth
        }

    @staticmethod
    def update_user_analytics(db: Session, user_id: int) -> None:
        """Recompute user average score, strongest, and weakest topics and write to database."""
        analytics = db.query(Analytics).filter(Analytics.user_id == user_id).first()
        if not analytics:
            analytics = Analytics(user_id=user_id)
            db.add(analytics)
            db.commit()
            db.refresh(analytics)
            
        sessions = db.query(InterviewSession.id).filter(InterviewSession.user_id == user_id).all()
        session_ids = [s[0] for s in sessions]
        
        if not session_ids:
            return
            
        # Update total count
        analytics.total_interviews = db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id,
            InterviewSession.status == "completed"
        ).count()
        
        # Calculate average score
        questions = db.query(Question.id).filter(Question.session_id.in_(session_ids)).all()
        q_ids = [q[0] for q in questions]
        
        if q_ids:
            avg_val = db.query(func.avg(Answer.score)).filter(Answer.question_id.in_(q_ids)).scalar()
            analytics.average_score = round(avg_val, 2) if avg_val else 0.0
            
            # Find strongest and weakest topics (average score per topic)
            topic_scores = db.query(
                Question.topic,
                func.avg(Answer.score)
            ).join(Answer, Answer.question_id == Question.id).filter(
                Question.session_id.in_(session_ids)
            ).group_by(Question.topic).all()
            
            if topic_scores:
                # Sort by score ascending
                sorted_topics = sorted(topic_scores, key=lambda x: x[1] if x[1] else 0.0)
                # Omit topics that don't have enough data
                analytics.weakest_topics = [t[0] for t in sorted_topics[:2]]
                analytics.strongest_topics = [t[0] for t in reversed(sorted_topics[-2:])]
                
        db.commit()
