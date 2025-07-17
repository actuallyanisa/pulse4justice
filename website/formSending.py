from flask import Flask, request, render_template_string
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure your email
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rohini@pulseforjustice.org'
app.config['MAIL_PASSWORD'] = 'PulseForJusticeColdEmail10!'  # Use the app password here

mail = Mail(app)

@app.route('/')
def form():
    return render_template_string(open("templates/form.html").read())

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict(flat=False)  # to handle multiple entries, like wishlist arrays

    # Extract fields safely
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

    ngo = data.get('ngo', [''])[0]
    paypal = data.get('paypal', [''])[0]

    organizerName = data.get('organizerName', [''])[0]
    organizerEmail = data.get('organizerEmail', [''])[0]
    organizerPhone = data.get('organizerPhone', [''])[0]
    relationship = data.get('relationship', [''])[0]

    description = data.get('description', [''])[0]
    story = data.get('story', [''])[0]

    # Wishlist arrays
    items = data.get('item[]', [])
    descriptions = data.get('description[]', [])
    costs = data.get('cost[]', [])

    wishlist_text = ""
    for i in range(len(items)):
        item = items[i] if i < len(items) else ''
        desc = descriptions[i] if i < len(descriptions) else ''
        cost = costs[i] if i < len(costs) else ''
        wishlist_text += f" - {item}: {desc}, Estimated cost: {cost}\n"

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

Partner NGO: {ngo}
PayPal Email: {paypal}

Organizer Information:
- Name: {organizerName}
- Email: {organizerEmail}
- Phone: {organizerPhone}
- Relationship to Beneficiary: {relationship}

Wishlist:
{wishlist_text if wishlist_text else "No wishlist items provided."}

Story:
Short Description: {description}

Full Story:
{story}
    """

    msg = Message(
        subject="New Fundraiser Submission",
        sender=app.config['MAIL_USERNAME'],
        recipients=["rohini@pulseforjustice.org"],
        body=email_body
    )

    mail.send(msg)
    return "Form submitted successfully!"
