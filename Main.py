import openai
import psycopg2

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Database connection details (Replace with your actual values)
DATABASE_URL = "postgresql://your_user:your_password@your_host:5432/your_database"

def generate_text(prompt):
  """
  Generates text using the OpenAI API.

  Args:
      prompt: The input text for the AI model.

  Returns:
      The AI-generated text, or None if an error occurs.
  """

  try:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()
  except openai.error.OpenAIError as e:
    print(f"Error: {e}")
    return None

def store_interaction(user_input, ai_response):
  """
  Stores user input and AI response in the database.

  Args:
      user_input: The user's input text.
      ai_response: The AI-generated text.
  """

  try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO user_interactions (user_input, ai_response) VALUES (%s, %s)", (user_input, ai_response))
    conn.commit()
    cur.close()
    conn.close()
    print("Interaction stored in database.")
  except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

if __name__ == "__main__":
  while True:
    user_input = input("Enter a prompt for the AI (or 'exit' to quit): ")

    if user_input.lower() == 'exit':
      break

    ai_generated_text = generate_text(user_input)

    if ai_generated_text:
      print(ai_generated_text)
      store_interaction(user_input, ai_generated_text) 
    else:
      print("An error occurred. Please try again.")
