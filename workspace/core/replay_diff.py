import json
import sys
from typing import Dict, Any, List

def load_jsonl(filepath: str) -> List[Dict[str, Any]]:
    """Loads a JSONL file into a list of dictionaries."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {line_num} in {filepath}: {e}", file=sys.stderr)
                sys.exit(1)
    return data

def normalize_json_object(obj: Dict[str, Any]) -> str:
    """Normalizes a JSON object to a stable string representation."""
    return json.dumps(obj, sort_keys=True, indent=None, ensure_ascii=False)

def compare_jsonl_files(file1_path: str, file2_path: str) -> bool:
    """
    Compares two JSONL files line by line, reporting differences.
    Returns True if files are identical, False otherwise.
    """
    data1 = load_jsonl(file1_path)
    data2 = load_jsonl(file2_path)

    if len(data1) != len(data2):
        print(f"Files have different number of lines: {len(data1)} vs {len(data2)}", file=sys.stderr)
        return False

    identical = True
    for i, (obj1, obj2) in enumerate(zip(data1, data2), 1):
        norm1 = normalize_json_object(obj1)
        norm2 = normalize_json_object(obj2)
        if norm1 != norm2:
            print(f"Difference found on line {i}:", file=sys.stderr)
            print(f"  File 1: {norm1}", file=sys.stderr)
            print(f"  File 2: {norm2}", file=sys.stderr)
            identical = False
    
    if identical:
        print(f"Files {file1_path} and {file2_path} are identical (JSONL content).")
    else:
        print(f"Files {file1_path} and {file2_path} differ (JSONL content).")

    return identical

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: .venv/bin/python workspace/core/replay_diff.py <file1.jsonl> <file2.jsonl>", file=sys.stderr)
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if not compare_jsonl_files(file1, file2):
        sys.exit(1)
