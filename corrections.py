#!/usr/bin/env python3
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class TrackCorrections:
    def __init__(self, corrections_dir: str = "corrections"):
        """Initialize track corrections handler."""
        self.corrections_dir = Path(corrections_dir)
        self.corrections_dir.mkdir(exist_ok=True)
        
    def _get_corrections_file(self, video_id: str) -> Path:
        """Get the path to the corrections file for a video."""
        return self.corrections_dir / f"{video_id}_corrections.json"
        
    def submit_correction(self, video_id: str, track_number: int, 
                         correction: Dict, submitter: str) -> bool:
        """Submit a correction for a track."""
        try:
            corrections_file = self._get_corrections_file(video_id)
            corrections = self._load_corrections(video_id)
            
            correction_data = {
                'track_number': track_number,
                'original': correction.get('original', {}),
                'corrected': correction.get('corrected', {}),
                'submitter': submitter,
                'timestamp': datetime.now().isoformat(),
                'status': 'pending'
            }
            
            corrections.append(correction_data)
            
            with open(corrections_file, 'w') as f:
                json.dump(corrections, f, indent=2)
                
            return True
        except Exception as e:
            logger.error(f"Failed to submit correction: {e}")
            return False
            
    def _load_corrections(self, video_id: str) -> List[Dict]:
        """Load corrections for a video."""
        corrections_file = self._get_corrections_file(video_id)
        if corrections_file.exists():
            with open(corrections_file) as f:
                return json.load(f)
        return []
        
    def get_corrections(self, video_id: str) -> List[Dict]:
        """Get all corrections for a video."""
        return self._load_corrections(video_id)
        
    def approve_correction(self, video_id: str, correction_index: int) -> bool:
        """Approve a correction."""
        try:
            corrections = self._load_corrections(video_id)
            if 0 <= correction_index < len(corrections):
                corrections[correction_index]['status'] = 'approved'
                
                with open(self._get_corrections_file(video_id), 'w') as f:
                    json.dump(corrections, f, indent=2)
                    
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to approve correction: {e}")
            return False
            
    def reject_correction(self, video_id: str, correction_index: int) -> bool:
        """Reject a correction."""
        try:
            corrections = self._load_corrections(video_id)
            if 0 <= correction_index < len(corrections):
                corrections[correction_index]['status'] = 'rejected'
                
                with open(self._get_corrections_file(video_id), 'w') as f:
                    json.dump(corrections, f, indent=2)
                    
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to reject correction: {e}")
            return False
            
    def apply_corrections(self, video_id: str, tracklist: List[Dict]) -> List[Dict]:
        """Apply approved corrections to a tracklist."""
        corrections = self._load_corrections(video_id)
        approved_corrections = [c for c in corrections if c['status'] == 'approved']
        
        for correction in approved_corrections:
            track_number = correction['track_number']
            if 0 <= track_number - 1 < len(tracklist):
                tracklist[track_number - 1].update(correction['corrected'])
                
        return tracklist 