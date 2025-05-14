from bs4 import BeautifulSoup
import csv

# 1. Load the HTML
with open('data2.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

rows = []

# 2. Iterate over each PI panel
for panel in soup.find_all('mat-expansion-panel'):
    # Extract PI name (skip the 'account_circle' icon text)
    title = panel.find('mat-panel-title')
    if not title:
        continue
    parts = list(title.stripped_strings)
    pi = parts[1] if parts and parts[0] == 'account_circle' else ' '.join(parts)
    pi = pi.replace('Professor', 'Prof.')
    pi = ' '.join(pi.split())

    # 3. For each project under this PI
    for listing in panel.find_all('app-y4-project-select-listing'):
        h3 = listing.find('h3')
        if not h3:
            continue
        code_span = h3.find('span', class_='mat-body-strong mat-body-2')
        if not code_span:
            continue

        code = code_span.text.strip()
        # the text node right after the <span> is " - Project Name"
        name = code_span.next_sibling.strip().lstrip('- ').strip()
        name = ' '.join(name.split())
        division = code.split('-')[0]  # e.g. 'C' from 'C-tb508-1'

        rows.append({
            'PI': pi,
            'Code': code,
            'Name': name,
            'Division': division
        })

# 4. Write out the CSV
with open('projects2.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['PI', 'Code', 'Name', 'Division'])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} projects to projects2.csv")
