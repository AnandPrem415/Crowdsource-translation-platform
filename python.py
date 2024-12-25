from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for translations
class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.String(200), nullable=False)
    translated_text = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Translation {self.source_text} -> {self.translated_text}>"

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_translation():
    source_text = request.form['source_text']
    translated_text = request.form['translated_text']
    language = request.form['language']

    new_translation = Translation(source_text=source_text, translated_text=translated_text, language=language)
    db.session.add(new_translation)
    db.session.commit()

    return jsonify({"message": "Translation submitted successfully!"})

@app.route('/translations', methods=['GET'])
def get_translations():
    translations = Translation.query.all()
    return jsonify([{"source_text": t.source_text, "translated_text": t.translated_text, "language": t.language} for t in translations])

if __name__ == '__main__':
    app.run(debug=True)