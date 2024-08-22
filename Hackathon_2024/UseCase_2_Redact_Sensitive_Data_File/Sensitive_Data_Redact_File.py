from flask import Flask, request, jsonify
from google.cloud import dlp_v2

app = Flask(__name__)

# Initialize the DLP client
dlp_client = dlp_v2.DlpServiceClient()

# Set your Google Cloud project ID
PROJECT_ID = '' #Project-ID

# Define the de-identify template name
DEIDENTIFY_TEMPLATE_NAME = 'projects/{project-id}/locations/global/deidentifyTemplates/Redact_Demo'.format(PROJECT_ID)

# Route to redact sensitive data from text
@app.route('/redact-text', methods=['POST'])
def redact_text():
    # Read text content from request body
    text_to_redact = request.data.decode('utf-8')

    # Construct the item to de-identify
    item = {'value': text_to_redact}

    # Call the DLP API to de-identify (redact) the content
    response = dlp_client.deidentify_content(
        request={
            'parent': f'projects/{PROJECT_ID}',
            'deidentify_template_name': DEIDENTIFY_TEMPLATE_NAME,
            'item': item
        }
    )

    # Get the redacted text
    redacted_text = response.item.value

    return jsonify({'redacted_text': redacted_text})

if __name__ == '__main__':
    app.run(debug=True)