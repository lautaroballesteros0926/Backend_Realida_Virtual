import google.generativeai as genai

genai.configure(api_key="AIzaSyBNErCncCpVuo9tM8Zxw1515VByzfTzKDI")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("¿Cuál es la capital de Francia?")
print(response.text)
