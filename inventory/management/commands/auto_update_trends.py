"""
Management command: auto_update_trends
Runs as a long-lived background process that updates product trend scores
at a configurable interval (default: every 10 minutes).

Reuses update_all_trend_scores() from inventory/trend_calculator.py — no
logic is duplicated here.

Usage:
    python manage.py auto_update_trends                 # simulation mode, 10-min interval
    python manage.py auto_update_trends --use-ai        # AI mode  (requires API key)
    python manage.py auto_update_trends --interval 30   # custom interval in minutes
    python manage.py auto_update_trends --once          # run once and exit
"""

import time
import signal
import sys

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from inventory.trend_calculator import update_all_trend_scores

# Default interval between updates (seconds)
DEFAULT_INTERVAL_MINUTES = 10


class Command(BaseCommand):
    help = (
        "Continuously updates product trend scores at a set interval. "
        "Uses simulation by default; pass --use-ai to enable Google Gemini AI."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--interval",
            type=int,
            default=DEFAULT_INTERVAL_MINUTES,
            metavar="MINUTES",
            help=(
                f"Minutes between each trend-score update cycle "
                f"(default: {DEFAULT_INTERVAL_MINUTES})."
            ),
        )
        parser.add_argument(
            "--use-ai",
            action="store_true",
            default=False,
            help=(
                "Use Google Gemini AI for scoring instead of the built-in "
                "simulation. Requires a valid GOOGLE_API_KEY in config.py or "
                "the GOOGLE_API_KEY environment variable."
            ),
        )
        parser.add_argument(
            "--once",
            action="store_true",
            default=False,
            help="Run a single update cycle and exit immediately.",
        )

    # ------------------------------------------------------------------
    # Graceful shutdown support
    # ------------------------------------------------------------------
    def _setup_signal_handlers(self):
        """Register SIGINT / SIGTERM so the loop exits cleanly."""

        def _handler(signum, frame):  # noqa: ANN001
            self.stdout.write(
                self.style.WARNING("\nShutdown signal received — stopping after this cycle…")
            )
            self._running = False

        signal.signal(signal.SIGINT, _handler)
        signal.signal(signal.SIGTERM, _handler)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------
    def handle(self, *args, **options):
        interval_minutes: int = options["interval"]
        use_ai: bool = options["use_ai"]
        run_once: bool = options["once"]

        if interval_minutes < 1:
            raise CommandError("--interval must be at least 1 minute.")

        interval_seconds = interval_minutes * 60
        mode_label = "AI (Google Gemini)" if use_ai else "Simulation"

        self.stdout.write(
            self.style.SUCCESS(
                f"🚀  auto_update_trends started  |  Mode: {mode_label}  |  "
                f"Interval: {interval_minutes} min"
            )
        )
        if run_once:
            self.stdout.write("   (--once flag set — will exit after first cycle)")

        self._running = True

        if not run_once:
            self._setup_signal_handlers()

        cycle = 0
        while self._running:
            cycle += 1
            now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            self.stdout.write(f"\n[{now}]  Cycle #{cycle} — updating trend scores…")

            try:
                updated = update_all_trend_scores(force_ai=use_ai)
                self.stdout.write(
                    self.style.SUCCESS(f"   ✅  {updated} product(s) updated.")
                )
            except Exception as exc:  # noqa: BLE001
                self.stderr.write(
                    self.style.ERROR(f"   ❌  Error during update: {exc}")
                )

            if run_once:
                break

            if not self._running:
                break

            self.stdout.write(
                f"   ⏱  Next update in {interval_minutes} minute(s). "
                "Press Ctrl+C to stop."
            )

            # Sleep in short chunks so Ctrl+C is handled promptly
            for _ in range(interval_seconds):
                if not self._running:
                    break
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("\nauto_update_trends stopped cleanly. Goodbye!"))
