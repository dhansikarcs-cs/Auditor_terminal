import os
import datetime
from google import genai

# --- CONFIG ---
# Paste your API Key here for local use. 
# Delete it before pushing to GitHub!
API_KEY = "" 

def run_audit():
    if not API_KEY:
        print("\n❌ API Key Missing: Please edit app.py and add your key to the API_KEY variable.")
        return

    client = genai.Client(api_key=API_KEY)

    # 1. LOAD ARCHITECT PERSONA
    rules = "Act as a professional auditor."
    if os.path.exists("instructions.txt"):
        with open("instructions.txt", "r") as f:
            rules = f.read()

    # 2. GET CODE INPUT
    print("\n🕵️  Senior Architect Auditor | Terminal Mode")
    print("Paste code & press Ctrl+D (Unix/Termux) or Ctrl+Z (Windows) to finish:\n")
    
    try:
        lines = []
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        user_code = "\n".join(lines)

    if not user_code.strip():
        print("Empty input. Exiting.")
        return

    # 3. THE ORIGINAL LOGIC + FORCED SECTIONS
    # This keeps the OG feel but ensures the 3 sections you want are always there.
    prompt = f"""
    {rules}

    AUDIT TASK:
    Analyze the following code for security vulnerabilities and architectural flaws.
    You MUST provide your response in exactly this order:
    
    1. WHAT NEEDS TO BE CHANGED (Identify bugs/risks)
    2. UPDATED CODE (Provide the full fixed script)
    3. CHANGES EXPLAINED (Human-readable reasoning)

    CODE:
    {user_code}
    """

    print("\n🚀 Architect is reviewing...")
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        
        print("\n" + "="*40)
        print(f"REPORT GENERATED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*40)
        print(response.text)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_audit()
