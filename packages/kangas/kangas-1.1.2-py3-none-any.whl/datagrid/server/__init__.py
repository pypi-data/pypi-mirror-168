# -*- coding: utf-8 -*-
######################################################
#     _____                  _____      _     _      #
#    (____ \       _        |  ___)    (_)   | |     #
#     _   \ \ ____| |_  ____| | ___ ___ _  _ | |     #
#    | |  | )/ _  |  _)/ _  | |(_  / __) |/ || |     #
#    | |__/ ( ( | | | ( ( | | |__| | | | ( (_| |     #
#    |_____/ \_||_|___)\_||_|_____/|_| |_|\____|     #
#                                                    #
#    Copyright (c) 2022 DataGrid Development Team    #
#    All rights reserved                             #
######################################################

import asyncio
import logging

import tornado.log
import tornado.web

from .handlers import datagrid_handlers
from .queries import DATAGRID_ROOT  # noqa


def start_tornado_server(port, output="yes"):
    """
    Args:
        port: (int) the port to start the frontend server
        output: (str) "no" means suppress output
    """

    async def main():
        if output == "no":
            hn = logging.NullHandler()
            hn.setLevel(logging.WARNING)
            for log_name in [
                "tornado.access",
                "tornado.application",
                "tornado.general",
            ]:
                logging.getLogger(log_name).addHandler(hn)
                logging.getLogger(log_name).propagate = False
        else:
            tornado.log.enable_pretty_logging()

        app = tornado.web.Application(datagrid_handlers)
        app.listen(port)
        await asyncio.Event().wait()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        print("Exiting datagrid server")
