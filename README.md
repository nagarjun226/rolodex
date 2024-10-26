# Rolodex
## Business Card Contact Extractor

You go to conferences, you receive business cards, you dont want to pay a subscription to get the contacts extracted, you dont want want to do it manually. So you use AI to help you write code that uses AI in 10 minutes and get your job done (paying $0.70 to open AI). You could do it that way too, but I just put it out there so you dont have to.

**rolodex** is a Python-based application that processes images of business cards, extracts key contact information (such as Name, Email, Company, and Contact), and saves the details into a CSV database. Using OCR and OpenAI's ChatGPT for natural language processing, the tool is designed to simplify contact management from physical cards paying the least amount possible.

## Features
- **OCR for Text Extraction**: Utilizes `pytesseract` to extract text from images in various formats, including HEIC, JPEG, and PNG.
- **AI-Powered Text Parsing**: Sends extracted text to ChatGPT to intelligently parse out relevant contact information.
- **Secure API Key Management**: Encrypts and securely stores the OpenAI API key in the user's home directory.
- **Database Generation**: Automatically saves parsed contact details in a CSV file for easy database creation and contact management.

## Future Work
- **Expand to More AI APIs**: Integrate additional AI APIs such as Entropic and Gemini for enhanced NLP capabilities and redundancy.
- **Enhanced Contact Information Extraction**: Extract additional details beyond basic contact information, such as job title, address, and department.
- **Contextual Awareness and Business Insights**: Use AI agents to analyze the company details and provide contextual suggestions on potential collaboration or networking opportunities.

## Requirements
- **Python 3.11.0+**
- **Python Packages**:
  - `openai`
  - `Pillow`
  - `pytesseract`
  - `pyheif`

Install the dependencies via `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Setting Up with pyenv

To ensure a consistent environment, it’s recommended to use pyenv to manage your Python version. This project is developed and tested with Python 3.11.0.

### Install pyenv
If you haven’t installed pyenv, you can do so by following these steps:

macOS:
```bash
brew install pyenv
```

After installation, add pyenv to your shell’s environment by adding the following to your .bashrc, .zshrc, or equivalent:

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
```

### Set up Python 3.11.0
Install Python 3.11.0 with pyenv:
```bash
pyenv install 3.11.0
```
Set it as the local version for this project:
```bash
pyenv local 3.11.0
```

## Setup

### Step 1: Install Tesseract OCR
Ensure Tesseract is installed on your system:
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt install tesseract-ocr`
- **Windows**: [Download Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

### Step 2: Obtain OpenAI API Key
1. Sign up for an API key from [OpenAI](https://beta.openai.com/signup/).
2. Run the application for the first time, and it will prompt you for the API key, securely storing it as a base64 encoded and hashed version in `~/.openai_key`.

## Usage

1. **Prepare Your Business Card Images**:
   - Store images of business cards in a dedicated folder. Supported formats: `.jpg`, `.jpeg`, `.png`, `.heic`.

2. **Run the Application**:
   - In the terminal, run:
     ```bash
     python your_script.py
     ```
   - When prompted, enter the path to the folder containing your business card images.

3. **Results**:
   - The extracted and parsed contact details will be saved in `contacts.csv` in the same directory.

## Example

### Sample Output in `contacts.csv`:

| Name       | Email             | Company     | Contact       |
|------------|--------------------|-------------|---------------|
| Jane Doe   | jane@example.com   | Acme Corp   | 123-456-7890 |
| John Smith | john@example.org   | OpenAI      | nil           |

## Code Overview

- **`get_api_key()`**: Manages secure storage and retrieval of the OpenAI API key using base64 encoding and hashing for verification.
- **`extract_text_from_image()`**: Uses `pytesseract` to extract text from a business card image, with automatic HEIC to JPEG conversion.
- **`get_parsed_details_from_chatgpt()`**: Sends the extracted text to ChatGPT to identify and structure relevant contact details.
- **`process_images_from_folder()`**: Processes each image in the specified folder, calling OCR and AI parsing functions.
- **`save_contacts_to_csv()`**: Saves parsed contact information to `contacts.csv`.

## Future Enhancements

### 1. AI API Integrations
- Integrating with other popular AI APIs
- Integrating with Local AI servers (like Msty)

### 2. Expanded Data Extraction
- Extract more fields such as job title, department, and location to make the contacts database more comprehensive.

### 3. AI Agents for Contextual Insights
- Use AI agents to gain insights into companies listed on business cards, suggesting potential collaboration or networking strategies.

## License
This project is licensed under the MIT License.

---

Let me know if you need any more details or specific adjustments to the `README.md`!