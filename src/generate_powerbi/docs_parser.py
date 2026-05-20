import re
import os

def load_descriptions(docs_path):
    """
    Parses a dbt docs markdown file and returns a dictionary of descriptions.
    The keys are the docblock names (e.g., 'table_dim_claim', 'column_agent_id').
    """
    if not os.path.exists(docs_path):
        print(f"Warning: docs file not found at {docs_path}")
        return {}

    with open(docs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find {% docs name %} ... {% enddocs %}
    # Re.DOTALL allows . to match newlines
    pattern = re.compile(r'{%\s*docs\s+([\w-]+)\s*%}(.*?){%\s*enddocs\s*%}', re.DOTALL)
    
    matches = pattern.findall(content)
    
    descriptions = {}
    for name, text in matches:
        # Clean up whitespace and newlines
        clean_text = text.strip()
        descriptions[name] = clean_text
        
    return descriptions

def normalize_column_name(pretty_name):
    """
    Converts a "Pretty Column Name" back to "pretty_column_name".
    This is the reverse of the logic used in export_reporting/utils.py.
    """
    # Replace spaces with underscores and lowercase
    name = pretty_name.replace(' ', '_').lower()
    return name
