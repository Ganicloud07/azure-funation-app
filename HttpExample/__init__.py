import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:

    # Sample data
    users = [
        {"id": 1, "name": "veera-don", "role": "DevOps Engineer"},
        {"id": 2, "name": "nareshit", "role": "Backend Developer"},
        {"id": 3, "name": "vsv", "role": "Cloud Engineer"}
    ]

    api = req.params.get('api')
    name = req.params.get('name')

    # ---------------- API MODE ----------------
    if api == "true":
        if name:
            user = next((u for u in users if u["name"].lower() == name.lower()), None)
            if user:
                return func.HttpResponse(
                    json.dumps(user),
                    mimetype="application/json"
                )
            else:
                return func.HttpResponse(
                    json.dumps({"message": "User not found"}),
                    status_code=404,
                    mimetype="application/json"
                )

        return func.HttpResponse(
            json.dumps(users),
            mimetype="application/json"
        )

    # ---------------- VIEW MODE ----------------
    html_page = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Viewer</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            button { padding: 8px 12px; margin: 5px; cursor: pointer; }
            .card {
                border: 1px solid #ddd;
                padding: 10px;
                margin-top: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>

    <h2>User Details Viewer</h2>

    <input type="text" id="username" placeholder="Enter user name" />
    <br><br>

    <button onclick="getUser()">Get User</button>
    <button onclick="getAllUsers()">Get All Users</button>

    <div id="result"></div>

    <script>
        const API_URL = "/api/HttpExample?api=true";

        function getUser() {
            const name = document.getElementById("username").value;
            fetch(API_URL + "&name=" + name)
                .then(function(res) { return res.json(); })
                .then(function(data) { showResult(data); });
        }

        function getAllUsers() {
            fetch(API_URL)
                .then(function(res) { return res.json(); })
                .then(function(data) { showResult(data); });
        }

        function showResult(data) {
            var result = document.getElementById("result");
            result.innerHTML = "";

            if (Array.isArray(data)) {
                data.forEach(function(user) {
                    result.innerHTML += 
                        "<div class='card'>" +
                        "<b>ID:</b> " + user.id + "<br>" +
                        "<b>Name:</b> " + user.name + "<br>" +
                        "<b>Role:</b> " + user.role +
                        "</div>";
                });
            } else {
                result.innerHTML =
                    "<div class='card'>" +
                    "<b>ID:</b> " + (data.id || "") + "<br>" +
                    "<b>Name:</b> " + (data.name || data.message) + "<br>" +
                    "<b>Role:</b> " + (data.role || "") +
                    "</div>";
            }
        }
    </script>

    </body>
    </html>
    """

    return func.HttpResponse(
        html_page,
        mimetype="text/html"
    )
