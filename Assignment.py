class MovieNode:
    """Node สำหรับเก็บข้อมูลหนังใน Linked List"""
    def __init__(self, movie_name):
        self.movie_name = movie_name
        self.next = None

class CinemaManager:
    def __init__(self, rows=5, cols=8):
        # 1. Linked List Setup (จัดการรายชื่อหนัง)
        self.head = None
        
        # 2. 2D Array Setup (จัดการที่นั่ง: 0=ว่าง, 1=จอง/แดง, 2=พัง/เหลือง)
        self.rows = rows
        self.cols = cols
        self.seats = [[0 for _ in range(cols)] for _ in range(rows)]

    # --- ส่วนของ Linked List (หนัง) ---

    def add_movie(self, name):
        """เพิ่มหนังใหม่ (Linked List Insertion)"""
        new_node = MovieNode(name)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        print(f"✅ เพิ่มหนังเรื่อง: '{name}' เรียบร้อย")

    def search_movie(self, name):
        """ค้นหาหนัง (Linear Search ใน Linked List)"""
        current = self.head
        pos = 1
        while current:
            if current.movie_name.lower() == name.lower():
                print(f"🔍 พบหนังเรื่อง '{current.movie_name}' (ลำดับที่ {pos})")
                return True
            current = current.next
            pos += 1
        print(f"❌ ไม่พบหนังเรื่อง '{name}' ในระบบ")
        return False

    def remove_movie(self, name):
        """ลบหนัง (Linked List Deletion)"""
        current = self.head
        prev = None
        while current and current.movie_name.lower() != name.lower():
            prev = current
            current = current.next
        
        if not current:
            print(f"⚠️ ไม่สามารถลบได้: ไม่พบหนังเรื่อง '{name}'")
            return

        if not prev:
            self.head = current.next
        else:
            prev.next = current.next
        print(f"🗑️ ลบหนังเรื่อง '{name}' ออกจากระบบแล้ว")

    # --- ส่วนของ 2D Array (ที่นั่ง) ---

    def update_seat(self, row, col, status):
        """แก้ไขสถานะที่นั่ง (Direct Access 2D Array)"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.seats[row][col] = status
            desc = "จอง (แดง)" if status == 1 else "พัง (เหลือง)" if status == 2 else "ว่าง"
            print(f"💺 อัปเดตที่นั่ง [{row}][{col}] เป็น: {desc}")
        else:
            print("❗ พิกัดที่นั่งไม่ถูกต้อง")

    def find_broken_seats(self):
        """ค้นหาที่นั่งที่พัง (Linear Search ใน 2D Array)"""
        broken_list = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.seats[r][c] == 2:
                    broken_list.append(f"({r},{c})")
        
        print("\n--- สรุปรายงานส่งเจ้าหน้าที่ ---")
        if broken_list:
            print(f"⚠️ พบที่นั่งชำรุด {len(broken_list)} จุด: {', '.join(broken_list)}")
        else:
            print("✅ ไม่พบที่นั่งชำรุด")
        return broken_list

    def display_visual_seats(self):
        """แสดงผล Visual ผังที่นั่ง"""
        print("\n--- Visual ผังที่นั่ง ( [ ]=ว่าง, [R]=จอง, [Y]=พัง ) ---")
        # พิมพ์เลขคอลัมน์
        print("    " + "  ".join([str(i) for i in range(self.cols)]))
        
        for r in range(self.rows):
            row_display = f"{r:2} "
            for c in range(self.cols):
                val = self.seats[r][c]
                if val == 1:
                    row_display += "[R]" # Red (Reserved)
                elif val == 2:
                    row_display += "[Y]" # Yellow (Broken)
                else:
                    row_display += "[ ]" # Empty
            print(row_display)
        print("--------------------------------------------------")

# --- ทดสอบการใช้งานระบบ ---

cinema = CinemaManager(rows=5, cols=10)

# 1. ทดสอบ Linked List
cinema.add_movie("Avatar 3")
cinema.add_movie("Spider-Man")
cinema.add_movie("Batman")
cinema.search_movie("Spider-Man")
cinema.remove_movie("Batman")

# 2. ทดสอบ 2D Array & Search
cinema.update_seat(0, 5, 1) # จองที่นั่ง 0,5
cinema.update_seat(2, 3, 2) # ที่นั่ง 2,3 พัง
cinema.update_seat(4, 9, 2) # ที่นั่ง 4,9 พัง

# 3. แสดงผลและสรุป
cinema.display_visual_seats()
cinema.find_broken_seats()
