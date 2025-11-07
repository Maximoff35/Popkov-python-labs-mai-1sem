from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
STORAGE_DIR = BASE_DIR / 'storage'
LOG_FILE = STORAGE_DIR / 'shell.log'
HISTORY_FILE = STORAGE_DIR / '.history'
UNDO_FILE = STORAGE_DIR / '.undo.json'
TRASH_DIR = STORAGE_DIR / '.trash'

LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_OK_FORMAT = '[{time}] {message}'
LOG_ERROR_FORMAT = '[{time}] ERROR: {message}'
