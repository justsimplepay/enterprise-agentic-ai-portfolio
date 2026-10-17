from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_app_and_graph(monkeypatch):
    monkeypatch.delenv("DOCUMENT_RESEARCH_CONFIG", raising=False)
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    assert app.button[0].disabled
    app.text_input[0].input("Who approves purchases?").run()
    app.button[0].click().run()
    assert not app.exception
    assert "prepared" in app.success[0].value


def test_invalid_config_is_displayed(tmp_path, monkeypatch):
    config = tmp_path / "bad.json"
    config.write_text('{"provider": "example"}')
    monkeypatch.setenv("DOCUMENT_RESEARCH_CONFIG", str(config))
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    assert "Invalid model configuration" in app.error[0].value
