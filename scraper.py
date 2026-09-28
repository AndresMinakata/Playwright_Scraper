import json
import os
import requests
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Iniciamos el navegador en modo headless
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navegar a un sitio de prueba
        print("Navegando a la página...")
        page.goto("https://news.ycombinator.com/")
        
        # Extraer datos: en este caso, los títulos y links de las noticias
        articles = []
        rows = page.locator('.athing').all()
        
        for row in rows[:10]: # Solo tomamos los primeros 10
            title_element = row.locator('.titleline > a').first
            title = title_element.inner_text()
            link = title_element.get_attribute('href')
            
            articles.append({
                "title": title,
                "url": link
            })
            
        browser.close()
        
        # 1. Guardar la data localmente como JSON
        output_file = 'output_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)
        print(f"Datos guardados en {output_file}")

        # 2. (Opcional) Enviar a un Webhook (ej. hacia un flujo de n8n)
        # webhook_url = os.getenv('WEBHOOK_URL') 
        # if webhook_url:
        #     requests.post(webhook_url, json={"data": articles})
        #     print("Datos enviados al webhook exitosamente.")

if __name__ == "__main__":
    run()
