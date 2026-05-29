from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Flask App</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f8f9fa;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: #333;
        }
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
            padding: 48px 56px;
            max-width: 520px;
            width: 100%;
            text-align: center;
        }
        .logo {
            font-size: 48px;
            margin-bottom: 16px;
        }
        h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #111;
        }
        p {
            color: #666;
            font-size: 15px;
            line-height: 1.6;
            margin-bottom: 28px;
        }
        .badge {
            display: inline-block;
            background: #e8f5e9;
            color: #2e7d32;
            font-size: 13px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 99px;
            margin-bottom: 32px;
        }
        .routes {
            text-align: left;
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px 24px;
        }
        .routes h2 {
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #888;
            margin-bottom: 14px;
        }
        .route {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
            font-size: 14px;
        }
        .method {
            font-size: 11px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 4px;
            background: #dbeafe;
            color: #1d4ed8;
            flex-shrink: 0;
        }
        .method.post { background: #fef9c3; color: #854d0e; }
        code {
            font-family: "SF Mono", "Fira Mono", monospace;
            font-size: 13px;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🐍</div>
        <h1>Flask App</h1>
        <p>Your Python Flask server is up and running.</p>
        <div class="badge">&#10003; Running</div>
        <div class="routes">
            <h2>Available Routes</h2>
            <div class="route">
                <span class="method">GET</span>
                <code>/</code> &mdash; this page
            </div>
            <div class="route">
                <span class="method">GET</span>
                <code>/api/hello</code> &mdash; JSON greeting
            </div>
            <div class="route">
                <span class="method post">POST</span>
                <code>/api/echo</code> &mdash; echo JSON body
            </div>
        </div>
    </div>
</body>
</html>
"""


@app.route("/api/hello")
def hello():
    name = request.args.get("name", "World")
    return jsonify({"message": f"Hello, {name}!", "status": "ok"})


@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"echo": data, "status": "ok"})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
