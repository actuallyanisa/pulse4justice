from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'admin@pulseforjustice.org'
app.config['MAIL_PASSWORD'] = 'PulseForJusticeColdEmail10!'  # Use app password or env var!

mail = Mail(app)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict(flat=False)

    title = data.get('title', [''])[0]
    category = data.get('category', [''])[0]
    goal = data.get('goal', [''])[0]
    location = data.get('location', [''])[0]
    beneficiary = data.get('beneficiary', [''])[0]

    gender = data.get('gender', [''])[0]
    race = data.get('race', [''])[0]
    sexualOrientation = data.get('sexualOrientation', [''])[0]
    disabilities = data.get('disabilities', [''])[0]
    otherInfo = data.get('otherInfo', [''])[0]

    paypal = data.get('paypal', [''])[0]

    organizerName = data.get('organizerName', [''])[0]
    organizerEmail = data.get('organizerEmail', [''])[0]
    organizerPhone = data.get('organizerPhone', [''])[0]
    relationship = data.get('relationship', [''])[0]

    story = data.get('story', [''])[0]

    items = data.get('item[]', [])
    descriptions = data.get('description[]', [])
    costs = data.get('cost[]', [])

    wishlist_text = ""
    for i in range(len(items)):
        item = items[i] if i < len(items) else ''
        desc = descriptions[i] if i < len(descriptions) else ''
        cost = costs[i] if i < len(costs) else ''
        wishlist_text += f" - {item}: {desc}, Estimated cost: {cost}\n"
    if not wishlist_text:
        wishlist_text = "No wishlist items provided."

    email_body = f"""
New Fundraiser Submission:

Title: {title}
Category: {category}
Fundraising Goal: {goal}
Location: {location}
Beneficiary: {beneficiary}

Personal Details:
- Gender: {gender}
- Race/Ethnicity: {race}
- Sexual Orientation: {sexualOrientation}
- Disabilities or Accessibility Needs: {disabilities}
- Other Info: {otherInfo}

PayPal Email: {paypal}

Organizer Information:
- Name: {organizerName}
- Email: {organizerEmail}
- Phone: {organizerPhone}
- Relationship to Beneficiary: {relationship}

Wishlist:
{wishlist_text}

Story:
{story}
    """

    try:
        msg = Message(
            subject="New Fundraiser Submission",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=email_body
        )
        mail.send(msg)
        return redirect(url_for('home'))  # Redirect to home page after successful submit
    except Exception as e:
        return f"Failed to send email: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
