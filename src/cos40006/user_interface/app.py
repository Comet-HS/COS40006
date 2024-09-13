from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data
# Replace with a database (suggestion: sqlite)
reminders = [
    "Monday 9 am: Take vitamin tablets",
    "Tuesday 12 noon: See doctor"
]

# initialization
@app.route('/')
def index():
    return render_template('index.html', reminders=reminders)

# route to add new reminder. Currently only updating a list!!
@app.route('/new_reminder', methods=['POST'])
def new_reminder():
    new_task = request.form.get('new_reminder')
    if new_task:
        reminders.append(new_task)
    return redirect(url_for('index'))


# A Placeholder form to communicate with an LLM
# Currently only prints the mressage received into the terminal
@app.route('/ask_assistant', methods=['POST'])
def ask_assistant():
    question = request.form.get('assistant_question')
    print(f"Assistant question received: {question}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
