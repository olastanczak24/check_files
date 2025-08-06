#!/bin/bash

# ========================================
#  File Checker Script for .csv files
# Checks existence and size of expected files
# for the 3 days prior to a given reference date.
# ========================================

# Path to the directory where files are stored
PATH=""

# Define the list of expected file name prefixes (editable)
EXPECTED_FILES=(
  "check_exadata_cpu_"
  "zabbix_percenfilehba_"
  "zabbix_fibra_time_5m_"
  "win_infra_mem_sar_"
  "win_infra_spazifs_perfd_"
)

# Input date (required) in format: YYYYMMDD
if [ -z "$1" ]; then
  echo "❗ Usage: $0 YYYYMMDD (e.g., 20250806)"
  exit 1
fi

DATE_INPUT=$1

# Display header
echo "Checking files in directory: $PATH"
echo "Reference date: $DATE_INPUT"
echo "----------------------------------------"

# Iterate over all expected file name prefixes
for PREFIX in "${EXPECTED_FILES[@]}"; do
  echo "Checking file type: ${PREFIX}*.csv"

  # Check for files from the 3 previous days
  for OFFSET in 1 2 3; do
    # Calculate date OFFSET days before the input date
    CHECK_DATE=$(date -j -v-"$OFFSET"d -f "%Y%m%d" "$DATE_INPUT" +%Y%m%d)

    # Build the full file path
    FILE="${PATH}/${PREFIX}${CHECK_DATE}.csv"

    #  Check if file exists and show size
    if [ -f "$FILE" ]; then
      SIZE=$(du -h "$FILE" | cut -f1)
      echo "$CHECK_DATE → Size: $SIZE"
    else
      echo "$CHECK_DATE → File not found: $FILE"
    fi
  done

  echo ""  # Blank line for readability
done
