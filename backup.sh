
#!/bin/bash
set -euo pipefail

# Week 4 - Automatic website backup
# Server A -> Server B

SOURCE="/var/www/html/"
DEST="webbackup@192.168.1.55"
BACKUP_DIR="/srv/backups/website"
KEY="/home/ubuntu/.ssh/week4_backup_ed25519"
LOG="/home/ubuntu/week4-backups.log"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
SSH_CMD="ssh -T -i $KEY -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes"

echo "$(date -Is) Starting backup: $TIMESTAMP" >> "$LOG"

if rsync -a \
    --no-owner --no-group --no-perms \
    -e "$SSH_CMD" \
    "$SOURCE" \
    "$DEST:$BACKUP_DIR/$TIMESTAMP/" >> "$LOG" 2>&1
then
    echo "$(date -Is) SUCCESS: $TIMESTAMP" >> "$LOG"
else
    echo "$(date -Is) ERROR: $TIMESTAMP" >> "$LOG"
    exit 1
fi
