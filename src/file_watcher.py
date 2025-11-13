import click
import requests
import time
from pathlib import Path
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

class LogFileWatcher:
    def __init__(self, file_path, poll_interval=2):
        self.file_path = Path(file_path)
        self.poll_interval = poll_interval
        self.last_position = 0
        
        if not self.file_path.exists():
            click.echo(f"Error: File {file_path} does not exist", err=True)
            raise FileNotFoundError(f"Log file not found: {file_path}")
    
    def read_new_lines(self):
        """only new lines from the file since last read"""
        try:
            with open(self.file_path, 'r') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()
                return new_lines
        except Exception as e:
            click.echo(f"Error reading file: {e}", err=True)
            return []
    
    def process_log_line(self, line):
        """send a log line to the API for processing"""
        line = line.strip()
        if not line:
            return
        
        try:
            data = {
                "source": "file_watcher",
                "message": line,
                "level": "INFO",
                "timestamp": datetime.now().isoformat()
            }
            response = requests.post(f"{API_BASE_URL}/logs", json=data)
            click.echo(f"Processed: {line[:60]}...")
            return response.json()
        except Exception as e:
            click.echo(f"Error processing log: {e}", err=True)
    
    def start(self):
        click.echo(f"Started watching {self.file_path}")
        click.echo(f"Poll interval: {self.poll_interval} seconds")
        
        try:
            while True:
                new_lines = self.read_new_lines()
                for line in new_lines:
                    self.process_log_line(line)
                
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            click.echo("\nFile watcher stopped")

@click.command()
@click.argument('file_path')
@click.option('--interval', default=2, help='Poll interval in seconds')
def watch_file(file_path, interval):
    """Watch a log file and process new entries"""
    watcher = LogFileWatcher(file_path, poll_interval=interval)
    watcher.start()

if __name__ == '__main__':
    watch_file()