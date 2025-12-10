from flask import Flask, render_template, request
from cs50 import SQL

app = Flask(__name__)

# Prompt database
db = SQL("sqlite:///finance.db")


@app.route("/", methods=["GET", "POST"])
def index():

    queries = [
        {"id": 1, "prompt": "Which company had the strongest revenue growth?"},
        {"id": 2, "prompt": "Describe the net income trends."},
        {"id": 3, "prompt": "Which company had the most asset growth?"},
        {"id": 4, "prompt": "Which company managed liabilities most effectively?"},
        {"id": 5, "prompt": "How did operating cash flow trends align with net income?"},
        {"id": 6, "prompt": "How were the company margins?"},
        {"id": 7, "prompt": "How were the return on assets?"},
        {"id": 8, "prompt": "How did each company's debt to asset ratio change?"},
        {"id": 9, "prompt": "How consistent or volatile was each company?"},
        {"id": 10, "prompt": "Describe each company's growth over time."},
        {"id": 11, "prompt": "Describe the risk of each company."},
        {"id": 12, "prompt": "How is the future outlook for each company?"},
        {"id": 13, "prompt": "How efficient was the revenue growth for each company?"},
        {"id": 14, "prompt": "How was each company's debt leveraged?"},
        {"id": 15, "prompt": "How sustainable was each company's cash flow?"}
    ]

    responses = [
        {"id": 1, "response": "Microsoft Corporation experienced 22% revenue growth from 2022-2024."},
        {"id": 2, "response": "Microsoft’s profits grew 21.8% in 2024 while revenue rose 15.7%, keeping a strong net margin of about 34%. Apple’s profits fell 3.4% with margin slipping from 25% to 24%, and Tesla’s profits collapsed 52.3% with net margin dropping from 15.5% to 7.3%."},
        {"id": 3, "response": "Tesla, Inc. experienced 44% asset growth from 2022-2024."},
        {"id": 4, "response": "Apple kept liabilities under control (net 2.2% growth), Microsoft’s rose with growth (22.2%), Tesla’s liabilities grew quickly (30.5%)."},
        {"id": 5, "response": "Microsoft’s cash flow matched its profit growth (33.8% growth), Apple was mixed (2.5% decrease), Tesla’s cash flow rose even as profits fell (2.6% increase)."},
        {"id": 6, "response": "Microsoft kept the healthiest margins (25% to 24%), Apple slipped slightly (36.7% to 34%), Tesla’s margins halved (15.5% to 7.3%)."},
        {"id": 7, "response": "Apple used assets most effectively (0.283 to 0.257), Microsoft was steady (0.199 to 0.172), Tesla’s efficiency dropped sharply (0.153 to 0.059)."},
        {"id": 8, "response": "All three reduced debt reliance, with Microsoft and Tesla showing the biggest improvements.\nApple: 0.856 to 0.844\nMicrosoft: 0.544 to 0.476\nTesla: 0.443 to 0.396"},
        {"id": 9, "response": "Microsoft was steady, Apple was flat (mostly stable), and Tesla was volatile."},
        {"id": 10, "response": "Microsoft’s growth carried forward (grew bother years), Apple stabilized (declined, then mild rebound), Tesla reversed course (strong in 2023, weak in 2024)."},
        {"id": 11, "response": "Microsoft looks safest (dropped debt ratio), Apple carries more debt (high debt ratio), Tesla’s profit drop is risky (debt ratio dropped but profit collapsed)."},
        {"id": 12, "response": "Microsoft is best positioned, Apple is steady, Tesla faces challenges."},
        {"id": 13, "response": "Microsoft turned growth into bigger profits, Apple didn’t, Tesla lost efficiency."},
        {"id": 14, "response": "Microsoft and Tesla reduced debt reliance, Apple stayed heavily leveraged."},
        {"id": 15, "response": "Microsoft’s cash flow growth looks most sustainable (cash flow surge), Apple is mixed (fell 9.5% then rose 7%), Tesla’s cash flow rise may not last (rose 12.6% in 2024)."}
    ]

    if request.method == "GET":
        return render_template("index.html", queries=queries)

    elif request.method == "POST":

        prompt_id = int(request.form.get("query"))
        prompt = ""
        response = ""

        for query in queries:
            if query["id"] == prompt_id:
                prompt = query["prompt"]

        print("Prompt: " + prompt)

        # Check prompt
        if not prompt:
            response = "Error: prompt not found"
            print(response)

        # Add prompt to database
        db.execute("INSERT INTO prompts (prompt) VALUES (?)", prompt)

        # Get the chatbot's response
        for reply in responses:
            if reply["id"] == prompt_id:
                response = reply["response"]

        # Render the page
        return render_template("prompt.html", queries=queries, response=response)


@app.route("/history")
def history():

    # Get prompts from database
    history = db.execute("SELECT * FROM prompts;")
    print(history)

    return render_template("history.html", history=history)
