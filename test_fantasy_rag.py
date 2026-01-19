"""Tests for the fantasy football RAG system.

Note: These tests require a properly configured database and OpenAI API key.
They are designed to demonstrate the testing structure rather than be run
in a CI/CD environment without proper setup.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from utils import (
    format_player_stats,
    validate_stats_data,
    parse_season,
    clean_text,
    calculate_fantasy_points
)


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_format_player_stats_dict(self):
        """Test formatting player stats from dictionary."""
        stats = {
            'passing_yards': 300,
            'touchdowns': 3,
            'interceptions': 1
        }
        result = format_player_stats(stats)
        self.assertIn('Passing Yards: 300', result)
        self.assertIn('Touchdowns: 3', result)
        self.assertIn('Interceptions: 1', result)
    
    def test_format_player_stats_json_string(self):
        """Test formatting player stats from JSON string."""
        import json
        stats = {'passing_yards': 300}
        stats_json = json.dumps(stats)
        result = format_player_stats(stats_json)
        self.assertIn('Passing Yards: 300', result)
    
    def test_validate_stats_data_valid(self):
        """Test validation of valid stats data."""
        stats = {'yards': 100, 'touchdowns': 2}
        self.assertTrue(validate_stats_data(stats))
    
    def test_validate_stats_data_invalid(self):
        """Test validation of invalid stats data."""
        stats = "not a dict"
        self.assertFalse(validate_stats_data(stats))
    
    def test_parse_season_single_year(self):
        """Test parsing single year season."""
        result = parse_season("2023")
        self.assertEqual(result, "2023-2024")
    
    def test_parse_season_range(self):
        """Test parsing season range."""
        result = parse_season("2023-2024")
        self.assertEqual(result, "2023-2024")
    
    def test_clean_text(self):
        """Test text cleaning."""
        dirty_text = "  Hello   World  \n  with   extra   spaces  "
        clean = clean_text(dirty_text)
        self.assertEqual(clean, "Hello World with extra spaces")
    
    def test_clean_text_empty(self):
        """Test cleaning empty text."""
        result = clean_text("")
        self.assertEqual(result, "")
    
    def test_calculate_fantasy_points_qb_standard(self):
        """Test fantasy points calculation for QB in standard scoring."""
        stats = {
            'passing_yards': 300,
            'touchdowns': 3,
            'interceptions': 1
        }
        points = calculate_fantasy_points(stats, 'standard')
        # 300 * 0.04 = 12, 3 * 4 = 12, 1 * -2 = -2, Total = 22
        self.assertEqual(points, 22.0)
    
    def test_calculate_fantasy_points_rb_ppr(self):
        """Test fantasy points calculation for RB in PPR scoring."""
        stats = {
            'rushing_yards': 100,
            'rushing_touchdowns': 1,
            'receptions': 5,
            'receiving_yards': 50,
            'receiving_touchdowns': 1
        }
        points = calculate_fantasy_points(stats, 'ppr')
        # 100 * 0.1 = 10, 1 * 6 = 6, 5 * 1 = 5, 50 * 0.1 = 5, 1 * 6 = 6, Total = 32
        self.assertEqual(points, 32.0)
    
    def test_calculate_fantasy_points_half_ppr(self):
        """Test fantasy points calculation in half-PPR scoring."""
        stats = {
            'receptions': 10,
            'receiving_yards': 100,
        }
        points = calculate_fantasy_points(stats, 'half-ppr')
        # 10 * 0.5 = 5, 100 * 0.1 = 10, Total = 15
        self.assertEqual(points, 15.0)


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    @patch.dict('os.environ', {
        'DB_HOST': 'testhost',
        'DB_PORT': '5433',
        'DB_NAME': 'testdb',
        'DB_USER': 'testuser',
        'DB_PASSWORD': 'testpass',
        'OPENAI_API_KEY': 'test-key',
        'VECTOR_DIMENSION': '1536'
    })
    def test_config_from_env(self):
        """Test configuration loading from environment."""
        from config import Config
        config = Config()
        self.assertEqual(config.DB_HOST, 'testhost')
        self.assertEqual(config.DB_PORT, 5433)
        self.assertEqual(config.DB_NAME, 'testdb')
        self.assertEqual(config.DB_USER, 'testuser')
        self.assertEqual(config.DB_PASSWORD, 'testpass')
        self.assertEqual(config.OPENAI_API_KEY, 'test-key')
        self.assertEqual(config.VECTOR_DIMENSION, 1536)


class TestEmbeddingService(unittest.TestCase):
    """Test embedding service."""
    
    @patch('embeddings.OpenAI')
    def test_generate_embedding(self, mock_openai):
        """Test single embedding generation."""
        from embeddings import EmbeddingService
        
        # Mock the OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        service = EmbeddingService()
        service.client = mock_client
        
        result = service.generate_embedding("test text")
        self.assertEqual(result, [0.1, 0.2, 0.3])
        mock_client.embeddings.create.assert_called_once()


if __name__ == '__main__':
    unittest.main()
