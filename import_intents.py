import csv
import os
from google.cloud import dialogflow_v2 as dialogflow

# Set your environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/risha/.vscode/Projects/AI Chat-bot/MC-Dialogflow-API-Key.json"

def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    # Define training phrases
    training_phrases = [
        dialogflow.Intent.TrainingPhrase(parts=[dialogflow.Intent.TrainingPhrase.Part(text=part)])
        for part in training_phrases_parts
    ]

    # Define message texts (responses)
    message = dialogflow.Intent.Message(text=dialogflow.Intent.Message.Text(text=message_texts))

    # Create the intent
    intent = dialogflow.Intent(
        display_name=display_name[:40],  # Ensure name is <= 40 chars
        training_phrases=training_phrases,
        messages=[message],
    )

    try:
        response = client.create_intent(request={"parent": parent, "intent": intent})
        print(f"Intent created: {response.name}")
    except Exception as e:
        print(f"Error creating intent '{display_name}': {e}")

def import_from_csv(project_id, csv_file_path):
    with open(csv_file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row['QUESTION'].strip()
            answer = row['ANSWER'].strip()

            print(f"Processing: {question}")
            create_intent(
                project_id=project_id,
                display_name=question[:40],  # Truncate to avoid length issues
                training_phrases_parts=[question],
                message_texts=[answer]
            )

def main():
    project_id = input("Enter your Google Cloud Project ID: ")

    # Only process the second CSV
    csv_file_path = os.path.join(os.getcwd(), 'MasterChief - AIChat2.csv')

    if os.path.exists(csv_file_path):
        print(f"Importing from MasterChief - AIChat2.csv...")
        import_from_csv(project_id, csv_file_path)
    else:
        print("File not found: MasterChief - AIChat2.csv")

if __name__ == "__main__":
    main()
