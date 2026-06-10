import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
fig.patch.set_facecolor('white')

layers = [
    (1.0, 5.8, 8.0, 1.4, '#dce8f5', '#2a6099', 'Presentation Layer',
     'HTML  |  CSS  |  JavaScript'),
    (1.0, 3.6, 8.0, 1.4, '#d5e8d4', '#2d6a2d', 'Business Logic Layer',
     'Python  |  Flask  |  Routes  |  Validation'),
    (1.0, 1.4, 8.0, 1.4, '#fff2cc', '#b37400', 'Data Layer',
     'SQLite Database  |  SQL Queries'),
]

for (x, y, w, h, fcolor, tcolor, title, subtitle) in layers:
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.15",
                         linewidth=1.5,
                         edgecolor=tcolor,
                         facecolor=fcolor)
    ax.add_patch(box)
    ax.text(x + w/2, y + h*0.62, title,
            ha='center', va='center',
            fontsize=13, fontweight='bold', color=tcolor)
    ax.text(x + w/2, y + h*0.28, subtitle,
            ha='center', va='center',
            fontsize=10, color='#444444')

# Arrows between layers
arrow_props = dict(arrowstyle='->', color='#555555',
                   lw=1.5, connectionstyle='arc3,rad=0')
ax.annotate('', xy=(5, 5.78), xytext=(5, 5.02),
            arrowprops=arrow_props)
ax.annotate('', xy=(5, 3.58), xytext=(5, 2.82),
            arrowprops=arrow_props)

# Labels on arrows
ax.text(5.15, 5.4, 'HTTP Request / Response',
        ha='left', fontsize=9, color='#555555')
ax.text(5.15, 3.2, 'SQL Query / Result',
        ha='left', fontsize=9, color='#555555')

ax.text(5, 7.6, 'System Architecture — Three-Layer Model',
        ha='center', fontsize=14, fontweight='bold', color='#222222')

plt.tight_layout()
plt.savefig('architecture_diagram.png', dpi=180,
            bbox_inches='tight', facecolor='white')
print("Architecture diagram saved!")cd C:\Users\chaim\Desktop\task-manager\docs\diagrams
python architecture_diagram.py