import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(32, 22))
ax.set_xlim(0, 22)
ax.set_ylim(0, 16)
ax.axis('off')
fig.patch.set_facecolor('white')

def draw_class_box(ax, x, y, width, title, attributes, methods, title_color):
    row_h   = 0.52
    attr_h  = len(attributes) * row_h
    meth_h  = len(methods)    * row_h
    total_h = row_h + attr_h + 0.25 + meth_h + 0.25

    # outer box
    box = FancyBboxPatch(
        (x, y - total_h), width, total_h,
        boxstyle="round,pad=0.05",
        linewidth=2.0, edgecolor='#333333', facecolor='white')
    ax.add_patch(box)

    # title band
    title_box = FancyBboxPatch(
        (x, y - row_h), width, row_h,
        boxstyle="round,pad=0.05",
        linewidth=0, edgecolor=title_color, facecolor=title_color)
    ax.add_patch(title_box)

    ax.text(x + width/2, y - row_h/2, title,
            ha='center', va='center',
            fontsize=14, fontweight='bold', color='white')

    # attributes
    for i, attr in enumerate(attributes):
        ay = y - row_h - i*row_h - row_h/2
        ax.text(x + 0.18, ay, attr,
                ha='left', va='center', fontsize=12, color='#111111')

    # divider
    div_y = y - row_h - attr_h - 0.1
    ax.plot([x, x + width], [div_y, div_y],
            color='#aaaaaa', linewidth=1.2)

    # methods
    for i, meth in enumerate(methods):
        my = div_y - i*row_h - row_h/2
        ax.text(x + 0.18, my, meth,
                ha='left', va='center', fontsize=12,
                color='#222222', style='italic')

def arrow(ax, x1, y1, x2, y2, lbl, lbl_x, lbl_y):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#444444', lw=1.8))
    ax.text(lbl_x, lbl_y, lbl,
            fontsize=12, color='#555555', fontweight='bold')

# ── Task entity ──
draw_class_box(ax, 7.5, 15.5, 6.0,
    '<<Entity>>  Task',
    ['- id : INTEGER',
     '- title : TEXT',
     '- description : TEXT',
     '- priority : TEXT',
     '- category : TEXT',
     '- due_date : TEXT',
     '- due_time : TEXT',
     '- completed : INTEGER',
     '- created_at : TEXT'],
    ['+ to_dict() : dict'],
    '#2a6099')

# ── database module ──
draw_class_box(ax, 0.3, 10.5, 5.5,
    '<<Module>>  database',
    ['- DB_PATH : str'],
    ['+ get_connection() : Connection',
     '+ init_db() : void'],
    '#2d6a2d')

# ── models module ──
draw_class_box(ax, 7.5, 8.5, 6.0,
    '<<Module>>  models',
    [],
    ['+ create_task(...) : void',
     '+ get_all_tasks() : list',
     '+ get_task_by_id(id) : dict',
     '+ update_task(...) : void',
     '+ delete_task(id) : void',
     '+ toggle_complete(id) : void',
     '+ search_tasks(kw) : list',
     '+ filter_tasks(...) : list'],
    '#7b4fa6')

# ── app module ──
draw_class_box(ax, 15.2, 11.5, 6.2,
    '<<Module>>  app (Flask)',
    ['- app : Flask'],
    ['+ index() : Response',
     '+ add_task() : Response',
     '+ edit_task(id) : Response',
     '+ delete_task(id) : Response',
     '+ toggle_complete(id) : Response',
     '+ search() : Response',
     '+ filter_tasks() : Response',
     '+ calendar_view() : Response'],
    '#b37400')

# ── Arrows ──
# database → Task (creates)
arrow(ax, 5.8, 8.8, 7.5, 10.2, 'creates', 6.0, 9.6)

# models → database (uses)
arrow(ax, 7.5, 6.2, 5.8, 8.5, 'uses', 6.0, 7.5)

# models → Task (manages)
arrow(ax, 10.5, 8.5, 10.5, 10.2, 'manages', 10.6, 9.3)

# app → models (calls)
arrow(ax, 15.2, 7.5, 13.5, 6.8, 'calls', 14.0, 7.3)

ax.text(11.0, 15.8,
        'Class Diagram — Personal Task Manager',
        ha='center', fontsize=18, fontweight='bold', color='#111111')

plt.tight_layout()
plt.savefig('class_diagram.png', dpi=250,
            bbox_inches='tight', facecolor='white')
print("Class diagram saved!")