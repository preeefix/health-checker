# health-checker

This is a simple health checking application. It's output is directly to the console.

## Running `health-checker`

There are several different ways depending on how involved you wish to get: Locally, Compiled, via Docker, and via Kubernetes.

### `local file`

- Requirements: Python 3
- Assmptions: A Linux-like environment

1. Clone the git repository to your local machine
   - `git clone https://github.com/preeefix/health-checker && cd health-checker`
2. Create a virtual environment to contain the dependencies and activate it.
   - `python3 -m venv venv`
   - `source venv/bin/activate`
3. Install the required dependencies
   - `python3 -m pip install -r requirements.txt`
4. Copy the test configuration and modify as you please
   - `cp test.config.yaml config.yaml`
5. Execute and enjoy!
   - `python3 health-checker.py`

### Compiled

Checkout the latest [release](https://github.com/preeefix/health-checker/releases) for your platform and create a `config.yaml` following the example in [`test.config.yaml`](./test.config.yaml)

Execute simply with `health-checker config.yaml`

### Docker

`health-checker` is available as `ghcr.io/preeefix/health-checker`. Both `amd64` and `arm64` are target platforms (because MacBooks are a thing).

The config file is expected to be mounted as `/config/config.yaml`.

Example
```
docker run -v config.yaml:/config/config.yaml ghcr.io/preeefix/health-checker
```

### Kubernetes

A sample kubernetes manifest is available as `kube.yaml`.