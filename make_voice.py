import asyncio
from pathlib import Path
import edge_tts

VOICE = "hi-IN-SwaraNeural"
RATE = "+10%"
OUT = Path(__file__).resolve().parent / "assets"

LINES = {
    "welcome.mp3": "नमस्ते! शिवैन सी एस सी सेंटर में आपका हार्दिक स्वागत है। मैं सोनिया हूँ। बताइए, मैं आपकी क्या सहायता कर सकती हूँ?",
    "aadhaar.mp3": "आधार सेवा के लिए कृपया अपना आधार कार्ड और आवश्यक दस्तावेज साथ रखें।",
    "baal_aadhaar.mp3": "बाल आधार के लिए बच्चे का जन्म प्रमाणपत्र और माता या पिता का आधार कार्ड आवश्यक है।",
    "pan.mp3": "पैन कार्ड आवेदन के लिए आधार कार्ड, फोटो और मोबाइल नंबर की आवश्यकता होगी।",
    "income.mp3": "आय प्रमाणपत्र के लिए आधार, पते का प्रमाण और आय से जुड़े दस्तावेज आवश्यक हैं।",
    "caste.mp3": "जाति प्रमाणपत्र के लिए आधार, पते का प्रमाण और परिवार का संबंधित प्रमाणपत्र साथ लाएँ।",
    "pcc.mp3": "पुलिस क्लीयरेंस सर्टिफिकेट के लिए पहचान, पते का प्रमाण और आवेदन का उद्देश्य आवश्यक होगा।",
    "print.mp3": "यहाँ प्रिंट, स्कैन, फोटोकॉपी और ऑनलाइन फॉर्म की सुविधा उपलब्ध है।",
}


async def main():
    OUT.mkdir(exist_ok=True)
    for filename, text in LINES.items():
        print("Creating", filename)
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(OUT / filename))


if __name__ == "__main__":
    asyncio.run(main())
