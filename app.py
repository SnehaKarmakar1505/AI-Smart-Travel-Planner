from flask import Flask, render_template, request
from google import genai
import os

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not found")

client = genai.Client(api_key=api_key)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/planner")
def planner():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    destination = request.form["destination"]
    days = request.form["days"]
    budget = request.form["budget"]
    travel_type = request.form["travel_type"]

    prompt = f"""
    Create a professional travel itinerary.

    Destination: {destination}
    Number of Days: {days}
    Budget: {budget}
    Travel Type: {travel_type}

    Include:
    1. Day-wise itinerary
    2. Budget breakdown
    3. Best places to visit
    4. Local food recommendations
    5. Packing suggestions

    Format nicely.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    result = response.text

    return render_template(
        "index.html",
        itinerary=result
    )

if __name__ == "__main__":
    app.run(debug=True)