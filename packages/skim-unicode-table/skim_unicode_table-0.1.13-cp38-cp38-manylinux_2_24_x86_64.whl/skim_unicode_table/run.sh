#!/bin/bash

# get script's own location, which will also have all other executables
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

SKIM_CMD="$SCRIPT_DIR/sk"
RENDER_GLYPH_CMD="$SCRIPT_DIR/render-glyph"
PRINT_TABLE_CMD="$SCRIPT_DIR/print-unicode-table"

$PRINT_TABLE_CMD \
| $SKIM_CMD -n 1,2,3,4,5,6,7  -d '  ' --with-nth 1,2 \
--preview='echo {1} | '"$RENDER_GLYPH_CMD"' | viu -w 32 ; echo {2..}'
