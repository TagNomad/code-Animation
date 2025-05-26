import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.lines import Line2D
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(16, 9), facecolor='#001428')
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.set_aspect('equal')
ax.axis('off')

# 定义颜色
DEEP_BLUE = '#001428'
GOLD = '#FFD700'
LIGHT_BLUE = '#6495ED'
WHITE = '#FFFFFF'

# 科技里程碑数据
milestones = [
    {"name": "造纸术", "year": "105年", "x": 1.5, "y": 4},
    {"name": "印刷术", "year": "1041年", "x": 2.5, "y": 4},
    {"name": "火药", "year": "9世纪", "x": 3.5, "y": 4},
    {"name": "指南针", "year": "11世纪", "x": 4.5, "y": 4},
    {"name": "蒸汽机", "year": "1769年", "x": 6, "y": 4},
    {"name": "内燃机", "year": "1876年", "x": 7.5, "y": 4},
    {"name": "计算机", "year": "1946年", "x": 9, "y": 4},
    {"name": "人工智能", "year": "2020s", "x": 10.5, "y": 4}
]

# 创建标题
title = ax.text(6, 7, '人类科技进步之路', fontsize=36, color=GOLD, 
                ha='center', va='center', weight='bold')
subtitle = ax.text(6, 6.3, '从四大发明到人工智能', fontsize=24, color=WHITE,
                   ha='center', va='center')

# 创建时间轴
timeline = Line2D([0.5, 11.5], [4, 4], linewidth=3, color=GOLD, alpha=0.6)
ax.add_line(timeline)

# 存储所有图形对象
nodes = []
node_texts = []
year_texts = []
connections = []
particles = []

# 创建节点
for i, milestone in enumerate(milestones):
    # 创建节点圆圈
    node = Circle((milestone['x'], milestone['y']), 0.2, 
                  facecolor=DEEP_BLUE, edgecolor=GOLD, linewidth=2)
    ax.add_patch(node)
    nodes.append(node)
    
    # 创建节点文本
    text = ax.text(milestone['x'], milestone['y'] + 0.6, milestone['name'],
                   fontsize=14, color=WHITE, ha='center', va='bottom', alpha=0)
    node_texts.append(text)
    
    # 创建年份文本
    year = ax.text(milestone['x'], milestone['y'] - 0.6, milestone['year'],
                   fontsize=12, color=GOLD, ha='center', va='top', alpha=0)
    year_texts.append(year)
    
    # 创建连接线（除了第一个节点）
    if i > 0:
        prev = milestones[i-1]
        line = Line2D([prev['x'], milestone['x']], [prev['y'], milestone['y']],
                     linewidth=2, color=LIGHT_BLUE, alpha=0)
        ax.add_line(line)
        connections.append(line)

# 创建背景粒子
for _ in range(30):
    x = np.random.uniform(0, 12)
    y = np.random.uniform(0, 8)
    particle = Circle((x, y), 0.02, facecolor=LIGHT_BLUE, alpha=0.3)
    ax.add_patch(particle)
    particles.append(particle)

# 动画参数
frame_count = 0
active_nodes = []

def animate(frame):
    global frame_count, active_nodes
    frame_count = frame
    
    # 背景粒子动画
    for particle in particles:
        x, y = particle.center
        x += 0.02
        if x > 12:
            x = 0
            y = np.random.uniform(0, 8)
        particle.center = (x, y)
    
    # 激活节点的逻辑
    node_interval = 30  # 每30帧激活一个节点
    current_node_index = min(frame // node_interval, len(nodes) - 1)
    
    # 激活当前节点
    if current_node_index not in active_nodes and frame % node_interval == 0:
        active_nodes.append(current_node_index)
    
    # 更新所有激活的节点
    for idx in active_nodes:
        node = nodes[idx]
        text = node_texts[idx]
        year = year_texts[idx]
        
        # 节点脉动效果
        scale = 1 + 0.2 * np.sin(frame * 0.1 + idx)
        node.set_radius(0.2 * scale)
        node.set_facecolor(GOLD)
        
        # 显示文本
        text.set_alpha(1)
        year.set_alpha(1)
        
        # 显示连接线
        if idx > 0 and idx - 1 < len(connections):
            connections[idx - 1].set_alpha(0.8)
            
            # 数据流动效果
            progress = (frame % 20) / 20
            if progress < 0.5:
                connections[idx - 1].set_linewidth(2 + progress * 4)
            else:
                connections[idx - 1].set_linewidth(4 - (progress - 0.5) * 4)
    
    # 标题闪烁效果
    title.set_alpha(0.8 + 0.2 * np.sin(frame * 0.05))
    
    return nodes + node_texts + year_texts + connections + particles + [title, subtitle]

# 创建动画
anim = animation.FuncAnimation(fig, animate, frames=300, interval=50, 
                              repeat=True, blit=True)

# 保存动画为GIF（可选）
# anim.save('tech_evolution.gif', writer='pillow', fps=20)

# 显示动画
plt.tight_layout()
plt.show() 