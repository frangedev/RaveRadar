import os
import pytest
from unittest.mock import Mock, patch
from raveradar import RaveRadar

@pytest.fixture
def mock_config():
    return {
        'api_keys': {
            'acrcloud': {
                'host': 'test-host',
                'access_key': 'test-key',
                'access_secret': 'test-secret'
            },
            'audd': {
                'api_token': 'test-token'
            },
            'shazam': {
                'api_key': 'test-key'
            }
        },
        'output': {
            'include_metadata': True
        }
    }

@pytest.fixture
def raveradar(mock_config):
    with patch('raveradar.RaveRadar._load_config', return_value=mock_config):
        return RaveRadar()

def test_extract_video_id(raveradar):
    # Test regular YouTube URL
    assert raveradar._extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    # Test youtu.be URL
    assert raveradar._extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    # Test direct ID
    assert raveradar._extract_video_id("dQw4w9WgXcQ") == "dQw4w9WgXcQ"

def test_deduplicate_tracks(raveradar):
    tracks = [
        {'title': 'Track 1', 'artist': 'Artist 1', 'source': 'test'},
        {'title': 'Track 1', 'artist': 'Artist 1', 'source': 'test'},  # Duplicate
        {'title': 'Track 2', 'artist': 'Artist 2', 'source': 'test'}
    ]
    
    deduped = raveradar._deduplicate_tracks(tracks)
    assert len(deduped) == 2
    assert deduped[0]['title'] == 'Track 1'
    assert deduped[1]['title'] == 'Track 2'

def test_save_tracklist(raveradar, tmp_path):
    video_info = {
        'title': 'Test Set',
        'author': 'Test DJ',
        'publish_date': '2024-04-23',
        'length': 3600,
        'views': 1000,
        'rating': 4.5,
        'description': 'Test description',
        'video_id': 'test123',
        'url': 'https://youtube.com/watch?v=test123',
        'thumbnail_url': 'https://i.ytimg.com/vi/test123/default.jpg'
    }
    
    tracks = [
        {'title': 'Track 1', 'artist': 'Artist 1', 'source': 'test'},
        {'title': 'Track 2', 'artist': 'Artist 2', 'source': 'test'}
    ]
    
    output_dir = tmp_path / "tracks"
    raveradar.save_tracklist(video_info, tracks, str(output_dir))
    
    assert output_dir.exists()
    files = list(output_dir.glob("*.md"))
    assert len(files) == 1
    
    with open(files[0]) as f:
        content = f.read()
        assert "Test Set" in content
        assert "Test DJ" in content
        assert "Track 1" in content
        assert "Track 2" in content
        assert "test123" in content
        assert "3600 seconds" in content
        assert "1000" in content
        assert "4.5" in content

@patch('raveradar.YouTube')
def test_process_video(mock_youtube, raveradar):
    # Mock YouTube object
    mock_yt = Mock()
    mock_yt.title = "Test Video"
    mock_yt.author = "Test Author"
    mock_yt.publish_date = "2024-04-23"
    mock_yt.length = 3600
    mock_yt.views = 1000
    mock_yt.rating = 4.5
    mock_yt.description = "Test description"
    mock_yt.thumbnail_url = "https://i.ytimg.com/vi/test123/default.jpg"
    mock_yt.streams.filter.return_value.first.return_value.download.return_value = None
    mock_youtube.return_value = mock_yt
    
    # Mock audio recognition results
    with patch.object(raveradar, '_detect_with_acrcloud', return_value=[]), \
         patch.object(raveradar, '_detect_with_audd', return_value=[]), \
         patch.object(raveradar, '_detect_with_shazam', return_value=[]):
        
        result = raveradar.process_video("https://youtube.com/watch?v=test123")
        assert result is not None
        assert result['video_info']['title'] == "Test Video"
        assert result['video_info']['author'] == "Test Author"
        assert result['video_info']['video_id'] == "test123"
        assert result['video_info']['views'] == 1000
        assert result['video_info']['rating'] == 4.5
        assert len(result['tracks']) == 0 