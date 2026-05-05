import os
import urllib.parse
import asyncio
import aiohttp
from dotenv import load_dotenv


load_dotenv()

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
DISK_TOKEN = os.environ.get('DISK_TOKEN')
AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}


async def async_upload_files_to_yadisk(files):
    """Загружает несколько файлов параллельно."""
    if files is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for file in files:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, file)
                    )
                )
            filenames_links = await asyncio.gather(*tasks)
        return filenames_links


async def upload_file_and_get_url(session, file):
    """Загружает один файл на Ядиск.
    Получает ссылку на загрузку файла.
    По данной ссылке загружает файл на ЯДиск.
    Получает ссылку для скачивания файла с ЯДиск.
    """
    payload = {
        'path': f'app:/{file.filename}',
        'overwrite': 'True'
    }
    async with session.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL
    ) as response:
        response = await response.json()
        upload_url = response['href']
    filename = file.filename
    file = file.read()
    async with session.put(
        data=file,
        url=upload_url
    ) as response:
        yadisk_path = response.headers['Location']
        yadisk_path = urllib.parse.unquote(yadisk_path)
        yadisk_path = yadisk_path.replace('/disk', '')
    async with session.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': yadisk_path}
    ) as response:
        response = await response.json()
        original_link = response['href']
    return (filename, original_link)
