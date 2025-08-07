import matplotlib.pyplot as plt
import re

def extract_numbers(text):
    # Finds all sequences of numbers separated by commas
    matches = re.findall(r'(\d+(?:\.\d+)?(?:,\s*\d+(?:\.\d+)?)*)', text)
    if len(matches) >= 2:
        x = [float(i) for i in matches[0].replace(" ", "").split(",")]
        y = [float(i) for i in matches[1].replace(" ", "").split(",")]
        return x, y
    return None, None

def draw_graph(x, y):
    plt.plot(x, y, marker='o')
    plt.title("Your Graph")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.show()

def chatbot():
    print("Hi! Describe the data you want to plot. Example: 'Plot 1,2,3,4 against 10,20,25,30'")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        x, y = extract_numbers(user_input)
        if x and y:
            draw_graph(x, y)
        else:
            print("Sorry, I couldn't understand. Try: 'Plot 1,2,3,4 against 10,20,25,30' or 'Draw a graph for 1,2,3 and 4,5,6'")

if __name__ == "__main__":
    chatbot()