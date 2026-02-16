from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.database import get_db
from app.schemas.quiz import QuizResponse, QuizSubmission, QuizResult, QuizCreate
from app.models.quiz import Quiz, QuizAttempt
from app.models.user import User
from app.api.deps import get_current_active_user, require_admin

router = APIRouter(prefix="/api/quizzes", tags=["Quizzes"])

@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(
    quiz_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/quizzes/{quiz_id} - Récupérer un quiz"""
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return QuizResponse(
        id=quiz.id,
        title=quiz.title,
        module_id=quiz.module_id,
        questions=quiz.questions,
        passing_score=quiz.passing_score,
        time_limit=quiz.time_limit
    )

@router.post("/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(
    quiz_id: str,
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """POST /api/quizzes/{quiz_id}/submit - Soumettre les réponses d'un quiz"""
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Calculer le score
    total_questions = len(quiz.questions)
    correct_answers_count = 0
    answers_correctness = {}
    
    for question in quiz.questions:
        q_id = question["id"]
        user_answers = submission.answers.get(q_id, [])
        correct_ans = question["correct_answers"]
        
        # Comparer les réponses
        is_correct = sorted(user_answers) == sorted(correct_ans)
        answers_correctness[q_id] = is_correct
        
        if is_correct:
            correct_answers_count += 1
    
    # Calculer le score en pourcentage
    score = int((correct_answers_count / total_questions) * 100)
    passed = score >= quiz.passing_score
    
    # Créer l'attempt
    attempt = QuizAttempt(
        id=str(uuid.uuid4()),
        quiz_id=quiz_id,
        user_id=current_user.id,
        score=score,
        passed=1 if passed else 0,
        correct_answers=correct_answers_count,
        total_questions=total_questions,
        time_taken=0,  # TODO: implementer le calcul du temps
        answers=answers_correctness
    )
    
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    return QuizResult(
        attempt_id=attempt.id,
        score=score,
        passed=passed,
        correct_answers=correct_answers_count,
        total_questions=total_questions,
        time_taken=attempt.time_taken,
        answers=answers_correctness
    )

@router.get("/{quiz_id}/results/{attempt_id}", response_model=QuizResult)
async def get_quiz_results(
    quiz_id: str,
    attempt_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """GET /api/quizzes/{quiz_id}/results/{attempt_id} - Récupérer les résultats"""
    
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id,
        QuizAttempt.quiz_id == quiz_id
    ).first()
    
    if not attempt:
        raise HTTPException(status_code=404, detail="Quiz attempt not found")
    
    # Vérifier que l'utilisateur a le droit de voir ces résultats
    if attempt.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return QuizResult(
        attempt_id=attempt.id,
        score=attempt.score,
        passed=bool(attempt.passed),
        correct_answers=attempt.correct_answers,
        total_questions=attempt.total_questions,
        time_taken=attempt.time_taken,
        answers=attempt.answers
    )

@router.post("", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """POST /api/quizzes - Créer un quiz (Admin uniquement)"""
    
    # Convertir les questions en dict pour JSON
    questions_dict = [q.dict() for q in quiz_data.questions]
    
    new_quiz = Quiz(
        id=f"quiz-{uuid.uuid4().hex[:8]}",
        title=quiz_data.title,
        module_id=quiz_data.module_id,
        questions=questions_dict,
        passing_score=quiz_data.passing_score,
        time_limit=quiz_data.time_limit
    )
    
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    
    return QuizResponse(
        id=new_quiz.id,
        title=new_quiz.title,
        module_id=new_quiz.module_id,
        questions=new_quiz.questions,
        passing_score=new_quiz.passing_score,
        time_limit=new_quiz.time_limit
    )
