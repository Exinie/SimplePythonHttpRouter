

class RouteHandler:

    def __init__(self):

        self.ROUTES = {
            ("GET", "/"): "index.html",
            ("GET", "/test"): "test.html",
            ("POST", "/test"): self.example_print_post,
            ("GET", "/style.css"): "style.css"
        }

        self.PLACEHOLDERS = {
            "loggedinUserName": "Exinie",
            "siteTitle": "Exinie's Personal Blog Site",
            "currentYear": 2025
        }

    def example_print_post(self, data):
        print(data)
