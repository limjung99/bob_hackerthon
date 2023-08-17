import uvicorn
from config import conf
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

if __name__ == '__main__':
    try:
        if conf['log'] != 'debug':
            uvicorn.run(
                "api:app",
                host='0.0.0.0',
                port=8080,
                workers=4,
                log_level='debug',
                reload=True,
            )
        else:
            uvicorn.run(
                "api:app",
                host='0.0.0.0',
                port=8080,
                workers=5,
                log_level='warning',
                reload=False,
            )
    except KeyboardInterrupt:
        print('\nExiting\n')
    except Exception as errormain:
        print('Failed to Start API')
        print('='*100)
        print(str(errormain))
        print('='*100)
        print('Exiting\n')