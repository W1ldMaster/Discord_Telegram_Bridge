import asyncio
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class MediaFile:
    url: Optional[str] = None
    file_path: Optional[str] = None
    file_id: Optional[str] = None
    type: Optional[str] = None
    duration: Optional[int] = None


@dataclass
class Message:
    source: str
    username: str
    text: str
    media: List[MediaFile] = field(default_factory=list)


message_queue = asyncio.Queue()
