"""Progress tracking utilities for LuminoraCore CLI."""

import time
from typing import Optional, Callable, Any
from contextlib import contextmanager

from rich.console import Console
from rich.progress import Progress, TaskID, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich import get_console

from luminoracore_cli.utils.console import console


class ProgressTracker:
    """Progress tracker for CLI operations."""
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or get_console()
        self.progress = None
        self.task_id: Optional[TaskID] = None
    
    @contextmanager
    def track(self, description: str, total: int = 100):
        """Context manager for tracking progress."""
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            TimeElapsedColumn(),
            "•",
            TimeRemainingColumn(),
            console=self.console,
            transient=True
        ) as progress:
            self.progress = progress
            self.task_id = progress.add_task(description, total=total)
            yield self
    
    def update(self, advance: int = 1, description: Optional[str] = None) -> None:
        """Update progress."""
        if self.progress and self.task_id is not None:
            if description:
                self.progress.update(self.task_id, description=description)
            self.progress.update(self.task_id, advance=advance)
    
    def set_total(self, total: int) -> None:
        """Set total progress value."""
        if self.progress and self.task_id is not None:
            self.progress.update(self.task_id, total=total)
    
    def set_description(self, description: str) -> None:
        """Set progress description."""
        if self.progress and self.task_id is not None:
            self.progress.update(self.task_id, description=description)


class SimpleProgress:
    """Simple progress indicator without rich."""
    
    def __init__(self, total: int = 100, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self.last_update = 0
        self.update_interval = 0.1  # Update every 100ms
    
    def update(self, advance: int = 1, description: Optional[str] = None) -> None:
        """Update progress."""
        self.current += advance
        if description:
            self.description = description
        
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self._print_progress()
            self.last_update = current_time
    
    def _print_progress(self) -> None:
        """Print progress bar."""
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0
        bar_length = 30
        filled_length = int(bar_length * self.current // self.total) if self.total > 0 else 0
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        elapsed = time.time() - self.start_time
        
        # Estimate remaining time
        if self.current > 0 and self.current < self.total:
            remaining = (elapsed / self.current) * (self.total - self.current)
            remaining_str = f"ETA: {remaining:.1f}s"
        else:
            remaining_str = "Done"
        
        print(f"\r{self.description}: [{bar}] {percentage:6.1f}% ({self.current}/{self.total}) {elapsed:.1f}s {remaining_str}", end="", flush=True)
    
    def finish(self) -> None:
        """Finish progress and print newline."""
        self.current = self.total
        self._print_progress()
        print()  # Newline


def track_progress(description: str, total: int = 100, use_rich: bool = True):
    """Track progress with context manager."""
    if use_rich:
        tracker = ProgressTracker()
        return tracker.track(description, total)
    else:
        return SimpleProgress(total, description)


def with_progress(func: Callable, description: str = "Processing", use_rich: bool = True):
    """Decorator to add progress tracking to functions."""
    def wrapper(*args, **kwargs):
        with track_progress(description, use_rich=use_rich) as progress:
            return func(*args, progress=progress, **kwargs)
    return wrapper


class BatchProcessor:
    """Process items in batches with progress tracking."""
    
    def __init__(self, items: list, batch_size: int = 10, description: str = "Processing"):
        self.items = items
        self.batch_size = batch_size
        self.description = description
        self.total = len(items)
        self.processed = 0
    
    def process(self, processor: Callable, use_rich: bool = True) -> list:
        """Process items in batches."""
        results = []
        
        with track_progress(self.description, self.total, use_rich) as progress:
            for i in range(0, self.total, self.batch_size):
                batch = self.items[i:i + self.batch_size]
                batch_results = processor(batch)
                results.extend(batch_results)
                
                self.processed += len(batch)
                progress.update(len(batch), f"{self.description} ({self.processed}/{self.total})")
        
        return results


def create_progress_bar(total: int, description: str = "Processing") -> ProgressTracker:
    """Create a progress bar."""
    return ProgressTracker().track(description, total)


def show_spinner(description: str = "Processing..."):
    """Show a simple spinner."""
    import itertools
    import sys
    import threading
    import time
    
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    stop_spinner = threading.Event()
    
    def spin():
        while not stop_spinner.is_set():
            sys.stdout.write(f'\r{next(spinner)} {description}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f'\r✓ {description} Done!\n')
        sys.stdout.flush()
    
    spinner_thread = threading.Thread(target=spin)
    spinner_thread.start()
    
    return stop_spinner
