from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

# Hardcoded activation key (Base32-encoded)
VALID_ACTIVATION_KEY = "TZAQ-XRQU-QXYC-ABOL-APJQ-SIEC-VWVA"
AES_DECRYPTION_KEY = "4c3aae9c55f3d61e6557f306eb8b881e40ca3898d683dbd958ba04f02259902c"  # Change this to a secure key!

@app.route('/validate', methods=['GET'])
def validate_key():
    key = request.args.get('key', '').upper()  # Convert input key to uppercase
    if key == VALID_ACTIVATION_KEY:
        response = {"status": "success", "aes_key": AES_DECRYPTION_KEY}
    else:
        response = {"status": "error", "message": "Invalid activation key"}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
