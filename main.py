import time
import subprocess
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from pynput import keyboard


def download_m3u8_with_ffmpeg(m3u8_url, filename="video_review.mp4"):
    print(f"Скачивание: {m3u8_url}")
    command = [
        'ffmpeg',
        '-i', m3u8_url,
        '-c', 'copy',
        filename
    ]
    subprocess.run(command)


def process_video(driver):
    time.sleep(1)
    m3u8_links = [
        request.url for request in driver.requests
        if request.response and ".m3u8" in request.url
    ]
    if m3u8_links:
        m3u8_url = m3u8_links[-1]
        download_m3u8_with_ffmpeg(m3u8_url)
    else:
        print("Ссылок .m3u8 не найдено. Возможно, видео еще не подгрузилось.")


def on_press(key, driver):
    try:
        if key == keyboard.Key.f4:
            print("Нажата клавиша F4, пытаемся скачать видео...")
            process_video(driver)
    except Exception as e:
        print(f"Ошибка в обработчике клавиш: {e}")


def main():
    chrome_options = Options()
    chrome_options.add_argument("--remote-debugging-port=9222")  # если нужно
    chrome_options.add_argument("--user-data-dir=ChromeDebug")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    listener = keyboard.Listener(on_press=lambda key: on_press(key, driver))
    listener.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Остановка скрипта.")
    finally:
        driver.quit()
        listener.stop()


if __name__ == "__main__":
    main()
