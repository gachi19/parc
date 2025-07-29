# GUI QR 코드 생성 및 디코딩 도구
# pip install qrcode[pil] pillow opencv-python
# 터미널에서 필수 실행

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import qrcode
from PIL import Image, ImageTk
import os
import numpy as np

class QRCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QR 코드 생성 및 디코딩 도구")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        # 변수들
        self.qr_data_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.input_path_var = tk.StringVar()
        self.box_size_var = tk.IntVar(value=10)
        self.border_var = tk.IntVar(value=4)

        self.create_widgets()

    def create_widgets(self):
        # 메인 노트북 (탭)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # QR 코드 생성 탭
        self.create_generate_tab(notebook)

        # QR 코드 디코딩 탭
        self.create_decode_tab(notebook)

    def create_generate_tab(self, notebook):
        # 생성 탭 프레임
        generate_frame = ttk.Frame(notebook)
        notebook.add(generate_frame, text="QR 코드 생성")

        # 데이터 입력 프레임
        data_frame = ttk.LabelFrame(generate_frame, text="QR 코드 데이터")
        data_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(data_frame, text="인코딩할 데이터:").pack(anchor='w', padx=5, pady=2)
        data_entry = tk.Text(data_frame, height=4, wrap=tk.WORD)
        data_entry.pack(fill='x', padx=5, pady=2)
        self.data_entry = data_entry

        # 설정 프레임
        settings_frame = ttk.LabelFrame(generate_frame, text="설정")
        settings_frame.pack(fill='x', padx=10, pady=5)

        # 박스 크기
        box_frame = ttk.Frame(settings_frame)
        box_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(box_frame, text="박스 크기:").pack(side='left')
        ttk.Spinbox(box_frame, from_=5, to=20, textvariable=self.box_size_var, width=10).pack(side='right')

        # 테두리 크기
        border_frame = ttk.Frame(settings_frame)
        border_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(border_frame, text="테두리 크기:").pack(side='left')
        ttk.Spinbox(border_frame, from_=1, to=10, textvariable=self.border_var, width=10).pack(side='right')

        # 출력 파일 선택
        output_frame = ttk.LabelFrame(generate_frame, text="출력 파일")
        output_frame.pack(fill='x', padx=10, pady=5)

        file_frame = ttk.Frame(output_frame)
        file_frame.pack(fill='x', padx=5, pady=2)
        ttk.Entry(file_frame, textvariable=self.output_path_var, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(file_frame, text="찾아보기", command=self.browse_output_file).pack(side='right', padx=(5, 0))

        # 생성 버튼
        ttk.Button(generate_frame, text="QR 코드 생성", command=self.generate_qr).pack(pady=10)

        # 미리보기 프레임
        preview_frame = ttk.LabelFrame(generate_frame, text="미리보기")
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.preview_label = ttk.Label(preview_frame, text="QR 코드가 여기에 표시됩니다.")
        self.preview_label.pack(expand=True)

    def create_decode_tab(self, notebook):
        # 디코딩 탭 프레임
        decode_frame = ttk.Frame(notebook)
        notebook.add(decode_frame, text="QR 코드 디코딩")

        # 입력 파일 선택
        input_frame = ttk.LabelFrame(decode_frame, text="입력 파일")
        input_frame.pack(fill='x', padx=10, pady=5)

        file_frame = ttk.Frame(input_frame)
        file_frame.pack(fill='x', padx=5, pady=2)
        ttk.Entry(file_frame, textvariable=self.input_path_var, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(file_frame, text="찾아보기", command=self.browse_input_file).pack(side='right', padx=(5, 0))

        # 디코딩 버튼
        ttk.Button(decode_frame, text="QR 코드 디코딩", command=self.decode_qr).pack(pady=10)

        # 결과 표시
        result_frame = ttk.LabelFrame(decode_frame, text="디코딩 결과")
        result_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # 스크롤바가 있는 텍스트 위젯
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.result_text = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def browse_output_file(self):
        """출력 파일 경로 선택"""
        file_path = filedialog.asksaveasfilename(
            title="QR 코드 저장 위치 선택",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            self.output_path_var.set(file_path)

    def browse_input_file(self):
        """입력 파일 경로 선택"""
        file_path = filedialog.askopenfilename(
            title="디코딩할 이미지 파일 선택",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        if file_path:
            self.input_path_var.set(file_path)

    def generate_qr(self):
        """QR 코드 생성"""
        data = self.data_entry.get('1.0', tk.END).strip()
        output_path = self.output_path_var.get().strip()

        if not data:
            messagebox.showerror("오류", "인코딩할 데이터를 입력하세요.")
            return

        if not output_path:
            messagebox.showerror("오류", "출력 파일 경로를 선택하세요.")
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=self.box_size_var.get(),
                border=self.border_var.get(),
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(output_path)

            # 미리보기 업데이트
            self.update_preview(img)

            messagebox.showinfo("성공", f"QR 코드가 성공적으로 생성되었습니다.\n저장 위치: {output_path}")

        except Exception as e:
            messagebox.showerror("오류", f"QR 코드 생성 중 오류가 발생했습니다:\n{str(e)}")

    def update_preview(self, pil_image):
        """미리보기 업데이트"""
        try:
            # 이미지 크기 조정 (최대 200x200)
            img_copy = pil_image.copy()
            img_copy.thumbnail((200, 200), Image.Resampling.LANCZOS)

            # tkinter에서 사용할 수 있는 형태로 변환
            photo = ImageTk.PhotoImage(img_copy)
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo  # 참조 유지

        except Exception as e:
            self.preview_label.configure(text=f"미리보기 오류: {str(e)}")

    def decode_qr(self):
        input_path = self.input_path_var.get().strip()

        if not input_path:
            messagebox.showerror("오류", "디코딩할 이미지 파일을 선택하세요.")
            return

        if not os.path.exists(input_path):
            messagebox.showerror("오류", "선택한 파일이 존재하지 않습니다.")
            return

        try:
            with open(input_path, 'rb') as f:
                file_bytes = np.frombuffer(f.read(), np.uint8)

            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if img is None:
                raise FileNotFoundError(f"이미지 파일을 읽을 수 없습니다: {input_path}")

            qr_detector = cv2.QRCodeDetector()
            data, bbox, _ = qr_detector.detectAndDecode(img)

            self.result_text.delete('1.0', tk.END)

            if data:
                self.result_text.insert(tk.END, "[QR 코드 디코딩 성공]\n")
                self.result_text.insert(tk.END, f"데이터: {data}\n")
                self.result_text.insert(tk.END, f"파일 경로: {input_path}\n")
                self.result_text.insert(tk.END, "-" * 50 + "\n")
                messagebox.showinfo("성공", "QR 코드를 성공적으로 디코딩했습니다.")
            else:
                self.result_text.insert(tk.END, "[디코딩 실패] QR 코드를 찾을 수 없습니다.\n")
                self.result_text.insert(tk.END, f"파일 경로: {input_path}\n")
                self.result_text.insert(tk.END, "- QR 코드가 이미지에 없거나 인식하기 어려울 수 있습니다.\n")
                self.result_text.insert(tk.END, "- 이미지가 흐리거나 해상도가 낮을 수 있습니다.\n")
                messagebox.showwarning("알림", "QR 코드를 찾을 수 없습니다.")

        except Exception as e:
            error_msg = f"이미지 처리 중 오류가 발생했습니다:\n{str(e)}\n파일 경로: {input_path}"
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, error_msg)
            messagebox.showerror("오류", error_msg)

def main():
    root = tk.Tk()
    app = QRCodeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
