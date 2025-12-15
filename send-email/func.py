import io
import json
import os
import smtplib
import ssl
from email.message import EmailMessage

from fdk import response


def _get_bool_env(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "y", "on"}


def handler(ctx, data: io.BytesIO = None):
    try:
        raw = (data.getvalue().decode("utf-8") if data else "").strip()
        payload = json.loads(raw) if raw else {}

        to_addrs = payload.get("to")
        subject = payload.get("subject")
        text_body = payload.get("text")
        html_body = payload.get("html")

        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]

        if not to_addrs or not isinstance(to_addrs, list):
            raise ValueError("'to' must be a non-empty string or array of strings")
        if not subject or not isinstance(subject, str):
            raise ValueError("'subject' must be a non-empty string")
        if (text_body is None or text_body == "") and (html_body is None or html_body == ""):
            raise ValueError("Provide at least one of 'text' or 'html'")

        smtp_host = os.environ.get("SMTP_HOST")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        smtp_user = os.environ.get("SMTP_USERNAME")
        smtp_pass = os.environ.get("SMTP_PASSWORD")
        smtp_from = os.environ.get("SMTP_FROM")
        use_starttls = _get_bool_env("SMTP_STARTTLS", True)

        missing = [
            k
            for k, v in {
                "SMTP_HOST": smtp_host,
                "SMTP_USERNAME": smtp_user,
                "SMTP_PASSWORD": smtp_pass,
                "SMTP_FROM": smtp_from,
            }.items()
            if not v
        ]
        if missing:
            raise ValueError("Missing required env var(s): " + ", ".join(missing))

        msg = EmailMessage()
        msg["From"] = smtp_from
        msg["To"] = ", ".join(to_addrs)
        msg["Subject"] = subject

        if text_body is not None and text_body != "":
            msg.set_content(text_body)
        if html_body is not None and html_body != "":
            if text_body is None or text_body == "":
                msg.set_content("This email contains HTML content. Please use an HTML-capable email client.")
            msg.add_alternative(html_body, subtype="html")

        ssl_ctx = ssl.create_default_context()

        with smtplib.SMTP(host=smtp_host, port=smtp_port, timeout=30) as server:
            server.ehlo()
            if use_starttls:
                server.starttls(context=ssl_ctx)
                server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        return response.Response(
            ctx,
            response_data=json.dumps({"ok": True, "to": to_addrs, "subject": subject}),
            headers={"Content-Type": "application/json"},
        )

    except Exception as e:
        return response.Response(
            ctx,
            response_data=json.dumps({"ok": False, "error": str(e)}),
            headers={"Content-Type": "application/json"},
            status_code=400,
        )
