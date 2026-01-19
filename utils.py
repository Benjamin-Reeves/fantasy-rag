"""Utility functions for the fantasy football RAG system."""
import json
from datetime import datetime


def format_player_stats(stats_dict):
    """
    Format player statistics dictionary into a readable string.
    
    Args:
        stats_dict (dict or str): Player statistics
        
    Returns:
        str: Formatted statistics
    """
    if isinstance(stats_dict, str):
        try:
            stats_dict = json.loads(stats_dict)
        except json.JSONDecodeError:
            return stats_dict
    
    formatted = []
    for key, value in stats_dict.items():
        # Convert snake_case to Title Case
        display_key = key.replace('_', ' ').title()
        formatted.append(f"{display_key}: {value}")
    
    return ", ".join(formatted)


def validate_stats_data(stats_data):
    """
    Validate statistics data.
    
    Args:
        stats_data (dict): Statistics dictionary
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(stats_data, dict):
        return False
    
    # Check that all values are numeric or can be converted
    for value in stats_data.values():
        if not isinstance(value, (int, float, str)):
            return False
    
    return True


def parse_season(season_str):
    """
    Parse season string into a standardized format.
    
    Args:
        season_str (str): Season string (e.g., "2023", "2023-2024")
        
    Returns:
        str: Standardized season string
    """
    if '-' in season_str:
        return season_str
    else:
        year = int(season_str)
        return f"{year}-{year + 1}"


def clean_text(text):
    """
    Clean text for embedding generation.
    
    Args:
        text (str): Raw text
        
    Returns:
        str: Cleaned text with normalized whitespace
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    return text.strip()


def calculate_fantasy_points(stats, scoring_system='standard'):
    """
    Calculate fantasy points based on player statistics.
    
    Args:
        stats (dict): Player statistics
        scoring_system (str): Scoring system ('standard', 'ppr', 'half-ppr')
        
    Returns:
        float: Calculated fantasy points
    """
    points = 0.0
    
    # QB scoring
    if 'passing_yards' in stats:
        points += stats.get('passing_yards', 0) * 0.04
    if 'passing_touchdowns' in stats or 'touchdowns' in stats:
        points += stats.get('passing_touchdowns', stats.get('touchdowns', 0)) * 4
    if 'interceptions' in stats:
        points -= stats.get('interceptions', 0) * 2
    
    # RB/WR/TE scoring
    if 'rushing_yards' in stats:
        points += stats.get('rushing_yards', 0) * 0.1
    if 'rushing_touchdowns' in stats:
        points += stats.get('rushing_touchdowns', 0) * 6
    if 'receiving_yards' in stats:
        points += stats.get('receiving_yards', 0) * 0.1
    if 'receiving_touchdowns' in stats:
        points += stats.get('receiving_touchdowns', 0) * 6
    
    # Receptions (varies by scoring system)
    if 'receptions' in stats:
        if scoring_system == 'ppr':
            points += stats.get('receptions', 0) * 1.0
        elif scoring_system == 'half-ppr':
            points += stats.get('receptions', 0) * 0.5
    
    # Fumbles
    if 'fumbles_lost' in stats:
        points -= stats.get('fumbles_lost', 0) * 2
    
    return round(points, 2)
