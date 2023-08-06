# © https://t.me/DKBOTZ or https://t.me/DK_BOTZ
# This API is Created By https://t.me/DKBOTZ

import asyncio
import re
import aiohttp
from urllib.parse import urlparse


class MdiskPro:
    """
    A Unofficial Wrapper for Adlinkfly Site and Alternative Sites
    
    :param api_key: Your API key
    :type api_key: str
    :param base_site: The site you want to use, defaults to droplink.co
    :type base_site: str (optional)
    """

    def __init__(self, api_key:str, base_site:str='mdiskpro.xyz'):
        self.__api_key = api_key
        self.__base_site = base_site
        self.__api_par = "api"
        self.__url_par = "url"
        self.__jsonpar = "shortenedUrl"
        self.qlink_par = "https://mdiskpro.xyz/st?api={api_key}&url={url}"
        self.__base_url = f"https://mdiskpro.xyz/api"
        self.mime_type = "application/json"




        if not self.__api_key:
            raise Exception("API key not provided")

    async def __fetch(self, session:aiohttp.ClientSession, params:dict) -> dict:
        """
        It takes a URL, a session, and a dictionary of parameters, and returns a JSON object
        
        :param url: The URL of the API endpoint we're requesting
        :param session: the aiohttp session object
        :param params: The parameters to pass to the API
        :return: A list of dictionaries.
        By https://t.me/DKBOTZ
        """
        async with session.get(self.__base_url, params=params, raise_for_status=True, ssl=False) as response:
            result = await response.json(content_type=self.mime_type) 
            return result

    async def convert(
        self, 
        link:str, 
        alias:str='',
        silently_fail:bool = False, 
        quick_link:bool = False,) -> str:
        """
        It converts a link to a short link.
        
        :param link: The link you want to shorten
        :type link: str

        :param alias: The alias you want to use for the link
        :type alias: str

        :param silently_fail: If this is set to True, then instead of raising an exception, it will return
        the original link, defaults to False
        :type silently_fail: bool (optional)

        :param quick_link: If you want to get a quick link, set this to True, defaults to False
        :type quick_link: bool (optional)
        
        :return: The shortened link is being returned.
        By https://t.me/DKBOTZ
        """

        is_short_link = await self.is_short_link(link)

        if not is_short_link:

            if quick_link:
                return await self.get_quick_link(url=link)

            else:  
                params = {
                    self.__api_par: self.__api_key,
                    self.__url_par : link,
                    'alias': alias,
                    'format':'json'
                        }
                try:
                    my_conn = aiohttp.TCPConnector(limit=10)
                    async with aiohttp.ClientSession(connector=my_conn) as session:
                        session = session     
                        data = await self.__fetch(session, params)

                        if data["status"] == "success":
                            return data[self.__jsonpar]
                        else:
                            print(data['message'])
                            return await self.__error_handler(url=link, silently_fail=silently_fail, exception=Exception)

                except Exception as e:
                    print(e)
                    return await self.__error_handler(url=link, silently_fail=silently_fail, exception=Exception)

        else: return link

    async def get_quick_link(self, url:str, **kwargs) -> str:
        """
        It returns the quick link for a given link
        
        :param urls: A list of urls to convert
        :alias: The alias to use for the link
        :return: The converted links.
        By https://t.me/DKBOTZ
        """
        link = self.qlink_par.format(base_site=self.__base_site, api_key=self.__api_key, url=url)
        return link





    async def is_short_link(self, link:str) -> bool:
        """
        It checks if the link is a valid mdisk link.
        
        :param link: The link to the file
        :type link: str
        :return: True if the link is a valid mdisk link, False otherwise
        By https://t.me/DKBOTZ
        """
        domain = urlparse(link).netloc
        if self.__base_site in domain:
            return True
        return False

    async def __error_handler(self, url:str, silently_fail:bool, exception=Exception, message="Some error occurred during converting: %s"):
        """
        If the URL is valid, return it. If it's not, return it or raise an exception, depending on the value
        of the `silently_fail` parameter
        
        :param url: The URL to be validated
        :type url: str
        :param silently_fail: If True, then if the URL is not valid, return the original URL. If False,
        raise an exception
        :type silently_fail: bool
        :param exception: The exception to raise if the URL is not valid
        :return: The url is being returned.
        """
        if silently_fail:
            return url
        else:
            raise exception(message % url)

    async def __extract_url(self, string:str) -> list:
        regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
        urls = re.findall(regex, string)
        return ["".join(x) for x in urls]

    @staticmethod
    def available_websites():
        available_websites = ["mdiskpro.in", "mdiskpro.xyz"]
        return "\n".join(available_websites)
