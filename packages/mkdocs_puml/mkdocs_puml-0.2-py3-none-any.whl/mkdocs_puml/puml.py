import re
import typing
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
from xml.dom.minidom import Element, parseString  # nosec

import requests

from mkdocs_puml.encoder import encode


class PlantUML:
    """PlantUML converter class.
    It requests PUML service, updates received `svg`
    and returns to the user.

    Attributes:
        base_url (str): Base URL to the PUML service
        num_worker (int): The size of pool to run requests in
        _format (str): The format of build diagram. Used in the requesting URL
        _html_comment_regex (re.Pattern): Regex pattern to remove html comments from received svg

    Examples:
        Use this class as::

            puml = PlantUML("https://www.plantuml.com")
            svg = puml.translate(diagram)
    """
    _format = 'svg'
    _html_comment_regex = re.compile(r"<!--.*?-->", flags=re.DOTALL)

    def __init__(self, base_url: str, num_worker: int = 5):
        self.base_url = base_url if base_url.endswith('/') else f"{base_url}/"

        if num_worker <= 0:
            raise ValueError("`num_worker` argument should be bigger than 0.")
        self.num_worker = num_worker

    def translate(self, diagrams: typing.List[str]) -> typing.List[str]:
        """Translate string diagram into HTML div
        block containing the received SVG image.

        Examples:
                This method translates content
                into <svg> image of the diagram

        Args:
            diagrams (str): string representation of PUML diagram
        Returns:
             SVG image of built diagram
        """
        encoded = [self.preprocess(v) for v in diagrams]

        with ThreadPoolExecutor(max_workers=self.num_worker) as executor:
            futures = [executor.submit(self.request, v) for v in encoded]
            svg_images = [v.result() for v in as_completed(futures)]

        return [self.postprocess(v) for v in svg_images]

    def preprocess(self, content: str) -> str:
        """Preprocess the content before pass it
        to the plantuml service.

        Encoding of the content should be
        done in the step of preprocessing.

        Args:
            content (str): string representation PUML diagram
        Returns:
            Preprocessed PUML diagram
        """
        return encode(content)

    def postprocess(self, content: str) -> str:
        """Postprocess the received from plantuml service
        SVG diagram.

        Potentially, here could be the code
        that applies CSS styling to the SVG.

        Args:
            content (str): SVG representation of build diagram
        Returns:
            Postprocessed SVG diagram
        """
        diagram_content = self._clean_comments(content)

        svg = self._convert_to_dom(diagram_content)
        self._stylize_svg(svg)

        return svg.toxml()

    def request(self, encoded_diagram: str) -> str:
        """Request plantuml service with the encoded diagram;
        return SVG content

        Args:
            encoded_diagram (str): Encoded string representation of the diagram
        Returns:
            SVG representation of the diagram
        """
        resp = requests.get(urljoin(self.base_url, f"{self._format}/{encoded_diagram}"))
        return resp.content.decode('utf-8')

    def _clean_comments(self, content: str) -> str:
        return self._html_comment_regex.sub("", content)

    def _convert_to_dom(self, content: str) -> Element:
        """The method to convert received SVG into XML DOM
        for future modifications
        """
        dom = parseString(content)  # nosec
        svg = dom.getElementsByTagName('svg')[0]
        return svg

    def _stylize_svg(self, svg: Element):
        """This method is used for SVG tags modifications.

        Notes:
            It can be used to add support of light / dark theme.
        """
        svg.setAttribute('preserveAspectRatio', "true")
        svg.setAttribute('style', 'background: #ffffff')
