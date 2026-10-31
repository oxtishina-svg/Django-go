from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

BASE_DIR = Path(__file__).resolve().parent.parent
HTML_DIR = BASE_DIR / "html"

HOST = "localhost"
PORT = 8000


class WebHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов."""

    def read_html_file(self, filename: str) -> str:
        """Читает HTML-файл и возвращает его содержимое."""
        file_path = HTML_DIR / filename

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def send_html_response(
        self,
        content: str,
        status_code: int = 200,
    ) -> None:
        """Отправляет HTML-ответ клиенту."""
        self.send_response(status_code)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def do_GET(self) -> None:
        """Обрабатывает GET-запрос."""
        if self.path == "/404":
            content = self.read_html_file("404.html")
            self.send_html_response(
                content,
                status_code=404,
            )
            return

        content = self.read_html_file("contacts.html")
        self.send_html_response(content)

    def do_POST(self) -> None:
        """Обрабатывает POST-запрос."""
        content_length = int(
            self.headers.get(
                "Content-Length",
                0,
            )
        )

        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = parse_qs(post_data)

        print("Получены данные формы:")
        print(parsed_data)

        content = self.read_html_file("contacts.html")
        self.send_html_response(content)


def run_server() -> None:
    """Запускает HTTP-сервер."""
    server = HTTPServer(
        (HOST, PORT),
        WebHandler,
    )

    print(f"Сервер запущен: http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
