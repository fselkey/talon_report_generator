
from website import create_app

import settings
import cursor



if __name__ == '__main__':

    settings.init()
    cursor.init()
    app = create_app()
    print('running on port: ', settings.port)
    print('running on host: ', settings.host)
    app.run(host=settings.host, port=settings.port, debug=False)

