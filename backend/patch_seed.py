"""
Patch script — removes lesson_id from QUIZZES_DATA in /app/seed_db.py
Run: docker exec didacticiel_api python /app/patch_seed.py
"""
import re

path = "/app/seed_db.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove any line that contains lesson_id inside a quiz dict
# Pattern: lines like:  lesson_id="quiz-devops",   or  lesson_id="final-quiz",
patched = re.sub(
    r'[ \t]+lesson_id\s*=\s*"[^"]*",?\s*(?:#[^\n]*)?\n',
    '',
    content
)

removed = content.count('lesson_id=') - patched.count('lesson_id=')
print(f"Removed {removed} lesson_id line(s) from QUIZZES_DATA")

with open(path, "w", encoding="utf-8") as f:
    f.write(patched)

print("✅ Patch applied. Now run: python seed_db.py")