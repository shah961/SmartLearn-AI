from flask import Flask, request
from google import genai
import os
import markdown

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=API_KEY)

# Shared HTML Header to avoid repeating CSS styles
HTML_HEADER = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartLearn AI Agent</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --primary: #38bdf8;
            --primary-hover: #0ea5e9;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .container {
            width: 100%;
            max-width: 600px;
            margin-top: 40px;
            text-align: center;
        }

        h1 {
            color: var(--primary);
            font-size: 2.2rem;
            margin-bottom: 10px;
            font-weight: 800;
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 1rem;
            margin-bottom: 30px;
        }

        /* Form & Input Styles */
        .search-box {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid #334155;
        }

        input[type="text"] {
            width: 100%;
            padding: 14px 18px;
            border-radius: 10px;
            border: 2px solid #334155;
            background-color: #0f172a;
            color: white;
            font-size: 1rem;
            margin-bottom: 15px;
            outline: none;
            transition: border-color 0.2s;
        }
        select {
            width: 100%;
            padding: 14px 18px;
            border-radius: 10px;
            border: 2px solid #334155;
            background-color: #0f172a;
            color: white;
            font-size: 1rem;
            margin-bottom: 15px;
            outline: none;
        }

        select:focus {
            border-color: var(--primary);
        }
        input[type="text"]:focus {
            border-color: var(--primary);
        }

        button {
            width: 100%;
            padding: 14px;
            background-color: var(--primary);
            color: #0f172a;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
        }

        button:hover {
            background-color: var(--primary-hover);
        }

        button:active {
            transform: scale(0.98);
        }

        /* AI Content Formatting (Markdown Output) */
        .content-card {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 16px;
            text-align: left;
            margin-top: 20px;
            border: 1px solid #334155;
            line-height: 1.7;
        }

        .content-card h1, .content-card h2, .content-card h3 {
            color: var(--primary);
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .content-card p {
            margin-bottom: 15px;
            color: #e2e8f0;
        }

        .content-card ul, .content-card ol {
            margin-left: 20px;
            margin-bottom: 15px;
            color: #e2e8f0;
        }

        .content-card li {
            margin-bottom: 8px;
        }

        /* Code block styling for mobile */
        .content-card pre {
            background: #0f172a;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 15px;
            border: 1px solid #334155;
        }

        .content-card code {
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9rem;
        }

        .back-link {
            display: inline-block;
            margin-top: 25px;
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
        }

        .back-link:hover {
            text-decoration: underline;
        }
        .pdf-btn{
            margin-bottom:15px;
        }

        @media print{
            .pdf-btn,
            .back-link{
                display:none;
            }
        }
        #loading{
            text-align:center;
            margin-top:15px;
            color:#38bdf8;
            font-weight:bold;
        }
        .content-card table{
            width:100%;
            border-collapse:collapse;
            margin:15px 0;
        }

        .content-card th,
        .content-card td{
            border:1px solid #334155;
            padding:10px;
        }

        .content-card th{
            background:#0f172a;
        }
    </style>
</head>
"""

@app.route("/")
def home():
    return f"""
    {HTML_HEADER}
    <body>
        <div class="container">
            <h1>SmartLearn AI </h1>
            <p class="subtitle">
Learn Faster.
Remember Longer.
Study Smarter.</p>

            <div class="search-box">
                <form action="/ask" method="get">
                    <input
                        type="text"
                        name="question"
                        placeholder="What do you want to learn today?"
                        required
                        autofocus
                    >
                    <select name="subject" required>
    <option value="" disabled selected>Select Subject</option>
    <option value="General">General</option>
    <option value="Programming">Programming</option>
    <option value="Mathematics">Mathematics</option>
    <option value="Physics">Physics</option>
    <option value="Chemistry">Chemistry</option>
    <option value="Biology">Biology</option>
</select>

<br><br>

<select name="difficulty" required>
   <option value="" disabled selected>Select Difficulty</option>
    <option value="Beginner">Beginner</option>
    <option value="Intermediate">Intermediate</option>
    <option value="Advanced">Advanced</option>
</select>

<br><br>

<select name="goal" required>
    <option value="" disabled selected>Select Goal</option>
    <option value="Exam Preparation">Exam Preparation</option>
    <option value="Quick Learning">Quick Learning</option>
    <option value="Interview Prep">Interview Prep</option>
    <option value="Revision">Revision</option>
</select>

<br><br>
                    <button type="submit" id="askBtn">
    Ask AI Partner
</button>
                </form>
                <p id="loading" style="display:none;">
🧠 AI is creating your lesson...
This may take a few seconds.
</p>
            </div>
        </div>
        <script>
document.querySelector("form").addEventListener("submit", function(){{
    document.getElementById("loading").style.display = "block";
    document.getElementById("askBtn").disabled = true;
    document.getElementById("askBtn").innerText = "Generating...";
}});
</script>
    </body>
    </html>
    """


            
@app.route("/ask")
def ask():
    question = request.args.get("question")
    subject = request.args.get("subject")
    difficulty = request.args.get("difficulty")
    goal = request.args.get("goal")

    if not question or not question.strip():
        return """
        <h1>Error</h1>
        <p>Please enter a topic.</p>
        """

    if not subject or not difficulty or not goal:
        return """
        <h1>Error</h1>
        <p>Please complete all fields.</p>
        """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are SmartLearn AI Agent.

Subject: {subject}
Difficulty Level: {difficulty}
Learning Goal: {goal}
Topic: {question}

Teach according to the selected difficulty level.

Beginner:
- Very simple language
- Everyday examples

Intermediate:
- More details
- Some technical terms

Advanced:
- Deep explanation
- Professional terminology

Provide:

# Short Explanation

# Key Points

# Quiz Questions
(3 questions)

# 30 Minute Study Plan
# Knowledge Gap Analysis

- Common mistakes
- Difficult concepts
- Recommended next topics
# Flashcards
Use proper markdown formatting.

For flashcards use:

Flashcard 1

Question:
...

Answer:
...

Flashcard 2

Question:
...

Answer:
...

# Revision Notes

# Summary

Give a short 5-line summary.

Use markdown headings.
Use tables when useful.
Highlight important terms in bold.
Keep the complete response under 600 words.
Use concise explanations.
Avoid long paragraphs.
End with a motivational study tip.
"""
        )

    except Exception as e:
        return f"""
        {HTML_HEADER}
        <body>
            <div class="container">
                <h1>⚠️ Error</h1>

                <div class="content-card">
                    <p>Something went wrong while contacting Gemini.</p>
                    <p>{str(e)}</p>
                </div>

                <a href="/" class="back-link">
                    ← Try Again
                </a>
            </div>
        </body>
        </html>
        """

    response_text = getattr(response, "text", "")

    if not response_text or not response_text.strip():
        return """
        <h1>Error</h1>
        <p>No response received from AI.</p>
        """

    html_response = markdown.markdown(
        response_text,
        extensions=["extra"]
    )

    return f"""
    {HTML_HEADER}
    <body>
        <div class="container">

            <h1>SmartLearn AI </h1>

            <p class="subtitle">
                Subject: {subject} |
                Level: {difficulty} |
                Goal: {goal}
            </p>

            <div class="content-card" id="studyContent">
<button onclick="copyContent()" class="pdf-btn">
📋 Copy Notes
</button>
                {html_response}

            </div>

            <a href="/" class="back-link">
                ← Teach me something else
            </a>

        </div>
        <script>
function copyContent() {{
    const content =
        document.getElementById("studyContent").innerText;

    navigator.clipboard.writeText(content);

    alert("Content copied!");
}}
</script>
    </body>
    </html>
    """


@app.route("/study")
def study():
    return f"""
    {HTML_HEADER}
    <body>
        <div class="container">
            <h1>Study Route Working </h1>
            <p class="subtitle">AI features are now being added...</p>
            
            <a href="/" class="back-link">← Go Back</a>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
    