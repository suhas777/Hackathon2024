from flask import Flask, request, jsonify
from google.cloud import dlp_v2
import json

app = Flask(__name__)

# Initialize DLP client
dlp_client = dlp_v2.DlpServiceClient()

# Set your Google Cloud project ID
PROJECT_ID = '' #Project ID

# Define template names
INSPECT_TEMPLATE_NAME = 'projects/{project-id}/locations/global/inspectTemplates/hacky_template'.format(PROJECT_ID)
DEIDENTIFY_TEMPLATE_NAME = 'projects/{project-id}/locations/global/deidentifyTemplates/Sensitive_Info_DeId'.format(PROJECT_ID)

# Route to de-identify JSON data
@app.route('/deidentify-json', methods=['POST'])
def deidentify_json():
    # Read JSON content from request body
    json_data = request.json

    # Convert JSON to string
    json_str = json.dumps(json_data)

    # Construct the item to de-identify
    item = {'value': json_str}

    # Call the DLP API to de-identify the content
    response = dlp_client.deidentify_content(
        request={
            'parent': f'projects/{PROJECT_ID}',
            'inspect_template_name': INSPECT_TEMPLATE_NAME,
            'deidentify_template_name': DEIDENTIFY_TEMPLATE_NAME,
            'item': item
        }
    )

    # Convert the de-identified string back to JSON
    deidentified_json = json.loads(response.item.value)

    return jsonify(deidentified_json)

if __name__ == '__main__':
    app.run(debug=True)