import pandas as pd
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer
import torch

# Define the allowed units (as provided)
entity_unit_map = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'maximum_weight_recommendation': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'imperial gallon', 'litre', 'microlitre', 'millilitre', 'pint', 'quart'}
}

test_df = pd.read_csv('dataset/final_test.csv')


import pandas as pd
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import requests
from io import BytesIO

# Load the model and tokenizer
model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, torch_dtype=torch.float16)
model = model.to(device='cuda:1')
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True)

# Define the function to process each row
def process_row(image_path, extracted_text, prompt):
    try:
        # Load and convert the image
        image = Image.open(image_path).convert('RGB')

        # Prepare the input text
        input_text = f"Extracted text: {extracted_text}\nPrompt: {prompt}"

        msgs = [{'role': 'user', 'content': input_text}]

        # Generate response from the model
        res = model.chat(
            image=image,
            msgs=msgs,
            tokenizer=tokenizer,
            sampling=True,
            temperature=0.7,  
            stream=False
        )


        # Collect the generated response
        generated_text = ""
        for new_text in res:
            generated_text += new_text

        return generated_text.strip()  # Return the final output
    except Exception as e:
        print(f"Error processing row: {e}")
        return ""

# Read the CSV file (input data)
input_csv_path = 'dataset/final_test.csv'
output_csv_path = 'output10000_15000.csv'
test_df = pd.read_csv(input_csv_path)

# Ensure 'easyocr_text' and 'tesseract_text' are strings, replacing NaN with empty strings
test_df['easyocr_text'] = test_df['easyocr_text'].fillna('').astype(str)
test_df['tesseract_text'] = test_df['tesseract_text'].fillna('').astype(str)

# Prepare the prompt for each row
prompt_template = "Identify the {entity_name} from the text and image and output only two words. The unit should be one of {allowed_units}. reply in very short and answer inteligently"

# Initialize the output CSV file
output_df = pd.DataFrame(columns=['index', 'prediction'])
output_df.to_csv(output_csv_path, index=False)

# Iterate over each row in the CSV
for index, row in test_df.iterrows():
    if(index < 10000): continue
    image_names = row['image_name']
    image_path = "/raid/ai23mtech11004/amazon-ml/test_images/" + image_names
    extracted_text = row['easyocr_text'] + " " + row['tesseract_text']  # Combine texts
    entity_name = row['entity_name']
    
    # Define allowed units based on the entity_name
    allowed_units = ", ".join(entity_unit_map.get(entity_name, []))
    
    # Skip if no allowed units are defined for this entity
    if not allowed_units:
        results = {"index": index, "prediction": ""}
    else:
        # Define the prompt based on entity_name
        prompt = prompt_template.format(entity_name=entity_name, allowed_units=allowed_units)
    
        # Process the row to generate the predicted entity_value
        entity_value = process_row(image_path, extracted_text, prompt)
    
        # Append the result
        results = {"index": index, "prediction": entity_value}

    # Append the result to the CSV file incrementally
    result_df = pd.DataFrame([results])
    result_df.to_csv(output_csv_path, mode='a', header=False, index=False)

    # Optional: Print status
    print(f"Processed row {index}")

print(f"Predictions saved to {output_csv_path}")
