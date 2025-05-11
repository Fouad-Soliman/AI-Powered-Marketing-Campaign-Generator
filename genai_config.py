import google.generativeai as genai

def configure_gemini():
    genai.configure(api_key="AIzaSyDphGovO3le5oZMfdCdVSuObg_9kz2tBWg")
    return genai.GenerativeModel("gemini-2.0-flash-exp")