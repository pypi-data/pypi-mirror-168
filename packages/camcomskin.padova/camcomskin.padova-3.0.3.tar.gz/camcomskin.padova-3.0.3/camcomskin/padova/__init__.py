# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory
from redturtle.chefcookie import defaults
from bs4 import BeautifulSoup
from redturtle.chefcookie import _
from zope.globalrequest import getRequest
from zope.i18n import translate

_ = MessageFactory("camcomskin.padova")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


def iframe_placeholder(name, soup=None):
    request = getRequest()
    if not soup:
        soup = BeautifulSoup("", "html.parser")
    tag = soup.new_tag("div")
    tag["class"] = "iframe-placeholder"
    tag[
        "style"
    ] = "padding: 10px; background-color: #eee; border:1px solid #ccc;width:98%; max-width:500px"
    p_tag = soup.new_tag("p")
    p_tag.string = "Devi accettare i cookie di {} per vedere questo contenuto.".format(
        name
    )
    tag.append(p_tag)

    span_tag = soup.new_tag("span")
    span_tag.string = "Per favore, abilitali dal menu di configurazione dei cookie che trovi sulla destra."
    tag.append(span_tag)
    return tag


defaults.iframe_placeholder = iframe_placeholder
