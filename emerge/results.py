"""
Defines non-abstract result classes, e.g. FileResult or EntityResult.
"""

# Authors: Grzegorz Lato <grzegorz.lato@gmail.com>
# License: MIT

from pathlib import PosixPath
from emerge.abstractresult import AbstractFileResult, AbstractEntityResult
from emerge.languages.abstractparser import AbstractParsingCore, CoreParsingKeyword, LanguageType
from emerge.statistics import Statistics
import coloredlogs
import logging
import os

from emerge.logging import Logger

from typing import Dict, List

LOGGER = Logger(logging.getLogger('parser'))
coloredlogs.install(level='E', logger=LOGGER.logger(), fmt=Logger.log_format)


class EntityResult(AbstractEntityResult):
    """An EntityResult is always generated from a FileResult and contains only the source of an extracted entity from the FileResult, e.g. a class.
    An EntityResult has a unique/entity name and can contain inheritace dependencies.
    """

    def __init__(self, *,
                 analysis,
                 scanned_file_name: str,
                 absolute_name: str,
                 display_name: str,
                 scanned_by,
                 scanned_language,
                 scanned_tokens,
                 scanned_import_dependencies: List,
                 entity_name: str,
                 module_name: str,
                 unique_name: str,
                 parent_file_result: 'FileResult'
                 ):
        self._analysis = analysis
        self._scanned_file_name = scanned_file_name
        self._absolute_name = absolute_name
        self._display_name = display_name
        self._scanned_language = scanned_language
        self._scanned_by = scanned_by
        self._scanned_tokens = scanned_tokens
        self._scanned_import_dependencies = scanned_import_dependencies
        self._entity_name = entity_name
        self._module_name = module_name
        self._unique_name = unique_name
        self._parent_file_result = parent_file_result
        self._scanned_inheritance_dependencies = []
        self._metrics: Dict = {}

    def __repr__(self):
        return f'''Entity result: {self.unique_name},
        entity name: {self.entity_name},
        tokens: {len(self.scanned_tokens)},
        import dependencies: {self._scanned_import_dependencies=},
        inheritance dependencies: {self._scanned_inheritance_dependencies=},
        scanned by: {self._scanned_by},
        module name: {self._module_name},
        metrics: {self.metrics=}'''

    @property
    def unique_name(self) -> str:
        return self._unique_name

    @unique_name.setter
    def unique_name(self, value):
        self._unique_name = value

    @property
    def analysis(self):
        return self._analysis

    @property
    def scanned_file_name(self) -> str:
        return self._scanned_file_name

    @property
    def absolute_name(self) -> str:
        return self._absolute_name

    @absolute_name.setter
    def absolute_name(self, value):
        self._absolute_name = value

    @property
    def display_name(self) -> str:
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value

    @property
    def scanned_by(self) -> str:
        return self._scanned_by

    @property
    def scanned_language(self) -> LanguageType:
        return self._scanned_language

    @property
    def scanned_tokens(self) -> List[str]:
        return self._scanned_tokens

    @property
    def scanned_import_dependencies(self) -> List[str]:
        return self._scanned_import_dependencies

    @scanned_import_dependencies.setter
    def scanned_import_dependencies(self, value):
        self._scanned_import_dependencies = value

    @property
    def entity_name(self) -> str:
        return self._entity_name

    @entity_name.setter
    def entity_name(self, value):
        self._entity_name = value

    @property
    def module_name(self) -> str:
        return self._module_name

    @module_name.setter
    def module_name(self, value):
        self._module_name = value

    @property
    def scanned_inheritance_dependencies(self) -> List:
        return self._scanned_inheritance_dependencies

    @scanned_inheritance_dependencies.setter
    def scanned_inheritance_dependencies(self, value):
        self._scanned_inheritance_dependencies = value

    @property
    def metrics(self) -> Dict:
        return self._metrics

    @metrics.setter
    def metrics(self, value):
        self._metrics = value

    @property
    def parent_file_result(self) -> AbstractFileResult:
        return self._parent_file_result

    @parent_file_result.setter
    def parent_file_result(self, value):
        self._parent_file_result = value


class FileResult(AbstractFileResult, AbstractParsingCore):
    """A FileResult is the most basic result type generated by a file scan. It contains the whole source code it could find within a file.
    """

    def __init__(self,
                 anaylsis,
                 scanned_file_name: str,
                 relative_file_path_to_analysis: str,
                 absolute_name: str,
                 display_name: str,
                 module_name: str,
                 scanned_by,
                 scanned_language,
                 scanned_tokens,
                 ):
        self._analysis = anaylsis
        self._scanned_file_name = scanned_file_name
        self._relative_file_path_to_analysis = relative_file_path_to_analysis
        self._relative_analysis_path = PosixPath(relative_file_path_to_analysis).parent
        self._absolute_name = absolute_name
        self._display_name = display_name
        self._unique_name = relative_file_path_to_analysis  # os.path.basename(os.path.normpath(self._scanned_file_name))
        self._module_name = module_name
        self._scanned_language = scanned_language
        self._scanned_by = scanned_by
        self._scanned_tokens = scanned_tokens
        self._scanned_import_dependencies = []
        self._metrics: Dict = {}

    def __repr__(self):
        return f'''File result: {self.unique_name},
        tokens: {len(self.scanned_tokens)},
        import dependencies: {self._scanned_import_dependencies=},
        scanned by: {self._scanned_by},
        module name: {self._module_name},
        metrics: {self._metrics=}'''

    @classmethod
    def create_file_result(cls, analysis, scanned_file_name, relative_file_path_to_analysis, absolute_name, display_name, module_name, scanned_by, scanned_language, scanned_tokens) -> 'FileResult':
        return FileResult(analysis, scanned_file_name, relative_file_path_to_analysis, absolute_name, display_name, module_name, scanned_by, scanned_language, scanned_tokens)

    @property
    def unique_name(self) -> str:
        return self._unique_name

    @unique_name.setter
    def unique_name(self, value):
        self._unique_name = value

    @property
    def analysis(self):
        return self._analysis

    @property
    def scanned_file_name(self) -> str:
        return self._scanned_file_name

    @property
    def relative_file_path_to_analysis(self) -> str:
        return self._relative_file_path_to_analysis

    @relative_file_path_to_analysis.setter
    def relative_file_path_to_analysis(self, value):
        self._relative_file_path_to_analysis = value

    @property
    def relative_analysis_path(self) -> str:
        return self._relative_analysis_path

    @property
    def module_name(self) -> str:
        return self._module_name

    @module_name.setter
    def module_name(self, value):
        self._module_name = value

    @property
    def scanned_by(self) -> str:
        return self._scanned_by

    @property
    def scanned_language(self) -> LanguageType:
        return self._scanned_language

    @property
    def scanned_tokens(self) -> List[str]:
        return self._scanned_tokens

    @property
    def scanned_import_dependencies(self) -> List[str]:
        return self._scanned_import_dependencies

    @scanned_import_dependencies.setter
    def scanned_import_dependencies(self, value):
        self._scanned_import_dependencies = value

    @property
    def metrics(self) -> Dict:
        return self._metrics

    @metrics.setter
    def metrics(self, value):
        self._metrics = value

    @property
    def absolute_name(self) -> str:
        return self._absolute_name

    @absolute_name.setter
    def absolute_name(self, value):
        self._absolute_name = value

    @property
    def display_name(self) -> str:
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value

    @staticmethod
    def _filter_source_tokens_without_comments(list_of_words: List[str], line_comment_string: str, start_comment_string: str, stop_comment_string: str) -> str:
        source = " ".join(list_of_words)
        source_lines = source.splitlines()
        source_lines_without_comments = []
        active_block_comment = False

        for line in source_lines:
            if start_comment_string in line:
                active_block_comment = True
                continue
            if stop_comment_string in line:
                active_block_comment = False
                continue
            if line.strip().startswith(line_comment_string):
                continue

            if not active_block_comment:
                source_lines_without_comments.append(line)

        return "\n".join(source_lines_without_comments)

    def generate_entity_results_from_scopes(self, entity_keywords, entity_expression, comment_keywords) -> List[EntityResult]:
        """Generate entity results by extracting everything within a scope that begins with an entity keyword."""
        open_scope_character: str = CoreParsingKeyword.OPENING_CURVED_BRACKET.value
        close_scope_character: str = CoreParsingKeyword.CLOSING_CURVED_BRACKET.value

        # TODO: make this configurable by parameters for language-specific reasons
        line_comment_keyword: str = comment_keywords[CoreParsingKeyword.LINE_COMMENT.value]
        start_block_comment_keyword: str = comment_keywords[CoreParsingKeyword.START_BLOCK_COMMENT.value]
        stop_block_comment_keyword: str = comment_keywords[CoreParsingKeyword.STOP_BLOCK_COMMENT.value]

        found_entities: Dict[str, List[str]] = {}
        created_entity_results: List[EntityResult] = []

        list_of_words_with_newline_strings = self.scanned_tokens
        source_string_no_comments = self._filter_source_tokens_without_comments(
            list_of_words_with_newline_strings, line_comment_keyword, start_block_comment_keyword, stop_block_comment_keyword)

        filtered_list_no_comments = self.preprocess_file_content_and_generate_token_list(source_string_no_comments)

        for _, obj, following in self._gen_word_read_ahead(filtered_list_no_comments):
            if obj in entity_keywords:
                read_ahead_string = self.create_read_ahead_string(obj, following)

                try:
                    parsing_result = entity_expression.parseString(read_ahead_string)
                except:
                    self.analysis.statistics.increment(Statistics.Key.PARSING_MISSES)
                    LOGGER.warning(f'warning: could not parse result {self=}')
                    LOGGER.warning(f'next tokens: {[obj] + following[:AbstractParsingCore.Constants.MAX_DEBUG_TOKENS_READAHEAD.value]}')
                    continue

                LOGGER.debug(f'entity definition found: {parsing_result.entity_name}')
                self.analysis.statistics.increment(Statistics.Key.PARSING_HITS)

                scope_level = 0
                found_entities[parsing_result.entity_name] = []
                all_tokens = [obj] + following
                for token in all_tokens:

                    if token == open_scope_character:
                        scope_level += 1

                    if token == close_scope_character:
                        scope_level -= 1
                        if scope_level == 0:
                            break

                    if parsing_result.entity_name in found_entities:
                        found_entities[parsing_result.entity_name].append(token)

        for entity_name, tokens in found_entities.items():

            unique_entity_name = self.absolute_name + "/" + entity_name
            entity_result = EntityResult(
                analysis=self.analysis,
                scanned_file_name=self.scanned_file_name,
                absolute_name=unique_entity_name,
                display_name=entity_name,
                scanned_by=self.scanned_by,
                scanned_language=self.scanned_language,
                scanned_tokens=tokens,
                scanned_import_dependencies=[],
                entity_name=entity_name,
                module_name=self.module_name,
                unique_name=entity_name,
                parent_file_result=self
            )

            created_entity_results.append(entity_result)
        return created_entity_results
