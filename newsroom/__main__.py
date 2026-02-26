"""CLI entry point — run with `python -m newsroom`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from newsroom.config import load_config, validate_config
from newsroom.pipeline import Pipeline
from newsroom.utils import setup_logging


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="newsroom",
        description="Newsroom — a pluggable news aggregation framework",
    )
    parser.add_argument(
        "-t", "--topic",
        required=True,
        help="Topic to search for (e.g. 'artificial intelligence')",
    )
    parser.add_argument(
        "-c", "--config",
        default="config.yaml",
        help="Path to YAML config file (default: config.yaml)",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["markdown", "json", "html", "plaintext"],
        default=None,
        help="Output format (overrides config file)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Write output to file instead of stdout",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    import logging
    setup_logging(logging.DEBUG if args.verbose else logging.INFO)
    logger = logging.getLogger("newsroom")

    try:
        config = load_config(args.config)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    issues = validate_config(config)
    for issue in issues:
        logger.warning("Config: %s", issue)

    pipeline = Pipeline(config)
    output = pipeline.run(args.topic, fmt=args.format)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        logger.info("Output written to %s", out_path)
    else:
        print(output)


if __name__ == "__main__":
    main()
