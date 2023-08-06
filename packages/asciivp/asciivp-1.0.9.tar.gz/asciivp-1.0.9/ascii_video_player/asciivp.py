import os
import sys
import argparse
from . import play


def main():
    desc = "\x1b[96;1mascii-vp\x1b[0m - Convert any video or GIF to ASCII play it in the terminal."
    eplg = "Project homepage on https://github.com/malkiAbdoo/ascii-vp"

    # get the arguments
    PARSER = argparse.ArgumentParser(prog="asciivp", description=desc, epilog=eplg)
    PARSER.add_argument('file', help="the file path or URL of a video or a GIF.")
    PARSER.add_argument('-r', '--replay', help="Replay the video automatically when the video ends.", action="store_true")
    PARSER.add_argument('-s', '--size', help="Set a size to the video.", type=str)
    PARSER.add_argument('-c', '--chars',  default=" .'~;icok0XN",type=str,
            help='characters depending on the grayscale value from black to white (default: "%(default)s")')
    ARGS = PARSER.parse_args()

    try:
	    play.play(path=ARGS.file, size=ARGS.size, replay=ARGS.replay, chars=ARGS.chars)
    except KeyboardInterrupt:
	    return

if __name__ == '__main__':
    main()

