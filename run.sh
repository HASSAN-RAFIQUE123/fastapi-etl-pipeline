#!/bin/bash
set -e
cd "$(dirname "$0")"
exec "$(pwd)/.venv/bin/python" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
