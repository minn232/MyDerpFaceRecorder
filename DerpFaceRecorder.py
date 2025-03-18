import cv2 as cv
import numpy as np

def mouse_callback(event, x, y, flags, param):
    """ 마우스 클릭 시 상태 변경하는 함수 """
    if event == cv.EVENT_LBUTTONDOWN:
        param[0] = not param[0]  # isClicked 상태 변경
        
def filter(img):
    height, width, channels = img.shape
    
    left_half = img[:, :width//2]
    right_half = cv.flip(left_half, 1)
    
    mirrored_image = np.hstack((left_half, right_half))
    
    return mirrored_image
    

def main():
    # 웹캠 열기 (0번 장치)
    video = cv.VideoCapture(0)

    # 녹화 설정 (코덱, 프레임 속도, 해상도 설정)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('recorded_video.avi', fourcc, 20.0, (640, 480))

    if not video.isOpened():
        print("웹캠을 열 수 없습니다.")
        return

    fps = video.get(cv.CAP_PROP_FPS)
    wait_msec = int(1 / fps * 1000)
    
    recording = False  # 초기 상태: 녹화 X
    isClicked = [False]  # 초기 상태: 원본본
    
    cv.namedWindow('Video Recorder')
    cv.setMouseCallback('Video Recorder', mouse_callback, isClicked)

    while True:
        valid, img = video.read()
        if not valid:
            break
        
        if isClicked[0]:
            img = filter(img)  # 좌우대칭
        
        # 녹화 중이면 프레임 저장 및 화면에 빨간색 원 표시
        if recording:
            out.write(img)
            cv.circle(img, (320, 20), 5, (0, 0, 255), -1)  # 빨간색 원 표시
            
        # 화면에 표시  
        cv.imshow('Video Recorder', img)    

        # 키 입력 확인
        key = cv.waitKey(wait_msec)
        if key == 27:  # ESC 키 종료
            break
        elif key == ord(' '):  # Space 키로 녹화 일시 정지/재개
            recording = not recording

    # 자원 해제
    video.release()
    out.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
