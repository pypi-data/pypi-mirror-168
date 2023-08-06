from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from stix2patterns.exceptions import STIXPatternErrorListener
from stix2patterns.v20.grammars.STIXPatternLexer import STIXPatternLexer as lexer_v20
from stix2patterns.v20.grammars.STIXPatternParser import STIXPatternParser as parser_v20
from stix2patterns.v20.inspector import InspectionListener as inspector_v20
from stix2patterns.v21.grammars.STIXPatternLexer import STIXPatternLexer as lexer_v21
from stix2patterns.v21.grammars.STIXPatternParser import STIXPatternParser as parser_v21
from stix2patterns.v21.inspector import InspectionListener as inspector_v21

_VALID_VERSIONS = ('2.0', '2.1')


class STIX2PatternParser:
    def __init__(self, version: str):
        self.__version = version.strip('.') if version in _VALID_VERSIONS else '2.1'

    @property
    def version(self) -> str:
        return self.__version

    def load_stix_pattern(self, pattern_str: str):
        getattr(self, f'_load_stix_{self.version}_pattern')(pattern_str)

    def _load_stix_20_pattern(self, pattern_str: str):
        pattern = InputStream(pattern_str)