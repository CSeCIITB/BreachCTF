from flask import Flask, request, jsonify, render_template_string, send_from_directory
import subprocess
import os
import uuid

app = Flask(__name__, static_url_path='/static', static_folder='static')

FLAG = "Breach{c0mb1n4to1c5_b3t73r_th4n_DP}"

SUBMISSIONS_DIR = "/tmp/submissions"
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)

submission_page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CTF PPC Challenge Submission (C++)</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f9;
      margin: 0;
      padding: 20px;
    }
    h1 {
      text-align: center;
      color: #333;
    }
    form {
      background-color: #fff;
      max-width: 600px;
      margin: 20px auto;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    label {
      font-weight: bold;
      margin-top: 10px;
      display: block;
    }
    textarea, input[type="file"] {
      width: 100%;
      margin-top: 5px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }
    input[type="submit"] {
      background-color: #5cb85c;
      color: white;
      border: none;
      padding: 10px 20px;
      text-transform: uppercase;
      cursor: pointer;
      border-radius: 4px;
      margin-top: 10px;
    }
    input[type="submit"]:hover {
      background-color: #4cae4c;
    }
    p {
      text-align: center;
    }
    a {
      color: #0275d8;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <h1>Submit Your C++ Code</h1>
  <form action="/submit" method="POST" enctype="multipart/form-data">
    <label for="code">Paste your C++ code here:</label>
    <textarea id="code" name="code" rows="15" placeholder="Paste your C++ code here"></textarea>

    <input type="submit" value="Submit">
  </form>
  <p><a href="/static/CTF-Cater_the_food.pdf" target="_blank">View Question PDF</a></p>
</body>
</html>

"""

@app.route("/")
def index():
    return render_template_string(submission_page)

@app.route("/submit", methods=["POST"])
def submit():
    code = request.form.get("code")
    if not code:
        return jsonify({"status": "error", "message": "No code provided"}), 400

    submission_id = str(uuid.uuid4())
    submission_path = os.path.join(SUBMISSIONS_DIR, f"{submission_id}.cpp")
    with open(submission_path, "w") as f:
        f.write(code)

    # Copy the submission file to a writable location (/home/runner/submission.cpp)
    os.system(f"cp {submission_path} /home/runner/submission.cpp")

    try:
        result = subprocess.run(
            ["/run_submission.sh"],
            capture_output=True,
            text=True,
            timeout=120
        )
    except subprocess.TimeoutExpired:
        os.remove(submission_path)
        return jsonify({"status": "error", "message": "Execution timed out"}), 400

    # os.remove(submission_path)

    if "ALL TESTS PASSED" in result.stdout:
        return jsonify({"status": "success", "flag": FLAG})
    else:
        return jsonify({
            "status": "fail",
            "message": "One or more test cases failed",
            "debug_output": result.stdout.strip()
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
