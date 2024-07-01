import json
from collections import Counter
from typing import List, Dict


def count_words(text: str) -> int:
    """Count the number of words in a given text."""
    return len(text.split())


def get_word_counts(conversation: List[Dict]) -> Dict[str, int]:
    """Count the number of words spoken by each person."""
    word_counts = Counter()
    for message in conversation:
        speaker = message['speaker_name']
        content = message['content']
        word_counts[speaker] += count_words(content)
    return dict(word_counts)


def get_full_text(conversation: List[Dict], speaker_name: str) -> str:
    """Extract the full text spoken by a given person."""
    return ' '.join(message['content'] for message in conversation
                    if message['speaker_name'] == speaker_name)


def get_speakers(conversation: List[Dict]) -> List[str]:
    """Extract the list of unique speakers."""
    return list(set(message['speaker_name'] for message in conversation))


def analyze_conversation(conversation: List[Dict]):
    """Analyze the conversation and print results."""

    print("Word counts per speaker:")
    for speaker, count in get_word_counts(conversation).items():
        print(f"{speaker}: {count} words")

    print("\nList of speakers:")
    print(", ".join(get_speakers(conversation)))

    print("\nExample of extracting full text for a speaker:")
    first_speaker = get_speakers(conversation)[0]
    print(f"Full text for {first_speaker}:")
    print(get_full_text(conversation, first_speaker)[:200] + "...")  # Print first 200 characters

    # save get_full_text(conversation, first_speaker) to a file. The text
    with open('full_text.txt', 'w') as f:
        f.write(get_full_text(conversation, 'משה טור פז (יש עתיד)'))

# Example usage
if __name__ == "__main__":
    # load the output.json file
    json_file = json.load(open('output.json'))

    analyze_conversation(json_file)