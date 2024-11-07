<p align="center">
  <img src="assets/🅰🔧🤖Typography_tool_kit_plugin.png" alt="Alt text" width="300"/>
</p>

![AI](https://img.shields.io/badge/AI-Machine_Learning-yellow)
![Static Badge](https://img.shields.io/badge/RAG-red) 
![Static Badge](https://img.shields.io/badge/Gemini%20-blue) 
![Typography](https://img.shields.io/badge/Typography-Minimalistic-blueviolet)
![Platform](https://img.shields.io/badge/Platform-Figma-brightgreen)

## 📖 About 
These an api that can be used to help you to choose font for your figma project I use the new 🦾Tech RAG with  Gemini To repersent the best result also it tells you why it choose it and what other fonts you can use with it 

## Installation 
```bash
cd typography-tool-kit-plugin
conda create --name typography python=3.10
conda activate typography
pip install -r requirements.txt
```
make .env file 
```bash 
### your api from google 
GOOGLE_API_KEY = 
```
Run 
```bash
uvicorn main:app --reload
```

