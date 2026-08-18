#!/usr/bin/env python3
"""Send a knowledge workflow email from a Markdown Overview section."""

from __future__ import annotations

import argparse
import os
import smtplib
import sys
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Mapping

try:
    from .extract_overview import OverviewError, extract_overview_file, read_text
except ImportError:  # pragma: no cover - used when running this file as a script.
    from extract_overview import OverviewError, extract_overview_file, read_text


DEFAULT_SMTP_HOST = "smtp.gmail.com"
DEFAULT_SMTP_PORT = 465
DEFAULT_SMTP_TIMEOUT_SECONDS = 30
DEFAULT_CONFIG_PATH = Path("config.yml")


class EmailConfigError(ValueError):
    """Raised when email environment values are missing or invalid."""


@dataclass(frozen=True)
class EmailSettings:
    to_address: str
    from_address: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str | None


def require_env(env: Mapping[str, str], name: str) -> str:
    value = env.get(name)
    if value is None or not value.strip():
        raise EmailConfigError(f"missing required environment variable {name}")
    return value.strip()


def env_or_default(env: Mapping[str, str], name: str, default: str) -> str:
    value = env.get(name)
    return value.strip() if value is not None and value.strip() else default


def parse_config_scalar(raw: str, label: str) -> str:
    """Parse a single quoted-or-bare YAML scalar, refusing anything ambiguous."""
    value = raw.strip()
    if value[:1] in {'"', "'"}:
        quote = value[0]
        end = value.find(quote, 1)
        if end == -1:
            raise EmailConfigError(f"{label}: unterminated {quote} quote")
        trailing = value[end + 1 :].strip()
        if trailing and not trailing.startswith("#"):
            raise EmailConfigError(
                f"{label}: unsupported quoting — put the name in one pair of quotes "
                "with no escaped quotes inside"
            )
        return value[1:end].strip()

    value = value.split("#", 1)[0].strip()
    if value.startswith(("{", "[", "&", "*", ">", "|")):
        raise EmailConfigError(
            f"{label}: unsupported YAML form — write it as a plain quoted string"
        )
    return value


def load_agent_name(path: Path = DEFAULT_CONFIG_PATH) -> str:
    """Read ``email.agent_name`` — the name the email body is signed off with.

    Deliberately understands only the small YAML subset the config file is
    written in, so the GitHub Actions email step needs no third-party package on
    the runner. Anything it does not recognize raises instead of guessing.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise EmailConfigError(f"{path}: file does not exist") from exc
    except OSError as exc:
        raise EmailConfigError(f"{path}: could not read file: {exc}") from exc

    in_email_section = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            # A new top-level key ends any section that came before it.
            in_email_section = line.split(":", 1)[0].strip() == "email"
            continue
        if not in_email_section:
            continue
        key, separator, raw = line.strip().partition(":")
        if separator and key.strip() == "agent_name":
            agent_name = parse_config_scalar(raw, f"{path}: email.agent_name")
            if not agent_name:
                raise EmailConfigError(f"{path}: email.agent_name must be a non-empty string")
            return agent_name

    raise EmailConfigError(f"{path}: email.agent_name is not set")


def parse_smtp_port(raw_port: str, env_name: str = "SMTP_PORT") -> int:
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise EmailConfigError(f"{env_name} must be an integer SMTP port") from exc
    if port < 1 or port > 65535:
        raise EmailConfigError(f"{env_name} must be between 1 and 65535")
    return port


def load_email_settings(
    env: Mapping[str, str],
    require_smtp: bool,
) -> EmailSettings:
    to_address = require_env(env, "KNOWLEDGE_EMAIL_TO")
    gmail_address = require_env(env, "GMAIL_ADDRESS")
    from_address = env_or_default(env, "KNOWLEDGE_EMAIL_FROM", gmail_address)
    smtp_host = env_or_default(env, "SMTP_HOST", DEFAULT_SMTP_HOST)
    raw_port = env_or_default(env, "SMTP_PORT", str(DEFAULT_SMTP_PORT))
    smtp_password = require_env(env, "GMAIL_APP_PASSWORD") if require_smtp else None

    return EmailSettings(
        to_address=to_address,
        from_address=from_address,
        smtp_host=smtp_host,
        smtp_port=parse_smtp_port(raw_port),
        smtp_user=gmail_address,
        smtp_password=smtp_password,
    )


def infer_subject(markdown_path: Path) -> str:
    text = read_text(markdown_path)
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            subject = stripped[2:].strip()
            if subject:
                return subject
    return f"Knowledge update: {markdown_path.stem}"


def build_email_body(
    overview: str,
    source_path: Path,
    agent_name: str,
    link: str | None = None,
) -> str:
    lines = [overview, "", f"Source: {source_path}"]
    if link:
        lines.append(f"Read it on GitHub: {link}")
    lines.extend(["", f"— {agent_name}"])
    return "\n".join(lines) + "\n"


def build_message(settings: EmailSettings, subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message["To"] = settings.to_address
    message["From"] = settings.from_address
    message["Subject"] = subject
    message.set_content(body)
    return message


def send_message(settings: EmailSettings, message: EmailMessage) -> None:
    if settings.smtp_password is None:
        raise EmailConfigError("GMAIL_APP_PASSWORD is required outside dry-run mode")

    if settings.smtp_port == 465:
        with smtplib.SMTP_SSL(
            settings.smtp_host,
            settings.smtp_port,
            timeout=DEFAULT_SMTP_TIMEOUT_SECONDS,
        ) as smtp:
            smtp.login(settings.smtp_user, settings.smtp_password)
            smtp.send_message(message)
        return

    with smtplib.SMTP(
        settings.smtp_host,
        settings.smtp_port,
        timeout=DEFAULT_SMTP_TIMEOUT_SECONDS,
    ) as smtp:
        smtp.starttls()
        smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.send_message(message)


def write_body_output(path: Path, body: str) -> None:
    try:
        path.write_text(body, encoding="utf-8")
    except OSError as exc:
        raise EmailConfigError(f"{path}: could not write email body: {exc}") from exc


def print_dry_run(
    settings: EmailSettings,
    subject: str,
    source_path: Path,
    body: str,
    body_output: Path | None,
) -> None:
    print("Dry run: no SMTP connection was made.")
    print(f"Recipient: {settings.to_address}")
    print(f"Subject: {subject}")
    print(f"Overview source: {source_path}")
    if body_output is not None:
        print(f"Body path: {body_output}")
    else:
        print("Body path: <not written>")
    print(f"Body characters: {len(body)}")
    print(f"Body lines: {len(body.splitlines())}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Send the Overview section from a knowledge Markdown file."
    )
    parser.add_argument("markdown_file", type=Path)
    parser.add_argument("--subject", help="Email subject. Defaults to the first H1 heading.")
    parser.add_argument("--link", help="GitHub URL to include in the body.")
    parser.add_argument(
        "--body-output",
        type=Path,
        help="Write the generated plain-text email body to this path.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not contact SMTP.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Config file holding email.agent_name.",
    )
    parser.add_argument(
        "--agent-name",
        help="Name used to sign off the email body. Defaults to email.agent_name in --config.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        settings = load_email_settings(os.environ, require_smtp=not args.dry_run)
        agent_name = args.agent_name or load_agent_name(args.config)
        overview = extract_overview_file(args.markdown_file)
        subject = args.subject or infer_subject(args.markdown_file)
        body = build_email_body(
            overview=overview,
            source_path=args.markdown_file,
            agent_name=agent_name,
            link=args.link,
        )
        if args.body_output is not None:
            write_body_output(args.body_output, body)

        message = build_message(settings, subject, body)
        if args.dry_run:
            print_dry_run(settings, subject, args.markdown_file, body, args.body_output)
            return 0

        send_message(settings, message)
        print(f"Sent email to {settings.to_address} with subject: {subject}")
        return 0
    except (EmailConfigError, OverviewError) as exc:
        print(f"Email send failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
