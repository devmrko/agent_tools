#!/bin/bash

# .env 파일 로드, set -a로 환경변수를 설정
set -a
if [ -f "./.env" ]; then
  source "./.env"
fi
set +a

: "${APP_NAME:?APP_NAME is required}"
: "${SMTP_HOST:?SMTP_HOST is required}"
: "${SMTP_PORT:=587}"
: "${SMTP_USERNAME:?SMTP_USERNAME is required}"
: "${SMTP_PASSWORD:?SMTP_PASSWORD is required}"
: "${SMTP_FROM:?SMTP_FROM is required}"
: "${SMTP_STARTTLS:=true}"

fn config app "$APP_NAME" SMTP_HOST "$SMTP_HOST"
fn config app "$APP_NAME" SMTP_PORT "$SMTP_PORT"
fn config app "$APP_NAME" SMTP_USERNAME "$SMTP_USERNAME"
fn config app "$APP_NAME" SMTP_PASSWORD "$SMTP_PASSWORD"
fn config app "$APP_NAME" SMTP_FROM "$SMTP_FROM"
fn config app "$APP_NAME" SMTP_STARTTLS "$SMTP_STARTTLS"