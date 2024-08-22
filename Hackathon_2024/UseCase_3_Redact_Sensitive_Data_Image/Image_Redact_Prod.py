from google.cloud import dlp_v2
from google.cloud.dlp_v2 import types
import base64

def redact_image(project_id, image_path, output_path):
    # Initialize the DLP client
    dlp_client = dlp_v2.DlpServiceClient()

    # Read the image file
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Convert the image to base64
    image_base64 = base64.b64encode(image_data).decode("utf-8")

    # Specify the info types to redact
    info_types = [{"name": "PHONE_NUMBER"},{"name": "EMAIL_ADDRESS"}, {"name": "INDIA_AADHAAR_INDIVIDUAL"},{"name": "INDIA_PAN_INDIVIDUAL"}]

    # Construct the request
    inspect_config = {"info_types": info_types}
    byte_item = {"type_": types.ByteContentItem.BytesType.IMAGE_PNG, "data": image_data}

    response = dlp_client.redact_image(
        request={
            "parent": f"projects/{project_id}",
            "inspect_config": inspect_config,
            "byte_item": byte_item,
        }
    )

    # Write the redacted image to the output path
    with open(output_path, "wb") as output_file:
        output_file.write(response.redacted_image)

    print(f"Redacted image saved to {output_path}")

# Usage example
project_id = "" #project-id
image_path = "" #path to image
output_path = "" #output path

redact_image(project_id, image_path, output_path)