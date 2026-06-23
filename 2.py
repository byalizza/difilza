import os
import glob
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def find_txt_files():
    desktop = get_desktop_path()
    txt_files = sorted(glob.glob(os.path.join(desktop, "*.txt")))
    return txt_files

def extract_embed_url(driver, film_url):
    try:
        driver.get(film_url)
        time.sleep(3)

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            src = iframe.get_attribute("src")
            if src and ("rapidvid" in src or "embed" in src or "vod" in src):
                return src

        page_source = driver.page_source
        import re
        urls = re.findall(r'https?://[^\s"\'<>]+(?:rapidvid|embed|vod)[^\s"\'<>]*', page_source)
        if urls:
            return urls[0]

        return None
    except Exception as e:
        print(f"    Hata: {e}")
        return None

def main():
    print("=" * 50)
    print("  Embed Link Cekici")
    print("=" * 50)

    txt_files = find_txt_files()

    if not txt_files:
        print("\nMasaustunde .txt dosyasi bulunamadi!")
        print("Once 1.py'yi calistirarak linkleri cekin.")
        input("\nCikis icin Enter'a basin...")
        return

    print("\nBulunan txt dosyalari:")
    for i, f in enumerate(txt_files, 1):
        print(f"  {i}. {os.path.basename(f)}")

    secim = input("\nHangi dosyayi islemek istersiniz? (sayi/hepsi): ").strip().lower()

    secili_dosyalar = []
    if secim == "hepsi":
        secili_dosyalar = txt_files
    else:
        try:
            idx = int(secim) - 1
            if 0 <= idx < len(txt_files):
                secili_dosyalar = [txt_files[idx]]
            else:
                print("Gecersiz secim!")
                input("Cikis icin Enter'a basin...")
                return
        except ValueError:
            print("Gecersiz secim!")
            input("Cikis icin Enter'a basin...")
            return

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    print("\nChrome baslatiliyor...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)

    desktop = get_desktop_path()

    try:
        for dosya in secili_dosyalar:
            dosya_adi = os.path.basename(dosya).replace(".txt", "")
            sonuc_dosyasi = os.path.join(desktop, f"{dosya_adi}_embed.txt")

            print(f"\n{'='*40}")
            print(f"Isleniyor: {dosya_adi}")
            print(f"Sonuc: {sonuc_dosyasi}")
            print(f"{'='*40}")

            with open(dosya, "r", encoding="utf-8") as f:
                links = [line.strip() for line in f if line.strip()]

            toplam = 0
            with open(sonuc_dosyasi, "w", encoding="utf-8") as sonuc:
                for i, link in enumerate(links, 1):
                    print(f"\n  [{i}/{len(links)}] {link}")

                    embed = extract_embed_url(driver, link)

                    if embed:
                        sonuc.write(f"{link} -> {embed}\n")
                        sonuc.flush()
                        toplam += 1
                        print(f"    Bulundu: {embed}")
                    else:
                        sonuc.write(f"{link} -> BULUNAMADI\n")
                        sonuc.flush()
                        print(f"    Embed bulunamadi")

            print(f"\n  {dosya_adi}: {toplam} embed cekildi")

    except KeyboardInterrupt:
        print("\n\nKullanici tarafindan durduruldu.")
    except Exception as e:
        print(f"\nHata: {e}")
    finally:
        driver.quit()
        print("\nIslem tamamlandi!")
        input("\nCikis icin Enter'a basin...")

if __name__ == "__main__":
    main()