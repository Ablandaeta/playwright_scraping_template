from playwright.sync_api import sync_playwright, Playwright
from datetime import datetime
from progress_state import load_state, save_state, save_to_csv, save_to_csv_init


start_time = datetime.now()
print(f"Tiempo de inicio: {start_time}")

BASE_URL = "URL_DE_EJEMPLO" # Reemplazar con la URL base real si es necesario
TARGET_URL = "URL_DE_EJEMPLO" # Reemplazar con la URL real

data = []

def run(playwright: Playwright) -> None:
    url = TARGET_URL
    chrome = playwright.chromium
    browser = chrome.launch(headless=False)
    context = browser.new_context()
    
    # Bloquear carga de imágenes para acelerar
    def route_intercept(route):
        if route.request.resource_type == "image":
            route.abort()
        else:
            route.continue_()
            
    context.route("**/*", route_intercept)
    
    page = context.new_page()

    # Cargar estado previo
    state = load_state()
    start_page = state["last_page"] + 1
    processed_urls = set(state["processed_urls"])
    processed_documents_urls = set(state["processed_documents_urls"])
    
    print(f"📌 Iniciando desde la página {start_page}")
    print(f"📊 URLs ya procesadas: {len(processed_urls)}")
    print(f"📊 Documentos ya procesados: {len(processed_documents_urls)}")
    response = page.goto(url)

    if response and (response.status == 500 or response.status == 404):
        print(f"  ⚠️  Error {response.status}  url: {url}")
        page.close()
        return

    # Navegar a la página donde quedamos
    if start_page > 1:
        print(f"⏩ Avanzando a la página {start_page}...")
        for _ in range(start_page - 1):
            next_btn = page.locator('') # Completar con el selector adecuado
            if next_btn.count() > 0:
                next_btn.click()
            else:
                print("⚠️ No se pudo avanzar, iniciando desde página actual")
                break    
    
    
    current_page = start_page
    page_data = []  # Datos de la página actual

    while True:
        # Lógica para procesar la página actual
        elements = page.locator('').all() # Completar con el selector adecuado
        print(f"\n📄 Procesando página {current_page} ({len(elements)} elementos)")

        for idx, element in enumerate(elements, 1):
            element_page = context.new_page() # Abrir nueva pestaña            
            element_url = element.get_attribute("href") # or BASE_URL + element.get_attribute("href") # Completa el atributo href si es necesario
            
            # Saltar si ya procesamos esta URL
            if element_url in processed_urls:
                print(f"  ⏭️  [{idx}/{len(elements)}] Ya procesada, saltando...")
                element_page.close()
                continue

            if element_url in processed_urls:
                print(f"     ⏭️  Ya procesada: {element_url}")
                continue

            if element_url is not None:
                try:
                    response = element_page.goto(element_url)
                    document_url = element_page.locator('').text_content()  # Completar con el selector adecuado
                    if document_url in processed_documents_urls:
                        print(f"     ⏭️  Documento procesado: {document_url}")
                        continue

                    page_data.append([title, element_url])  # Guardar datos de la publicación
                    processed_urls.add(element_url)
                    print(f"  ✅ [{idx}/{len(elements)}] {title[:50]}...")

                except Exception as e:
                    print(f"  ❌ [{idx}/{len(elements)}] {title[:50]}... ¡Scraping interrumpido! \n{element_page.url}")
                                        
                    end_time = datetime.now()
                    duration = end_time - start_time
                    
                    print(f"  ❌ Tiempo total: {duration}")
                    print(f"  ❌ Error: {e}")                 
                    
                    return
                finally:
                    element_page.close()
            else:
                element_page.close()    

        # Guardar progreso de esta página
        if page_data:
            if current_page == 1:
                # Inicializar CSV
                save_to_csv_init([['Título', 'Fecha','Document_URL']]) # titulos de las columnas
            save_to_csv(page_data)
            data.extend(page_data)
            print(f"💾 Guardados {len(page_data)} registros de la página {current_page}")
            page_data = []
        
        # Guardar estado
        save_state(current_page, list(processed_urls), list(processed_documents_urls))

        # Lógica de paginacion y break
        page_number = page.locator('') # Completar con el selector adecuado
        print(f"📍 Página {page_number[0]} de {page_number[2]}")

        if int(page_number[0]) >= int(page_number[2]):
            end_time = datetime.now()
            duration = end_time - start_time
            print(f"Tiempo total: {duration}")
            print("\n✅ ¡Scraping completado!")
            break
        else:
            # Navegar a la siguiente página
            next_button = page.locator('') # Completar con el selector adecuado
            if next_button.is_enabled():
                next_button.click()
                current_page += 1
            else:
                print("  ⚠️  No se pudo encontrar el botón de siguiente página.")
                break

    print(f"\n📊 Total de registros extraídos: {len(data)}")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)