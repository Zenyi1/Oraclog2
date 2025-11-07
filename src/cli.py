import click
import requests

API_BASE_URL = "http://localhost:8000"  # Updated to match app.py port

@click.group()
def cli():
    """Oraclog CLI - Command line interface for Oraclog API"""
    pass

# Log Management
@cli.group()
def logs():
    """Log management commands"""
    pass

@logs.command()
@click.option('--limit', default=10, help='Number of logs to retrieve')
@click.option('--offset', default=0, help='Starting offset')
@click.option('--level', help='Filter by log level')
def list(limit, offset, level):
    """List all logs"""
    params = {'limit': limit, 'offset': offset}
    if level:
        params['level'] = level
    response = requests.get(f"{API_BASE_URL}/logs", params=params)
    click.echo(response.json())

@logs.command()
@click.argument('source')
@click.argument('message')
@click.option('--level', default='INFO')
@click.argument('timestamp')
def create(source, message, level, timestamp):
    """Create a new log entry"""
    data = {
        "source": source,
        "level": level,
        "message": message,
        "timestamp": timestamp
    }
    response = requests.post(f"{API_BASE_URL}/logs", json=data)
    click.echo(response.json())

# Rules Management
@cli.group()
def rules():
    """Rule management commands"""
    pass

@rules.command()
def list():
    """List all rules"""
    response = requests.get(f"{API_BASE_URL}/rules")
    click.echo(response.json())

@rules.command()
@click.argument('keyword')
@click.option('--level', default=None)
def create(keyword, level):
    """Create a new rule"""
    data = {
        "id": 0,  # Will be set by the server
        "keyword": keyword,
        "level": level
    }
    response = requests.post(f"{API_BASE_URL}/rules", json=data)
    click.echo(response.json())

@rules.command()
@click.argument('rule_id', type=int)
def delete(rule_id):
    """Delete a rule"""
    response = requests.delete(f"{API_BASE_URL}/rules/{rule_id}")
    click.echo(response.json())

# Analysis
@cli.group()
def analyze():
    """Log analysis commands"""
    pass

@analyze.command()
@click.argument('log_id', type=int)
@click.option('--prompt', help='Optional prompt override')
def log(log_id, prompt):
    """Analyze a specific log"""
    data = {
        "log_id": log_id,
        "prompt_override": prompt
    }
    response = requests.post(f"{API_BASE_URL}/analyze", json=data)
    click.echo(response.json())

@analyze.command()
@click.option('--limit', default=10)
@click.option('--offset', default=0)
def insights(limit, offset):
    """Get analysis insights"""
    response = requests.get(
        f"{API_BASE_URL}/analyze/insights",
        params={'limit': limit, 'offset': offset}
    )
    click.echo(response.json())

if __name__ == '__main__':
    cli()