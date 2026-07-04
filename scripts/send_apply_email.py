#!/usr/bin/env python3
"""Send a job-application email with resume attachment via SMTP (A-channel apply).

Credentials are read from the macOS Keychain (never from the repo):
    security add-generic-password -s ai-job-smtp -a <email> -w <auth_code>

Usage:
    python3 send_apply_email.py \
        --from me@163.com --to talent@example.com \
        --subject "姓名-岗位-联系方式" \
        --body-file body.txt --attach resume.pdf [--dry-run]

Common SMTP hosts: 163.com -> smtp.163.com:465 (SSL, requires授权码 not password),
qq.com -> smtp.qq.com:465, gmail -> smtp.gmail.com:465 (app password).
"""
import argparse
import mimetypes
import pathlib
import smtplib
import subprocess
import sys
from email.message import EmailMessage

HOSTS = {
    "163.com": ("smtp.163.com", 465),
    "126.com": ("smtp.126.com", 465),
    "qq.com": ("smtp.qq.com", 465),
    "gmail.com": ("smtp.gmail.com", 465),
    "outlook.com": ("smtp-mail.outlook.com", 587),
}


def keychain_password(account):
    r = subprocess.run(
        ["security", "find-generic-password", "-s", "ai-job-smtp", "-a", account, "-w"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        sys.exit(
            f"No SMTP credential in Keychain for {account}.\n"
            f"Store it first (auth code, NOT login password):\n"
            f"  security add-generic-password -s ai-job-smtp -a {account} -w <auth_code>"
        )
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="sender", required=True)
    ap.add_argument("--to", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True)
    ap.add_argument("--attach", action="append", default=[])
    ap.add_argument("--dry-run", action="store_true", help="build the message but do not send")
    args = ap.parse_args()

    domain = args.sender.rsplit("@", 1)[1]
    if domain not in HOSTS:
        sys.exit(f"Unknown SMTP host for {domain}; add it to HOSTS.")
    host, port = HOSTS[domain]

    msg = EmailMessage()
    msg["From"] = args.sender
    msg["To"] = args.to
    msg["Subject"] = args.subject
    msg.set_content(pathlib.Path(args.body_file).read_text(encoding="utf-8"))

    for path in args.attach:
        p = pathlib.Path(path)
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        msg.add_attachment(p.read_bytes(), maintype=maintype, subtype=subtype, filename=p.name)

    print(f"From: {args.sender}\nTo: {args.to}\nSubject: {args.subject}")
    print(f"Attachments: {[pathlib.Path(a).name for a in args.attach]}")
    if args.dry_run:
        print("[dry-run] message built OK, not sent")
        return

    password = keychain_password(args.sender)
    if port == 465:
        server = smtplib.SMTP_SSL(host, port, timeout=30)
    else:
        server = smtplib.SMTP(host, port, timeout=30)
        server.starttls()
    with server:
        server.login(args.sender, password)
        server.send_message(msg)
    print("sent")


if __name__ == "__main__":
    main()
