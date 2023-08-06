#===============================================================================
# gtracks.py
#===============================================================================

"""Plot bigWig, bedGraph, or BED signal tracks and gene annotations in a
genomic region
"""




# Imports ======================================================================

import argparse
import gzip
import os
import os.path
import re
import subprocess
import seaborn as sns
import tempfile
from itertools import cycle




# Constants ====================================================================

BIGWIG_CONFIG_FORMAT = """
[{title}]
file = {file}
title = {title}
height = 2
color = {color}
min_value = 0
max_value = {max}
type = {plot_type}
overlay_previous = {overlay}
file_type = bigwig
"""

BEDGRAPH_CONFIG_FORMAT = """
[{title}]
file = {file}
title = {title}
height = 2
color = {color}
min_value = 0
max_value = {max}
type = {plot_type}
overlay_previous = {overlay}
file_type = bedgraph
"""

BED4_CONFIG_FORMAT = """
[{title}]
file = {file}
title = {title}
fontsize = 10
height = 1
file_type = bed
color = {color}
global_max_row = false
line_width = 1.5
labels = {labels}
"""

SPACER = """

[spacer]

"""

GENES_CONFIG_FORMAT = """
[genes]
file = {}
title = genes
fontsize = 10
height = {}
gene_rows = {}
"""

X_AXIS_CONFIG_FORMAT = """
[x-axis]
where = {}
"""

VLINES_CONFIG_FORMAT = """
[vlines]
file = {}
type = vlines
"""

HG19_GENES_PATH = os.path.join(os.path.dirname(__file__), 'hg19.bed12.bed.gz')
HG38_GENES_PATH = os.path.join(os.path.dirname(__file__), 'hg38.bed12.bed.gz')
SP9512_GENES_PATH = os.path.join(os.path.dirname(__file__),
                                 'sp9512.a02u1.bed12.bed.gz')
GENES_PATH = os.environ.get('GTRACKS_GENES_PATH', HG19_GENES_PATH)
COLOR_PALETTE = os.environ.get('GTRACKS_COLOR_PALETTE',
    ','.join(sns.color_palette().as_hex())).split(',')
TRACKS = os.environ.get('GTRACKS_TRACKS',
    os.path.join(os.path.dirname(__file__),
        'pancreatic_islet_atac_seq_ins_igf2.bw')).split(',')

COORD_REGEX = re.compile(os.environ.get('GTRACKS_COORD_REGEX',
                                        '([Cc]hr)?[0-9XY]+:[0-9]+-[0-9]+$'))
# ALT_COORD_REGEX = re.compile('[\s\S]+:[0-9]+-[0-9]+$')

GENOME_TO_GENES = {
    'GRCh38': HG38_GENES_PATH, 'hg38': HG38_GENES_PATH,
    'GRCh37': HG19_GENES_PATH, 'hg19': HG19_GENES_PATH,
    'Sp9512': SP9512_GENES_PATH
}

SP9512_EXAMPLE_REGION = '7:6975000-6989000'


# Functions ====================================================================

def make_tracks_file(
    *tracks,
    vlines_bed=None,
    genes=None,
    max=['auto'],
    plot_type=['fill'],
    overlay=False,
    color_palette=COLOR_PALETTE,
    genes_height=2,
    gene_rows=1,
    x_axis='top',

    bed_labels=False,
):
    X_AXIS_CONFIG = X_AXIS_CONFIG_FORMAT.format(x_axis)
    overlay_strs = ('no',)+(len(tracks)-1)*({True: 'share-y', False: 'no'}[overlay],)
    return (
        bool(x_axis == 'top') * X_AXIS_CONFIG
        + '\n'.join(
            BIGWIG_CONFIG_FORMAT.format(
                file=track, title=os.path.basename(track).split('.')[0] if not overlay else ' ',
                color=color, max=m, plot_type=pt, overlay=ov
            ) if track.endswith('.bw') else BEDGRAPH_CONFIG_FORMAT.format(
                file=track, title=os.path.basename(track).split('.')[0] if not overlay else ' ',
                color=color, max=m, plot_type=pt, overlay=ov
            ) if track.endswith('.bdg') else SPACER + BED4_CONFIG_FORMAT.format(
                file=track, title=os.path.basename(track).split('.')[0],
                color=color, labels='true' if bed_labels else 'false'
            ) if track.endswith('.bed') else ''
            for track, color, m, pt, ov in zip(tracks, cycle(color_palette),
                                           cycle(max), cycle(plot_type),
                                           overlay_strs)
        )
        + SPACER
        + bool(genes) * GENES_CONFIG_FORMAT.format(genes, genes_height, gene_rows)
        + bool(x_axis == 'bottom') * X_AXIS_CONFIG
        + bool(vlines_bed) * VLINES_CONFIG_FORMAT.format(vlines_bed)
    )


def generate_plot(region, tracks_file, output_file, width: int = 40):
    subprocess.run(
        (
            'pyGenomeTracks',
            '--tracks', tracks_file,
            '--region', region,
            '--outFileName', output_file,
            '--width', str(width)
        )
    )


def parse_region(region):
    chrom, start, end = region.replace('-', ':').split(':')
    return chrom, int(start), int(end)


def parse_gene(gene, genes_path=GENES_PATH):
    with gzip.open(genes_path, 'rt') as f:
        for line in f:
            parsed_line = line.split()
            if parsed_line[3] == gene:
                chrom, start, end = parsed_line[:3]
                break
        else:
            raise RuntimeError('gene not found')
    return chrom, int(start), int(end)


def gtracks(region, output, tracks=TRACKS, genes: str = 'GRCh38',
            flank: int = 0, color_palette=COLOR_PALETTE, max=None,
            plot_type=['fill'], overlay: bool = False, tmp_dir=None,
            width: int = 40, genes_height: int = 2, gene_rows: int = 1,
            x_axis: str = 'top', vlines_bed=None, bed_labels: bool = False,
            coord_regex=COORD_REGEX):
    if not any(output.endswith(ext) for ext in ('pdf', 'png', 'svg')):
        raise RuntimeError(
            'Please make sure the output file extension is pdf, png, or svg')
    if coord_regex.match(region):
        chrom, xmin, xmax = parse_region(region)
        xmin -= flank
        xmax += flank
    elif flank > 0:
        chrom, xmin, xmax = parse_gene(region, genes_path=genes)
        xmin -= flank
        xmax += flank
    else:
        chrom, start, end = parse_gene(region, genes_path=genes)
        center = (end + start) / 2
        xmin = int(center - 0.55 * (end - start))
        xmax = int(center + 0.55 * (end - start))
    with tempfile.NamedTemporaryFile(dir=tmp_dir) as temp_tracks:
        tracks_file = make_tracks_file(*tracks, vlines_bed=vlines_bed,
            genes=genes, max=(max or ['auto']), plot_type=plot_type,
            overlay=overlay, color_palette=color_palette,
            genes_height=genes_height, gene_rows=gene_rows, x_axis=x_axis,
            bed_labels=bed_labels)
        temp_tracks.write(tracks_file.encode())
        temp_tracks.seek(0)
        generate_plot(f'{chrom}:{xmin}-{xmax}', temp_tracks.name, output,
            width=width)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Plot bigWig, bedGraph, and BED signal tracks with gene annotations'
            'in a genomic region'
        )
    )
    parser.add_argument(
        'region',
        metavar='<{chr:start-end,GENE}>',
        help='coordinates or gene name to plot'
    )
    parser.add_argument(
        'track',
        metavar='<track.{bw,bdg,bed}>',
        nargs='*',
        default=TRACKS,
        help='bigWig, bedGraph, or bed files containing tracks'
    )
    parser.add_argument(
        'output',
        metavar='<path/to/output.{pdf,png,svg}>',
        help='path to output file'
    )
    parser.add_argument(
        '--genes',
        metavar='<{path/to/genes.bed.gz,GRCh37,GRCh38,hg19,hg38,Sp9512}>',
        default='GRCh38',
        help=(
            'compressed 6-column BED file or 12-column BED12 file containing '
            'gene annotations. Alternatively, providing a genome identifier '
            'will use one of the included gene tracks. (default: GRCh37)'
        )
    )
    parser.add_argument(
        '--flank',
        metavar='<int>',
        type=int,
        default=0,
        help='add flanks to the plotting region'
    )
    parser.add_argument(
        '--color-palette',
        metavar='<#color>',
        nargs='+',
        default=COLOR_PALETTE,
        help='color pallete for tracks'
    )
    parser.add_argument(
        '--max',
        metavar='<float>',
        type=float,
        nargs='+',
        help='max value of y-axis'
    )
    parser.add_argument(
        '--plot-type',
        metavar='<{"fill","line:lw","points:ms"}>',
        default=['fill'],
        nargs='+',
        help='plot type, either fill, line, or points (default: fill)'
    )
    parser.add_argument(
        '--overlay',
        action='store_true',
        help='Overlay plots instead of stacking them'
    )
    parser.add_argument(
        '--tmp-dir',
        metavar='<temp/file/dir>',
        help='directory for temporary files'
    )
    parser.add_argument(
        '--width',
        metavar='<int>',
        type=int,
        default=40,
        help='width of plot in cm (default: 40)'
    )
    parser.add_argument(
        '--genes-height',
        metavar='<int>',
        type=int,
        default=2,
        help='height of genes track (default: 2)'
    )
    parser.add_argument(
        '--gene-rows',
        metavar='<int>',
        type=int,
        default=1,
        help='number of gene rows (default: 1)'
    )
    parser.add_argument(
        '--x-axis',
        choices=('top', 'bottom', 'none'),
        default='top',
        help='where to draw the x-axis (default: top)'
    )
    parser.add_argument(
        '--vlines-bed',
        metavar='<path/to/vlines.bed>',
        help='BED file defining vertical lines'
    )
    parser.add_argument(
        '--bed-labels',
        action='store_true',
        help='include labels on BED tracks'
    )
    parser.add_argument(
        '--coord-regex',
        metavar="<regex>",
        type=re.compile,
        default=COORD_REGEX,
        help=f'regular expression indicating the format for coordinates (default: {COORD_REGEX.pattern})'
    )
    args = parser.parse_args()
    for t in args.track:
        if not any((t.endswith(ext) for ext in ('.bw', '.bdg', '.bed'))):
            raise RuntimeError(
                'track file extensions must be one of .bw, .bdg, or .bed')
    if args.genes in set(GENOME_TO_GENES.keys()):
        genes_path = GENOME_TO_GENES[args.genes]
        args.genes = genes_path
    return args


def main():
    args = parse_arguments()
    gtracks(args.region, args.output, tracks=args.track, genes=args.genes,
            flank=args.flank, color_palette=args.color_palette, max=args.max,
            plot_type=args.plot_type, overlay=args.overlay,
            tmp_dir=args.tmp_dir, width=args.width,
            genes_height=args.genes_height, gene_rows=args.gene_rows,
            x_axis=args.x_axis, vlines_bed=args.vlines_bed,
            bed_labels=args.bed_labels, coord_regex=args.coord_regex)
