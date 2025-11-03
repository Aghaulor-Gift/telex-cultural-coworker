#!/bin/bash
# Run, stop, or restart the Telex Cultural Coworker FastAPI app

APP_NAME="telex-cultural-coworker"
VENV_PATH="telex_venv"
UVICORN_CMD="uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

activate_venv() {
    if [ -d "$VENV_PATH" ]; then
        source "$VENV_PATH/bin/activate"
    else
        echo "Virtual environment not found at $VENV_PATH"
        exit 1
    fi
}

start_app() {
    echo " Starting $APP_NAME..."
    activate_venv
    $UVICORN_CMD
}

stop_app() {
    echo "Stopping $APP_NAME..."
    pkill -f "uvicorn app.main:app" && echo "Stopped successfully" || echo "No running process found"
}

restart_app() {
    stop_app
    echo " Restarting $APP_NAME..."
    start_app
}

case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    *)
        echo "Usage: ./run.sh {start|stop|restart}"
        exit 1
        ;;
esac
