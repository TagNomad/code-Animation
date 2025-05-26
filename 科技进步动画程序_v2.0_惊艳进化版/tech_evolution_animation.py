import pygame
import math
import random
import numpy as np
from datetime import datetime

# 初始化Pygame
pygame.init()

# 设置窗口大小
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("人类科技进步 - 从四大发明到人工智能")

# 定义颜色
DEEP_BLUE = (0, 20, 60)
GOLD = (255, 215, 0)
LIGHT_BLUE = (100, 149, 237)
WHITE = (255, 255, 255)
DARK_GOLD = (184, 134, 11)

# 字体设置
try:
    font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑字体路径
    title_font = pygame.font.Font(font_path, 48)
    subtitle_font = pygame.font.Font(font_path, 32)
    text_font = pygame.font.Font(font_path, 24)
except:
    # 如果找不到中文字体，使用默认字体
    title_font = pygame.font.Font(None, 48)
    subtitle_font = pygame.font.Font(None, 32)
    text_font = pygame.font.Font(None, 24)

# 科技里程碑
tech_milestones = [
    {"name": "造纸术", "year": "105", "era": "中国四大发明", "x": 100},
    {"name": "印刷术", "year": "1041", "era": "中国四大发明", "x": 200},
    {"name": "火药", "year": "9世纪", "era": "中国四大发明", "x": 300},
    {"name": "指南针", "year": "11世纪", "era": "中国四大发明", "x": 400},
    {"name": "蒸汽机", "year": "1769", "era": "工业革命", "x": 550},
    {"name": "内燃机", "year": "1876", "era": "第二次工业革命", "x": 700},
    {"name": "计算机", "year": "1946", "era": "信息时代", "x": 850},
    {"name": "人工智能", "year": "2020s", "era": "智能时代", "x": 1000}
]

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 100
        self.color = GOLD if random.random() > 0.5 else LIGHT_BLUE
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vx *= 0.98
        self.vy *= 0.98
        
    def draw(self, surface):
        alpha = self.life / 100
        radius = int(3 * alpha)
        if radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)

class DataFlow:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.progress = 0
        self.speed = random.uniform(0.01, 0.03)
        self.color = GOLD if random.random() > 0.5 else LIGHT_BLUE
        
    def update(self):
        self.progress += self.speed
        if self.progress > 1:
            self.progress = 0
            
    def draw(self, surface):
        if self.progress > 0:
            current_x = self.start_x + (self.end_x - self.start_x) * self.progress
            current_y = self.start_y + (self.end_y - self.start_y) * self.progress
            
            # 绘制流动的点
            pygame.draw.circle(surface, self.color, (int(current_x), int(current_y)), 3)
            
            # 绘制轨迹
            alpha = 1 - self.progress
            for i in range(5):
                trail_progress = self.progress - i * 0.05
                if trail_progress > 0:
                    trail_x = self.start_x + (self.end_x - self.start_x) * trail_progress
                    trail_y = self.start_y + (self.end_y - self.start_y) * trail_progress
                    radius = int(2 * (1 - i/5))
                    if radius > 0:
                        pygame.draw.circle(surface, self.color, (int(trail_x), int(trail_y)), radius)

class TechNode:
    def __init__(self, milestone, index):
        self.milestone = milestone
        self.x = milestone["x"]
        self.y = HEIGHT // 2
        self.radius = 20
        self.pulse = 0
        self.active = False
        self.index = index
        self.particles = []
        
    def activate(self):
        self.active = True
        # 创建爆发粒子效果
        for _ in range(20):
            self.particles.append(Particle(self.x, self.y))
            
    def update(self):
        if self.active:
            self.pulse = (self.pulse + 0.1) % (2 * math.pi)
            
        # 更新粒子
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
            
    def draw(self, surface):
        # 绘制节点光晕
        if self.active:
            glow_radius = self.radius + 10 * math.sin(self.pulse)
            for i in range(5):
                alpha = 50 - i * 10
                glow_color = (*GOLD, alpha) if i % 2 == 0 else (*LIGHT_BLUE, alpha)
                pygame.draw.circle(surface, glow_color[:3], (int(self.x), int(self.y)), 
                                 int(glow_radius + i * 5), 1)
        
        # 绘制节点
        color = GOLD if self.active else DARK_GOLD
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        
        # 绘制粒子
        for particle in self.particles:
            particle.draw(surface)
        
        # 绘制文字
        if self.active:
            name_text = text_font.render(self.milestone["name"], True, WHITE)
            name_rect = name_text.get_rect(center=(self.x, self.y - 40))
            surface.blit(name_text, name_rect)
            
            year_text = text_font.render(self.milestone["year"], True, GOLD)
            year_rect = year_text.get_rect(center=(self.x, self.y + 40))
            surface.blit(year_text, year_rect)

class TechEvolutionAnimation:
    def __init__(self):
        self.nodes = [TechNode(m, i) for i, m in enumerate(tech_milestones)]
        self.connections = []
        self.data_flows = []
        self.current_node = 0
        self.animation_time = 0
        self.background_particles = []
        
        # 创建背景粒子
        for _ in range(50):
            self.background_particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'speed': random.uniform(0.1, 0.5),
                'size': random.randint(1, 3)
            })
        
    def update(self):
        self.animation_time += 1
        
        # 每隔一段时间激活下一个节点
        if self.animation_time % 120 == 0 and self.current_node < len(self.nodes):
            self.nodes[self.current_node].activate()
            
            # 创建连接线和数据流
            if self.current_node > 0:
                prev_node = self.nodes[self.current_node - 1]
                curr_node = self.nodes[self.current_node]
                
                # 创建多条数据流
                for _ in range(3):
                    self.data_flows.append(DataFlow(
                        prev_node.x, prev_node.y,
                        curr_node.x, curr_node.y
                    ))
            
            self.current_node += 1
        
        # 更新所有节点
        for node in self.nodes:
            node.update()
        
        # 更新数据流
        for flow in self.data_flows:
            flow.update()
        
        # 更新背景粒子
        for particle in self.background_particles:
            particle['x'] += particle['speed']
            if particle['x'] > WIDTH:
                particle['x'] = 0
                particle['y'] = random.randint(0, HEIGHT)
    
    def draw_connections(self, surface):
        # 绘制节点之间的连接线
        for i in range(len(self.nodes) - 1):
            if self.nodes[i].active and self.nodes[i + 1].active:
                start_x = self.nodes[i].x
                start_y = self.nodes[i].y
                end_x = self.nodes[i + 1].x
                end_y = self.nodes[i + 1].y
                
                # 绘制渐变连接线
                for j in range(5):
                    alpha = 100 - j * 20
                    color = (*LIGHT_BLUE, alpha) if j % 2 == 0 else (*GOLD, alpha)
                    pygame.draw.line(surface, color[:3], 
                                   (start_x, start_y), (end_x, end_y), 3 - j // 2)
    
    def draw_background(self, surface):
        # 绘制背景粒子
        for particle in self.background_particles:
            pygame.draw.circle(surface, LIGHT_BLUE, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
    
    def draw_timeline(self, surface):
        # 绘制时间轴
        pygame.draw.line(surface, GOLD, (50, HEIGHT // 2), (WIDTH - 50, HEIGHT // 2), 2)
        
        # 绘制时间轴装饰
        for i in range(0, WIDTH, 50):
            y = HEIGHT // 2 + 5 * math.sin(self.animation_time * 0.01 + i * 0.01)
            pygame.draw.circle(surface, LIGHT_BLUE, (i, int(y)), 1)
    
    def draw_title(self, surface):
        # 绘制标题
        title_text = title_font.render("人类科技进步之路", True, GOLD)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        surface.blit(title_text, title_rect)
        
        # 绘制副标题
        subtitle_text = subtitle_font.render("从四大发明到人工智能", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 100))
        surface.blit(subtitle_text, subtitle_rect)
    
    def draw(self, surface):
        # 填充背景
        surface.fill(DEEP_BLUE)
        
        # 绘制背景效果
        self.draw_background(surface)
        
        # 绘制时间轴
        self.draw_timeline(surface)
        
        # 绘制连接线
        self.draw_connections(surface)
        
        # 绘制数据流
        for flow in self.data_flows:
            flow.draw(surface)
        
        # 绘制节点
        for node in self.nodes:
            node.draw(surface)
        
        # 绘制标题
        self.draw_title(surface)

# 主程序
def main():
    clock = pygame.time.Clock()
    animation = TechEvolutionAnimation()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # 重置动画
                    animation = TechEvolutionAnimation()
        
        # 更新动画
        animation.update()
        
        # 绘制
        animation.draw(screen)
        
        # 更新显示
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 