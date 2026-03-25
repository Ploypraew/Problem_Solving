import streamlit as st

# --- 1. Data Structures ---

class MovieNode:
    def __init__(self, movie_name, rows=5, cols=8):
        self.movie_name = movie_name
        # สร้าง 2D Array แยกสำหรับหนังแต่ละเรื่อง
        self.seats = [[0 for _ in range(cols)] for _ in range(rows)]
        self.next = None

class CinemaLogic:
    def __init__(self):
        self.head = None
        self.rows = 6
        self.cols = 10

    def add_movie(self, name):
        new_node = MovieNode(name, self.rows, self.cols)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get_movie_node(self, name):
        """ค้นหา Node ของหนังเพื่อดึงข้อมูลที่นั่ง (Linear Search)"""
        current = self.head
        while current:
            if current.movie_name == name:
                return current
            current = current.next
        return None

    def get_all_movies(self):
        movies = []
        current = self.head
        while current:
            movies.append(current.movie_name)
            current = current.next
        return movies

# --- 2. Streamlit UI Setup ---

st.set_page_config(page_title="Cinema Admin Pro", layout="wide")
st.title("🎬 ระบบจัดการโรงภาพยนตร์ (รายเรื่อง)")

if 'cinema' not in st.session_state:
    st.session_state.cinema = CinemaLogic()

cinema = st.session_state.cinema

# --- 3. Sidebar: Management ---
st.sidebar.header("⚙️ ตั้งค่าระบบ")
new_movie = st.sidebar.text_input("เพิ่มชื่อหนังใหม่")
if st.sidebar.button("ยืนยันการเพิ่มหนัง"):
    if new_movie:
        cinema.add_movie(new_movie)
        st.rerun()

all_movies = cinema.get_all_movies()

# --- 4. Main Interface ---
if not all_movies:
    st.info("กรุณาเพิ่มชื่อหนังที่แถบด้านซ้ายเพื่อเริ่มต้นระบบ")
else:
    # เลือกหนังที่จะจัดการ
    selected_movie_name = st.selectbox("เลือกภาพยนตร์ที่ต้องการจัดการที่นั่ง:", all_movies)
    movie_node = cinema.get_movie_node(selected_movie_name)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"💺 ผังที่นั่ง: {selected_movie_name}")
        
        # แสดงผลและแก้ไขสถานะ
        for r in range(cinema.rows):
            cols_ui = st.columns(cinema.cols)
            for c in range(cinema.cols):
                status = movie_node.seats[r][c]
                label = f"{r},{c}"
                
                # เงื่อนไขสีและไอคอน
                if status == 1: # จองแล้ว (สีแดง)
                    icon, color = "🔴", "red"
                    disabled = True  # ล็อกไว้แก้ไขไม่ได้
                elif status == 2: # พัง (สีเหลือง)
                    icon, color = "⚠️", "orange"
                    disabled = False # แก้ไขได้
                else: # ว่าง
                    icon, color = "⬜", "gray"
                    disabled = False # แก้ไขได้ (เพื่อแจ้งพัง)

                # ปุ่มกดที่นั่ง
                if cols_ui[c].button(f"{icon}\n{label}", key=f"seat_{selected_movie_name}_{r}_{c}", disabled=disabled):
                    # Logic: ถ้าว่าง (0) -> กดแล้วเป็น พัง (2) | ถ้าพัง (2) -> กดแล้วกลับเป็น ว่าง (0)
                    movie_node.seats[r][c] = 2 if status == 0 else 0
                    st.rerun()

        st.caption("หมายเหตุ: 🔴 ที่นั่งจองแล้ว (แก้ไขไม่ได้) | ⚠️ ที่นั่งชำรุด (คลิกเพื่อแจ้งซ่อม/คืนสถานะ) | ⬜ ที่นั่งปกติ")

    with col2:
        st.subheader("📋 รายงานสถานะ")
        
        # 1. ค้นหาที่นั่งพัง (Linear Search ใน 2D Array)
        st.write("**ที่นั่งที่ต้องแจ้งซ่อม:**")
        broken_found = []
        for r in range(cinema.rows):
            for c in range(cinema.cols):
                if movie_node.seats[r][c] == 2:
                    broken_found.append(f"แถว {r}-คอลัมน์ {c}")
        
        if broken_found:
            for item in broken_found:
                st.warning(f"📍 {item}")
            if st.button("ยืนยันการซ่อมเสร็จทั้งหมด"):
                for r in range(cinema.rows):
                    for c in range(cinema.cols):
                        if movie_node.seats[r][c] == 2:
                            movie_node.seats[r][c] = 0
                st.rerun()
        else:
            st.success("ไม่มีที่นั่งชำรุด")

        st.divider()
        
        # 2. จำลองการจอง (เพื่อทดสอบการ Lock ที่นั่ง)
        st.write("**จำลองการจอง (Admin Only):**")
        r_in = st.number_input("แถว", 0, cinema.rows-1, key="r_in")
        c_in = st.number_input("หลัก", 0, cinema.cols-1, key="c_in")
        if st.button("จองที่นั่งนี้ (Lock)"):
            if movie_node.seats[r_in][c_in] == 0:
                movie_node.seats[r_in][c_in] = 1
                st.rerun()
            else:
                st.error("ที่นั่งไม่ว่างหรือชำรุด")
