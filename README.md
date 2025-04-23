# 🎛️ RaveRadar

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

---

## 🎯 Use Cases
- Track IDs from DJ sets on YouTube.
- Monitor new emerging tracks/artists in the techno scene.
- Build a public archive of rave/techno tracklists.
- Detect unknown tracks via audio recognition.
- Follow genre-specific trends over time.

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
python raveradar.py https://www.youtube.com/watch?v=VIDEO_ID
```
- RaveRadar will:
  1. Parse video info.
  2. Attempt to extract or detect songs.
  3. Save results to `/tracks/` folder.
  4. Optionally push updates to your GitHub collection.

---

## ⚙️ Configuration
Edit `config.yaml` for:
- API keys (e.g., ACRCloud, AudD, Shazam)
- GitHub repo settings
- Genre filters
- Update frequency

---

## 📂 Example Output
```
/tracks/
└── 2024-04-23_DJ_XYZ_RaveSet.md
```
```markdown
# DJ XYZ - Live Rave Set [23.04.2024]
1. Klangkuenstler – "Engels Gesang"
2. Parallx – "Red Clouds"
3. SNTS – "Chapter VI"
...
```

---

## 🛠️ Roadmap
- [ ] Web interface for easier tracking
- [ ] Playlist export (Spotify, YouTube Music)
- [ ] Community-submitted corrections
- [ ] Advanced trend analytics

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
