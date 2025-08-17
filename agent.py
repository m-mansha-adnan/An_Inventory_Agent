import os
from dotenv import load_dotenv
import google.generativeai as genai

# === Environment Setup ===
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# AI model setup
bot_model = genai.GenerativeModel("gemini-1.5-flash")

# Store for products
inventory_data = []

# === Inventory Operations ===
def add_item(prod_id: int, prod_name: str, prod_qty: int, prod_action: str):
    """Insert a product entry into inventory."""
    if not prod_id:
        return "⚠️ Missing product ID!"
    
    entry = {
        "product_id": prod_id,
        "name": prod_name,
        "qty": prod_qty,
        "action": prod_action
    }
    inventory_data.append(entry)
    return f"✅ Item added: {prod_name} | ID: {prod_id}, Qty: {prod_qty}, Action: {prod_action}"


def remove_item(prod_id: int):
    """Remove an entry by its product ID."""
    for idx, entry in enumerate(inventory_data):
        if entry["product_id"] == prod_id:
            inventory_data.pop(idx)
            return f"🗑️ Product with ID {prod_id} removed."
    return f"❌ No record exists with ID {prod_id}."


def update_item(prod_id: int, prod_name: str, prod_qty: int, prod_action: str):
    """Modify an existing product's details."""
    for idx, entry in enumerate(inventory_data):
        if entry["product_id"] == prod_id:
            inventory_data[idx] = {
                "product_id": prod_id,
                "name": prod_name,
                "qty": prod_qty,
                "action": prod_action
            }
            return f"🔄 Product {prod_id} updated → {prod_name}, Qty: {prod_qty}, Action: {prod_action}"
    return f"❌ No product found with ID {prod_id}."


# === Chat Handler ===
print("🤖 Inventory Assistant Ready (type 'exit' anytime to stop)")

while True:
    user_input = input("You: ")
    if user_input.lower().strip() == "exit":
        break

    # Instruction for Gemini
    task_prompt = f"""
User said: {user_input}

You are the inventory assistant. 
You have these tools:
  - add_item(product_id, name, qty, action)
  - remove_item(product_id)
  - update_item(product_id, name, qty, action)

When the user wants to add, delete, or update an item:
  → Call the correct function with sample values if the user didn’t provide details.
  → If details are given (like id, name, qty, action), use them directly.

❌ Do not show Python code.
✅ Just respond with the function call result.

If you truly cannot match the request, reply: "I don't know".
"""


    ai_reply = bot_model.generate_content(task_prompt)
    print("Bot:", ai_reply.text)
