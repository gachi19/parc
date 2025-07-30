# 사용법
# 터미널에서 python project_qr.py -i
# 또는 python project_qr.py encode 'Hello, World!' output --box-size 10 --border 4
# 또는 python project_qr.py decode input.png
# 를 실행하여 QR 코드 생성 및 디코딩 도구를 사용가능
# pip install qrcode[pil] pillow opencv-python pyzbar
# 터미널에서 필수 실행


import cv2
import qrcode
from pyzbar.pyzbar import decode
import argparse

def decode_qr(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        decoded_objs = decode(gray)

        if not decoded_objs:
            print("[디코딩 실패] QR 코드를 찾을 수 없습니다.")
            return []

        results = []
        for obj in decoded_objs:
            try:
                data = obj.data.decode('utf-8')
                results.append(data)
                print(f"[디코딩 성공] 데이터: {data}")
            except UnicodeDecodeError:
                print("[디코딩 실패] UTF-8로 디코딩할 수 없는 데이터입니다.")

        return results
    except Exception as e:
        print(f"[에러] 이미지 처리 중 오류가 발생했습니다: {e}")
        return []

def generate_qr(data, output_path, box_size=10, border=4):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        print(f"[생성 성공] QR 코드가 저장되었습니다: {output_path}")
    except Exception as e:
        print(f"[에러] QR 코드 생성 실패: {e}")

def interactive_mode():
    while True:
        print("\n=== QR 코드 도구 ===")
        print("1. QR 코드 생성")
        print("2. QR 코드 디코딩")
        print("3. 종료")

        choice = input("선택하세요 (1-3): ").strip()

        if choice == '1':
            data = input("인코딩할 데이터를 입력하세요: ")
            output = input("출력 파일 이름을 입력하세요: ").strip() + ".jpg"
            box_size = input("박스 크기 (기본값 10): ").strip()
            border = input("테두리 크기 (기본값 4): ").strip()

            box_size = int(box_size) if box_size else 10
            border = int(border) if border else 4

            generate_qr(data, output, box_size, border)
        elif choice == '2':
            input_path = input("디코딩할 이미지 파일 이름을 입력하세요. 한글 불가: ").strip() + ".jpg"
            results = decode_qr(input_path)
            if not results:
                print("[알림] 디코딩된 QR 코드가 없습니다.")
        elif choice == '3':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1-3 중에서 선택하세요.")

def main():
    parser = argparse.ArgumentParser(description='QR 코드 생성 및 디코딩 도구')
    parser.add_argument('--interactive', '-i', action='store_true', help='대화식 모드 실행')
    subparsers = parser.add_subparsers(dest='command', help='사용 가능한 명령어')

    # encode 명령어
    encode_parser = subparsers.add_parser('encode', help='QR 코드 생성')
    encode_parser.add_argument('data', help='QR 코드에 인코딩할 데이터')
    encode_parser.add_argument('output', help='출력 파일 경로')
    encode_parser.add_argument('--box-size', type=int, default=10, help='박스 크기 (기본값: 10)')
    encode_parser.add_argument('--border', type=int, default=4, help='테두리 크기 (기본값: 4)')

    # decode 명령어
    decode_parser = subparsers.add_parser('decode', help='QR 코드 디코딩')
    decode_parser.add_argument('input', help='입력 이미지 파일 경로')

    args = parser.parse_args()

    # 대화식 모드가 지정된 경우
    if args.interactive:
        interactive_mode()
        return

    # 명령어 처리
    if args.command == 'encode':
        try:
            generate_qr(args.data, args.output, args.box_size, args.border)
        except Exception as e:
            print(f"[에러] QR 코드 생성 실패: {e}")
    elif args.command == 'decode':
        results = decode_qr(args.input)
        if not results:
            print("[알림] 디코딩된 QR 코드가 없습니다.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
