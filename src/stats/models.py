from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class PlayerStatsDocument:
    content: str
    embedding: list[float]

    player_name: str
    position: str
    week: int
    season: int
    id: Optional[int] = None
    player_id: Optional[str] = None
    team: Optional[str] = None

    # Key stats for filtering
    fantasy_points_ppr: Optional[float] = None
    fantasy_points_std: Optional[float] = None

    # Position-specific stats
    passing_yards: Optional[int] = None
    passing_tds: Optional[int] = None
    rushing_yards: Optional[int] = None
    rushing_tds: Optional[int] = None
    receptions: Optional[int] = None
    receiving_yards: Optional[int] = None
    receiving_tds: Optional[int] = None
    targets: Optional[int] = None

    created_at: Optional[datetime] = None
    