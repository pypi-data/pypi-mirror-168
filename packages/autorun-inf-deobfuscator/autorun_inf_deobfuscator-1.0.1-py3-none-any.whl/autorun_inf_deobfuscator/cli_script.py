import argparse
import os
from typing import List
import configparser
from cli_formatter.output_formatting import warning, error, info


class AutorunInfDeobfuscator:
    def __init__(self, path_to_file: str):
        self._deobfuscated_lines = AutorunInfDeobfuscator._load_ini_file_as_ascii(path_to_file=path_to_file)

    def get_content(self) -> str:
        return '\n'.join(self._deobfuscated_lines)

    def remove_comments(self):
        """ removes lines which start with an ';' as prefix """
        self._deobfuscated_lines = [line for line in self._deobfuscated_lines if not line.startswith(';')]

    def remove_empty_lines(self):
        self._deobfuscated_lines = [line for line in self._deobfuscated_lines if len(line) > 0]

    def return_sections(self) -> List[str]:
        """ returns a list of sections which are present in the INF file """
        config = configparser.RawConfigParser()
        config.read_string(self.get_content())
        return config.sections()

    def remove_junk_sections(self):
        """ remove junk sections which are not valid in an Windows INF file """
        config = configparser.RawConfigParser()
        config.read_string(self.get_content())

        possible_sections = {
            'autorun': 'Autorun',
            'content': 'Content',
            'exclusivecontentpaths': 'ExclusiveContentPaths',
            'ignorecontentpaths': 'IgnoreContentPaths',
            'deviceinstall': 'DeviceInstall'
        }

        new_lines = list()
        for section in config.sections():
            if section.lower() in possible_sections:
                new_name = possible_sections[section.lower()]
                new_lines.extend(AutorunInfDeobfuscator._section_to_lines(section_name=new_name, section_content=config[section]))
        self._deobfuscated_lines = new_lines

    @staticmethod
    def _section_to_lines(section_name: str, section_content: configparser.SectionProxy) -> List[str]:
        new_lines = list()
        new_lines.append('[{}]'.format(section_name))
        for key, value in section_content.items():
            new_lines.append('{key} = {value}'.format(key=key, value=value))
        return new_lines

    def fix_missing_section_brackets(self):
        """ adds a closing bracket ']' to sections where a closing bracket is missing """
        new_lines = list()
        for line in self._deobfuscated_lines:
            if line.startswith('['):
                while True:
                    before = len(line)
                    for stop_character in [' ', '\t']:
                        line = line.removesuffix(stop_character)
                    after = len(line)
                    if before == after:
                        break
                if not line.endswith(']'):
                    line = line + ']'
                new_lines.append(line)
            else:
                new_lines.append(line)
        self._deobfuscated_lines = new_lines

    @staticmethod
    def _load_ini_file_as_ascii(path_to_file: str) -> List[str]:
        """ loads the provided file and remove non ASCII characters """
        deobfuscated_lines = list()
        with open(path_to_file, mode='r', encoding='ASCII', errors='ignore') as file:
            file = ''.join([i for i in file.read() if 32 <= ord(i) < 128 or ord(i) == 10 or 160 < ord(i) <= 255])

            for line in file.split('\n'):
                formatted_line = line
                while True:
                    before = len(formatted_line)
                    for stop_character in [' ', '\t']:
                        formatted_line = formatted_line.removeprefix(stop_character)
                    after = len(formatted_line)
                    if before == after:
                        break
                deobfuscated_lines.append(formatted_line)
        return deobfuscated_lines


def main():
    argument_parser = argparse.ArgumentParser(usage='deobfuscate-autorun-inf [OPTION]... -i FILE', description='A cli script to deobfuscate obfuscated autorun.inf files as used by the Conficker / Downadup malware for example.')
    argument_parser.add_argument('-i', '--input', help="path to the eml-file (is required)", type=str)
    argument_parser.add_argument('--no-deobfuscation', dest='no_deobfuscation', action='store_true', default=False, help="No deobfuscation")
    argument_parser.add_argument('--remove-comments', dest='remove_comments', action='store_true', default=False, help="Remove comments")
    argument_parser.add_argument('--remove-empty-lines', dest='remove_empty_lines', action='store_true', default=False, help="Remove empty lines")
    argument_parser.add_argument('--fix-missing-brackets', dest='fix_missing_brackets', action='store_true', default=False, help="Fix missing section brackets")
    argument_parser.add_argument('--remove-junk-sections', dest='remove_junk_sections', action='store_true', default=False, help="Remove junk sections by filtering on the legitimate sections of an autorun.inf file")
    argument_parser.add_argument('--show-sections', dest='show_sections', action='store_true', default=False, help="Prints out only the name of the sections contained in the file")
    argument_parser.add_argument('-o', '--output', help="Writes the obfuscated file to the given file", type=str)

    arguments = argument_parser.parse_args()

    if arguments.input is None or len(arguments.input) == 0:
        warning('No input file specified')
        argument_parser.print_help()
        exit()

    # get the absolute path to the input file
    path_to_input = os.path.abspath(arguments.input)

    try:
        deobfuscator: AutorunInfDeobfuscator = AutorunInfDeobfuscator(path_to_file=path_to_input)
    except Exception as e:
        error('Error: {}'.format(e))
        error('File could not be loaded')
        info('Existing')
        return

    # use default functionality if no options are specified
    is_default_functionality = not (arguments.remove_comments or
                                    arguments.remove_empty_lines or
                                    arguments.fix_missing_brackets or
                                    arguments.remove_junk_sections or
                                    arguments.no_deobfuscation)

    if is_default_functionality:
        arguments.remove_comments = True
        arguments.remove_empty_lines = True
        arguments.fix_missing_brackets = True
        arguments.remove_junk_sections = True

    if arguments.remove_empty_lines:
        deobfuscator.remove_empty_lines()
    if arguments.remove_comments:
        deobfuscator.remove_comments()
    if arguments.fix_missing_brackets:
        deobfuscator.fix_missing_section_brackets()
    if arguments.remove_junk_sections:
        deobfuscator.remove_junk_sections()

    if arguments.show_sections:
        sections = deobfuscator.return_sections()
        info("inf-file contains {} sections".format(len(sections)))
        for section in sections:
            print("-", section)
    else:
        deobfuscated_content: str = deobfuscator.get_content()

        if arguments.output is not None:
            path_to_output = os.path.abspath(arguments.output)
            with open(path_to_output, mode='w') as output_file:
                output_file.write(deobfuscated_content)
            info('wrote {} lines to {}'.format(len(deobfuscated_content.split('\n')), path_to_output))
        else:
            print(deobfuscated_content)


if __name__ == '__main__':
    main()
