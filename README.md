# Rhythm Theory Basics

A DAWless rhythm workbook in development. Practice one musical decision by ear, on live pads, in TR-REC, and in DOOM OS on the Roland SP-404MKII.

- [Practice course](PRACTICE.md) — a repeatable four-session routine, with musical tests from pulse to arrangement.
- [First listening lesson](pilot/kick-placement.html) and [printable card](pilot/kick-placement.pdf) — three original takes compare kick placement and duration. Open the HTML file in a browser with the adjacent `audio` folder.
- [First-edition publishing workflow](docs/first-edition-publishing-workflow.md) — manuscript, notation, audio, print, and interactive options.
- [Project backlog and writing skills](BACKLOG.md) — beginner questions, the six writing roles, and the next release checks.

The roles can be called by name in this project. Ask `$music-teacher` for a recall drill, `$roland-sp404mkii` to translate it between recording methods, or `$electronic-music-genre-specialist` for a sourced listening comparison.

The [pilot source](pilot/kick-placement.qmd) uses Quarto Markdown. To regenerate its guide tracks, run `python3 pilot/render_audio.py`. The supplied HTML and PDF are local proofs made from that source with markdown-it and PyMuPDF. The native Quarto render and the author's hardware takes are pending.

The GitHub preview runs only on request. Open **Actions → Build the pilot lesson → Run workflow**, choose the branch, and start the run. The workflow must be on the default branch, and the person starting it needs write access. [GitHub manual workflow runs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
