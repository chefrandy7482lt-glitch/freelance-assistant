@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Freelance Assistant</title>
        </head>
        <body style="font-family: Arial; padding: 40px;">

            <h1>Freelance Assistant</h1>

            <h2>System Active</h2>

            <p>This system is now running live pricing logic.</p>

            <ul>
                <li>TDU Value Engine → ACTIVE</li>
                <li>Pricing Engine → ACTIVE</li>
                <li>Freelance Pipeline → ACTIVE</li>
            </ul>

            <p>Status: ONLINE ✔</p>

        </body>
    </html>
    """