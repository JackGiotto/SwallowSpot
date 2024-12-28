import os

def read_env_file(filepath):
    """Reads a .env file and sets environment variables."""
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f'{filepath} not found.')

    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            value = value.replace('"', '')
            os.environ[key.strip()] = value.strip()
    
    #print(os.environ)