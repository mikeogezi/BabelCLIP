import asyncio
from pyppeteer import launch
import os
import numpy as np

async def main():
    browser = await launch(
        options={
            'headless': True,
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                '--disable-gpu',
            ],
        },
    )

    for id in ['.25g.1', '.25g.2', '.25s.1', '.25s.2'][:2]:
        # print('Converting .ipynb to .html')
        # proc = await asyncio.create_subprocess_exec(
        #     'jupyter nbconvert --to html evaluate.ipynb --output evaluate{}.html'.format(id),
        #     stdout=asyncio.subprocess.PIPE,
        #     stderr=asyncio.subprocess.PIPE
        # )
        # stdout, stderr = await proc.communicate()

        page = await browser.newPage()
        
        print('Converting .html to .pdf')
        await page.goto('file:///home/ogezi/CMPUT_600/project/evaluate{}.html'.format(id))
        
        await page.pdf({'path': 'evaluate{}.pdf'.format(id)})
    
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
