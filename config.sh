
#!/bin/bash
set -a
if [ -f "./.env" ]; then
  source "./.env"
fi
set +a

: "${APP_NAME:?APP_NAME is required}"

fn inspect app "$APP_NAME"
fn list functions "$APP_NAME"
fn inspect function "$APP_NAME" send-email