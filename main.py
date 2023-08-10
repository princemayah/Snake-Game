import pygame
import random

pygame.init()

# Colors
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# Display dimensions
dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

score_font = pygame.font.SysFont(None, 35)

high_score = 0
leaderboard = []

def initialize_leaderboard_entry(score, time):
  return {"score": score, "time": time, "games_played": 0}

def increment_games_played(leaderboard):
  for entry in leaderboard:
    entry["games_played"] += 1

def Your_score(score):
  highest_leaderboard_score = leaderboard[0]["score"] if leaderboard else 0
  score_text = f"Your Score: {score}   {'New High Score' if score > highest_leaderboard_score else 'High Score'}: {high_score}"
  score_render = score_font.render(score_text, True, yellow)
  dis.blit(score_render, [10, 10])

def show_timer(timer):
  timer_text = f"Time: {timer:.2f}"
  timer_render = score_font.render(timer_text, True, yellow)
  dis.blit(timer_render, [dis_width - timer_render.get_width() - 10, 10])

def show_leaderboard(leaderboard):
  dis.fill(black)
  leaderboard_text = "Leaderboard:"
  leaderboard_render = score_font.render(leaderboard_text, True, yellow)
  dis.blit(leaderboard_render, [10, 50])

  leaderboard.sort(key=lambda entry: (-entry["score"], entry["time"]))

  y_offset = 90
  for i, entry in enumerate(leaderboard[:10], start=1):
    entry_text = f"{i}. Score: {entry['score']} - Time: {entry['time']:.2f} seconds"
    entry_render = score_font.render(entry_text, True, yellow)
    dis.blit(entry_render, [10, y_offset])

    if entry['games_played'] == 0:
      new_entry_render = score_font.render("New Entry", True, green)
      dis.blit(new_entry_render, [entry_render.get_width() + 20, y_offset])

    y_offset += entry_render.get_height() + 5

def our_snake(snake_list):
  for x in snake_list:
    pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
  mesg = score_font.render(msg, True, color)
  dis.blit(mesg, [(dis_width - mesg.get_width()) / 2, 10])

def gameLoop():
  global high_score
  global leaderboard
  game_over = False
  game_close = False

  x1 = dis_width / 2
  y1 = dis_height / 2

  x1_change = 0
  y1_change = 0

  last_x_change = 0
  last_y_change = 0

  snake_List = []
  Length_of_snake = 1

  foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
  foody = round(random.randrange(25, dis_height - snake_block) / 10.0) * 10.0
    
  start_time = pygame.time.get_ticks()

  while not game_over:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        game_over = True
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and last_x_change != snake_block:
          x1_change = -snake_block
          y1_change = 0
        elif event.key == pygame.K_RIGHT and last_x_change != -snake_block:
          x1_change = snake_block
          y1_change = 0
        elif event.key == pygame.K_UP and last_y_change != snake_block:
          y1_change = -snake_block
          x1_change = 0
        elif event.key == pygame.K_DOWN and last_y_change != -snake_block:
          y1_change = snake_block
          x1_change = 0

    if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
      game_close = True
    x1 += x1_change
    y1 += y1_change
    dis.fill(black)
    pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
    snake_Head = [x1, y1]
    snake_List.append(snake_Head)
    if len(snake_List) > Length_of_snake:
      del snake_List[0]

    for x in snake_List[:-1]:
      if x == snake_Head:
        game_close = True

    our_snake(snake_List)
    Your_score(Length_of_snake - 1)

    current_time = (pygame.time.get_ticks() - start_time) / 1000
    show_timer(current_time)

    pygame.display.update()

    if x1 == foodx and y1 == foody:
      foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
      foody = round(random.randrange(50, dis_height - snake_block) / 10.0) * 10.0
      Length_of_snake += 1

      if Length_of_snake - 1 > high_score:
        high_score = Length_of_snake - 1

    last_x_change = x1_change
    last_y_change = y1_change

    clock.tick(snake_speed)

    if game_close:
      increment_games_played(leaderboard)
      leaderboard.append(initialize_leaderboard_entry(Length_of_snake - 1, current_time))
      leaderboard.sort(key=lambda entry: entry["score"], reverse=True)
            
      while game_close:
        show_leaderboard(leaderboard)
        message("You Lost! Press C-Play Again or Q-Quit", red)
        pygame.display.update()

        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
              game_over = True
              game_close = False
            if event.key == pygame.K_c:
              gameLoop()

  pygame.quit()
  quit()

gameLoop()
