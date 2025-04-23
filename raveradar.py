#!/usr/bin/env python3
import os
import sys
import yaml
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from pytube import YouTube
from acrcloud.recognizer import ACRCloudRecognizer
from audd import API
from shazamio import Shazam
from playlist_exporter import PlaylistExporter
from corrections import TrackCorrections

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RaveRadar:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize RaveRadar with configuration."""
        self.config = self._load_config(config_path)
        self.acr = self._init_acrcloud()
        self.audd = self._init_audd()
        self.shazam = Shazam()
        self.playlist_exporter = PlaylistExporter(config_path)
        self.corrections = TrackCorrections()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            sys.exit(1)

    def _init_acrcloud(self) -> ACRCloudRecognizer:
        """Initialize ACRCloud recognizer."""
        config = self.config['api_keys']['acrcloud']
        return ACRCloudRecognizer({
            'host': config['host'],
            'access_key': config['access_key'],
            'access_secret': config['access_secret'],
            'timeout': 10
        })

    def _init_audd(self) -> API:
        """Initialize AudD API."""
        return API(self.config['api_keys']['audd']['api_token'])

    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL."""
        if 'youtube.com' in url:
            return url.split('v=')[1].split('&')[0]
        elif 'youtu.be' in url:
            return url.split('/')[-1]
        return url

    def process_video(self, video_url: str) -> Dict:
        """Process a YouTube video to detect tracks."""
        try:
            # Extract video ID
            video_id = self._extract_video_id(video_url)
            
            # Download video
            yt = YouTube(video_url)
            video_info = {
                'title': yt.title,
                'author': yt.author,
                'publish_date': yt.publish_date,
                'length': yt.length,
                'views': yt.views,
                'rating': yt.rating,
                'description': yt.description,
                'video_id': video_id,
                'url': video_url,
                'thumbnail_url': yt.thumbnail_url
            }
            
            # Extract audio
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_path = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            audio_stream.download(filename=audio_path)
            
            # Try different recognition methods
            tracks = []
            try:
                tracks.extend(self._detect_with_acrcloud(audio_path))
            except Exception as e:
                logger.warning(f"ACRCloud detection failed: {e}")
            
            try:
                tracks.extend(self._detect_with_audd(audio_path))
            except Exception as e:
                logger.warning(f"AudD detection failed: {e}")
            
            try:
                tracks.extend(self._detect_with_shazam(audio_path))
            except Exception as e:
                logger.warning(f"Shazam detection failed: {e}")
            
            # Clean up
            os.remove(audio_path)
            
            # Apply corrections if enabled
            if self.config['corrections']['enabled']:
                tracks = self.corrections.apply_corrections(video_id, tracks)
            
            return {
                'video_info': video_info,
                'tracks': self._deduplicate_tracks(tracks)
            }
            
        except Exception as e:
            logger.error(f"Failed to process video: {e}")
            return None

    def _detect_with_acrcloud(self, audio_path: str) -> List[Dict]:
        """Detect tracks using ACRCloud."""
        result = self.acr.recognize_by_file(audio_path, 0)
        if result and 'metadata' in result:
            return [{
                'title': track['title'],
                'artist': track['artists'][0]['name'],
                'source': 'acrcloud'
            } for track in result['metadata']['music']]
        return []

    def _detect_with_audd(self, audio_path: str) -> List[Dict]:
        """Detect tracks using AudD."""
        result = self.audd.recognize(audio_path)
        if result and 'result' in result:
            return [{
                'title': result['result']['title'],
                'artist': result['result']['artist'],
                'source': 'audd'
            }]
        return []

    def _detect_with_shazam(self, audio_path: str) -> List[Dict]:
        """Detect tracks using Shazam."""
        result = self.shazam.recognize_song(audio_path)
        if result and 'track' in result:
            return [{
                'title': result['track']['title'],
                'artist': result['track']['subtitle'],
                'source': 'shazam'
            }]
        return []

    def _deduplicate_tracks(self, tracks: List[Dict]) -> List[Dict]:
        """Remove duplicate tracks based on title and artist."""
        seen = set()
        unique_tracks = []
        for track in tracks:
            key = (track['title'].lower(), track['artist'].lower())
            if key not in seen:
                seen.add(key)
                unique_tracks.append(track)
        return unique_tracks

    def save_tracklist(self, video_info: Dict, tracks: List[Dict], output_dir: str = "tracks"):
        """Save detected tracks to a markdown file."""
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{datetime.now().strftime('%Y-%m-%d')}_{video_info['author']}_{video_info['title']}.md"
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))
        
        with open(os.path.join(output_dir, filename), 'w') as f:
            # Write video information
            f.write(f"# {video_info['title']}\n\n")
            f.write(f"## Video Details\n")
            f.write(f"- **Artist/DJ:** {video_info['author']}\n")
            f.write(f"- **Date:** {video_info['publish_date']}\n")
            f.write(f"- **Duration:** {video_info['length']} seconds\n")
            f.write(f"- **Views:** {video_info['views']}\n")
            f.write(f"- **Rating:** {video_info['rating']}\n")
            f.write(f"- **YouTube ID:** {video_info['video_id']}\n")
            f.write(f"- **URL:** {video_info['url']}\n\n")
            
            # Write tracklist
            f.write("## Tracklist\n\n")
            for i, track in enumerate(tracks, 1):
                f.write(f"{i}. {track['artist']} - {track['title']}\n")
                if self.config['output']['include_metadata']:
                    f.write(f"   - Source: {track['source']}\n")
                    
            # Add corrections section if enabled
            if self.config['corrections']['enabled']:
                corrections = self.corrections.get_corrections(video_info['video_id'])
                if corrections:
                    f.write("\n## Corrections\n\n")
                    for correction in corrections:
                        status = "✅" if correction['status'] == 'approved' else "⏳" if correction['status'] == 'pending' else "❌"
                        f.write(f"- {status} Track {correction['track_number']}: ")
                        f.write(f"{correction['original'].get('artist', '?')} - {correction['original'].get('title', '?')} ")
                        f.write(f"→ {correction['corrected'].get('artist', '?')} - {correction['corrected'].get('title', '?')}\n")
                        f.write(f"  - Submitted by: {correction['submitter']}\n")
                        f.write(f"  - Date: {correction['timestamp']}\n")

    def export_playlist(self, tracks: List[Dict], playlist_name: str, platform: Optional[str] = None) -> Optional[str]:
        """Export tracks to a playlist on the specified platform."""
        if platform is None:
            platform = self.config['playlist']['default_platform']
        return self.playlist_exporter.export_playlist(tracks, playlist_name, platform)

def main():
    if len(sys.argv) < 2:
        print("Usage: python raveradar.py <youtube_url> [--export <platform>]")
        sys.exit(1)
        
    video_url = sys.argv[1]
    export_platform = None
    
    if len(sys.argv) > 2 and sys.argv[2] == '--export':
        if len(sys.argv) > 3:
            export_platform = sys.argv[3]
        else:
            print("Please specify a platform (spotify or youtube)")
            sys.exit(1)
    
    radar = RaveRadar()
    
    result = radar.process_video(video_url)
    if result:
        radar.save_tracklist(result['video_info'], result['tracks'])
        print("Tracklist saved successfully!")
        
        if export_platform:
            playlist_url = radar.export_playlist(result['tracks'], result['video_info']['title'], export_platform)
            if playlist_url:
                print(f"Playlist exported successfully: {playlist_url}")
            else:
                print("Failed to export playlist")
    else:
        print("Failed to process video.")

if __name__ == "__main__":
    main() 