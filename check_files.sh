#!/bin/bash

# 📁 Ścieżka do folderu z plikami
FOLDER="/Users/macbook/Desktop/Test"

# 📅 Pobierz datę jako argument
if [ -z "$1" ]; then
  echo "❗ Użycie: $0 RRRRMMDD (np. 20250806)"
  exit 1
fi

DATE_INPUT=$1

# 📃 Lista nazw bazowych plików (prefiksy)
FILES=(
  "check_exadata_cpu_"
  "zabbix_percenfilehba_"
  "zabbix_fibra_time_5m_"
  "win_infra_mem_sar_"
  "win_infra_spazifs_perfd_"
)

echo "📂 Sprawdzanie plików w folderze: $FOLDER"
echo "📅 Data wejściowa: $DATE_INPUT"
echo "----------------------------------------"

# 🔁 Iteracja po nazwach plików
for BASE in "${FILES[@]}"; do
  echo "🔍 Plik: ${BASE}*.rtf"
  
  for OFFSET in 1 2 3; do
    # ✅ PRAWIDŁOWE formatowanie daty (RRRRMMDD)
    CHECK_DATE=$(date -j -v-"$OFFSET"d -f "%Y%m%d" "$DATE_INPUT" +%Y%m%d)
    FILE="${FOLDER}/${BASE}${CHECK_DATE}.rtf"

    if [ -f "$FILE" ]; then
      SIZE=$(du -h "$FILE" | cut -f1)
      echo "✅ $CHECK_DATE → Rozmiar: $SIZE"
    else
      echo "❌ $CHECK_DATE → Brak pliku: $FILE"
    fi
  done

  echo ""
done

