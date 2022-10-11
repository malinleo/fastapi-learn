from ..app import app
from .collect_securities import collect_securities


@app.command()
async def start_collect_securities():
    """Collect securities and overview."""
    await collect_securities.cast()
