from playwright.sync_api import sync_playwright, Playwright
from datetime import datetime
from progress_state import load_state, save_state, save_to_csv, save_to_csv_init


start_time = datetime.now()
print(f"Tiempo de inicio: {start_time}")

data = []

def run(playwright: Playwright) -> None:
    url = "URL_DE_EJEMPLO" # Reemplazar con la URL real 
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
    
    print(f"📌 Iniciando desde la página {start_page}")
    print(f"📊 URLs ya procesadas: {len(processed_urls)}")
    response = page.goto(url)

    if response and (response.status == 500 or response.status == 404):
        print(f"  ⚠️  Error {response.status}  url: {url}")
        page.close()
        return
    
    
    current_page = start_page
    page_data = []  # Datos de la página actual

    while True:
        # Lógica para procesar la página actual
        elements = page.locator('').all() # Completar con el selector adecuado
        print(f"\n📄 Procesando página {current_page} ({len(elements)} elementos)")

        for idx, element in enumerate(elements, 1):
            element_page = context.new_page() # Abrir nueva pestaña
            base_url = "BASE_URL" # Reemplazar con la URL base real si es necesario
            element_url = element.get_attribute("href") or base_url + element.get_attribute("href") # Completa el atributo href si es necesario
            
            # Saltar si ya procesamos esta URL
            if element_url in processed_urls:
                print(f"  ⏭️  [{idx}/{len(elements)}] Ya procesada, saltando...")
                element_page.close()
                continue

            if element_url is not None:
                try:
                    response = element_page.goto(element_url)
                    title = element_page.locator('').text_content()  # Completar con el selector adecuado
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
                save_to_csv_init([['Título', 'URL']])  # Encabezados CSV (solo primera página)
            save_to_csv(page_data)
            data.extend(page_data)
            print(f"💾 Guardados {len(page_data)} registros de la página {current_page}")
            page_data = []
        
        # Guardar estado
        save_state(current_page, list(processed_urls))

        # Lógica de paginacion y break 
        ''' leer el número de página actual y total      
        @ejemplo de selector: <span class="text-base -mt-1">1 de 10</span>
        page_number = (page.locator('span[class="text-base -mt-1"]').text_content().split(' '))
        @returns ['1', 'de', '10']
        '''
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