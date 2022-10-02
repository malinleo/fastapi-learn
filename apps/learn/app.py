import enum
from config.main import app
from pydantic import BaseModel


class ItemType(str, enum.Enum):
    """Item types."""
    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"


class Item(BaseModel):
    """Some item for API."""
    name: str
    description: str | None
    quantity: int
    item_type: ItemType


@app.get("/")
async def root(item: Item):
    return item