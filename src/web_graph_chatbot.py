from flask import Flask, request, render_template_string
import matplotlib.pyplot as plt
import io
import base64
import re
import matplotlib
matplotlib.use('Agg')  # For GUI environments (will show window, but can save images)


app = Flask(__name__)

HTML = """
<!doctype html>
<title>Graph Chatbot</title>
<h2>Describe the data you want to plot:</h2>
<form method="post">
  <input name="user_input" style="width:400px" placeholder="Plot 1,2,3,4 against 10,20,25,30">
  <input type="submit">
</form>
{% if graph %}
  <h3>Your Graph:</h3>
  <img src="data:image/png;base64,{{ graph }}">
{% elif error %}
  <p style="color:red;">{{ error }}</p>
{% endif %}
"""

def extract_numbers(text):
    matches = re.findall(r'(\d+(?:\.\d+)?(?:,\s*\d+(?:\.\d+)?)*)', text)
    if len(matches) >= 2:
        x = [float(i) for i in matches[0].replace(" ", "").split(",")]
        y = [float(i) for i in matches[1].replace(" ", "").split(",")]
        return x, y
    return None, None

def plot_to_base64(x, y):
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title("Your Graph")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route("/", methods=["GET", "POST"])
def home():
    graph = None
    error = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        x, y = extract_numbers(user_input)
        if x and y:
            graph = plot_to_base64(x, y)
        else:
            error = "Sorry, I couldn't understand. Try: 'Plot 1,2,3,4 against 10,20,25,30'"
    return render_template_string(HTML, graph=graph, error=error)

if __name__ == "__main__":
    app.run(debug=True,
               port=5001)  # Changed port to 5001 to avoid conflict with other services