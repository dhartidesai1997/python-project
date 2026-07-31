import sys
from datetime import datetime
import random
import re
import argparse
import csv
import json
import os
from debug_logger import DebugLogger
from app_logger import AppLogger

# ----------------------------------------
# TIME PRINTING
# ----------------------------------------
def print_with_time(message):
    current_time = datetime.now().strftime("%H:%M:%S %p")
    print(f"{current_time} Chatbot: {message}")
    
def input_with_time(prompt="User: "):
    timestamp = datetime.now().strftime("%H:%M:%S %p")
    return input(f"{timestamp} {prompt}").strip()
    

# ----------------------------------------
# INTERNAL QUESTIONS FILE
# ----------------------------------------
INTERNAL_FILE = "internal_questions.json"

def load_internal_questions():
    global questions_answers
    if os.path.exists(INTERNAL_FILE):
        with open(INTERNAL_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)
            questions_answers.update(saved)

def save_internal_questions():
    with open(INTERNAL_FILE, "w", encoding="utf-8") as f:
        json.dump(questions_answers, f, indent=2)
        
        

# ----------------------------------------
# QUESTIONS AND ANSWERS (10 keywords, 4-5 variants each)
# ----------------------------------------
questions_answers = {
    "weather": {
        "variants": [
            "what is the weather",
            "how is the weather today",
            "tell me the weather",
            "what's the forecast",
            "how does the weather look"
        ],
        "answers": [
            "It's sunny today.",
            "Looks like it might rain later.",
            "Cloudy skies are expected.",
            "The forecast says sunny intervals."
        ]
    },
    "travel": {
        "variants": [
            "where should I travel",
            "what is the best vacation place",
            "tell me a travel destination",
            "what is your favorite place",
            "suggest a holiday destination"
        ],
        "answers": [
            "I would love to visit Japan.",
            "Paris is beautiful and full of history.",
            "Beaches are relaxing and fun to visit.",
            "Consider Italy for food and culture."
        ]
    },
    "time": {
        "variants": [
            "what time is it",
            "current time",
            "can you tell me the time",
            "what's the time now",
            "tell me the current time"
        ],
        "answers": [
            "It's {time}.",
            "The current time is {time}.",
            "Right now, it is {time}.",
            "According to my clock, it's {time}."
        ]
    },
    "date": {
        "variants": [
            "what is the date today",
            "today's date",
            "can you tell me the date",
            "what date is it today",
            "show me today's date"
        ],
        "answers": [
            "Today is {date}.",
            "It's {date} today.",
            "The date today is {date}.",
            "According to my calendar, today is {date}."
        ]
    },
    "name": {
        "variants": [
            "what is your name",
            "who are you",
            "how do you call yourself",
            "introduce yourself",
            "your name"
        ],
        "answers": [
            "I am ChatBot. I can help you with your query",
            
        ]
    },
    "location": {
        "variants": [
            "where are you",
            "what is the location",
            "where is this",
            "can you tell me the location",
            "how do I reach there"
        ],
        "answers": [
            "I exist in the cloud.",
            "I am everywhere and nowhere at the same time.",
            "I live in the digital world.",
            "Think of me as being online."
        ]
    },
    "python": {
        "variants": [
            "what is python",
            "how to learn python",
            "best python book",
            "python programming",
            "python tutorial"
        ],
        "answers": [
            "Python is a programming language widely used in data science and web development.",
            "'Automate the Boring Stuff' is great for beginners.",
            "'Python Crash Course' is highly recommended.",
            "'Learn Python the Hard Way' is also useful."
        ]
    },
    "food": {
        "variants": [
            "what is your favorite food",
            "what food do you like",
            "tell me about food",
            "favorite cuisine",
            "recommend a dish"
        ],
        "answers": [
            "I love virtual cookies!",
            "Pizza sounds delicious.",
            "Sushi is very tasty.",
            "I enjoy all kinds of food virtually."
        ]
    },
    "joke": {
        "variants": [
            "tell me a joke",
            "can you make me laugh",
            "say a joke",
            "I want to hear a joke",
            "make me laugh"
        ],
        "answers": [
            "Why did the computer go to the doctor? It caught a virus!",
            "Why was the math book sad? Too many problems.",
            "Why did the programmer quit his job? He didn't get arrays.",
            "I would tell you a UDP joke, but you might not get it."
        ]
    },
    "machine learning": {
        "variants": [
            "what is machine learning?",
            "what does machine learning mean?",
            "how does machine learning work?",
            "explain machine learning.",
            "give me a definition of machine learning."
        ],
        "answers": [
            "Machine Learning is a type of AI where systems learn from data.",
            "Machine Learning helps computers learn patterns automatically.",
            "It is a method that allows computers to improve through experience.",
            "ML enables systems to make predictions or decisions without being explicitly programmed."
        ]
    },
    "music": {
        "variants": [
            "what kind of music do you like",
            "what is your favorite music",
            "tell me about music",
            "do you like music",
            "music preference"
        ],
        "answers": [
            "I enjoy all kinds of music.",
            "Pop and jazz are my favorites.",
            "Music helps me relax, even as a chatbot.",
            "I like classical music too!"
        ]
    }
    
}

keywords_dict = {key: [key] for key in questions_answers.keys()}

# ----------------------------------------
# CLEAN TEXT
# ----------------------------------------
def clean_text(text):
    text = text.strip().lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# ----------------------------------------
# IMPORT CSV
# ----------------------------------------
def import_csv(filepath):
    imported_data = {}
        # Check file extension
    if not filepath.lower().endswith('.csv'):
        print_with_time(f"Unsupported file type: {os.path.splitext(filepath)[1][1:].upper()}")
        DebugLogger.log(f"Unsupported file type: {filepath}")
        return None


    # Check file existence and read access
    if not os.path.exists(filepath):
        print_with_time(f"CSV file not found: {filepath}")
        DebugLogger.log(f"CSV file not found: {filepath}")
        AppLogger.log(f"CSV file not found: {filepath}", "WARNING")  # external file logs
        return None


    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
           
            try:
                reader = csv.DictReader(csvfile)


                # Check for required columns
                required_columns = {'keyword', 'variant', 'answer'}
                if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
                    print_with_time(f"CSV file format error: missing columns. Required columns are {required_columns}")
                    DebugLogger.log(f"CSV file format error: {reader.fieldnames}")
                    return None

                for row_num, row in enumerate(reader, start=1):
                    if not row:
                        continue  # Skip empty rows

                    try:
                        keyword = clean_text(row.get('keyword') or '')
                        variant = clean_text(row.get('variant') or '')
                        answer_cell = row.get('answer') or ''
                        answers = [a.strip() for a in answer_cell.split('|') if a.strip()]
                    except Exception as e:
                        DebugLogger.log(f"Row {row_num} parsing error: {e}")
                        continue  # Skip row if parsing fails

                    if not keyword or not variant:
                        DebugLogger.log(f"Row {row_num} skipped: missing keyword or variant")
                        continue

                    # --- Debug log for every imported row ---
                    DebugLogger.log(f"Imported row {row_num}: keyword='{keyword}', variant='{variant}', answers={answers}")

                    if keyword not in imported_data:
                        imported_data[keyword] = {"variants": [], "answers": []}

                    if variant not in imported_data[keyword]["variants"]:
                        imported_data[keyword]["variants"].append(variant)

                    imported_data[keyword]["answers"].extend(answers)
                    imported_data[keyword]["answers"] = list(dict.fromkeys(imported_data[keyword]["answers"]))

                DebugLogger.log(f"Finished importing CSV. Total keywords imported: {len(imported_data)}")
                return imported_data

            except Exception as e:
                print_with_time(f"Error reading CSV file: {e}")
                DebugLogger.log(f"CSV reading error: {e}")
                return None

    except PermissionError:
        print_with_time(f"Permission denied: cannot read file {filepath}")
        DebugLogger.log(f"Permission denied for file: {filepath}")
        return None
    except Exception as e:
        print_with_time(f"Error opening file: {e}")
        DebugLogger.log(f"Error opening CSV file: {e}")
        return None

# ----------------------------------------
# CLEAN INPUT
# ----------------------------------------
def clean_input(user_input):
    text = user_input.strip().lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# ----------------------------------------
# SPLIT COMPOUND QUESTIONS
# ----------------------------------------
def split_compound_questions(user_input):
    user_input = re.sub(r'\s+', ' ', user_input.strip())
    questions = re.split(r'\?', user_input)
    final_questions = []
    for q in questions:
        q = q.strip()
        if not q:
            continue
        parts = re.split(r'\s+(?:and|or)\s+', q, flags=re.IGNORECASE)
        parts = [p.strip() for p in parts if p]
        final_questions.extend(parts)
    return final_questions

# ----------------------------------------
# GET ANSWER FOR SINGLE QUESTION
# ----------------------------------------
def get_answer_for_question(question):
    cleaned = clean_input(question)
    DebugLogger.log(f"Processing question: '{question}' -> cleaned: '{cleaned}'")
    AppLogger.log(f"Question asked: {question}")

    for key, value in questions_answers.items():
        for variant in value["variants"]:
            if clean_input(variant) == cleaned:
                answer = random.choice(value["answers"])
                answer = answer.replace("{time}", datetime.now().strftime("%H:%M:%S %p"))
                answer = answer.replace("{date}", datetime.now().strftime("%d-%m-%Y"))
                DebugLogger.log(f"Exact match found for keyword '{key}' with variant '{variant}'. Answer: '{answer}'")
                AppLogger.log(f"Answer returned: {answer}", "INFO")
                return {"mode": "answer", "text": answer}
                
    for key, value in questions_answers.items():
        for variant in value["variants"]:
            if cleaned in clean_input(variant) or clean_input(variant) in cleaned:
                answer = random.choice(value["answers"])
                answer = answer.replace("{time}", datetime.now().strftime("%H:%M:%S %p"))
                answer = answer.replace("{date}", datetime.now().strftime("%d-%m-%Y"))
                DebugLogger.log(f"Partial match found for keyword '{key}' with variant '{variant}'. Answer: '{answer}'")
                AppLogger.log(f"Answer returned: {answer}", "INFO")
                return {"mode": "answer", "text": answer}
            
    DebugLogger.log(f"No match found for question: '{question}'")
    AppLogger.log(f"No answer found for: {question}", "WARNING")

    return {"mode": "answer", "text": "Sorry, I didn't understand that question."}

# ----------------------------------------
# LIST ALL QUESTIONS
# ----------------------------------------
def list_all_questions():
    print_with_time("Listing all questions in the knowledge base:")
    counter = 1
    for key, value in questions_answers.items():
        DebugLogger.log(f"Listing keyword: '{key}' with variants: {value['variants']}")
        for variant in value["variants"]:
            print(f"{counter}. {variant}")
            DebugLogger.log(f"Printed question {counter}: '{variant}'")
            counter += 1

# ----------------------------------------
# ADD / REMOVE QUESTIONS
# ----------------------------------------
def add_question(keyword, question, answers):
    key = clean_text(keyword)
    DebugLogger.log(f"Attempting to add/update keyword: '{key}' with question: '{question}' and answers: {answers}")
    
    # If Keyword already exists
    if key in questions_answers:
        DebugLogger.log(f"Keyword '{key}' exists. Checking for new variants/answers.")
        
        # Add question if unique
        if question not in questions_answers[key]["variants"]:
            questions_answers[key]["variants"].append(question)
            DebugLogger.log(f"Added new variant for '{key}': '{question}'")
        else:
            DebugLogger.log(f"Variant '{question}' already exists for '{key}'")
                
        # Add answers uniquely
        for ans in answers:
            if ans not in questions_answers[key]["answers"]:
                questions_answers[key]["answers"].append(ans)
                DebugLogger.log(f"Added new answer for '{key}': '{ans}'")
            else:
                DebugLogger.log(f"Answer '{ans}' already exists for '{key}'")

        print_with_time(f"Updated existing keyword '{key}'.")

    else:
        # New keyword entry
        questions_answers[key] = {
            "variants": [question],
            "answers": list(dict.fromkeys(answers))
        }
        DebugLogger.log(f"Created new keyword entry '{key}' with variants: {[question]} and answers: {answers}")
        print_with_time(f"Created new keyword entry '{key}'.")

    save_internal_questions()
    DebugLogger.log(f"Saved questions_answers after adding/updating '{key}'")

    
    print_with_time(f"Added/Updated question: '{question}'")

def remove_question(question):
    key = clean_text(question)
    DebugLogger.log(f"Attempting to remove question with keyword: '{key}'")
    
    
    if key in questions_answers:
        questions_answers.pop(key)
        save_internal_questions()
        print_with_time(f"Removed question: '{question}'")
        DebugLogger.log(f"Question removed from internal storage: '{key}'")
        DebugLogger.log(f"Current keywords after removal: {list(questions_answers.keys())}")
    else:
        print_with_time(f"Question not found: '{question}'")
        DebugLogger.log(f"Tried to remove non-existent question: '{key}'")
  
# Remove Answers    
def remove_answer(keyword, question, answer_to_remove):
    key = clean_text(keyword)
    DebugLogger.log(f"Attempting to remove answer '{answer_to_remove}' from question '{question}' under keyword '{key}'")

    if key not in questions_answers:
        print_with_time(f"Keyword not found: '{keyword}'")
        DebugLogger.log(f"Keyword '{key}' does not exist in questions_answers")
        return

    # Check if question exists under the keyword
    if question not in questions_answers[key]["variants"]:
        print_with_time(f"Question not found under keyword '{keyword}': '{question}'")
        DebugLogger.log(f"Question '{question}' does not exist under keyword '{key}'")
        return

    # Check if answer exists and remove
    if answer_to_remove in questions_answers[key]["answers"]:
        questions_answers[key]["answers"].remove(answer_to_remove)
        print_with_time(f"Removed answer '{answer_to_remove}' from question '{question}'")
        DebugLogger.log(f"Remaining answers for '{key}': {questions_answers[key]['answers']}")


        # If no answers left, remove the whole keyword
        if not questions_answers[key]["answers"]:
            questions_answers.pop(key)
            print_with_time(f"No answers left. Removed entire keyword '{keyword}'")
            DebugLogger.log(f"Keyword '{keyword}' removed due to no answers")

    else:
        print_with_time(f"Answer not found: '{answer_to_remove}'")
        DebugLogger.log(f"Tried to remove non-existent answer: '{answer_to_remove}' for keyword '{key}'")

    save_internal_questions()
    DebugLogger.log(f"Saved questions_answers after removal operation for keyword '{key}'")
        

def is_single_keyword(user_text):
    words = user_text.split()
    # Only 1–2 words are allowed to be a keyword
    if len(words) > 2:
        return False

    # Must match a real keyword inside the dict
    return user_text in questions_answers



# ... This is the end of your existing is_single_keyword function ...
    return user_text in questions_answers

# ----------------------------------------
# ADDING TRIVIA GAME CLASS
# ----------------------------------------
class TriviaGame:
    def __init__(self):
        self.active = False
        self.score = 0
        self.count = 0
        self.max = 5 
        self.current_q = None
        self.questions = [
            {"q": "What is the capital of France?", "o": ["A) Berlin", "B) Madrid", "C) Paris", "D) Rome"], "a": "C"},
            {"q": "Which planet is known as the Red Planet?", "o": ["A) Earth", "B) Mars", "C) Venus", "D) Jupiter"], "a": "B"},
            {"q": "Who wrote 'Romeo and Juliet'?", "o": ["A) Dickens", "B) Hemingway", "C) Shakespeare", "D) Twain"], "a": "C"},
            {"q": "What is the largest mammal?", "o": ["A) Elephant", "B) Blue Whale", "C) Giraffe", "D) Shark"], "a": "B"},
            {"q": "Which element has the symbol 'O'?", "o": ["A) Gold", "B) Silver", "C) Oxygen", "D) Iron"], "a": "C"}
        ]

    def start(self):
        self.active = True
        self.score = 0
        self.count = 0
        print_with_time("Built-in trivia game is activated!")

    def next_question(self):
        if self.count >= self.max: 
            return None
        
        # Select the next question
        self.current_q = random.choice(self.questions)
        self.count += 1
        
        # Calculate current progress and score indicator
        # Note: We show score out of total questions (self.max) as per standard trivia UX
        progress_info = f"--- Question {self.count} of {self.max}; Score {self.score}/{self.max} ---"
        
        return f"{progress_info}\nQuestion {self.count}: {self.current_q['q']}\n" + "\n".join(self.current_q['o'])



# ----------------------------------------
# MAIN FUNCTION
# ----------------------------------------
def main():
    parser = argparse.ArgumentParser(description="ChatBot with CSV import, add/remove questions")
    parser.add_argument('--import', dest='import_csv_flag', action='store_true', help='Import Q&A from CSV')
    parser.add_argument('--filetype', type=str, default='CSV', help='File type: CSV')
    parser.add_argument('--filepath', type=str, help='Path to CSV file')
    parser.add_argument('--list-questions', action='store_true', help='List all questions in the knowledge base')
    parser.add_argument('--add', action='store_true', help='Add a question to internal list')
    parser.add_argument('--keyword', type=str, help='add Keyword in internal list')
    parser.add_argument('--remove', action='store_true', help='Remove a question from internal list')
    parser.add_argument('--question', type=str, help='Question text for add/remove')
    parser.add_argument('--answer', type=str, help='Answer(s) for add command (pipe-separated if multiple)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--log', action='store_true', help='Enable file-based logging')
    parser.add_argument('--log-level', choices=['INFO', 'WARNING'], default='WARNING',
                    help='Logging level (default: WARNING)')
    args = parser.parse_args()
    # -------------------------------------
    # CALL LOGGER SETUP HERE (TOP OF MAIN)
    # -------------------------------------
    AppLogger.setup(args.log, args.log_level)
    AppLogger.log("Logger initialized at program start.", "INFO")
    DebugLogger.enabled = args.debug
    DebugLogger.log(f"Command-line arguments: {args}")
    DebugLogger.log("Debug mode enabled")
    

    
    
    global questions_answers, keywords_dict

    # Load previously saved internal questions
    load_internal_questions()
    DebugLogger.log(f"Loaded {len(questions_answers)} questions from JSON: {list(questions_answers.keys())}")


    # Merge CSV if file path is provided
    if args.filepath:
        DebugLogger.log(f"CSV file path provided: {args.filepath}")
        imported = import_csv(args.filepath)
        DebugLogger.log(f"Raw imported data: {imported}")
        if imported:
            for key, value in imported.items():
                DebugLogger.log(f"Processing imported keyword: '{key}' with data: {value}")
                if key in questions_answers:
                    existing_variants = set(questions_answers[key]["variants"])
                    for v in value["variants"]:
                        if v not in existing_variants:
                            questions_answers[key]["variants"].append(v)
                            DebugLogger.log(f"Added variant '{v}' to existing keyword '{key}'")
                    existing_answers = set(questions_answers[key]["answers"])
                    for a in value["answers"]:
                        if a not in existing_answers:
                            questions_answers[key]["answers"].append(a)
                            DebugLogger.log(f"Added answer '{a}' to existing keyword '{key}'")
                else:
                    questions_answers[key] = value
                    DebugLogger.log(f"Created new keyword '{key}' from CSV")
            keywords_dict = {k: [k] for k in questions_answers.keys()}
            if args.import_csv_flag:
                print_with_time(f"Successfully imported {len(imported)} keywords from CSV.")
                DebugLogger.log(f"Imported keywords: {list(imported.keys())}")
        else:
            print_with_time("CSV import failed. Continuing in chat mode.")
            DebugLogger.log("CSV import failed or returned empty")


    # Add question
    if args.add:
        DebugLogger.log("Add command detected")
        if not args.keyword or not args.question or not args.answer:
            print_with_time("Error: --keyword, --question and --answer are required for --add")
            DebugLogger.log("Missing --keyword or --question or --answer for add")
            sys.exit(1)

        answers_list = [a.strip() for a in args.answer.split("|") if a.strip()]
        DebugLogger.log(f"Adding question '{args.question}' under keyword '{args.keyword}' with answers {answers_list}")
        add_question(args.keyword, args.question, answers_list)
        sys.exit(0)


    # Remove question
    if args.remove:
        DebugLogger.log("Remove command detected")
        if not args.keyword or not args.question or not args.answer:
            print_with_time("Error: --keyword, --question and --answer are required for --remove")
            DebugLogger.log("Missing --keyword or --question or --answer for remove")
            sys.exit(1)

        DebugLogger.log(f"Removing answer '{args.answer}' from question '{args.question}' under keyword '{args.keyword}'")
        remove_answer(args.keyword, args.question, args.answer)
        sys.exit(0)
        
                  
                  
    # List all questions
    if args.list_questions:
        DebugLogger.log("List questions command detected")
        list_all_questions()
        sys.exit(0)

    # Chatbot interactive loop
    print_with_time("Type anything. Type 'bye' to exit.")
    DebugLogger.log("Entering interactive chat loop")
    
    AppLogger.setup(args.log, args.log_level)
    AppLogger.log("Application started.", "INFO")
    
    # ----------------------------------------
    # CREATING OBJECT OF CLASS TriviaGame:
    # ----------------------------------------
    trivia = TriviaGame()

    while True:
        user_input = input_with_time()
        DebugLogger.log(f"User input received: '{user_input}'")
        cleaned = clean_input(user_input)
        DebugLogger.log(f"Cleaned user input: '{cleaned}'")

        if cleaned == "bye":
            print_with_time("Goodbye!")
            DebugLogger.log("User exited chat")
            break


        # ----------------------------------------
        # INSERTING TRIVIA LOGIC HERE
        # ----------------------------------------
        if cleaned == "trivia":
            if not trivia.active:
                trivia.start()
                print_with_time(trivia.next_question())
            else:
                print_with_time(f"Your score: {trivia.score}/{trivia.count}. Exiting game.")
                trivia.active = False
            continue

        if trivia.active:
            # Check answer
            correct = trivia.current_q['a']
            if user_input.strip().upper() == correct:
                trivia.score += 1
                print_with_time(f"Correct! The answer was {correct}.")
            else:
                print_with_time(f"Incorrect! The correct answer was {correct}.")
            
            # Ask next or end
            next_q = trivia.next_question()
            if next_q:
                print_with_time(next_q)
            else:
                print_with_time(f"Game over! Final score: {trivia.score}/{trivia.max}")
                trivia.active = False
            continue
        # ----------------------------------------
        # This only runs if trivia.active is False
        # ----------------------------------------
        if is_single_keyword(cleaned):
            DebugLogger.log(f"Detected single keyword: '{cleaned}'")
        
        
        
        # ----------------------------------------
        # NEW KEYWORD MENU LOGIC (only for real short keywords)
        # ----------------------------------------
        if is_single_keyword(cleaned):
            DebugLogger.log(f"Detected single keyword: '{cleaned}'")
            category = cleaned
            related_questions = questions_answers[category]["variants"]

            print_with_time(f"Here are the questions related to '{category}':")
            for i, qtext in enumerate(related_questions, 1):
                print(f"{i}. {qtext}")
            print("0. Cancel")

            selection = input_with_time("Select number: ")
            DebugLogger.log(f"User selected: {selection}")

            if selection.isdigit():
                selection = int(selection)
                if selection == 0:
                    print_with_time("Cancelled.")
                    DebugLogger.log("User cancelled selection")
                    continue
                if 1 <= selection <= len(related_questions):
                    selected_question = related_questions[selection - 1]
                    response = get_answer_for_question(selected_question)
                    DebugLogger.log(f"Answer returned: {response['text']}")
                    print_with_time(response["text"])
                    continue
                else:
                    print_with_time("Invalid selection.")
                    DebugLogger.log(f"User selected invalid number: {selection}")
                    continue
            else:
                print_with_time("Invalid input.")
                DebugLogger.log(f"User input not a number: {selection}")
                continue
            

        # ----------------------------------------
        # NORMAL QUESTION PROCESSING LOGIC
        # ----------------------------------------
        questions = split_compound_questions(user_input)
        DebugLogger.log(f"Split user input into questions: {questions}")
        for q in questions:
            response = get_answer_for_question(q)
            DebugLogger.log(f"Answer for '{q}': {response['text']}")
            print_with_time(response["text"])


if __name__ == "__main__":
    main()