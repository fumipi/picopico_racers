#!/bin/bash

# Git push with retry logic
# Usage: ./git_push_retry.sh [max_retries] [delay_seconds]

MAX_RETRIES=${1:-5}
DELAY=${2:-10}
RETRY_COUNT=0

echo "Attempting to push to GitHub (max retries: $MAX_RETRIES, delay: ${DELAY}s)"

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo ""
    echo "Attempt $((RETRY_COUNT + 1))/$MAX_RETRIES..."
    
    if git push; then
        echo "✓ Push successful!"
        exit 0
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "✗ Push failed. Retrying in ${DELAY} seconds..."
            sleep $DELAY
        else
            echo "✗ Push failed after $MAX_RETRIES attempts."
            echo ""
            echo "Troubleshooting suggestions:"
            echo "1. Check your internet connection"
            echo "2. Verify GitHub is accessible: ping github.com"
            echo "3. Try using SSH instead of HTTPS:"
            echo "   git remote set-url origin git@github.com:fumipi/picopico_racers.git"
            exit 1
        fi
    fi
done

