from flask import Flask, request, jsonify
from flask_cors import CORS
import pywhatkit as kit
from datetime import datetime, timedelta
import time

app = Flask(__name__)
CORS(app)  # Allow requests from your website

# Your WhatsApp number (with country code, no '+')
YOUR_WHATSAPP_NUMBER = "962790489125"

@app.route('/send-order', methods=['POST'])
def send_order():
    try:
        data = request.json  # Order data from your website
        name = data.get('name')
        phone = data.get('phone')
        items = data.get('items')
        total = data.get('total')
        address = data.get('address', 'Pickup')
        notes = data.get('notes', 'None')

        # Format the WhatsApp message
        message = f"📋 *NEW ORDER* 📋\n\n"
        message += f"👤 *Customer:* {name}\n"
        message += f"📞 *Phone:* {phone}\n"
        message += f"📍 *Delivery:* {address}\n\n"
        message += "🛒 *Order Items:*\n"
        for item in items:
            message += f"- {item['quantity']}x {item['name']} (${item['price']})\n"
        message += f"\n💰 *Total:* ${total}\n"
        message += f"📝 *Notes:* {notes}\n\n"
        message += f"⏰ *Time:* {datetime.now().strftime('%H:%M %d/%m/%Y')}"

        # Send to WhatsApp (opens web browser, sends, then closes)
        kit.sendwhatmsg_instantly(
            phone_no=YOUR_WHATSAPP_NUMBER,
            message=message,
            tab_close=True  # Closes browser tab after sending
        )

        return jsonify({"success": True, "message": "Order sent to WhatsApp!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the server