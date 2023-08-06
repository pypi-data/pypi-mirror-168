from datetime import datetime
from typing import Union

import pymsteams

from pyiris.infrastructure.common.message import ErrorMessage
from pyiris.infrastructure.service.monitor.log.logger import Logger

logger = Logger(__name__)


class MsTeams(object):
    @staticmethod
    def send_error_message(
        webhook_url: str, message: Union[ErrorMessage], default_timeout: int = 10
    ):
        try:
            card_section = pymsteams.cardsection()
            card_section.activityTitle(message.title)
            card_section.activityImage(message.image)
            card_section.addImage(message.image, ititle="Error ")

            card_section.addFact("Message:", f"{message.subtitle} At: {datetime.now()}")
            card_section.addFact("Error:", message.message)
            card_section.addFact("Traceback:", message.traceback)
            card_section.linkButton("Open for more details", message.link)

            connector = pymsteams.connectorcard(
                hookurl=webhook_url, http_timeout=default_timeout
            )
            connector.addSection(card_section)
            connector.summary(message.title)
            connector.color(mcolor=message.color)
            return connector.send()
        except Exception as e:
            logger.error(
                message="Error when try to send message to Microsoft Teams. {message}".format(
                    message=repr(e)
                )
            )
