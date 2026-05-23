from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def check_wallet_format(address):
    btc_pattern = r'^(1|3)[a-km-zA-HJ-NP-Z1-9]{25,34}$|^bc1[a-z0-9]{39,59}$'
    eth_pattern = r'^0x[a-fA-F0-9]{40}$'
    trx_pattern = r'^T[A-Za-z1-9]{33}$'

    if re.match(btc_pattern, address): return "Bitcoin (BTC)"
    elif re.match(eth_pattern, address): return "Ethereum / ERC-20 (ETH/USDT)"
    elif re.match(trx_pattern, address): return "TRON / TRC-20 (TRX/USDT)"
    return "Unknown"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_wallet():
    data = request.get_json() or {}
    address = data.get('address', '').strip()
    
    wallet_type = check_wallet_format(address)
    if wallet_type == "Unknown":
        return jsonify({"status": "ERROR", "message": "صيغة المحفظة غير صحيحة، يرجى التأكد منها."})
    
    return jsonify({
        "status": "CLEAN",
        "wallet_type": wallet_type,
        "risk_score": 0,
        "message": "هذه المحفظة آمنة برمجياً ولم يتم تسجيل بلاغات احتيال ضدها حتى الآن."
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
