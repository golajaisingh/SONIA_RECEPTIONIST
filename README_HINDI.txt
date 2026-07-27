SONIA AI RECEPTIONIST FINAL COMPLETE — SHIVEN CSC CENTRE
=========================================

इस folder में Sonia_Setup.exe बनाने के लिए सभी project files व्यवस्थित हैं।

WINDOWS 11 पर केवल यह करें:

1. इस ZIP को Extract All करें।
2. Python 3 install करें और “Add Python to PATH” चुनें।
3. Inno Setup 6 install करें।
4. BUILD_SONIA_SETUP.bat पर double-click करें।
5. तैयार installer यहाँ मिलेगा:
   OUTPUT\Sonia_Setup.exe

पहली बार app चलाने पर:

1. Logitech 720p camera और microphone जोड़ें।
2. Windows Settings > Privacy & security > Camera में Camera access ON करें।
3. Windows Settings > Time & language > Speech में Hindi voice install करें।
4. Sonia खोलकर “कैमरा चालू करें” दबाएँ।

जरूरी बात:

- Sonia का EXE बनने के बाद Python की आवश्यकता नहीं रहती।
- Hindi female voice Windows में installed voice पर निर्भर है।
- ग्राहक के सामने movement होने पर Sonia स्वागत बोलेगी।
- एक स्वागत के बाद 45 सेकंड का अंतर रखा गया है।
- BUILD002 camera 0, 1 और 2 तथा Windows के अलग camera modes स्वयं जाँचती है।
- Sonia जो भी बोलेगी, वही Hindi message screen पर भी दिखाई देगा।
- BUILD003 में Windows voice उसी thread में शुरू और चलती है, जिससे silent voice की समस्या ठीक होती है।
- BUILD004 में screen पर Hindi रहती है और voice को Roman Hindi pronunciation दी जाती है,
  ताकि Windows केवल “CSC” नहीं बल्कि पूरा Hindi स्वागत बोले।
- BUILD005 build के समय साफ Hindi female Swara voice बनाकर app में save करती है।
  Build के समय internet चाहिए; तैयार EXE की saved welcome और service आवाजें offline चलेंगी।
- यह corrected package नए Python के साथ चलने वाला हल्का audio player उपयोग करती है।
- FINAL BUILD006 में “सोनिया सुनो” microphone button है।
- Button दबाने के बाद 6 सेकंड तक Hindi में बोलें। आवाज पहचानने के लिए internet चाहिए।
- Camera, saved Hindi female voice और typed CSC answers offline चलते हैं।
- सभी प्रमुख CSC service categories services.json में हैं और “सभी CSC सेवाएँ देखें” button से खुलती हैं।
- नई या स्थानीय service जोड़ने के लिए services.json edit करें; EXE दोबारा बनाने की जरूरत नहीं।
- किसी service की वास्तविक उपलब्धता Digital Seva/Delhi portal पर समय के साथ बदल सकती है।
- App खुलते ही Logitech camera अपने-आप ON होता है।
- ग्राहक के प्रवेश/movement पर Sonia Hindi female voice में स्वागत करती है।
- दो automatic welcome के बीच 60 सेकंड का अंतर है।

Business name: SHIVEN CSC Centre
Spoken pronunciation: शिवैन CSC सेंटर
Default welcome:
“नमस्ते! शिवैन CSC सेंटर में आपका हार्दिक स्वागत है।”
