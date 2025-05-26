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
RED = (255, 100, 100)
GREEN = (100, 255, 100)
ORANGE = (255, 165, 0)

# 字体设置
try:
    font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑字体路径
    title_font = pygame.font.Font(font_path, 48)
    subtitle_font = pygame.font.Font(font_path, 32)
    text_font = pygame.font.Font(font_path, 24)
    small_font = pygame.font.Font(font_path, 16)
except:
    # 如果找不到中文字体，使用默认字体
    title_font = pygame.font.Font(None, 48)
    subtitle_font = pygame.font.Font(None, 32)
    text_font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 16)

# 科技里程碑
tech_milestones = [
    {"name": "造纸术", "year": "105", "era": "中国四大发明", "x": 100, "icon": "paper"},
    {"name": "印刷术", "year": "1041", "era": "中国四大发明", "x": 200, "icon": "printing"},
    {"name": "火药", "year": "9世纪", "era": "中国四大发明", "x": 300, "icon": "gunpowder"},
    {"name": "指南针", "year": "11世纪", "era": "中国四大发明", "x": 400, "icon": "compass"},
    {"name": "蒸汽机", "year": "1769", "era": "工业革命", "x": 550, "icon": "steam"},
    {"name": "内燃机", "year": "1876", "era": "第二次工业革命", "x": 700, "icon": "engine"},
    {"name": "计算机", "year": "1946", "era": "信息时代", "x": 850, "icon": "computer"},
    {"name": "人工智能", "year": "2020s", "era": "智能时代", "x": 1000, "icon": "ai"}
]

class IconDrawer:
    """绘制各个时代的图标"""
    
    @staticmethod
    def draw_paper(surface, x, y, size, color):
        """绘制纸张图标"""
        # 绘制纸张轮廓
        rect = pygame.Rect(x - size//2, y - size//2, size, size * 1.4)
        pygame.draw.rect(surface, color, rect, 2)
        # 绘制纸张的折角
        corner_size = size // 4
        points = [
            (x + size//2, y - size//2),
            (x + size//2 - corner_size, y - size//2),
            (x + size//2, y - size//2 + corner_size)
        ]
        pygame.draw.polygon(surface, color, points, 2)
        # 绘制文字线条
        for i in range(3):
            line_y = y - size//4 + i * size//4
            pygame.draw.line(surface, color, (x - size//3, line_y), (x + size//3, line_y), 1)
    
    @staticmethod
    def draw_printing(surface, x, y, size, color):
        """绘制印刷术图标（印章）"""
        # 绘制印章外框
        pygame.draw.rect(surface, color, (x - size//2, y - size//2, size, size), 2)
        # 绘制印章内部的字符（简化为方块）
        inner_size = size // 3
        for i in range(2):
            for j in range(2):
                rect_x = x - size//3 + i * inner_size
                rect_y = y - size//3 + j * inner_size
                pygame.draw.rect(surface, color, (rect_x, rect_y, inner_size - 5, inner_size - 5))
    
    @staticmethod
    def draw_gunpowder(surface, x, y, size, color):
        """绘制火药图标（爆炸）"""
        # 绘制爆炸的星形
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            inner_r = size // 3
            outer_r = size // 1.5
            if angle % 60 == 0:
                r = outer_r
            else:
                r = inner_r
            end_x = x + r * math.cos(rad)
            end_y = y + r * math.sin(rad)
            pygame.draw.line(surface, color, (x, y), (end_x, end_y), 2)
        # 中心圆
        pygame.draw.circle(surface, color, (int(x), int(y)), size // 6)
    
    @staticmethod
    def draw_compass(surface, x, y, size, color):
        """绘制指南针图标"""
        # 外圆
        pygame.draw.circle(surface, color, (int(x), int(y)), size // 2, 2)
        # 指针
        needle_length = size // 2 - 5
        # 北针（红色部分）
        north_points = [
            (x, y - needle_length),
            (x - size//8, y),
            (x, y - size//8),
            (x + size//8, y)
        ]
        pygame.draw.polygon(surface, RED, north_points)
        # 南针
        south_points = [
            (x, y + needle_length),
            (x - size//8, y),
            (x, y + size//8),
            (x + size//8, y)
        ]
        pygame.draw.polygon(surface, color, south_points)
        # 中心点
        pygame.draw.circle(surface, color, (int(x), int(y)), 3)
    
    @staticmethod
    def draw_steam(surface, x, y, size, color):
        """绘制蒸汽机图标"""
        # 绘制锅炉
        boiler_rect = pygame.Rect(x - size//3, y - size//4, size//1.5, size//2)
        pygame.draw.rect(surface, color, boiler_rect, 2)
        # 绘制烟囱
        chimney_rect = pygame.Rect(x - size//6, y - size//2, size//6, size//4)
        pygame.draw.rect(surface, color, chimney_rect, 2)
        # 绘制蒸汽（云朵）
        for i in range(3):
            steam_y = y - size//2 - i * 10
            steam_x = x - size//12 + (i % 2) * 5
            pygame.draw.circle(surface, LIGHT_BLUE, (int(steam_x), int(steam_y)), 5, 1)
        # 绘制轮子
        wheel_y = y + size//4
        pygame.draw.circle(surface, color, (int(x - size//4), int(wheel_y)), size//6, 2)
        pygame.draw.circle(surface, color, (int(x + size//4), int(wheel_y)), size//6, 2)
    
    @staticmethod
    def draw_engine(surface, x, y, size, color):
        """绘制内燃机图标（活塞）"""
        # 绘制气缸
        cylinder_rect = pygame.Rect(x - size//4, y - size//2, size//2, size)
        pygame.draw.rect(surface, color, cylinder_rect, 2)
        # 绘制活塞
        piston_y = y - size//4
        piston_rect = pygame.Rect(x - size//5, piston_y, size//2.5, size//4)
        pygame.draw.rect(surface, color, piston_rect)
        # 绘制连杆
        pygame.draw.line(surface, color, (x, piston_y + size//8), (x, y + size//3), 3)
        # 绘制曲轴
        pygame.draw.circle(surface, color, (int(x), int(y + size//3)), size//8, 2)
    
    @staticmethod
    def draw_computer(surface, x, y, size, color):
        """绘制计算机图标"""
        # 显示器
        monitor_rect = pygame.Rect(x - size//2, y - size//2, size, size//1.5)
        pygame.draw.rect(surface, color, monitor_rect, 2)
        # 屏幕
        screen_rect = pygame.Rect(x - size//2 + 5, y - size//2 + 5, size - 10, size//2)
        pygame.draw.rect(surface, color, screen_rect, 1)
        # 底座
        pygame.draw.rect(surface, color, (x - size//6, y + size//6, size//3, size//8))
        pygame.draw.rect(surface, color, (x - size//4, y + size//4, size//2, size//10))
        # 屏幕上的代码线
        for i in range(3):
            line_y = y - size//3 + i * 10
            pygame.draw.line(surface, GREEN, (x - size//3, line_y), (x - size//6, line_y), 1)
            pygame.draw.line(surface, LIGHT_BLUE, (x - size//8, line_y), (x + size//6, line_y), 1)
    
    @staticmethod
    def draw_ai(surface, x, y, size, color):
        """绘制AI图标（神经网络）"""
        # 绘制神经网络节点
        node_positions = []
        layers = 3
        nodes_per_layer = [3, 4, 3]
        
        # 计算节点位置
        for layer in range(layers):
            layer_x = x - size//3 + layer * size//3
            num_nodes = nodes_per_layer[layer]
            layer_nodes = []
            for node in range(num_nodes):
                node_y = y - size//3 + node * (size*0.7) / (num_nodes - 1)
                layer_nodes.append((layer_x, node_y))
                # 绘制节点
                pygame.draw.circle(surface, color, (int(layer_x), int(node_y)), 4)
            node_positions.append(layer_nodes)
        
        # 绘制连接线
        for layer in range(layers - 1):
            for node1 in node_positions[layer]:
                for node2 in node_positions[layer + 1]:
                    pygame.draw.line(surface, LIGHT_BLUE, node1, node2, 1)

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
        self.icon_size = 60
        self.pulse = 0
        self.active = False
        self.index = index
        self.particles = []
        self.icon_drawer = IconDrawer()
        
    def activate(self):
        self.active = True
        # 创建爆发粒子效果
        for _ in range(30):
            self.particles.append(Particle(self.x, self.y))
            
    def update(self):
        if self.active:
            self.pulse = (self.pulse + 0.1) % (2 * math.pi)
            
        # 更新粒子
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
            
    def draw(self, surface):
        # 绘制光晕效果
        if self.active:
            glow_radius = self.icon_size // 2 + 10 * math.sin(self.pulse)
            for i in range(5):
                alpha = 50 - i * 10
                glow_color = (*GOLD, alpha) if i % 2 == 0 else (*LIGHT_BLUE, alpha)
                pygame.draw.circle(surface, glow_color[:3], (int(self.x), int(self.y)), 
                                 int(glow_radius + i * 5), 1)
        
        # 绘制图标背景
        bg_color = GOLD if self.active else DARK_GOLD
        bg_alpha = 255 if self.active else 128
        
        # 绘制半透明背景圆
        bg_surface = pygame.Surface((self.icon_size * 2, self.icon_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(bg_surface, (*DEEP_BLUE, 200), 
                         (self.icon_size, self.icon_size), self.icon_size // 2)
        surface.blit(bg_surface, (self.x - self.icon_size, self.y - self.icon_size))
        
        # 根据类型绘制图标
        icon_color = GOLD if self.active else DARK_GOLD
        icon_method = getattr(self.icon_drawer, f"draw_{self.milestone['icon']}")
        icon_method(surface, self.x, self.y, self.icon_size, icon_color)
        
        # 绘制粒子
        for particle in self.particles:
            particle.draw(surface)
        
        # 绘制文字
        if self.active:
            # 名称
            name_text = text_font.render(self.milestone["name"], True, WHITE)
            name_rect = name_text.get_rect(center=(self.x, self.y - self.icon_size - 20))
            surface.blit(name_text, name_rect)
            
            # 年份
            year_text = text_font.render(self.milestone["year"], True, GOLD)
            year_rect = year_text.get_rect(center=(self.x, self.y + self.icon_size + 20))
            surface.blit(year_text, year_rect)
            
            # 时代
            era_text = small_font.render(self.milestone["era"], True, LIGHT_BLUE)
            era_rect = era_text.get_rect(center=(self.x, self.y + self.icon_size + 40))
            surface.blit(era_text, era_rect)

class TechEvolutionAnimation:
    def __init__(self):
        self.nodes = [TechNode(m, i) for i, m in enumerate(tech_milestones)]
        self.connections = []
        self.data_flows = []
        self.current_node = 0
        self.animation_time = 0
        self.background_particles = []
        self.show_ending = False
        self.ending_alpha = 0
        
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
            
            # 如果所有节点都激活了，等待一段时间后显示结尾
            if self.current_node >= len(self.nodes):
                self.show_ending_timer = 180  # 3秒后显示结尾
        
        # 检查是否显示结尾
        if hasattr(self, 'show_ending_timer'):
            self.show_ending_timer -= 1
            if self.show_ending_timer <= 0:
                self.show_ending = True
                
        # 更新结尾画面的透明度
        if self.show_ending and self.ending_alpha < 255:
            self.ending_alpha = min(255, self.ending_alpha + 3)
        
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
    
    def draw_ending(self, surface):
        """绘制结尾致敬画面"""
        if self.show_ending:
            # 创建半透明黑色遮罩
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(int(self.ending_alpha * 0.8))
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            
            # 计算文字透明度
            text_alpha = int(self.ending_alpha)
            
            # 创建文字表面
            ending_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            
            # 主标题
            ending_text = title_font.render("致敬每一次不甘于平凡的创新", True, (*GOLD, text_alpha))
            ending_rect = ending_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            ending_surface.blit(ending_text, ending_rect)
            
            # 副标题
            subtitle1 = text_font.render("从古至今，人类文明的每一次飞跃", True, (*WHITE, text_alpha))
            subtitle1_rect = subtitle1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            ending_surface.blit(subtitle1, subtitle1_rect)
            
            subtitle2 = text_font.render("都源于那些敢于突破、勇于创新的伟大灵魂", True, (*WHITE, text_alpha))
            subtitle2_rect = subtitle2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            ending_surface.blit(subtitle2, subtitle2_rect)
            
            # 绘制装饰性的创新火花
            if text_alpha > 200:
                spark_count = 20
                for i in range(spark_count):
                    angle = (i / spark_count) * 2 * math.pi + self.animation_time * 0.01
                    radius = 200 + 50 * math.sin(self.animation_time * 0.02 + i)
                    x = WIDTH // 2 + radius * math.cos(angle)
                    y = HEIGHT // 2 + radius * math.sin(angle)
                    
                    spark_alpha = int((text_alpha - 200) * 2)
                    pygame.draw.circle(ending_surface, (*GOLD, spark_alpha), 
                                     (int(x), int(y)), 3)
                    
                    # 绘制连接线
                    if i % 3 == 0:
                        next_i = (i + 3) % spark_count
                        next_angle = (next_i / spark_count) * 2 * math.pi + self.animation_time * 0.01
                        next_x = WIDTH // 2 + radius * math.cos(next_angle)
                        next_y = HEIGHT // 2 + radius * math.sin(next_angle)
                        pygame.draw.line(ending_surface, (*LIGHT_BLUE, spark_alpha // 2),
                                       (int(x), int(y)), (int(next_x), int(next_y)), 1)
            
            # 绘制到主表面
            surface.blit(ending_surface, (0, 0))
    
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
        
        # 绘制结尾
        self.draw_ending(surface)

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