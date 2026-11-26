# Development Process

## Tools used

Python with Requests downloads the source CSV. Pandas reads dates and rainfall values, and Matplotlib exports the chart. The scripts use uv inline dependency metadata so their dependencies are explicit. Code and documentation corrections were made with Codex assistance.

## What is kept

1. The original `data/rainfall.csv` snapshot is preserved unchanged. Downloading and plotting remain separate steps.
2. The generated chart is committed at `out/rainfall_plot.png`, allowing reviewers to see the result without running Python.
3. Dates, units, source and missing-value conventions are stated alongside the output.

## Corrections made during review

The previous `plot.py` generated a sine-wave temperature series instead of reading rainfall observations. It has been replaced with CSV-based rainfall plotting, and its output now matches the README. The old temperature description was removed.

The downloader now uses the same `rainfall.csv` filename as the checked-in data and plotting script. The HTTP header name was corrected to the ASCII spelling `User-Agent`. Existing snapshots are reused rather than overwritten.

The original archive includes unavailable February 29 placeholders in non-leap years, such as 1900. Parsing removes those impossible dates while rejecting invalid dates that contain actual measurements.

The README's unclosed code fence was fixed, the directory listing is fenced, and the source URL now points directly to the rainfall dataset. Descriptions of data and output folders now reflect the committed files.

## Choices and rejected alternatives

- Keep unavailable and incomplete observations missing instead of replacing them with zero. Zero would incorrectly imply a confirmed dry day.
- Show trace rainfall as 0.025 mm, with an explicit note that the source only specifies less than 0.05 mm. These display values should not be interpreted as exact measurements.
- Prefer the latest full calendar year to a partial current year, while allowing `--year` for explicit comparisons.
- Keep the raw archive intact; perform cleaning in memory. A single station and year do not justify conclusions about all of Hong Kong or a long-term climate trend.

## Verification

Run the two commands in the README and confirm that the generated image shows rainfall, the selected year and millimetre units. Check that the original data file has no changes. Parsing rejects duplicate dates and unrecognised rainfall values. The course workflow checks the submitted repository structure; visual quality and the interpretation of the chart still require human review.
