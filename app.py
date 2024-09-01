from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# Route for the login page
@app.route('/')
def login():
    return render_template('index.html')

# Route for the home page after login
@app.route('/home')
def home():
    # This should be protected, ensure a user is logged in before rendering this
    return render_template('home.html')

# Route for handling login
@app.route('/do-login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Simple authentication logic
    if username == 'admin' and password == 'password':
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

# Route for handling retrofitting recommendations
@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    building_type = data['building_type']
    building_size = data['building_size']
    energy_usage = int(data['energy_usage'])  # Convert energy_usage to an integer

    recommendations = []
    message = ""

    # Define threshold values for each building type and size
    thresholds = {
        "residential": {
            "small": 1500,
            "medium": 3000,
            "large": 5000
        },
        "commercial": {
            "small": 5000,
            "medium": 10000,
            "large": 20000
        }
    }

    # Get the relevant threshold based on building type and size
    threshold = thresholds[building_type][building_size]

    # Check if the current energy usage exceeds or is below the threshold
    if energy_usage > threshold:
        message = f"<strong style='color: red;'>Warning:</strong> Your energy usage of {energy_usage} kWh/month exceeds the recommended threshold of {threshold} kWh/month for a {building_size} {building_type} building. Consider taking immediate actions to reduce energy consumption."
        recommendations.append("Reduce usage of high-energy appliances during peak hours.")
        recommendations.append("Consider upgrading to energy-efficient appliances.")
        recommendations.append("Implement energy management systems to monitor and optimize usage.")
    else:
        message = f"<strong style='color: green;'>Great job!</strong> Your energy usage of {energy_usage} kWh/month is within the recommended threshold of {threshold} kWh/month for a {building_size} {building_type} building. Keep up the good work!"
    
    # Add additional recommendations based on building type and size
    if building_type == "residential":
        if building_size == "small":
            recommendations += ["Install LED lighting", "Add insulation", "Consider solar panels"]
        elif building_size == "medium":
            recommendations += ["Upgrade HVAC system", "Install smart thermostats", "Increase insulation"]
        elif building_size == "large":
            recommendations += ["Install solar panels", "Upgrade to energy-efficient windows", "Consider geothermal heating"]
    elif building_type == "commercial":
        if building_size == "small":
            recommendations += ["Implement energy management systems", "Upgrade lighting to LED", "Improve insulation"]
        elif building_size == "medium":
            recommendations += ["Consider solar panels", "Install high-efficiency HVAC", "Implement building automation"]
        elif building_size == "large":
            recommendations += ["Optimize HVAC systems", "Invest in renewable energy", "Install advanced building management systems"]

    # Return the message and recommendations as JSON
    return jsonify(message=message, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
