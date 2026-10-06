import os
import re

from colorama import Fore, Style, init
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


init(autoreset=True)
load_dotenv()


MODEL_NAME = "gpt-6-luna"
TOTAL_MOCK_QUESTIONS = 5


def create_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print(Fore.RED + "OPENAI_API_KEY is missing.")
        print(
            Fore.YELLOW
            + "Create a .env file and add your OpenAI API key before continuing."
        )
        raise SystemExit(1)

    return OpenAI(api_key=api_key)


client = create_client()


def ask_model(user_prompt, instructions=None):
    if instructions is None:
        instructions = (
            "You are an expert technical interviewer and patient instructor. "
            "Provide accurate, clear, and educational responses. "
            "Follow the requested format carefully."
        )

    try:
        response = client.responses.create(
            model=MODEL_NAME,
            instructions=instructions,
            input=user_prompt,
        )

        output_text = response.output_text.strip()

        if not output_text:
            print(Fore.YELLOW + "The model returned an empty response.")
            return None

        return Fore.LIGHTGREEN_EX + Style.BRIGHT + output_text

    except OpenAIError as error:
        print(Fore.RED + f"OpenAI API error: {error}")
        return None


def print_section_heading(title, color):
    print("\n" + color + Style.BRIGHT + title)
    print(color + "-" * 60)


def print_result_heading(title, color):
    print("\n" + color + Style.BRIGHT + title)
    print(color + "=" * 60)


def get_non_empty_input(prompt):
    while True:
        try:
            value = input(prompt).strip()
        except EOFError:
            print(Fore.RED + "\nInput stream was closed.")
            return "menu"

        if value:
            return value

        print(Fore.YELLOW + "Input cannot be empty. Please try again.")


def get_difficulty():
    valid_difficulties = {
        "1": "Beginner",
        "2": "Intermediate",
        "3": "Advanced",
    }

    while True:
        print("\nChoose a difficulty level:")
        print("1. Beginner")
        print("2. Intermediate")
        print("3. Advanced")

        choice = input("Choose an option: ").strip()

        if choice in valid_difficulties:
            return valid_difficulties[choice]

        print(Fore.YELLOW + "Invalid choice. Please select 1, 2, or 3.")


def get_learning_level():
    valid_levels = {
        "1": "Beginner",
        "2": "Intermediate",
    }

    while True:
        print("\nChoose your learning level:")
        print("1. Beginner")
        print("2. Intermediate")

        choice = input("Choose an option: ").strip()

        if choice in valid_levels:
            return valid_levels[choice]

        print(Fore.YELLOW + "Invalid choice. Please select 1 or 2.")


def extract_score(evaluation):
    match = re.search(
        r"\bscore\s*:\s*(10|[0-9])\s*/\s*10\b",
        evaluation,
        re.IGNORECASE,
    )

    if not match:
        return None

    score = int(match.group(1))

    if 0 <= score <= 10:
        return score

    return None


def generate_interview_questions():
    print_section_heading("Generate Interview Questions", Fore.GREEN)

    topic = get_non_empty_input(
        "Enter a topic, such as Python, SQL, OOP, DSA, React, or GenAI: "
    )

    if topic.lower() == "menu":
        return

    difficulty = get_difficulty()

    prompt = f"""
Generate exactly 5 technical interview questions about "{topic}".

Difficulty level: {difficulty}

For each question, provide:

1. The interview question
2. A short answer
3. A clear explanation
4. One common mistake candidates make

Number the questions from 1 to 5.
Keep the answers accurate and suitable for the selected difficulty.
Use plain text and clear headings.
"""

    print(Fore.YELLOW + "\nGenerating questions...\n")

    result = ask_model(prompt)

    if result is not None:
        print_result_heading("Interview Questions", Fore.GREEN)
        print(Fore.WHITE + result)

    input("\nPress Enter to return to the main menu...")


def explain_topic():
    print_section_heading("Explain a Technical Topic", Fore.BLUE)

    topic = get_non_empty_input(
        "Enter a technical topic, such as Python functions, SQL joins, or REST APIs: "
    )

    if topic.lower() == "menu":
        return

    learning_level = get_learning_level()

    prompt = f"""
Explain the technical topic "{topic}" to a {learning_level.lower()} learner.

Your response must include:

1. A simple definition
2. Why the concept is important
3. How it works
4. One practical example
5. Two common mistakes or misunderstandings

If the topic involves programming, include a short code example
and explain it clearly.

Use simple language and organize the response with headings.
Avoid assuming advanced prior knowledge.
"""

    print(Fore.YELLOW + "\nGenerating explanation...\n")

    result = ask_model(prompt)

    if result is not None:
        print_result_heading("Technical Explanation", Fore.BLUE)
        print(Fore.WHITE + result)

    input("\nPress Enter to return to the main menu...")


def generate_mock_question(topic, question_number):
    prompt = f"""
You are conducting a technical interview.

Generate question {question_number} of {TOTAL_MOCK_QUESTIONS}
about the topic "{topic}".

Ask exactly one interview question.
Do not provide the answer.
Do not include multiple questions.
Keep the question appropriate for an interview candidate.
"""

    return ask_model(prompt)


def evaluate_interview_answer(question, answer):
    prompt = f"""
You are evaluating a technical interview answer.

Interview question:
{question}

Candidate answer:
{answer}

Evaluate the answer fairly.

Your response must contain exactly these sections:

Score: X/10

What was correct:
- Explain the important correct points.

What could be improved:
- Explain missing, incorrect, or unclear points.

Suggested answer:
- Give a concise answer that would be strong in an interview.

Follow-up question:
- Provide one related question the candidate should prepare for.

The score must be a whole number from 0 to 10.
The first section must begin with this exact format:

Score: X/10
"""

    return ask_model(prompt)


def get_score_color(score):
    if score >= 8:
        return Fore.GREEN

    if score >= 5:
        return Fore.YELLOW

    return Fore.RED


def mock_interview():
    print_section_heading("Mock Interview", Fore.MAGENTA)

    topic = get_non_empty_input(
        "Enter an interview topic, such as Python, SQL, OOP, or DSA: "
    )

    if topic.lower() == "menu":
        return

    print(
        Fore.CYAN
        + "\nType 'menu' instead of an answer to return to the main menu."
    )

    scores = []

    for question_number in range(1, TOTAL_MOCK_QUESTIONS + 1):
        print(
            Fore.MAGENTA
            + Style.BRIGHT
            + f"\nQuestion {question_number} of {TOTAL_MOCK_QUESTIONS}"
        )
        print(Fore.MAGENTA + "-" * 60)

        print(Fore.YELLOW + "Generating question...\n")

        question = generate_mock_question(topic, question_number)

        if question is None:
            print(Fore.RED + "Could not generate the interview question.")
            print(Fore.YELLOW + "The mock interview will now end.")
            break

        print(Fore.WHITE + question)

        answer = get_non_empty_input(
            "\nYour answer, or type 'menu' to stop: "
        )

        if answer.lower() == "menu":
            print(Fore.CYAN + "Returning to the main menu.")
            return

        print(Fore.YELLOW + "\nEvaluating your answer...\n")

        evaluation = evaluate_interview_answer(question, answer)

        if evaluation is None:
            print(Fore.RED + "Could not evaluate this answer.")
            print(Fore.YELLOW + "Moving to the next question.")
            continue

        print_result_heading("Feedback", Fore.MAGENTA)
        print(Fore.WHITE + evaluation)

        score = extract_score(evaluation)

        if score is not None:
            scores.append(score)
            print(Fore.CYAN + f"\nExtracted score: {score}/10")
        else:
            print(
                Fore.YELLOW
                + "\nThe evaluation was displayed, but a valid score was not found."
            )

    if scores:
        total_score = sum(scores)
        overall_score = total_score / len(scores)

        print_result_heading("Mock Interview Complete", Fore.CYAN)
        print(Fore.WHITE + f"Questions scored: {len(scores)} of {TOTAL_MOCK_QUESTIONS}")

        score_color = get_score_color(overall_score)
        print(score_color + f"Overall score: {overall_score:.1f}/10")
    else:
        print(Fore.YELLOW + "\nNo valid scores were available.")

    input("\nPress Enter to return to the main menu...")


def display_menu():
    print("\n" + Fore.CYAN + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "AI INTERVIEW ASSISTANT")
    print(Fore.CYAN + "=" * 60)
    print(Fore.WHITE + "1. Generate Interview Questions")
    print(Fore.WHITE + "2. Explain a Technical Topic")
    print(Fore.WHITE + "3. Mock Interview")
    print(Fore.WHITE + "4. Exit")
    print(Fore.CYAN + "=" * 60)


def main():
    while True:
        display_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            generate_interview_questions()

        elif choice == "2":
            explain_topic()

        elif choice == "3":
            mock_interview()

        elif choice == "4":
            print(
                Fore.GREEN
                + "\nThank you for using AI Interview Assistant."
            )
            print(Fore.CYAN + "Goodbye! Have a nice day.")
            break

        else:
            print(
                Fore.YELLOW
                + "\nInvalid choice. Please select a number from 1 to 4."
            )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n\nApplication closed by user.")