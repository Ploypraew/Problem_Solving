import streamlit as st

# --- Song Class (โครงสร้างเดิม เพิ่ม audio_data) ---
class Song:
    def __init__(self, title, artist, audio_data):
        self.title = title
        self.artist = artist
        self.audio_data = audio_data  # เพิ่มส่วนเก็บข้อมูลเสียง
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"

# --- MusicPlaylist Class (โครงสร้างเดิมทั้งหมด) ---
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, audio_data):
        new_song = Song(title, artist, audio_data)
        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song
        self.length += 1
        st.success(f"Added: {new_song}")

    def display_playlist(self):
        if self.head is None:
            return []

        playlist_songs = []
        current = self.head
        count = 1
        while current:
            # เพิ่มมาร์กเกอร์บอกว่าเพลงไหนกำลังเล่นอยู่
            indicator = "👉" if current == self.current_song else f"{count}."
            playlist_songs.append(f"{indicator} {current.title} by {current.artist}")
            current = current.next_song
            count += 1
        return playlist_songs

    def play_current_song(self):
        if self.current_song:
            st.info(f"Now playing: {self.current_song}")
            # เล่นเพลงจริงผ่าน Streamlit
            st.audio(self.current_song.audio_data)
        else:
            st.warning("Playlist is empty or no song is selected to play.")

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
        elif self.current_song and not self.current_song.next_song:
            st.warning("End of playlist. No next song.")
        else:
            st.warning("Playlist is empty.")

    def prev_song(self):
        if self.head is None or self.current_song is None:
            st.warning("Playlist is empty or no song is selected.")
            return
        if self.current_song == self.head:
            st.warning("Already at the beginning of the playlist.")
            return

        current = self.head
        while current.next_song != self.current_song:
            current = current.next_song
        self.current_song = current

    def get_length(self):
        return self.length

    def delete_song(self, title):
        if self.head is None:
            st.error(f"Cannot delete '{title}'. Playlist is empty.")
            return

        if self.head.title == title:
            if self.current_song == self.head:
                self.current_song = self.head.next_song
            self.head = self.head.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
            if self.length == 0:
                self.current_song = None
            return

        current = self.head
        prev = None
        while current and current.title != title:
            prev = current
            current = current.next_song

        if current:
            if self.current_song == current:
                if current.next_song:
                    self.current_song = current.next_song
                elif prev:
                    self.current_song = prev
                else:
                    self.current_song = None

            prev.next_song = current.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
        else:
            st.error(f"Song '{title}' not found in the playlist.")

# --- Streamlit App Layout (คงเดิมแต่เพิ่ม File Uploader) ---
st.title("🎶 Music Playlist App")

if 'playlist' not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

# Sidebar for adding songs
st.sidebar.header("Add New Song")
# เพิ่มส่วน Upload ไฟล์
uploaded_file = st.sidebar.file_uploader("Upload MP3 File", type=['mp3'])
new_title = st.sidebar.text_input("Title")
new_artist = st.sidebar.text_input("Artist")

if st.sidebar.button("Add Song to Playlist"):
    if new_title and new_artist and uploaded_file:
        # อ่านไฟล์เป็น bytes เพื่อเก็บลงในโหนด Song
        audio_bytes = uploaded_file.read()
        st.session_state.playlist.add_song(new_title, new_artist, audio_bytes)
        st.rerun() # รีเฟรชเพื่อให้เห็นรายการเพลงใหม่ทันที
    else:
        st.sidebar.warning("Please enter title, artist, and upload a file.")

st.sidebar.markdown("--- 🎶")
st.sidebar.header("Delete Song")
delete_title = st.sidebar.text_input("Song Title to Delete")
if st.sidebar.button("Delete Song"):
    if delete_title:
        st.session_state.playlist.delete_song(delete_title)
        st.rerun()
    else:
        st.sidebar.warning("Please enter a song title to delete.")

# Main content
st.header("Your Current Playlist")
playlist_content = st.session_state.playlist.display_playlist()
if playlist_content:
    for song_str in playlist_content:
        st.write(song_str)
else:
    st.write("Playlist is empty. Add some songs from the sidebar!")

st.markdown("--- 🎶")
st.header("Playback Controls")

# เรียกใช้งานฟังก์ชันเดิมที่แสดงผลตัวเล่นเพลง
st.session_state.playlist.play_current_song()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏪ Previous"):
        st.session_state.playlist.prev_song()
        st.rerun()

with col2:
    if st.button("▶️ Play Current"):
        # ใน streamlit การกดปุ่มจะรันโค้ดใหม่ทั้งหมดอยู่แล้ว 
        # play_current_song() ถูกเรียกด้านบนแล้ว เพลงจะเล่นตาม current_song ปัจจุบัน
        pass

with col3:
    if st.button("⏩ Next"):
        st.session_state.playlist.next_song()
        st.rerun()

st.markdown("--- 🎶")
st.write(f"Total songs in playlist: {st.session_state.playlist.get_length()} song(s)")
