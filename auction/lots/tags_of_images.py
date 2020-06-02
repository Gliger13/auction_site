import asyncio

import aiohttp

from auction import secrets
from lots.models import ImageTags


async def images_tags(lot):
    headers = {
        'Ocp-Apim-Subscription-Key': secrets.SUBSCRIPTION_KEY,
        'Content-Type': 'application/octet-stream',
    }
    params = {'visualFeatures': 'Categories,Description,Color'}
    image_data = lot.image.read()
    async with aiohttp.ClientSession() as session:
        async with session.post(
                secrets.FOR_IMG_API,
                headers=headers,
                params=params,
                data=image_data,
        ) as response:
            data = await response.json()
            response_status = response.status
            await session.close()
    if response_status == 200 and data:
        for tag in data.get('tags'):
            image_tags = ImageTags()
            image_tags.lot = lot
            image_tags.tag_name = tag.get('name')
            confidence = tag.get('confidence')
            image_tags.confidence = round(float(confidence), 2)
            await asyncio.get_running_loop().run_in_executor(None, image_tags.save)
