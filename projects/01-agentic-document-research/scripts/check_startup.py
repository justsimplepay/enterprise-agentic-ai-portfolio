"""Start a real local Streamlit server, check health, and always clean up."""

import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def main() -> None:
    app = Path(__file__).resolve().parents[1] / "app.py"
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app),
            "--server.headless=true",
            "--server.address=127.0.0.1",
            "--server.port=18501",
            "--browser.gatherUsageStats=false",
        ]
    )
    # Loopback must not be sent through an inherited corporate/session proxy.
    client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f"Streamlit exited early: {process.returncode}")
            try:
                with client.open("http://127.0.0.1:18501/_stcore/health", timeout=1) as response:
                    if response.status == 200 and response.read() == b"ok":
                        print("Streamlit startup check passed")
                        return
            except (urllib.error.URLError, TimeoutError):
                time.sleep(0.2)
        raise RuntimeError("Streamlit did not become healthy within 30 seconds")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


if __name__ == "__main__":
    main()
