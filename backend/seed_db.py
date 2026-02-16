"""
Script pour peupler la base de données avec des données de test
Usage: python seed_db.py
"""

from app.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.module import Module
from app.models.lesson import Lesson, LessonType
from app.models.quiz import Quiz
from app.models.progression import UserProgression, UserBadge
from app.core.security import get_password_hash
import uuid

def seed_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("🌱 Seeding database...")
        
        # Create admin user
        admin = User(
            id=str(uuid.uuid4()),
            email="admin@didacticiel.com",
            hashed_password=get_password_hash("Admin123!"),
            first_name="Admin",
            last_name="System",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        
        # Create instructor
        instructor = User(
            id=str(uuid.uuid4()),
            email="instructor@didacticiel.com",
            hashed_password=get_password_hash("Instructor123!"),
            first_name="Marie",
            last_name="Dubois",
            role=UserRole.INSTRUCTOR,
            is_active=True
        )
        db.add(instructor)
        
        # Create students
        students = []
        student_names = [
            ("Jean", "Martin"), ("Sophie", "Bernard"), ("Lucas", "Thomas"),
            ("Emma", "Petit"), ("Hugo", "Robert"), ("Léa", "Richard"),
            ("Tom", "Durand"), ("Chloé", "Moreau"), ("Louis", "Simon"),
            ("Camille", "Laurent"), ("Gabriel", "Lefevre"), ("Manon", "Michel")
        ]
        
        for first_name, last_name in student_names:
            student = User(
                id=str(uuid.uuid4()),
                email=f"{first_name.lower()}.{last_name.lower()}@student.com",
                hashed_password=get_password_hash("Student123!"),
                first_name=first_name,
                last_name=last_name,
                role=UserRole.STUDENT,
                is_active=True
            )
            students.append(student)
            db.add(student)
        
        db.commit()
        print(f"✅ Created {len(students) + 2} users")
        
        # Create progressions for students
        for student in students:
            progression = UserProgression(
                id=str(uuid.uuid4()),
                user_id=student.id,
                progression=0,
                modules_completed=[],
                time_spent=0
            )
            db.add(progression)
        
        db.commit()
        print("✅ Created user progressions")
        
        # Create Module 1: DevOps Basics
        module1 = Module(
            id="module-1",
            title="DevOps Basics",
            description="Introduction aux principes DevOps, CI/CD et conteneurisation avec Docker",
            week=1,
            order=1,
            total_duration=180
        )
        db.add(module1)
        
        # Lessons for Module 1
        lessons_m1 = [
            Lesson(
                id="lesson-1-1",
                module_id="module-1",
                title="Introduction to DevOps",
                type=LessonType.VIDEO,
                duration="5:30",
                url="https://loom.com/share/example1",
                order=1
            ),
            Lesson(
                id="lesson-1-2",
                module_id="module-1",
                title="Understanding CI/CD Pipelines",
                type=LessonType.VIDEO,
                duration="8:15",
                url="https://loom.com/share/example2",
                order=2
            ),
            Lesson(
                id="lesson-1-3",
                module_id="module-1",
                title="Docker Fundamentals",
                type=LessonType.VIDEO,
                duration="10:45",
                url="https://loom.com/share/example3",
                order=3
            ),
            Lesson(
                id="lesson-1-4",
                module_id="module-1",
                title="GitHub Actions Basics",
                type=LessonType.TEXT,
                duration="6:00",
                content="# GitHub Actions\n\nGitHub Actions permet d'automatiser...",
                order=4
            )
        ]
        
        for lesson in lessons_m1:
            db.add(lesson)
        
        # Quiz for Module 1
        quiz1 = Quiz(
            id="quiz-1",
            title="DevOps Fundamentals Quiz",
            module_id="module-1",
            passing_score=70,
            time_limit=1800,
            questions=[
                {
                    "id": "q1",
                    "question": "What does CI/CD stand for?",
                    "type": "single",
                    "options": [
                        "Continuous Integration / Continuous Deployment",
                        "Code Integration / Code Deployment",
                        "Constant Integration / Constant Delivery",
                        "None of the above"
                    ],
                    "correct_answers": [0],
                    "explanation": "CI/CD stands for Continuous Integration and Continuous Deployment"
                },
                {
                    "id": "q2",
                    "question": "Which command is used to run a Docker container?",
                    "type": "single",
                    "options": [
                        "docker start",
                        "docker run",
                        "docker execute",
                        "docker launch"
                    ],
                    "correct_answers": [1],
                    "explanation": "The 'docker run' command creates and starts a container"
                },
                {
                    "id": "q3",
                    "question": "What are the benefits of using GitHub Actions? (Select all that apply)",
                    "type": "multiple",
                    "options": [
                        "Automated workflows",
                        "Built-in CI/CD",
                        "Free for open source",
                        "Works only with GitHub"
                    ],
                    "correct_answers": [0, 1, 2],
                    "explanation": "GitHub Actions provides automation, CI/CD, and is free for open source projects"
                }
            ]
        )
        db.add(quiz1)
        
        # Create Module 2: MLOps Fundamentals
        module2 = Module(
            id="module-2",
            title="MLOps Fundamentals",
            description="Découverte de DVC, MLflow et gestion du cycle de vie ML",
            week=2,
            order=2,
            total_duration=240
        )
        db.add(module2)
        
        # Lessons for Module 2
        lessons_m2 = [
            Lesson(
                id="lesson-2-1",
                module_id="module-2",
                title="Introduction to MLOps",
                type=LessonType.VIDEO,
                duration="7:20",
                url="https://loom.com/share/example4",
                order=1
            ),
            Lesson(
                id="lesson-2-2",
                module_id="module-2",
                title="Data Version Control with DVC",
                type=LessonType.VIDEO,
                duration="12:30",
                url="https://loom.com/share/example5",
                order=2
            ),
            Lesson(
                id="lesson-2-3",
                module_id="module-2",
                title="Experiment Tracking with MLflow",
                type=LessonType.VIDEO,
                duration="15:00",
                url="https://loom.com/share/example6",
                order=3
            )
        ]
        
        for lesson in lessons_m2:
            db.add(lesson)
        
        # Create Module 3: Deployment & API
        module3 = Module(
            id="module-3",
            title="Deployment & API",
            description="Création d'API avec FastAPI et déploiement de modèles ML",
            week=3,
            order=3,
            total_duration=200
        )
        db.add(module3)
        
        # Create Module 4: Advanced Topics
        module4 = Module(
            id="module-4",
            title="Advanced MLOps",
            description="Monitoring, scaling et best practices en production",
            week=4,
            order=4,
            total_duration=220
        )
        db.add(module4)
        
        db.commit()
        print("✅ Created 4 modules with lessons and quizzes")
        
        # Add some badges to first student
        if students:
            badge1 = UserBadge(
                id=str(uuid.uuid4()),
                user_id=students[0].id,
                badge_name="first-lesson"
            )
            badge2 = UserBadge(
                id=str(uuid.uuid4()),
                user_id=students[0].id,
                badge_name="quiz-master"
            )
            db.add(badge1)
            db.add(badge2)
        
        db.commit()
        print("✅ Added badges")
        
        print("\n" + "="*60)
        print("🎉 Database seeded successfully!")
        print("="*60)
        print("\n📝 Test Credentials:")
        print("-" * 60)
        print("👑 Admin:")
        print("   Email: admin@didacticiel.com")
        print("   Password: Admin123!")
        print("\n👨‍🏫 Instructor:")
        print("   Email: instructor@didacticiel.com")
        print("   Password: Instructor123!")
        print("\n👨‍🎓 Student:")
        print("   Email: jean.martin@student.com")
        print("   Password: Student123!")
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
