#!/usr/bin/env python3
"""Parse iiko products+groups → ~/DESU_MENU.md with Top-5 sales."""
import json
from collections import defaultdict

with open('/tmp/iiko_products.json') as f:
    products = json.load(f)
with open('/tmp/iiko_groups.json') as f:
    groups = json.load(f)

group_map = {g['id']: g for g in groups}
children_map = {}
for g in groups:
    p = g.get('parent')
    if p:
        children_map.setdefault(p, []).append(g['id'])

# Find Desu root
desu_root = None
for g in groups:
    if g['name'] == '[desu] меню 2026':
        desu_root = g['id']
        break

desu_group_ids = set()
def walk(gid):
    desu_group_ids.add(gid)
    for cid in children_map.get(gid, []):
        walk(cid)
walk(desu_root)

# ─── Build menu tree ───
lines = []
lines.append("# 🍜 Меню [desu] Лиговский 121")
lines.append("")
lines.append("> Структура меню из iikoServer. Цены из `defaultSalePrice` (0₽ = модификатор/ланч-компонент).")
lines.append("")

def fmt_price(p):
    return f"{int(p)}₽" if p else "—"

def build_tree(gid, depth=0):
    g = group_map.get(gid)
    if not g or g.get('deleted'):
        return
    name = g['name']
    prefix = "##" if depth == 0 else "#" * min(depth + 2, 6)
    prods = [p for p in products if p.get('parent') == gid and not p.get('deleted')]
    
    lines.append(f"{prefix} {name}")
    lines.append("")
    
    for p in sorted(prods, key=lambda x: x.get('position') or 0):
        pname = p['name']
        price = p.get('defaultSalePrice', 0)
        mods = p.get('modifiers', [])
        schema_id = p.get('modifierSchemaId')
        
        # Check for modifiers
        mod_note = ""
        if mods:
            mod_names = [m.get('name', '?') for m in mods[:5]]
            mod_prices = [f"{m.get('name','?')}={int(m.get('defaultSalePrice',0))}₽" for m in mods[:5]]
            mod_note = f" _модификаторы: {', '.join(mod_prices)}_"
        if schema_id:
            # Find schema name in groups
            schema_group = group_map.get(schema_id)
            if schema_group:
                mod_note += f" _схема: {schema_group['name']}_"
        
        if price > 0:
            lines.append(f"- **{pname}** — {fmt_price(price)}{mod_note}")
        else:
            lines.append(f"- {pname} — {fmt_price(price)}{mod_note}")
    
    lines.append("")
    
    # Recurse into child groups (sorted by num)
    child_ids = sorted(children_map.get(gid, []), key=lambda cid: group_map.get(cid, {}).get('num', ''))
    for cid in child_ids:
        build_tree(cid, depth + 1)

build_tree(desu_root)

# ─── Modifier schemas (groups under [all] Модификаторы) ───
mod_root = None
for g in groups:
    if g['name'] == '[all] Модификаторы':
        mod_root = g['id']
        break

if mod_root:
    lines.append("---")
    lines.append("")
    lines.append("## 🔧 Модификаторы")
    lines.append("")
    mod_child_ids = sorted(children_map.get(mod_root, []), key=lambda cid: group_map.get(cid, {}).get('num', ''))
    for cid in mod_child_ids:
        cg = group_map.get(cid)
        if not cg:
            continue
        lines.append(f"### {cg['name']}")
        lines.append("")
        mod_prods = [p for p in products if p.get('parent') == cid and not p.get('deleted')]
        for mp in sorted(mod_prods, key=lambda x: x.get('defaultSalePrice', 0)):
            lines.append(f"- **{mp['name']}** — {fmt_price(mp.get('defaultSalePrice', 0))}")
        lines.append("")

# ─── Top-5 ───
lines.append("---")
lines.append("")
lines.append("## 📊 Топ-5 продаж 14.07.2026")
lines.append("")
lines.append("| # | Блюдо | Кол-во | Выручка |")
lines.append("|---|-------|--------|---------|")
lines.append("| 1 | 🍜 Сио с лососем и креветками панко (4× XL) | 4 | 2 640 ₽ |")
lines.append("| 2 | 🍱 Ланч макси | 3 | 2 010 ₽ |")
lines.append("| 3 | 🍜 Сырный с курицей карааге (2×M + 1×XL) | 3 | 1 820 ₽ |")
lines.append("| 4 | 🍝 Якиудон с курицей лапша | 3 | 1 170 ₽ |")
lines.append("| 5 | 🍱 Ланч стандарт | 2 | 1 140 ₽ |")
lines.append("")

# ─── Menu stats ───
lines.append("---")
lines.append("")
lines.append("## 📈 Статистика меню")
lines.append("")
group_count = len(desu_group_ids)
prod_count = sum(1 for p in products if p.get('parent') in desu_group_ids and not p.get('deleted'))
lines.append(f"- **{group_count}** категорий")
lines.append(f"- **{prod_count}** товаров")
lines.append(f"- Рамены: обязательный модификатор размера (M / XL)")
lines.append(f"- Ланчи: 3 вида (макси, стандарт, мини) с выбором компонентов")
lines.append("")

with open('/home/simba87/DESU_MENU.md', 'w') as f:
    f.write('\n'.join(lines))

print(f"Written ~/DESU_MENU.md ({len(lines)} lines, {group_count} groups, {prod_count} products)")

# Print the tree summary for display
for line in lines:
    print(line)
