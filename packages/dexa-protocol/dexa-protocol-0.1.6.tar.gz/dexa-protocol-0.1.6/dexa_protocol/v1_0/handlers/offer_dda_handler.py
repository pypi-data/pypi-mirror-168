from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)
from dexa_protocol.v1_0.messages.negotiation.offer_dda import OfferDDAMessage
from dexa_sdk.managers.dexa_manager import DexaManager


class OfferDDAMessageHandler(BaseHandler):
    """Offer DDA message handler logic"""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """Handle function"""

        assert isinstance(context.message, OfferDDAMessage)

        # Initialise the manager.
        mgr = DexaManager(context)

        # Process the message.
        await mgr.process_offer_dda_message(context.message, context.message_receipt)
