import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def save_links(links, batch_num):
    desktop = get_desktop_path()
    dosya_isimleri = {
        1: "ilk10.txt",
        2: "ikinci10.txt",
        3: "ucuncu10.txt",
        4: "dorduncu10.txt",
        5: "besinci10.txt",
        6: "altinci10.txt",
        7: "yedinci10.txt",
        8: "sekizinci10.txt",
        9: "dokuzuncu10.txt",
        10: "onuncu10.txt",
    }
    filename = dosya_isimleri.get(batch_num, f"batch_{batch_num}.txt")
    filepath = os.path.join(desktop, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")
    print(f"  {len(links)} link kaydedildi: {filepath}")

def clean_url(url):
    url = url.rstrip("/")
    return url

def main():
    print("=" * 50)
    print("  FullHDFilmizlesene Film Linki Cekici")
    print("=" * 50)

    category_url = input("\nKategori URL'sini girin: ").strip()
    category_url = clean_url(category_url)
    if not category_url.startswith("http"):
        category_url = "https://www.fullhdfilmizlesene.life" + category_url

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)

    all_links = []
    batch_num = 1
    page = 1
    links_per_batch = []

    try:
        while True:
            if page == 1:
                url = category_url
            else:
                url = f"{category_url}/{page}"

            print(f"\nSayfa {page} yukleniyor: {url}")
            driver.get(url)
            time.sleep(5)

            title = driver.title
            print(f"  Sayfa basligi: {title}")

            film_elements = driver.find_elements(By.CSS_SELECTOR, "li.film a.tt")

            if not film_elements:
                film_elements = driver.find_elements(By.CSS_SELECTOR, "a.tt[href*='/film/']")

            if not film_elements:
                film_elements = driver.find_elements(By.CSS_SELECTOR, "ul.list li a[href*='/film/']")

            if not film_elements:
                print(f"  Sayfa {page}'de film bulunamadi!")
                links = driver.find_elements(By.TAG_NAME, "a")
                film_links = [l for l in links if "/film/" in (l.get_attribute("href") or "")]
                print(f"  /film/ iceren link sayisi: {len(film_links)}")
                break

            page_links = []
            for elem in film_elements:
                href = elem.get_attribute("href")
                if href and href not in page_links:
                    page_links.append(href)

            all_links.extend(page_links)
            links_per_batch.extend(page_links)

            print(f"  {len(page_links)} film linki bulundu (Toplam: {len(all_links)})")

            if (page) % 10 == 0:
                save_links(links_per_batch, batch_num)
                links_per_batch = []
                batch_num += 1

                devam = input("\nDevam etmek istiyor musunuz? (E/H): ").strip().upper()
                if devam != "E":
                    print("Durduruldu.")
                    break

            page += 1

    except KeyboardInterrupt:
        print("\nKullanici tarafindan durduruldu.")
    except Exception as e:
        print(f"\nHata olustu: {e}")
    finally:
        if links_per_batch:
            save_links(links_per_batch, batch_num)

        driver.quit()
        print(f"\nToplam {len(all_links)} link cekildi.")
        print("Islem tamamlandi!")

if __name__ == "__main__":
    main()
