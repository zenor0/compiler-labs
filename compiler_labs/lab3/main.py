import sys
import os
import argparse
import logging

from rich import print
from rich.logging import RichHandler
from rich.columns import Columns
from rich.console import Console

from compiler_labs.lab3.models import *
from compiler_labs.lab3.utils import reader
from compiler_labs.lab2.utils.display import get_all_info
from compiler_labs.lab2.vis import render_parse_tree
from compiler_labs.lab2.middlewares import parse_source
from compiler_labs.lab2.models.lr0 import LR0
from compiler_labs.lab2.models.lr1 import LR1
from compiler_labs.lab2.models.slr1 import SLR1

from compiler_labs.lab3.models.semantic import top_down_traverse
from compiler_labs.lab3.utils.display import display_semantic_result

logger = logging.getLogger("rich")
logger.setLevel(logging.INFO)
rich_handler = RichHandler(rich_tracebacks=True)
logger.addHandler(rich_handler)

file_handler = logging.FileHandler("err-log.txt", mode="w")
file_handler.setLevel(logging.ERROR)
file_handler.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger.addHandler(file_handler)

tmp_path = "./tmp/"

console_width = 400
console = Console(record=True, width=console_width)


import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class WatchHandler(FileSystemEventHandler):
    def __init__(self, code_path, grammar_path, output_path):
        super().__init__()
        self.code_path = code_path
        self.grammar_path = grammar_path
        self.output_path = output_path
        self._modified_times = {}

        with open(grammar_path, "r") as f:
            grammar = f.read()
        self.semantic_productions, self.global_functions = reader.read_semantic_grammar(
            grammar
        )

    def on_modified(self, event):
        if event.is_directory:
            return
        current_modified_time = os.path.getmtime(event.src_path)
        if self._modified_times.get(event.src_path) == current_modified_time:
            return
        self._modified_times[event.src_path] = current_modified_time

        logger.info(f"File {event.src_path} has been modified")
        token_stream = tokenize_code(self.code_path)
        with open(tmp_path + "tokens.out", "w") as f:
            for token in token_stream:
                f.write(str(token) + "\n")

        with open(self.grammar_path, "r") as f:
            grammar = f.read()

        try:
            self.semantic_productions, self.global_functions = (
                reader.read_semantic_grammar(grammar)
            )
            stack_node, result_raw = semantic_parse(
                token_stream,
                self.semantic_productions,
                self.global_functions,
                True,
                output_path,
                True,
            )
            result = result_raw["output_result"]
            output = display_semantic_result(
                result["mem"].memory, result["code"], result["label"]
            )
            print(output)
        except Exception as e:
            logger.error(f"Error: {e}")
            
        logger.info("Grammar updated.")


def visualize_parse_tree(stack, grammar, output_path):
    logger.info("Visualizing parse tree...")
    html, _ = render_parse_tree(stack, grammar)
    with open(output_path + "parse_tree.html", "w") as f:
        f.write(html)
    logger.info("Parse tree saved to 'parse_tree.html'")


def tokenize_code(filename):
    with open(filename, "r") as f:
        code = f.read()
    return parse_source(code)[0]


def semantic_parse(
    code,
    semantic_productions,
    global_functions: dict,
    visualize=False,
    output_path="./outputs/",
    debug=False,
):
    result, stack = grammar.parse_node(code)

    if visualize:
        visualize_parse_tree(stack, grammar, output_path)

    top_down_traverse(stack[0], semantic_productions, global_functions)
    logger.info("Semantic parsing done.")

    exclude_key = ["__builtins__"]
    display_dict = {k: v for k, v in global_functions.items() if k not in exclude_key}
    # logger.info(f'Success, node info: {stack[0]}, global: {display_dict}')
    logger.info(display_dict["output_result"])
    return stack[0], display_dict


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Grammar Parser")

    ap.add_argument("filename", type=str, help="input grammar file")
    ap.add_argument("-m", "--mode", type=str, help="mode", default="lr1")
    ap.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="watch target file then parse in realtime",
    )
    ap.add_argument("-d", "--debug", action="store_true", help="debug mode")
    ap.add_argument(
        "-o", "--output-path", type=str, help="output file path", default="./outputs/"
    )
    ap.add_argument(
        "-s",
        "--source",
        type=str,
        help="Load source code file, pipe file into lexical parser, generate token stream then parse them with grammar parser.",
        default=False,
    )

    args = ap.parse_args()

    filename = args.filename
    mode = args.mode.lower()
    source_file = args.source
    output_path = args.output_path
    debug = args.debug
    mode = args.mode

    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("debug mode enabled.")
        logger.debug(f"Input file: {filename}")

    try:
        with open(filename, "r") as f:
            grammar_raw = f.read()
            logger.info(f"File '{filename}' loaded.")
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        sys.exit(1)

    productions = reader.read_semantic_grammar(grammar_raw, no_snippet=True)[0]
    match mode:
        case "lr0":
            grammar = LR0(productions)
        case "slr1":
            grammar = SLR1(productions)
        case "lr1":
            grammar = LR1(productions)
        case _:
            logger.error(f"Invalid mode: {mode}")
            sys.exit(1)

    logger.info("Parsing done.")
    if debug:
        info = get_all_info(grammar)
        console.print(info)
        console.save_text(output_path + "result.txt")
        

    if args.watch:
        path = "./tmp/input"

        event_handler = WatchHandler(source_file, filename, output_path)
        observer = Observer()
        observer.schedule(event_handler, source_file)
        observer.schedule(event_handler, filename)

        logger.info(f"Start monitoring '{filename}' and '{source_file}' for changes...")
        # logger.info(f"Start monitoring '{source_file}' for changes...")
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            sys.exit(0)

    semantic_productions, global_functions = reader.read_semantic_grammar(grammar_raw)
    semantic_parse(
        tokenize_code(source_file),
        semantic_productions,
        global_functions,
        True,
        output_path,
        debug,
    )

    logger.info("Done. Exiting...")
