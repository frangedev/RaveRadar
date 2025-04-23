# 🎛️ RaveRadar

![RaveRadar logo](raveradar_logo.png)

**RaveRadar** is an open-source tool designed to **detect, collect, and track songs played in YouTube videos**, with a focus on electronic music scenes like **Hard Techno**, **Rave**, and **Underground** genres. Whether you're scouting new DJ sets, tracking trends, or archiving your favorite drops — RaveRadar keeps your finger on the pulse of the beat.

---

## 🚀 Features
- 🎵 **Auto-Detect Songs**  
   Uses metadata, captions, and audio recognition to identify tracks in YouTube videos.
- 📄 **YouTube Info Parsing**  
   Extracts tracklists from video descriptions, comments, or translations when available.
- 🎧 **Audio Fingerprinting Fallback**  
   If no info is found, RaveRadar attempts to detect music via audio analysis APIs.
- 🗂️ **Organized Track Collection**  
   Automatically organizes tracks by **genre**, **DJ/Artist**, or **event**.
- 🔄 **GitHub Integration**  
   Sync and publish collected tracklists to a GitHub repository for community sharing.
- 📊 **Track Scene Changes**  
   Monitor evolving trends in the Hard Techno & Rave scene.
- ⚡ **CLI & API Ready**  
   Use from terminal or integrate into your own workflows.
- 🎵 **Playlist Export**  
   Export detected tracks to Spotify or YouTube Music playlists.
- ✏️ **Community Corrections**  
   Submit and manage track corrections with approval workflow.

---

## 🎯 Use Cases
- Track IDs from DJ sets on YouTube.
- Monitor new emerging tracks/artists in the techno scene.
- Build a public archive of rave/techno tracklists.
- Detect unknown tracks via audio recognition.
- Follow genre-specific trends over time.
- Create playlists on your favorite music platforms.
- Collaborate with the community to improve track accuracy.

---

## 📥 Installation
```bash
git clone https://github.com/frangedev/RaveRadar.git
cd RaveRadar
pip install -r requirements.txt
```

---

## ⚡ Quick Start
```bash
# Basic usage
python raveradar.py https://www.youtube.com/watch?v=VIDEO_ID

# Export to Spotify
python raveradar.py https://www.youtube.com/watch?v=VIDEO_ID --export spotify

# Export to YouTube Music
python raveradar.py https://www.youtube.com/watch?v=VIDEO_ID --export youtube
```

- RaveRadar will:
  1. Parse video info.
  2. Attempt to extract or detect songs.
  3. Save results to `/tracks/` folder.
  4. Optionally push updates to your GitHub collection.
  5. Export tracks to your preferred music platform (if requested).

---

## ⚙️ Configuration
Edit `config.yaml` for:
- API keys (e.g., ACRCloud, AudD, Shazam, Spotify, YouTube)
- GitHub repo settings
- Genre filters
- Update frequency
- Playlist export settings
- Community corrections settings

---

## 📂 Example Output
```
/tracks/
└── 2024-04-23_DJ_XYZ_RaveSet.md
```
```markdown
# DJ XYZ - Live Rave Set [23.04.2024]

## Video Details
- **Artist/DJ:** DJ XYZ
- **Date:** 2024-04-23
- **Duration:** 3600 seconds
- **Views:** 1000
- **Rating:** 4.5
- **YouTube ID:** VIDEO_ID
- **URL:** https://youtube.com/watch?v=VIDEO_ID

## Tracklist
1. Klangkuenstler – "Engels Gesang"
   - Source: acrcloud
2. Parallx – "Red Clouds"
   - Source: audd
...

## Corrections
- ✅ Track 3: Wrong Artist - Wrong Title → Correct Artist - Correct Title
  - Submitted by: username
  - Date: 2024-04-23T12:00:00
```

---

## 🎵 Playlist Export
RaveRadar can export detected tracks to:
- **Spotify**: Create playlists with automatic track matching
- **YouTube Music**: Build playlists with video links

Requirements:
- Spotify Developer account and API credentials
- YouTube API credentials
- OAuth setup for both platforms

---

## ✏️ Community Corrections
Submit and manage track corrections:
1. Submit corrections for inaccurate track info
2. Corrections are stored in `/corrections/` directory
3. Approve/reject corrections through the API
4. Approved corrections are automatically applied to tracklists

Correction format:
```json
{
  "track_number": 1,
  "original": {"artist": "Wrong Artist", "title": "Wrong Title"},
  "corrected": {"artist": "Correct Artist", "title": "Correct Title"},
  "submitter": "username",
  "timestamp": "2024-04-23T12:00:00",
  "status": "pending"
}
```

---

## 🛠️ Roadmap
- [x] Playlist export (Spotify, YouTube Music)
- [x] Community-submitted corrections
- [ ] Web interface for easier tracking
- [ ] Advanced trend analytics
- [ ] Batch processing for multiple videos
- [ ] Discord bot integration

---

## 🤝 Contributing
Feel free to fork, improve detection algorithms, or expand genre coverage!  
PRs are welcome.

---

## 📄 License
MIT License

---

## 🎚️ Stay Tuned
RaveRadar is your **underground scout** — never miss a drop again.  
Follow the project and contribute to building the ultimate techno tracklist archive!
