from flask import Flask, request, jsonify
import pywhatkit as kit
from datetime import datetime
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
WHATSAPP_NUMBER = "962790489125"  # Your WhatsApp number with country code
CHROME_PATH = os.getenv("CHROME_PATH", "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
@app.route('/send-order', methods=['POST'])
def send_order():
    print("\n=== Incoming Request ===")
    print("Headers:", request.headers)
    print("JSON Data:", request.json)
    try:
        # Get order data from request
        data = request.json
        name = data.get('name')
        phone = data.get('phone')
        items = data.get('items', [])
        total = data.get('total', "$0.00")
        notes = data.get('notes', "None")

        # Format message
        message = f"📋 *NEW ORDER* 📋\n\n"
        message += f"👤 *Customer* : {name}\n"
        message += f"📞 *Phone* : {phone}\n\n"
        message += "🛒 *Order Items* :\n"
        for item in items:
            message += f"- {item['quantity']}x {item['name']} (${item['price']})\n"
        message += f"\n💰 *Total* : {total}\n"
        message += f"📝 *Notes* : {notes}\n\n"
        message += f"⏰ *Time* : {datetime.now().strftime('%H:%M %d/%m/%Y')}"

        # Send to WhatsApp
        kit.sendwhatmsg_instantly(
            phone_no=WHATSAPP_NUMBER,
            message=message,
            tab_close=True,  # Closes browser tab after sending
            browser_path=CHROME_PATH,  # Specify Chrome path
            close_time=10  # Seconds to wait before closing
        )

        return jsonify({"success": True, "message": "Order sent to WhatsApp!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)  