def calculate_rank(core):
    """Hàm tiện ích để tính điểm trung bình và xếp loại"""
    average = round(sum(core) / len(core), 2)
    if average >= 8.0:
        rank = "Giỏi"
    elif average >= 6.5:
        rank = "Khá"
    else:
        rank = "Trung bình"
    return average, rank


def input_score(prompt, current_score=None):
    """Hàm nhập điểm có bẫy lỗi chữ và xử lý logic cập nhật (để trống)"""
    while True:
        score_str = input(prompt).strip()
        if score_str == "":
            # Nếu là hàm update và để trống, giữ nguyên điểm cũ. Nếu là hàm add, mặc định 0.0
            return current_score if current_score is not None else 0.0
        
        try:
            score = float(score_str)
            if 0.0 <= score <= 10.0:
                return score
            print("Điểm phải nằm trong khoảng từ 0 đến 10. Vui lòng nhập lại.")
        except ValueError:
            print("Điểm phải là một số thực. Vui lòng nhập lại.")


def display_students(students):
    if not students:
        print("Danh sách sinh viên trống.")
        return
    
    # In tiêu đề cột cho đẹp và rõ ràng
    print(f"{'ID':<7}| {'Name':<15}| {'Math':<5}| {'Phys':<5}| {'Chem':<5}| {'Avg':<5}| {'Rank'}")
    print("-" * 60)
    for student in students:
        print(f"{student['id_student']:<7}| {student['name']:<15}| "
              f"{student['core'][0]:<5}| {student['core'][1]:<5}| {student['core'][2]:<5}| "
              f"{student['average']:<5}| {student['rank']}")


def add_student(students):
    id_student = input("Nhập ID sinh viên: ").strip().upper()
    if not id_student:
        print("ID sinh viên không được để trống.")
        return
    
    if any(student['id_student'] == id_student for student in students):
        print("ID sinh viên đã tồn tại. Vui lòng nhập lại.")
        return

    name_student = input("Nhập tên sinh viên: ").strip().title()
    if not name_student:
        print("Tên sinh viên không được để trống.")
        return

    print("Vui lòng nhập điểm môn sinh viên theo thứ tự: Toán, Lý, Hóa")
    math = input_score("Nhập điểm Toán: ")
    physics = input_score("Nhập điểm Lý: ")
    chemistry = input_score("Nhập điểm Hóa: ")
    
    core = (math, physics, chemistry)
    average, rank = calculate_rank(core)

    new_student = {
        'id_student': id_student,
        'name': name_student,
        'core': core,
        'average': average,
        'rank': rank
    }
    students.append(new_student)
    print("Thêm sinh viên thành công!")


def update_student(students):
    id_student = input("Nhập ID sinh viên cần cập nhật: ").strip().upper()
    
    # Tìm sinh viên trực tiếp trong danh sách thay vì list comprehension gây đè biến
    target_student = None
    for student in students:
        if student['id_student'] == id_student:
            target_student = student
            break
            
    if not target_student:
        print("Không tìm thấy sinh viên với ID đã nhập.")
        return

    print(f"Đang cập nhật cho sinh viên: {target_student['name']}")
    # Truyền điểm cũ vào hàm để nếu nhấn Enter sẽ giữ nguyên điểm cũ
    input_math = input_score("Nhập điểm Toán mới (để trống nếu giữ nguyên): ", target_student['core'][0])
    input_physics = input_score("Nhập điểm Lý mới (để trống nếu giữ nguyên): ", target_student['core'][1])
    input_chemistry = input_score("Nhập điểm Hóa mới (để trống nếu giữ nguyên): ", target_student['core'][2])
    
    core = (input_math, input_physics, input_chemistry)
    average, rank = calculate_rank(core)
    
    # Cập nhật trực tiếp vào reference của sinh viên trong list
    target_student['core'] = core
    target_student['average'] = average
    target_student['rank'] = rank
    print("Cập nhật kết quả học tập thành công.")


def delete_student(students):
    id_student = input("Nhập ID sinh viên cần xóa: ").strip().upper()
    
    for i, student in enumerate(students):
        if student['id_student'] == id_student:
            submit = input(f"Bạn có chắc chắn muốn xóa SV {student['name']} không? (Y/N): ").strip().upper()
            if submit == "Y":
                del students[i]
                print("Xóa sinh viên thành công.")
            else:
                print("Hủy thao tác xóa sinh viên.")
            return
            
    print("Không tìm thấy sinh viên với ID đã nhập.")


def search_student(students):
    if not students:
        print("Danh sách sinh viên trống.")
        return
    keyword = input("Nhập từ khóa (ID hoặc Tên) để tìm kiếm: ").strip().lower()
    
    matched = [student for student in students if keyword == student['id_student'].lower() or keyword in student['name'].lower()]
    
    if not matched:
        print("Không tìm thấy sinh viên nào khớp với từ khóa.")
        return
        
    print(f"{'ID':<7}| {'Name':<15}| {'Math':<5}| {'Phys':<5}| {'Chem':<5}| {'Avg':<5}| {'Rank'}")
    for student in matched:
        print("-" * 60)
        print(f"{student['id_student']:<7}| {student['name']:<15}| "
              f"{student['core'][0]:<5}| {student['core'][1]:<5}| {student['core'][2]:<5}| "
              f"{student['average']:<5}| {student['rank']}")
            
    

def average_score(students):
    if not students:
        print("Danh sách trống, không thể thống kê.")
        return
        
    count_rank1 = sum(1 for s in students if s['rank'] == "Giỏi")
    count_rank2 = sum(1 for s in students if s['rank'] == "Khá")
    count_rank3 = sum(1 for s in students if s['rank'] == "Trung bình")
    
    print(f"Số lượng học sinh xếp loại Giỏi: {count_rank1}")
    print(f"Số lượng học sinh xếp loại Khá: {count_rank2}")
    print(f"Số lượng học sinh xếp loại Trung bình: {count_rank3}")


# --- Chương trình chính ---
list_student = [
    {'id_student': "SV001", 'name': 'Nguyen Van A', "core": (8.5, 7.0, 9.0), 'average': 8.17, 'rank': "Giỏi"},
    {'id_student': "SV002", 'name': 'Le Thi B', "core": (6.0, 7.5, 8.0), 'average': 7.17, 'rank': "Khá"},
    {'id_student': "SV003", 'name': 'Tran Van C', "core": (5.0, 6.0, 7.0), 'average': 6.0, 'rank': "Trung bình"},
]

while True:
    choose = input("""
                    1. Hiển thị danh sách sinh viên
                    2. Tiếp nhận sinh viên
                    3. Cập nhật kết quả học tập
                    4. Xóa sinh viên
                    5. Tìm kiếm sinh viên
                    6. Thống kê điểm trung bình
                    7. Thoát
                    Chọn chức năng: """).strip()
    
    print("\n" + "="*40)
    match choose:
        case "1":
            print("Danh sách sinh viên:")
            display_students(list_student)
        case "2":
            print("Tiếp nhận sinh viên:")
            add_student(list_student)
        case "3":
            print("Cập nhật kết quả học tập:")
            update_student(list_student)
        case "4":
            print("Xóa sinh viên:")
            delete_student(list_student)
        case "5":
            print("Tìm kiếm sinh viên:")
            search_student(list_student)
        case "6":
            print("Thống kê điểm trung bình:")
            average_score(list_student)
        case "7":
            print("Thoát chương trình.")
            break
        case _:
            print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1 đến 7.")
    print("="*40)