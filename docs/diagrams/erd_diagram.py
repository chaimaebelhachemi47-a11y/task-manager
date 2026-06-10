import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(10, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 9)
ax.axis('off')
fig.patch.set_facecolor('white')

# --- Entity box ---
entity_box = FancyBboxPatch(
    (2.5, 1.0), 5.0, 7.2,
    boxstyle="round,pad=0.1",
    linewidth=2.0,
    edgecolor='#2a6099',
    facecolor='white'
)
ax.add_patch(entity_box)

# --- Entity title background ---
title_box = FancyBboxPatch(
    (2.5, 7.2), 5.0, 1.0,
    boxstyle="round,pad=0.1",
    linewidth=0,
    edgecolor='#2a6099',
    facecolor='#2a6099'
)
ax.add_patch(title_box)

ax.text(5.0, 7.72, 'tasks',
        ha='center', va='center',
        fontsize=14, fontweight='bold', color='white')

# --- Columns ---
columns = [
    ('PK', 'id', 'INTEGER', '#fff2cc'),
    ('',   'title', 'TEXT NOT NULL', 'white'),
    ('',   'description', 'TEXT', 'white'),
    ('',   'priority', "TEXT DEFAULT 'Medium'", 'white'),
    ('',   'category', "TEXT DEFAULT 'General'", 'white'),
    ('',   'due_date', 'TEXT', 'white'),
    ('',   'due_time', 'TEXT', 'white'),
    ('',   'completed', 'INTEGER DEFAULT 0', 'white'),
    ('',   'created_at', 'TEXT DEFAULT datetime(now)', 'white'),
]

row_h = 0.68
start_y = 7.1

for i, (key, col, dtype, bg) in enumerate(columns):
    y = start_y - (i * row_h)
    # row background
    row_bg = FancyBboxPatch(
        (2.55, y - row_h + 0.05), 4.9, row_h - 0.05,
        boxstyle="square,pad=0",
        linewidth=0,
        facecolor=bg
    )
    ax.add_patch(row_bg)

    # divider
    ax.plot([2.55, 7.45], [y - row_h + 0.05, y - row_h + 0.05],
            color='#cccccc', linewidth=0.6)

    # key badge
    if key:
        badge = FancyBboxPatch(
            (2.65, y - row_h + 0.15), 0.45, 0.38,
            boxstyle="round,pad=0.03",
            linewidth=0.8,
            edgecolor='#b37400',
            facecolor='#fff2cc'
        )
        ax.add_patch(badge)
        ax.text(2.875, y - row_h + 0.34, key,
                ha='center', va='center',
                fontsize=7.5, fontweight='bold', color='#b37400')

    # column name
    ax.text(3.25, y - row_h/2, col,
            ha='left', va='center',
            fontsize=10, fontweight='bold', color='#222222')

    # data type
    ax.text(7.35, y - row_h/2, dtype,
            ha='right', va='center',
            fontsize=9, color='#555555')

# --- Title ---
ax.text(5.0, 8.7, 'Entity-Relationship Diagram — tasks table',
        ha='center', fontsize=13, fontweight='bold', color='#222222')

# --- Note ---
ax.text(5.0, 0.5,
        'PK = Primary Key   |   The system contains one entity: tasks',
        ha='center', fontsize=9, color='#777777', style='italic')

plt.tight_layout()
plt.savefig(
    r'C:\Users\chaim\Desktop\task-manager\docs\diagrams\erd_diagram.png',
    dpi=180, bbox_inches='tight', facecolor='white')
print("ERD diagram saved!")