import streamlit as st

# --- 1. โครงสร้างข้อมูล (Data Structures) ---

class CinemaShowtime:
    def __init__(self, time, price):
        self.time = time
        self.price = price
        # 2D Array: 0=ว่าง, 1=จองแล้ว, 2=ชำรุด (Maintenance)
        self.seats = [[0 for _ in range(10)] for _ in range(5)]
        self.next_showtime = None # Pointer สำหรับ Linked List ของรอบฉาย

class Movie:
    def __init__(self, title):
        self.title = title
        self.head_showtime = None # Head ของ Linked List รอบฉาย

    def add_showtime(self, time, price):
        new_show = CinemaShowtime(time, price)
        if not self.head_showtime:
            self.head_showtime = new_show
        else:
            current = self.head_showtime
            while current.next_showtime:
                current = current.next_showtime
            current.next_showtime = new_show

    def delete_showtime(self, time_str):
        if not self.head_showtime: return
        if self.head_showtime.time == time_str:
            self.head_showtime = self.head_showtime.next_showtime
            return
        current = self.head_showtime
        while current.next_showtime and current.next_showtime.time != time_str:
            current = current.next_showtime
        if current.next_showtime:
            current.next_showtime = current.next_showtime.next_showtime

# --- 2. การจัดการสถานะระบบ (Initial Session) ---

def init_session():
    if 'movies' not in st.session_state:
        # สร้างข้อมูลตัวอย่างเริ่มต้น
        m1 = Movie("Dune: Part Two")
        m1.add_showtime("11:00", 250)
        m1.add_showtime("14:30", 250)
        st.session_state.movies = {m1.title: m1}

    if 'rows' not in st.session_state:
        st.session_state.rows = ["A", "B", "C", "D", "E"]

    if 'temp_selection' not in st.session_state:
        st.session_state.temp_selection = []

# --- 3. ส่วนสำหรับลูกค้า (Customer Mode) ---

def customer_view():
    st.header("🎟️ จองตั๋วภาพยนตร์")

    movie_names = list(st.session_state.movies.keys())
    selected_name = st.selectbox("เลือกภาพยนตร์", movie_names)
    movie = st.session_state.movies[selected_name]

    # ดึงรอบฉายจาก Linked List มาแสดงใน Slider
    showtimes = []
    curr = movie.head_showtime
    while curr:
        showtimes.append(curr)
        curr = curr.next_showtime

    if not showtimes:
        st.warning("ยังไม่มีรอบฉายสำหรับเรื่องนี้")
        return

    selected_show = st.select_slider("เลือกรอบเวลา", options=showtimes, format_func=lambda x: x.time)

    st.subheader(f"ผังที่นั่ง: {selected_name} ({selected_show.time})")
    st.caption("⬜ ว่าง | 🔴 จองแล้ว | 🚧 ชำรุด | ✅ เลือกอยู่")

    st.markdown("<div style='background-color:#333;color:white;text-align:center;padding:10px;margin-bottom:15px'>SCREEN</div>", unsafe_allow_html=True)

    # วาดที่นั่งด้วย 2D Array
    for r_idx, row_name in enumerate(st.session_state.rows):
        cols = st.columns([1] + [1]*10)
        cols[0].write(f"**{row_name}**")
        for c_idx in range(10):
            status = selected_show.seats[r_idx][c_idx]
            seat_id = f"{row_name}{c_idx+1}"

            if status == 1:
                cols[c_idx+1].write("🔴")
            elif status == 2:
                cols[c_idx+1].write("🚧")
            else:
                is_sel = seat_id in st.session_state.temp_selection
                if cols[c_idx+1].button("✅" if is_sel else "⬜", key=f"c_{seat_id}"):
                    if is_sel: st.session_state.temp_selection.remove(seat_id)
                    else: st.session_state.temp_selection.append(seat_id)
                    st.rerun()

    if st.session_state.temp_selection:
        st.divider()
        st.subheader("สรุปการจอง")
        count = len(st.session_state.temp_selection)
        total = count * selected_show.price
        st.write(f"**ที่นั่ง:** {', '.join(st.session_state.temp_selection)}")
        st.write(f"**ราคารวม:** {total:,} บาท")
        if st.button("ยืนยันการจองทั้งหมด", type="primary"):
            for s in st.session_state.temp_selection:
                r, c = st.session_state.rows.index(s[0]), int(s[1:])-1
                selected_show.seats[r][c] = 1 # Update 2D Array
            st.session_state.temp_selection = []
            st.success("จองที่นั่งสำเร็จ!")
            st.rerun()

# --- 4. ส่วนสำหรับผู้ให้บริการ (Admin Mode) ---

def admin_view():
    st.header("⚙️ ระบบจัดการหลังบ้าน")

    tab1, tab2 = st.tabs(["เพิ่มหนัง/รอบฉาย", "จัดการผังที่นั่งชำรุด"])

    with tab1:
        st.subheader("เพิ่มภาพยนตร์ใหม่")
        new_title = st.text_input("ชื่อหนัง")
        if st.button("บันทึกภาพยนตร์"):
            if new_title:
                st.session_state.movies[new_title] = Movie(new_title)
                st.success("เพิ่มหนังเรียบร้อย")
                st.rerun()

        st.divider()
        movie_list = list(st.session_state.movies.keys())
        if movie_list:
            target = st.selectbox("เลือกหนังเพื่อเพิ่มรอบ", movie_list)
            m = st.session_state.movies[target]
            col_t, col_p = st.columns(2)
            at = col_t.text_input("เวลาฉาย (เช่น 19:00)")
            ap = col_p.number_input("ราคาต่อที่นั่ง", min_value=0, value=200)
            if st.button("เพิ่มรอบฉาย"):
                m.add_showtime(at, ap)
                st.rerun()

    with tab2:
        movie_list = list(st.session_state.movies.keys())
        if not movie_list: return
        target_m = st.selectbox("เลือกหนังที่ต้องการจัดการ", movie_list, key="adm_m")
        m = st.session_state.movies[target_m]

        shows = []
        curr = m.head_showtime
        while curr:
            shows.append(curr)
            curr = curr.next_showtime

        if shows:
            sel_s = st.selectbox("เลือกรอบเวลา", shows, format_func=lambda x: x.time)

            # แก้ราคาและลบรอบ
            c1, c2 = st.columns(2)
            new_p = c1.number_input("แก้ไขราคาตั๋ว", value=sel_s.price)
            if c1.button("อัปเดตราคา"):
                sel_s.price = new_p
                st.success("อัปเดตแล้ว")

            if c2.button("ลบรอบฉายนี้", type="secondary"):
                m.delete_showtime(sel_s.time)
                st.rerun()

            st.divider()
            st.subheader("ระบุที่นั่งชำรุด (Maintenance)")
            for r_idx, row_name in enumerate(st.session_state.rows):
                cols = st.columns([1] + [1]*10)
                cols[0].write(row_name)
                for c_idx in range(10):
                    val = sel_s.seats[r_idx][c_idx]
                    icon = "🚧" if val == 2 else "🔴" if val == 1 else "⬜"
                    if cols[c_idx+1].button(icon, key=f"a_{row_name}{c_idx}"):
                        if val != 1: # แก้ได้เฉพาะที่นั่งที่ยังไม่มีคนจอง
                            sel_s.seats[r_idx][c_idx] = 2 if val == 0 else 0
                            st.rerun()
        else:
            st.info("ยังไม่มีรอบฉาย")

# --- 5. การรันโปรแกรม ---

def main():
    st.set_page_config(page_title="Cinema Sync", layout="wide")
    init_session()

    choice = st.sidebar.radio("เลือกโหมด", ["ฝั่งลูกค้า (Booking)", "ฝั่งผู้ให้บริการ (Admin)"])
    if choice == "ฝั่งลูกค้า (Booking)":
        customer_view()
    else:
        admin_view()

if __name__ == "__main__":
    main()
