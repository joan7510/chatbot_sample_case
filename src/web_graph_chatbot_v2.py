from flask import Flask, request, render_template_string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import re

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Graph Chatbot</title>
<h2>Describe the data you want to plot:</h2>
<form method="post">
  <input name="user_input" style="width:400px" placeholder="Plot 1,2,3,4 against 10,20,25,30">
  <br><br>
  <label for="graph_type">Choose graph type:</label>
  <select name="graph_type" id="graph_type">
    <option value="line">Line Chart</option>
    <option value="bar">Bar Chart</option>
    <option value="scatter">Scatter Plot</option>
  </select>
  <br><br>
  <input type="checkbox" name="fit_line" id="fit_line">
  <label for="fit_line">Add fitted line</label>
  <br><br>
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

def plot_to_base64(x, y, graph_type, fit_line):
    plt.figure()
    if graph_type == "line":
        plt.plot(x, y, marker='o', label="Line")
    elif graph_type == "bar":
        plt.bar(x, y, label="Bar")
    elif graph_type == "scatter":
        plt.scatter(x, y, label="Scatter")
    else:
        plt.plot(x, y, marker='o', label="Line")
    # Add fitted line if requested
    if fit_line and len(x) > 1:
        coeffs = np.polyfit(x, y, 1)
        fit_y = np.polyval(coeffs, x)
        plt.plot(x, fit_y, color='red', linestyle='--', label="Fitted Line")
    plt.title("Your Graph")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.legend()
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
        graph_type = request.form.get("graph_type", "line")
        fit_line = request.form.get("fit_line") == "on"
        x, y = extract_numbers(user_input)
        if x and y:
            graph = plot_to_base64(x, y, graph_type, fit_line)
        else:
            error = "Sorry, I couldn't understand. Try: 'Plot 1,2,3,4 against 10,20,25,30'"
    return render_template_string(HTML, graph=graph, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    # To run on a different port, change the port number here
    # app.run(debug=True, port=5001)  # Uncomment to run on port