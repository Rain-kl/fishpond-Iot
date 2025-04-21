import cv2
import mediapipe as mp
import time
import math
import numpy as np


class GestureRecognizer:
    def __init__(self):
        # --- Configuration ---
        # 可调整的严格度
        self.STRICTNESS_LEVEL = 2  # 1=宽松, 2=中等, 3=严格, 4=非常严格
        self.strictness_presets = {
            1: {
                "stability_frames": 3,
                "min_stability_score": 0.7,
                "palm_facing_threshold": 0.1,
                "extension_ratio": 0.65,
                "confidence_threshold": 0.5,
            },
            2: {
                "stability_frames": 5,
                "min_stability_score": 0.75,
                "palm_facing_threshold": 0.2,
                "extension_ratio": 0.75,
                "confidence_threshold": 0.6,
            },
            3: {
                "stability_frames": 7,
                "min_stability_score": 0.8,
                "palm_facing_threshold": 0.3,
                "extension_ratio": 0.85,
                "confidence_threshold": 0.7,
            },
            4: {
                "stability_frames": 10,
                "min_stability_score": 0.85,
                "palm_facing_threshold": 0.4,
                "extension_ratio": 0.95,
                "confidence_threshold": 0.8,
            },
        }

        # --- Initialization ---
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.hands_static = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.mp_drawing = mp.solutions.drawing_utils

        # 不在初始化时打开摄像头，而是在需要时才打开
        self.cap = None

        self.tip_ids = [4, 8, 12, 16, 20]  # 指尖关键点
        self.pTime = 0

        # 用于稳定性检测的历史记录
        self.last_positions = []
        self.stable_count = 0
        self.last_gesture = None

    def get_current_config(self):
        """获取当前严格度的配置"""
        return self.strictness_presets[self.STRICTNESS_LEVEL]

    def calculate_palm_normal(self, landmarks):
        """计算手掌法向量，判断手掌是否面向摄像头"""
        # 使用手腕、中指MCP和小指MCP形成平面
        wrist = np.array([landmarks[0].x, landmarks[0].y, landmarks[0].z])
        middle_mcp = np.array([landmarks[9].x, landmarks[9].y, landmarks[9].z])
        pinky_mcp = np.array([landmarks[17].x, landmarks[17].y, landmarks[17].z])

        # 计算两个向量
        v1 = middle_mcp - wrist
        v2 = pinky_mcp - wrist

        # 计算法向量（叉积）
        normal = np.cross(v1, v2)

        # 归一化
        normal = normal / np.linalg.norm(normal)

        # Z分量为负表示手掌朝向摄像头
        config = self.get_current_config()
        palm_facing_camera = -normal[2] > config["palm_facing_threshold"]

        return palm_facing_camera

    def check_hand_stability(self, landmarks, prev_positions):
        """检查手部是否保持稳定"""
        config = self.get_current_config()

        if not prev_positions:
            return False, []

        # 提取关键点坐标
        current_pos = []
        for lm in landmarks:
            current_pos.append((lm.x, lm.y))

        if len(prev_positions) < config["stability_frames"]:
            prev_positions.append(current_pos)
            return False, prev_positions

        # 计算当前位置与历史位置的差异
        stability_score = 1.0
        for prev_pos in prev_positions:
            total_diff = 0
            for i, (cur_x, cur_y) in enumerate(current_pos):
                prev_x, prev_y = prev_pos[i]
                diff = math.sqrt((cur_x - prev_x) ** 2 + (cur_y - prev_y) ** 2)
                total_diff += diff

            avg_diff = total_diff / len(current_pos)
            stability_score *= 1 - min(avg_diff * 10, 0.5)  # 差异越小，稳定性越高

        # 更新历史记录（保持固定长度）
        prev_positions.pop(0)
        prev_positions.append(current_pos)

        return stability_score > config["min_stability_score"], prev_positions

    def is_finger_fully_extended(self, lm_list, finger_id):
        """判断手指是否完全伸展"""
        config = self.get_current_config()

        # 获取指尖和各关节坐标
        tip = lm_list[self.tip_ids[finger_id]]
        pip = lm_list[self.tip_ids[finger_id] - 2]
        mcp = lm_list[self.tip_ids[finger_id] - 3]

        # 计算指尖到PIP的距离
        tip_to_pip = math.sqrt((tip[1] - pip[1]) ** 2 + (tip[2] - pip[2]) ** 2)

        # 计算PIP到MCP的距离
        pip_to_mcp = math.sqrt((pip[1] - mcp[1]) ** 2 + (pip[2] - mcp[2]) ** 2)

        # 手指伸展时，指尖到PIP的距离应接近或大于PIP到MCP的距离
        extension_ratio = tip_to_pip / pip_to_mcp if pip_to_mcp > 0 else 0

        # 手指应该相对垂直于手掌
        vertical_check = tip[2] < pip[2]

        # 根据严格度调整判断条件
        if self.STRICTNESS_LEVEL >= 3:
            return extension_ratio > config["extension_ratio"] and vertical_check
        else:
            return extension_ratio > config["extension_ratio"] or vertical_check

    def detect_fingers(self, lm_list, handedness):
        """检测伸出的手指数量"""
        fingers = []

        # 拇指检测逻辑
        thumb_is_open = False
        if handedness:
            # 根据手的左右判断拇指方向
            thumb_tip = lm_list[4][1]
            thumb_ip = lm_list[3][1]
            thumb_mcp = lm_list[2][1]

            # 宽松模式下的拇指检测
            if self.STRICTNESS_LEVEL == 1:
                if (handedness == "Right" and thumb_tip < thumb_mcp) or (
                    handedness == "Left" and thumb_tip > thumb_mcp
                ):
                    thumb_is_open = True
            else:
                # 严格模式下的拇指检测
                if (handedness == "Right" and thumb_tip < thumb_ip < thumb_mcp) or (
                    handedness == "Left" and thumb_tip > thumb_ip > thumb_mcp
                ):
                    # 额外检查：拇指应该与其他手指有一定角度
                    index_mcp = lm_list[5][1:3]
                    thumb_cmc = lm_list[1][1:3]
                    thumb_tip_pos = lm_list[4][1:3]

                    # 计算向量和角度
                    v1 = [
                        thumb_tip_pos[0] - thumb_cmc[0],
                        thumb_tip_pos[1] - thumb_cmc[1],
                    ]
                    v2 = [index_mcp[0] - thumb_cmc[0], index_mcp[1] - thumb_cmc[1]]

                    # 检查向量长度避免除零错误
                    len_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
                    len_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

                    if len_v1 > 0 and len_v2 > 0:
                        cosine = (v1[0] * v2[0] + v1[1] * v2[1]) / (len_v1 * len_v2)
                        angle = math.acos(min(max(cosine, -1.0), 1.0)) * 180 / math.pi

                        # 角度要求随严格度增加
                        min_angle = (
                            20 + (self.STRICTNESS_LEVEL - 2) * 5
                        )  # 20°, 25°, 30°
                        if angle > min_angle:
                            thumb_is_open = True

        fingers.append(1 if thumb_is_open else 0)

        # 四指检测（根据严格度调整）
        for finger_id in range(1, 5):  # 食指、中指、无名指、小指
            if self.STRICTNESS_LEVEL <= 2:
                # 宽松/中等模式：简单检查指尖位置
                if (
                    lm_list[self.tip_ids[finger_id]][2]
                    < lm_list[self.tip_ids[finger_id] - 2][2]
                ):
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                # 严格模式：检查手指是否完全伸展
                if self.is_finger_fully_extended(lm_list, finger_id):
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers

    def process_frame(self, img, enable_stabilizer=True):
        """处理单帧图像并识别手势"""
        img = cv2.flip(img, 1)
        h, w, c = img.shape

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if enable_stabilizer:
            results = self.hands.process(img_rgb)
        else:
            results = self.hands_static.process(img_rgb)

        display_text = "null"  # 默认显示
        hand_found = False
        lm_list = []
        hand_confidence = 0.0
        handedness = None
        palm_facing = False
        is_stable = not enable_stabilizer  # 当不启用稳定器时，直接视为稳定

        # 获取当前配置
        config = self.get_current_config()

        if results.multi_hand_landmarks:
            my_hand = results.multi_hand_landmarks[0]

            if results.multi_handedness:
                handedness_info = results.multi_handedness[0].classification[0]
                handedness = handedness_info.label
                hand_confidence = handedness_info.score

            # 1. 检查手掌是否面向摄像头（在宽松模式下可以跳过）
            palm_facing = True
            if self.STRICTNESS_LEVEL >= 2:
                palm_facing = self.calculate_palm_normal(my_hand.landmark)

            # 2. 检查手部稳定性（仅当启用稳定器且严格度大于等于2时）
            is_stable = True
            if enable_stabilizer:
                if self.STRICTNESS_LEVEL >= 2:
                    is_stable, self.last_positions = self.check_hand_stability(
                        my_hand.landmark, self.last_positions
                    )
            else:
                # 不启用稳定器时清空历史记录但保持稳定状态为True
                self.last_positions = []
                self.stable_count = 0

            if hand_confidence >= config["confidence_threshold"] and (
                palm_facing or self.STRICTNESS_LEVEL == 1
            ):
                hand_found = True
                self.mp_drawing.draw_landmarks(
                    img, my_hand, self.mp_hands.HAND_CONNECTIONS
                )

                # 提取关键点坐标
                for id, lm in enumerate(my_hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])

                # 手指检测逻辑
                if len(lm_list) == 21:  # 确保检测到所有21个关键点
                    fingers = self.detect_fingers(lm_list, handedness)

                    # 计算伸出的手指总数
                    total_fingers = fingers.count(1)

                    # 根据严格度和稳定器状态确定是否需要稳定性检查
                    if not enable_stabilizer or self.STRICTNESS_LEVEL <= 2 or is_stable:
                        if enable_stabilizer and self.stable_count < min(
                            2, self.STRICTNESS_LEVEL
                        ):  # 仅在启用稳定器时检查
                            self.stable_count += 1
                            display_text = (
                                self.last_gesture if self.last_gesture else "null"
                            )
                        else:
                            display_text = str(total_fingers)
                            self.last_gesture = display_text
                    else:
                        display_text = (
                            self.last_gesture if self.last_gesture else "null"
                        )
                else:
                    display_text = "null"
            else:
                display_text = "null"
        else:
            if enable_stabilizer:
                self.last_positions = []  # 仅在启用稳定器时重置历史记录
                self.stable_count = 0
            self.last_gesture = None

        # 绘制手势显示
        self.draw_results(
            img, display_text, results, hand_confidence, palm_facing, is_stable, w, h
        )

        # FPS计算
        cTime = time.time()
        fps = 1 / (cTime - self.pTime) if (cTime - self.pTime) > 0 else 0
        self.pTime = cTime
        cv2.putText(
            img,
            f"FPS: {int(fps)}",
            (w - 150, 50),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (255, 0, 0),
            2,
        )

        return img, display_text

    def draw_results(
        self, img, display_text, results, hand_confidence, palm_facing, is_stable, w, h
    ):
        """绘制识别结果和状态信息"""
        # 绘制手势数字
        cv2.rectangle(img, (20, 20), (200, 120), (0, 255, 0), cv2.FILLED)
        cv2.putText(
            img, display_text, (45, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5
        )

        # 显示严格度和状态信息
        status_text = [f"严格度: {self.STRICTNESS_LEVEL}/4"]
        if results and results.multi_hand_landmarks:
            status_text.append(f"置信度: {hand_confidence:.2f}")
            status_text.append(f'手掌朝向: {"是" if palm_facing else "否"}')
            status_text.append(f'稳定性: {"是" if is_stable else "否"}')

            y_pos = 160
            for text in status_text:
                cv2.putText(
                    img, text, (20, y_pos), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2
                )
                y_pos += 30
        else:
            cv2.putText(
                img,
                status_text[0],
                (20, 160),
                cv2.FONT_HERSHEY_PLAIN,
                1.5,
                (0, 0, 255),
                2,
            )

        # 操作指南
        cv2.putText(
            img,
            "按 '+' 增加严格度, '-' 降低严格度",
            (w - 350, h - 20),
            cv2.FONT_HERSHEY_PLAIN,
            1.2,
            (255, 255, 255),
            1,
        )

    def adjust_strictness(self, key):
        """调整识别严格度"""
        if key == ord("+") or key == ord("="):  # 增加严格度
            self.STRICTNESS_LEVEL = min(self.STRICTNESS_LEVEL + 1, 4)
            print(f"严格度提高到: {self.STRICTNESS_LEVEL}/4")
        elif key == ord("-") or key == ord("_"):  # 降低严格度
            self.STRICTNESS_LEVEL = max(self.STRICTNESS_LEVEL - 1, 1)
            print(f"严格度降低到: {self.STRICTNESS_LEVEL}/4")

    def run_on_image(self, image_path, no_display=False):
        """处理单个图像文件"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                print(f"无法读取图像: {image_path}")
                return "错误：无法读取图像"

            # 处理图像并识别手势
            result = self.process_frame(img, enable_stabilizer=False)

            # process_frame可能返回2个或5个值，需要检查
            if isinstance(result, tuple) and len(result) == 5:
                img, gesture, confidence, palm_facing, is_stable = result
            else:
                # 旧版本只返回img和gesture
                img, gesture = result

            # 如果不显示，则直接返回识别结果
            if no_display:
                return gesture

            # 显示结果
            cv2.imshow("Image", img)
            cv2.waitKey(0)
            return gesture

        except Exception as e:
            print(f"处理图像时出错: {str(e)}")
            return "错误：处理图像失败"

    def run(self):
        """运行实时摄像头手势识别"""
        try:
            # 只在需要实时识别时才打开摄像头
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("错误：无法打开摄像头")
                return False

            while True:
                success, img = self.cap.read()
                if not success:
                    print("无法获取摄像头帧")
                    break

                img, gesture, confidence, palm_facing, is_stable = self.process_frame(
                    img
                )

                cTime = time.time()
                fps = 1 / (cTime - self.pTime)
                self.pTime = cTime

                cv2.putText(
                    img,
                    f"FPS: {int(fps)}",
                    (10, 70),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (255, 0, 255),
                    3,
                )

                cv2.imshow("Image", img)
                key = cv2.waitKey(1)

                # ESC键退出
                if key == 27:
                    break
                # 数字键调整严格度
                elif 49 <= key <= 52:  # 1-4
                    self.adjust_strictness(key)

            self.cleanup()
            return True

        except Exception as e:
            print(f"运行时出错: {str(e)}")
            self.cleanup()
            return False

    def cleanup(self):
        """清理资源"""
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    recognizer = GestureRecognizer()
    recognizer.run()
    # recognizer.run_on_image("1.jpg")  # 替换为你的图像文件路径
