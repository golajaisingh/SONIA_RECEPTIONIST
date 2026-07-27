import os
import sys
import time
import json
import threading
import tkinter as tk
from tkinter import messagebox

APP_NAME = "SONIA AI Receptionist"
CENTRE_NAME = "SHIVEN CSC Centre"
WELCOME = "नमस्ते! शिवैन CSC सेंटर में आपका हार्दिक स्वागत है। मैं सोनिया हूँ। बताइए, मैं आपकी क्या सहायता कर सकती हूँ?"

FAQ = {
    "आधार": "आधार सेवा के लिए कृपया अपना आधार कार्ड और आवश्यक दस्तावेज साथ रखें।",
    "बाल आधार": "बाल आधार के लिए बच्चे का जन्म प्रमाणपत्र और माता या पिता का आधार कार्ड आवश्यक है।",
    "पैन": "पैन कार्ड आवेदन के लिए आधार कार्ड, फोटो और मोबाइल नंबर की आवश्यकता होगी।",
    "आय प्रमाण": "आय प्रमाणपत्र के लिए आधार, पते का प्रमाण और आय से जुड़े दस्तावेज आवश्यक हैं।",
    "जाति": "जाति प्रमाणपत्र के लिए आधार, पते का प्रमाण और परिवार का संबंधित प्रमाणपत्र साथ लाएँ।",
    "पीसीसी": "पुलिस क्लीयरेंस सर्टिफिकेट के लिए पहचान, पते का प्रमाण और आवेदन का उद्देश्य आवश्यक होगा।",
    "प्रिंट": "यहाँ प्रिंट, स्कैन, फोटोकॉपी और ऑनलाइन फॉर्म की सुविधा उपलब्ध है।",
}

VOICE_ROMAN = {
    WELCOME: "Namaste! Sheeven C S C Centre mein aapka hardik swagat hai. Main Sonia hoon. Batayiye, main aapki kya sahayata kar sakti hoon?",
    FAQ["आधार"]: "Aadhaar seva ke liye kripya apna Aadhaar card aur zaroori documents saath rakhein.",
    FAQ["बाल आधार"]: "Baal Aadhaar ke liye bachche ka birth certificate aur mata ya pita ka Aadhaar card zaroori hai.",
    FAQ["पैन"]: "PAN card application ke liye Aadhaar card, photo aur mobile number zaroori hai.",
    FAQ["आय प्रमाण"]: "Income certificate ke liye Aadhaar, address proof aur income documents zaroori hain.",
    FAQ["जाति"]: "Caste certificate ke liye Aadhaar, address proof aur family certificate saath laayein.",
    FAQ["पीसीसी"]: "Police clearance certificate ke liye identity, address proof aur application ka purpose zaroori hai.",
    FAQ["प्रिंट"]: "Yahaan print, scan, photocopy aur online form ki suvidha available hai.",
}

AUDIO_FILES = {
    WELCOME: "welcome.mp3",
    FAQ["आधार"]: "aadhaar.mp3",
    FAQ["बाल आधार"]: "baal_aadhaar.mp3",
    FAQ["पैन"]: "pan.mp3",
    FAQ["आय प्रमाण"]: "income.mp3",
    FAQ["जाति"]: "caste.mp3",
    FAQ["पीसीसी"]: "pcc.mp3",
    FAQ["प्रिंट"]: "print.mp3",
}


def resource_path(relative):
    base = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base, relative)

def load_services():
    external = os.path.join(os.path.dirname(sys.executable if getattr(sys, "frozen", False) else __file__), "services.json")
    path = external if os.path.exists(external) else resource_path("services.json")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return []

SERVICE_CATALOG = load_services()


class Voice:
    def __init__(self):
        self.lock = threading.Lock()

    def speak(self, text):
        def run():
            with self.lock:
                try:
                    audio_name = AUDIO_FILES.get(text)
                    audio_path = resource_path(os.path.join("assets", audio_name)) if audio_name else ""
                    if audio_path and os.path.exists(audio_path):
                        import ctypes
                        winmm = ctypes.windll.winmm
                        winmm.mciSendStringW("close sonia_voice", None, 0, None)
                        winmm.mciSendStringW(f'open "{audio_path}" type mpegvideo alias sonia_voice', None, 0, None)
                        winmm.mciSendStringW("play sonia_voice wait", None, 0, None)
                        winmm.mciSendStringW("close sonia_voice", None, 0, None)
                        return
                    try:
                        import pythoncom
                        pythoncom.CoInitialize()
                    except Exception:
                        pythoncom = None
                    import pyttsx3
                    engine = pyttsx3.init()
                    voices = engine.getProperty("voices")
                    preferred = None
                    female = None
                    for voice in voices:
                        descriptor = f"{voice.name} {voice.id} {getattr(voice, 'languages', '')}".lower()
                        if any(word in descriptor for word in ("female", "heera", "kalpana", "zira")):
                            female = female or voice.id
                        if ("hindi" in descriptor or "hi-in" in descriptor) and any(word in descriptor for word in ("female", "heera", "kalpana")):
                            preferred = voice.id
                            break
                        if "hindi" in descriptor or "hi-in" in descriptor:
                            preferred = preferred or voice.id
                    engine.setProperty("voice", preferred or female or voices[0].id)
                    engine.setProperty("rate", 140)
                    engine.setProperty("volume", 1.0)
                    engine.say(VOICE_ROMAN.get(text, text))
                    engine.runAndWait()
                    engine.stop()
                    if pythoncom:
                        pythoncom.CoUninitialize()
                except Exception:
                    pass
        threading.Thread(target=run, daemon=True).start()


class SoniaApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} — {CENTRE_NAME}")
        self.root.geometry("1050x680")
        self.root.minsize(900, 580)
        self.root.configure(bg="#071a2c")
        self.voice = Voice()
        self.camera_running = False
        self.last_greeting = 0
        self.cap = None
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(1200, self.start_camera_automatically)

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#0b2f4f", height=92)
        header.pack(fill="x")
        tk.Label(header, text="SONIA", font=("Segoe UI", 28, "bold"), fg="#42d6ff", bg="#0b2f4f").pack(side="left", padx=28, pady=17)
        tk.Label(header, text="AI Receptionist  •  SHIVEN CSC Centre", font=("Segoe UI", 17), fg="white", bg="#0b2f4f").pack(side="left")
        self.status = tk.Label(header, text="● तैयार", font=("Segoe UI", 12, "bold"), fg="#55ef9c", bg="#0b2f4f")
        self.status.pack(side="right", padx=28)

        body = tk.Frame(self.root, bg="#071a2c")
        body.pack(fill="both", expand=True, padx=24, pady=22)

        left = tk.Frame(body, bg="#102a43", bd=0)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(left, text="कैमरा", font=("Segoe UI", 18, "bold"), fg="white", bg="#102a43").pack(pady=(18, 8))
        self.camera_label = tk.Label(left, text="कैमरा बंद है\n\nनीचे ‘कैमरा चालू करें’ दबाएँ", font=("Segoe UI", 15), fg="#a9c7dd", bg="#06131f")
        self.camera_label.pack(fill="both", expand=True, padx=18, pady=8)
        controls = tk.Frame(left, bg="#102a43")
        controls.pack(pady=16)
        self.camera_btn = tk.Button(controls, text="कैमरा चालू करें", command=self.toggle_camera, font=("Segoe UI", 12, "bold"), bg="#12b4e8", fg="#001722", padx=18, pady=9, relief="flat")
        self.camera_btn.pack(side="left", padx=6)
        tk.Button(controls, text="स्वागत बोलें", command=lambda: self.say(WELCOME), font=("Segoe UI", 12, "bold"), bg="#ffca3a", fg="#261c00", padx=18, pady=9, relief="flat").pack(side="left", padx=6)
        self.mic_btn = tk.Button(controls, text="🎤 सोनिया सुनो", command=self.listen, font=("Nirmala UI", 12, "bold"), bg="#55ef9c", fg="#062416", padx=18, pady=9, relief="flat")
        self.mic_btn.pack(side="left", padx=6)
        tk.Button(left, text="सभी CSC सेवाएँ देखें", command=self.show_services, font=("Nirmala UI", 11, "bold"), bg="#a78bfa", fg="white", relief="flat", padx=18, pady=7).pack(pady=(0, 12))

        right = tk.Frame(body, bg="#102a43", width=390)
        right.pack(side="right", fill="y", padx=(12, 0))
        right.pack_propagate(False)
        tk.Label(right, text="ग्राहक सहायता", font=("Segoe UI", 18, "bold"), fg="white", bg="#102a43").pack(pady=(18, 10))
        self.chat = tk.Text(right, height=20, wrap="word", font=("Nirmala UI", 12), bg="#f4fbff", fg="#14213d", relief="flat", padx=12, pady=12)
        self.chat.pack(fill="both", expand=True, padx=16)
        self.chat.insert("end", "सोनिया: " + WELCOME + "\n\n")
        self.chat.configure(state="disabled")
        entry_row = tk.Frame(right, bg="#102a43")
        entry_row.pack(fill="x", padx=16, pady=16)
        self.entry = tk.Entry(entry_row, font=("Nirmala UI", 12), relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, ipady=9)
        self.entry.bind("<Return>", lambda _e: self.answer())
        tk.Button(entry_row, text="पूछें", command=self.answer, font=("Segoe UI", 11, "bold"), bg="#55ef9c", fg="#062416", relief="flat", padx=14, pady=8).pack(side="left", padx=(8, 0))

    def say(self, text):
        self.chat.configure(state="normal")
        self.chat.insert("end", f"सोनिया: {text}\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")
        self.voice.speak(text)
        self.status.configure(text="● बोल रही हूँ", fg="#42d6ff")
        self.root.after(3000, lambda: self.status.configure(text="● तैयार", fg="#55ef9c"))

    def answer(self):
        question = self.entry.get().strip()
        if not question:
            return
        response = "इस सेवा की पूरी जानकारी के लिए कृपया जय सिंह जी से संपर्क करें।"
        lower = question.lower()
        for key, value in FAQ.items():
            if key in lower:
                response = value
                break
        else:
            for category in SERVICE_CATALOG:
                for service in category.get("services", []):
                    terms = [service] + category.get("keywords", [])
                    if any(term.lower() in lower for term in terms):
                        response = category.get("response", response)
                        break
                if response != "इस सेवा की पूरी जानकारी के लिए कृपया जय सिंह जी से संपर्क करें।":
                    break
        self.chat.configure(state="normal")
        self.chat.insert("end", f"आप: {question}\nसोनिया: {response}\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")
        self.entry.delete(0, "end")
        self.say(response)

    def show_services(self):
        window = tk.Toplevel(self.root)
        window.title("SHIVEN CSC Centre — सभी सेवाएँ")
        window.geometry("760x620")
        text = tk.Text(window, wrap="word", font=("Nirmala UI", 12), padx=18, pady=18)
        text.pack(fill="both", expand=True)
        for category in SERVICE_CATALOG:
            text.insert("end", category["category"] + "\n", "heading")
            text.insert("end", " • " + "\n • ".join(category["services"]) + "\n\n")
        text.tag_configure("heading", font=("Nirmala UI", 14, "bold"), foreground="#0b5b8e")
        text.configure(state="disabled")

    def listen(self):
        self.mic_btn.configure(state="disabled", text="🎤 सुन रही हूँ...")
        self.status.configure(text="● बोलिए", fg="#ffca3a")

        def record_and_recognize():
            try:
                import sounddevice as sd
                import speech_recognition as sr
                sample_rate = 16000
                seconds = 6
                recording = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
                sd.wait()
                audio = sr.AudioData(recording.tobytes(), sample_rate, 2)
                recognizer = sr.Recognizer()
                question = recognizer.recognize_google(audio, language="hi-IN")
                self.root.after(0, lambda q=question: self._handle_spoken(q))
            except Exception:
                self.root.after(0, self._listen_failed)

        threading.Thread(target=record_and_recognize, daemon=True).start()

    def _handle_spoken(self, question):
        self.mic_btn.configure(state="normal", text="🎤 सोनिया सुनो")
        self.status.configure(text="● समझ गई", fg="#55ef9c")
        self.entry.delete(0, "end")
        self.entry.insert(0, question)
        self.answer()

    def _listen_failed(self):
        self.mic_btn.configure(state="normal", text="🎤 सोनिया सुनो")
        self.status.configure(text="● फिर से बोलें", fg="#ff6b6b")
        messagebox.showinfo("सोनिया सुन नहीं पाई", "Internet और microphone ON रखें। Button दबाकर 6 सेकंड तक साफ Hindi में बोलें।")

    def toggle_camera(self):
        if self.camera_running:
            self.stop_camera()
        else:
            try:
                import cv2
                self.cv2 = cv2
                self.cap = None
                backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY] if os.name == "nt" else [cv2.CAP_ANY]
                for camera_index in (0, 1, 2):
                    for backend in backends:
                        candidate = cv2.VideoCapture(camera_index, backend)
                        if candidate.isOpened():
                            ok, _frame = candidate.read()
                            if ok:
                                self.cap = candidate
                                break
                        candidate.release()
                    if self.cap:
                        break
                if self.cap is None:
                    raise RuntimeError("Camera unavailable")
                self.camera_running = True
                self.camera_btn.configure(text="कैमरा बंद करें", bg="#ff6b6b")
                self.prev_gray = None
                self._camera_loop()
            except Exception:
                messagebox.showerror("कैमरा", "कैमरा नहीं खुला। Logitech camera जोड़ें और Windows Camera permission चालू करें।")

    def start_camera_automatically(self):
        if not self.camera_running:
            self.toggle_camera()

    def _camera_loop(self):
        if not self.camera_running or not self.cap:
            return
        ok, frame = self.cap.read()
        if ok:
            frame = self.cv2.flip(frame, 1)
            gray = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2GRAY)
            small = self.cv2.resize(gray, (160, 120))
            if self.prev_gray is not None:
                change = self.cv2.absdiff(small, self.prev_gray)
                score = float(change.mean())
                if score > 8 and time.time() - self.last_greeting > 60:
                    self.last_greeting = time.time()
                    self.say(WELCOME)
            self.prev_gray = small
            rgb = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
            from PIL import Image, ImageTk
            image = Image.fromarray(rgb)
            image.thumbnail((590, 410))
            photo = ImageTk.PhotoImage(image)
            self.camera_label.configure(image=photo, text="")
            self.camera_label.image = photo
        self.root.after(40, self._camera_loop)

    def stop_camera(self):
        self.camera_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.camera_label.configure(image="", text="कैमरा बंद है\n\nनीचे ‘कैमरा चालू करें’ दबाएँ")
        self.camera_label.image = None
        self.camera_btn.configure(text="कैमरा चालू करें", bg="#12b4e8")

    def close(self):
        self.stop_camera()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    SoniaApp(root)
    root.mainloop()
