#!/bin/sh
set -e

ENV_CONFIG="/usr/share/nginx/html/env-config.js"

cat > "$ENV_CONFIG" <<'EOJS'
window.__ENV__ = {
EOJS

env | grep '^VITE_' | while IFS='=' read -r key value; do
  echo "  \"$key\": \"$value\"," >> "$ENV_CONFIG"
done

echo "};" >> "$ENV_CONFIG"
