import re
import json
import docx
import argparse
from typing import List, Dict


def extract_structured_conversation(doc_path: str) -> List[Dict[str, str]]:
    """
    Extract text between special markers from a DOCX file and structure it as a list of messages.

    Args:
        doc_path (str): Path to the DOCX file.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each representing a message in the conversation.
    """
    try:
        doc = docx.Document(doc_path)
    except Exception as e:
        print(f"Error opening document: {e}")
        return []

    full_text = "\n".join([para.text for para in doc.paragraphs])

    # Regex pattern to match markers and extract speaker names and types
    pattern = r'<<\s*([^>]+)\s*>>\s*([^:]+):\s*<<\s*\1\s*>>\s*(.*?)(?=<<\s*[^>]+\s*>>|$)'

    matches = re.findall(pattern, full_text, re.DOTALL)

    conversation = []
    for speaker_type, speaker_name, text in matches:
        message = {
            "speaker_type": speaker_type.strip(),
            "speaker_name": speaker_name.strip(),
            "content": text.strip()
        }
        conversation.append(message)

    return conversation


def main():
    parser = argparse.ArgumentParser(description="Extract structured conversation from a DOCX file and output as JSON.")
    parser.add_argument("docx_path", help="Path to the DOCX file")
    parser.add_argument("-o", "--output", help="Output JSON file path")
    args = parser.parse_args()

    conversation = extract_structured_conversation(args.docx_path)

    if not conversation:
        print("No text sections found between markers.")
        return

    json_output = json.dumps(conversation, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"JSON data written to {args.output}")
    else:
        print(json_output)


if __name__ == "__main__":
    main()