import openai
from PIL import Image
import pytesseract
import pyheif
import os
import csv
import hashlib
import base64
from pathlib import Path

# Path for storing the encoded API key
key_file_path = Path.home() / '.openai_key'

def hash_key(api_key):
    """Hash the API key for storage validation."""
    return hashlib.sha256(api_key.encode()).hexdigest()

def encode_key(api_key):
    """Encode the API key for storage."""
    return base64.b64encode(api_key.encode()).decode()

def decode_key(encoded_key):
    """Decode the API key for use."""
    return base64.b64decode(encoded_key.encode()).decode()

def store_api_key(api_key):
    """Store the encoded API key and its hash in ~/.openai_key."""
    with open(key_file_path, 'w') as f:
        f.write(f"{encode_key(api_key)}\n{hash_key(api_key)}")
    print("API key stored securely.")

def get_api_key():
    """Retrieve the API key, check integrity with the hash, and set it in openai.api_key."""
    if key_file_path.exists():
        with open(key_file_path, 'r') as f:
            encoded_key, stored_hash = f.read().strip().split('\n')
        
        api_key = decode_key(encoded_key)
        
        # Verify integrity of the stored key with the stored hash
        if hash_key(api_key) == stored_hash:
            print("API key loaded successfully.")
            return api_key
        else:
            print("API key hash mismatch. Re-entering and storing new key.")
    
    # Prompt for a new API key if none found or if hash mismatch
    api_key = input("Enter your OpenAI API key (it will be stored securely): ").strip()
    store_api_key(api_key)
    return api_key

# Retrieve the API key and set it for use with OpenAI
openai.api_key = get_api_key()

# Convert HEIC images to JPEG
def convert_heic_to_jpeg(heic_path):
    try:
        heif_file = pyheif.read(heic_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        jpeg_path = heic_path.replace(".heic", ".jpg").replace(".HEIC", ".jpg")
        image.save(jpeg_path, "JPEG")
        return jpeg_path
    except Exception as e:
        print(f"Error converting HEIC to JPEG: {str(e)}")
        return None

# Extract text from the image using OCR
def extract_text_from_image(image_path):
    try:
        if image_path.lower().endswith(".heic"):
            print(f"Converting HEIC image: {image_path}")
            image_path = convert_heic_to_jpeg(image_path)
            if image_path is None:
                return None
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img)
        return extracted_text
    except Exception as e:
        print(f"Error reading the image: {str(e)}")
        return None

# Send extracted text to OpenAI's ChatGPT using the correct chat completion endpoint
def get_parsed_details_from_chatgpt(extracted_text):
    messages = [
        {"role": "system", "content": "You are an assistant that extracts details from text."},
        {"role": "user", "content": f"""
        Extract the following details from this text:
        Name:
        Email: <one email address only - user@domain>
        Company: <company name only - if company not found use domain of email>
        Contact: <phone number if any - else nil>
        Text: {extracted_text}
        """}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" if you want to use a cheaper model
        messages=messages,
        max_tokens=200
    )
    
    return response['choices'][0]['message']['content'].strip()

# Function to process all images in a folder
def process_images_from_folder(folder_path):
    contacts = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing {image_path}")
            
            # Extract text from the image using OCR
            extracted_text = extract_text_from_image(image_path)
            
            if extracted_text:
                # Get parsed details from ChatGPT
                parsed_details = get_parsed_details_from_chatgpt(extracted_text)
                print(f"Parsed Details for {filename}:\n{parsed_details}")
                
                # Append to the contact list (for storing in CSV later)
                contacts.append(parsed_details)
            else:
                print(f"No text could be extracted from {image_path}")
    
    return contacts

# Save contacts to a CSV file (database)
def save_contacts_to_csv(contacts, csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Company", "Contact"])  # Write the CSV headers
        
        for contact in contacts:
            # Split the contact into individual lines and filter out "Text" lines
            contact_details = contact.split('\n')
            
            contact_row = []
            for detail in contact_details:
                if ":" in detail and not detail.startswith("Text:"):
                    # Extract the value after the ":" and strip any extra spaces
                    contact_row.append(detail.split(":")[1].strip())
            
            # Write the contact details to the CSV file if the row has valid data
            if contact_row:
                writer.writerow(contact_row)
    
    print(f"Contacts saved to {csv_file_path}")

# Main function
if __name__ == "__main__":
    folder_path = input("Enter the folder path containing business card images: ")
    output_csv_path = "contacts.csv"  # Output CSV file to store the contact database

    # Process images from folder and get contact details
    contacts = process_images_from_folder(folder_path)
    
    # Save the contacts to a CSV file
    if contacts:
        save_contacts_to_csv(contacts, output_csv_path)
    else:
        print("No contacts to save.")
