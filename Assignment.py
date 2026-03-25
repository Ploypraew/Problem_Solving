import streamlit as st

# --- 1. Data Structures ---

class MovieNode:
    def __init__(self, movie_name):
        self.movie_name = movie_name
        self.next = None

class CinemaLogic:
    """คลาสจัดการ Logic เบื้องหลัง (Linked List & 2D Array)"""
    def __init__(self, rows=5, cols=8):
        self.head = None
        self.rows = rows
        self.cols = cols
        self.seats = [[0 for _ in range(cols)] for _ in range(rows)]

    def add_movie(self, name):
        new_node = MovieNode(name)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get_all_movies(self):
        movies = []
        current = self.head
        while current:
            movies.append(current.movie_name)
            current = current.next
        return movies

    def remove_movie(self, name):
        current = self.head
        prev = None
        while current and current.movie_name != name:
            prev = current
            current = current.next
        if current:
            if not prev:
                self.head = current.next
            else:
                prev.next = current.next

# --- 2. Streamlit UI Setup ---

st.set_page_config(page_title="Cinema Management System", layout="wide")
st.title("🎬 Cinema Management System")

# ใช้ Session State เพื่อเก็บข้อมูลไว้ในหน่วยความจำของ Browser
if 'cinema' not in st.session_state:
    st.session_state.cinema = CinemaLogic(rows=6, cols=10)

cinema = st.session_state.cinema

# --- 3. Sidebar: Movie Management (Linked List) ---
st.sidebar.header("🎥 จัดการข้อมูลภาพยนตร์")
new_movie = st.sidebar.text_input("ชื่อหนังใหม่")
if st.sidebar.button("เพิ่มหนัง"):
    if new_movie:
        cinema.add_movie(new_movie)
        st.sidebar.success(f"เพิ่ม {new_movie} แล้ว")
    else:
        st.sidebar.error("กรุณาใส่ชื่อหนัง")

all_movies = cinema.get_all_movies()
if all_movies:
    movie_to_delete = st.sidebar.selectbox("เลือกหนังที่ต้องการลบ", all_movies)
    if st.sidebar.button("ลบหนังเรื่องนี้"):
        cinema.remove_movie(movie_to_delete)
        st.rerun()
else:
    st.sidebar.info("ยังไม่มีหนังในระบบ")

# --- 4. Main Area: Seat Management (2D Array) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💺 ผังที่นั่งในโรงภาพยนตร์")
    
    # แสดงผล Visual ด้วยปุ่มหรือตาราง
    for r in range(cinema.rows):
        cols_ui = st.columns(cinema.cols)
        for c in range(cinema.cols):
            status = cinema.seats[r][c]
            label = f"{r},{c}"
            
            # กำหนดสีตามสถานะ
            if status == 1: # จอง
                btn_type = "primary" # สีแดง/น้ำเงินเด่น
                icon = "🔴"
            elif status == 2: # พัง
                btn_type = "secondary"
                icon = "⚠️"
            else:
                btn_type = "secondary"
                icon = "⬜"
            
            if cols_ui[c].button(f"{icon}\n{label}", key=f"btn_{r}_{c}"):
                # คลิกเพื่อวนสถานะ: ว่าง -> จอง -> พัง -> ว่าง
                cinema.seats[r][c] = (status + 1) % 3
                st.rerun()

    st.caption("คำอธิบาย: ⬜ ว่าง | 🔴 จองแล้ว | ⚠️ ที่นั่งชำรุด (คลิกที่ที่นั่งเพื่อเปลี่ยนสถานะ)")

with col2:
    st.subheader("🛠️ รายงานสำหรับเจ้าหน้าที่")
    
    # ค้นหาชื่อหนัง (Linear Search)
    search_query = st.text_input("🔍 ค้นหาชื่อหนังในระบบ")
    if search_query:
        found = False
        for idx, m in enumerate(all_movies):
            if search_query.lower() in m.lower():
                st.write(f"✅ พบหนัง: **{m}** (ลำดับที่ {idx+1})")
                found = True
        if not found:
            st.warning("ไม่พบชื่อหนังที่ค้นหา")

    st.divider()

    # ค้นหาที่นั่งพัง (Linear Search ใน 2D Array)
    if st.button("🔍 ตรวจสอบที่นั่งชำรุด"):
        broken = []
        for r in range(cinema.rows):
            for c in range(cinema.cols):
                if cinema.seats[r][c] == 2:
                    broken.append(f"แถว {r} หลัก {c}")
        
        if broken:
            st.error(f"พบที่นั่งชำรุด {len(broken)} จุด:")
            for b in broken:
                st.write(f"- {b}")
        else:
            st.success("ไม่พบที่นั่งชำรุดในขณะนี้")
