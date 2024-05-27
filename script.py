from flask import Flask, render_template, jsonify
import json
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = ""

# Function to read profiles from JSON files
def read_profiles(file_path):
    with open(file_path, 'r') as file:
        profiles_data = json.load(file)
    return profiles_data

# Function to generate response using OpenAI API
def generate_response(customers_data, sales_reps_data):
    # Format customer and sales rep profiles for the prompt
    customers_prompt = "\n".join([f"- {customer['name']}: {customer['age']} years old, {customer['occupation']}, interests in {', '.join(customer['interests'])}." for customer in customers_data['customers']])
    sales_reps_prompt = "\n".join([f"- {sales_rep['name']}: {sales_rep['age']} years old, {sales_rep['occupation']}, interests in {', '.join(sales_rep['interests'])}." for sales_rep in sales_reps_data['sales_reps']])

    # Define the prompt using the formatted profiles
    prompt = f"""
    Prompt: Describe the characteristics of the customers and sales reps. Ask GPT-3.5 to find common interests between them or suggest potential buyers for the sales reps.

    Customers:
    {customers_prompt}

    Sales Reps:
    {sales_reps_prompt}

    Common Interests or Potential Buyers:
    """

    # Call the OpenAI API to generate the response
    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "system", "content": prompt}],
      max_tokens=150
    )
    print(response)

    generated_text = response.choices[0].message.content.strip()

    return generated_text

# Route to display the response in an HTML table
@app.route('/')

def index():
    # Read customer and sales rep profiles from JSON files
    customers_data = read_profiles("customer.json")
    sales_reps_data = read_profiles("buyer.json")
    
    # Generate response using OpenAI API
    response = generate_response(customers_data, sales_reps_data)

    # Convert the response into a list of rows
    rows = response.split("\n")
    table_data = [row.split(":") for row in rows]

    return render_template('table.html', table_data=table_data, customers=customers_data['customers'], sales_reps=sales_reps_data['sales_reps'])

if __name__ == '__main__':
    app.run(debug=True)
