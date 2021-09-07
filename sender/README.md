# Sender software

- Work out-of-box with [Makelangelo-firmware](https://github.com/MarginallyClever/Makelangelo-firmware)

  Tested with MEGA2560 + RAMPS1.4

- Send G-code to the Makelangelo firmware

## Usage

See [`example.py`](./example.py)


## Development

**Requirements**

- Python `>=3.7`
- poetry

**Prepare**
```bash
poetry install
```

**Run Tests**
```bash
poetry run pytest
```

**Run Example**
```bash
poetry run python example.py
```
