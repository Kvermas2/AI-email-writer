from google import genai
from flask import Flask, render_template, request

client = genai.Client(api_key="")

website = Flask(__name__)


@website.route("/main-page", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # Step 1: Get what the user typed
        user_text = request.form["prompt"]

        # Step 2: Find out which button was clicked
        action = request.form["action"]

        # ==========================
        # GENERATE BUTTON
        # ==========================
        if action == "generate":

            # Check if the user entered anything
            if not user_text.strip():
                return render_template(
                    "index.html",
                    result="",
                    prompt="",
                    message="Please enter something."
                )

            # Build the AI prompt
            prompt = f"""
You are an expert professional email writer.

Write a complete email based on the user's request.

Rules:
- Write only ONE email.
- Don't give multiple options.
- Don't explain your answer.
- Use a professional tone unless the user asks for a casual one.
- Include a subject line.
- Make the email clear and well formatted.

User Request:
{user_text}
"""

            # Send it to Gemini
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            # Show the generated email
            return render_template(
                "index.html",
                result=response.text,
                prompt=user_text,
                message=""
            )

        # ==========================
        # CLEAR BUTTON
        # ==========================
        elif action == "clear":
            return render_template(
                "index.html",
                result="",
                prompt="",
                message=""
            )

    # First time opening the website
    return render_template(
        "index.html",
        result="",
        prompt="",
        message=""
    )


@website.route("/about")
def about():
    return "This website is made by Kriday!"


if __name__ == "__main__":
    website.run(debug=True)