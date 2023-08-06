from alive_progress import alive_bar
from rich.progress import Progress


class probar:
    bar_options = ["smooth", "classic", "classic2", "brackets", "blocks", "bubbles", "solid", "checks", "circles",
                   "squares", "halloween", "filling", "notes", "ruler", "ruler2", "fish", "scuba"]

    def __init__(self, iterable, total_steps=None, dual_line=True, title=None, bar='smooth', force_tty=None):
        """
        bar: probar.bar_options
        """
        self.iterable = iterable
        if total_steps is None:
            try:
                total_steps = len(iterable)
                if not total_steps: total_steps = None
            except:
                total_steps = None
        self.total_steps = total_steps
        self.dual_line = dual_line
        # self.ctrl_c = ctrl_c
        self.title = title
        self.bar = bar
        self.force_tty = force_tty

    def __iter__(self):
        with alive_bar(
                self.total_steps,
                bar=self.bar,
                dual_line=self.dual_line,
                title=self.title,
                force_tty=self.force_tty
        ) as pbar:
            for idx, item in enumerate(self.iterable):
                yield item
                pbar()


class probar2:
    def __init__(self, iterable, total_steps=None, title=None):
        """
        """
        self.iterable = iterable
        if total_steps is None:
            try:
                total_steps = len(iterable)
                if not total_steps: total_steps = None
            except:
                total_steps = None
        self.total_steps = total_steps
        self.title = title

    def __iter__(self):
        with Progress() as progress:
            task = progress.add_task(self.title, total=self.total_steps)
            for idx, item in enumerate(self.iterable):
                yield item
                progress.update(task, advance=1)


if __name__ == "__main__":
    import time
    import threading


    def test1():
        def show():
            with Progress() as progress:
                task = progress.add_task('emmm', total=1000)
                for i in probar2(range(1000), title='Download'):
                    time.sleep(.005)
                    progress.update(task, advance=1)

        results = []
        for x in 1000, 1500, 700, 0:
            t = threading.Thread(target=show, )
            results.append(t)
            t.start()
        [i.join() for i in results]


    def test2():
        with Progress() as progress:
            task1 = progress.add_task("[red]Downloading...", total=1000)
            task2 = progress.add_task("[green]Processing...", total=100)
            task3 = progress.add_task("[cyan]Cooking...", total=1000)

            while not progress.finished:
                progress.update(task1, advance=0.5)
                progress.update(task2, advance=0.3)
                progress.update(task3, advance=0.9)
                time.sleep(0.02)


    # test1()
    # test2()

    def test3():
        from time import sleep

        from rich.live import Live
        from rich.panel import Panel
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
        from rich.table import Table

        job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        job1 = job_progress.add_task("[green]Cooking")
        job2 = job_progress.add_task("[magenta]Baking", total=200)
        job3 = job_progress.add_task("[cyan]Mixing", total=400)

        total = sum(task.total for task in job_progress.tasks)
        overall_progress = Progress()
        overall_task = overall_progress.add_task("All Jobs", total=int(total))

        progress_table = Table.grid()
        progress_table.add_row(
            Panel.fit(
                overall_progress, title="Overall Progress", border_style="green", padding=(2, 2)
            ),
            Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
        )

        with Live(progress_table, refresh_per_second=10):
            while not overall_progress.finished:
                sleep(0.1)
                for job in job_progress.tasks:
                    if not job.finished:
                        job_progress.advance(job.id)

                completed = sum(task.completed for task in job_progress.tasks)
                overall_progress.update(overall_task, completed=completed)


    test3()
