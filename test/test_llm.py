import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm import generate_music_insights

result = generate_music_insights("Imagine", "John Lennon")

print(result)
