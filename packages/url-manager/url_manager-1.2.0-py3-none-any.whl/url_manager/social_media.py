import re

from url_manager.enum import StrEnum
from url_manager.helper import compose


class TopLevelDomains(StrEnum):
    COM = "com"
    ME = "me"


def extract_valid_url(url: str) -> str:
    url_formatted = compose(
        _remove_www_from_url,
        _remove_query_params_from_url,
        _transform_http_to_https,
        _remove_everything_after_dot_top_domains,
    )(url)

    return url_formatted


def _remove_www_from_url(source_url: str) -> str:
    return source_url.replace("www.", "")


def _remove_query_params_from_url(source_url: str) -> str:
    return re.sub(r"\?.*", "", source_url)


def _transform_http_to_https(source_url: str) -> str:
    return source_url.replace("http://", "https://")


def _remove_everything_after_dot_top_domains(source_url: str) -> str:
    """
    Remove everything after the first dot and the dot itself.

    Examples:

        input: https://www.teste.com/xpto
        output: https://www.teste.com

        input: https://www.instagram.com/jorge.comoficial/
        output: https://www.instagram.com

    """
    top_level_domains = list(TopLevelDomains)

    for top_level_domain in top_level_domains:
        if source_url.find(f".{top_level_domain}") >= 0:
            source_url = source_url[:source_url.find(f".{top_level_domain}") + len(top_level_domain) + 1]

    return source_url
