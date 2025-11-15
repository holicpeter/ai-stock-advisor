import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Test všetky známe Claude 3.5 a 4.x modely
models_to_test = [
    # Claude 3.5 verzie
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-latest",
    
    # Claude 3 verzie  
    "claude-3-opus-20240229",
    "claude-3-opus-latest",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    
    # Možné nové verzie (ak existujú)
    "claude-4-opus",
    "claude-4-sonnet", 
    "claude-sonnet-4.5",
    "claude-3-5-haiku-20241022",
]

print("="*70)
print("TESTING CLAUDE API - Checking available models")
print("="*70)
print()

working_models = []
failed_models = []

for model in models_to_test:
    try:
        print(f"Testing: {model}...", end=" ")
        response = client.messages.create(
            model=model,
            max_tokens=20,
            messages=[{"role": "user", "content": "Say OK"}]
        )
        print(f"✅ WORKS!")
        print(f"   → Response: {response.content[0].text}")
        print(f"   → Tokens: in={response.usage.input_tokens}, out={response.usage.output_tokens}")
        working_models.append(model)
        print()
    except Exception as e:
        error_str = str(e)
        if "not_found_error" in error_str:
            print(f"❌ Model not found")
            failed_models.append((model, "Not available"))
        elif "permission" in error_str.lower() or "access" in error_str.lower():
            print(f"⚠️  No permission (tier issue)")
            failed_models.append((model, "Permission denied - upgrade needed"))
        else:
            print(f"❌ Error: {error_str[:80]}")
            failed_models.append((model, error_str[:80]))
        print()

print("="*70)
print("SUMMARY")
print("="*70)
print(f"\n✅ WORKING MODELS ({len(working_models)}):")
if working_models:
    for m in working_models:
        print(f"   • {m}")
else:
    print("   None")

print(f"\n❌ FAILED MODELS ({len(failed_models)}):")
if failed_models:
    for m, reason in failed_models:
        print(f"   • {m}")
        print(f"     Reason: {reason}")
else:
    print("   None")

print("\n" + "="*70)
if working_models:
    print(f"✅ BEST MODEL TO USE: {working_models[0]}")
else:
    print("❌ No working models found! Check your API key.")
print("="*70)
