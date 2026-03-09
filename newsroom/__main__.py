"""CLI entry point — run with `python -m newsroom`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from newsroom.config import load_config, validate_config
from newsroom.pipeline import Pipeline
from newsroom.utils import setup_logging


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="newsroom",
        description="Newsroom — a pluggable news aggregation framework",
    )
    sub = parser.add_subparsers(dest="command")

    # --- Default (run) command flags on the root parser ---
    parser.add_argument(
        "-t", "--topic",
        default=None,
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
    parser.add_argument(
        "--no-export",
        action="store_true",
        help="Skip all exporters (even if configured)",
    )

    # --- rewriter-setup subcommand ---
    rw_parser = sub.add_parser(
        "rewriter-setup",
        help="Manage the rewriter corpus and style analysis",
    )
    rw_parser.add_argument(
        "-c", "--config",
        default="config.yaml",
        help="Path to YAML config file (default: config.yaml)",
    )
    rw_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    rw_sub = rw_parser.add_subparsers(dest="rw_action")

    # rewriter-setup import
    imp_parser = rw_sub.add_parser("import", help="Import a WordPress WXR XML export")
    imp_parser.add_argument("xml_file", help="Path to the WordPress XML export file")
    imp_parser.add_argument(
        "--min-words", type=int, default=50,
        help="Minimum word count to include an article (default: 50)",
    )

    # rewriter-setup analyze
    analyze_parser = rw_sub.add_parser("analyze", help="Run style analysis on the corpus")
    analyze_parser.add_argument(
        "--use-batch", action="store_true", default=False,
        help="Use Anthropic Batch API (50%% cost savings, slower)",
    )
    analyze_parser.add_argument(
        "--resume", action="store_true", default=False,
        help="Resume from existing chunk analyses if available",
    )
    analyze_parser.add_argument(
        "--cost-estimate", action="store_true", default=False,
        help="Only estimate cost, do not run analysis",
    )

    # rewriter-setup stats
    rw_sub.add_parser("stats", help="Show corpus statistics")

    # --- gdrive-auth subcommand ---
    gd_parser = sub.add_parser(
        "gdrive-auth",
        help="Manage Google Drive OAuth2 authentication",
    )
    gd_parser.add_argument(
        "gd_action",
        choices=["login", "revoke", "status"],
        help="Action: login (authenticate), revoke (remove token), status (show token info)",
    )
    gd_parser.add_argument(
        "--credentials",
        default="credentials.json",
        help="Path to OAuth client secrets file (default: credentials.json)",
    )
    gd_parser.add_argument(
        "--token",
        default="token.json",
        help="Path to stored token file (default: token.json)",
    )

    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = _build_parser()
    return parser.parse_args(argv)


def _cmd_run(args: argparse.Namespace) -> None:
    """Run the main news aggregation pipeline."""
    if not args.topic:
        print("Error: --topic is required for the default pipeline.", file=sys.stderr)
        sys.exit(1)

    try:
        config = load_config(args.config)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    import logging
    logger = logging.getLogger("newsroom")

    if args.no_export:
        config["exporters"] = []

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


def _cmd_rewriter_setup(args: argparse.Namespace) -> None:
    """Handle rewriter-setup subcommands."""
    import logging
    logger = logging.getLogger("newsroom")

    try:
        config = load_config(args.config)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    rw_config = config.get("rewriter", {})

    from newsroom.rewriter.adapter import RewriterConfig

    settings = RewriterConfig(rw_config)

    if args.rw_action == "import":
        _rewriter_import(settings, args, logger)
    elif args.rw_action == "analyze":
        _rewriter_analyze(settings, args, logger)
    elif args.rw_action == "stats":
        _rewriter_stats(settings)
    else:
        print("Usage: python -m newsroom rewriter-setup {import,analyze,stats}", file=sys.stderr)
        sys.exit(1)


def _rewriter_import(settings, args, logger) -> None:
    """Import WordPress XML into the corpus."""
    from newsroom.rewriter.corpus.store import CorpusStore
    from newsroom.rewriter.importer.wordpress import parse_wxr

    xml_path = Path(args.xml_file)
    if not xml_path.exists():
        print(f"Error: file not found: {xml_path}", file=sys.stderr)
        sys.exit(1)

    store = CorpusStore(settings.db_path)
    try:
        articles = list(parse_wxr(xml_path, min_words=args.min_words))
        count = store.insert_articles_batch(articles)
        total = store.count_articles()
        logger.info("Imported %d new articles (%d total in corpus).", count, total)
        print(f"Imported {count} new articles ({total} total in corpus).")
    finally:
        store.close()


def _rewriter_analyze(settings, args, logger) -> None:
    """Run style analysis on the corpus."""
    from newsroom.rewriter.analyzer.examples import ExampleSelector
    from newsroom.rewriter.analyzer.style_extractor import StyleExtractor
    from newsroom.rewriter.corpus.store import CorpusStore

    store = CorpusStore(settings.db_path)
    try:
        extractor = StyleExtractor(settings, store)

        # Cost estimate only
        if getattr(args, "cost_estimate", False):
            est = extractor.estimate_cost()
            print(f"Sample size:       {est['sample_size']} articles")
            print(f"Chunks:            {est['n_chunks']}")
            print(f"Input tokens:      {est['total_input_tokens']:,}")
            print(f"Output tokens:     {est['total_output_tokens']:,}")
            print(f"Cost (Batch API):  ${est['estimated_cost_batch']:.2f}")
            print(f"Cost (Direct API): ${est['estimated_cost_direct']:.2f}")
            return

        # Step 1: Extract style guide
        use_batch = getattr(args, "use_batch", False)
        resume = getattr(args, "resume", False)
        guide = extractor.run(use_batch=use_batch, resume=resume)
        logger.info("Style guide version %d created.", guide.version)

        # Step 2: Build example clusters
        selector = ExampleSelector(settings, store)
        examples = selector.build_clusters()
        logger.info("Selected %d few-shot examples.", len(examples))

        print(f"Analysis complete: style guide + {len(examples)} examples.")
    finally:
        store.close()


def _rewriter_stats(settings) -> None:
    """Print corpus statistics."""
    from newsroom.rewriter.corpus.stats import compute_stats, print_stats
    from newsroom.rewriter.corpus.store import CorpusStore

    store = CorpusStore(settings.db_path)
    try:
        stats = compute_stats(store)
        print_stats(stats)
    finally:
        store.close()


def _cmd_gdrive_auth(args: argparse.Namespace) -> None:
    """Handle gdrive-auth subcommands."""
    from newsroom.gdrive_auth import get_drive_service, revoke_token, token_status

    if args.gd_action == "login":
        try:
            get_drive_service(args.credentials, args.token)
            print("Google Drive authentication successful. Token saved.")
        except ImportError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    elif args.gd_action == "revoke":
        try:
            ok = revoke_token(args.token)
            if ok:
                print("Token revoked and deleted.")
            else:
                print("No active token found.")
        except ImportError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    elif args.gd_action == "status":
        info = token_status(args.token)
        if info.get("authenticated"):
            print(f"Authenticated: yes")
            print(f"Token path:    {info['path']}")
            print(f"Scopes:        {', '.join(info.get('scopes', []))}")
            print(f"Client ID:     {info.get('client_id', 'unknown')}")
        else:
            print(f"Authenticated: no")
            print(f"Token path:    {info['path']}")
            if info.get("error"):
                print(f"Error:         {info['error']}")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    import logging
    setup_logging(logging.DEBUG if getattr(args, "verbose", False) else logging.INFO)

    if args.command == "rewriter-setup":
        _cmd_rewriter_setup(args)
    elif args.command == "gdrive-auth":
        _cmd_gdrive_auth(args)
    else:
        _cmd_run(args)


if __name__ == "__main__":
    main()
