from __future__ import annotations

from email.message import EmailMessage
from pathlib import Path
from textwrap import dedent

import pytest

from scripts import send_email


def write_fixture(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).lstrip(), encoding="utf-8")
    return path


def test_email_settings_use_gmail_defaults() -> None:
    settings = send_email.load_email_settings(
        {
            "KNOWLEDGE_EMAIL_TO": " reader@example.com ",
            "GMAIL_ADDRESS": " sender@gmail.com ",
        },
        require_smtp=False,
    )

    assert settings == send_email.EmailSettings(
        to_address="reader@example.com",
        from_address="sender@gmail.com",
        smtp_host="smtp.gmail.com",
        smtp_port=465,
        smtp_user="sender@gmail.com",
        smtp_password=None,
    )


def test_email_settings_accept_optional_overrides() -> None:
    settings = send_email.load_email_settings(
        {
            "KNOWLEDGE_EMAIL_TO": "reader@example.com",
            "GMAIL_ADDRESS": "sender@gmail.com",
            "GMAIL_APP_PASSWORD": "app-password",
            "KNOWLEDGE_EMAIL_FROM": "briefings@example.com",
            "SMTP_HOST": "smtp.example.com",
            "SMTP_PORT": "587",
        },
        require_smtp=True,
    )

    assert settings == send_email.EmailSettings(
        to_address="reader@example.com",
        from_address="briefings@example.com",
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_user="sender@gmail.com",
        smtp_password="app-password",
    )


def test_dry_run_writes_email_body_without_smtp_or_app_password(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    markdown_path = write_fixture(
        tmp_path / "daily.md",
        """
        # Daily Knowledge Summary: 2026-07-09

        ## Overview
        Dry-run delivery creates the body from this paragraph.
        """,
    )
    config_path = write_fixture(
        tmp_path / "config.yml",
        """
        email:
          agent_name: "Test Agent"
        """,
    )
    body_output = tmp_path / "email-body.txt"
    monkeypatch.setenv("KNOWLEDGE_EMAIL_TO", "reader@example.com")
    monkeypatch.setenv("GMAIL_ADDRESS", "sender@gmail.com")
    monkeypatch.delenv("GMAIL_APP_PASSWORD", raising=False)

    def fail_send(*args: object, **kwargs: object) -> None:
        raise AssertionError("dry-run must not contact SMTP")

    monkeypatch.setattr(send_email, "send_message", fail_send)

    exit_code = send_email.main(
        [
            str(markdown_path),
            "--dry-run",
            "--config",
            str(config_path),
            "--body-output",
            str(body_output),
            "--link",
            "https://github.com/example/repo/blob/main/KNOWLEDGE/daily/2026-07-09.md",
        ]
    )

    assert exit_code == 0
    assert body_output.read_text(encoding="utf-8") == (
        "Dry-run delivery creates the body from this paragraph.\n"
        "\n"
        f"Source: {markdown_path}\n"
        "Read it on GitHub: "
        "https://github.com/example/repo/blob/main/KNOWLEDGE/daily/2026-07-09.md\n"
        "\n"
        "— Test Agent\n"
    )
    captured = capsys.readouterr()
    assert "Dry run: no SMTP connection was made." in captured.out
    assert "Recipient: reader@example.com" in captured.out
    assert "Subject: Daily Knowledge Summary: 2026-07-09" in captured.out


AGENT_NAME_FORMS = [
    ('email:\n  agent_name: "Research Bot"\n', "Research Bot"),
    ("email:\n  agent_name: 'Research Bot'\n", "Research Bot"),
    ("email:\n  agent_name: Research Bot\n", "Research Bot"),
    ('email:\n  agent_name: "Research Bot"  # sign-off\n', "Research Bot"),
    ("email:\n  agent_name: Research Bot # sign-off\n", "Research Bot"),
    ('email:\n  # which name to sign off with\n  agent_name: "Research Bot"\n', "Research Bot"),
    ('timezone: "Etc/UTC"\nemail:\n  agent_name: "Research Bot"\nquality:\n  x: 1\n', "Research Bot"),
    ('recyclebin:\n  retention_days: 30\nemail:\n  agent_name: "Le petit Kev"\n', "Le petit Kev"),
]


@pytest.mark.parametrize("content,expected", AGENT_NAME_FORMS)
def test_load_agent_name_reads_supported_forms(
    tmp_path: Path, content: str, expected: str
) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text(content, encoding="utf-8")

    assert send_email.load_agent_name(config_path) == expected


REJECTED_CONFIGS = [
    pytest.param('timezone: "Etc/UTC"\n', id="no-email-section"),
    pytest.param("email:\n  reply_to: nobody\n", id="no-agent-name"),
    pytest.param('email:\n  agent_name: ""\n', id="empty-value"),
    pytest.param("email:\n  agent_name:\n", id="missing-value"),
    pytest.param('email: {agent_name: "Research Bot"}\n', id="flow-mapping"),
    pytest.param('email:\n  agent_name: "unterminated\n', id="unterminated-quote"),
    pytest.param('email:\n  agent_name: "Le petit \\"Kev\\""\n', id="escaped-quotes"),
    pytest.param(
        'email:\n  agent_name: "Research Bot"\n'.replace("email:", "notemail:"),
        id="other-section-only",
    ),
]


@pytest.mark.parametrize("content", REJECTED_CONFIGS)
def test_load_agent_name_rejects_unsupported_configs(tmp_path: Path, content: str) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text(content, encoding="utf-8")

    with pytest.raises(send_email.EmailConfigError):
        send_email.load_agent_name(config_path)


def test_load_agent_name_ignores_agent_name_in_other_sections(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text(
        'quality:\n  agent_name: "Wrong Section"\nemail:\n  agent_name: "Right Section"\n',
        encoding="utf-8",
    )

    assert send_email.load_agent_name(config_path) == "Right Section"


def test_load_agent_name_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(send_email.EmailConfigError):
        send_email.load_agent_name(tmp_path / "missing.yml")


def test_repo_config_agent_name_matches_pyyaml() -> None:
    """The stdlib reader must agree with a real YAML parser on the shipped config."""
    yaml = pytest.importorskip("yaml")
    config_path = Path(__file__).resolve().parent.parent / "config.yml"
    expected = yaml.safe_load(config_path.read_text(encoding="utf-8"))["email"]["agent_name"]

    assert send_email.load_agent_name(config_path) == expected


def test_structured_overview_reaches_the_email_body(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    markdown_path = write_fixture(
        tmp_path / "daily.md",
        """
        # Daily Knowledge Summary: 2026-07-09

        ## Overview

        Six items today; two durable.

        - **Infra:** one kernel-optimization agent.

        ---

        - **Formalisation:** no Lean-specific update.
        """,
    )
    config_path = write_fixture(
        tmp_path / "config.yml",
        """
        email:
          agent_name: "Test Agent"
        """,
    )
    body_output = tmp_path / "email-body.txt"
    monkeypatch.setenv("KNOWLEDGE_EMAIL_TO", "reader@example.com")
    monkeypatch.setenv("GMAIL_ADDRESS", "sender@gmail.com")

    exit_code = send_email.main(
        [str(markdown_path), "--dry-run", "--config", str(config_path),
         "--body-output", str(body_output)]
    )

    assert exit_code == 0
    assert body_output.read_text(encoding="utf-8") == (
        "Six items today; two durable.\n"
        "\n"
        "- **Infra:** one kernel-optimization agent.\n"
        "\n"
        "---\n"
        "\n"
        "- **Formalisation:** no Lean-specific update.\n"
        "\n"
        f"Source: {markdown_path}\n"
        "\n"
        "— Test Agent\n"
    )
    assert "Dry run: no SMTP connection was made." in capsys.readouterr().out


def test_live_send_requires_gmail_app_password(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    markdown_path = write_fixture(
        tmp_path / "daily.md",
        """
        # Daily Knowledge Summary: 2026-07-09

        ## Overview
        This live send must require an app password.
        """,
    )
    monkeypatch.setenv("KNOWLEDGE_EMAIL_TO", "reader@example.com")
    monkeypatch.setenv("GMAIL_ADDRESS", "sender@gmail.com")
    monkeypatch.delenv("GMAIL_APP_PASSWORD", raising=False)

    def fail_send(*args: object, **kwargs: object) -> None:
        raise AssertionError("validation must fail before contacting SMTP")

    monkeypatch.setattr(send_email, "send_message", fail_send)

    assert send_email.main([str(markdown_path)]) == 1
    assert "missing required environment variable GMAIL_APP_PASSWORD" in capsys.readouterr().err


def test_port_465_uses_smtp_ssl(monkeypatch: pytest.MonkeyPatch) -> None:
    events: list[object] = []

    class FakeSMTPSSL:
        def __init__(self, host: str, port: int, timeout: int) -> None:
            events.append(("connect", host, port, timeout))

        def __enter__(self) -> FakeSMTPSSL:
            return self

        def __exit__(self, *args: object) -> None:
            events.append("close")

        def login(self, user: str, password: str) -> None:
            events.append(("login", user, password))

        def send_message(self, message: EmailMessage) -> None:
            events.append(("send", message["Subject"]))

    def fail_starttls_smtp(*args: object, **kwargs: object) -> None:
        raise AssertionError("port 465 must not use STARTTLS SMTP")

    monkeypatch.setattr(send_email.smtplib, "SMTP_SSL", FakeSMTPSSL)
    monkeypatch.setattr(send_email.smtplib, "SMTP", fail_starttls_smtp)
    settings = send_email.EmailSettings(
        to_address="reader@example.com",
        from_address="sender@gmail.com",
        smtp_host="smtp.gmail.com",
        smtp_port=465,
        smtp_user="sender@gmail.com",
        smtp_password="app-password",
    )
    message = send_email.build_message(settings, "Briefing", "Body\n")

    send_email.send_message(settings, message)

    assert events == [
        ("connect", "smtp.gmail.com", 465, 30),
        ("login", "sender@gmail.com", "app-password"),
        ("send", "Briefing"),
        "close",
    ]


def test_non_465_port_uses_starttls(monkeypatch: pytest.MonkeyPatch) -> None:
    events: list[object] = []

    class FakeSMTP:
        def __init__(self, host: str, port: int, timeout: int) -> None:
            events.append(("connect", host, port, timeout))

        def __enter__(self) -> FakeSMTP:
            return self

        def __exit__(self, *args: object) -> None:
            events.append("close")

        def starttls(self) -> None:
            events.append("starttls")

        def login(self, user: str, password: str) -> None:
            events.append(("login", user, password))

        def send_message(self, message: EmailMessage) -> None:
            events.append(("send", message["Subject"]))

    def fail_ssl_smtp(*args: object, **kwargs: object) -> None:
        raise AssertionError("non-465 ports must not use SMTP_SSL")

    monkeypatch.setattr(send_email.smtplib, "SMTP", FakeSMTP)
    monkeypatch.setattr(send_email.smtplib, "SMTP_SSL", fail_ssl_smtp)
    settings = send_email.EmailSettings(
        to_address="reader@example.com",
        from_address="sender@gmail.com",
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_user="sender@gmail.com",
        smtp_password="app-password",
    )
    message = send_email.build_message(settings, "Briefing", "Body\n")

    send_email.send_message(settings, message)

    assert events == [
        ("connect", "smtp.example.com", 587, 30),
        "starttls",
        ("login", "sender@gmail.com", "app-password"),
        ("send", "Briefing"),
        "close",
    ]
